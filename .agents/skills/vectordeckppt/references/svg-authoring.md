# SVG Authoring Contract

## Contents

1. Required root
2. Supported visible elements
3. Coordinates and groups
4. Text
5. Shapes and styles
6. Images
7. Fallback features
8. Forbidden features
9. Authoring checklist

## Required root

For a default 16:9 slide, use exactly:

```svg
<svg xmlns="http://www.w3.org/2000/svg"
     width="1600"
     height="900"
     viewBox="0 0 1600 900">
  <!-- complete slide -->
</svg>
```

Use a different canvas only when the user explicitly requests another aspect ratio. Keep `width`, `height`, and `viewBox` consistent.

## Supported visible elements

Native editable PowerPoint conversion:

- `<text>` and basic `<tspan>` runs/lines;
- `<rect>` and `<rect rx="...">`;
- `<circle>` and `<ellipse>`;
- `<line>`;
- straight-segment `<polyline>` and `<polygon>` without markers or dashed strokes;
- `<image>`;
- basic `<g>` style, opacity, translation, and scaling inheritance.

Allowed but normally compiled as embedded Office SVG:

- `<path>`;
- `<polyline>` or `<polygon>` using markers, dashed strokes, or paint servers;
- native elements using gradients, clipping, rotation, or skew that cannot be represented faithfully by the native converter.

Use fallback features deliberately. If individual editing is required, simplify the visual into supported elements.

## Coordinates and groups

Author in canvas units. Use the shared 8-unit grid and keep core content within page margins.

Supported transforms include `translate`, `scale`, `rotate`, `skewX`, `skewY`, and `matrix` for validation/rendering. Native conversion is reliable for axis-aligned translation/scaling. Rotation or skew causes the affected visible element to use embedded SVG fallback.

Groups must not hide unsupported behavior. Parent fill, stroke, font, opacity, translation, and scaling are inherited/accumulated by the compiler.

Example:

```svg
<g transform="translate(96 180)" opacity="0.92"
   font-family="Microsoft YaHei, PingFang SC, Noto Sans CJK SC, sans-serif">
  <rect width="620" height="360" rx="24" fill="#FFFFFF" stroke="#E2E8F0"/>
  <text x="40" y="72" font-size="32" font-weight="700" fill="#0F172A">Key message</text>
</g>
```

## Text

Keep user-facing text as text. Do not convert Chinese or Latin text to paths by default.

Give every visible `<text>` element a semantic `data-role`. Supported role names are `deck-title`, `slide-title`, `section-title`, `subheading`, `body`, `label`, `metric`, `caption`, `source`, `quote`, `annotation`, and `page-number`. The attribute does not change rendering or compilation; it enables the strict deck typography audit to verify that recurring roles and same-page peers use exact shared tokens.

Supported properties:

- `x`, `y` (SVG alphabetic baseline);
- `font-family`, `font-size`, `font-weight`, `font-style`;
- `fill`, `fill-opacity`, `opacity`;
- `text-anchor="start|middle|end"`;
- basic `<tspan>` text runs with `x`, `y`, `dx`, and `dy` line positioning.

Native text assumes an alphabetic baseline. `dominant-baseline="auto|alphabetic"` remains native; other baseline modes use explicit Office SVG fallback so the compiler does not silently shift text.

Use an explicit font stack:

```svg
<text x="96" y="128"
      data-role="slide-title"
      font-family="Microsoft YaHei, PingFang SC, Noto Sans CJK SC, sans-serif"
      font-size="52" font-weight="700" fill="#0F172A">系统整体架构</text>
```

The compiler estimates the PowerPoint textbox from the SVG baseline and text anchor. Keep one-line titles concise and allow a small amount of horizontal breathing room. Render the PPTX itself when exact font fidelity is important.

For multiple lines, use explicit tspans:

```svg
<text data-role="body" x="96" y="300" font-size="26" fill="#475569">
  <tspan x="96" y="300">第一行</tspan>
  <tspan x="96" dy="42">第二行</tspan>
</text>
```

Do not depend on browser text wrapping or `foreignObject`.

For native shape strokes, `stroke-linecap="butt|round|square"` and `stroke-linejoin="miter|round|bevel"` are preserved in PowerPoint. Keep polygon/polyline strokes solid and marker-free when point-level freeform editing is required.

## Shapes and styles

Supported native style properties:

- `fill` and `fill-opacity`;
- `stroke`, `stroke-opacity`, and `stroke-width`;
- element/group `opacity`;
- `rx`/`ry` for rounded rectangles.

Use CSS hex colors or simple `rgb()`/`rgba()` values. Named colors are intentionally limited. Gradients expressed as `url(#...)` render correctly through SVG fallback but are not native fills.

Do not rely on PowerPoint theme effects. Author every visible fill and stroke explicitly. The compiler removes default theme shadows from native shapes.

## Images

Use local relative paths or embedded `data:image/...` URIs:

```svg
<image x="900" y="160" width="560" height="560"
       preserveAspectRatio="xMidYMid meet"
       href="assets/product.png"/>
```

- `meet` contains and centers the image without distortion.
- `slice` fills the frame using centered crop.
- Remote HTTP(S) images are forbidden.
- Relative paths resolve from the SVG file's directory.
- Prefer relative paths over absolute paths for portability.

## Fallback features

Fallback creates a PNG compatibility preview plus an Office SVG relationship for the affected element. It preserves appearance in modern PowerPoint but does not make the element's internal path points individually editable.

Fallback is an acceptable last resort for a complex icon, curve, or compound decoration. It is not a substitute for native text or simple shapes.

## Forbidden features

Do not use:

- `<script>` or event attributes such as `onclick`;
- `<foreignObject>` or browser HTML;
- animation elements or CSS animation;
- remote JavaScript, remote fonts, or HTTP(S) assets;
- iframe, audio, video, interactive controls;
- filters or masks in the MVP authoring subset;
- complex browser-only CSS.

The validator rejects unsafe or unsupported constructs rather than silently accepting them.

## Authoring checklist

- Root has explicit `1600×900` dimensions and matching `viewBox`.
- One SVG contains the complete slide in final z-order.
- All audience text remains `<text>`/`<tspan>`.
- Every visible `<text>` has a supported `data-role`, and repeated roles use the locked deck token.
- Important native editability uses text/rect/circle/ellipse/line/image.
- Group transforms are simple and intentional.
- Images are local/embedded and preserve aspect ratio.
- No element is unintentionally outside the canvas.
- No text is below the readability floor without a deliberate exception.
- The SVG validates, renders, and matches the shared design system.
