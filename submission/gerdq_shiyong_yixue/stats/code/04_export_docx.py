"""Step 4 (optional): collect all tables and figures into one Word file for checking.

Output: submission/gerdq_shiyong_yixue/06_统计图表汇总.docx  (and the .md source next to it)
Requires pypandoc + python-docx (used by tools/md2docx.py).
"""

import subprocess
import sys

from common import FIG, ROOT, TAB

BASE = ROOT.parent
TITLES = {
    "表1": "不同肥胖程度组患者基线资料比较", "表2": "103例患者基线GerdQ各条目得分分布及条目-总分相关性",
    "表3": "GerdQ总分不同截断值识别GERD复合诊断的效能", "表4": "GerdQ总分分层似然比及验后概率",
    "表5": "103例患者治疗前后GerdQ评分及体重变化", "表6": "症状改善组与未改善组临床资料比较",
    "表7": "症状改善相关因素的多因素Logistic回归分析",
    "附表S1": "重建的GerdQ总分与GERD复合诊断交叉分布", "附表S2": "不同诊断路径患者的GerdQ评分与4周症状改善",
    "附表S3": "症状改善的单因素与多因素OR及E值", "附表S4": "胃镜阴性者PPI试验与4周症状改善的一致性",
    "附表S5": "原列线图模型评价指标重估", "附表S6": "后续研究样本量估算",
}
FIGS = {
    "图1": "基线GerdQ总分分布（A）、各条目得分构成（B）及条目-总分相关性（C）",
    "图2": "不同肥胖程度组基线GerdQ总分（A）及基线4GerdQ、4GerdQ下降值和减重幅度（B）比较",
    "图3": "GerdQ总分识别GERD复合诊断的ROC曲线（A）及分层似然比（B）",
    "图4": "治疗前后GerdQ评分变化（A）、不同诊断路径患者的4周症状改善率（B）及PPI试验与4周症状改善的一致性（C）",
    "图5": "症状改善相关因素的单因素与多因素分析",
}

parts = ["# GerdQ高原肥胖GERD研究：统计图表汇总（供核对）", "",
         "本文件由`stats/code/run_all.py`自动生成。表中数据均来自`stats/inputs/summary_data.json`（原稿报告值）"
         "及由其精确推算的结果；121项一致性核查见`stats/output/checks/一致性核查.csv`。", "", "## 一、正文表格", ""]
for key in ["表1", "表2", "表3", "表4", "表5", "表6", "表7"]:
    md = next(TAB.glob(f"{key}_*.md"))
    parts += [f"**{key}　{TITLES[key]}**", "", md.read_text(encoding="utf-8").strip(), ""]
parts += ["## 二、正文图件", ""]
for key, title in FIGS.items():
    png = next(FIG.glob(f"{key}_*.png"))
    parts += [f"![]({png.relative_to(BASE).as_posix()}){{width=16cm}}", "", f"**{key}　{title}**", ""]
parts += ["## 三、附表", ""]
for key in ["附表S1", "附表S2", "附表S3", "附表S4", "附表S5", "附表S6"]:
    md = next(TAB.glob(f"{key}_*.md"))
    parts += [f"**{key}　{TITLES[key]}**", "", md.read_text(encoding="utf-8").strip(), ""]

out_md = BASE / "06_统计图表汇总.md"
out_md.write_text("\n".join(parts), encoding="utf-8")
subprocess.run([sys.executable, str(BASE / "tools" / "md2docx.py"), out_md.name, "06_统计图表汇总.docx"],
               cwd=BASE, check=True)
print(f"[04] 已生成 {out_md.with_suffix('.docx')}")
