"""Markdown -> formatted .docx. Usage: python3 md2docx.py in.md out.docx"""
import re
import subprocess
import sys

import pypandoc

src, out = sys.argv[1], sys.argv[2]
t = open(src, encoding="utf-8").read()
t = re.sub(r"<sup>\[(.*?)\]</sup>", lambda m: "^\\[" + m.group(1) + "\\]^", t)
t = t.replace("~", "\\~")
pypandoc.convert_text(t, "docx", format="markdown-smart+superscript+tex_math_dollars",
                      outputfile=out, extra_args=["--wrap=none"])
subprocess.run([sys.executable, __file__.replace("md2docx.py", "format_docx.py"), out, out], check=True)
