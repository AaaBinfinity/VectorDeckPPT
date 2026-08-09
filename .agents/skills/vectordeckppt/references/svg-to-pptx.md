# SVG to PowerPoint Mapping

## Contents

1. Conversion priority
2. Mapping table
3. Coordinates
4. Text strategy
5. Images
6. Groups and opacity
7. Office SVG fallback
8. Compilation report
9. Known limitations

## Conversion priority

The compiler uses this order:

```text
native PowerPoint object -> embedded Office SVG fallback -> explicit failure
```

It never silently drops a visible element and never rasterizes the whole slide as the default path.

## Mapping table

| SVG | PowerPoint | Status | Editability |
|---|---|---|---|
| `text` | TextBox | Native | text, font, size, color editable |
| basic `tspan` | Text run / positioned TextBox line | Native | editable |
| `rect` | Rectangle | Native | editable |
| `rect rx/ry` | Rounded rectangle | Native | editable |
| `circle` | Oval | Native | editable |
| `ellipse` | Oval | Native | editable |
| `line` | Straight connector | Native | editable |
| `image` | Picture | Native | picture/crop editable |
| basic `g` | flattened objects with inherited style/transform | Native basics | child objects editable |
| straight-segment `polygon`/`polyline` | PowerPoint Freeform | Native freeform | points, fill, and stroke editable |
| `path` | PNG preview + Office SVG relation | Fallback | object editable; internal path not native |
| gradient/clip/rotated element or styled freeform with markers/dashes | PNG preview + Office SVG relation | Fallback | object-level editing only |
| forbidden/invalid element | compilation error | Failed | no output deck |

Native freeforms cover straight-segment `polygon` and `polyline` geometry, including accumulated axis-aligned translation/scaling and non-zero `viewBox` origins. Complex `path` data, markers, dashed freeforms, paint servers, rotation, and skew remain explicit fallbacks.

## Coordinates

Default mapping:

```text
SVG 1600 × 900
PowerPoint 13.333333 × 7.5 inches
```

All conversion lives in `scripts/lib/coordinates.py`. ViewBox origins are subtracted before scaling. The compiler sets a 16:9 slide size and keeps the SVG draw order as PowerPoint z-order.

## Text strategy

SVG `y` is an alphabetic baseline while a PowerPoint TextBox uses a top coordinate. The compiler applies a baseline-to-top estimate based on font size, converts the SVG font size through the same viewBox-to-slide scale used for geometry, estimates line width, and positions the textbox using `text-anchor`. On the default 1600 × 900 canvas, `font-size="48"` maps to `28.8 pt` in PowerPoint.

Native text supports font family, size, bold weight, italic style, fill color, fill opacity, group opacity, basic tspans, and alphabetic baselines. Pretty-print-only whitespace between tspans is removed unless `xml:space="preserve"` requests literal spacing. Non-alphabetic `dominant-baseline` modes use explicit fallback instead of silently changing placement. Chinese text remains searchable, copyable, and editable.

Font metrics differ across systems. The PNG SVG preview is the visual source, but the compiled PPTX must also be rendered and inspected when exact line breaks or alignment are important.

## Images

Local files and embedded data URIs become PowerPoint pictures. The compiler reads the source aspect ratio:

- `meet` calculates a centered contain box;
- `slice` fills the specified box and sets non-destructive PowerPoint crop fractions;
- images are not stretched to arbitrary width and height.

## Groups and opacity

Groups are flattened to individual PowerPoint objects while preserving child order. Basic inherited styles, translation, scaling, and multiplicative opacity are resolved before conversion.

Rotation and skew cannot be flattened faithfully into every native PowerPoint shape, so affected visible elements use fallback.

## Office SVG fallback

For each fallback element, the compiler creates an isolated full-canvas SVG containing the element, inherited styles, accumulated transform, and relevant `<defs>`. It then:

1. renders a PNG compatibility preview;
2. inserts the preview as a picture;
3. adds the original SVG as an `image/svg+xml` package part;
4. adds the Office `svgBlip` extension relation.

This preserves appearance in modern Office while retaining a compatibility image. Treat fallback as partially editable and disclose it to the user.

## Compilation report

The CLI emits JSON and can persist it with `--report`:

```json
{
  "valid": true,
  "slide_count": 5,
  "native": 42,
  "freeform": 3,
  "embedded_svg": 2,
  "failed": 0,
  "slides": []
}
```

- `native`: source elements converted to native PowerPoint objects;
- `freeform`: source polygons or polylines converted to editable PowerPoint freeforms;
- `embedded_svg`: source elements preserved through fallback;
- `failed`: validation or conversion failures.

Any non-zero `failed` count prevents the compiler from writing the output PPTX.

## Known limitations

- Full SVG specification coverage is not a goal.
- Complex SVG path-to-PowerPoint freeform conversion is not implemented; only straight-segment polygons and polylines are native.
- Gradients, clipping, rotation, and skew generally use fallback.
- Font substitution can change line metrics across machines.
- Tspan positioning is intentionally basic; browser text layout is not reproduced.
- SVG filters, masks, animation, `foreignObject`, remote resources, and interaction are rejected.
- PowerPoint charts, animations, transitions, and speaker notes are outside the MVP compiler.
