from __future__ import annotations

import re
from pathlib import Path
from urllib.parse import unquote, urlparse

from lxml import etree

from .svg_models import Matrix, SvgDocument, ValidationResult
from .svg_parser import (
    get_href,
    local_name,
    parse_length,
    parse_number,
    parse_points,
    parse_svg,
    parse_transform,
)

ALLOWED_TAGS = {
    "svg",
    "g",
    "text",
    "tspan",
    "rect",
    "circle",
    "ellipse",
    "line",
    "polyline",
    "polygon",
    "path",
    "image",
    "defs",
    "linearGradient",
    "radialGradient",
    "stop",
    "clipPath",
    "marker",
    "title",
    "desc",
    "metadata",
}
FORBIDDEN_TAGS = {
    "script",
    "foreignObject",
    "animate",
    "animateMotion",
    "animateTransform",
    "set",
    "iframe",
    "audio",
    "video",
    "filter",
    "mask",
}
FALLBACK_TAGS = {"path"}
DEFINITION_TAGS = {"defs", "linearGradient", "radialGradient", "stop", "clipPath", "marker"}
REMOTE_RE = re.compile(r"(?:https?:)?//", re.IGNORECASE)


def validate_svg(path: str | Path) -> ValidationResult:
    source = Path(path).expanduser().resolve()
    result = ValidationResult(source=source)
    if not source.is_file():
        result.add_error("file_not_found", f"SVG file does not exist: {source}")
        return result

    try:
        raw = source.read_text(encoding="utf-8")
    except UnicodeDecodeError:
        raw = source.read_text(encoding="utf-8-sig")
    except OSError as exc:
        result.add_error("file_read_error", str(exc))
        return result

    if "<!DOCTYPE" in raw.upper() or "<!ENTITY" in raw.upper():
        result.add_error(
            "doctype_forbidden",
            "DOCTYPE and custom entities are forbidden in slide SVGs",
        )

    try:
        document = parse_svg(source)
    except ValueError as exc:
        result.add_error("xml_parse_error", str(exc))
        return result

    _validate_canvas(document, result)
    _validate_elements(document, result)
    return result


def _validate_canvas(document: SvgDocument, result: ValidationResult) -> None:
    root_tag = local_name(document.root.tag) if isinstance(document.root.tag, str) else ""
    if root_tag != "svg":
        result.add_error("invalid_root", "Root element must be <svg>", element=root_tag)
        return

    if document.view_box is None:
        result.add_error("missing_viewbox", "Root <svg> must define viewBox")
    else:
        x, y, width, height = document.view_box
        result.canvas = {
            "width": document.width,
            "height": document.height,
            "viewBox": [x, y, width, height],
        }
        if width <= 0 or height <= 0:
            result.add_error("invalid_viewbox", "viewBox width and height must be positive")
        if (x, y) != (0.0, 0.0):
            result.add_warning(
                "nonzero_viewbox_origin",
                "A non-zero viewBox origin may shift PowerPoint coordinates",
            )
        if abs(width - 1600) > 0.01 or abs(height - 900) > 0.01:
            result.add_warning(
                "nonstandard_canvas",
                "Default slide canvas is 1600x900; confirm the requested aspect ratio",
            )

    if document.width is None or document.height is None:
        result.add_error("missing_dimensions", "Root <svg> must define width and height")
    elif document.width <= 0 or document.height <= 0:
        result.add_error("invalid_dimensions", "SVG width and height must be positive")
    elif document.view_box is not None:
        _, _, view_width, view_height = document.view_box
        if abs(document.width - view_width) > 0.01 or abs(document.height - view_height) > 0.01:
            result.add_warning(
                "dimension_viewbox_mismatch",
                "width/height differ from viewBox dimensions; verify scaling intentionally",
            )


def _validate_elements(document: SvgDocument, result: ValidationResult) -> None:
    ids: set[str] = set()
    world_transforms = _world_transforms(document)
    for element in document.root.iter():
        if not isinstance(element.tag, str):
            continue
        tag = local_name(element.tag)
        line = element.sourceline
        context = {"element": tag, "line": line}

        if tag in FORBIDDEN_TAGS:
            result.add_error(
                "forbidden_element",
                f"<{tag}> is forbidden in slide SVGs",
                **context,
            )
        elif tag not in ALLOWED_TAGS:
            result.add_error(
                "unsupported_element",
                f"<{tag}> is outside the supported SVG subset",
                **context,
            )
        elif tag in FALLBACK_TAGS:
            result.add_warning(
                "embedded_svg_fallback",
                f"<{tag}> may compile as an embedded SVG asset instead of a native shape",
                **context,
            )

        element_id = element.get("id")
        if element_id:
            if element_id in ids:
                result.add_error(
                    "duplicate_id",
                    f"Duplicate SVG id: {element_id}",
                    **context,
                )
            ids.add(element_id)

        for attribute, value in element.attrib.items():
            attribute_name = local_name(attribute)
            if attribute_name.lower().startswith("on"):
                result.add_error(
                    "event_handler_forbidden",
                    f"Event handler attribute {attribute_name!r} is forbidden",
                    attribute=attribute_name,
                    **context,
                )
            if REMOTE_RE.search(value):
                result.add_error(
                    "remote_resource",
                    f"Remote resource is forbidden in {attribute_name}: {value}",
                    attribute=attribute_name,
                    **context,
                )

        try:
            transform = parse_transform(element.get("transform"))
        except ValueError as exc:
            result.add_error("invalid_transform", str(exc), attribute="transform", **context)
            transform = Matrix()

        world_transform = world_transforms.get(document.tree.getpath(element), transform)
        if not world_transform.is_axis_aligned:
            result.add_warning(
                "complex_transform",
                "Rotation or skew may require embedded SVG fallback during compilation",
                attribute="transform",
                **context,
            )

        if tag == "image":
            _validate_image(document, element, result)
        if tag in {"rect", "image", "circle", "ellipse", "line", "text", "polyline", "polygon"}:
            _validate_geometry(document, element, world_transform, result)
        if tag == "path" and not element.get("d", "").strip():
            result.add_error("missing_path_data", "<path> must define non-empty d data", **context)


def _validate_image(
    document: SvgDocument,
    element: etree._Element,
    result: ValidationResult,
) -> None:
    href = get_href(element)
    context = {"element": "image", "line": element.sourceline, "attribute": "href"}
    if not href:
        result.add_error("missing_image_href", "<image> must define href", **context)
        return
    if href.startswith("data:image/"):
        return
    raw_path = Path(unquote(href.split("#", 1)[0]))
    parsed = urlparse(href)
    if raw_path.is_absolute():
        image_path = raw_path
    elif parsed.scheme:
        if parsed.scheme.lower() == "file":
            image_path = Path(unquote(parsed.path.lstrip("/")))
        else:
            result.add_error("unsupported_image_uri", f"Unsupported image URI: {href}", **context)
            return
    else:
        image_path = raw_path
        if not image_path.is_absolute():
            image_path = document.source.parent / image_path
    if not image_path.is_file():
        result.add_error(
            "missing_image_file",
            f"Referenced image does not exist: {image_path.resolve()}",
            **context,
        )
    elif Path(href).is_absolute():
        result.add_warning(
            "absolute_image_path",
            "Absolute image paths reduce deck portability; prefer a relative path",
            **context,
        )


def _validate_geometry(
    document: SvgDocument,
    element: etree._Element,
    transform: Matrix,
    result: ValidationResult,
) -> None:
    if document.view_box is None:
        return
    tag = local_name(element.tag)
    line = element.sourceline
    context = {"element": tag, "line": line}
    try:
        box = _element_box(element, document)
    except ValueError as exc:
        result.add_error("invalid_geometry", str(exc), **context)
        return
    if box is None:
        return
    raw_left, raw_top, raw_right, raw_bottom = box
    if raw_right < raw_left or raw_bottom < raw_top:
        result.add_error("negative_size", f"<{tag}> has a negative width or height", **context)
        return
    transformed_points = [
        transform.apply(raw_left, raw_top),
        transform.apply(raw_right, raw_top),
        transform.apply(raw_left, raw_bottom),
        transform.apply(raw_right, raw_bottom),
    ]
    xs, ys = zip(*transformed_points, strict=True)
    left, top, right, bottom = min(xs), min(ys), max(xs), max(ys)
    width = right - left
    height = bottom - top

    view_x, view_y, view_width, view_height = document.view_box
    view_right = view_x + view_width
    view_bottom = view_y + view_height
    if right < view_x or bottom < view_y or left > view_right or top > view_bottom:
        result.add_warning(
            "element_outside_canvas",
            f"<{tag}> is completely outside the viewBox",
            **context,
        )
    elif left < view_x or top < view_y or right > view_right or bottom > view_bottom:
        result.add_warning(
            "element_overflow",
            f"<{tag}> extends beyond the viewBox",
            **context,
        )
    if width > view_width * 4 or height > view_height * 4:
        result.add_warning(
            "abnormal_size",
            f"<{tag}> is more than four times the canvas size",
            **context,
        )
    if tag == "text":
        font_size = parse_length(element.get("font-size")) or 16.0
        style = element.get("style", "")
        match = re.search(r"(?:^|;)\s*font-size\s*:\s*([^;]+)", style)
        if match:
            font_size = parse_length(match.group(1)) or font_size
        if font_size < 12:
            result.add_warning(
                "small_text",
                f"Text size {font_size:g}px may be unreadable in presentation mode",
                attribute="font-size",
                **context,
            )


def _element_box(
    element: etree._Element,
    document: SvgDocument,
) -> tuple[float, float, float, float] | None:
    tag = local_name(element.tag)
    canvas_width = document.view_box[2] if document.view_box else document.width
    canvas_height = document.view_box[3] if document.view_box else document.height

    def length(name: str, default: float = 0.0, *, horizontal: bool = True) -> float:
        base = canvas_width if horizontal else canvas_height
        return parse_length(element.get(name), percentage_base=base) or default

    if tag in {"rect", "image"}:
        x, y = length("x"), length("y", horizontal=False)
        width, height = length("width"), length("height", horizontal=False)
        return x, y, x + width, y + height
    if tag == "circle":
        cx, cy, radius = length("cx"), length("cy", horizontal=False), length("r")
        return cx - radius, cy - radius, cx + radius, cy + radius
    if tag == "ellipse":
        cx, cy = length("cx"), length("cy", horizontal=False)
        rx, ry = length("rx"), length("ry", horizontal=False)
        return cx - rx, cy - ry, cx + rx, cy + ry
    if tag == "line":
        x1, y1 = length("x1"), length("y1", horizontal=False)
        x2, y2 = length("x2"), length("y2", horizontal=False)
        return min(x1, x2), min(y1, y2), max(x1, x2), max(y1, y2)
    if tag in {"polyline", "polygon"}:
        points = parse_points(element.get("points"))
        minimum_points = 3 if tag == "polygon" else 2
        if len(points) < minimum_points:
            raise ValueError(f"<{tag}> must define at least {minimum_points} coordinate pairs")
        xs, ys = zip(*points, strict=True)
        return min(xs), min(ys), max(xs), max(ys)
    if tag == "text":
        x, y = parse_number(element.get("x")), parse_number(element.get("y"))
        font_size = parse_length(element.get("font-size")) or 16.0
        text = "".join(element.itertext()).strip()
        estimated_width = sum(0.58 if ord(char) < 128 else 1.0 for char in text) * font_size
        anchor = element.get("text-anchor", "start")
        left = x - estimated_width / 2 if anchor == "middle" else x
        if anchor == "end":
            left = x - estimated_width
        return left, y - font_size, left + estimated_width, y + font_size * 0.25
    return None


def _world_transforms(document: SvgDocument) -> dict[str, Matrix]:
    transforms: dict[str, Matrix] = {}

    def walk(element: etree._Element, parent: Matrix) -> None:
        try:
            local = parse_transform(element.get("transform"))
        except ValueError:
            local = Matrix()
        current = parent.multiply(local)
        transforms[document.tree.getpath(element)] = current
        for child in element:
            if isinstance(child.tag, str):
                walk(child, current)

    walk(document.root, Matrix())
    return transforms
