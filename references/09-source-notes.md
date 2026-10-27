# Source notes: what was measured, what was reconstructed

## How the data was captured (27 October 2026)

1. Public pages were fetched with a rendering scraper (JavaScript executed, 5–6s wait): `/` (logged-out home), `/courses/`, `/courses/logic-deduction/` (course map), `/subscribe/` (pricing) and `/welcome/` (onboarding).
2. Their stylesheets (`/_next/static/chunks/*.css`, Panda CSS, ~1.1MB) were downloaded.
3. `tools/capture/extract_tokens.py` parsed the Panda token blocks: `:where(:root,:host)` (light + all scales) and `[data-theme=dark]` (dark overrides), every `.panda-textStyle_*` class, the `badge` / `progress` / `lessonContent` recipes and all 50 `@keyframes`. Output: `source/brilliant-tokens.json` (values only, no Brilliant code).
4. The captured HTML was rendered locally with Playwright (scripts stripped, CSS inlined, fonts substituted) to read computed styles of buttons, headings, cards and layouts, and to screenshot the course map, pricing and onboarding pages.
5. `tools/build_tokens.py` generated `tokens/*`; `tools/build_token_docs.py` generated `references/10-token-tables.md`.

Re-run: capture the CSS again, then `python3 tools/capture/extract_tokens.py main.css source/brilliant-tokens.json && python3 tools/build_tokens.py && python3 tools/build_token_docs.py`.

## Measured (exact)

- All colour primitives and semantic roles, light and dark (`colors.*`), including lesson-feedback, streak, probe-code and overlay roles.
- All 34 text styles, the font stacks, letter-spacing scale.
- Spacing, sizes, containers (1216 / 432 / 64 app bar / 44 NUX header), radii, shadows, breakpoints, z-indices, gradients.
- 3D button mechanics: face radius 60 / wrapper 56, `translateY(-4px)`, `0 4px 0 0` lip, 100ms ease-out, padding 14×24, hover opacity .85, text-shadow on colour, every lip colour used in production, premium variant.
- Flat buttons (54px radius, 2px border, h48 / h40), marketing CTA (h60, shadow), hero button (h68).
- Badge recipe (all palettes and variants), progress heights, lesson-content typography recipe.
- App bar, floating marketing nav, hero (oat + lattice pattern geometry), stat tiles (radius 44), media panel hexes (#ffede0, #e7eee2, #f5f3f1), feature cards, oat band (radius 44), testimonial cards (radius 17), segmented switch, chips, pricing tabs and plan frames.
- Course page: course card, level header (h64, radius 18, 2px ring + lip underlay in blue-400 / gray-200), path column (392px, 30px gap, zig-zag), node box (128×134), label (138px, 3-line clamp), lesson popover (radius 40, 2px gray-200), blue Start 3D button.
- Onboarding: 480px × 48px dark 3D Continue, `ui.actions.xl` prompt, 390px column.
- Keyframes (fadeIn, slideUp, slideFromBottom, scaleIn, shakeX, floatyNudge, xpCounterPulse, fillProgress, skeletonPulse, borderGlow, shimmer, streak end-state family, …) and easing (`spring-smooth` cubic-bezier(.2,1.1,.36,1) 833ms).
- Wiki/MCQ states: correct = green-600 border + green-200 fill; incorrect = red-500 border + red-200 fill.

## Reconstructed (from the measured tokens, the visible product and the author's Blueprint course)

- The logged-in lesson player layout: top bar arrangement, step segments with partial fill, beats, need card, widget card, "Go deeper" drawer, choice tile geometry (radius 16, min-height 56), feedback sheet layout and copy, end state. The colours and motion are measured; the arrangement is reconstructed.
- The lesson node artwork: Brilliant draws nodes as detailed SVG/Rive coins; this system draws an original CSS coin in the same proportions and greys.
- Dashboard / KPI components (Brilliant's dashboards are behind login).
- Print, deck and email adaptations (Brilliant has no print system).
- Sound set (adapted from the author's own AI Engineering Blueprint `src/sound.js`).
- Fonts: CoFo Brilliant, CoFo Robert and CoFo Semi Mono are commercial (Contrast Foundry) and are not included. Substitutes: Inter, Source Serif 4, DM Mono. Source Code Pro and KaTeX are exact.

## What is deliberately not included

The Brilliant name and wordmark, Koji and other characters, illustrations, product photos, Rive animations, and the CoFo font files. The system reproduces the visual language (tokens, proportions, behaviour), which is what a design skill needs; brand assets stay with their owner. Do not use this system to make anything that could be mistaken for brilliant.org.
