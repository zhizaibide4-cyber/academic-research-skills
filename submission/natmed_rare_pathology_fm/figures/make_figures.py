"""Draft display items for the Nature Medicine Review (Figs 1-5).

Output: vector PDF + 300 dpi PNG per figure, 180 mm double-column width,
sans-serif 6-8 pt, Okabe-Ito colour-blind-safe palette.
Run: python3 make_figures.py
"""
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyArrowPatch, FancyBboxPatch, Rectangle

OUT = Path(__file__).resolve().parent
MM = 1 / 25.4
W = 180 * MM

plt.rcParams.update({
    "font.family": "sans-serif",
    "font.sans-serif": ["Arial", "Helvetica", "Liberation Sans", "DejaVu Sans"],
    "font.size": 7,
    "axes.linewidth": 0.6,
    "axes.labelsize": 7,
    "xtick.labelsize": 6,
    "ytick.labelsize": 6,
    "legend.fontsize": 6,
    "pdf.fonttype": 42,
    "svg.fonttype": "none",
})

OI = {
    "orange": "#E69F00", "sky": "#56B4E9", "green": "#009E73", "yellow": "#F0E442",
    "blue": "#0072B2", "verm": "#D55E00", "purple": "#CC79A7", "grey": "#999999",
}


def box(ax, x, y, w, h, text, fc, ec="none", fs=6.5, weight="normal", color="black", ha="center"):
    ax.add_patch(FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.004,rounding_size=0.012",
                                fc=fc, ec=ec, lw=0.6))
    tx = x + w / 2 if ha == "center" else x + 0.01
    ax.text(tx, y + h / 2, text, ha=ha, va="center", fontsize=fs, weight=weight, color=color,
            wrap=True)


def arrow(ax, p0, p1, color="#444444", ls="-", lw=0.8):
    ax.add_patch(FancyArrowPatch(p0, p1, arrowstyle="-|>", mutation_scale=7, color=color,
                                 lw=lw, ls=ls))


def save(fig, name):
    fig.savefig(OUT / f"{name}.pdf")
    fig.savefig(OUT / f"{name}.png", dpi=300)
    plt.close(fig)


def fig1():
    fig = plt.figure(figsize=(W, 110 * MM))
    ax = fig.add_axes([0, 0, 1, 1]); ax.axis("off"); ax.set_xlim(0, 1); ax.set_ylim(0, 1)
    layers = [
        (0.80, "Clinical end points", OI["blue"], "white",
         ["Subtype diagnosis", "Triage and referral", "Molecular / genetic inference",
          "Prognosis", "Treatment selection"]),
        (0.58, "Data-efficient adaptation", OI["green"], "white",
         ["Zero-shot prompting", "Prototype / retrieval", "Linear probe / MIL",
          "PEFT / prompt tuning", "Full fine-tuning"]),
        (0.36, "Pathology foundation models", OI["orange"], "black",
         ["Self-supervised tile encoders", "Vision-language models", "Slide encoders"]),
        (0.14, "Pretraining corpora", OI["grey"], "white",
         ["Public cohorts", "Real-world archives", "Pathology reports",
          "Rare disease registries", "Spatial / molecular omics"]),
    ]
    x0, x1 = 0.03, 0.72
    for y, title, col, tcol, items in layers:
        ax.add_patch(Rectangle((x0, y - 0.01), x1 - x0, 0.17, fc=col, alpha=0.12, ec="none"))
        ax.text(x0 + 0.005, y + 0.145, title, fontsize=7.5, weight="bold", va="center")
        n = len(items); gap = 0.008; bw = (x1 - x0 - 0.01 - gap * (n - 1)) / n
        for i, it in enumerate(items):
            box(ax, x0 + 0.005 + i * (bw + gap), y + 0.01, bw, 0.10, it, col, fs=6, color=tcol)
    for ya, yb in [(0.27, 0.36), (0.49, 0.58), (0.71, 0.80)]:
        arrow(ax, (0.375, ya), (0.375, yb))
    ax.text(x1 - 0.005, 0.715, "left \u2192 right: increasing labels and trainable parameters",
            fontsize=5.5, style="italic", va="center", ha="right", color="#333333")
    cx, cw = 0.75, 0.22
    ax.add_patch(Rectangle((cx, 0.13), cw, 0.83, fc=OI["verm"], alpha=0.10, ec=OI["verm"], lw=0.6))
    ax.text(cx + cw / 2, 0.93, "Cross-cutting constraints", ha="center", fontsize=7.5, weight="bold")
    cons = ["Label scarcity", "Domain shift", "Disease-spectrum shift", "Population bias",
            "Miscalibration", "Evidence gaps", "Access"]
    for i, c in enumerate(cons):
        box(ax, cx + 0.01, 0.82 - i * 0.10, cw - 0.02, 0.075, c, "white", ec=OI["verm"], fs=6.3)
    ax.text(0.5, 0.04, "Figure 1 (draft) \u2013 overall framework", ha="center", fontsize=6, color="#777777")
    save(fig, "Fig1_framework")


def fig2():
    fig, (a, b) = plt.subplots(1, 2, figsize=(W, 75 * MM), gridspec_kw={"width_ratios": [1.1, 1]})
    strat = [
        ("Zero-shot prompting", 0.7, 1e-6, OI["blue"]),
        ("Prototype / retrieval", 3, 1e-5, OI["sky"]),
        ("Linear probe", 15, 1e-4, OI["green"]),
        ("ABMIL / TransMIL", 60, 3e-3, OI["yellow"]),
        ("PEFT (LoRA, adapters)", 150, 1e-2, OI["orange"]),
        ("Prompt tuning", 25, 5e-4, OI["purple"]),
        ("Full fine-tuning", 1500, 1.0, OI["verm"]),
    ]
    for name, x, y, c in strat:
        a.scatter(x, y, s=55, color=c, edgecolor="black", lw=0.4, zorder=3)
        a.annotate(name, (x, y), xytext=(5, 3), textcoords="offset points", fontsize=5.8)
    a.set_xscale("log"); a.set_yscale("log")
    a.set_xlim(0.3, 1e4); a.set_ylim(3e-7, 5)
    a.set_xlabel("Labelled cases per class (target disease, log scale)")
    a.set_ylabel("Fraction of trainable parameters (log scale)")
    a.annotate("", xy=(2500, 2), xytext=(0.6, 3e-7 * 3),
               arrowprops=dict(arrowstyle="-|>", ls="--", color="#555555", lw=0.8))
    a.text(0.02, 0.97, "Positions are schematic", transform=a.transAxes, fontsize=5.5,
           style="italic", va="top", color="#555555")
    a.set_title("a", loc="left", weight="bold", fontsize=8)
    for s in ("top", "right"):
        a.spines[s].set_visible(False)

    dims = ["Labelling\nrequirement", "Trainable\nparameters", "Cross-site\nrobustness",
            "Interpret-\nability", "Deployment\ncost", "Rare-disease\nfit"]
    rows = ["Zero-shot", "Prototype", "Linear probe", "MIL", "PEFT / prompt", "Full FT"]
    # 1 = low, 3 = high (qualitative synthesis of the cited literature)
    R = [[1, 1, 2, 2, 1, 2],
         [1, 1, 2, 3, 1, 3],
         [2, 1, 2, 2, 1, 3],
         [2, 2, 2, 3, 2, 3],
         [2, 2, 2, 2, 2, 2],
         [3, 3, 1, 1, 3, 1]]
    lab = {1: "Low", 2: "Med", 3: "High"}
    cmap = matplotlib.colors.ListedColormap(["#DCEAF5", "#8DBBDD", "#2C6FA6"])
    b.imshow(R, cmap=cmap, vmin=0.5, vmax=3.5, aspect="auto")
    for i in range(len(rows)):
        for j in range(len(dims)):
            b.text(j, i, lab[R[i][j]], ha="center", va="center", fontsize=5.5,
                   color="white" if R[i][j] == 3 else "black")
    b.set_xticks(range(len(dims))); b.set_xticklabels(dims, fontsize=5.5)
    b.set_yticks(range(len(rows))); b.set_yticklabels(rows)
    b.tick_params(length=0)
    for s in b.spines.values():
        s.set_visible(False)
    b.set_title("b", loc="left", weight="bold", fontsize=8, pad=10)
    b.text(0, 1.01, "Ratings summarize the cited literature and are not measured on a common benchmark",
           transform=b.transAxes, fontsize=5, style="italic", ha="left", va="bottom",
           color="#555555")
    b.text(0, -0.2, "Ratings are author placeholders \u2013 confirm against the cited literature",
           transform=b.transAxes, fontsize=5, color=OI["verm"])
    fig.tight_layout()
    save(fig, "Fig2_adaptation")


def fig3():
    fig = plt.figure(figsize=(W, 80 * MM))
    a = fig.add_axes([0.0, 0.0, 0.55, 1]); a.axis("off"); a.set_xlim(0, 1); a.set_ylim(0, 1)
    a.text(0.02, 0.96, "a", weight="bold", fontsize=8)
    src = [("Staining and reagents", OI["purple"]), ("Scanners and acquisition", OI["sky"]),
           ("Centre and tissue processing", OI["orange"]), ("Tissue type", OI["green"]),
           ("Disease spectrum and population", OI["blue"])]
    for i, (s, c) in enumerate(src):
        box(a, 0.04, 0.78 - i * 0.15, 0.40, 0.10, s, c, fs=6,
            color="white" if c in (OI["blue"], OI["purple"]) else "black")
        arrow(a, (0.45, 0.83 - i * 0.15), (0.55, 0.53), color="#888888", lw=0.5)
    chain = ["Few cases from\nfew centres", "Centre signatures\nlearned as shortcuts",
             "Unpredictable\ndegradation elsewhere"]
    for i, t in enumerate(chain):
        box(a, 0.57, 0.72 - i * 0.25, 0.38, 0.15, t, "white", ec=OI["verm"], fs=6)
        if i < 2:
            arrow(a, (0.76, 0.72 - i * 0.25), (0.76, 0.62 - i * 0.25), color=OI["verm"])

    b = fig.add_axes([0.66, 0.22, 0.32, 0.66])
    b.text(-0.45, 1.08, "b", transform=b.transAxes, weight="bold", fontsize=8)
    labels = ["Lymphoma: balanced\naccuracy (ref. 50)", "Kidney: rare-lesion\nprecision (ref. 64)"]
    b.barh([1], [70.3], color=OI["verm"], height=0.5, label="Relative loss (%)")
    b.barh([0], [20], color=OI["blue"], height=0.5, label="Absolute loss (percentage points)")
    b.text(71.5, 1, "up to 70.3%", va="center", fontsize=5.8)
    b.text(21.5, 0, "~20 pp\n(>80% \u2192 ~60%)", va="center", fontsize=5.8)
    b.set_yticks([0, 1]); b.set_yticklabels(labels, fontsize=5.8)
    b.set_xlim(0, 100); b.set_xlabel("Out-of-distribution performance loss")
    for s in ("top", "right"):
        b.spines[s].set_visible(False)
    b.legend(loc="lower right", frameon=False, ncol=1)
    fig.text(0.66, 0.95, "Centre predictable from embeddings: 88\u201398% (PathoROB, ref. 30)",
             fontsize=5.8, style="italic")
    save(fig, "Fig3_domain_shift")


def fig4():
    fig, (a, b) = plt.subplots(1, 2, figsize=(W, 95 * MM), gridspec_kw={"width_ratios": [1, 1.25]})
    # (disease, level, marker): F filled = external/prospective, S open square = internal only, X = inferred
    data = [
        ("CNS tumours (Hetairos)", 3, "F"),
        ("Autoimmune hepatitis (AIOLI)", 3, "F"),
        ("Rare glomerular lesions", 2, "F"),
        ("Paediatric brain tumours", 2, "F"),
        ("Paediatric soft-tissue sarcoma", 2, "F"),
        ("Peripheral T-cell lymphoma", 2, "F"),
        ("Common lymphoma subtypes", 2, "F"),
        ("Paediatric and rare cancers (PathPT)", 1.5, "S"),
        ("B-cell lymphoma (LymphoVision)", 1, "S"),
        ("Uterine leiomyosarcoma", 1, "S"),
        ("Rare renal tumours", 1, "S"),
        ("Fabry nephropathy", 1, "S"),
        ("Urogenital schistosomiasis", 1, "S"),
        ("Granulomatous infections", 0, "X"),
        ("Ultra-rare paediatric tumours", 0, "X"),
        ("Ultra-rare lymphoma subtypes", 0, "X"),
    ]
    a.axvspan(-0.5, 0.5, color="#EEEEEE", zorder=0)
    for i, (d, lv, m) in enumerate(data):
        y = len(data) - 1 - i
        if m == "F":
            a.scatter(lv, y, s=30, color=OI["blue"], zorder=3)
        elif m == "S":
            a.scatter(lv, y, s=26, marker="s", facecolor="white", edgecolor=OI["orange"], lw=1, zorder=3)
        else:
            a.scatter(lv, y, s=26, marker="x", color=OI["grey"], lw=1, zorder=3)
    a.set_yticks(range(len(data))); a.set_yticklabels([d for d, _, _ in data][::-1], fontsize=5.6)
    a.set_xticks(range(5)); a.set_xticklabels(["L0", "L1", "L2", "L3", "L4"])
    a.set_xlim(-0.5, 4.5); a.grid(axis="x", lw=0.3, color="#CCCCCC")
    a.text(4, len(data) / 2, "empty", ha="center", rotation=90, fontsize=6, color="#999999")
    a.set_xlabel("Evidence-maturity level (Box 1)")
    a.set_title("a", loc="left", weight="bold", fontsize=8)
    for s in ("top", "right"):
        a.spines[s].set_visible(False)
    from matplotlib.lines import Line2D
    h = [Line2D([], [], marker="o", ls="", color=OI["blue"], label="External / prospective"),
         Line2D([], [], marker="s", ls="", mfc="white", mec=OI["orange"], label="Internal retrospective only"),
         Line2D([], [], marker="x", ls="", color=OI["grey"], label="Inferred feasibility")]
    a.legend(handles=h, loc="lower right", frameon=False, fontsize=5.3)

    b.axis("off"); b.set_title("b", loc="left", weight="bold", fontsize=8)
    rows = [
        ("CNS tumours", "102 methylation subtypes from H&E; prospective routine use; 12 d \u2192 12 min", "L3"),
        ("Autoimmune hepatitis", "AUC 0.92 dev. vs 0.74 external; prospective testing", "L3"),
        ("Rare glomerular lesions", "Precision \u221270.3% across domains; up to 63.4% recovery", "L2"),
        ("Paediatric brain tumours", "FM linear probes >> ImageNet; H&E + Ki-67 fusion", "L2"),
        ("Paediatric sarcoma", "RMS vs non-RMS; alveolar vs embryonal", "L2"),
        ("PTCL", "ALCL / TFH / PTCL-NOS; external cohort n = 118", "L2"),
        ("Paediatric / rare cancers", "Balanced acc. 0.679, 30 subtypes, 10-shot", "L1\u2013L2"),
        ("B-cell lymphoma", "Six-class AUC 0.98; recall MCL 70.8%", "L1"),
        ("Fabry nephropathy", "Score separates cases from controls", "L1"),
        ("Ultra-rare entities", "No disease-specific validated models", "L0"),
    ]
    lc = {"L3": OI["blue"], "L2": OI["sky"], "L1\u2013L2": OI["yellow"], "L1": OI["orange"], "L0": OI["grey"]}
    for i, (d, r, lv) in enumerate(rows):
        y = 0.95 - i * 0.095
        b.text(0.0, y, d, fontsize=5.8, weight="bold", va="center", transform=b.transAxes)
        b.text(0.0, y - 0.038, r, fontsize=5.3, va="center", transform=b.transAxes, color="#333333")
        b.add_patch(FancyBboxPatch((0.88, y - 0.03), 0.11, 0.05, transform=b.transAxes,
                                   boxstyle="round,pad=0.004", fc=lc[lv], ec="none"))
        b.text(0.935, y - 0.005, lv, fontsize=5.8, ha="center", va="center", transform=b.transAxes,
               color="white" if lv in ("L3", "L0") else "black")
    fig.tight_layout()
    save(fig, "Fig4_evidence_landscape")


def fig5():
    fig = plt.figure(figsize=(W, 85 * MM))
    ax = fig.add_axes([0, 0, 1, 1]); ax.axis("off"); ax.set_xlim(0, 1); ax.set_ylim(0, 1)
    stages = ["S0 Technical\ndevelopment", "S1 Internal\nvalidation", "S2 External\nvalidation",
              "S3 Prospective\nsilent evaluation", "S4 Controlled\nclinical utility",
              "S5 Authorization,\ndeployment,\nsurveillance"]
    fails = ["Leakage;\nslide-level\nsplits", "Site shortcuts;\nwide CIs", "Miscalibration;\nsubgroup gaps",
             "Workflow\nmismatch;\ndrift", "No patient\nbenefit"]
    reached = [True, True, True, True, False, False]
    bw = 0.135; base = 0.36
    for i, s in enumerate(stages):
        x = 0.04 + i * 0.155; h = 0.10 + i * 0.06
        fc = OI["blue"] if reached[i] else "white"
        ax.add_patch(Rectangle((x, base), bw, h, fc=fc, ec=OI["blue"], lw=0.8,
                               alpha=1 if reached[i] else 1, hatch=None if reached[i] else "///"))
        ax.text(x + bw / 2, base + h + 0.04, s, ha="center", va="bottom", fontsize=6, weight="bold")
        if i < 5:
            ax.text(x + bw + 0.01, base - 0.015, fails[i].replace("\n", " ").replace("; ", ";\n"),
                    fontsize=4.8, color=OI["verm"], ha="center", va="top")
            ax.plot([x + bw + 0.01] * 2, [base - 0.01, base + 0.02], color=OI["verm"], lw=0.6)
    ax.text(0.04 + 3 * 0.155 + bw / 2, base + 0.10 + 3 * 0.06 - 0.04,
            "reached for two\ndisease groups\n(CNS tumours,\nautoimmune hepatitis)",
            ha="center", va="top", fontsize=4.9, color="white")
    ax.text(0.04 + 4.5 * 0.155 + bw / 2, base + 0.08, "not yet reached\nin rare disease histology",
            ha="center", fontsize=5.3, style="italic", color="#555555",
            bbox=dict(fc="white", ec="none", pad=1))
    arrow(ax, (0.04, 0.93), (0.96, 0.93), color="#555555")
    ax.text(0.5, 0.95, "Evidence strength and cost of translation increase together", ha="center",
            fontsize=6, style="italic")
    ax.add_patch(Rectangle((0.03, 0.02), 0.94, 0.15, fc=OI["green"], alpha=0.15, ec="none"))
    ax.text(0.5, 0.13, "Baseline across all stages: reporting, regulation and governance", ha="center",
            fontsize=6.5, weight="bold")
    ax.text(0.5, 0.06, "TRIPOD+AI \u00b7 STARD-AI \u00b7 PROBAST+AI \u00b7 DECIDE-AI \u00b7 SPIRIT-AI / CONSORT-AI \u00b7 "
            "TRIPOD-LLM \u00b7 FDA PCCP guidance \u00b7 EU AI Act", ha="center", fontsize=5.8)
    save(fig, "Fig5_translation_pathway")


if __name__ == "__main__":
    for f in (fig1, fig2, fig3, fig4, fig5):
        f()
    print("done")
