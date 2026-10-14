"""Shared paths, input loading and statistical helpers for all analysis scripts."""

import json
import math
from pathlib import Path

import numpy as np
from scipy import stats

ROOT = Path(__file__).resolve().parents[1]
INPUT = ROOT / "inputs" / "summary_data.json"
OUT = ROOT / "output"
TAB = OUT / "tables"
FIG = OUT / "figures"
CHK = OUT / "checks"
for d in (TAB, FIG, CHK):
    d.mkdir(parents=True, exist_ok=True)

Z = stats.norm.ppf(0.975)


def load():
    return json.loads(INPUT.read_text(encoding="utf-8"))


def load_reconstructed():
    return json.loads((CHK / "reconstructed.json").read_text(encoding="utf-8"))


# ---------------------------------------------------------------------------
# Proportions
# ---------------------------------------------------------------------------
def wilson(k, n):
    """Wilson score 95% CI for k/n, returned as proportions."""
    p = k / n
    d = 1 + Z ** 2 / n
    c = (p + Z ** 2 / (2 * n)) / d
    h = Z * math.sqrt(p * (1 - p) / n + Z ** 2 / (4 * n ** 2)) / d
    return max(0.0, c - h), min(1.0, c + h)


def chi2_rxc(table, yates=False):
    """Pearson chi-square for an r x c table; Yates correction applies to 2 x 2 only."""
    r = stats.chi2_contingency(np.asarray(table), correction=yates)
    return r[0], r[1], r[3]


def odds_ratio_woolf(a, b, c, d):
    """Odds ratio (a*d)/(b*c) with Woolf logit 95% CI; rows = exposed/unexposed, cols = event/no event."""
    or_ = (a * d) / (b * c)
    se = math.sqrt(1 / a + 1 / b + 1 / c + 1 / d)
    return or_, or_ * math.exp(-Z * se), or_ * math.exp(Z * se)


def cochran_armitage(events, totals, scores):
    """Two-sided Cochran-Armitage test for trend in proportions."""
    k, n, s = (np.asarray(x, float) for x in (events, totals, scores))
    p = k.sum() / n.sum()
    t = (k * s).sum() - p * (n * s).sum()
    v = p * (1 - p) * ((n * s ** 2).sum() - (n * s).sum() ** 2 / n.sum())
    z = t / math.sqrt(v)
    return z, 2 * stats.norm.sf(abs(z))


def cohen_kappa(table):
    t = np.asarray(table, float)
    n = t.sum()
    po = np.trace(t) / n
    pe = (t.sum(1) * t.sum(0)).sum() / n ** 2
    k = (po - pe) / (1 - pe)
    se = math.sqrt(po * (1 - po) / (n * (1 - pe) ** 2))
    return k, k - Z * se, k + Z * se, po


# ---------------------------------------------------------------------------
# Diagnostic accuracy
# ---------------------------------------------------------------------------
def grouped_auc_delong(pos, neg):
    """AUC (ties = 1/2) and DeLong SE for ordinal data given as counts per ordered category."""
    n1, n0 = sum(pos), sum(neg)
    v10, v01 = [], []
    for i, c in enumerate(pos):
        v10 += [(sum(neg[:i]) + 0.5 * neg[i]) / n0] * c
    for j, c in enumerate(neg):
        v01 += [(sum(pos[j + 1:]) + 0.5 * pos[j]) / n1] * c
    auc = float(np.mean(v10))
    se = math.sqrt(np.var(v10, ddof=1) / n1 + np.var(v01, ddof=1) / n0)
    return auc, se


def hanley_mcneil_se(auc, n1, n0):
    q1, q2 = auc / (2 - auc), 2 * auc ** 2 / (1 + auc)
    return math.sqrt((auc * (1 - auc) + (n1 - 1) * (q1 - auc ** 2) + (n0 - 1) * (q2 - auc ** 2)) / (n1 * n0))


def likelihood_ratio(k_pos, n_pos, k_neg, n_neg):
    """(k_pos/n_pos)/(k_neg/n_neg) with log-method 95% CI (Simel et al.)."""
    lr = (k_pos / n_pos) / (k_neg / n_neg)
    se = math.sqrt(1 / k_pos - 1 / n_pos + 1 / k_neg - 1 / n_neg)
    return lr, lr * math.exp(-Z * se), lr * math.exp(Z * se)


def post_test(pre, lr):
    o = pre / (1 - pre) * lr
    return o / (1 + o)


# ---------------------------------------------------------------------------
# Effect sizes
# ---------------------------------------------------------------------------
def hedges_g(m1, s1, n1, m0, s0, n0):
    sp = math.sqrt(((n1 - 1) * s1 ** 2 + (n0 - 1) * s0 ** 2) / (n1 + n0 - 2))
    return (m1 - m0) / sp * (1 - 3 / (4 * (n1 + n0) - 9))


def e_value_or_common(or_):
    """E-value for an OR with a common outcome: OR -> RR by sqrt (VanderWeele & Ding 2017)."""
    if or_ < 1:
        or_ = 1 / or_
    rr = math.sqrt(or_)
    return rr + math.sqrt(rr * (rr - 1))


# ---------------------------------------------------------------------------
# Formatting
# ---------------------------------------------------------------------------
def fmt_p(p):
    if isinstance(p, str):
        return p
    if p < 0.001:
        return "<0.001"
    return f"{p:.3f}"


def p_eq(p):
    """'*P*=0.012' or '*P*<0.001' for use in running text."""
    s = fmt_p(p)
    return "*P*" + (s if s.startswith("<") else "=" + s)


def pct(k, n, d=1):
    return f"{k}（{100 * k / n:.{d}f}）"


def ci_pct(lo, hi, d=1):
    return f"{100 * lo:.{d}f}%~{100 * hi:.{d}f}%"


def msd(m, s, d=2):
    return f"{m:.{d}f}±{s:.{d}f}"


def write_table(name, header, rows, note=""):
    """Write one table as CSV (Excel-readable UTF-8 BOM) and Markdown; return the record for the workbook."""
    import csv
    import re

    minus = lambda s: re.sub(r"(?<![\w.])-(?=\d)", "−", str(s))
    header = [minus(h) for h in header]
    rows = [[minus(c) for c in r] for r in rows]
    note = minus(note)

    with open(TAB / f"{name}.csv", "w", newline="", encoding="utf-8-sig") as fh:
        w = csv.writer(fh)
        w.writerow(header)
        w.writerows(rows)
        if note:
            w.writerow([])
            w.writerow([note])
    md = ["| " + " | ".join(header) + " |", "|" + "---|" * len(header)]
    md += ["| " + " | ".join(str(c) for c in r) + " |" for r in rows]
    if note:
        md += ["", note]
    (TAB / f"{name}.md").write_text("\n".join(md) + "\n", encoding="utf-8")
    return dict(name=name, header=header, rows=rows, note=note)
