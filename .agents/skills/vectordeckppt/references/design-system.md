# Presentation Design System

## Contents

1. System contract
2. Canvas and grid
3. Color
4. Typography
5. Spacing and geometry
6. Imagery and icons
7. Consistency checks

## System contract

Define the design system before slide authoring and reuse it across the deck. Variation should come from composition and content, not from changing the visual language page by page.

Record a compact token set. JSON is optional, but the decisions are not.

## Canvas and grid

Default canvas:

```json
{
  "width": 1600,
  "height": 900,
  "aspect_ratio": "16:9",
  "grid": 8,
  "page_margin_x": 96,
  "page_margin_y": 72
}
```

Use the 8-unit grid for baselines and component gaps. Keep equal left/right margins unless a deliberate full-bleed composition requires otherwise. Align slide titles, core content, and footers to shared rails.

## Color

Default minimal technology palette:

```json
{
  "background": "#F8FAFC",
  "surface": "#FFFFFF",
  "primary": "#2563EB",
  "secondary": "#7C3AED",
  "title": "#0F172A",
  "text": "#475569",
  "muted": "#94A3B8",
  "border": "#E2E8F0",
  "positive": "#059669",
  "warning": "#D97706",
  "negative": "#DC2626"
}
```

Use one primary and one restrained secondary accent. Reserve semantic colors for meaning. Check contrast on the actual rendered preview. Avoid gradients unless the content benefits and accept that paint servers compile as embedded SVG fallback.

## Typography

Recommended SVG sizes for the 1600×900 canvas:

| Role | SVG px | Approx. PowerPoint pt |
|---|---:|---:|
| Deck title | 72–88 | 54–66 |
| Slide title | 48–56 | 36–42 |
| Section lead | 36–40 | 27–30 |
| Subheading/callout | 32 | 24 |
| Body | 22–28 | 16.5–21 |
| Caption/footer | 16–20 | 12–15 |

Default Chinese font stack:

```text
Microsoft YaHei, PingFang SC, Noto Sans CJK SC, sans-serif
```

Keep one-line titles on one line. Shorten copy or change layout before shrinking type. Use weight and scale for hierarchy; avoid many unrelated font sizes.

## Spacing and geometry

Recommended spacing values:

```text
8, 16, 24, 32, 40, 48, 64, 80, 96
```

Default shape rules:

- border: 1–3 canvas units depending on emphasis;
- card radius: 20–28 only where a surface is genuinely useful;
- no theme shadows unless explicitly authored in a supported representation;
- generous internal padding: normally 24–40;
- consistent connector weight and direction semantics.

Do not wrap every section in a card. Prefer flat composition, whitespace, bands, rails, and direct alignment. Use stylized boxes only when they clarify grouping.

## Imagery and icons

Choose one image treatment: full-bleed, framed editorial crop, clean product cutout, or documentary screenshot. Keep crop logic and corner treatment consistent.

Use `<image>` for photos, screenshots, complex illustrations, and product renders. Preserve aspect ratio with `preserveAspectRatio="xMidYMid meet"` for contain or `xMidYMid slice` for cover.

Use a coherent icon family with consistent stroke/fill style. Simple icons may be authored as SVG paths but will compile as embedded SVG fallback. If individual editability is required, rebuild the icon from supported basic shapes.

## Consistency checks

- Same background and palette logic across the deck.
- Same title rail, title scale, and page-margin system.
- Same font families, weights, and body sizes.
- Same border, radius, connector, and icon language.
- Similar visual density across adjacent slides unless a deliberate pacing shift is planned.
- Repeated elements share exact geometry rather than near-matches.
- Section transitions change composition without appearing to switch templates.
