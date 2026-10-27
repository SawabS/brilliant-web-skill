#!/usr/bin/env python3
"""Export an HTML page (or one element of it) as a true vector SVG for READMEs and docs.

    python3 tools/export_vector.py templates/landing.html preview/screens/landing.svg --width 1440 --height 900
    python3 tools/export_vector.py preview/index.html out.svg --selector "#buttons" --theme dark

Chromium prints the page with screen styles to a PDF whose page size equals the captured
area, then poppler's `pdftocairo -svg` converts it: text becomes glyph outlines (renders the
same everywhere, no font loading), shapes stay shapes. Blurred shadows are the only raster
bits. Requires: playwright (chromium) and poppler-utils."""
import argparse, pathlib, subprocess, tempfile
from playwright.sync_api import sync_playwright

ap = argparse.ArgumentParser()
ap.add_argument("page"); ap.add_argument("out")
ap.add_argument("--width", type=int, default=1440); ap.add_argument("--height", type=int, default=0, help="0 = full page")
ap.add_argument("--theme", default="light"); ap.add_argument("--selector", default="")
ap.add_argument("--hash", default=""); ap.add_argument("--wait", type=int, default=600)
ap.add_argument("--script", default="", help="JS to run before capture")
ap.add_argument("--keep-pdf", default="", help="also keep the intermediate PDF here")
a = ap.parse_args()

with sync_playwright() as p:
    b = p.chromium.launch()
    pg = b.new_page(viewport={"width": a.width, "height": a.height or 900})
    pg.goto(pathlib.Path(a.page).resolve().as_uri() + (("#" + a.hash) if a.hash else ""), wait_until="load")
    pg.evaluate(f"document.documentElement.dataset.theme = '{a.theme}'")
    if a.script: pg.evaluate(a.script)
    pg.evaluate("document.fonts.ready"); pg.wait_for_timeout(a.wait)
    pg.emulate_media(media="screen", reduced_motion="reduce")
    # freeze animations so the capture is a still
    pg.add_style_tag(content="*,*::before,*::after{animation:none!important;transition:none!important;caret-color:transparent!important}")
    if a.selector:
        box = pg.eval_on_selector(a.selector, "e => { const r = e.getBoundingClientRect(); return [r.left + scrollX, r.top + scrollY, r.width, r.height]; }")
    else:
        h = a.height or pg.evaluate("Math.ceil(document.documentElement.getBoundingClientRect().height)") + 2
        box = [0, 0, a.width, h]
    import math
    x, y, w, h = round(box[0]), round(box[1]), math.ceil(box[2]), math.ceil(box[3])
    # isolate the area: shift the page so the box sits at 0,0 and size the PDF page to it
    css = f"@page {{ size: {w}px {h}px; margin: 0; }} * {{ break-inside: auto !important; break-before: auto !important; break-after: auto !important; }} .export-flat {{ background: none !important; }}"
    if a.selector:  # isolate one element: shift it to the page origin
        css += f" html {{ width: {a.width}px; overflow: hidden !important; }} body {{ transform: translate({-x}px, {-y}px); transform-origin: 0 0; }}"
    pg.add_style_tag(content=css)
    # fixed bars would repeat or drift in print: pin them where they sit on screen; hide deck chrome.
    # Alpha-gradient veils turn into grey bands in pdftocairo, so elements marked .export-flat lose
    # their background in the export (see .level__head in templates/app-course.html).
    pg.evaluate("""document.querySelectorAll('body *').forEach(e => {
      if (e.classList.contains('deck__nav')) { e.style.display = 'none'; return; }
      if (getComputedStyle(e).position === 'fixed') e.style.setProperty('position', 'absolute', 'important');
    })""")
    with tempfile.TemporaryDirectory() as t:
        pdf = pathlib.Path(a.keep_pdf) if a.keep_pdf else pathlib.Path(t) / "page.pdf"
        pg.pdf(path=str(pdf), width=f"{w}px", height=f"{h}px", print_background=True, page_ranges="1")
        subprocess.run(["pdftocairo", "-svg", "-f", "1", "-l", "1", str(pdf), a.out], check=True)
    b.close()
out = pathlib.Path(a.out)
# shrink: 2-decimal coordinates are sub-pixel accurate at any README size
import re
svg = out.read_text()
svg = re.sub(r"(?<![#\w])(-?\d+\.\d{3,})", lambda m: f"{float(m.group(1)):.2f}".rstrip("0").rstrip("."), svg)
svg = re.sub(r">\s+<", "><", svg)
# pdftocairo writes pt units (0.75 px); declare the true pixel size so it displays 1:1
svg = re.sub(r'<svg([^>]*?) width="[\d.]+" height="[\d.]+"', lambda m: f'<svg{m.group(1)} width="{w}" height="{h}"', svg, count=1)
out.write_text(svg)
print(f"{out}  {w}x{h}  {out.stat().st_size // 1024} KB")
