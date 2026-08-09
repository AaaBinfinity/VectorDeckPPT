import json
import subprocess
import sys
from pathlib import Path
from zipfile import ZipFile

from lib.pptx_compiler import compile_pptx
from lib.pptx_validator import validate_pptx

ROOT = Path(__file__).resolve().parents[1]
FIXTURES = Path(__file__).parent / "fixtures"
VALIDATOR = ROOT / ".agents" / "skills" / "vectordeckppt" / "scripts" / "validate_pptx.py"


def test_generated_pptx_passes_package_validation(tmp_path: Path) -> None:
    output = tmp_path / "deck.pptx"
    compile_pptx(FIXTURES / "mixed_slide.svg", output)

    result = validate_pptx(output)
    assert result.valid, result.to_dict()
    assert result.slides == 1
    assert result.media == 1


def test_invalid_container_and_missing_parts_fail(tmp_path: Path) -> None:
    plain = tmp_path / "plain.pptx"
    plain.write_text("not a zip", encoding="utf-8")
    assert not validate_pptx(plain).valid

    partial = tmp_path / "partial.pptx"
    with ZipFile(partial, "w") as archive:
        archive.writestr("[Content_Types].xml", "<Types/>")
    result = validate_pptx(partial)
    assert not result.valid
    assert any("Missing required" in error for error in result.errors)


def test_validator_cli_emits_json(tmp_path: Path) -> None:
    output = tmp_path / "deck.pptx"
    compile_pptx(FIXTURES / "simple_rect.svg", output)
    completed = subprocess.run(
        [sys.executable, str(VALIDATOR), str(output), "--json"],
        check=False,
        capture_output=True,
        text=True,
        encoding="utf-8",
    )
    payload = json.loads(completed.stdout)
    assert completed.returncode == 0
    assert payload["valid"] is True
    assert payload["slides"] == 1
