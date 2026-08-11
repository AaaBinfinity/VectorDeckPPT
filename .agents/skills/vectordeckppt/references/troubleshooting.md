# Troubleshooting

## Contents

1. SVG validation
2. Rendering
3. Fonts and text
4. Images
5. Compilation and editability
6. PPTX validation
7. Environment and commands

## SVG validation

### XML parse error

Check unescaped `&`, mismatched tags, invalid quotes, duplicate attributes, and truncated markup. Keep UTF-8 encoding. Do not enable parser recovery; repair the source.

### Missing viewBox or dimensions

Add `width`, `height`, and `viewBox`. For default slides use `1600`, `900`, and `0 0 1600 900`.

### Forbidden element

Replace scripts, `foreignObject`, animation, filters, masks, or browser-only content with supported SVG shapes/text/images. Do not suppress the validator.

### Remote resource

Save an authorized local copy in the deck workspace and use a relative path. Remote fonts and remote images make deterministic rendering and packaging unreliable.

### Overflow warning

Render and inspect. Fix an unintended overflow at the source. A deliberate full-bleed background may touch the canvas edge but should not extend by arbitrary large values.

## Rendering

### Renderer import or native-library failure

Run `uv sync` and confirm `resvg-py` is installed from a wheel compatible with the active Python/platform. The current renderer does not require a system Cairo installation.

### Missing characters

Install or select a font covering the characters and provide the documented fallback stack. `resvg` loads system fonts by default. Verify the actual preview.

### Different output size

Use the default `1600×900` output or pass both `--width` and `--height`. Keep the target aspect ratio consistent with the SVG viewBox.

## Fonts and text

### PPT text is vertically shifted

SVG positions text by baseline while PowerPoint positions a textbox by its top. Adjust the SVG `y` or the compiler's centralized `baseline_to_top` strategy only with regression tests. Do not add per-slide magic offsets in the compiler.

### Title wraps only in PowerPoint

Shorten the title, widen its logical SVG composition, or choose a more stable font. The compiler estimates width and cannot guarantee identical metrics on every system.

### Chinese font substitution

Use `Microsoft YaHei, PingFang SC, Noto Sans CJK SC, sans-serif` and render the PPTX on the target platform. Keep text editable unless exact glyph shape is more important and fallback is explicitly accepted.

### Artistic display font is missing or changes shape

Confirm the named display font is installed and that its fallback stack was approved during art direction. Restrict it to short `deck-title`, `section-title`, or featured `quote` roles; do not apply it to ordinary slide titles, charts, labels, or body copy. Re-render both the SVG and compiled PPTX on the delivery environment. If exact licensed glyph artwork is essential, use a local authorized vector/image treatment for that one display role and report the resulting editability reduction.

### Tspan line is misplaced

Use explicit `x` and either `y` or `dy`. Avoid complex nested tspans, baseline-shift, browser wrapping, or percentage font sizes.

### Typography audit fails

Run the strict deck audit and read its JSON diagnostics before compiling:

```bash
python "<SKILL_ROOT>/scripts/audit_typography.py" "<DECK_ROOT>/slides/" --strict --json
```

- `missing_text_role`: add a supported semantic `data-role` to every visible `<text>` element. Use the role that matches meaning, not the nearest-looking size.
- `inconsistent_peer_size`: elements with the same role on one slide use different sizes. Apply the same exact role token to all peers.
- `inconsistent_deck_size`: a recurring deck role, especially `slide-title`, differs between slides. Restore the shared deck token.
- `inconsistent_deck_title_family` or `inconsistent_deck_title_weight`: ordinary slide titles use different font families or weights. Restore the shared title family and weight.

Do not fix these failures by shrinking only the overflowing text box. Shorten the copy, introduce an intentional line break, widen the composition, or change the layout while keeping the locked role token.

## Images

### Image file not found

Resolve paths relative to the SVG file, not the current terminal directory. Prefer `assets/name.png` next to the slide workspace.

### Image looks stretched

Use `preserveAspectRatio="xMidYMid meet"` for contain or `xMidYMid slice` for cover. The compiler intentionally ignores stretch-to-fill behavior.

### Embedded data URI fails

Confirm the URI starts with `data:image/<type>;base64,` and contains valid base64 payload. Large assets are easier to maintain as local files.

## Compilation and editability

### Element enters embedded SVG fallback

Check the report warning. Common causes are complex paths, gradients, clip paths, rotation, skew, or polygons/polylines that use markers or dashed strokes. Plain straight-segment polygons and polylines compile as editable PowerPoint freeforms. Simplify other elements into text, basic shapes, lines, images, or plain freeforms when individual editing matters.

### Fallback fails

Validate the isolated feature in the original SVG, remove unsupported dependencies, and confirm referenced assets are local. A fallback failure increments `failed` and prevents deck output.

### Shape has an unexpected shadow

Recompile with the current compiler. It removes PowerPoint's default theme style from native shapes. Do not compensate by adding opaque background shapes.

### Wrong slide order

Use zero-padded filenames (`slide_01.svg`) or clear numeric names. The compiler uses natural filename ordering and excludes non-SVG files.

## PPTX validation

### Broken relationship

Inspect the named `.rels` part and target. Every internal relationship must resolve to a package member. For SVG fallback, both PNG preview and SVG media parts must be present.

### Deck opens in python-pptx but not PowerPoint

Run ZIP integrity and relationship validation, then render in a real Office-compatible engine. Inspect `[Content_Types].xml`, slide relationships, and media content types.

### Slide count mismatch

Remove stale slide SVG versions from the input directory and recompile. Compare `ppt/presentation.xml`, `ppt/slides/`, and the compiler report.

## Environment and commands

### `uv` selects the wrong Python

Use a project-local `.venv`, run `uv sync`, or pass an explicit compatible interpreter. The project requires Python 3.12+.

### Tests cannot use the system temp directory

Pass a writable project-local base temp, for example:

```bash
uv run pytest --basetemp output/pytest-temp
```

This is an environment workaround, not a product behavior change.
