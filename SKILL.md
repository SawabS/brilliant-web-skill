---
name: brilliant-design
description: Build web apps, landing pages, lesson players, dashboards, PDF documents, slide decks and interactive visuals in the Brilliant.org design language (tokens captured from production). Use whenever the user asks for a Brilliant-style, Brilliant-like, "learn by doing", tactile 3D-button, course/lesson or explorable-explanation look, or names this skill.
---

# Brilliant design system

A faithful, token-level replica of the visual language of brilliant.org: a white canvas and black ink, a medium-weight serif for big ideas, a friendly sans for everything else, pill-shaped controls with a solid **lip** that sinks when pressed, an oat-coloured stage for diagrams, and colour that always means something (a course, a result, a reward).

Every colour, text style, radius, spacing step, shadow, breakpoint, z-index and keyframe in `tokens/` was extracted from brilliant.org's production Panda CSS (October 2026). Component geometry was measured from the live markup. Logged-in lesson internals, which are not public, were reconstructed from those tokens and refined with the author's Brilliant-style course (AI Engineering Blueprint). `references/09-source-notes.md` says which is which.

## Files

| Path | What it is |
|---|---|
| `tokens/tokens.css` | All tokens as CSS variables: 174 primitives, 186 semantic roles × light/dark, 34 text styles (`.ts-*` classes), scales, motion. **Load first.** |
| `tokens/fonts.css` · `tokens/fonts/` | Bundled OFL substitutes for the licensed CoFo faces — **Besley** (CoFo Robert, a Clarendon), Inter (CoFo Brilliant), DM Mono (CoFo Semi Mono) — plus exact Source Code Pro. Works offline; a Google-Fonts import covers single-file pages. |
| `tokens/tokens.json` · `tokens/tailwind.preset.js` | Same tokens as DTCG JSON and a Tailwind preset. |
| `css/brilliant.css` | Every component: 3D buttons, pills, badges, chips, segmented, tabs, cards, course map, lesson nodes, lesson player, feedback, inputs, slider, code, callouts, tables, overlays, motion, and the vector hero lattice (`--lattice-*`). |
| `css/print.css` · `css/deck.css` | Paged A4 documents; 1920×1080 decks. |
| `js/brilliant.js` | Theme toggle, segmented/chips/tabs/choices wiring, slider fill, beat reveal, the synthesized sound set (`B.sfx.correct()` …), **lesson-node rendering** (`B.node()`, `.lesson-node` → SVG) and the path rhythm (`B.layoutPath()`). |
| `assets/icons.svg` | Original 24px icon sprite (`#i-check`, `#i-x`, …). Run `tools/inline_icons.py` so pages work from `file://`. |
| `templates/` | Working starting points: `landing`, `app-course`, `app-lesson`, `dashboard`, `interactive`, `deck`, `document`, `social-card` (1200×630 Open Graph). |
| `tools/md2pdf/md2pdf.py` | Markdown → Brilliant-style PDF (cover, contents, part openers, coins, callouts, black-header tables, Mermaid, KaTeX). |
| `references/` | The rules. Read the one for your output before building. |
| `tools/export_vector.py` | Any page or element → true vector SVG (README art, docs, Figma). `tools/lattice.py` regenerates the lattice SVGs. |
| `preview/index.html` · `preview/poster.html` · `preview/svg/` | Living specimen, the README poster, and vector exports of every template. |

## How to use it

1. **Pick the starting template** closest to the request and copy it (keep the `<link>`s to `tokens/fonts.css`, `tokens/tokens.css`, `css/brilliant.css`, and `js/brilliant.js` if it is interactive). For a single self-contained file (an artifact, an email-able page), inline those files' contents into `<style>`/`<script>` instead of linking.
2. **Read the reference for the output type**:
   - web app, product UI, dashboard → `references/03-web-patterns.md` + `02-components.md`
   - marketing / landing page → `03-web-patterns.md` (Marketing)
   - document / report / PDF → `04-documents.md` (prefer `tools/md2pdf` for anything long)
   - slide deck → `05-decks.md`
   - interactive visual, explorable, chart, diagram, lesson → `06-interactive-visuals.md`
   - copy and microcopy → `07-voice-and-content.md`
3. **Use roles, never raw hex**: `var(--text-secondary)`, `var(--bg-oat)`, `var(--border-solid)`. Ramps (`--blue-500`) are for charts, illustrations and course hues only.
4. **Verify by looking**: screenshot light and dark (`python3 tools/screenshot.py page.html out 1440 900 --full`), check 320px width, and run the checklist at the end of this file. For crisp images in a README or doc, export vector: `python3 tools/export_vector.py page.html out.svg --width 1440 --height 900 [--theme dark] [--selector '#id']`.

## The rules that make it look like Brilliant

1. **White and black first.** `--bg-primary` canvas, `--text-primary` ink. Most of any screen is white space and black type. Long copy uses `--text-secondary` (60% black); captions and inactive labels `--text-tertiary` (40%).
2. **Serif for big ideas, sans for everything else.** Display styles (`.ts-display-*`, 24–76px, weight 500, tight negative tracking) are the serif — a sharp Clarendon. Campaign headlines put their key words in the serif *italic* with `<em>` ("Your personal tutor for <em>maths</em> and <em>code</em>"). Headings are the sans at 700. UI labels are the sans at 500. Never bold the serif; never use the serif below 24px.
3. **One lip-pressed primary per view.** The product CTA is the **3D button**: face `--bg-inverse-secondary` (#383838) resting 4px above a black lip, 100ms ease-out press. Course actions use the blue 3D button; a correct answer's Continue is green. Marketing CTAs are flat pills (green `--bg-success-primary`, h60, radius full, soft 0 4px 7px shadow).
4. **Depth is a solid lip, never a blur.** Tiles, choices, level headers and inputs that you press sit on `0 4px 0 0 <lip>`; on `:active` they translate down 4px and the lip disappears. Blurred shadows are only for floating surfaces (`--shadow-elevation-base/md/lg`).
5. **Everything is rounded generously.** Buttons and chips are pills (54–60px). Cards 20px (`--radius-2xl`), lesson popovers 40px, marketing bands and stat tiles 44px, modals 32px, inputs 12px, badges 12px.
6. **Borders are 2px in product, 1px in marketing.** Product cards: 2px `--border-primary` (10% black). Choices and lip tiles: 2px `--border-solid` (#e5e5e5). Marketing tiles and bands: 1px `--border-oat` (#e4e4e4).
7. **Oat is the stage.** `--bg-oat` (#f5f3f1) sits behind heroes, diagrams, interactives, quotes and bands; heroes, slides, covers and social cards add the isometric line lattice (30°/150° lines, strongest at the bottom) via `var(--lattice-hero|field|print)`.
8. **Colour means something.** Blue = selection, focus, links, course actions. Green = correct, success, sign-up. Pear (#d8e82e) = XP, streaks, rewards and the key-term marker band. Yellow = retry. Red only marks a wrong choice; the incorrect feedback sheet is **grey**. Course hues (blue, green, purple, orange, teal, pink, papaya, pear, mint) colour nodes, kickers, charts.
9. **Feedback glows from the bottom.** Correct = green-200 radial glow + "Correct!" + green 3D Continue + white "Why?". Incorrect = grey glow + "Not quite" + a hint, never the answer. Wrong choices shake (`shakeX`).
10. **One idea per screen.** Lessons reveal content in beats; each step has one question; Check stays disabled until there's an answer; slides have one headline that states the finding.
11. **Springy, short motion.** Presses 100ms ease-out; things that appear use `--ease-spring-smooth` (cubic-bezier(.2,1.1,.36,1)) over 300–830ms; content rises 8–12px as it fades in. Honour `prefers-reduced-motion`.
12. **Respect the brand line.** This is Brilliant's *design language*, not its brand. Never use the Brilliant name, wordmark, Koji or other mascots, their illustrations or animations, or their licensed fonts without a licence, and never make a page that could pass for brilliant.org. Use the user's own product name (templates use the placeholder "Lumen").
13. **Lessons are 3D plates on a path, not flat circles.** Each lesson is an isometric plate: a base ellipse, a lighter top plate, and a split progress ring (two arcs with gaps at top and bottom) — grey when locked, the course hue when current (gently floating, with a Start bubble), filled when done; reviews are an 8-point star plate. Rows sit 30px apart in a 392px column and step centre → start → centre → end. Always use `.lesson-node` (rendered by `js/brilliant.js`); never draw a node with CSS circles or an emoji. Spec: `references/02-components.md` → Lesson node.

## Quick reference

```html
<!-- 3D button (product CTA) -->
<button class="btn3d"><span class="btn3d__face">Continue</span></button>
<button class="btn3d btn3d--blue btn3d--block"><span class="btn3d__face">Start</span></button>
<button class="btn3d btn3d--white"><span class="btn3d__face">Why?</span></button>
<!-- flat pills -->
<a class="btn btn--outline">Sign in</a> <a class="btn btn--success">Sign up</a>
<!-- badge / chip / segmented -->
<span class="badge badge--solid badge--purple">Save 33%</span>
<button class="chip" aria-pressed="true">Math</button>
<div class="segmented" role="tablist"><span class="segmented__thumb"></span><button aria-selected="true">Math</button><button aria-selected="false">Coding</button></div>
<!-- answer tiles + feedback -->
<div class="choices" role="radiogroup"><button class="choice" role="radio" aria-checked="false">Bo</button>…</div>
<div class="feedback feedback--correct"><div class="feedback__inner">…</div></div>
<!-- lesson path: nodes render from data attributes; rows get the rhythm automatically -->
<div class="path">
  <div class="path__row"><button class="path__item"><span class="lesson-node" data-state="done" data-hue="blue"></span><span class="path__label"><span>Order logic</span></span></button></div>
  <div class="path__row"><button class="path__item"><span class="start-bubble">Start</span><span class="lesson-node" data-state="current" data-hue="blue" data-progress="1"></span><span class="path__label"><span>Heights</span></span></button></div>
  <div class="path__row"><button class="path__item"><span class="lesson-node" data-state="locked" data-shape="review"></span><span class="path__label"><span>Level review</span></span></button></div>
</div>
<!-- standalone mark (SVG string): B.node({shape:'lesson', segments:2, progress:2, beam:120}) -->
<!-- campaign headline -->
<h1 class="ts-display-6xl">Your personal tutor for <em>maths</em> and <em>code</em></h1>
<!-- type -->
<h1 class="ts-display-6xl">Your personal tutor</h1> <h2 class="ts-heading-lg">Logic</h2> <p class="ts-body-lg c-secondary">…</p>
```

Themes: `<html data-theme="light|dark">` (dark follows the OS when unset). Higher-contrast text for small coloured copy: `data-contrast="more"`.

## Before you hand it over

- Light **and** dark screenshots look right; nothing invisible (check `--text-tertiary` text, pear/yellow text, white-on-green).
- At 320px: no sideways scroll, controls ≥ 44px tall, 16–20px gutters.
- One primary 3D button per view; disabled until it can act.
- Only roles in components; ramps only in charts/illustrations.
- Serif only at ≥ 24px, weight 500; sans headings 700; UI labels 500; key words of a campaign headline in the serif italic.
- Lesson paths use `.lesson-node` plates with split rings and the centre/start/centre/end rhythm.
- Every pressable thing has the lip, a 100ms press and a visible focus ring (`0 0 0 3px var(--border-select)`).
- Copy follows `07-voice-and-content.md`: buttons are verbs, titles state the finding, no exclamation marks except "Correct!".
- No Brilliant name, logo, mascot or illustration anywhere.
