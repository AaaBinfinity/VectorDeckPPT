from __future__ import annotations

from pathlib import Path

import resvg_py
from PIL import Image

from .path_safety import PathSafetyError, ensure_distinct_paths, require_suffix
from .svg_validator import validate_svg


class SvgRenderError(RuntimeError):
    """Raised when a slide cannot be rendered safely."""


def render_svg(
    source: str | Path,
    output: str | Path | None = None,
    *,
    width: int = 1600,
    height: int = 900,
) -> Path:
    source_path = Path(source).expanduser().resolve()
    output_candidate = output if output is not None else source_path.with_suffix(".png")
    try:
        output_path = require_suffix(output_candidate, ".png", label="PNG output")
        ensure_distinct_paths({"SVG input": source_path, "PNG output": output_path})
    except PathSafetyError as exc:
        raise SvgRenderError(str(exc)) from exc

    result = validate_svg(source_path)
    if not result.valid:
        details = "; ".join(f"{item.code}: {item.message}" for item in result.errors)
        raise SvgRenderError(f"SVG validation failed: {details}")
    if width <= 0 or height <= 0:
        raise SvgRenderError("Render width and height must be positive")

    output_path.parent.mkdir(parents=True, exist_ok=True)
    try:
        png_data = resvg_py.svg_to_bytes(
            svg_path=str(source_path),
            width=width,
            height=height,
            resources_dir=str(source_path.parent),
            shape_rendering="geometric_precision",
            text_rendering="optimize_legibility",
            image_rendering="optimize_quality",
        )
        output_path.write_bytes(png_data)
        with Image.open(output_path) as preview:
            preview.verify()
        with Image.open(output_path) as preview:
            if preview.size != (width, height):
                raise SvgRenderError(
                    f"Renderer returned {preview.size[0]}x{preview.size[1]}, "
                    f"expected {width}x{height}"
                )
    except SvgRenderError:
        raise
    except Exception as exc:
        raise SvgRenderError(f"Failed to render {source_path}: {exc}") from exc
    return output_path


def render_directory(
    source_dir: str | Path,
    output_dir: str | Path,
    *,
    width: int = 1600,
    height: int = 900,
) -> list[Path]:
    source_path = Path(source_dir).expanduser().resolve()
    output_path = Path(output_dir).expanduser().resolve()
    slides = sorted(source_path.glob("*.svg"), key=lambda item: item.name.casefold())
    if not slides:
        raise SvgRenderError(f"No SVG files found in directory: {source_path}")
    return [
        render_svg(slide, output_path / f"{slide.stem}.png", width=width, height=height)
        for slide in slides
    ]
