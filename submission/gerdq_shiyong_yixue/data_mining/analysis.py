"""Summary-level re-analysis and data mining of the GerdQ high-altitude obesity study.

No individual patient data are available; every count used below is either
reported in the manuscript or reconstructed exactly from reported
percentages (each reconstruction is checked against the reported values).

Run:  python3 analysis.py      (writes results/ and figures/ next to this file)
"""

import json
import math
from pathlib import Path

import numpy as np
from scipy import stats
from scipy.optimize import milp, LinearConstraint, Bounds
import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib import font_manager

HERE = Path(__file__).resolve().parent
RES = HERE / "results"
FIG = HERE / "figures"
RES.mkdir(exist_ok=True)
FIG.mkdir(exist_ok=True)

for f in font_manager.findSystemFonts():
    if "NotoSansCJK" in f or "NotoSerifCJK" in f:
        font_manager.fontManager.addfont(f)
plt.rcParams["font.family"] = ["Noto Sans CJK SC", "Noto Serif CJK SC", "DejaVu Sans"]
plt.rcParams["axes.unicode_minus"] = False
plt.rcParams["savefig.dpi"] = 300

out = {}
audit = []


def check(name, reported, recomputed, tol, note=""):
    ok = abs(reported - recomputed) <= tol
    audit.append(dict(item=name, reported=reported, recomputed=round(recomputed, 4),
                      status="一致" if ok else "不一致", note=note))
    return ok


def wilson(k, n, z=1.959964):
    p = k / n
    d = 1 + z * z / n
    c = (p + z * z / (2 * n)) / d
    h = z * math.sqrt(p * (1 - p) / n + z * z / (4 * n * n)) / d
    return c - h, c + h


def chi2_2x2(a, b, c, d, yates):
    t = np.array([[a, b], [c, d]])
    r = stats.chi2_contingency(t, correction=yates)
    return r[0], r[1]


# ---------------------------------------------------------------------------
# 1. Reconstruct GerdQ total score x composite GERD table from Table 3/4
# ---------------------------------------------------------------------------
N_POS, N_NEG = 79, 24
cuts = [8, 9, 10, 11, 12]
sens = {8: 93.7, 9: 82.3, 10: 62.0, 11: 43.0, 12: 34.2}
spec = {8: 29.2, 9: 41.7, 10: 70.8, 11: 79.2, 12: 87.5}
ppv = {8: 81.3, 9: 82.3, 10: 87.5, 11: 87.2, 12: 90.0}
npv = {8: 58.3, 9: 41.7, 10: 36.2, 11: 29.7, 12: 28.8}

pos_ge = {c: round(sens[c] / 100 * N_POS) for c in cuts}
neg_ge = {c: N_NEG - round(spec[c] / 100 * N_NEG) for c in cuts}
pos_ge[7], neg_ge[7] = N_POS, N_NEG
for c in cuts:
    tp, fp = pos_ge[c], neg_ge[c]
    fn, tn = N_POS - tp, N_NEG - fp
    check(f"≥{c}分 灵敏度(%)", sens[c], 100 * tp / N_POS, 0.06)
    check(f"≥{c}分 特异度(%)", spec[c], 100 * tn / N_NEG, 0.06)
    check(f"≥{c}分 PPV(%)", ppv[c], 100 * tp / (tp + fp), 0.06)
    check(f"≥{c}分 NPV(%)", npv[c], 100 * tn / (tn + fn), 0.06)

bands = ["7", "8", "9", "10", "11", "≥12"]
edges = [7, 8, 9, 10, 11, 12]
pos_b = [pos_ge[e] - pos_ge.get(e + 1, 0) if e < 12 else pos_ge[12] for e in edges]
neg_b = [neg_ge[e] - neg_ge.get(e + 1, 0) if e < 12 else neg_ge[12] for e in edges]
tot_b = [p + n for p, n in zip(pos_b, neg_b)]
check("GerdQ≥8分人数", 91, sum(tot_b[1:]), 0)
out["score_table"] = dict(bands=bands, gerd_pos=pos_b, gerd_neg=neg_b, total=tot_b)

cum = np.cumsum(tot_b)
q = lambda p: edges[int(np.searchsorted(cum, p * 103, side="left"))]
out["score_quartiles_check"] = dict(Q1=q(0.25), median=q(0.5), Q3_lower_bound=q(0.75))


def grouped_auc(pos, neg):
    """Mann-Whitney AUC for ordinal grouped data (ties count 1/2)."""
    u = 0.0
    for i, p in enumerate(pos):
        below = sum(neg[:i])
        u += p * (below + 0.5 * neg[i])
    return u / (sum(pos) * sum(neg))


def delong_grouped(pos, neg):
    n1, n0 = sum(pos), sum(neg)
    v10, v01 = [], []
    for i in range(len(pos)):
        psi = (sum(neg[:i]) + 0.5 * neg[i]) / n0
        v10 += [psi] * pos[i]
    for j in range(len(neg)):
        psi = (sum(pos[j + 1:]) + 0.5 * pos[j]) / n1
        v01 += [psi] * neg[j]
    a = np.mean(v10)
    s = np.var(v10, ddof=1) / n1 + np.var(v01, ddof=1) / n0
    return a, math.sqrt(s)


def hanley_mcneil(a, n1, n0):
    q1, q2 = a / (2 - a), 2 * a * a / (1 + a)
    se = math.sqrt((a * (1 - a) + (n1 - 1) * (q1 - a * a) + (n0 - 1) * (q2 - a * a)) / (n1 * n0))
    return se


auc_g, se_g = delong_grouped(pos_b, neg_b)
check("AUC=U/(n₁n₀)（U=1 330）", 0.701, 1330 / (N_POS * N_NEG), 0.0006)
check("按重建分布计算的AUC", 0.701, auc_g, 0.012,
      "≥12分合并为一组，组内并列使AUC略低于原始数据")
se_hm = hanley_mcneil(0.701, N_POS, N_NEG)
out["auc"] = dict(reported=0.701, from_U=round(1330 / (N_POS * N_NEG), 4),
                  grouped=round(auc_g, 4),
                  delong_ci=[round(auc_g - 1.96 * se_g, 3), round(auc_g + 1.96 * se_g, 3)],
                  hanley_mcneil_ci=[round(0.701 - 1.96 * se_hm, 3), round(0.701 + 1.96 * se_hm, 3)])

# Stratum-specific likelihood ratios (SSLR) and post-test probabilities
def sslr(p, n):
    lr = (p / N_POS) / (n / N_NEG)
    se = math.sqrt(1 / p - 1 / N_POS + 1 / n - 1 / N_NEG)
    return lr, lr * math.exp(-1.96 * se), lr * math.exp(1.96 * se)


def post(pre, lr):
    o = pre / (1 - pre) * lr
    return o / (1 + o)


sslr_rows = []
merged = [("7分", [0]), ("8~9分", [1, 2]), ("≥10分", [3, 4, 5])]
for label, idx in merged:
    p = sum(pos_b[i] for i in idx)
    n = sum(neg_b[i] for i in idx)
    lr, lo, hi = sslr(p, n)
    sslr_rows.append(dict(band=label, gerd_pos=p, gerd_neg=n, n=p + n,
                          prob_in_cohort=round(p / (p + n), 3), lr=round(lr, 2),
                          lr_ci=[round(lo, 2), round(hi, 2)],
                          post_30=round(post(0.30, lr), 3), post_50=round(post(0.50, lr), 3),
                          post_767=round(post(0.767, lr), 3)))
out["sslr_bands"] = sslr_rows
single = []
for i, b in enumerate(bands):
    lr, lo, hi = sslr(pos_b[i], neg_b[i])
    single.append(dict(band=b, gerd_pos=pos_b[i], gerd_neg=neg_b[i],
                       prob=round(pos_b[i] / tot_b[i], 3), lr=round(lr, 2),
                       lr_ci=[round(lo, 2), round(hi, 2)]))
out["sslr_single"] = single

chi_trend = None
scores = np.array([7, 8, 9, 10, 11, 12.5])
props_n = np.array(tot_b)
xs = np.array(pos_b)
pbar = xs.sum() / props_n.sum()
tnum = (xs * scores).sum() - pbar * (props_n * scores).sum()
tden = pbar * (1 - pbar) * ((props_n * scores ** 2).sum() - (props_n * scores).sum() ** 2 / props_n.sum())
chi_trend = tnum ** 2 / tden
out["gerd_by_score_trend"] = dict(chi2=round(chi_trend, 2), p=round(stats.chi2.sf(chi_trend, 1), 4))

# LR+ / LR- at >=10
lrp = (49 / 79) / (7 / 24)
lrn = (30 / 79) / (17 / 24)
check("≥10分 阳性似然比", 2.13, lrp, 0.006)
check("≥10分 阴性似然比", 0.54, lrn, 0.006)

# ---------------------------------------------------------------------------
# 2. Endoscopy outcome and the endoscopy-negative subgroup
# ---------------------------------------------------------------------------
E_POS, E_NEG = 39, 64
e_pos_ge10 = round(0.718 * E_POS)
e_neg_lt10 = round(0.562 * E_NEG)
e_neg_ge10 = E_NEG - e_neg_lt10
check("胃镜异常 ≥10分 灵敏度(%)", 71.8, 100 * e_pos_ge10 / E_POS, 0.06)
check("胃镜异常 ≥10分 特异度(%)", 56.2, 100 * e_neg_lt10 / E_NEG, 0.06)
check("≥10分总人数（两种结局一致性）", pos_ge[10] + neg_ge[10], e_pos_ge10 + e_neg_ge10, 0)

ppi_pos_ge10 = pos_ge[10] - e_pos_ge10
ppi_neg_ge10 = neg_ge[10]
sub = np.array([[ppi_pos_ge10, 40 - ppi_pos_ge10], [ppi_neg_ge10, 24 - ppi_neg_ge10]])
or_sub, p_sub = stats.fisher_exact(sub)
out["endo_negative_subgroup"] = dict(
    n=64, ppi_pos=40, ppi_neg=24, table_ge10=sub.tolist(),
    sens=round(ppi_pos_ge10 / 40, 3), spec=round((24 - ppi_neg_ge10) / 24, 3),
    sens_ci=[round(x, 3) for x in wilson(ppi_pos_ge10, 40)],
    spec_ci=[round(x, 3) for x in wilson(24 - ppi_neg_ge10, 24)],
    odds_ratio=round(or_sub, 2), fisher_p=round(p_sub, 4))
ge10_rates = dict(endo_pos=(e_pos_ge10, E_POS), endo_neg_ppi_pos=(ppi_pos_ge10, 40),
                  endo_neg_ppi_neg=(ppi_neg_ge10, 24))
out["ge10_by_phenotype"] = {k: dict(k=v[0], n=v[1], pct=round(100 * v[0] / v[1], 1),
                                    ci=[round(100 * x, 1) for x in wilson(*v)])
                            for k, v in ge10_rates.items()}


def cochran_armitage(ks, ns, scores):
    ks, ns, scores = map(np.asarray, (ks, ns, scores))
    pb = ks.sum() / ns.sum()
    T = (ks * scores).sum() - pb * (ns * scores).sum()
    V = pb * (1 - pb) * ((ns * scores ** 2).sum() - (ns * scores).sum() ** 2 / ns.sum())
    z = T / math.sqrt(V)
    return z, 2 * stats.norm.sf(abs(z))


z10, p10 = cochran_armitage([v[0] for v in ge10_rates.values()], [v[1] for v in ge10_rates.values()], [2, 1, 0])
out["ge10_by_phenotype_trend"] = dict(z=round(z10, 2), p=round(p10, 4))

# PPI-test positives among endoscopy-abnormal patients
out["ppi_test_in_endo_pos"] = dict(total_ppi_pos=57, endo_neg_ppi_pos=40,
                                   implied_endo_pos_ppi_pos=57 - 40,
                                   pct_if_all_39_tested=round(100 * 17 / 39, 1))
for grp, (k, n, kk) in {"轻度": (34, 63, None), "中度": (13, 26, None), "重度": (10, 14, None)}.items():
    pass

# ---------------------------------------------------------------------------
# 3. Four-week response by diagnostic pathway
# ---------------------------------------------------------------------------
resp_e_pos = 33
resp_gerd = 59
resp_all = 72
resp_e_neg_ppi_pos = resp_gerd - resp_e_pos
resp_ppi_neg = resp_all - resp_gerd
check("GERD阴性者改善例数（72−59）", 13, resp_ppi_neg, 0)
check("GERD阴性者改善率(%)", 54.2, 100 * resp_ppi_neg / 24, 0.06)
phen = [("胃镜异常", resp_e_pos, 39), ("胃镜阴性+PPI试验阳性", resp_e_neg_ppi_pos, 40),
        ("胃镜阴性+PPI试验阴性", resp_ppi_neg, 24)]
rows = []
for name, k, n in phen:
    lo, hi = wilson(k, n)
    rows.append(dict(group=name, responders=k, n=n, pct=round(100 * k / n, 1),
                     ci=[round(100 * lo, 1), round(100 * hi, 1)]))
k = np.array([r["responders"] for r in rows])
n = np.array([r["n"] for r in rows])
sc = np.array([2, 1, 0])
pb = k.sum() / n.sum()
T = (k * sc).sum() - pb * (n * sc).sum()
V = pb * (1 - pb) * ((n * sc ** 2).sum() - (n * sc).sum() ** 2 / n.sum())
z_ca = T / math.sqrt(V)
out["response_by_phenotype"] = dict(rows=rows, cochran_armitage_z=round(z_ca, 2),
                                    p_trend=round(2 * stats.norm.sf(abs(z_ca)), 4))
chi_e, p_e = chi2_2x2(33, 6, 39, 25, True)
chi_e_u, p_e_u = chi2_2x2(33, 6, 39, 25, False)
check("胃镜异常×症状改善 χ²（连续性校正）", 5.38, chi_e, 0.02)
crude_or_e = (33 * 25) / (6 * 39)
out["endo_response"] = dict(crude_or=round(crude_or_e, 2), yates_chi2=round(chi_e, 2),
                            p=round(p_e, 4), uncorrected_chi2=round(chi_e_u, 2),
                            rate_pos=round(33 / 39, 3), rate_neg=round(39 / 64, 3),
                            rr=round((33 / 39) / (39 / 64), 2))
chi_g, p_g = chi2_2x2(59, 13, 20, 11, True)
check("GERD诊断×症状改善 χ²（连续性校正）", 2.77, chi_g, 0.02)

# Agreement between 14-day PPI test and 4-week response in endoscopy-negative patients
agree = np.array([[resp_e_neg_ppi_pos, 40 - resp_e_neg_ppi_pos],
                  [resp_ppi_neg, 24 - resp_ppi_neg]])
po = np.trace(agree) / agree.sum()
pe = (agree[0].sum() * agree[:, 0].sum() + agree[1].sum() * agree[:, 1].sum()) / agree.sum() ** 2
kappa = (po - pe) / (1 - pe)
se_k = math.sqrt(po * (1 - po) / (agree.sum() * (1 - pe) ** 2))
out["ppi_test_vs_4wk"] = dict(table=agree.tolist(), po=round(po, 3), kappa=round(kappa, 3),
                              kappa_ci=[round(kappa - 1.96 * se_k, 3), round(kappa + 1.96 * se_k, 3)],
                              ppi_pos_no_response=int(agree[0, 1]),
                              ppi_neg_response=int(agree[1, 0]))

# ---------------------------------------------------------------------------
# 4. Symptom-change mining
# ---------------------------------------------------------------------------
n_all = 103
check("4GerdQ均数=条目1+2+5+6均数之和", 6.11, 2.12 + 2.31 + 1.20 + 0.48, 0.006)
check("GerdQ总分均数=6条目均数之和", 10.06, 2.12 + 2.31 + 1.99 + 1.96 + 1.20 + 0.48, 0.006)
items = {"烧心": [0, 19, 53, 31], "反流": [0, 15, 41, 47], "上腹痛": [3, 20, 55, 25],
         "恶心": [1, 25, 54, 23], "睡眠障碍": [22, 48, 23, 10], "额外服药": [56, 45, 2, 0]}
item_sd = {}
for nm, cnt in items.items():
    v = np.repeat([0, 1, 2, 3], cnt)
    item_sd[nm] = v.std(ddof=1)
rep_mean = {"烧心": 2.12, "反流": 2.31, "上腹痛": 1.99, "恶心": 1.96, "睡眠障碍": 1.20, "额外服药": 0.48}
rep_sd = {"烧心": 0.69, "反流": 0.71, "上腹痛": 0.75, "恶心": 0.71, "睡眠障碍": 0.89, "额外服药": 0.54}
for nm, cnt in items.items():
    v = np.repeat([0, 1, 2, 3], cnt)
    check(f"{nm}条目均数（由频数表）", rep_mean[nm], v.mean(), 0.006)
    check(f"{nm}条目标准差（由频数表）", rep_sd[nm], v.std(ddof=1), 0.006)
var_items = sum(s ** 2 for s in item_sd.values())
alpha6 = 6 / 5 * (1 - var_items / 2.02 ** 2)
var4 = sum(item_sd[k] ** 2 for k in ["烧心", "反流", "睡眠障碍", "额外服药"])
alpha4 = 4 / 3 * (1 - var4 / 1.84 ** 2)
check("Cronbach α（6条目，由方差推算）", 0.281, alpha6, 0.01)
check("Cronbach α（4条目，由方差推算）", 0.515, alpha4, 0.01)
cov_sum6 = (2.02 ** 2 - var_items) / 2
cov_sum4 = (1.84 ** 2 - var4) / 2
mean_r4 = cov_sum4 / sum(item_sd[a] * item_sd[b] for i, a in enumerate(["烧心", "反流", "睡眠障碍", "额外服药"])
                          for b in ["烧心", "反流", "睡眠障碍", "额外服药"][i + 1:])
out["reliability"] = dict(alpha6=round(alpha6, 3), alpha4=round(alpha4, 3),
                          mean_interitem_r_4item=round(mean_r4, 3),
                          neg_items_baseline=round(10.06 - 6.11, 2),
                          neg_items_post=round(8.36 - 4.46, 2),
                          neg_items_change=round((10.06 - 6.11) - (8.36 - 4.46), 2))

mean_d, sd_d = 1.65, 1.67
t = mean_d / (sd_d / math.sqrt(n_all))
check("配对t值", 10.01, t, 0.05)
ci = stats.t.ppf(0.975, n_all - 1) * sd_d / math.sqrt(n_all)
check("下降值95%CI下限", 1.31, mean_d - ci, 0.015, "按两位小数均数/标准差推算，差0.01属舍入误差")
check("下降值95%CI上限", 1.99, mean_d + ci, 0.015, "同上")
for k_, n_, lo_, hi_ in [(72, 103, 60.5, 77.9), (31, 103, 22.1, 39.5), (8, 103, 4.0, 14.6),
                         (79, 103, 67.7, 83.8), (39, 103, 29.1, 47.5), (91, 103, 80.7, 93.2)]:
    lo, hi = wilson(k_, n_)
    check(f"Wilson 95%CI {k_}/{n_}", lo_, 100 * lo, 0.06)
    check(f"Wilson 95%CI {k_}/{n_}（上限）", hi_, 100 * hi, 0.06)

sum_d = round(mean_d * n_all)
sumsq_lo = (n_all - 1) * 1.665 ** 2 + sum_d ** 2 / n_all
sumsq_hi = (n_all - 1) * 1.675 ** 2 + sum_d ** 2 / n_all
resp_mean = sum_d / 72
resp_sd = math.sqrt(((sumsq_lo + sumsq_hi) / 2 - 72 * resp_mean ** 2) / 71)
check("各肥胖组下降值加权合计=总下降值", sum_d, 1.54 * 63 + 1.81 * 26 + 1.86 * 14, 1.0)
check("各肥胖组减重加权均数", 1.62, (1.43 * 63 + 2.06 * 26 + 1.68 * 14) / 103, 0.006)
check("改善组/未改善组减重加权均数", 1.62, (1.86 * 72 + 1.08 * 31) / 103, 0.006)


def bound_count(kmin, sense):
    """Min/max number of responders with a decrease >= kmin, given the reported
    count (72), sum (170) and sum of squares of decreases, with every
    non-responder at exactly 0 (Wilcoxon W=0, no worsening)."""
    ks = np.arange(1, 13)
    c = np.array([1.0 if k >= kmin else 0.0 for k in ks]) * (1 if sense == "min" else -1)
    cons = [LinearConstraint(np.ones(12), 72, 72),
            LinearConstraint(ks.astype(float), sum_d, sum_d),
            LinearConstraint((ks ** 2).astype(float), math.ceil(sumsq_lo), math.floor(sumsq_hi))]
    r = milp(c, constraints=cons, integrality=np.ones(12), bounds=Bounds(0, 72))
    if not r.success:
        return None
    return int(round(abs(r.fun)))


delta_bounds = {f"≥{k}": [bound_count(k, "min"), bound_count(k, "max")] for k in (2, 3, 4)}
out["delta_mining"] = dict(sum_decrease=sum_d, sum_sq_range=[round(sumsq_lo, 1), round(sumsq_hi, 1)],
                           responders_mean=round(resp_mean, 2), responders_sd=round(resp_sd, 2),
                           cohen_dz=round(mean_d / sd_d, 2), bounds=delta_bounds)

# ---------------------------------------------------------------------------
# 5. Weight loss and the logistic model
# ---------------------------------------------------------------------------
m1, s1, n1 = 1.86, 1.30, 72
m0, s0, n0 = 1.08, 0.80, 31
sp = math.sqrt(((n1 - 1) * s1 ** 2 + (n0 - 1) * s0 ** 2) / (n1 + n0 - 2))
g = (m1 - m0) / sp * (1 - 3 / (4 * (n1 + n0) - 9))
mp1, ms1, mp0, ms0 = 2.26, 1.55, 1.23, 0.92
spp = math.sqrt(((n1 - 1) * ms1 ** 2 + (n0 - 1) * ms0 ** 2) / (n1 + n0 - 2))
gp = (mp1 - mp0) / spp * (1 - 3 / (4 * (n1 + n0) - 9))
check("减重百分比均数≈减重/体重（总体）", 1.95, 100 * 1.62 / 84.94, 0.08,
      "比值的均数与均数之比不完全相等，差异可接受")


def evalue_or_common(or_):
    rr = math.sqrt(or_)
    return rr + math.sqrt(rr * (rr - 1)) if rr > 1 else 1.0


coef = {"减重幅度（每1 kg）": (0.597, 0.224), "胃镜异常": (1.164, 0.533)}
model = {}
for nm, (b, se) in coef.items():
    lo, hi = math.exp(b - 1.96 * se), math.exp(b + 1.96 * se)
    model[nm] = dict(or_=round(math.exp(b), 2), ci=[round(lo, 2), round(hi, 2)],
                     p=round(2 * stats.norm.sf(abs(b / se)), 4),
                     evalue=round(evalue_or_common(math.exp(b)), 2),
                     evalue_ci=round(evalue_or_common(lo), 2))
check("减重 OR", 1.82, math.exp(0.597), 0.006)
check("减重 OR 95%CI下限", 1.17, math.exp(0.597 - 1.96 * 0.224), 0.006)
check("减重 OR 95%CI上限", 2.82, math.exp(0.597 + 1.96 * 0.224), 0.006)
check("胃镜 OR", 3.20, math.exp(1.164), 0.006)
check("胃镜 OR 95%CI下限", 1.13, math.exp(1.164 - 1.96 * 0.533), 0.006)
check("胃镜 OR 95%CI上限", 9.10, math.exp(1.164 + 1.96 * 0.533), 0.03)
check("常数项 P", 0.334, 2 * stats.norm.sf(0.379 / 0.392), 0.002)
expit = lambda x: 1 / (1 + math.exp(-x))
check("列线图 最低概率（0 kg，胃镜阴性）", 0.41, expit(-0.379), 0.005)
check("列线图 最高概率（5 kg，胃镜异常）", 0.98, expit(-0.379 + 5 * 0.597 + 1.164), 0.005)
check("列线图 示例（2 kg+胃镜异常）概率", 0.88, expit(-0.379 + 2 * 0.597 + 1.164), 0.005)
check("列线图 减重每1 kg赋分", 51.3, 100 * 0.597 / 1.164, 0.05)

se_app = hanley_mcneil(0.728, 72, 31)
se_cor = hanley_mcneil(0.714, 72, 31)
out["model"] = dict(
    coefficients=model, epv=round(31 / 8, 2),
    weight_loss_hedges_g=round(g, 2), weight_pct_hedges_g=round(gp, 2),
    apparent_auc_ci_hm=[round(0.728 - 1.96 * se_app, 3), round(0.728 + 1.96 * se_app, 3)],
    corrected_auc_ci_hm=[round(0.714 - 1.96 * se_cor, 3), round(0.714 + 1.96 * se_cor, 3)],
    endo_neg_0kg_prob=round(expit(-0.379), 3),
    endo_pos_0kg_prob=round(expit(-0.379 + 1.164), 3),
    kg_to_match_endoscopy=round(1.164 / 0.597, 2))

# ---------------------------------------------------------------------------
# 6. Table 1 / Table 5 statistics
# ---------------------------------------------------------------------------
def chi_rxc(ks, ns):
    t = np.array([ks, [n - k for k, n in zip(ks, ns)]])
    return stats.chi2_contingency(t, correction=False)[:2]


for nm, ks, rep in [("男性", [38, 13, 4], 4.80), ("吸烟和（或）饮酒", [25, 7, 2], 3.92),
                    ("胃镜异常", [25, 10, 4], 0.61), ("PPI试验阳性", [34, 13, 10], 1.81),
                    ("GERD复合诊断", [48, 20, 11], 0.04)]:
    c2, _ = chi_rxc(ks, [63, 26, 14])
    check(f"表1 {nm} χ²", rep, c2, 0.03)
for nm, a, b, rep in [("男性", 41, 14, 0.78), ("吸烟和（或）饮酒", 26, 8, 0.63)]:
    c2, _ = chi2_2x2(a, 72 - a, b, 31 - b, True)
    check(f"表5 {nm} χ²（连续性校正）", rep, c2, 0.03)

# ---------------------------------------------------------------------------
# 7. Sample size for a confirmatory study
# ---------------------------------------------------------------------------
def n_for_precision(p, half_width):
    return math.ceil(1.959964 ** 2 * p * (1 - p) / half_width ** 2)


n_neg_spec = n_for_precision(0.30, 0.10)
n_pos_sens = n_for_precision(0.90, 0.05)
prev = 0.767
out["sample_size"] = dict(
    spec_30_pm10_neg=n_neg_spec, total_for_spec=math.ceil(n_neg_spec / (1 - prev)),
    sens_90_pm5_pos=n_pos_sens, total_for_sens=math.ceil(n_pos_sens / prev),
    validation_min_events=100, validation_total_at_30pct_nonresponse=math.ceil(100 / 0.301))

# ---------------------------------------------------------------------------
# Save
# ---------------------------------------------------------------------------
(RES / "results.json").write_text(json.dumps(out, ensure_ascii=False, indent=2))
import csv

with open(RES / "consistency_audit.csv", "w", newline="", encoding="utf-8-sig") as fh:
    w = csv.DictWriter(fh, fieldnames=["item", "reported", "recomputed", "status", "note"])
    w.writeheader()
    w.writerows(audit)
with open(RES / "reconstructed_score_by_gerd.csv", "w", newline="", encoding="utf-8-sig") as fh:
    w = csv.writer(fh)
    w.writerow(["GerdQ总分", "GERD复合诊断阳性", "GERD复合诊断阴性", "合计"])
    for row in zip(bands, pos_b, neg_b, tot_b):
        w.writerow(row)

# ---------------------------------------------------------------------------
# Figures
# ---------------------------------------------------------------------------
BLUE, RED, GREY = "#2b5b84", "#b8463c", "#8c8c8c"

fig, axes = plt.subplots(1, 2, figsize=(10, 4))
x = np.arange(len(bands))
axes[0].bar(x - 0.2, pos_b, 0.4, color=BLUE, label="GERD复合诊断阳性（n=79）")
axes[0].bar(x + 0.2, neg_b, 0.4, color=RED, label="GERD复合诊断阴性（n=24）")
axes[0].set_xticks(x, bands)
axes[0].set_xlabel("基线GerdQ总分（分）")
axes[0].set_ylabel("例数")
axes[0].legend(frameon=False, fontsize=8)
axes[0].set_title("A  按截断值表重建的评分分布", loc="left", fontsize=10)
for i in x:
    axes[0].text(i - 0.2, pos_b[i] + 0.4, pos_b[i], ha="center", fontsize=8)
    axes[0].text(i + 0.2, neg_b[i] + 0.4, neg_b[i], ha="center", fontsize=8)
lab = [r["band"] for r in sslr_rows]
lr = [r["lr"] for r in sslr_rows]
lo = [r["lr"] - r["lr_ci"][0] for r in sslr_rows]
hi = [r["lr_ci"][1] - r["lr"] for r in sslr_rows]
axes[1].errorbar(range(3), lr, yerr=[lo, hi], fmt="o", color=BLUE, capsize=4)
axes[1].axhline(1, color=GREY, ls="--", lw=0.8)
axes[1].set_yscale("log")
axes[1].set_yticks([0.1, 0.2, 0.5, 1, 2, 5], ["0.1", "0.2", "0.5", "1", "2", "5"])
axes[1].set_xticks(range(3), lab)
axes[1].set_xlim(-0.5, 2.5)
axes[1].set_ylabel("分层似然比（95%CI，对数刻度）")
for i, r in enumerate(sslr_rows):
    axes[1].text(i + 0.08, r["lr"], f"LR={r['lr']}\n验后概率{100 * r['prob_in_cohort']:.0f}%", fontsize=8, va="center")
axes[1].set_title("B  分层似然比", loc="left", fontsize=10)
fig.tight_layout()
fig.savefig(FIG / "图A_评分分布与分层似然比.png")
plt.close(fig)

fig, ax = plt.subplots(figsize=(4.6, 4.4))
tpr = [1] + [pos_ge[c] / N_POS for c in cuts] + [0]
fpr = [1] + [neg_ge[c] / N_NEG for c in cuts] + [0]
ax.plot(fpr, tpr, "-o", color=BLUE, ms=4)
for c in cuts:
    ax.annotate(f"≥{c}", (neg_ge[c] / N_NEG, pos_ge[c] / N_POS), textcoords="offset points",
                xytext=(6, -10), fontsize=8)
ax.plot([0, 1], [0, 1], ls="--", color=GREY, lw=0.8)
ax.set_xlabel("1−特异度")
ax.set_ylabel("灵敏度")
ax.set_title(f"重建ROC（分组AUC={auc_g:.3f}）", fontsize=10)
ax.set_aspect("equal")
fig.tight_layout()
fig.savefig(FIG / "图B_重建ROC曲线.png")
plt.close(fig)

fig, axes = plt.subplots(1, 2, figsize=(10, 4), gridspec_kw={"width_ratios": [1.4, 1]})
r = out["response_by_phenotype"]["rows"]
pct = [x["pct"] for x in r]
err = [[x["pct"] - x["ci"][0] for x in r], [x["ci"][1] - x["pct"] for x in r]]
axes[0].bar(range(3), pct, color=[BLUE, "#5f8fb8", RED], width=0.6)
axes[0].errorbar(range(3), pct, yerr=err, fmt="none", color="k", capsize=4, lw=0.8)
axes[0].set_xticks(range(3), ["胃镜异常\n（n=39）", "胃镜阴性\nPPI试验阳性（n=40）", "胃镜阴性\nPPI试验阴性（n=24）"], fontsize=8)
axes[0].set_ylabel("4周症状改善率（%，95%CI）")
axes[0].set_ylim(0, 100)
for i, x in enumerate(r):
    axes[0].text(i, 4, f"{x['responders']}/{x['n']}\n{x['pct']}%", ha="center", color="white", fontsize=9)
pt = out["response_by_phenotype"]["p_trend"]
axes[0].set_title(f"A  按诊断路径的症状改善率（趋势检验P={pt:.3f}）", loc="left", fontsize=10)
im = axes[1].imshow(agree, cmap="Blues")
for i in range(2):
    for j in range(2):
        axes[1].text(j, i, agree[i, j], ha="center", va="center", fontsize=14,
                     color="white" if agree[i, j] > 18 else "black")
axes[1].set_xticks([0, 1], ["4周改善", "4周未改善"])
axes[1].set_yticks([0, 1], ["PPI试验阳性", "PPI试验阴性"])
axes[1].set_title(f"B  胃镜阴性者两次疗效判断一致性（κ={kappa:.2f}）", loc="left", fontsize=10)
fig.tight_layout()
fig.savefig(FIG / "图C_诊断路径与疗效.png")
plt.close(fig)

fig, ax = plt.subplots(figsize=(5, 4.2))
pre = np.linspace(0.05, 0.95, 91)
for rr_, col in zip(sslr_rows, [RED, GREY, BLUE]):
    ax.plot(pre, [post(p, rr_["lr"]) for p in pre], color=col, label=f"GerdQ {rr_['band']}（LR={rr_['lr']}）")
ax.plot(pre, pre, ls="--", color="k", lw=0.6)
ax.axvline(0.767, color=GREY, lw=0.6, ls=":")
ax.text(0.775, 0.06, "本组验前\n概率76.7%", fontsize=8)
ax.set_xlabel("验前概率")
ax.set_ylabel("验后概率")
ax.legend(frameon=False, fontsize=8)
ax.set_title("不同验前概率下GerdQ分层的验后概率", fontsize=10)
fig.tight_layout()
fig.savefig(FIG / "图D_验前验后概率.png")
plt.close(fig)

n_bad = sum(a["status"] != "一致" for a in audit)
print(f"audit: {len(audit)} checks, {n_bad} inconsistent")
for a in audit:
    if a["status"] != "一致":
        print("  ", a)
print(json.dumps(out, ensure_ascii=False, indent=1))
