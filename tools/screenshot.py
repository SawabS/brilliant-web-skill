#!/usr/bin/env python3
"""Screenshot HTML pages with Playwright (light and dark) for visual QA.
    python3 tools/screenshot.py <page.html> <out-prefix> [width] [height] [--full]
Writes <out-prefix>-light.png and <out-prefix>-dark.png."""
import sys, pathlib
from playwright.sync_api import sync_playwright
page_path, prefix = sys.argv[1], sys.argv[2]
w = int(sys.argv[3]) if len(sys.argv) > 3 and sys.argv[3].isdigit() else 1440
h = int(sys.argv[4]) if len(sys.argv) > 4 and sys.argv[4].isdigit() else 900
full = "--full" in sys.argv
with sync_playwright() as p:
    b = p.chromium.launch()
    for theme in ("light", "dark"):
        pg = b.new_page(viewport={"width": w, "height": h}, device_scale_factor=1)
        errors = []
        pg.on("pageerror", lambda e: errors.append(str(e)))
        pg.goto(pathlib.Path(page_path).resolve().as_uri(), wait_until="load")
        pg.evaluate(f"document.documentElement.dataset.theme='{theme}'")
        pg.wait_for_timeout(700)
        pg.screenshot(path=f"{prefix}-{theme}.png", full_page=full)
        if errors: print("JS errors:", errors)
        pg.close()
    b.close()
print("ok", prefix)
