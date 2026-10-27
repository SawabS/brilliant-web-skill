#!/usr/bin/env python3
"""Extract design tokens from a captured brilliant.org stylesheet.

Brilliant's web app is built with Panda CSS. Every token is a custom property
named --panda-<category>-<name> declared in two blocks:
  :where(:root,:host)                    -> light theme + all non-colour tokens
  [data-theme=dark]:not(...)             -> dark-theme overrides
Text styles are emitted as `.panda-textStyle_<name>` classes and component
recipes as `.panda-<recipe>--<variant>` classes.

Usage:
  python3 extract_tokens.py <main.css> <out.json>

The output (source/brilliant-tokens.json) is what tools/build_tokens.py reads.
Re-run capture.py first if you want fresh data.
"""
import json
import re
import sys


def clean(css: str) -> str:
    # Panda pads every selector with :not(#\#...) to raise specificity; drop it.
    return re.sub(r":not\(#(?:\\#)+(?:#(?:\\#)+)*\)", "", css)


def decls(body: str) -> dict:
    out = {}
    for d in body.split(";"):
        if ":" not in d or not d.strip().startswith("--panda-"):
            continue
        k, v = d.split(":", 1)
        out[k.strip()[len("--panda-"):]] = v.strip()
    return out


def main(src: str, dst: str) -> None:
    css = clean(open(src, encoding="utf-8").read())
    blocks = list(re.finditer(r"([^{}]{0,200})\{((?:--panda-[^;{}]+;){20,}[^{}]*)\}", css))
    light, dark = {}, {}
    for m in blocks:
        sel = m.group(1)
        if "data-theme=dark" in sel:
            dark.update(decls(m.group(2)))
        elif ":root" in sel:
            light.update(decls(m.group(2)))

    text_styles = {}
    for sel, body in re.findall(r"([^{}@]+)\{([^{}]*)\}", css):
        m = re.match(r"^\s*\.panda-textStyle_(\S+)\s*$", sel)
        if m:
            name = m.group(1).replace("\\", "")
            props = dict(p.split(":", 1) for p in body.split(";") if ":" in p)
            text_styles[name] = props

    recipes = {}
    for sel, body in re.findall(r"([^{}@]+)\{([^{}]*)\}", css):
        m = re.match(r"^\s*\.panda-(badge|progress|lessonContent)((?:--[\w]+)*)([^,{]*)$", sel.strip())
        if m:
            recipes.setdefault(m.group(1), {})[(m.group(2) + m.group(3)).strip() or "base"] = body

    keyframes = {n: b for n, b in re.findall(r"@keyframes ([\w-]+)\{((?:[^{}]*\{[^{}]*\})*)\}", css)}

    json.dump({"light": light, "dark": dark, "textStyles": text_styles,
               "recipes": recipes, "keyframes": keyframes}, open(dst, "w"), indent=1, sort_keys=True)
    print(f"light={len(light)} dark={len(dark)} textStyles={len(text_styles)} "
          f"recipes={sum(len(v) for v in recipes.values())} keyframes={len(keyframes)}")


if __name__ == "__main__":
    main(*sys.argv[1:3])
