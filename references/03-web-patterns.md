# Web patterns

Page-level recipes. Each one has a working template in `templates/`.

## Marketing / landing page — `templates/landing.html`

Measured from brilliant.org's logged-out homepage, top to bottom:

1. **Floating pill nav** (`.float-nav`): wordmark left, a single outline "Sign in" pill right. No menu on desktop.
2. **Hero** (`.hero`, oat): two-column grid at ≥1280 (`590px | 1fr`), centred single column below.
   - Headline: serif `.display-hero` (30 → 76px), black, 2–3 short lines. States the promise, not the product name ("Your personal tutor for math and coding").
   - Sub: `body.lg`, `--text-secondary`, ≤ 2 lines.
   - CTA row: green pill (`.btn--cta.btn--success`) + soft white pill — often an audience switch ("I'm a learner / I'm a parent or teacher").
   - Social proof: award laurels, tiny.
   - Media: a white card, radius 32, with a product shot or illustration, `drop-shadow(0 0 110px rgba(0,0,0,.05))`.
   - The isometric lattice (`.hero__pattern`) rises from the bottom half and fades upward.
3. **Proof row**: three `.stat-tile`s (icon, `headline.xl` value, tertiary label).
4. **"Meet …" section**: centred serif section title + a `.segmented` switch (Math | Coding) that swaps the feature rows below.
5. **Feature rows** (`.feature-row`, alternating): copy (sans 36/400 title, 2–3 short `body.base` secondary paragraphs, max 440px) beside a pastel `.media-panel` (papaya #ffede0, sage #e7eee2, oat). ~96px between rows.
6. **"Effective and trusted"**: serif title + three `.feature-card`s (pastel media top, 16/500 title, `body.sm` secondary copy).
7. **Oat band** (`.band`, radius 44): serif title, topic `.chip`s, a white card listing covered topics with green checks, and a diagram panel.
8. **Testimonials**: serif title, horizontally scrolling `.quote-card`s (oat, quote in `display.lg`).
9. **Pricing**: serif title, purple `.tabs` (Monthly | Annual + "SAVE 33%" badge), two `.plan-option`s (selected one wrapped in the iridescent frame), the premium 3D button (max 438–480px), fine print in `body.xs` tertiary.
10. **Final CTA band**: near-black (`gray-950`), white serif headline, white `.btn--hero`, a faint iridescent bloom.
11. **Footer**: hairline, `body.sm` links.

Spacing: sections 80–112px apart; content max 1216px; hero top pad accounts for the floating nav (`.float-nav__spacer`).

## Product shell — `templates/app-course.html`, `dashboard.html`

- `.app-bar` (64px, sticky, subtle shadow), wordmark, 2–4 nav links with icons (16px), right side: streak/XP chip, theme toggle, avatar or Sign in/Sign up pills.
- Body on white. Cards with 2px borders, radius 20. One `.btn3d` or `.btn--inverse` per view.
- Page heading: kicker + `heading.2xl` that states the finding ("Algebra is clicking; fractions need a revisit").

### Course page (measured layout)

- ≥992px: three columns centred: sticky `.course-card` (350–487px) · path column (364–488px) · optional side rail (streak card, "Up next" callout). Below 992: single column, course card un-bordered and centred above the path.
- Levels: sticky `.level-header` at the top of the column with a white→transparent fade under it, then a `.path` of nodes zig-zagging (centre, left, centre, right), ending each level in a scalloped **Level review** node.
- The current node shows a `START` bubble and, when tapped, a `.popover-card` (radius 40) with the lesson title, meta and a full-width blue 3D **Start**.
- Locked lessons are grey coins with tertiary labels; done lessons are coloured coins with a green tick.

### Dashboard

KPI row (`.kpi`, auto-fit min 220px), a 2:1 chart grid (cards with `heading.md` titles and the legend on the right), and a table card whose header row is black. Filters as a `.segmented` (Week | Term | Year). Charts follow `06-interactive-visuals.md`.

## Lesson player — `templates/app-lesson.html`

Full-screen, no app bar.

```
[×] 3. Heights   ‹ [■■■■][■■□□][□□□□][□□□□] ›   ⚡ 20   ◐
                 ┌──────────── 640px ────────────┐
                 │ STEP 2 OF 4  (eyebrow)          │
                 │ [Need card, first step only]    │
                 │ Prompt (20px) with one .term    │
                 │ [Widget: oat stage + controls]  │
                 │ [Choices: lip tiles, 1 or 2 col]│
                 │ [Go deeper drawer]              │
                 └─────────────────────────────────┘
 Enter to read on · ← → steps                [ Continue ]
```

Flow:
1. A step's content arrives in **beats**: Continue reveals the next `.beat` (with the "reveal" sound) until the step is complete, then advances. The step segment fills as beats appear (`--f`).
2. Question steps: the button reads **Check** and stays disabled until an answer exists (the "unlock" note plays when it enables).
3. Check → **feedback sheet** glows up from the bottom. Correct: "Correct!" + reason + white **Why?** + green **Continue**, correct-chime, +XP pulse, the choice turns green. Incorrect: grey sheet, "Not quite" + a hint that points at what to look at, dark **Try again**, low knock, the choice turns red and shakes.
4. Keyboard: Enter = primary action, ← → = previous/next seen step. Close (×) returns to the course.
5. End state: pear coin with a star, `display.3xl` "Lesson complete", XP, streak days, **Finish**.

## Onboarding / NUX (measured on /welcome)

A single centred column (max 390px text), a large illustration or animation (150px), one sentence in `ui.actions.xl` (24/500, centred, balanced), and a full-width (max 480px, h48) dark 3D **Continue** pinned to the bottom with safe-area padding. Header 44px with only a back button and a thin progress bar. One question per screen; options as lip tiles.

## Pricing / paywall (measured on /subscribe)

Centred: a premium illustration, serif `display` title ("Unlock …"), one-line sub, purple tabs, plan cards (selected = iridescent frame, others grey frame), premium 3D CTA, fine print. Below: a proof strip of press quotes (serif) and ratings, a "Level up with Premium" feature list with icon tiles beside a phone mock, and a dark band with topic chips.

## Responsive rules

- Gutters 20–24px on phones; nothing wider than the viewport; every control ≥ 44px tall.
- Hero and sections go single-column below 1280/992; feature rows stack copy above media.
- Sticky course card becomes a centred header below 992.
- Bottom CTAs become full-width; feedback sheets and modals become bottom sheets.
- App bar nav collapses to icons (labels hidden below 769) or a menu button.
