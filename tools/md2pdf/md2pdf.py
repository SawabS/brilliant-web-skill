#!/usr/bin/env python3
"""md2pdf — Markdown → Brilliant-style A4 PDF.

A generic version of the Scaling-v5 pipeline (markdown-it → HTML → Chromium print),
restyled in the Brilliant design language and with nothing report-specific hard-coded.

    python3 md2pdf.py report.md                 # → report.pdf next to it
    python3 md2pdf.py report.md -o out.pdf --html out.html
    python3 md2pdf.py report.md --katex ~/md2pdf/node_modules/katex/dist   # offline maths

Needs: Python 3.10+, `pip install markdown-it-py playwright` and `playwright install chromium`.
Optional: `mmdc` (Mermaid CLI) on PATH renders ```mermaid blocks; KaTeX renders $…$ maths
(from --katex DIR, else from the jsDelivr CDN when online; offline it prints the TeX source).

Markdown conventions (all optional):
  front matter   ---\ntitle: …\nsubtitle: …\nkicker: …\nlead: …\nshort_title: …\nmeta_left: …\nmeta_right: …
                 badges: [Done · 240/240 | green, Evaluated | blue]\nstats: [240 | tokenizers, 8 | vocab sizes]\n---
                 (no front matter → no cover; the first # heading becomes the title)
  # Part I · The study          → full-bleed part opener; an *italic-only* paragraph after it is the subtitle
  ## 3. Title (2026-10-24)      → numbered section with a hue coin and a date pill
  ## Title                      → unnumbered (minor) section
  ### 3.1 Title                 → subsection with a muted number
  > **Note.** …                 → callout: Note/Info/Tip=blue · Done/Complete=green · Caveat/Warning/Limit=yellow ·
                                   Equation/Definition/Theorem=purple · Failure/Error=red
  ```stats\n240 | tokenizers trained | 0 failures\n```  → stat tiles (value | label | note)
  ![alt](path.png) + *Figure 3. Caption*               → figure on an oat stage with a numbered caption
  ```python …```                → black code slab with a language tag and light syntax colouring
  $x$  $$…$$                    → KaTeX
"""
from __future__ import annotations

import argparse
import html
import json
import pathlib
import re
import shutil
import subprocess
import sys
import tempfile

from markdown_it import MarkdownIt

HERE = pathlib.Path(__file__).resolve().parent
ROOT = HERE.parent.parent
ACCENTS = ["blue", "orange", "purple", "green", "pink", "teal"]
COINS = ["blue", "orange", "purple", "green"]


# ───────────────────────── front matter ─────────────────────────
def front_matter(md: str) -> tuple[dict, str]:
    m = re.match(r"^---\n(.*?)\n---\n", md, re.S)
    if not m:
        return {}, md
    meta = {}
    for line in m.group(1).splitlines():
        if ":" not in line:
            continue
        k, v = line.split(":", 1)
        v = v.strip()
        if v.startswith("[") and v.endswith("]"):
            v = [x.strip() for x in v[1:-1].split(",") if x.strip()]
        meta[k.strip()] = v
    return meta, md[m.end():]


# ───────────────────────── helpers ─────────────────────────
KW = {
    "python": r"\b(def|class|return|if|elif|else|for|while|in|not|and|or|import|from|as|with|try|except|finally|raise|yield|lambda|pass|break|continue|None|True|False|is|async|await)\b",
    "js": r"\b(const|let|var|function|return|if|else|for|while|of|in|new|class|import|from|export|default|await|async|try|catch|throw|null|undefined|true|false)\b",
    "bash": r"\b(if|then|else|fi|for|do|done|while|case|esac|function|export|cd|echo|set)\b",
}
KW["javascript"] = KW["ts"] = KW["typescript"] = KW["js"]
KW["sh"] = KW["shell"] = KW["zsh"] = KW["bash"]


def highlight(code: str, lang: str) -> str:
    """Tiny tokenizer: comments, strings, numbers, keywords, calls. Input is already HTML-escaped."""
    kw = KW.get(lang)
    if not kw:
        return code
    comment = r"(#[^\n]*)" if lang in ("python", "bash", "sh", "shell", "zsh") else r"(//[^\n]*)"
    pat = re.compile(comment + r"|(&quot;.*?&quot;|&#x27;.*?&#x27;|'[^'\n]*'|\"[^\"\n]*\")|(\b\d+(?:\.\d+)?\b)|" + kw + r"|(\b[A-Za-z_]\w*)(?=\()")
    def sub(m):
        if m.group(1): return f'<span class="c">{m.group(1)}</span>'
        if m.group(2): return f'<span class="s">{m.group(2)}</span>'
        if m.group(3): return f'<span class="n">{m.group(3)}</span>'
        if m.group(4): return f'<span class="k">{m.group(4)}</span>'
        if m.group(5): return f'<span class="f">{m.group(5)}</span>'
        return m.group(0)
    return pat.sub(sub, code)


def callout_kind(title: str) -> str:
    t = title.lower()
    if re.search(r"done|complete|success|hosted|result", t): return "good"
    if re.search(r"caveat|warning|limit|careful|note well", t): return "warn"
    if re.search(r"equation|definition|theorem|proof|lemma|formula", t): return "math"
    if re.search(r"fail|error|broken|bug", t): return "bad"
    return "info"


def mermaid_svg(src: str, idx: int, tmp: pathlib.Path) -> str | None:
    mmdc = shutil.which("mmdc")
    if not mmdc:
        return None
    inp, out = tmp / f"m{idx}.mmd", tmp / f"m{idx}.svg"
    inp.write_text(src)
    cmd = [mmdc, "-q", "-i", str(inp), "-o", str(out), "-c", str(HERE / "mermaid.json"), "-b", "transparent"]
    pc = tmp / "puppeteer.json"
    try:
        from playwright.sync_api import sync_playwright
        with sync_playwright() as p:
            exe = p.chromium.executable_path
        pc.write_text(json.dumps({"executablePath": exe, "args": ["--no-sandbox"]}))
        cmd += ["-p", str(pc)]
    except Exception:
        pass
    try:
        subprocess.run(cmd, check=True, capture_output=True, timeout=120)
        svg = re.sub(r"<\?xml.*?\?>", "", out.read_text())
        # Brilliant blocks are rounded: give Mermaid's rectangles a 10px radius
        svg = re.sub(r'(<rect[^>]*class="basic label-container"[^>]*?)(/?>)', r'\1 rx="10" ry="10"\2', svg)
        return svg.replace('style="max-width:', 'style="height:auto; max-width:', 1)
    except Exception as e:  # keep going; show the source instead
        print(f"  mermaid block {idx} failed: {e}", file=sys.stderr)
        return None


# ───────────────────────── build ─────────────────────────
def build(md_path: pathlib.Path, katex_dir: str | None) -> str:
    raw = md_path.read_text(encoding="utf-8")
    meta, md = front_matter(raw)
    tmp = pathlib.Path(tempfile.mkdtemp(prefix="md2pdf-"))

    if not meta.get("title"):
        m = re.search(r"^# (?!Part\b)(.+)$", md, re.M)
        if m:
            meta.setdefault("title", m.group(1).strip())
            md = md[:m.start()] + md[m.end():]

    # protect maths and special fences before markdown-it sees them
    stash: list[str] = []
    def keep(s: str) -> str:
        stash.append(s)
        return f"MDSTASH{len(stash) - 1}X"

    def fence(m):
        lang, body = m.group(1).strip().lower(), m.group(2)
        if lang == "mermaid":
            svg = mermaid_svg(body, len(stash), tmp)
            if svg:
                return "\n" + keep(f'<figure class="fig"><div class="stage">{svg}</div></figure>') + "\n"
        if lang == "stats":
            tiles = []
            for i, line in enumerate(l for l in body.splitlines() if l.strip()):
                parts = [html.escape(p.strip()) for p in line.split("|")] + ["", ""]
                tiles.append(f'<div class="stat a-{ACCENTS[i % 6]}"><div class="stat__n">{parts[0]}</div>'
                             f'<div class="stat__l">{parts[1]}</div><div class="stat__s">{parts[2]}</div></div>')
            return "\n" + keep(f'<div class="stats">{"".join(tiles)}</div>') + "\n"
        tag = {"py": "Python", "python": "Python", "js": "JavaScript", "ts": "TypeScript", "bash": "Shell", "sh": "Shell",
               "shell": "Shell", "json": "JSON", "yaml": "YAML", "sql": "SQL", "text": "Pseudocode", "": "Code"}.get(lang, lang.title())
        code = highlight(html.escape(body.rstrip("\n")), lang)
        return "\n" + keep(f'<pre><span class="pre-tag">{tag}</span><code>{code}</code></pre>') + "\n"
    md = re.sub(r"^```([^\n]*)\n(.*?)^```\s*$", fence, md, flags=re.S | re.M)
    md = re.sub(r"\$\$(.+?)\$\$", lambda m: keep(f'<div class="eq">\\[{html.escape(m.group(1).strip())}\\]</div>'), md, flags=re.S)
    md = re.sub(r"(?<![\\$])\$([^$\n]+?)\$", lambda m: keep(f'<span class="math">\\({html.escape(m.group(1))}\\)</span>'), md)

    mdi = MarkdownIt("commonmark", {"html": True, "typographer": True}).enable(["table", "strikethrough"])
    body = mdi.render(md)
    body = re.sub(r"<p>\s*(MDSTASH\d+X)\s*</p>", r"\1", body)
    body = re.sub(r"MDSTASH(\d+)X", lambda m: stash[int(m.group(1))], body)

    # figures: image paragraph (+ optional italic caption paragraph)
    fig_n = [0]
    def figure(src, alt, cap=None):
        fig_n[0] += 1
        cap = cap or f"<b>Figure {fig_n[0]}.</b> {alt}"
        cap = re.sub(r"^(Figure\s+\d+\.)", r"<b>\1</b>", cap)
        src_abs = src if re.match(r"^(https?:|data:|file:)", src) else (md_path.parent / src).resolve().as_uri()
        return f'<figure class="fig"><div class="stage"><img src="{src_abs}" alt="{alt}"></div><figcaption>{cap}</figcaption></figure>'
    body = re.sub(r'<p><img src="([^"]+)" alt="([^"]*)"\s*/?></p>\s*<p><em>(.*?)</em></p>', lambda m: figure(m.group(1), m.group(2), m.group(3)), body, flags=re.S)
    body = re.sub(r'<p><img src="([^"]+)" alt="([^"]*)"\s*/?></p>', lambda m: figure(m.group(1), m.group(2)), body)

    # callouts
    def callout(m):
        t, rest = m.group(1).rstrip("."), m.group(2)
        return f'<div class="callout {callout_kind(t)}"><div class="callout__tag">{t}</div><p>{rest.strip()}</p></div>'
    body = re.sub(r"<blockquote>\s*<p><strong>([^<]+?)</strong>(.*?)</p>\s*</blockquote>", callout, body, flags=re.S)

    # tables: wrap, mark numeric cells
    def table(m):
        inner = m.group(1)
        cols = len(re.findall(r"<th", (re.search(r"<thead>.*?</thead>", inner, re.S) or [""])[0] if re.search(r"<thead>.*?</thead>", inner, re.S) else ""))
        inner = re.sub(r"<td>([−\-+]?[\d.,]+\s?(?:%|×|x|ms|s|MB|GB|K|M|B)?)</td>", r'<td class="num">\1</td>', inner)
        inner = re.sub(r'<td style="text-align:right">', '<td class="num">', inner)
        return f'<div class="tw{" wide" if cols >= 8 else ""}"><table>{inner}</table></div>'
    body = re.sub(r"<table>(.*?)</table>", table, body, flags=re.S)
    body = re.sub(r"<p><strong>([^<]{1,40})</strong></p>\s*(?=<div class=\"tw)", r'<div class="tlabel">\1</div>', body)

    # parts (h1), sections (h2), subsections (h3)
    secs = [(int(n), re.sub(r"\s*\(\d{4}-\d\d-\d\d\)\s*$", "", t)) for n, t in re.findall(r"<h2>(\d+)\. ([^<]+)</h2>", body)]
    parts = []
    for m in re.finditer(r"<h1>(.*?)</h1>", body):
        nxt = re.search(r"<h2>(\d+)\.", body[m.end():])
        parts.append((m.group(1), int(nxt.group(1)) if nxt else 10 ** 9))
    def part_of(n):
        k = -1
        for i, (_, first) in enumerate(parts):
            if n >= first: k = i
        return k

    pi = [0]
    def part(m):
        i = pi[0]; pi[0] += 1
        raw_t = re.sub(r"<[^>]+>", "", m.group(1))
        k, _, t = raw_t.partition("·") if "·" in raw_t else raw_t.partition(":")
        k, t = (k.strip(), t.strip()) if t else ("", raw_t.strip())
        sub = m.group(2) or ""
        items = "".join(f'<div><span class="coin coin--sm">{n}</span>{html.escape(st)}</div>' for n, st in secs if part_of(n) == i)
        return (f'<section class="part a-{ACCENTS[i % 6]}"><div class="part__inner">'
                f'<div class="part__k">{html.escape(k)}</div><div class="part__t">{html.escape(t)}</div>'
                f'{f"<div class=part__s>{sub}</div>" if sub else ""}'
                f'{f"<div class=part__list>{items}</div>" if items else ""}</div></section>')
    body = re.sub(r"<h1>(.*?)</h1>\s*(?:<p><em>(.*?)</em></p>)?", part, body, flags=re.S)

    def h2(m):
        n, t = int(m.group(1)), m.group(2)
        t = re.sub(r"\s*\((\d{4}-\d\d-\d\d)\)\s*$", r' <span class="date">\1</span>', t)
        acc = ACCENTS[part_of(n) % 6] if parts and part_of(n) >= 0 else COINS[n % 4]
        return f'<h2 class="ch a-{acc}" id="s{n}"><span class="coin">{n}</span><span>{t}</span></h2>'
    body = re.sub(r"<h2>(\d+)\. ([^<]+)</h2>", h2, body)
    body = re.sub(r"<h2>([^<]+)</h2>", r'<h2 class="ch minor">\1</h2>', body)
    body = re.sub(r"<h3>(\d+(?:\.\d+)+) (.*?)</h3>", lambda m: f'<h3><span class="h3n">{m.group(1)}</span>'
                  + re.sub(r"\s*\((\d{4}-\d\d-\d\d)\)\s*$", r' <span class="date">\1</span>', m.group(2)) + "</h3>", body)

    # contents
    toc = ""
    if len(secs) >= 3 and str(meta.get("toc", "true")).lower() != "false":
        if parts:
            groups = [(re.sub(r"<[^>]+>", "", p[0]), [s for s in secs if part_of(s[0]) == i]) for i, p in enumerate(parts)]
        else:
            groups = [("Sections", secs)]
        toc = '<section class="toc"><div class="toc__h">Contents</div><div class="toc__grid">' + "".join(
            f'<div class="toc__part a-{ACCENTS[i % 6]}"><div class="toc__p">{html.escape(g)}</div>' + "".join(
                f'<a class="toc__i a-{COINS[n % 4] if not parts else ACCENTS[i % 6]}" href="#s{n}"><span class="coin coin--sm">{n}</span>{html.escape(t)}</a>'
                for n, t in items) + "</div>" for i, (g, items) in enumerate(groups) if items) + "</div></section>"

    # cover
    cover = ""
    if meta.get("subtitle") or meta.get("stats") or meta.get("kicker"):
        def as_list(v): return v if isinstance(v, list) else ([v] if v else [])
        badges = "".join(
            f'<span class="badge badge--subtle badge--{(b.split("|") + ["blue"])[1].strip() or "blue"}">{html.escape(b.split("|")[0].strip())}</span>'
            for b in as_list(meta.get("badges")))
        stats = "".join(
            f'<div class="stat"><div class="stat__n" style="color: var(--{ACCENTS[i % 6]}-{"700" if ACCENTS[i % 6] in ("blue", "purple") else "800"})">{html.escape(s.split("|")[0].strip())}</div>'
            f'<div class="stat__l">{html.escape((s.split("|") + [""])[1].strip())}</div></div>'
            for i, s in enumerate(as_list(meta.get("stats"))[:4]))
        cover = f'''<section class="cover"><div class="cover__field"></div>
<svg class="cover__art" viewBox="0 0 92 100" aria-hidden="true"><g transform="translate(46 62)">
<path d="M0 -22 L36 -1 L0 20 L-36 -1Z" style="fill: var(--blue-400)"/><path d="M-36 -1 L0 20 L0 32 L-36 11Z" style="fill: var(--blue-600)"/><path d="M36 -1 L0 20 L0 32 L36 11Z" style="fill: var(--blue-700)"/>
<g transform="translate(0 -17)"><path d="M0 -15 L26 0 L0 15 L-26 0Z" style="fill: var(--pear-500)"/><path d="M-26 0 L0 15 L0 23 L-26 8Z" style="fill: var(--pear-600)"/><path d="M26 0 L0 15 L0 23 L26 8Z" style="fill: var(--pear-700)"/></g>
<g transform="translate(0 -31)"><path d="M0 -9 L16 0 L0 9 L-16 0Z" style="fill: var(--pink-400)"/><path d="M-16 0 L0 9 L0 14 L-16 5Z" style="fill: var(--pink-600)"/><path d="M16 0 L0 9 L0 14 L16 5Z" style="fill: var(--pink-700)"/></g>
<circle cx="-30" cy="-46" r="6" style="fill: var(--yellow-400)"/><rect x="24" y="-56" width="13" height="13" rx="3.5" style="fill: var(--teal-300)" transform="rotate(14 30 -50)"/></g></svg>
<div class="cover__body">{f'<div class="cover__kicker">{html.escape(meta["kicker"])}</div>' if meta.get("kicker") else ""}
<h1 class="cover__title">{html.escape(meta.get("title", md_path.stem))}</h1>
{f'<div class="cover__subtitle">{html.escape(meta["subtitle"])}</div>' if meta.get("subtitle") else ""}
{f'<p class="cover__lead">{html.escape(meta["lead"])}</p>' if meta.get("lead") else ""}
{f'<div class="cover__badges">{badges}</div>' if badges else ""}</div>
{f'<div class="cover__stats">{stats}</div>' if stats else ""}
<div class="cover__meta"><span>{html.escape(meta.get("meta_left", ""))}</span><span>{html.escape(meta.get("meta_right", ""))}</span></div></section>'''
    elif meta.get("title"):
        body = f'<h1 style="font: 500 34pt/1.05 var(--font-display); letter-spacing: -.02em; margin: 0 0 8mm">{html.escape(meta["title"])}</h1>' + body

    css = "".join((ROOT / p).read_text() for p in ("tokens/fonts.css", "tokens/tokens.css", "css/brilliant.css", "css/print.css"))
    css = css.replace('url("fonts/', 'url("' + (ROOT / "tokens" / "fonts").as_uri() + '/')  # bundled OFL fonts, offline-safe
    short = meta.get("short_title") or meta.get("title", md_path.stem)
    css += '\n@page { @bottom-left { content: "' + short.replace('"', "'") + '"; } }\n'
    css += "body.doc{background:#fff} .doc .badge{font-size:7.5pt}\n"
    if katex_dir:
        kd = pathlib.Path(katex_dir).expanduser().resolve()
        katex_head = (f'<link rel="stylesheet" href="{(kd / "katex.min.css").as_uri()}">'
                      f'<script defer src="{(kd / "katex.min.js").as_uri()}"></script>')
    else:
        katex_head = ('<link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/katex@0.16.11/dist/katex.min.css">'
                      '<script defer src="https://cdn.jsdelivr.net/npm/katex@0.16.11/dist/katex.min.js"></script>')
    render = ("<script>addEventListener('load',()=>{if(window.katex)document.querySelectorAll('span.math, div.eq').forEach(el=>{"
              "const d=el.tagName==='DIV',t=el.textContent.trim().replace(/^\\\\[\\[(]/,'').replace(/\\\\[\\])]$/,'');"
              "try{katex.render(t,el,{displayMode:d,throwOnError:false})}catch(e){}});document.body.dataset.ready=1})</script>")
    has_math = "\\(" in body or "\\[" in body
    return (f'<!doctype html><html lang="en" data-theme="light"><head><meta charset="utf-8"><title>{html.escape(meta.get("title", md_path.stem))}</title>'
            f'{katex_head if has_math else ""}<style>{css}</style></head><body class="doc">{cover}{toc}<main>{body}</main>'
            f'{render if has_math else "<script>document.body.dataset.ready=1</script>"}</body></html>')


def to_pdf(html_path: pathlib.Path, pdf_path: pathlib.Path) -> None:
    from playwright.sync_api import sync_playwright
    with sync_playwright() as p:
        b = p.chromium.launch()
        pg = b.new_page()
        pg.goto(html_path.resolve().as_uri(), wait_until="load", timeout=60000)
        try:
            pg.wait_for_selector("body[data-ready]", timeout=15000)
        except Exception:
            pass
        pg.evaluate("document.fonts.ready")
        pg.wait_for_timeout(400)
        pg.pdf(path=str(pdf_path), prefer_css_page_size=True, print_background=True)
        b.close()


def main():
    ap = argparse.ArgumentParser(description="Markdown → Brilliant-style PDF")
    ap.add_argument("markdown")
    ap.add_argument("-o", "--out", help="output PDF (default: <markdown>.pdf)")
    ap.add_argument("--html", help="also keep the intermediate HTML here")
    ap.add_argument("--katex", help="local KaTeX dist dir (katex.min.css + katex.min.js)")
    a = ap.parse_args()
    src = pathlib.Path(a.markdown)
    out = pathlib.Path(a.out) if a.out else src.with_suffix(".pdf")
    html_path = pathlib.Path(a.html) if a.html else out.with_suffix(".html")
    html_path.write_text(build(src, a.katex), encoding="utf-8")
    to_pdf(html_path, out)
    if not a.html:
        html_path.unlink()
    print(f"done: {out}")


if __name__ == "__main__":
    main()
