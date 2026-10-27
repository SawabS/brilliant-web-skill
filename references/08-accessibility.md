# Accessibility

Brilliant's palette is bright, and some of its production pairings fall short of WCAG AA. This system keeps the faithful values and tells you where to be careful.

## Contrast (measured on white unless noted)

| Pair | Ratio | Verdict |
|---|---|---|
| `--text-primary` (black) | 21:1 | ✓ |
| `--text-secondary` (black 60%) | 5.7:1 | ✓ body text |
| `--text-tertiary` (black 40%) | 2.9:1 | ✗ for essential text — captions, placeholders, inactive labels only |
| `--text-link` blue-500 | 4.3:1 | ≈ use at ≥ 16px/500 or underline; `data-contrast="more"` switches to blue-600 (5.5:1) |
| blue-700, purple-700, red-700 text | 7.2 / 6.7 / 5.3:1 | ✓ |
| teal-700, pink-700, papaya-700 | 4.5 / 4.3 / 4.2:1 | ≈ borderline |
| green-700, orange-700, yellow-700 | 3.7 / 3.7 / 3.2:1 | ✗ small text — large/bold only, or `data-contrast="more"` (800 = 5.4 / 5.5 / 4.8:1) |
| pear-700, mint-700 | 2.5 / 2.4:1 | ✗ never for text; use black on pear/mint fills |
| White on #383838 (primary 3D button) | 11.7:1 | ✓ |
| White on blue-500 | 4.3:1 | ≈ (16px/500 + text-shadow, as production does) |
| White on green-500 | 2.1:1 | ✗ production uses it for Sign up/Continue; prefer 20px/500 labels, the 0.25 text-shadow, or black text for small sizes |
| Black on pear-500 / yellow-500 | 15.5 / 12.8:1 | ✓ |
| Dark theme: white 70% on #141414 | 9.3:1 | ✓ |

Set `<html data-contrast="more">` to move every small coloured text role one step darker in light mode.

## Required behaviours

- **Focus**: every interactive element shows `0 0 0 3px var(--border-select)` (or the 1px+3px link ring). Never remove it.
- **Targets**: ≥ 44×44px on touch; ≥ 24px absolute minimum.
- **Not colour alone**: correct/incorrect use words ("Correct!", "Not quite"), icons (check) and motion (shake), plus `data-state` for scripts and `aria-live="polite"` on the feedback sheet.
- **Choices**: `role="radiogroup"` + `role="radio"` + `aria-checked`; segmented/tabs use `role="tab"` + `aria-selected`; toggles use `aria-pressed`.
- **Sliders**: native `<input type="range">` with a visible label and readout.
- **Motion**: honour `prefers-reduced-motion` (all animations collapse) and `data-reduced-motion="true"`.
- **Sound**: only after user actions; mutable, remembered.
- **Type**: never below 12px on screen or 7pt in print. Line length ≤ 60–70ch.
- **Dark mode**: check every hue text in dark; dark roles use 400s, which pass.
- **Language & direction**: the system works RTL with logical properties for new components (`margin-inline`, `padding-inline`, `inset-inline`); test Arabic-script text with a font that covers it.
