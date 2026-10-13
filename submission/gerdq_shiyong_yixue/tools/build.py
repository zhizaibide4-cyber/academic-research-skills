"""Number [@key; @key] citations by first appearance and append the reference list.

Usage: python3 build.py manuscript_src.md ../02_修改稿全文.md
"""
import re
import sys

from refs import REFS

src, out = sys.argv[1], sys.argv[2]
text = open(src, encoding="utf-8").read()
order = []


def compress(nums):
    nums = sorted(set(nums))
    parts, i = [], 0
    while i < len(nums):
        j = i
        while j + 1 < len(nums) and nums[j + 1] == nums[j] + 1:
            j += 1
        if j - i >= 2:
            parts.append(f"{nums[i]}-{nums[j]}")
        else:
            parts.extend(str(n) for n in nums[i:j + 1])
        i = j + 1
    return ",".join(parts)


def repl(m):
    keys = [k.strip().lstrip("@") for k in m.group(1).split(";")]
    nums = []
    for k in keys:
        if k not in REFS:
            raise KeyError(k)
        if k not in order:
            order.append(k)
        nums.append(order.index(k) + 1)
    return f"<sup>[{compress(nums)}]</sup>"


body = re.sub(r"\[(@[^\]]+)\]", repl, text)
unused = [k for k in REFS if k not in order]
if unused:
    print("unused:", unused)
refs = "\n\n".join(f"[{i}] {REFS[k]}" for i, k in enumerate(order, 1))
body = body.replace("{{REFERENCES}}", refs)
open(out, "w", encoding="utf-8").write(body)
print(f"{len(order)} references")
for i, k in enumerate(order, 1):
    print(i, k)
