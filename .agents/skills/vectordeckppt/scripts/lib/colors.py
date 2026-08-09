from __future__ import annotations

import re
from dataclasses import dataclass

_RGB_RE = re.compile(r"rgba?\(\s*([^)]+)\s*\)", re.IGNORECASE)
_NAMED_COLORS = {
    "black": "#000000",
    "white": "#FFFFFF",
    "red": "#FF0000",
    "green": "#008000",
    "blue": "#0000FF",
    "gray": "#808080",
    "grey": "#808080",
    "yellow": "#FFFF00",
    "orange": "#FFA500",
    "purple": "#800080",
    "transparent": "#00000000",
}


@dataclass(frozen=True, slots=True)
class SvgColor:
    red: int
    green: int
    blue: int
    alpha: float = 1.0

    def __post_init__(self) -> None:
        if not all(0 <= channel <= 255 for channel in (self.red, self.green, self.blue)):
            raise ValueError("RGB channels must be between 0 and 255")
        if not 0.0 <= self.alpha <= 1.0:
            raise ValueError("Alpha must be between 0 and 1")

    @property
    def rgb(self) -> tuple[int, int, int]:
        return self.red, self.green, self.blue

    @property
    def hex(self) -> str:
        return f"{self.red:02X}{self.green:02X}{self.blue:02X}"

    def with_opacity(self, opacity: float) -> SvgColor:
        return SvgColor(self.red, self.green, self.blue, self.alpha * max(0.0, min(1.0, opacity)))


def parse_color(value: str | None, *, opacity: float = 1.0) -> SvgColor | None:
    if value is None:
        return None
    normalized = value.strip().lower()
    if not normalized or normalized == "none":
        return None
    normalized = _NAMED_COLORS.get(normalized, normalized)
    if normalized.startswith("url("):
        raise ValueError("Paint servers such as gradients are not native-color values")

    if normalized.startswith("#"):
        color = _parse_hex(normalized)
    else:
        match = _RGB_RE.fullmatch(normalized)
        if match is None:
            raise ValueError(f"Unsupported color value: {value!r}")
        color = _parse_rgb_function(match.group(1))
    return color.with_opacity(opacity)


def _parse_hex(value: str) -> SvgColor:
    digits = value[1:]
    if len(digits) in {3, 4}:
        digits = "".join(character * 2 for character in digits)
    if len(digits) not in {6, 8} or not re.fullmatch(r"[0-9a-fA-F]+", digits):
        raise ValueError(f"Invalid hex color: {value!r}")
    red, green, blue = int(digits[0:2], 16), int(digits[2:4], 16), int(digits[4:6], 16)
    alpha = int(digits[6:8], 16) / 255.0 if len(digits) == 8 else 1.0
    return SvgColor(red, green, blue, alpha)


def _parse_rgb_function(body: str) -> SvgColor:
    parts = [part.strip() for part in body.split(",")]
    if len(parts) not in {3, 4}:
        raise ValueError("rgb()/rgba() requires three or four channels")

    def channel(raw: str) -> int:
        if raw.endswith("%"):
            return round(float(raw[:-1]) * 2.55)
        return round(float(raw))

    red, green, blue = (max(0, min(255, channel(part))) for part in parts[:3])
    alpha = 1.0
    if len(parts) == 4:
        alpha = float(parts[3][:-1]) / 100.0 if parts[3].endswith("%") else float(parts[3])
    return SvgColor(red, green, blue, max(0.0, min(1.0, alpha)))
