#!/usr/bin/env python3
"""Replace the <!--ICONS--> marker in HTML files with the inline sprite from
assets/icons.svg, so pages work from file:// (external <use> is blocked there).
    python3 tools/inline_icons.py templates/*.html preview/index.html
Idempotent: the sprite is wrapped in <!--ICONS:start-->…<!--ICONS:end-->."""
import pathlib, re, sys
root = pathlib.Path(__file__).resolve().parent.parent
sprite = (root / "assets" / "icons.svg").read_text()
sprite = re.sub(r"<!--.*?-->", "", sprite, flags=re.S).strip()
block = f"<!--ICONS:start-->\n{sprite}\n<!--ICONS:end-->"
for f in sys.argv[1:]:
    p = pathlib.Path(f); s = p.read_text()
    s2 = re.sub(r"<!--ICONS:start-->.*?<!--ICONS:end-->", lambda m: block, s, flags=re.S)
    s2 = s2.replace("<!--ICONS-->", block)
    if s2 != s:
        p.write_text(s2); print("icons ->", f)
