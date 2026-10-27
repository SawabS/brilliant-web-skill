# Components

All classes live in `css/brilliant.css`. "Measured" values come from brilliant.org markup; see `09-source-notes.md`.

## Buttons

### 3D button `.btn3d` (the product CTA) — measured

```html
<button class="btn3d"><span class="btn3d__face">Continue</span></button>
```

| Part | Value |
|---|---|
| Wrapper | radius 56px, no padding, hover opacity .85, focus = elevation outline, `margin-top: 4px` reserves the lift |
| Face | radius 60px, padding 14px 24px, min-height 48px, `ui.actions.base` (16/500), `transform: translateY(-4px)`, `box-shadow: 0 4px 0 0 <lip>` |
| Press | `:active` → `transform: none; box-shadow: none` in 100ms ease-out |
| Disabled | face `--bg-disabled`, text `--text-disabled`, no lip, no lift |
| Coloured faces | text-shadow `0 0 3px rgba(0,0,0,.25)` |

Variants (face / lip):

| Class | Face | Lip | Use |
|---|---|---|---|
| *(default)* | `--bg-inverse-secondary` #383838 | black | Continue, Check, Finish — the lesson CTA. Dark theme: gray-200 face, gray-400 lip, dark text. |
| `--blue` | blue-500 | blue-600 | Course actions: Start, Resume. |
| `--green` | green-500 | green-600 | Continue after a correct answer. |
| `--white` | white + 2px `--border-primary` | black 10% | Secondary: Why?, Skip, Reset. Hover border/lip 30%. |
| `--fill` | gray-200 | black 20% | Tertiary filled. |
| `--oat` | oat | #dcdad8 (hover #acaaa9) | On oat surfaces. |
| `--premium` | iridescent gradient, purple-950 text | 4px bottom border blue-900 @ 30% | Subscribe, upgrade. |
| `--purple --orange --teal --pink --papaya --red` | hue-500 | hue-600 | Course-coloured actions. |
| `--yellow --pear --mint` | hue-500 | yellow-700 / pear-600 / mint-700 | Black text. |

Sizes: default (48px), `--sm` (40px, 3px lip), `--lg` (56px, `ui.actions.lg`). Layout: `--block` (100%), `--wide` (100% up to 480px — the onboarding/lesson bottom CTA), `--icon` (48×48). Add `--shimmer` for a periodic light sweep on promotional CTAs.

### Flat pill `.btn` — measured

Radius 54px, 2px transparent border, `ui.actions.base`, height 48px, padding 0 20px (`--sm` 40px / 14px). Variants: `--outline` (Sign in), `--success` (Sign up, green), `--inverse` (black), `--ghost`, `--danger`. Marketing: `--cta` (h60, `ui.actions.lg`, radius full, `0 4px 7px rgba(0,0,0,.05)`), with `aria-pressed="false"` rendering the soft white unselected state used in the "I'm a learner / I'm a parent" toggle; `--hero` (white, h68, black text, `0 4px 14px rgba(0,0,0,.05)`) on dark bands.

### Icon button `.icon-btn`, step arrows `.step-arrow`

40px round, icon 24px in `--icon-tertiary`, hover `--bg-alpha`. Step arrows: 36px circles, 2px `--border-solid`, 2px lip.

## Badges, chips, toggles

- **Badge** `.badge` (measured recipe): `ui.actions.sm` (12/700, uppercase, +.48px), padding 4px 8px, radius 12px. Variants `--solid` (palette-500 + white), `--subtle` (100 + 700; dark: 950 + 400), `--outline` (1px 500, pill, 700 text), `--minimal` (700 text). Palettes: blue, green, purple, orange, teal, pink, red, yellow, pear, mint, papaya, cyan, plus `--primary` (black) and `--premium` (pink-300→yellow-400 gradient).
- **XP chip** `.xp`: pear-500 pill, black `ui.actions.sm` text, `xpCounterPulse` on change.
- **Chip** `.chip` (measured): h44, padding 0 16px, pill, `ui.actions.base`, white with 40% text; `aria-pressed="true"` = black fill, white text. Topic filters on marketing.
- **Segmented** `.segmented` (measured): `--bg-secondary` track, pill, 6px inset, h56 (68 at ≥769), black thumb sliding with the spring ease; selected label white, others `--text-tertiary`. Set `--n` (options) and `--i` (selected index), or let `brilliant.js` do it.
- **Tabs** `.tabs .tab` (measured on pricing): h48, 1px baseline in `--border-primary`, selected 2px underline (`--border-active`, or purple with `.tabs--purple`).
- **Switch** `.switch` (green when on) and **check** `.check` (24px, radius 6, blue when checked).

## Surfaces

| Class | Spec |
|---|---|
| `.card` | `--bg-primary`, 2px `--border-primary`, radius 20, padding 24 → 32 |
| `.card--lip` | 2px `--border-solid` + 4px lip; hover border/lip `--border-hover`; press sinks |
| `.card--oat` | oat fill, 1px `--border-oat`, radius 16 |
| `.card--elevated` | no border, `--shadow-elevation-base` |
| `.stat-tile` | marketing proof point: 1px oat border, radius 44, value `headline.xl`, label `body.sm` tertiary, centred |
| `.kpi` | product KPI card: 2px border, label `heading.xs` secondary, value `heading.2xl` |
| `.media-panel` + `.tint-papaya/-sage/-oat/-sky/-lilac` | radius 20, aspect 460/321, pastel behind a product shot or diagram |
| `.feature-card` | 1px oat border, radius 20, media on top, body padding 20/24 |
| `.quote-card` | oat, radius 17, padding 24/40/36, quote in `display.lg` |
| `.band` | the big oat section: 1px oat border, radius 44 at ≥992, padding 48/56 → 70 |
| `.hue-card--<hue>` | course gradient card |
| `.iridescent-frame` / `.plan-option` | 4px gradient frame around an elevated card (premium plans) |
| `.popover-card` | radius 40, 2px `--border-solid`, padding 24/16/16, gap 16 — the lesson popover with a blue Start |
| `.modal` | radius 32, padding 32, `--shadow-elevation-lg`, over `--special-overlay-default` (black 50%) |
| `.sheet` | bottom sheet, radius 32 top corners |
| `.toast` | black pill, white `ui.actions.base`, slides up |
| `.tooltip` | `--bg-inverse-secondary`, radius 8, `body.sm` |

## Navigation

- **App bar** `.app-bar` (measured): sticky, h64, `--bg-elevated`, 1px bottom `--border-primary`, `elevation.subtle` → `elevation.base` at ≥769. Inner max 1216, gap 32. Nav links `ui.nav.default` secondary; current = `ui.nav.selected` primary + 2px black underline. Right: Sign in (outline) + Sign up (green) pills, or XP/streak chips + avatar.
- **Floating pill nav** `.float-nav` (marketing, measured): fixed 16/24px from top, white pill with 1px oat border, padding 6 6 6 20 (8 8 8 28 at ≥992). Add `.float-nav__spacer` at the top of the page.
- **Footer** `.site-footer`: 1px top border, `body.sm` secondary.

## Course map

- **Course card** `.course-card` (measured): sticky at `top: 41px` on ≥992, 2px border, radius 20, padding 32, gap 16, max-width 487; 100px art, title `heading.lg`, description `body.base` secondary, meta row `body.sm` with 16px icons, then progress.
- **Level header** `.level-header` (measured): a button h64, radius 18, on an underlay that adds a 2px ring and a 4px lip in the level colour (current = blue-400 with a blue-700 "LEVEL 1" kicker; others gray-200 with a tertiary kicker; done = green-400). Pressing moves it down 4px.
- **Path** `.path` (measured): 392px column, 30px gap, rows alternate centre → left → centre → right. Labels 138px wide, `body.base`, tertiary when locked, primary when current, clamp 3 lines.
- **Node** `.node` (reconstructed geometry, measured greys): an isometric coin, face over a darker edge with a light inner rim. Locked = gray-200/gray-400; `--current` = hue-500/700 with `floatyNudge`; `--done` = hue-400/600 with a `.node__tick`; `--review` = scalloped badge for level reviews. Hue via `.hue-<name>`. Hover dims (`brightness(.95)`, Brilliant uses .9). A `.start-bubble` floats above the current node.

## Lesson player

- **Shell** `.lesson`: sticky `.lesson__bar` (max 800, close · title · ‹ steps › · XP), `.lesson__body` (max 640, gap 24), sticky `.lesson__footer` holding one `.btn3d` (Continue → Check → Finish) and an optional `.kbd-hint`.
- **Steps** `.steps .steps__seg`: 8px pills, `--f` (0–1) fills a segment as beats are revealed; `--current` gets a soft green ring; `--correct` green; `--incorrect` gray-700.
- **Lesson content** `.lesson-content` (measured recipe): 16/1.6rem, paragraphs 1.4rem apart, h1 2em, h2 1.6em, h3 1.3em, 4px gray-200 blockquote rule, inline code on `--bg-secondary` at 15/500, links underlined with .5 opacity hover. `--lg` for 20px lesson text.
- **Beat** `.beat[hidden]`: reveal one at a time with `B.reveal(container)`; each rises 12px.
- **Key term** `.term`: bold + pear marker band under the one idea that matters.
- **Need card** `.need-card`: lip card with a green "THE NEED" kicker, a `heading.md` question, and the concepts the lesson adds as badges.
- **Widget** `.widget`: 2px bordered card with an "INTERACTIVE" eyebrow, hint, the `.stage` (oat, radius 20) and a `.widget__prompt`.
- **Choice** `.choice` (lip tile): 2px `--border-solid`, radius 16, min-height 56, `ui.actions.base`, 4px lip. States: hover (border-hover), `aria-checked/pressed="true"` (blue-500 border + lip, blue-100 fill, blue-700 text), `data-state="correct"` (green-600 border, green-200 fill), `data-state="incorrect"` (red-500 border, red-100 fill, `shakeX`). `.choice--keyed` adds a lettered `.choice__key`. Grid via `.choices` / `.choices--2`.
- **Answer input** `.input--answer`: 56px, centred, semi-mono 20px, lip.
- **Feedback sheet** `.feedback` (measured colours): fixed bottom, `radial-gradient(ellipse 130% 100% at center bottom, <feedback> 30%, transparent)`, slides up with the spring. Title `heading.lg` ("Correct!" with a check, green-700; "Not quite" in ink), a one-line reason, and actions: white "Why?" + green "Continue" (correct) or dark "Try again" (incorrect). `--retryable` uses yellow-300.
- **Feedback bar** `.feedback-bar`: flat alternative (green-200 / gray-200 fill bar with a round icon).
- **Go deeper** `details.deeper`: lip drawer with a purple icon tile, title + semi-mono subtitle, rotating chevron; body holds maths, code, sources.
- **End state**: 112px pear coin with a 6px pear-600 lip and a star, `display.3xl` "Lesson complete", XP chip pulse, streak row.

## Inputs and readouts

- `.input`: h48, radius 12, 2px `--border-primary`, focus border blue-500, invalid red-500, placeholder `--text-placeholder` (#999).
- `.field__label` `heading.xs`; `.field__hint` `body.sm` secondary; `.field__error` red-700.
- `.slider`: 8px track (`--bg-tertiary`) filled to `--value` with `--slider-fill` (default blue-500), 28px white thumb with 2px border and 3px lip.
- `.readout`: semi-mono 16 (20 with `--lg`), tabular.
- `.progress`: track `--bg-tertiary`, pill, 4 / 8 / 12px; fill green (or `--progress`), width `--value`, spring transition.

## Content blocks

- **Code** `.code` (measured "probe" theme): black ground, white 90% text, comments white 50%, control flow pink-400 (`.k`), calls teal-400 (`.f`), definitions green-400 (`.d`), numbers purple-400 (`.n`), strings pear-400 (`.s`); Source Code Pro 15/24; radius 16.
- **Callout** `.callout--<hue>`: `-tertiary` fill, `heading.sm` title in `-primary` ink with an 18px icon, black body. Blue = note, green = done, yellow = caveat, purple = maths/definition, red = failure, oat = aside.
- **Table** `.table-wrap .table` (measured): **black header row** (`--bg-table-header`) with white `heading.xs`; cells `body.sm`, 10px 14px, 1px `--border-secondary` row rules; `td.num` right-aligned tabular; selected row blue-100. `.table--plain` for a quiet grey header.
- **Kicker** `.kicker` (`ui.actions.sm`, tertiary or a hue) and **eyebrow** `.eyebrow` (semi-mono 14, uppercase, tertiary).
- **Streak** `.streak__day`: 36px circles, 2px border; done = pear fill; today = pear outline ring.
- **Skeleton** `.skeleton`: gray-100, radius 20, opacity .7, `skeletonPulse .8s alternate`.
- **Icon tile** `.icon-tile`: 44px, radius 12, hue-tertiary fill, hue icon.
