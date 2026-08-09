from __future__ import annotations

import base64
from io import BytesIO
from pathlib import Path
from urllib.parse import unquote, urlparse

from PIL import Image

from .coordinates import CoordinateMapper
from .pptx_shapes import NativeShapeUnsupported
from .svg_models import RenderElement, SvgDocument
from .svg_parser import get_href, parse_length


def add_native_image(
    slide: object,
    item: RenderElement,
    document: SvgDocument,
    mapper: CoordinateMapper,
) -> object:
    if not item.transform.is_axis_aligned:
        raise NativeShapeUnsupported("rotated or skewed image")
    href = get_href(item.element)
    if not href:
        raise NativeShapeUnsupported("image has no href")
    data = _load_image(document, href)
    with Image.open(BytesIO(data)) as image:
        image_width, image_height = image.size
    if image_width <= 0 or image_height <= 0:
        raise NativeShapeUnsupported("image has invalid dimensions")

    x = _length(item, document, "x", 0.0)
    y = _length(item, document, "y", 0.0, horizontal=False)
    width = _length(item, document, "width", None)
    height = _length(item, document, "height", None, horizontal=False)
    start_x, start_y = item.transform.apply(x, y)
    end_x, end_y = item.transform.apply(x + width, y + height)
    left, top = min(start_x, end_x), min(start_y, end_y)
    box_width, box_height = abs(end_x - start_x), abs(end_y - start_y)
    if box_width <= 0 or box_height <= 0:
        raise NativeShapeUnsupported("zero-size image")

    preserve = item.element.get("preserveAspectRatio", "xMidYMid meet").strip().lower()
    if "slice" in preserve:
        picture = slide.shapes.add_picture(
            BytesIO(data),
            mapper.x(left),
            mapper.y(top),
            mapper.width(box_width),
            mapper.height(box_height),
        )
        _apply_cover_crop(picture, image_width / image_height, box_width / box_height)
    else:
        image_ratio = image_width / image_height
        box_ratio = box_width / box_height
        if image_ratio > box_ratio:
            draw_width = box_width
            draw_height = box_width / image_ratio
            draw_left = left
            draw_top = top + (box_height - draw_height) / 2
        else:
            draw_height = box_height
            draw_width = box_height * image_ratio
            draw_top = top
            draw_left = left + (box_width - draw_width) / 2
        picture = slide.shapes.add_picture(
            BytesIO(data),
            mapper.x(draw_left),
            mapper.y(draw_top),
            mapper.width(draw_width),
            mapper.height(draw_height),
        )
    picture.name = item.element.get("id") or "SVG image"
    return picture


def _load_image(document: SvgDocument, href: str) -> bytes:
    if href.startswith("data:image/"):
        try:
            header, payload = href.split(",", 1)
            return base64.b64decode(payload) if ";base64" in header else unquote(payload).encode()
        except (ValueError, base64.binascii.Error) as exc:
            raise NativeShapeUnsupported(f"invalid embedded image: {exc}") from exc

    parsed = urlparse(href)
    if parsed.scheme and not Path(href).is_absolute():
        raise NativeShapeUnsupported(f"unsupported image URI: {href}")
    image_path = Path(unquote(href.split("#", 1)[0]))
    if not image_path.is_absolute():
        image_path = document.source.parent / image_path
    try:
        return image_path.read_bytes()
    except OSError as exc:
        raise NativeShapeUnsupported(f"cannot read image {image_path}: {exc}") from exc


def _length(
    item: RenderElement,
    document: SvgDocument,
    name: str,
    default: float | None,
    *,
    horizontal: bool = True,
) -> float:
    base = document.canvas_width if horizontal else document.canvas_height
    value = parse_length(item.element.get(name), percentage_base=base)
    if value is None:
        if default is None:
            raise NativeShapeUnsupported(f"image requires {name}")
        return default
    return value


def _apply_cover_crop(picture: object, image_ratio: float, box_ratio: float) -> None:
    if image_ratio > box_ratio:
        total_crop = 1.0 - box_ratio / image_ratio
        picture.crop_left = total_crop / 2
        picture.crop_right = total_crop / 2
    elif image_ratio < box_ratio:
        total_crop = 1.0 - image_ratio / box_ratio
        picture.crop_top = total_crop / 2
        picture.crop_bottom = total_crop / 2
