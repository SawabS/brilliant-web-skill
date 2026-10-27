# Documents and PDFs

Brilliant has no print system of its own, so this is its web language translated to paper (`css/print.css`): white A4 pages, serif display titles, sans body, hue "coins" for section numbers, tertiary-tint callouts, the **black table header**, black code slabs, oat stages behind figures, and the isometric lattice on cover and part pages. Lips become flat in print except on the small section coins.

## Fastest path: Markdown → PDF

```bash
pip install markdown-it-py playwright && playwright install chromium   # once
python3 tools/md2pdf/md2pdf.py report.md                               # → report.pdf
python3 tools/md2pdf/md2pdf.py report.md -o out.pdf --html out.html    # keep the HTML to tweak
python3 tools/md2pdf/md2pdf.py report.md --katex ~/md2pdf/node_modules/katex/dist   # offline maths
```

It is the generic, restyled version of the Scaling-v5 pipeline: one HTML file, printed by Chromium with named pages (`cover`, `part`) and `@page` margin boxes for the footer, so no merge step is needed. Mermaid blocks render through `mmdc` with `tools/md2pdf/mermaid.json` (Brilliant palette, rounded nodes); without `mmdc` they print as code.

### Markdown conventions

```markdown
---
title: Scaling study
subtitle: What 240 tokenizers taught us
kicker: Research report · Kurdish tokenizer
lead: One or two sentences under the title on the cover.
short_title: Scaling study · v5            # running footer
badges: [Training complete · 240 / 240 | green, Evaluated | blue]
stats: [240 | tokenizers trained, 8 | vocabulary sizes, 15 | mixtures, 264 | evaluated]
meta_left: Created 24 Oct 2026 · updated 27 Oct 2026
meta_right: SentencePiece 0.2.1 · 20 h CPU
toc: true
---

# Part I · The study
*What was asked, and how the experiment is built.*      ← part opener page + subtitle

## 1. Summary (2026-10-24)                                 ← coin "1" + date pill
```stats
240 | tokenizers trained | 0 failures
0.589 | best boundary F1 | Unigram 16K
```
### 1.1 Variables                                         ← muted number
> **Note.** Blue callout.        > **Caveat.** Yellow.   > **Done.** Green.
> **Definition.** Purple.        > **Failure.** Red.

![Alt text](figs/f1.svg)
*Figure 1. Caption that says what to see.*

**Unigram**                                               ← dark label above the next table
| Size | F1 |
|---|---|
```

Numeric cells are right-aligned automatically. A paragraph that is only `**Label**` right before a table becomes a black pill label. `$…$` and `$$…$$` render with KaTeX.

## Page anatomy (A4)

| Element | Spec |
|---|---|
| Margins | 18 / 17 / 20 / 17 mm; cover and part pages full-bleed |
| Body | sans 9.8pt / 1.6, `#1e1e1e`; bold in black |
| Cover | top 158mm oat field with the lattice and isometric tile art; kicker 9pt blue-700 uppercase; title serif 54pt/500 −.025em; subtitle sans 17pt 60% black; lead 11pt; subtle badges; four stat tiles (1px oat border, radius 6mm, hue-coloured sans numbers); meta line 8pt 40% black |
| Contents | serif 30pt "Contents", two-column part cards (1px gray-200, radius 4.5mm) with coin-numbered entries |
| Part opener | full oat page, lattice rising, hue kicker, serif 50pt title, 13pt subtitle, white list card of the part's sections |
| Section (H2) | hue **coin** (9mm pill, white number, 0.9mm darker lip) + serif 21pt title; 11mm above, 5mm below |
| Subsection (H3) | sans 12pt/700 with a 40% number |
| Stat tiles | 3-up, 1px gray-200, radius 4.5mm; value sans 19pt in the hue ink; label 8.8pt/600; note 7.8pt 50% |
| Callouts | tertiary tints (blue-100, green-100, yellow-100, purple-100, red-100), radius 4mm, 7.4pt uppercase tag in the 700/800 ink |
| Tables | 1px gray-200 frame, radius 3.5mm, **black header row** with white 7.8pt bold, 8.4pt cells, gray-100 row rules, wide tables shrink to 7.5pt |
| Figures | oat stage, radius 4.5mm, caption 8.2pt 60% with a bold "Figure N." |
| Code | black slab, radius 4mm, 7.8pt Source Code Pro, pear language tag, probe syntax colours |
| Equations | purple-50 panel, centred |
| Footer | short title left, page number right, 7.5pt |

Rotate accents by part: blue, orange, purple, green, pink, teal. Section coins without parts rotate blue, orange, purple, green so neighbours differ.

## Hand-built documents

Start from `templates/document.html` (generated from the example) or write HTML with the classes above and print from Chromium/Playwright:

```python
page.pdf(path="out.pdf", prefer_css_page_size=True, print_background=True)
```

Rules for any printed piece:
- Every figure has a numbered caption that says what to see; every number is traceable.
- Titles state the finding ("Unigram beats BPE at every size"), not the topic ("Results").
- One serif title per page at most, besides section titles.
- Keep `break-inside: avoid` on figures, callouts, code and table rows (already in `print.css`).
- Charts for print: SVG, Inter text, series in the chart order (blue-500, orange-500, purple-500, teal-500, pink-500, yellow-600), direct line labels in the hue's 700 ink, light grid, no chart border.
- Fonts: the substitutes load from Google Fonts when online; offline, install Inter and Source Serif 4 locally or the PDF falls back to Helvetica/Georgia.

## Other document formats

- **Word / Google Docs**: headings in Source Serif 4 500 (Title 28pt, H1 20pt), body Inter 10.5pt, tables with a black header row and white bold text, callouts as shaded single-cell tables in the tertiary tints.
- **Email**: system-safe version: Arial/Helvetica 16px, black text, one green or black pill button (`border-radius: 999px`), oat (#f5f3f1) footer band.
