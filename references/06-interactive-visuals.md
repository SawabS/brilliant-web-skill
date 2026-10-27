# Interactive visuals, charts, diagrams

Brilliant teaches by letting people move things. Templates: `templates/interactive.html` (an explorable), `app-lesson.html` (a lesson widget), `dashboard.html` and `deck.html` (charts).

## Explorables

Structure, top to bottom:
1. Kicker (hue) + serif title that names the idea as a claim ("Three numbers shape every parabola").
2. One sentence of instruction with a single `.term`.
3. A `.widget` holding the visual on an oat `.stage`, a hint in the corner ("Drag the sliders").
4. Controls: `.slider`s (each in its own hue, matching what it controls in the visual and the formula), `.segmented` for modes, `.btn3d--white` Reset + one dark 3D action.
5. Readouts in semi-mono (`.readout`), tabular.
6. A **challenge** (a `card--lip` goal) that turns green with `borderGlow` and the correct chime when met. Always give one concrete goal.

Behaviour:
- Respond on `input`, not `change`: the visual follows the finger in real time.
- Colour-link everything: the `a` slider is blue, `a` in the formula is blue, the curve part it affects is blue.
- Snap to meaningful steps (0.1, 0.5, integers); show the value next to the label.
- Give feedback in words beside the visual ("At x = 2 the curve is at y = 3.0. You need 2."), never just colour.
- Start from a state that is wrong in an interesting way, so the first move teaches something.
- Keep it keyboard-operable (native range inputs, buttons) and label everything.

## Sound (optional, on by default in templates)

`js/brilliant.js` ships a synthesized set (Web Audio, no files): `tap` (wooden tok on any press), `toggle`, `select` (bubble pop on choosing), `tick` (slider detents), `reveal` (page breath + mallet), `unlock` (Check becomes available), `correct` (three rising mallet notes C5-E5-G5), `wrong` (low muffled double knock, never harsh), `open`/`close` (drawers), `complete` (arpeggio + chord). Sounds only ever follow a user action. `B.sfx.setEnabled(false)` mutes and is remembered.

## Charts

| Rule | Value |
|---|---|
| Series order | blue-500, orange-500, purple-500, teal-500, pink-500, yellow-600 (then green-500, papaya-500) |
| Comparison / baseline series | the same hue at 300, or grey-400 dashed |
| Lines | 3px (7px on slides), round caps and joins; end marker = 5px circle, background fill, hue stroke |
| Labels | direct, at the line end, 12px/500 in `--text-<hue>-primary`; a legend only when lines cross a lot |
| Bars | hue-500 fill, 4–8px top radius, gaps ≥ 30% of bar width; single-series bars in one hue, highlight the point of interest in the hue and the rest grey-300 |
| Axes | left and bottom only; baseline `--border-gray-primary`; grid `--border-secondary`, horizontal only; ticks `body.xs` tertiary (data.axis 10px only for dense charts) |
| Background | none, or the oat stage; no chart borders, no 3D, no gradients, no drop shadows |
| Highlights | annotate the one number that matters (filled dot + bold label) |
| Ranges | a `-tertiary` band behind the line |
| Progress / share | `.progress` bars in hue-500 with right-aligned tabular percentages |

Matplotlib equivalent:

```python
import matplotlib as mpl
mpl.rcParams.update({
  "font.family": "Inter", "font.size": 11, "axes.spines.top": False, "axes.spines.right": False,
  "axes.edgecolor": "#b3b3b3", "axes.grid": True, "grid.color": "#0000000d", "axes.axisbelow": True,
  "xtick.color": "#00000099", "ytick.color": "#00000099", "axes.labelcolor": "#00000099",
  "axes.prop_cycle": mpl.cycler(color=["#456dff", "#ff8d23", "#9d62ff", "#2cb0a1", "#ff6bd5", "#d7a613"]),
  "lines.linewidth": 2.5, "lines.solid_capstyle": "round", "svg.fonttype": "none", "figure.facecolor": "white",
})
```

## Diagrams

- Blocks: white rounded rectangles (radius 12–16), 2px `--border-solid` (1px in print), on an oat stage. Group by tinting the block with a `-tertiary` fill and `-primary` text.
- Pipelines: black pills (`--bg-inverse-primary`, white text) joined by `--text-tertiary` arrows, 1.5–2px, small heads.
- Isometric objects (tiles, coins, stacks) for anything physical: top face hue-400, left side hue-600, right side hue-700.
- Mermaid: use `tools/md2pdf/mermaid.json` (blue-100 nodes with blue-400 borders, grey lines, Inter 15px) and round the rectangles.
- Highlight the active element with a 3px blue-500 ring and `borderGlow`.

## Maths and code

- Maths: KaTeX (`ui.interactives.math` 19/24, 23/30 for display). Colour variables to match their controls. Load `katex.min.css` + `katex.min.js` (+ auto-render) from jsDelivr or a vendored copy.
- Code: the black "probe" theme (`.code`), 15/24 Source Code Pro; highlight the active line with `.line--active`; run buttons are `.btn3d--sm`.
- Inline code: `--bg-secondary`, 15px/500.

## Canvas / WebGL visuals

Read colours from CSS at runtime so themes work: `getComputedStyle(document.documentElement).getPropertyValue('--blue-500')`. Redraw on `data-theme` change (observe the attribute). Keep 60fps on interaction, and freeze ambient loops under reduced motion.
