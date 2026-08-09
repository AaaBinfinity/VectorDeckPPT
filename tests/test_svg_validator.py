import json
import subprocess
import sys
from pathlib import Path

from lib.svg_validator import validate_svg

ROOT = Path(__file__).resolve().parents[1]
FIXTURES = Path(__file__).parent / "fixtures"
VALIDATOR = ROOT / ".agents" / "skills" / "vectordeckppt" / "scripts" / "validate_svg.py"


def test_valid_svg_fixtures_pass() -> None:
    for name in [
        "simple_text.svg",
        "simple_rect.svg",
        "simple_circle.svg",
        "simple_line.svg",
        "simple_image.svg",
    ]:
        result = validate_svg(FIXTURES / name)
        assert result.valid, (name, result.to_dict())


def test_forbidden_tags_are_reported() -> None:
    script_result = validate_svg(FIXTURES / "invalid_script.svg")
    foreign_result = validate_svg(FIXTURES / "invalid_foreign_object.svg")

    assert {error.code for error in script_result.errors} == {"forbidden_element"}
    assert "forbidden_element" in {error.code for error in foreign_result.errors}
    assert "unsupported_element" in {error.code for error in foreign_result.errors}


def test_missing_and_remote_images_are_rejected(tmp_path: Path) -> None:
    missing = tmp_path / "missing.svg"
    missing.write_text(
        '<svg xmlns="http://www.w3.org/2000/svg" width="1600" height="900" '
        'viewBox="0 0 1600 900"><image href="nope.png" width="10" height="10"/></svg>',
        encoding="utf-8",
    )
    remote = tmp_path / "remote.svg"
    remote.write_text(
        '<svg xmlns="http://www.w3.org/2000/svg" width="1600" height="900" '
        'viewBox="0 0 1600 900"><image href="https://example.com/a.png" '
        'width="10" height="10"/></svg>',
        encoding="utf-8",
    )

    assert "missing_image_file" in {item.code for item in validate_svg(missing).errors}
    assert "remote_resource" in {item.code for item in validate_svg(remote).errors}


def test_overflow_and_small_text_are_warnings(tmp_path: Path) -> None:
    source = tmp_path / "warnings.svg"
    source.write_text(
        '<svg xmlns="http://www.w3.org/2000/svg" width="1600" height="900" '
        'viewBox="0 0 1600 900"><rect x="1500" y="800" width="200" height="200"/>'
        '<text x="20" y="20" font-size="8">tiny</text></svg>',
        encoding="utf-8",
    )

    result = validate_svg(source)
    codes = {item.code for item in result.warnings}
    assert result.valid
    assert {"element_overflow", "small_text"} <= codes


def test_cli_json_and_exit_codes() -> None:
    completed = subprocess.run(
        [sys.executable, str(VALIDATOR), str(FIXTURES / "simple_text.svg"), "--json"],
        check=False,
        capture_output=True,
        text=True,
        encoding="utf-8",
    )
    payload = json.loads(completed.stdout)

    assert completed.returncode == 0
    assert payload["valid"] is True
    assert payload["canvas"]["viewBox"] == [0.0, 0.0, 1600.0, 900.0]

    invalid = subprocess.run(
        [sys.executable, str(VALIDATOR), str(FIXTURES / "invalid_script.svg"), "--json"],
        check=False,
        capture_output=True,
        text=True,
        encoding="utf-8",
    )
    assert invalid.returncode == 1
