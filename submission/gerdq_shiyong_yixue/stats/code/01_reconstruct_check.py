"""Step 1: reconstruct exact counts from reported percentages and verify every reported statistic.

Outputs
  output/checks/reconstructed.json   reconstructed cross-tables used by steps 2 and 3
  output/checks/一致性核查.csv        each reported value, the recomputed value and the verdict
"""

import csv
import json
import math

import numpy as np
from scipy import stats

from common import CHK, chi2_rxc, grouped_auc_delong, load, wilson

D = load()
rows = []


def check(section, item, reported, recomputed, tol, method):
    ok = abs(reported - recomputed) <= tol
    rows.append([section, item, reported, round(recomputed, 4), "一致" if ok else "不一致", method])
    return ok


# ---------------------------------------------------------------------------
# A. GerdQ total score x composite GERD (from cut-off table)
# ---------------------------------------------------------------------------
dg = D["diagnosis"]
npos, nneg = dg["n_pos"], dg["n_neg"]
pos_ge = {7: npos}
neg_ge = {7: nneg}
for c, se, sp, ppv, npv, yj in zip(dg["cutoffs"], dg["sens"], dg["spec"], dg["ppv"], dg["npv"], dg["youden"]):
    tp = round(se / 100 * npos)
    tn = round(sp / 100 * nneg)
    fp, fn = nneg - tn, npos - tp
    pos_ge[c], neg_ge[c] = tp, fp
    s = "A 截断值表（原稿表4）"
    m = f"由灵敏度反推TP={tp}、由特异度反推TN={tn}"
    check(s, f"≥{c}分 灵敏度(%)", se, 100 * tp / npos, 0.05, m)
    check(s, f"≥{c}分 特异度(%)", sp, 100 * tn / nneg, 0.05, m)
    check(s, f"≥{c}分 阳性预测值(%)", ppv, 100 * tp / (tp + fp), 0.05, "TP/(TP+FP)")
    check(s, f"≥{c}分 阴性预测值(%)", npv, 100 * tn / (tn + fn), 0.05, "TN/(TN+FN)")
    check(s, f"≥{c}分 约登指数", yj, tp / npos + tn / nneg - 1, 0.0015, "灵敏度+特异度−1")

bands = ["7", "8", "9", "10", "11", "≥12"]
lows = [7, 8, 9, 10, 11, 12]
pos_b = [pos_ge[l] - pos_ge.get(l + 1, 0) if l < 12 else pos_ge[12] for l in lows]
neg_b = [neg_ge[l] - neg_ge.get(l + 1, 0) if l < 12 else neg_ge[12] for l in lows]
tot_b = [a + b for a, b in zip(pos_b, neg_b)]
assert min(pos_b + neg_b) >= 0
s = "A 截断值表（原稿表4）"
check(s, "GerdQ≥8分人数", D["general"]["gerdq_ge8"], sum(tot_b[1:]), 0, "重建分布中8分及以上例数之和")
cum = np.cumsum(tot_b)
med = lows[int(np.searchsorted(cum, 103 / 2))]
q1 = lows[int(np.searchsorted(cum, 103 / 4))]
check(s, "GerdQ总分中位数", 10, med, 0, "重建分布的中位数")
check(s, "GerdQ总分Q1", 9, q1, 0, "重建分布的下四分位数")
auc_u = dg["U"] / (npos * nneg)
check(s, "AUC（=U/(n₁n₀)）", dg["auc"], auc_u, 0.0006, "Mann-Whitney U=1330除以79×24")
auc_g, se_g = grouped_auc_delong(pos_b, neg_b)
check(s, "AUC（重建分布，≥12分合并）", dg["auc"], auc_g, 0.002, "≥12分合并为一组导致组内并列，故允许0.002误差")
lr_p = (pos_ge[10] / npos) / (neg_ge[10] / nneg)
lr_n = ((npos - pos_ge[10]) / npos) / ((nneg - neg_ge[10]) / nneg)
check(s, "≥10分 阳性似然比", dg["lr_pos_ge10"], lr_p, 0.005, "灵敏度/(1−特异度)")
check(s, "≥10分 阴性似然比", dg["lr_neg_ge10"], lr_n, 0.005, "(1−灵敏度)/特异度")

# Endoscopy outcome
e_pos, e_neg = D["general"]["endo_abnormal"], D["N"] - D["general"]["endo_abnormal"]
e_pos_ge10 = round(dg["endo_sens_ge10"] / 100 * e_pos)
e_neg_lt10 = round(dg["endo_spec_ge10"] / 100 * e_neg)
s = "B 胃镜异常为结局"
check(s, "≥10分 灵敏度(%)", dg["endo_sens_ge10"], 100 * e_pos_ge10 / e_pos, 0.05, f"反推{e_pos_ge10}/{e_pos}")
check(s, "≥10分 特异度(%)", dg["endo_spec_ge10"], 100 * e_neg_lt10 / e_neg, 0.05, f"反推{e_neg_lt10}/{e_neg}")
check(s, "两种结局下≥10分总人数相同", pos_ge[10] + neg_ge[10], e_pos_ge10 + (e_neg - e_neg_lt10), 0,
      "同一批患者，≥10分人数必须相等")

# ---------------------------------------------------------------------------
# C. Diagnostic pathway x 4-week response
# ---------------------------------------------------------------------------
r = D["response"]
resp_e = r["endo_abnormal"][0]
resp_g = r["gerd"][0]
resp_all = r["n"][0]
path_n = [e_pos, D["general"]["endo_neg_ppi_pos"], D["N"] - D["general"]["gerd_composite"]]
path_resp = [resp_e, resp_g - resp_e, resp_all - resp_g]
path_ge10 = [e_pos_ge10, pos_ge[10] - e_pos_ge10, neg_ge[10]]
s = "C 诊断路径"
check(s, "胃镜异常+胃镜阴性PPI阳性=GERD", D["general"]["gerd_composite"], path_n[0] + path_n[1], 0, "39+40")
check(s, "GERD阴性者改善率(%)（原稿讨论）", 54.2, 100 * path_resp[2] / path_n[2], 0.05, "(72−59)/24")
check(s, "GERD阳性者改善率(%)（原稿讨论）", 74.7, 100 * resp_g / 79, 0.05, "59/79")
check(s, "PPI试验阳性者中胃镜异常例数", D["general"]["ppi_test_pos_total"] - path_n[1], 17, 0, "57−40")

# ---------------------------------------------------------------------------
# D. Items and reliability
# ---------------------------------------------------------------------------
it = D["items"]
s = "D 条目（原稿表2）"
item_sd = {}
for nm in it["order"]:
    cnt = it["counts"][nm]
    v = np.repeat([0, 1, 2, 3], cnt)
    item_sd[nm] = v.std(ddof=1)
    check(s, f"{nm} 例数合计", 103, sum(cnt), 0, "四个分值例数之和")
    check(s, f"{nm} 均数", it["mean"][nm], v.mean(), 0.005, "由频数表计算")
    check(s, f"{nm} 标准差", it["sd"][nm], v.std(ddof=1), 0.005, "由频数表计算（n−1）")
check(s, "6条目均数之和=总分均数", it["total_mean_sd"][0], sum(it["mean"].values()), 0.005, "加和")
pos4 = ["烧心", "反流", "睡眠障碍", "额外服药"]
check(s, "4条目均数之和=4GerdQ均数", D["groups"]["gerdq4_total"][0], sum(it["mean"][k] for k in pos4), 0.005, "加和")
alpha6 = 6 / 5 * (1 - sum(x ** 2 for x in item_sd.values()) / it["total_mean_sd"][1] ** 2)
alpha4 = 4 / 3 * (1 - sum(item_sd[k] ** 2 for k in pos4) / D["groups"]["gerdq4_total"][1] ** 2)
check(s, "Cronbach α（6条目）", it["cronbach_alpha_6"], alpha6, 0.01, "k/(k−1)×(1−Σ条目方差/总分方差)")
check(s, "Cronbach α（4条目）", it["cronbach_alpha_4"], alpha4, 0.01, "同上")

# ---------------------------------------------------------------------------
# E. Table 1 and Table 6 chi-square tests
# ---------------------------------------------------------------------------
g = D["groups"]
s = "E 卡方检验（原稿表1、表6）"
TOTALS = dict(male=55, smoke_drink=34, endo_abnormal=39, ppi_test_pos=57, gerd=79)
for key, label in [("male", "男性"), ("smoke_drink", "吸烟和（或）饮酒"), ("endo_abnormal", "胃镜异常"),
                   ("ppi_test_pos", "PPI试验阳性"), ("gerd", "GERD复合诊断")]:
    k = g[key]
    tab = [k, [n - x for n, x in zip(g["n"], k)]]
    c2, p, _ = chi2_rxc(tab)
    check(s, f"表1 {label} χ²", g[f"{key}_chi2"], c2, 0.02, "3×2表Pearson χ²（不校正）")
    check(s, f"表1 {label} P", g[f"{key}_P"], p, 0.002, "同上")
    check(s, f"表1 {label} 三组合计=合计列", TOTALS[key], sum(k), 0, "三组例数相加")
for key, label in [("male", "男性"), ("smoke_drink", "吸烟和（或）饮酒"), ("endo_abnormal", "胃镜异常"), ("gerd", "GERD复合诊断")]:
    a, b, chi_rep, p_rep = r[key]
    tab = [[a, r["n"][0] - a], [b, r["n"][1] - b]]
    c2, p, _ = chi2_rxc(tab, yates=True)
    check(s, f"表6 {label} χ²", chi_rep, c2, 0.02, "2×2表连续性校正χ²")
    check(s, f"表6 {label} P", p_rep, p, 0.002, "同上")

# ---------------------------------------------------------------------------
# F. Treatment
# ---------------------------------------------------------------------------
t = D["treatment"]
s = "F 治疗前后（原稿表5）"
n = D["N"]
check(s, "前后均数之差=下降值均数", t["delta"][0], t["gerdq4_pre"][0] - t["gerdq4_post"][0], 0.005, "6.11−4.46")
tt = t["delta"][0] / (t["delta"][1] / math.sqrt(n))
check(s, "配对t值", t["paired_t"], tt, 0.05, "均数/(标准差/√n)")
h = stats.t.ppf(0.975, n - 1) * t["delta"][1] / math.sqrt(n)
check(s, "下降值95%CI下限", t["delta_ci"][0], t["delta"][0] - h, 0.015, "t分布；两位小数输入导致约0.01舍入误差")
check(s, "下降值95%CI上限", t["delta_ci"][1], t["delta"][0] + h, 0.015, "同上")
check(s, "改善+未改善=103", n, t["improved"] + t["not_improved"], 0, "加和")
for k_, lo, hi in [(72, 60.5, 77.9), (31, 22.1, 39.5), (8, 4.0, 14.6), (79, 67.7, 83.8), (39, 29.1, 47.5), (91, 80.7, 93.2)]:
    a, b = wilson(k_, n)
    check(s, f"Wilson 95%CI {k_}/103 下限", lo, 100 * a, 0.05, "Wilson法")
    check(s, f"Wilson 95%CI {k_}/103 上限", hi, 100 * b, 0.05, "Wilson法")
sum_d = round(t["delta"][0] * n)
check(s, "各肥胖组下降值加权和=总和", sum_d, sum(m * k for m, k in zip(t["delta_by_group_mean"], g["n"])), 1.0, "Σ均数×例数")
check(s, "各肥胖组减重加权均数", t["wl"][0], sum(m * k for m, k in zip(g["wl_mean"], g["n"])) / n, 0.01,
      "Σ均数×例数/103；两位小数舍入，允许0.01")
check(s, "改善组/未改善组减重加权均数", t["wl"][0], (r["wl"][0][0] * 72 + r["wl"][1][0] * 31) / n, 0.01,
      "各组均数与合计均为两位小数，加权后最大舍入误差约0.01")
check(s, "各肥胖组基线4GerdQ加权均数", g["gerdq4_total"][0], sum(m * k for m, k in zip(g["gerdq4_mean"], g["n"])) / n, 0.01, "同上")
check(s, "改善组/未改善组基线4GerdQ加权均数", g["gerdq4_total"][0], (r["gerdq4"][0][0] * 72 + r["gerdq4"][1][0] * 31) / n, 0.01, "同上")
check(s, "各肥胖组年龄加权均数", g["age_total"][0], sum(m * k for m, k in zip(g["age_mean"], g["n"])) / n, 0.01, "同上")
check(s, "各肥胖组BMI加权均数", g["bmi_total"][0], sum(m * k for m, k in zip(g["bmi_mean"], g["n"])) / n, 0.01, "同上")

# ---------------------------------------------------------------------------
# G. Logistic model
# ---------------------------------------------------------------------------
s = "G Logistic回归（原稿表7）"
expit = lambda x: 1 / (1 + math.exp(-x))
for nm, (b, se, or_, lo, hi, p) in D["logistic"]["terms"].items():
    check(s, f"{nm} P", p, 2 * stats.norm.sf(abs(b / se)), 0.0015, "Wald z=β/SE")
    if or_ is not None:
        check(s, f"{nm} OR", or_, math.exp(b), 0.005, "exp(β)")
        check(s, f"{nm} OR下限", lo, math.exp(b - 1.959964 * se), 0.005, "exp(β−1.96SE)")
        check(s, f"{nm} OR上限", hi, math.exp(b + 1.959964 * se), 0.03, "exp(β+1.96SE)；β为三位小数输入，允许0.03")
b0 = D["logistic"]["terms"]["常数项"][0]
b1 = D["logistic"]["terms"]["减重幅度（每1 kg）"][0]
b2 = D["logistic"]["terms"]["胃镜异常（是/否）"][0]
check(s, "列线图最低概率（0 kg、胃镜阴性）", 0.41, expit(b0), 0.005, "原稿2.7节")
check(s, "列线图最高概率（5 kg、胃镜异常）", 0.98, expit(b0 + 5 * b1 + b2), 0.005, "原稿2.7节")
check(s, "列线图示例概率（2 kg+胃镜异常）", 0.88, expit(b0 + 2 * b1 + b2), 0.005, "原稿2.7节")
check(s, "列线图每1 kg赋分", 51.3, 100 * b1 / b2, 0.05, "β₁/β₂×100")

# ---------------------------------------------------------------------------
# Delta (4GerdQ decrease) moments for responders
# ---------------------------------------------------------------------------
sumsq = [(n - 1) * sd ** 2 + sum_d ** 2 / n for sd in (t["delta"][1] - 0.005, t["delta"][1] + 0.005)]
resp_mean = sum_d / t["improved"]
resp_sd = math.sqrt((sum(sumsq) / 2 - t["improved"] * resp_mean ** 2) / (t["improved"] - 1))

rec = dict(
    score_bands=bands, score_pos=pos_b, score_neg=neg_b, score_total=tot_b,
    pos_ge={str(k): v for k, v in pos_ge.items()}, neg_ge={str(k): v for k, v in neg_ge.items()},
    auc_grouped=auc_g, auc_grouped_se=se_g,
    endo_pos=e_pos, endo_neg=e_neg, endo_pos_ge10=e_pos_ge10, endo_neg_ge10=e_neg - e_neg_lt10,
    pathway_names=["胃镜异常", "胃镜阴性、PPI试验阳性", "胃镜阴性、PPI试验阴性"],
    pathway_n=path_n, pathway_resp=path_resp, pathway_ge10=path_ge10,
    item_sd={k: float(v) for k, v in item_sd.items()}, alpha6=alpha6, alpha4=alpha4,
    sum_delta=sum_d, responder_delta_mean=resp_mean, responder_delta_sd=resp_sd,
)
(CHK / "reconstructed.json").write_text(json.dumps(rec, ensure_ascii=False, indent=2), encoding="utf-8")
with open(CHK / "一致性核查.csv", "w", newline="", encoding="utf-8-sig") as fh:
    w = csv.writer(fh)
    w.writerow(["部分", "核查项目", "原稿报告值", "重新计算值", "结论", "计算方法"])
    w.writerows(rows)

bad = [x for x in rows if x[4] != "一致"]
print(f"[01] 核查 {len(rows)} 项，不一致 {len(bad)} 项")
for x in bad:
    print("    ", x)
