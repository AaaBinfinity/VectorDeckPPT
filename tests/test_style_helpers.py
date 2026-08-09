import pytest
from lib.colors import parse_color
from lib.fonts import baseline_to_top, estimate_text_width, font_candidates, is_bold


@pytest.mark.parametrize(
    ("value", "rgb", "alpha"),
    [
        ("#2563EB", (37, 99, 235), 1.0),
        ("#fff8", (255, 255, 255), 136 / 255),
        ("rgb(255, 0, 128)", (255, 0, 128), 1.0),
        ("rgba(10, 20, 30, 0.5)", (10, 20, 30), 0.5),
        ("transparent", (0, 0, 0), 0.0),
    ],
)
def test_parse_color_formats(value: str, rgb: tuple[int, int, int], alpha: float) -> None:
    color = parse_color(value)
    assert color is not None
    assert color.rgb == rgb
    assert color.alpha == pytest.approx(alpha)


def test_none_and_gradient_color_behavior() -> None:
    assert parse_color("none") is None
    with pytest.raises(ValueError, match="Paint servers"):
        parse_color("url(#gradient)")


def test_font_helpers_handle_cjk_and_weight() -> None:
    candidates = font_candidates("'Microsoft YaHei', PingFang SC, sans-serif")

    assert candidates == ["Microsoft YaHei", "PingFang SC", "sans-serif"]
    assert is_bold("700")
    assert is_bold("bold")
    assert not is_bold("500")
    assert estimate_text_width("中文", 20) > estimate_text_width("ii", 20)
    assert baseline_to_top(100, 20) == pytest.approx(83.6)
