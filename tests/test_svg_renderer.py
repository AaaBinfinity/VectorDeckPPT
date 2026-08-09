import subprocess
import sys
from pathlib import Path

import pytest
from lib.svg_renderer import SvgRenderError, render_directory, render_svg
from PIL import Image

ROOT = Path(__file__).resolve().parents[1]
FIXTURES = Path(__file__).parent / "fixtures"
RENDERER = ROOT / ".agents" / "skills" / "vectordeckppt" / "scripts" / "render_svg.py"


def test_render_single_svg_to_expected_size(tmp_path: Path) -> None:
    output = render_svg(FIXTURES / "simple_text.svg", tmp_path / "preview.png")

    assert output.is_file()
    with Image.open(output) as preview:
        assert preview.size == (1600, 900)
        assert preview.mode in {"RGB", "RGBA"}


def test_renderer_refuses_invalid_svg(tmp_path: Path) -> None:
    with pytest.raises(SvgRenderError, match="validation failed"):
        render_svg(FIXTURES / "invalid_script.svg", tmp_path / "invalid.png")


def test_batch_render_and_cli(tmp_path: Path) -> None:
    source_dir = tmp_path / "slides"
    output_dir = tmp_path / "previews"
    source_dir.mkdir()
    for name in ["simple_rect.svg", "simple_circle.svg"]:
        (source_dir / name).write_bytes((FIXTURES / name).read_bytes())

    outputs = render_directory(source_dir, output_dir, width=800, height=450)
    assert [item.name for item in outputs] == ["simple_circle.png", "simple_rect.png"]
    with Image.open(outputs[0]) as preview:
        assert preview.size == (800, 450)

    cli_output = tmp_path / "cli.png"
    completed = subprocess.run(
        [
            sys.executable,
            str(RENDERER),
            str(FIXTURES / "simple_line.svg"),
            "--output",
            str(cli_output),
        ],
        check=False,
        capture_output=True,
        text=True,
        encoding="utf-8",
    )
    assert completed.returncode == 0, completed.stderr
    assert cli_output.is_file()
