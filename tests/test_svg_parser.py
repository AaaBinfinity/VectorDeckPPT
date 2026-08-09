from pathlib import Path

import pytest
from lib.svg_parser import iter_render_elements, parse_length, parse_svg, parse_transform

FIXTURES = Path(__file__).parent / "fixtures"


def test_parse_svg_canvas_and_elements() -> None:
    document = parse_svg(FIXTURES / "simple_text.svg")
    elements = list(iter_render_elements(document))

    assert document.width == 1600
    assert document.height == 900
    assert document.view_box == (0.0, 0.0, 1600.0, 900.0)
    assert [element.tag for element in elements] == ["rect", "text", "text"]
    assert "可编辑标题" in "".join(elements[1].element.itertext())


def test_group_transform_and_opacity_are_accumulated() -> None:
    document = parse_svg(FIXTURES / "simple_line.svg")
    [line] = list(iter_render_elements(document))

    assert line.styles["stroke"] == "#2563EB"
    assert line.opacity == pytest.approx(0.8)
    assert line.transform.apply(0, 0) == pytest.approx((96, 96))
    assert line.transform.apply(640, 360) == pytest.approx((736, 456))


@pytest.mark.parametrize(
    ("value", "expected"),
    [("12", 12), ("12px", 12), ("72pt", 96), ("1in", 96), ("25.4mm", 96)],
)
def test_parse_length_units(value: str, expected: float) -> None:
    assert parse_length(value) == pytest.approx(expected)


def test_transform_order_matches_svg_matrix_composition() -> None:
    transform = parse_transform("translate(10 20) scale(2)")
    assert transform.apply(5, 5) == pytest.approx((20, 30))


def test_malformed_transform_is_rejected() -> None:
    with pytest.raises(ValueError, match="Unsupported or malformed"):
        parse_transform("translate(10, 20, 30)")
