#!/usr/bin/env python3
"""Generate Brilliant's isometric hero lattice as a vector SVG data URI (no masks, no alpha
gradients, so it stays vector in print/PDF/SVG exports).

Measured on brilliant.org: 30°/150° hairlines on a 72×42px tile (64×37 at ≥1280px), colour
rgba(236,230,225,.6) on oat #f5f3f1, fading out towards the top (full strength for the bottom 40%).
The fade is done by stroking with an opaque gradient from the background colour to the line colour.

    python3 tools/lattice.py            # prints the CSS custom properties used in css/*.css
"""
import urllib.parse


def lattice(w, h, tw, th, bg, line, fade_to=0.6, stroke=1.1, unit=""):
    k_run = h * tw / th                     # horizontal run of a line across the full height
    lines = []
    start = -int((k_run + w / 2) // tw) - 1
    stop = int((k_run + w / 2) // tw) + 2
    for k in range(start, stop):
        x0 = w / 2 + k * tw
        lines.append(f"M{x0:.1f} {h}L{x0 - k_run:.1f} 0")
        lines.append(f"M{x0:.1f} {h}L{x0 + k_run:.1f} 0")
    svg = (f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}{unit}" height="{h}{unit}" viewBox="0 0 {w} {h}">'
           f'<defs><linearGradient id="g" gradientUnits="userSpaceOnUse" x1="0" y1="0" x2="0" y2="{h}">'
           f'<stop offset="0" stop-color="{bg}"/><stop offset="{1 - fade_to:.2f}" stop-color="{line}"/></linearGradient></defs>'
           f'<path d="{"".join(lines)}" stroke="url(#g)" stroke-width="{stroke}" fill="none"/></svg>')
    return "data:image/svg+xml," + urllib.parse.quote(svg, safe="/:=,.- ")


VARIANTS = {
    # web hero (48% of the hero, bottom-aligned): light + dark, two tile sizes
    "--lattice-hero": dict(w=2880, h=440, tw=72, th=42, bg="#f5f3f1", line="#ece6e1"),
    "--lattice-hero-2xl": dict(w=2880, h=440, tw=64, th=37.33, bg="#f5f3f1", line="#ece6e1"),
    "--lattice-hero-dark": dict(w=2880, h=440, tw=72, th=42, bg="#383838", line="#474747"),
    # full-field (OG cards, deck title slides): fades over the whole height
    "--lattice-field": dict(w=2400, h=1080, tw=72, th=42, bg="#f5f3f1", line="#ebe5e0", fade_to=0.9),
    # print: millimetre units for A4 covers and part pages
    "--lattice-print": dict(w=210, h=170, tw=19, th=11.08, bg="#f5f3f1", line="#e2dbd5", stroke=0.28, unit="mm"),
}

if __name__ == "__main__":
    for name, v in VARIANTS.items():
        print(f'  {name}: url("{lattice(**v)}");')
