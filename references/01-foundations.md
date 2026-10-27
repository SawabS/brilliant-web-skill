# Foundations

Exact values live in `tokens/tokens.css` and, as tables, in `10-token-tables.md`. This file explains how to use them.

## Colour

### Neutrals and surfaces

| Role | Light | Dark | Use |
|---|---|---|---|
| `--bg-primary` | #ffffff | #141414 | The canvas. Most of every screen. |
| `--bg-secondary` | #f8f8f8 | #1e1e1e | Quiet fills: segmented track, inline code, table header (plain). |
| `--bg-elevated` | #ffffff | #1e1e1e | App bar, popovers, modals, sheets. |
| `--bg-oat` | #f5f3f1 | #383838 | The warm stage: hero, diagrams, interactives, quotes, bands. |
| `--bg-alpha` / `--bg-hover` / `--bg-active` | black 5 / 10 / 20% | white 10 / 10 / 20% | Hover and press washes on neutral things. |
| `--bg-tertiary` | black 10% | white 20% | Progress tracks, slider tracks. |
| `--bg-inverse-primary` | #000000 | #f2f2f2 | Selected chip, segmented thumb, toast, table header. |
| `--bg-inverse-secondary` | #383838 | #e5e5e5 | **The primary 3D button face**, tooltips. |

### Text and icons

| Role | Light | Use |
|---|---|---|
| `--text-primary` | #000000 | Headings, labels, anything that must be read. |
| `--text-secondary` | black 60% | Body copy under headings, descriptions. 5.7:1 on white. |
| `--text-tertiary` | black 40% | Captions, inactive nav, path labels of locked lessons, axis ticks. 2.9:1 — never for essential text. |
| `--text-disabled` | black 20% | Disabled labels only. |
| `--text-link` | blue-500 | Links. 4.3:1 — fine at 16px+ medium, or underline it. |
| `--text-<hue>-primary` | hue-700 | Coloured text: kickers, chart labels, badge text. Green/orange/yellow/pear/mint 700 are below 4.5:1; use them at ≥ 18.66px bold or switch on `data-contrast="more"`. |
| `--icon-primary/secondary/tertiary` | black / 60% / 30% | Icons follow the same ladder. |

### Borders

| Role | Light | Use |
|---|---|---|
| `--border-primary` | black 10% | Product cards (2px), outline buttons, inputs, table frames. |
| `--border-secondary` | black 5% | Hairlines inside tables and lists. |
| `--border-solid` | #e5e5e5 | Opaque border + lip for choices, lip cards, popovers, level headers. |
| `--border-hover` | black 30% | Hover state of outlined things. |
| `--border-active` | #000000 | Selected nav underline. |
| `--border-select` | blue-500 | Focus ring, selected choice. |
| `--border-oat` | #e4e4e4 | 1px marketing hairline (stat tiles, feature cards, bands, floating nav). |

### Status and lesson feedback

| Role | Light | Dark |
|---|---|---|
| `--bg-success-primary` | green-500 #29cc57 | green-400 |
| `--special-lesson-feedback-correct` | green-200 #d4f5dd | #00370f |
| `--special-lesson-feedback-incorrect` | gray-200 #e5e5e5 | gray-900 |
| `--special-lesson-feedback-retryable` | yellow-300 #fce49d | #403000 |
| `--special-lesson-progress-active` | black 20% | white 20% |
| `--special-lesson-progress-incorrect` | gray-700 | white 70% |
| `--special-endstate-streak-counter` | pear-500 #d8e82e | pear-500 |
| `--status-error / promo / success / warning` | #ff5d5d / #456dff / #29cc57 / #f7c325 | same |

### Hues

Fourteen ramps, 50→950: gray, blue, green, yellow, orange, red, pink, purple, teal, mint, cyan, pear, papaya, plus oat-50/200. Every hue has semantic roles in four strengths: `--bg-<hue>-primary` (500, the fill), `-secondary` (200), `-tertiary` (100, the tint), `--text-<hue>-primary` (700), `--border-<hue>-primary` (400) and `-bold` (600), `--icon-<hue>-primary` (700).

- The signature blue is **#456dff** (blue-500), not a navy. Focus, selection and course actions.
- The signature green is **#29cc57** (green-500). Sign-up, correct, progress fill.
- **Pear #d8e82e** is the reward colour: XP chip, streak days, key-term marker band. Text on pear is black.
- Oat #f5f3f1 is the only warm neutral.
- Marketing pastels behind product shots (measured): papaya tint **#ffede0**, sage **#e7eee2**, oat **#f5f3f1**.

### Proportions

On any screen: ~85% white/oat, ~10% black type, one primary button, at most two hues, pear at most once. A course page adds exactly one course hue.

### Gradients (use sparingly)

- `--gradient-iridescent-frame` (blue-400 → pink-400 → yellow-500, 86°): premium plan frame, premium CTA, the one iridescent moment on a page.
- `--gradient-iridescent-premium-copy`: gradient text for the word "Premium".
- `--gradient-hue-shift-color-<hue>-primary`: soft course-colour cards (the gradient is mostly grey-white with a hue wash).
- No other gradients. No glassmorphism, no neon, no glows except `borderGlow` on a success moment.

## Typography

Brilliant ships three licensed Contrast Foundry faces. Open substitutes are bundled in `tokens/fonts/` (WOFF, SIL OFL) with a Google Fonts fallback; font stacks put the real faces first.

| Token | Brilliant | Substitute | Role |
|---|---|---|---|
| `--font-sans` | CoFo Brilliant 400/500/700 | Inter | All UI, headings, body. |
| `--font-display` | CoFo Robert 500 + italic — a sharp contemporary Clarendon | **Besley** instanced at wght 600, registered as "Besley Display" 500 (Besley revives Robert Besley's original Clarendon; 600 matches CoFo Robert Medium's colour) | Display headlines only; key words in italic (`<em>`). |
| `--font-semi-mono` | CoFo Semi Mono | DM Mono | Interactive readouts, eyebrows. |
| `--font-code` | Source Code Pro | Source Code Pro (exact) | Code. |
| `--font-math` | KaTeX_Main | KaTeX (exact) | Maths. |

**Display italic for emphasis.** Brilliant's campaign art sets the key words of a headline in the display italic: "Your personal tutor for *math* and *coding*". Inside any `.ts-display-*` / `.display-*` element, `<em>` switches to the italic automatically. Use it for one or two words, never a whole line.

### The scale (exact, from production)

| Family | Styles |
|---|---|
| **display** (serif 500) | lg 24/1.1 · xl 30/1.1 · 2xl 36/1.1 −.36px · 3xl 40/1.1 −.4px · 4xl 50/1.1 −.5px · 5xl 60/1.1 −1.2px · 6xl 76/1.05 −1.4px |
| **headline** (sans 400) | xl 30/1.25 −.3px — big numbers and soft titles (marketing stat tiles). Feature-row titles use 36/1.2 −.36px (`.ts-headline-2xl`). |
| **heading** (sans 700) | xs 14/1.4 · sm 16/1.4 · md 20/1.25 · lg 24/1.25 · xl 30/1.25 · 2xl 36/1.25 · 3xl 48/1.25 · 4xl 60/1.25 |
| **body** (sans 400, 1.5) | xs 12 · sm 14 · base 16 · lg 20 |
| **ui.actions** (sans 500, 1.25) | sm 12/1.1 **700 uppercase +.48px** (badges, kickers) · base 16 · lg 20 · xl 24 |
| **ui.nav** (sans 16/1.5) | default 400 · selected 500 |
| **interactives** | code 15/24 and 19/30 · math 19/24 and 23/30 · semiMono 14/16/20 ·1.5 · data.axis 10/1.5 |

Rules:
- Display is responsive on marketing: hero climbs xl → 2xl → 3xl → 5xl → 6xl across breakpoints (`.display-hero`); section titles 2xl → 4xl → 5xl (`.display-section`).
- Product screens are sans-only except the lesson-complete title and onboarding.
- Sentence case everywhere. Uppercase only through `ui.actions.sm` (badges, kickers, level labels).
- Lesson body text is 16/1.6rem (`.lesson-content`) or 20px (`--lg`); paragraphs space 1.4rem.
- Numbers: tabular figures (`.tabular`, `font-variant-numeric: tabular-nums`) in tables, KPIs, readouts.

## Space, size, layout

- 4px base (`--space-1` = .25rem … `--space-96` = 24rem), identical to Tailwind's scale.
- Containers: content `1216px` (`--size-container-lg`), narrow `432px`, prose `60ch`, app bar `64px`, onboarding header `44px`.
- Gutters: 24px phone, 32px ≥ 481px. Marketing outer padding `clamp(32px, 10vw − 72px, 72px)` at ≥ 992px; page max 1440.
- Breakpoints (min-width): xs 320 · sm 360 · md 481 · lg 769 · xl 992 · 2xl 1280.

## Radius

`--radius-sm` 2 · `base` 4 · `xs` 6 · `md` 8 · `lg` 12 · `xl` 16 · `2xl` 20 · `3xl` 32 · `full`. Plus measured specials: buttons 54px (flat) / 56–60px (3D), level header 18px, lesson popover 40px, testimonial card 17px, oat band & stat tile 44px, hero media 32px.

## Elevation

- **Lip** (pressable): `box-shadow: 0 4px 0 0 <lip>`; pressed = `translateY(4px)` + no shadow. 3D buttons: face `translateY(-4px)` + `0 4px 0 0 lip`.
- **Float** (overlaying): `--shadow-elevation-base` 0 0 15px black 10% · `-md` 0 0 25px black 20% · `-lg` 0 0 40px black 20% · `-subtle` 0 1px 3px 4%.
- **Focus**: `--shadow-elevation-outline` 0 0 0 3px blue-500, or `0 0 0 1px bg, 0 0 0 3px blue-500` on links.
- Plan cards: `inset 0 -6px rgba(0,0,0,.15)` — a lip drawn inside.

## Motion

| Token | Value | Use |
|---|---|---|
| `--dur-press` | 100ms ease-out | 3D press, lip press |
| `--ease-standard` / `--dur-fast` | cubic-bezier(.4,0,.2,1) / 150ms | colour/border transitions |
| `--ease-spring-smooth` / `--dur-spring-smooth` | cubic-bezier(.2,1.1,.36,1) / 833ms | sheets, popovers, thumbs, progress |
| `--ease-xp-pulse` | cubic-bezier(.25,.75,.18,1.09) | XP counter pulse |

Keyframes from production: `fadeIn`, `slideUp` (8px), `slideFromBottom`, `scaleIn`, `shakeX` (wrong answer), `floatyNudge` (5px bob on the current node), `xpCounterPulse` (1.2×), `fillProgress`, `skeletonPulse` (.8s alternate), `borderGlow`, `shimmer`, `typingDotWave`, `spin`, plus the streak end-state family. Respect `prefers-reduced-motion` and `data-reduced-motion="true"`.

## z-index

base 0 · docked 10 · app-bar 999 · dropdown 1000 · sticky 1100 · banner 1200 · overlay 1300 · modal 1400 · popover 1500 · skip-nav 1600 · toast 1700 · tooltip 1800.

## Iconography

Brilliant's icons are custom: 16px in meta rows, 24px in navigation, single colour (`currentColor`), rounded joins, mostly filled shapes for objects (star, bolt, flame, play) and 2px strokes for UI glyphs (x, arrows, check). Use `assets/icons.svg` (original, same grammar) or Lucide/Phosphor Bold at stroke 2. Put icons that introduce a card in a 44px rounded-12 tile with a `-tertiary` fill (`.icon-tile`). No emoji in UI.

## Illustration

Brilliant illustrates with clean, flat-shaded 3D objects: isometric tiles, coins and blocks in course hues with a lighter top face and two darker sides (400 / 600 / 700 of one hue), on white or pastel panels, no outlines, no gradients, no characters. The templates draw these in SVG; reuse that grammar for your own art. Do not copy Brilliant's illustrations, Koji or other characters.
