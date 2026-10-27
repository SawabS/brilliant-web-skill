# md2pdf — Markdown → Brilliant-style PDF

```bash
pip install markdown-it-py playwright && playwright install chromium
python3 md2pdf.py report.md                       # → report.pdf
python3 md2pdf.py report.md -o out.pdf --html out.html
python3 md2pdf.py report.md --katex /path/to/katex/dist   # offline maths
```

Generic version of the Scaling-v5 pipeline: Markdown → one HTML file (cover, contents, part openers, numbered "coins",
callouts, black-header tables, figures on oat stages, code slabs, KaTeX, Mermaid via `mmdc`) → Chromium PDF with named
pages and `@page` footers. Nothing report-specific is hard-coded; everything comes from front matter and Markdown
conventions, documented at the top of `md2pdf.py` and in `../../references/04-documents.md`.

Try it: `python3 md2pdf.py example/sample-report.md` (see `example/sample-report.pdf`).
