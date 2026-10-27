#!/usr/bin/env python3
"""Generate tokens/tokens.css, tokens/tokens.json and tokens/tailwind.preset.js
from source/brilliant-tokens.json (the raw capture).

    python3 tools/build_tokens.py

Naming: Panda's `--panda-colors-bg-primary` becomes `--bg-primary`,
`--panda-colors-blue-500` becomes `--blue-500`, `--panda-radii-2xl` becomes
`--radius-2xl`, `--panda-spacing-4` becomes `--space-4`, text style
`heading.lg` becomes the class `.ts-heading-lg` and the token group
`--ts-heading-lg-*`.
"""
import json
import pathlib
import re

ROOT = pathlib.Path(__file__).resolve().parent.parent
RAW = json.loads((ROOT / "source" / "brilliant-tokens.json").read_text())
L, D = RAW["light"], RAW["dark"]

RAMPS = ["gray", "blue", "green", "yellow", "orange", "red", "pink", "purple",
         "teal", "mint", "cyan", "pear", "papaya", "oat"]
STEPS = ["50", "100", "200", "300", "400", "500", "600", "700", "800", "850", "900", "950"]
ALPHA = ["50", "100", "200", "300", "400", "500", "600", "700", "800", "900", "950", "1000"]

SEMANTIC_PREFIXES = ("bg-", "text-", "icon-", "border-", "elevation-shadow-", "status-")
SPECIAL_KEEP = ("special-lesson-", "special-probe-code-", "special-overlay-",
                "special-endstate-streak-", "special-bg-primary-0")
SEMANTIC_DROP = ("quip", "tutor", "upsell", "sale", "video-ad", "iridescent-secondary",
                 "special-probe-expand")

FONT_STACKS = {
    "brilliant": '"CoFo Brilliant", "Inter", "Helvetica Neue", Arial, system-ui, sans-serif',
    "robert": '"CoFo Robert", "Besley Display", "Besley", Georgia, serif',
    "semi-mono": '"CoFo Semi Mono", "DM Mono", "IBM Plex Mono", ui-monospace, monospace',
    "code": '"Source Code Pro", ui-monospace, "SFMono-Regular", Menlo, monospace',
    "math": 'KaTeX_Main, "Latin Modern Roman", "Times New Roman", serif',
}
FONT_VAR = {"brilliant": "--font-sans", "robert": "--font-display", "semi-mono": "--font-semi-mono",
            "code": "--font-code", "math": "--font-math"}


def ref(v: str, theme: dict) -> str:
    """Rewrite var(--panda-colors-x) -> var(--x); resolve autoflip aliases per theme."""
    def sub(m):
        name = m.group(1)
        if name.startswith("autoflip-"):
            target = theme.get("colors-" + name) or L.get("colors-" + name)
            if target:
                return ref(target, theme)
        return f"var(--{name})"
    v = re.sub(r"var\(--panda-colors-([\w-]+)\)", sub, v)
    v = re.sub(r"var\(--panda-shadows-([\w-]+)\)", r"var(--shadow-\1)", v)
    return v


def hexnorm(v: str) -> str:
    v = v.strip()
    if v == "gray":
        return "#808080"
    m = re.fullmatch(r"#([0-9a-fA-F]{3,8})", v)
    if not m:
        return v
    h = m.group(1).lower()
    if len(h) in (3, 4):
        h = "".join(c * 2 for c in h)
    return "#" + h


def primitives():
    out = {"black": "#000000", "white": "#ffffff", "dark-gray": hexnorm(L["colors-dark-gray"]),
           "dark-gray-alpha": hexnorm(L["colors-dark-gray-alpha"])}
    for r in RAMPS:
        for s in STEPS:
            k = f"colors-{r}-{s}"
            if k in L:
                out[f"{r}-{s}"] = hexnorm(L[k])
    for a in ("black", "white"):
        for s in ALPHA:
            k = f"colors-{a}-alpha-{s}"
            if k in L:
                out[f"{a}-alpha-{s}"] = hexnorm(L[k])
    return out


def semantic(theme: dict):
    out = {}
    for k, v in theme.items():
        if not k.startswith("colors-"):
            continue
        n = k[len("colors-"):]
        if not (n.startswith(SEMANTIC_PREFIXES) or n.startswith(SPECIAL_KEEP)):
            continue
        if any(x in n for x in SEMANTIC_DROP):
            continue
        out[n] = hexnorm(ref(v, theme))
    return out


def text_styles():
    out = {}
    for name, props in RAW["textStyles"].items():
        fam = props.get("font-family", "")
        m = re.search(r"--panda-fonts-([\w-]+)", fam)
        out[name.replace(".", "-")] = {
            "family": m.group(1) if m else "brilliant",
            "size": props.get("font-size"), "weight": props.get("font-weight"),
            "lineHeight": props.get("line-height"),
            "letterSpacing": props.get("letter-spacing", "0").replace("0em", "0"),
            "transform": props.get("text-transform"),
        }
    return dict(sorted(out.items()))


def scale(prefix: str, src: dict, strip: str):
    out = {}
    for k, v in src.items():
        if k.startswith(strip):
            out[k[len(strip):].replace("\\.", ".")] = v
    return out


PRIM = primitives()
DM = {**L, **D}  # dark only lists overrides; aliases (autoflip-*) must resolve against dark
SEM_L, SEM_D = semantic(L), semantic(DM)
TS = text_styles()
SPACE = scale("space", L, "spacing-")
RADII = scale("radius", L, "radii-")
SHADOWS = {k: ref(v, L) for k, v in scale("shadow", L, "shadows-").items()}
LS = scale("ls", L, "letter-spacings-")
SIZES = {k: v for k, v in scale("size", L, "sizes-").items()
         if k in ("prose", "app-bar", "container-sm", "container-lg", "nux-header-height")
         or k in ("xs", "sm", "md", "lg", "xl", "2xl", "3xl", "4xl", "5xl", "6xl", "7xl", "8xl")}
BREAKPOINTS = scale("bp", L, "breakpoints-")
ZKEEP = ["hide", "base", "docked", "relative-front", "app-bar", "dropdown", "sticky", "banner",
         "overlay", "modal", "popover", "skip-nav", "toast", "tooltip"]
Z = {k: L[f"z-index-{k}"] for k in ZKEEP if f"z-index-{k}" in L}
GRAD_KEEP = ["iridescent-frame", "iridescent-frame-faded", "iridescent-frame-muted",
             "iridescent-premium-copy", "iridescent-secondary", "hue-shift-upgrade-iridescent-primary",
             "discount-gold"] + [f"hue-shift-color-{h}-{t}" for h in
                                 ("blue", "orange", "papaya", "pear", "purple", "teal", "yellow")
                                 for t in ("primary", "secondary")]
GRAD_L = {k: ref(L["gradients-" + k], L) for k in GRAD_KEEP if "gradients-" + k in L}
GRAD_D = {k: ref(D["gradients-" + k], D) for k in GRAD_KEEP if "gradients-" + k in D}

MOTION = {
    "ease-standard": "cubic-bezier(.4, 0, .2, 1)",
    "ease-spring-smooth": "cubic-bezier(.2, 1.1, .36, 1)",
    "ease-xp-pulse": "cubic-bezier(.25, .75, .18, 1.09)",
    "ease-out": "ease-out",
    "dur-press": "100ms",
    "dur-fast": "150ms",
    "dur-normal": "200ms",
    "dur-slow": "300ms",
    "dur-spring-smooth": "833ms",
}


def block(selector: str, items: list, indent="  ") -> str:
    return selector + " {\n" + "\n".join(f"{indent}{k}: {v};" for k, v in items) + "\n}\n"


def css():
    parts = ["/* Brilliant design tokens — generated by tools/build_tokens.py from\n"
             "   source/brilliant-tokens.json (captured from brilliant.org, Oct 2026).\n"
             "   Do not edit by hand: change the generator or the source and re-run. */\n"]
    prim = [(f"--{k}", v) for k, v in PRIM.items()]
    base = []
    base += [(FONT_VAR[k], v) for k, v in FONT_STACKS.items()]
    base += [("--font-body", "var(--font-sans)"), ("--font-heading", "var(--font-sans)")]
    base += [(f"--space-{k.replace('.', '_')}", v) for k, v in SPACE.items()]
    base += [(f"--radius-{k}", v) for k, v in RADII.items()]
    base += [(f"--size-{k}", v) for k, v in SIZES.items()]
    base += [(f"--ls-{k}", v) for k, v in LS.items()]
    base += [(f"--z-{k}", v) for k, v in Z.items()]
    base += [(f"--{k}", v) for k, v in MOTION.items()]
    for name, t in TS.items():
        fam = FONT_VAR.get(t["family"], "--font-sans")
        base += [(f"--ts-{name}", f'{t["weight"]} {t["size"]}/{t["lineHeight"]} var({fam})'),
                 (f"--ts-{name}-ls", t["letterSpacing"] or "0")]
    parts.append("/* Primitives (identical in every theme) and scales */\n")
    parts.append(block(":root", prim + base))

    light = [(f"--{k}", v) for k, v in sorted(SEM_L.items())]
    light += [(f"--shadow-{k}", v) for k, v in SHADOWS.items()]
    light += [(f"--gradient-{k}", v) for k, v in GRAD_L.items()]
    light += [("color-scheme", "light")]
    dark = [(f"--{k}", v) for k, v in sorted(SEM_D.items())]
    dark += [(f"--shadow-{k}", v) for k, v in SHADOWS.items()]
    dark += [(f"--gradient-{k}", v) for k, v in {**GRAD_L, **GRAD_D}.items()]
    dark += [("color-scheme", "dark")]
    parts.append("\n/* Semantic roles: light (default) */\n")
    parts.append(block(':root, [data-theme="light"]', light))
    parts.append("\n/* Semantic roles: dark — explicit opt-in */\n")
    parts.append(block('[data-theme="dark"]', dark))
    parts.append("\n/* Semantic roles: dark — follow the OS unless the page forces light */\n")
    parts.append("@media (prefers-color-scheme: dark) {\n" +
                 block('  :root:not([data-theme="light"])', dark, "    ").replace("\n}", "\n  }") + "}\n")

    parts.append("\n/* Text styles: one class per named style (Brilliant's textStyle tokens) */\n")
    for name, t in TS.items():
        extra = f" text-transform: {t['transform']};" if t["transform"] else ""
        parts.append(f".ts-{name} {{ font: var(--ts-{name}); letter-spacing: var(--ts-{name}-ls);{extra} }}\n")
    bp = ", ".join(f"{k} {v}" for k, v in BREAKPOINTS.items())
    parts.append(f"\n/* Breakpoints (min-width, use literally in @media): {bp} */\n")
    return "".join(parts)


def dtcg():
    def c(v):
        return {"$type": "color", "$value": v}
    color = {}
    for k, v in PRIM.items():
        m = re.match(r"(.+)-(\d+)$", k)
        if m:
            color.setdefault(m.group(1), {})[m.group(2)] = c(v)
        else:
            color[k] = c(v)
    return {
        "$description": "Brilliant design tokens (captured from brilliant.org Panda CSS, Oct 2026). "
                        "Semantic values reference primitives as CSS var() strings.",
        "color": color,
        "semantic": {"light": {k: c(v) for k, v in sorted(SEM_L.items())},
                     "dark": {k: c(v) for k, v in sorted(SEM_D.items())}},
        "font": {k: {"$type": "fontFamily", "$value": v} for k, v in FONT_STACKS.items()},
        "textStyle": {k: {"$type": "typography", "$value": {
            "fontFamily": f"{{font.{v['family']}}}", "fontSize": v["size"], "fontWeight": v["weight"],
            "lineHeight": v["lineHeight"], "letterSpacing": v["letterSpacing"],
            **({"textTransform": v["transform"]} if v["transform"] else {})}} for k, v in TS.items()},
        "space": {k: {"$type": "dimension", "$value": v} for k, v in SPACE.items()},
        "radius": {k: {"$type": "dimension", "$value": v} for k, v in RADII.items()},
        "shadow": {k: {"$type": "shadow", "$value": v} for k, v in SHADOWS.items()},
        "size": {k: {"$type": "dimension", "$value": v} for k, v in SIZES.items()},
        "letterSpacing": {k: {"$type": "dimension", "$value": v} for k, v in LS.items()},
        "breakpoint": {k: {"$type": "dimension", "$value": v} for k, v in BREAKPOINTS.items()},
        "zIndex": {k: {"$type": "number", "$value": v} for k, v in Z.items()},
        "motion": {k: {"$value": v} for k, v in MOTION.items()},
        "gradient": {"light": GRAD_L, "dark": {**GRAD_L, **GRAD_D}},
        "keyframes": RAW["keyframes"],
    }


def tailwind():
    prim = {}
    for k in PRIM:
        m = re.match(r"(.+)-(\d+)$", k)
        if m:
            prim.setdefault(m.group(1), {})[m.group(2)] = f"var(--{k})"
        else:
            prim[k] = f"var(--{k})"
    groups = {}
    for k in SEM_L:
        head, _, rest = k.partition("-")
        groups.setdefault(head, {})[rest] = f"var(--{k})"
    fs = {k: [t["size"], {"lineHeight": t["lineHeight"], "letterSpacing": t["letterSpacing"] or "0",
                          "fontWeight": t["weight"]}] for k, t in TS.items()}
    preset = {
        "darkMode": ["selector", '[data-theme="dark"]'],
        "theme": {
            "screens": BREAKPOINTS,
            "extend": {
                "colors": {**prim, **{f"{g}": v for g, v in groups.items()}},
                "fontFamily": {"sans": [FONT_STACKS["brilliant"]], "display": [FONT_STACKS["robert"]],
                               "semimono": [FONT_STACKS["semi-mono"]], "code": [FONT_STACKS["code"]],
                               "math": [FONT_STACKS["math"]]},
                "fontSize": fs,
                "borderRadius": RADII,
                "boxShadow": {**{k: f"var(--shadow-{k})" for k in SHADOWS},
                              "lip": "0 4px 0 0 var(--border-solid)",
                              "lip-inverse": "0 4px 0 0 var(--elevation-shadow-cta-default)"},
                "zIndex": Z,
                "maxWidth": {"container": SIZES.get("container-lg", "1216px"), "prose": "60ch"},
                "transitionTimingFunction": {"standard": MOTION["ease-standard"],
                                             "spring": MOTION["ease-spring-smooth"]},
            },
        },
    }
    return ("/** Tailwind preset for the Brilliant design system — generated by tools/build_tokens.py.\n"
            " *  Requires tokens/tokens.css to be loaded (colours resolve through CSS variables,\n"
            " *  so light/dark switch with data-theme). Usage: presets: [require('./tailwind.preset.js')] */\n"
            "module.exports = " + json.dumps(preset, indent=2) + ";\n")


if __name__ == "__main__":
    (ROOT / "tokens").mkdir(exist_ok=True)
    (ROOT / "tokens" / "tokens.css").write_text(css())
    (ROOT / "tokens" / "tokens.json").write_text(json.dumps(dtcg(), indent=1))
    (ROOT / "tokens" / "tailwind.preset.js").write_text(tailwind())
    print(f"primitives={len(PRIM)} semantic light={len(SEM_L)} dark={len(SEM_D)} textStyles={len(TS)}")
