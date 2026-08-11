# Presentation Design System

## Contents

1. System contract
2. Canvas and grid
3. Color
4. Typography
5. Spacing and geometry
6. Rhythm and optical alignment
7. Imagery and icons
8. System prompt
9. Consistency checks

## System contract

Define the design system before slide authoring and reuse it across the deck. Variation should come from composition and content, not from changing the visual language page by page.

Derive the system from the visual thesis in `art-direction.md`. A design system is not a neutral token library: it is the repeatable expression of the deck's character. Record not only values but also the intended behavior of those values.

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

Define a color ratio and emphasis rule. A useful starting point is approximately 70–85% field/surface, 10–25% text and structure, and no more than 5–10% accent. Adjust for dark or expressive directions, but keep accent scarce enough to mean something.

Avoid using accent color on every title, icon, number, connector, and border. Choose its semantic job, such as “recommended path,” “causal link,” “new state,” or “selected evidence.”

## Typography

Recommended SVG sizes for the 1600×900 canvas:

| Role | SVG px | Approx. PowerPoint pt |
|---|---:|---:|
| Deck title | 72–88 | 43.2–52.8 |
| Slide title | 48–56 | 28.8–33.6 |
| Section lead | 36–40 | 21.6–24 |
| Subheading/callout | 32 | 19.2 |
| Body | 22–28 | 13.2–16.8 |
| Caption/footer | 16–20 | 9.6–12 |

These ranges are selection guidance, not permission to vary sizes slide by slide. Before authoring the representative samples, convert them into one exact deck contract. A practical default is:

```json
{
  "deck_title": {"size": 80, "weight": 700, "line_height": 1.05},
  "slide_title": {"size": 52, "weight": 700, "line_height": 1.1},
  "section_title": {"size": 40, "weight": 700, "line_height": 1.12},
  "subheading": {"size": 30, "weight": 700, "line_height": 1.2},
  "body": {"size": 24, "weight": 400, "line_height": 1.4},
  "label": {"size": 20, "weight": 600, "line_height": 1.25},
  "caption": {"size": 18, "weight": 400, "line_height": 1.3}
}
```

Adapt the values once for the audience, venue, language, and selected art direction, then freeze them. Apply these invariants:

- Every ordinary `slide-title` uses the same exact size, family, weight, and line-height across the deck.
- Every recurring semantic role uses one exact token across the deck unless the design-system contract explicitly defines a named variant.
- All peer headings, peer labels, comparison columns, process steps, and repeated card headings on the same slide use identical tokens.
- Cover titles, section transitions, hero metrics, and quotations may use separate named roles; they are not arbitrary exceptions to `slide-title`.
- Define hero typography through named `deck-title` or `section-title` treatments. It may use a display family, extreme scale, stacked lines, outline-like contrast, crop, overlap, or controlled rotation, but every recurrence of that named treatment must remain intentional and legible.
- Do not create near-duplicate sizes such as 30/31/32 merely to make individual boxes fit.
- Shorten copy, adjust line breaks, widen the region, or split the slide before reducing a locked font size.
- Add `data-role="slide-title|section-title|subheading|body|label|metric|caption|source|quote|annotation|page-number"` to each visible `<text>` element so the deterministic typography audit can verify the contract.

The compiler maps font size through the same `viewBox`-to-slide scale as geometry. On the default 1600×900 canvas, one SVG unit is `0.6 pt`; for example, `48` compiles to `28.8 pt`. A different `viewBox` changes that ratio, so validate typography in both rendered PNGs and the compiled PPTX instead of assuming a fixed CSS-pixel conversion.

Default Chinese font stack:

```text
Microsoft YaHei, PingFang SC, Noto Sans CJK SC, sans-serif
```

When the approved direction calls for artistic Chinese display type, define it as a separate named role instead of replacing the deck's readable type system. A practical stack is:

```text
STXingkai, FZShuTi, KaiTi, STKaiti, serif
```

Apply that display stack only to short `deck-title`, `section-title`, or featured `quote` treatments. Keep ordinary `slide-title`, `subheading`, `body`, labels, chart text, and sources in the readable sans-serif stack. Before authoring, verify the selected display font is installed on the rendering and delivery systems, record the approved fallback, and never bundle a font file unless its redistribution license is clear. If exact artistic glyph shape matters more than editability, convert only that display treatment to an authorized vector/image asset and disclose the tradeoff; never rasterize ordinary presentation text.

Keep one-line titles on one line. Shorten copy or change layout before shrinking type. Use weight and scale for hierarchy; avoid many unrelated font sizes.

Define a small set of typographic behaviors in addition to sizes:

- title case and punctuation policy;
- maximum title line length and preferred line-break shape;
- numeric treatment for metrics and dates;
- weight contrast between claim, evidence, and annotation;
- Chinese/Latin pairing and fallback expectations;
- caption and source treatment;
- when text may become the dominant visual.

Use line length as a design variable. Wide lines reduce reading comfort and weaken hierarchy; narrow lines can create deliberate rhythm but should not fragment ordinary body copy. Align text by visible letterforms, not only by textbox edges.

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

Do not make the grid visible on every slide. Keep shared rails and spacing underneath the system, then allow a dominant headline, image, number, diagonal, arc, crop, or foreground layer to break the grid deliberately. Professional compositions may be asymmetric and visually tense while remaining precise; distinguish controlled off-grid gestures from accidental misalignment.

Define geometry by meaning. Sharp corners may feel exacting or editorial; moderate radii may feel approachable; large pill shapes imply controls or tags and should not be used as generic decoration. Use circles for cycles, focal nodes, or numeric moments—not as arbitrary background bubbles.

## Rhythm and optical alignment

Grid alignment establishes trust, but optical correction makes the result feel finished.

- Reuse a small set of vertical rails, baselines, and content widths.
- Align visual centers, not only mathematical boxes, when icons or type have uneven mass.
- Let large type or images break the grid only as an intentional focal gesture.
- Use diagonals, curves, overlap, and crop as directional forces that guide attention; do not scatter them as decorative noise.
- Keep recurring title, footer, and source positions exact across slides.
- Vary composition through scale and proportion while preserving spatial cadence.
- Use repeated gaps as rhythm; use one larger gap to mark a change in meaning.
- Check projected viewing distance: weak gray, hairline borders, and small captions often disappear.

Plan density bands for the deck, for example:

```text
quiet opening -> medium orientation -> dense evidence -> quiet synthesis
```

Do not let every page occupy the same percentage of the canvas.

## Imagery and icons

Choose one image treatment: full-bleed, framed editorial crop, clean product cutout, or documentary screenshot. Keep crop logic and corner treatment consistent.

Use `<image>` for photos, screenshots, complex illustrations, and product renders. Preserve aspect ratio with `preserveAspectRatio="xMidYMid meet"` for contain or `xMidYMid slice` for cover.

Use a coherent icon family with consistent stroke/fill style. Simple icons may be authored as SVG paths but will compile as embedded SVG fallback. If individual editability is required, rebuild the icon from supported basic shapes.

Treat photography, screenshots, illustration, diagrams, and icons as different evidence classes. Give each a defined role and treatment. Do not mix glossy stock photography, flat icons, hand-drawn illustration, and photorealistic renders without an explicit art-direction reason.

## System prompt

Use this internal prompt before authoring slide 1:

```text
Translate the approved visual thesis into a compact, reusable design system.

Define:
- canvas, safe area, grid, rails, and preferred content widths;
- field/surface behavior and light or dark mode;
- color roles, ratios, semantic accent rules, and contrast floor;
- type families, roles, sizes, weights, line heights, and title behavior;
- spacing scale, border language, radius logic, and connector grammar;
- image crop, frame, caption, and annotation treatment;
- icon/illustration family and fallback implications;
- recurring page furniture and section-transition behavior;
- density plan and the conditions under which a slide may break the grid.

For every token, state what it communicates and where it must not be used.
Keep the system small enough to remember and rich enough to produce varied slides.
```

## Consistency checks

- Same background and palette logic across the deck.
- Same title rail, title scale, and page-margin system.
- Same font families, weights, and body sizes.
- Artistic display fonts are restricted to approved named hero roles, have a tested fallback, and do not leak into ordinary titles or body copy.
- One exact `slide-title` token across the deck and exact peer-heading tokens within each slide.
- Strict typography audit passes with no missing roles or inconsistent deck tokens.
- Same border, radius, connector, and icon language.
- Similar visual density across adjacent slides unless a deliberate pacing shift is planned.
- Repeated elements share exact geometry rather than near-matches.
- Section transitions change composition without appearing to switch templates.
- Color, geometry, imagery, and typography express the approved visual thesis.
- Accent remains meaningful because it is not used everywhere.
- Optical alignment and density rhythm have been checked on rendered slides.
