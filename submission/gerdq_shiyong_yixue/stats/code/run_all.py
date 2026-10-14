"""Run the whole analysis in order: reconstruction/check -> tables -> figures -> Word summary.

The Word summary (step 4) needs pypandoc and python-docx; it is skipped if they are missing.
"""

import importlib.util
import runpy
from pathlib import Path

HERE = Path(__file__).resolve().parent
for step in ("01_reconstruct_check.py", "02_tables.py", "03_figures.py"):
    runpy.run_path(str(HERE / step), run_name="__main__")
if importlib.util.find_spec("pypandoc") and importlib.util.find_spec("docx"):
    runpy.run_path(str(HERE / "04_export_docx.py"), run_name="__main__")
else:
    print("[04] 未安装pypandoc/python-docx，跳过Word汇总")
