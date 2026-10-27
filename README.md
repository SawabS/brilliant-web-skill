# Brilliant Web Skill

An agent skill (and a plain CSS/JS kit) that reproduces the **brilliant.org design language** for web apps, landing pages, lesson players, dashboards, PDF documents, slide decks and interactive visuals.

Every colour, text style, radius, spacing step, shadow, breakpoint, z-index and keyframe was **extracted from brilliant.org's production CSS** (Panda CSS, captured 27 October 2026) and turned into tokens; component geometry was measured from the live markup with Playwright. The logged-in lesson experience, which isn't public, is reconstructed from those tokens and refined with patterns from [AI Engineering Blueprint](https://sawabs.github.io/ai-engineering-blueprint/).

![Specimen](preview/screenshots/specimen.png)

## What's inside

```
SKILL.md                 ← entry point for Claude / agents: rules, file map, checklist
tokens/                  ← tokens.css (light + dark), fonts.css, tokens.json (DTCG), tailwind.preset.js
css/                     ← brilliant.css (components) · print.css (A4 documents) · deck.css (16:9 slides)
js/brilliant.js          ← theme toggle, segmented/chips/tabs/choices, slider fill, beat reveal, synthesized sounds
assets/icons.svg         ← original 24px icon sprite
templates/               ← landing · app-course · app-lesson · dashboard · interactive · deck · document
tools/md2pdf/            ← Markdown → Brilliant-style PDF (cover, contents, parts, coins, callouts, Mermaid, KaTeX)
tools/                   ← build_tokens.py, build_token_docs.py, capture/extract_tokens.py, screenshot.py, inline_icons.py
references/              ← 01 foundations … 10 token tables
source/                  ← the raw captured token values
preview/                 ← index.html specimen + screenshots
```

## Use it as a skill

Claude Code / Agent SDK:

```bash
git clone https://github.com/SawabS/brilliant-web-skill ~/.claude/skills/brilliant-design
```

Then ask for "a Brilliant-style …" (landing page, lesson, dashboard, report PDF, deck, explorable). The agent reads `SKILL.md`, picks a template and the matching reference, and builds with the tokens.

## Use it directly

```html
<link rel="stylesheet" href="tokens/fonts.css">
<link rel="stylesheet" href="tokens/tokens.css">
<link rel="stylesheet" href="css/brilliant.css">
<script src="js/brilliant.js" defer></script>

<h1 class="ts-display-6xl">Learn by doing</h1>
<button class="btn3d btn3d--blue"><span class="btn3d__face">Start</span></button>
```

Tailwind: `presets: [require('./tokens/tailwind.preset.js')]` (keep `tokens.css` loaded; colours resolve through CSS variables so `data-theme="dark"` just works).

PDF from Markdown:

```bash
pip install markdown-it-py playwright && playwright install chromium
python3 tools/md2pdf/md2pdf.py report.md          # → report.pdf
```

## Screens

| Landing | Course map | Lesson (mobile) |
|---|---|---|
| ![](preview/screenshots/landing.png) | ![](preview/screenshots/course.png) | ![](preview/screenshots/lesson-mobile.png) |

| Dashboard (dark) | Interactive | Deck |
|---|---|---|
| ![](preview/screenshots/dashboard-dark.png) | ![](preview/screenshots/interactive.png) | ![](preview/screenshots/deck.png) |

## Fonts and brand

Brilliant's typefaces (CoFo Brilliant, CoFo Robert, CoFo Semi Mono by Contrast Foundry) are commercial and **not included**; the stacks put them first, so they're used if you license and install them, and fall back to Inter, Source Serif 4 and DM Mono. Source Code Pro and KaTeX are exact.

This repository reproduces a visual language, not a brand: it contains no Brilliant logo, wordmark, characters, illustrations or animations, and the templates use a placeholder product name ("Lumen"). Don't use it to build anything that could be mistaken for brilliant.org.

## Refreshing the tokens

```bash
# capture main.css from brilliant.org (any scraper/browser), then:
python3 tools/capture/extract_tokens.py main.css source/brilliant-tokens.json
python3 tools/build_tokens.py && python3 tools/build_token_docs.py
python3 tools/inline_icons.py templates/*.html preview/index.html
```

