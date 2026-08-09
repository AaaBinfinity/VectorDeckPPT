from __future__ import annotations

import math
import re
from collections.abc import Iterator, Mapping
from pathlib import Path

from lxml import etree

from .svg_models import Matrix, RenderElement, SvgDocument

SVG_NAMESPACE = "http://www.w3.org/2000/svg"
XLINK_NAMESPACE = "http://www.w3.org/1999/xlink"

_LENGTH_RE = re.compile(
    r"^\s*([+-]?(?:\d+(?:\.\d*)?|\.\d+)(?:[eE][+-]?\d+)?)\s*([a-zA-Z%]*)\s*$"
)
_NUMBER_RE = re.compile(r"[+-]?(?:\d+(?:\.\d*)?|\.\d+)(?:[eE][+-]?\d+)?")
_TRANSFORM_RE = re.compile(r"([A-Za-z]+)\s*\(([^)]*)\)")

_UNIT_TO_PX = {
    "": 1.0,
    "px": 1.0,
    "pt": 96.0 / 72.0,
    "pc": 16.0,
    "in": 96.0,
    "cm": 96.0 / 2.54,
    "mm": 96.0 / 25.4,
}

STYLE_KEYS = {
    "fill",
    "fill-opacity",
    "stroke",
    "stroke-opacity",
    "stroke-width",
    "stroke-linecap",
    "stroke-linejoin",
    "font-family",
    "font-size",
    "font-weight",
    "font-style",
    "text-anchor",
    "dominant-baseline",
    "opacity",
    "display",
    "visibility",
}
INHERITED_STYLE_KEYS = STYLE_KEYS - {"opacity", "display"}


class SvgParseError(ValueError):
    """Raised when an SVG cannot be parsed safely or has malformed core values."""


def local_name(value: str) -> str:
    return value.rsplit("}", 1)[-1]


def parse_length(value: str | None, *, percentage_base: float | None = None) -> float | None:
    if value is None or not value.strip():
        return None
    match = _LENGTH_RE.match(value)
    if match is None:
        raise ValueError(f"Invalid SVG length: {value!r}")
    number = float(match.group(1))
    unit = match.group(2).lower()
    if unit == "%":
        if percentage_base is None:
            raise ValueError(f"Percentage length requires a base: {value!r}")
        return percentage_base * number / 100.0
    if unit not in _UNIT_TO_PX:
        raise ValueError(f"Unsupported SVG length unit: {unit!r}")
    return number * _UNIT_TO_PX[unit]


def parse_number(value: str | None, default: float = 0.0) -> float:
    if value is None or not value.strip():
        return default
    match = _NUMBER_RE.search(value)
    if match is None:
        raise ValueError(f"Invalid SVG number: {value!r}")
    return float(match.group(0))


def parse_view_box(value: str | None) -> tuple[float, float, float, float] | None:
    if value is None or not value.strip():
        return None
    numbers = [float(item) for item in _NUMBER_RE.findall(value)]
    if len(numbers) != 4:
        raise ValueError("viewBox must contain exactly four numbers")
    return numbers[0], numbers[1], numbers[2], numbers[3]


def parse_points(value: str | None) -> list[tuple[float, float]]:
    if value is None:
        return []
    numbers = [float(item) for item in _NUMBER_RE.findall(value)]
    if len(numbers) % 2:
        raise ValueError("points must contain an even number of coordinates")
    return list(zip(numbers[0::2], numbers[1::2], strict=True))


def parse_style_attribute(value: str | None) -> dict[str, str]:
    if not value:
        return {}
    declarations: dict[str, str] = {}
    for chunk in value.split(";"):
        if ":" not in chunk:
            continue
        key, raw_value = chunk.split(":", 1)
        key = key.strip().lower()
        if key:
            declarations[key] = raw_value.strip()
    return declarations


def element_styles(
    element: etree._Element,
    inherited: Mapping[str, str] | None = None,
) -> dict[str, str]:
    styles = dict(inherited or {})
    for key in STYLE_KEYS:
        if key in element.attrib:
            styles[key] = element.attrib[key].strip()
    styles.update(parse_style_attribute(element.get("style")))
    return styles


def get_href(element: etree._Element) -> str | None:
    return element.get("href") or element.get(f"{{{XLINK_NAMESPACE}}}href")


def parse_opacity(value: str | None, default: float = 1.0) -> float:
    if value is None or not value.strip():
        return default
    return max(0.0, min(1.0, float(value)))


def parse_transform(value: str | None) -> Matrix:
    if value is None or not value.strip():
        return Matrix()

    position = 0
    result = Matrix()
    for match in _TRANSFORM_RE.finditer(value):
        if value[position : match.start()].strip(" ,\t\r\n"):
            raise ValueError(f"Malformed transform list: {value!r}")
        name = match.group(1).lower()
        args = [float(item) for item in _NUMBER_RE.findall(match.group(2))]
        operation = _transform_operation(name, args)
        result = result.multiply(operation)
        position = match.end()
    if value[position:].strip(" ,\t\r\n"):
        raise ValueError(f"Malformed transform list: {value!r}")
    return result


def _transform_operation(name: str, args: list[float]) -> Matrix:
    if name == "matrix" and len(args) == 6:
        return Matrix(*args)
    if name == "translate" and len(args) in {1, 2}:
        return Matrix(e=args[0], f=args[1] if len(args) == 2 else 0.0)
    if name == "scale" and len(args) in {1, 2}:
        return Matrix(a=args[0], d=args[1] if len(args) == 2 else args[0])
    if name == "rotate" and len(args) in {1, 3}:
        angle = math.radians(args[0])
        rotation = Matrix(
            a=math.cos(angle),
            b=math.sin(angle),
            c=-math.sin(angle),
            d=math.cos(angle),
        )
        if len(args) == 1:
            return rotation
        cx, cy = args[1], args[2]
        return Matrix(e=cx, f=cy).multiply(rotation).multiply(Matrix(e=-cx, f=-cy))
    if name == "skewx" and len(args) == 1:
        return Matrix(c=math.tan(math.radians(args[0])))
    if name == "skewy" and len(args) == 1:
        return Matrix(b=math.tan(math.radians(args[0])))
    raise ValueError(f"Unsupported or malformed transform: {name}({', '.join(map(str, args))})")


def parse_svg(path: str | Path) -> SvgDocument:
    source = Path(path).expanduser().resolve()
    parser = etree.XMLParser(
        resolve_entities=False,
        no_network=True,
        recover=False,
        remove_comments=False,
        huge_tree=False,
    )
    try:
        tree = etree.parse(str(source), parser)
    except (OSError, etree.XMLSyntaxError) as exc:
        raise SvgParseError(str(exc)) from exc

    root = tree.getroot()
    try:
        width = parse_length(root.get("width"))
        height = parse_length(root.get("height"))
        view_box = parse_view_box(root.get("viewBox"))
    except ValueError as exc:
        raise SvgParseError(str(exc)) from exc
    return SvgDocument(
        source=source,
        tree=tree,
        root=root,
        width=width,
        height=height,
        view_box=view_box,
    )


def iter_render_elements(document: SvgDocument) -> Iterator[RenderElement]:
    root_styles = element_styles(document.root)
    root_opacity = parse_opacity(root_styles.get("opacity"))
    root_transform = parse_transform(document.root.get("transform"))
    yield from _walk_render_elements(
        document,
        document.root,
        root_styles,
        root_transform,
        root_opacity,
        is_root=True,
    )


def _walk_render_elements(
    document: SvgDocument,
    element: etree._Element,
    inherited_styles: Mapping[str, str],
    parent_transform: Matrix,
    parent_opacity: float,
    *,
    is_root: bool = False,
) -> Iterator[RenderElement]:
    tag = local_name(element.tag) if isinstance(element.tag, str) else ""
    if tag in {"defs", "title", "desc", "metadata"}:
        return

    if is_root:
        styles = dict(inherited_styles)
        transform = parent_transform
        opacity = parent_opacity
    else:
        inherited = {
            key: value for key, value in inherited_styles.items() if key in INHERITED_STYLE_KEYS
        }
        styles = element_styles(element, inherited)
        transform = parent_transform.multiply(parse_transform(element.get("transform")))
        opacity = parent_opacity * parse_opacity(styles.get("opacity"))

    if styles.get("display", "").lower() == "none" or styles.get("visibility", "").lower() in {
        "hidden",
        "collapse",
    }:
        return

    if not is_root and tag not in {"g", "tspan"}:
        yield RenderElement(
            element=element,
            tag=tag,
            styles=styles,
            transform=transform,
            opacity=opacity,
            xpath=document.tree.getpath(element),
        )

    if tag == "text":
        return
    for child in element:
        if isinstance(child.tag, str):
            yield from _walk_render_elements(
                document,
                child,
                styles,
                transform,
                opacity,
            )
