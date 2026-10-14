"""Step 3: draw manuscript figures 图1~图5 from the summary data.

Each figure is saved as PNG (300 dpi), TIFF (300 dpi, LZW) and PDF (vector) in output/figures/.
Only quantities that are reported or exactly reconstructed are plotted; no individual data are simulated.
"""

import math

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
from matplotlib import font_manager
from PIL import Image

from common import FIG, Z, cohen_kappa, cochran_armitage, likelihood_ratio, load, load_reconstructed, odds_ratio_woolf, wilson

for f in font_manager.findSystemFonts():
    if "NotoSansCJK" in f:
        font_manager.fontManager.addfont(f)
plt.rcParams.update({
    "font.family": ["Noto Sans CJK SC", "DejaVu Sans"], "axes.unicode_minus": False, "font.size": 9,
    "axes.spines.top": False, "axes.spines.right": False, "axes.titlesize": 10, "axes.titleweight": "bold",
    "axes.titlelocation": "left", "pdf.fonttype": 42,
})
BLUE, LBLUE, RED, GREY = "#2b5b84", "#7fa7c9", "#b8463c", "#8c8c8c"
ITEM_COL = ["#f2f2f2", "#c6dbef", "#6baed6", "#2171b5"]

D = load()
R = load_reconstructed()
N = D["N"]


def save(fig, name):
    png = FIG / f"{name}.png"
    fig.savefig(png, dpi=300, bbox_inches="tight")
    fig.savefig(FIG / f"{name}.pdf", bbox_inches="tight")
    Image.open(png).convert("RGB").save(FIG / f"{name}.tif", dpi=(300, 300), compression="tiff_lzw")
    plt.close(fig)


def label_bars(ax, xs, ys, texts, dy=0.5, **kw):
    for x, y, t in zip(xs, ys, texts):
        ax.text(x, y + dy, t, ha="center", va="bottom", fontsize=8, **kw)


# ---------------------------------------------------------------------------
# 图1 基线GerdQ总分分布、条目得分分布、条目-总分相关
# ---------------------------------------------------------------------------
fig = plt.figure(figsize=(12, 3.9))
gs = fig.add_gridspec(1, 3, width_ratios=[1.1, 1.3, 0.9], wspace=0.38)
ax = fig.add_subplot(gs[0])
x = np.arange(len(R["score_bands"]))
ax.bar(x, R["score_pos"], 0.7, color=BLUE, label="GERD复合诊断阳性（n=79）")
ax.bar(x, R["score_neg"], 0.7, bottom=R["score_pos"], color=RED, label="GERD复合诊断阴性（n=24）")
label_bars(ax, x, R["score_total"], [str(v) for v in R["score_total"]], dy=0.4)
ax.set_xticks(x, R["score_bands"])
ax.set_xlabel("基线GerdQ总分（分）")
ax.set_ylabel("例数")
ax.set_ylim(0, 34)
ax.legend(frameon=False, fontsize=8, loc="upper left")
ax.set_title("A")

ax = fig.add_subplot(gs[1])
it = D["items"]
order = it["order"]
cnt = np.array([it["counts"][k] for k in order]) / N * 100
left = np.zeros(len(order))
y = np.arange(len(order))[::-1]
for s in range(4):
    ax.barh(y, cnt[:, s], left=left, color=ITEM_COL[s], edgecolor="white", lw=0.5, label=f"{s}分")
    for yi, l, w in zip(y, left, cnt[:, s]):
        if w >= 8:
            ax.text(l + w / 2, yi, f"{w:.0f}", ha="center", va="center", fontsize=7.5,
                    color="white" if s >= 2 else "black")
    left += cnt[:, s]
ylab = [k + ("*" if k in it["negative_items"] else "") for k in order]
ax.set_yticks(y, ylab)
ax.set_xlim(0, 100)
ax.set_xlabel("构成比（%）")
ax.legend(ncol=4, frameon=False, fontsize=8, loc="lower center", bbox_to_anchor=(0.5, 1.0))
ax.set_title("B", pad=18)

ax = fig.add_subplot(gs[2])
rs = [it["item_total_rs"][k] for k in order]
ax.barh(y, rs, color=[RED if k in it["negative_items"] else BLUE for k in order], height=0.6)
for yi, v in zip(y, rs):
    ax.text(v + 0.01, yi, f"{v:.3f}", va="center", fontsize=8)
ax.set_yticks(y, ylab)
ax.set_xlim(0, 0.85)
ax.set_xlabel("条目-总分Spearman *r*ₛ".replace("*", ""))
ax.set_title("C")
save(fig, "图1_基线GerdQ总分分布及条目分析")

# ---------------------------------------------------------------------------
# 图2 不同肥胖程度组比较
# ---------------------------------------------------------------------------
g = D["groups"]
names = ["轻度肥胖组\n（n=63）", "中度肥胖组\n（n=26）", "重度肥胖组\n（n=14）"]
fig, axes = plt.subplots(1, 2, figsize=(10, 3.9), gridspec_kw={"width_ratios": [0.8, 1.4], "wspace": 0.3})
ax = axes[0]
mq = np.array(g["gerdq_median_q1_q3"], float)
xs = np.arange(3)
ax.errorbar(xs, mq[:, 0], yerr=[mq[:, 0] - mq[:, 1], mq[:, 2] - mq[:, 0]], fmt="o", color=BLUE,
            ms=7, capsize=6, lw=1.4)
for xi, (m, q1, q3) in zip(xs, mq):
    ax.text(xi + 0.2, m, f"{m:g}（{q1:g}，{q3:g}）", va="center", fontsize=8)
ax.set_xticks(xs, names)
ax.set_xlim(-0.5, 2.9)
ax.set_ylim(7, 14)
ax.set_ylabel("基线GerdQ总分（分）")
ax.set_title(f"A  H={g['gerdq_H']:.2f}，P={g['gerdq_P']:.3f}")
oc = D["obesity_comparison"]
ax.plot([0, 0, 1, 1], [13.2, 13.4, 13.4, 13.2], color="k", lw=0.8)
ax.text(0.5, 13.45, f"校正P={oc['pairwise_mild_moderate_Padj']:.3f}", ha="center", fontsize=8)

ax = axes[1]
metrics = [("基线4GerdQ（分）", g["gerdq4_mean"], g["gerdq4_sd"], g["gerdq4_P"]),
           ("4GerdQ下降值（分）", D["treatment"]["delta_by_group_mean"], D["treatment"]["delta_by_group_sd"], D["treatment"]["delta_by_group_P"]),
           ("减重幅度（kg）", g["wl_mean"], g["wl_sd"], g["wl_P"])]
w = 0.25
cols = [LBLUE, BLUE, "#1a3550"]
for gi in range(3):
    m = [mt[1][gi] for mt in metrics]
    s = [mt[2][gi] for mt in metrics]
    pos = np.arange(3) + (gi - 1) * w
    ax.bar(pos, m, w, yerr=s, capsize=3, color=cols[gi], error_kw=dict(lw=0.8),
           label=names[gi].replace("\n", ""))
ax.set_xticks(np.arange(3), [f"{mt[0]}\nP={mt[3]:.3f}" for mt in metrics])
ax.set_ylabel("均数±标准差")
ax.legend(frameon=False, fontsize=8, ncol=1, loc="upper right")
ax.set_ylim(0, 10)
ax.set_title("B")
save(fig, "图2_不同肥胖程度组GerdQ评分及减重比较")

# ---------------------------------------------------------------------------
# 图3 ROC曲线与分层似然比
# ---------------------------------------------------------------------------
dg = D["diagnosis"]
npos, nneg = dg["n_pos"], dg["n_neg"]
cuts = dg["cutoffs"]
fig, axes = plt.subplots(1, 2, figsize=(10, 4.3), gridspec_kw={"wspace": 0.32})
ax = axes[0]
tpr = [1.0] + [R["pos_ge"][str(c)] / npos for c in cuts] + [0.0]
fpr = [1.0] + [R["neg_ge"][str(c)] / nneg for c in cuts] + [0.0]
ax.plot(fpr, tpr, "-o", color=BLUE, ms=4, lw=1.5)
ax.fill_between(fpr, tpr, step=None, alpha=0.08, color=BLUE)
for c, a, b in zip(cuts, fpr[1:-1], tpr[1:-1]):
    ax.annotate(f"≥{c}分", (a, b), xytext=(7, -11), textcoords="offset points", fontsize=8)
best = cuts.index(10)
ax.plot(fpr[best + 1], tpr[best + 1], "o", ms=9, mfc="none", mec=RED, mew=1.5)
ax.plot([0, 1], [0, 1], ls="--", lw=0.8, color=GREY)
ax.text(0.42, 0.12, f"AUC={dg['auc']:.3f}\n（95%CI：{dg['auc_ci'][0]:.3f}~{dg['auc_ci'][1]:.3f}）", fontsize=9)
ax.set_xlabel("1−特异度")
ax.set_ylabel("灵敏度")
ax.set_xlim(-0.02, 1.02)
ax.set_ylim(-0.02, 1.02)
ax.set_aspect("equal")
ax.set_title("A")

ax = axes[1]
merged = [("7分", [0]), ("8~9分", [1, 2]), ("≥10分", [3, 4, 5])]
vals = []
for lab, idx in merged:
    p = sum(R["score_pos"][i] for i in idx)
    n = sum(R["score_neg"][i] for i in idx)
    vals.append((lab, p, n) + likelihood_ratio(p, npos, n, nneg))
xs = np.arange(3)
lr = [v[3] for v in vals]
ax.errorbar(xs, lr, yerr=[[v[3] - v[4] for v in vals], [v[5] - v[3] for v in vals]], fmt="o", ms=7,
            capsize=6, color=BLUE, lw=1.4)
ax.axhline(1, ls="--", lw=0.8, color=GREY)
ax.set_yscale("log")
ax.set_yticks([0.05, 0.1, 0.2, 0.5, 1, 2, 5], ["0.05", "0.1", "0.2", "0.5", "1", "2", "5"])
ax.minorticks_off()
ax.set_ylim(0.05, 6)
ax.set_xlim(-0.5, 2.7)
ax.set_xticks(xs, [f"{v[0]}\n（{v[1]}/{v[2]}）" for v in vals])
for xi, v in zip(xs, vals):
    ax.text(xi + 0.12, v[3], f"{v[3]:.2f}（{v[4]:.2f}~{v[5]:.2f}）\n验后概率{100 * v[1] / (v[1] + v[2]):.1f}%",
            va="center", fontsize=8)
ax.set_xlabel("GerdQ总分区间（GERD阳性/阴性例数）")
ax.set_ylabel("分层似然比（95%CI，对数刻度）")
ax.set_title("B")
save(fig, "图3_GerdQ诊断GERD的ROC曲线及分层似然比")

# ---------------------------------------------------------------------------
# 图4 治疗前后变化、诊断路径与疗效、PPI试验一致性
# ---------------------------------------------------------------------------
t = D["treatment"]
fig = plt.figure(figsize=(13, 4.0))
gsp = fig.add_gridspec(1, 3, width_ratios=[0.9, 1.15, 0.85], wspace=0.35)
ax = fig.add_subplot(gsp[0])
lab = ["4GerdQ", "GerdQ总分"]
pre = [t["gerdq4_pre"], t["total_pre"]]
post = [t["gerdq4_post"], t["total_post"]]
xs = np.arange(2)
ax.bar(xs - 0.18, [p[0] for p in pre], 0.34, yerr=[p[1] for p in pre], capsize=3, color=LBLUE, label="治疗前")
ax.bar(xs + 0.18, [p[0] for p in post], 0.34, yerr=[p[1] for p in post], capsize=3, color=BLUE, label="治疗4周后")
for xi, a, b in zip(xs, pre, post):
    top = max(a[0] + a[1], b[0] + b[1]) + 0.5
    ax.plot([xi - 0.18, xi - 0.18, xi + 0.18, xi + 0.18], [top - 0.3, top, top, top - 0.3], color="k", lw=0.8)
    ax.text(xi, top + 0.1, "P<0.001", ha="center", fontsize=8)
ax.set_xticks(xs, lab)
ax.set_ylabel("评分（分，均数±标准差）")
ax.set_ylim(0, 15)
ax.legend(frameon=False, fontsize=8, loc="upper left")
ax.set_title("A")

ax = fig.add_subplot(gsp[1])
pn, presp = R["pathway_n"], R["pathway_resp"]
rates = [100 * k / n for k, n in zip(presp, pn)]
ci = [wilson(k, n) for k, n in zip(presp, pn)]
xs = np.arange(3)
ax.bar(xs, rates, 0.6, color=[BLUE, LBLUE, RED])
ax.errorbar(xs, rates, yerr=[[r_ - 100 * c[0] for r_, c in zip(rates, ci)], [100 * c[1] - r_ for r_, c in zip(rates, ci)]],
            fmt="none", ecolor="k", capsize=4, lw=0.8)
for xi, k, n, r_ in zip(xs, presp, pn, rates):
    ax.text(xi, 4, f"{k}/{n}\n{r_:.1f}%", ha="center", color="white", fontsize=8.5)
z_, p_ = cochran_armitage(presp, pn, [2, 1, 0])
ax.set_xticks(xs, ["胃镜异常\n（n=39）", "胃镜阴性\nPPI试验阳性（n=40）", "胃镜阴性\nPPI试验阴性（n=24）"], fontsize=8)
ax.set_ylabel("4周症状改善率（%，95%CI）")
ax.set_ylim(0, 100)
ax.set_title(f"B  趋势检验Z={z_:.2f}，P={p_:.3f}")

ax = fig.add_subplot(gsp[2])
agree = np.array([[presp[1], pn[1] - presp[1]], [presp[2], pn[2] - presp[2]]])
k, klo, khi, po = cohen_kappa(agree)
ax.imshow(agree, cmap="Blues", vmin=0, vmax=agree.max() * 1.2)
for i in range(2):
    for j in range(2):
        ax.text(j, i, agree[i, j], ha="center", va="center", fontsize=15, color="white" if agree[i, j] > 20 else "black")
ax.set_xticks([0, 1], ["4周改善", "4周未改善"])
ax.set_yticks([0, 1], ["PPI试验阳性\n（n=40）", "PPI试验阴性\n（n=24）"])
for s in ax.spines.values():
    s.set_visible(False)
ax.set_title(f"C  κ={k:.2f}（95%CI：{klo:.2f}~{khi:.2f}）".replace("-", "−"))
save(fig, "图4_治疗前后评分变化及不同诊断路径的疗效")

# ---------------------------------------------------------------------------
# 图5 OR森林图
# ---------------------------------------------------------------------------
r = D["response"]
rows = []
for key, label in [("male", "男性"), ("smoke_drink", "吸烟和（或）饮酒"), ("gerd", "GERD复合诊断"), ("endo_abnormal", "胃镜异常")]:
    a, b = r[key][:2]
    rows.append(("单因素", label) + odds_ratio_woolf(a, b, 72 - a, 31 - b))
for nm, (b, se, *_x) in D["logistic"]["terms"].items():
    if nm != "常数项":
        rows.append(("多因素", nm, math.exp(b), math.exp(b - Z * se), math.exp(b + Z * se)))
fig, ax = plt.subplots(figsize=(8.2, 3.8))
ys = np.arange(len(rows))[::-1].astype(float)
ys[: 4] += 0.6
for yv, (kind, lab, o, lo, hi) in zip(ys, rows):
    col = BLUE if kind == "多因素" else GREY
    ax.plot([lo, hi], [yv, yv], color=col, lw=1.5)
    ax.plot(o, yv, "s" if kind == "多因素" else "o", color=col, ms=7)
    ax.text(16, yv, f"{o:.2f}（{lo:.2f}~{hi:.2f}）", va="center", fontsize=8.5)
ax.axvline(1, color="k", lw=0.8, ls="--")
ax.set_xscale("log")
ax.set_xticks([0.5, 1, 2, 5, 10], ["0.5", "1", "2", "5", "10"])
ax.minorticks_off()
ax.set_xlim(0.4, 14)
ax.set_yticks(ys, [lab for _, lab, *_r in rows])
ax.text(16, ys[0] + 0.9, "OR（95%CI）", fontsize=8.5, fontweight="bold")
ax.text(0.42, ys[0] + 0.55, "单因素分析", fontsize=8.5, color=GREY, fontweight="bold", va="center")
ax.text(0.42, ys[4] + 0.55, "多因素分析（后退法最终模型）", fontsize=8.5, color=BLUE, fontweight="bold", va="center")
ax.set_xlabel("OR（95%CI，对数刻度）    ← 不利于症状改善    有利于症状改善 →")
ax.spines["left"].set_visible(False)
ax.tick_params(axis="y", length=0)
ax.set_ylim(-0.6, ys[0] + 1.2)
save(fig, "图5_症状改善相关因素的OR森林图")

print(f"[03] 生成 5 幅图（PNG/TIFF/PDF），已写入 {FIG}")
