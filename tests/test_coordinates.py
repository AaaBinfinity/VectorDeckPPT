import pytest
from lib.coordinates import (
    DEFAULT_SLIDE_HEIGHT_INCHES,
    DEFAULT_SLIDE_WIDTH_INCHES,
    CoordinateMapper,
    css_px_to_points,
    emu_to_inches,
)


def test_default_canvas_maps_to_widescreen_slide() -> None:
    mapper = CoordinateMapper()

    assert emu_to_inches(mapper.width(1600)) == pytest.approx(DEFAULT_SLIDE_WIDTH_INCHES)
    assert emu_to_inches(mapper.height(900)) == pytest.approx(DEFAULT_SLIDE_HEIGHT_INCHES)
    assert mapper.point(0, 0) == (0, 0)


def test_coordinates_respect_viewbox_origin() -> None:
    mapper = CoordinateMapper(canvas_width=800, canvas_height=450, view_x=100, view_y=50)

    assert mapper.point(100, 50) == (0, 0)
    assert emu_to_inches(mapper.x(900)) == pytest.approx(DEFAULT_SLIDE_WIDTH_INCHES)
    assert emu_to_inches(mapper.y(500)) == pytest.approx(DEFAULT_SLIDE_HEIGHT_INCHES)


def test_invalid_canvas_is_rejected() -> None:
    with pytest.raises(ValueError, match="Canvas dimensions"):
        CoordinateMapper(canvas_width=0)


def test_css_pixels_convert_to_points() -> None:
    assert css_px_to_points(96) == pytest.approx(72)
