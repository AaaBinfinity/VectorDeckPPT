from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

from lxml import etree


@dataclass(frozen=True, slots=True)
class Matrix:
    """SVG affine matrix using the standard ``a b c d e f`` representation."""

    a: float = 1.0
    b: float = 0.0
    c: float = 0.0
    d: float = 1.0
    e: float = 0.0
    f: float = 0.0

    def multiply(self, other: Matrix) -> Matrix:
        """Return ``self * other`` for column-vector SVG coordinates."""

        return Matrix(
            a=self.a * other.a + self.c * other.b,
            b=self.b * other.a + self.d * other.b,
            c=self.a * other.c + self.c * other.d,
            d=self.b * other.c + self.d * other.d,
            e=self.a * other.e + self.c * other.f + self.e,
            f=self.b * other.e + self.d * other.f + self.f,
        )

    def apply(self, x: float, y: float) -> tuple[float, float]:
        return (
            self.a * x + self.c * y + self.e,
            self.b * x + self.d * y + self.f,
        )

    @property
    def is_axis_aligned(self) -> bool:
        return abs(self.b) < 1e-9 and abs(self.c) < 1e-9

    def to_svg(self) -> str:
        values = (self.a, self.b, self.c, self.d, self.e, self.f)
        return "matrix(" + " ".join(f"{value:.8g}" for value in values) + ")"


@dataclass(frozen=True, slots=True)
class Diagnostic:
    code: str
    message: str
    element: str | None = None
    line: int | None = None
    attribute: str | None = None

    def to_dict(self) -> dict[str, Any]:
        result: dict[str, Any] = {"code": self.code, "message": self.message}
        if self.element is not None:
            result["element"] = self.element
        if self.line is not None:
            result["line"] = self.line
        if self.attribute is not None:
            result["attribute"] = self.attribute
        return result


@dataclass(slots=True)
class ValidationResult:
    source: Path
    errors: list[Diagnostic] = field(default_factory=list)
    warnings: list[Diagnostic] = field(default_factory=list)
    canvas: dict[str, Any] | None = None

    @property
    def valid(self) -> bool:
        return not self.errors

    def add_error(self, code: str, message: str, **context: Any) -> None:
        self.errors.append(Diagnostic(code=code, message=message, **context))

    def add_warning(self, code: str, message: str, **context: Any) -> None:
        self.warnings.append(Diagnostic(code=code, message=message, **context))

    def to_dict(self) -> dict[str, Any]:
        result: dict[str, Any] = {
            "valid": self.valid,
            "source": str(self.source),
            "errors": [item.to_dict() for item in self.errors],
            "warnings": [item.to_dict() for item in self.warnings],
        }
        if self.canvas is not None:
            result["canvas"] = self.canvas
        return result


@dataclass(frozen=True, slots=True)
class RenderElement:
    element: etree._Element
    tag: str
    styles: dict[str, str]
    transform: Matrix
    opacity: float
    xpath: str


@dataclass(slots=True)
class SvgDocument:
    source: Path
    tree: etree._ElementTree
    root: etree._Element
    width: float | None
    height: float | None
    view_box: tuple[float, float, float, float] | None

    @property
    def canvas_width(self) -> float:
        if self.view_box is not None:
            return self.view_box[2]
        if self.width is not None:
            return self.width
        raise ValueError("SVG has no usable canvas width")

    @property
    def canvas_height(self) -> float:
        if self.view_box is not None:
            return self.view_box[3]
        if self.height is not None:
            return self.height
        raise ValueError("SVG has no usable canvas height")
