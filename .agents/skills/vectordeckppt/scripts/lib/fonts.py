from __future__ import annotations

import unicodedata

DEFAULT_FONT_FAMILY = "Microsoft YaHei"
GENERIC_FONT_MAP = {
    "sans-serif": "Arial",
    "serif": "Times New Roman",
    "monospace": "Consolas",
}


def font_candidates(value: str | None) -> list[str]:
    if not value:
        return [DEFAULT_FONT_FAMILY]
    candidates = [item.strip().strip("'\"") for item in value.split(",") if item.strip()]
    return candidates or [DEFAULT_FONT_FAMILY]


def primary_font(value: str | None) -> str:
    candidate = font_candidates(value)[0]
    return GENERIC_FONT_MAP.get(candidate.lower(), candidate)


def is_bold(value: str | None) -> bool:
    if not value:
        return False
    normalized = value.strip().lower()
    if normalized in {"bold", "bolder"}:
        return True
    try:
        return int(float(normalized)) >= 600
    except ValueError:
        return False


def estimate_text_width(text: str, font_size: float, *, bold: bool = False) -> float:
    """Estimate SVG text width in canvas units without platform font dependencies."""

    width_em = 0.0
    for character in text:
        if character == "\t":
            width_em += 2.4
        elif character.isspace():
            width_em += 0.34
        elif unicodedata.east_asian_width(character) in {"W", "F"}:
            width_em += 1.0
        elif character.isupper():
            width_em += 0.67
        elif character.isdigit():
            width_em += 0.58
        else:
            width_em += 0.54
    return width_em * font_size * (1.04 if bold else 1.0)


def baseline_to_top(baseline_y: float, font_size: float) -> float:
    """Approximate a PowerPoint text-box top from an SVG alphabetic baseline."""

    return baseline_y - font_size * 0.82


def line_box_height(font_size: float, line_height: float = 1.2) -> float:
    return font_size * line_height
