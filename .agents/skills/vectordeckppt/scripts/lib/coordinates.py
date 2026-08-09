from __future__ import annotations

from dataclasses import dataclass

EMU_PER_INCH = 914_400
POINTS_PER_INCH = 72.0
CSS_PIXELS_PER_INCH = 96.0
DEFAULT_CANVAS_WIDTH = 1600.0
DEFAULT_CANVAS_HEIGHT = 900.0
DEFAULT_SLIDE_WIDTH_INCHES = 40.0 / 3.0
DEFAULT_SLIDE_HEIGHT_INCHES = 7.5


def inches_to_emu(value: float) -> int:
    return round(value * EMU_PER_INCH)


def emu_to_inches(value: int) -> float:
    return value / EMU_PER_INCH


def css_px_to_points(value: float) -> float:
    return value * POINTS_PER_INCH / CSS_PIXELS_PER_INCH


@dataclass(frozen=True, slots=True)
class CoordinateMapper:
    canvas_width: float = DEFAULT_CANVAS_WIDTH
    canvas_height: float = DEFAULT_CANVAS_HEIGHT
    view_x: float = 0.0
    view_y: float = 0.0
    slide_width_inches: float = DEFAULT_SLIDE_WIDTH_INCHES
    slide_height_inches: float = DEFAULT_SLIDE_HEIGHT_INCHES

    def __post_init__(self) -> None:
        if self.canvas_width <= 0 or self.canvas_height <= 0:
            raise ValueError("Canvas dimensions must be positive")
        if self.slide_width_inches <= 0 or self.slide_height_inches <= 0:
            raise ValueError("Slide dimensions must be positive")

    @property
    def x_inches_per_unit(self) -> float:
        return self.slide_width_inches / self.canvas_width

    @property
    def y_inches_per_unit(self) -> float:
        return self.slide_height_inches / self.canvas_height

    def x_inches(self, value: float) -> float:
        return (value - self.view_x) * self.x_inches_per_unit

    def y_inches(self, value: float) -> float:
        return (value - self.view_y) * self.y_inches_per_unit

    def width_inches(self, value: float) -> float:
        return value * self.x_inches_per_unit

    def height_inches(self, value: float) -> float:
        return value * self.y_inches_per_unit

    def x(self, value: float) -> int:
        return inches_to_emu(self.x_inches(value))

    def y(self, value: float) -> int:
        return inches_to_emu(self.y_inches(value))

    def width(self, value: float) -> int:
        return inches_to_emu(self.width_inches(value))

    def height(self, value: float) -> int:
        return inches_to_emu(self.height_inches(value))

    def point(self, x: float, y: float) -> tuple[int, int]:
        return self.x(x), self.y(y)

    def rect(self, x: float, y: float, width: float, height: float) -> tuple[int, int, int, int]:
        return self.x(x), self.y(y), self.width(width), self.height(height)
