# Slide decks

Template: `templates/deck.html` + `css/deck.css`. Slides are authored at **1920×1080** and scaled to fit the window; ← → / space / PageUp/Down navigate, `F` goes fullscreen, `#3` deep-links a slide, and printing produces one slide per PDF page (Chromium: `page.pdf(prefer_css_page_size=True, print_background=True)`).

## Slide types

| Type | Build |
|---|---|
| **Title** | `.slide--oat` + `.slide__lattice`; kicker with dash; serif `.s-display-xl` (132px) title; `.s-headline` subtitle in secondary; isometric tile art top-right; footer. |
| **Part opener** | `.slide--oat` + lattice; hue kicker (`--k: var(--text-purple-primary)`); `.s-display` (96px) title; one-line `.s-body`. |
| **Finding + numbers** | kicker; `.s-display-sm` (72px) headline that **is the finding**; three `.s-stat` tiles (radius 44, 2px border, sans 88px numbers in hue ink) at the bottom. |
| **Chart** | kicker names the measure; headline states what the chart shows; chart in an oat `.s-media` (radius 40) with direct labels. |
| **Two cards** | headline; `.s-cols` of two `.s-card`s (radius 40, tinted with `--c-bg`, `--c-ink`): Do / Don't, Before / After, Option A / B. |
| **Quick check** | a question headline; `.choices.choices--2` lip tiles at deck scale; a dark 3D **Check**. For live teaching. |
| **Quote** | oat; serif 72px quote with curly quotes; tertiary attribution. |
| **Closing** | `.slide--dark` (gray-950), white serif "Questions?" or a call to action, white `.btn--hero`. |

## Rules

- **One idea per slide.** The headline states the takeaway ("Unigram beats BPE at every size"); the kicker names the topic ("Summary", "Boundary F1 by size").
- Body text ≤ 30 words per slide; 28–30px minimum; captions 22px.
- Margins 96px top/bottom, 120px sides; footer 48px from the bottom (short title left, slide number right) in 20px tertiary.
- Colour: white or oat slides; at most two hues per slide; one dark slide (the close) per deck.
- Stats: three per slide, never four; numbers in sans 400 (not serif), hue-coloured, with a one-line label and a tertiary note.
- Charts: same rules as `06-interactive-visuals.md`, scaled ×2 (lines 7px, labels 22–26px).
- Section rhythm: Title → (Part opener → 2–5 content slides)× → Close. Rotate part hues blue, purple, green, orange.
- No bullet walls, no logos grid, no stock photos, no drop shadows, no slide transitions beyond the 300ms fade.

## Other slide tools

- **PowerPoint / Keynote / Google Slides**: 16:9; title font Source Serif 4 Medium (or CoFo Robert if licensed) at 54–66pt; body Inter 20–24pt; background white or #F5F3F1; accents #456DFF, #29CC57, #9D62FF, #FF8D23; rounded rectangles radius ≈ 0.25in with 1.5pt #E5E5E5 outline and no shadow; tables with a black header row.
- **Claude Slides artifacts**: use these same values as the theme (fonts, colours, radius), and keep the one-finding-per-slide headline rule.
