import struct
from pathlib import Path

import pytest
import yaml

ROOT = Path(__file__).resolve().parents[1]
SKILL_DIR = ROOT / ".agents" / "skills" / "vectordeckppt"
REFERENCES = {
    "workflow.md",
    "presentation-planning.md",
    "art-direction.md",
    "design-system.md",
    "slide-design.md",
    "svg-authoring.md",
    "svg-to-pptx.md",
    "visual-review.md",
    "troubleshooting.md",
    "style-templates.md",
}
STYLE_TEMPLATES = {
    "bright-tech-systems.png",
    "dark-engineered-systems.png",
    "editorial-intelligence.png",
    "expressive-cultural.png",
    "human-documentary.png",
}


def test_skill_metadata_and_interface_are_complete() -> None:
    content = (SKILL_DIR / "SKILL.md").read_text(encoding="utf-8")
    _, frontmatter, body = content.split("---", 2)
    metadata = yaml.safe_load(frontmatter)

    assert metadata["name"] == "vectordeckppt"
    assert "PPTX" in metadata["description"]
    assert "TODO" not in content
    assert "Required workflow" in body
    assert "Design decision order" in body

    interface = yaml.safe_load((SKILL_DIR / "agents" / "openai.yaml").read_text(encoding="utf-8"))[
        "interface"
    ]
    assert interface["display_name"] == "VectorDeckPPT"
    assert "$vectordeckppt" in interface["default_prompt"]
    assert "art-directed" in interface["default_prompt"]
    assert {path.name for path in (SKILL_DIR / "references").glob("*.md")} == REFERENCES
    assert all((SKILL_DIR / "references" / name).stat().st_size > 1000 for name in REFERENCES)

    art_direction = (SKILL_DIR / "references" / "art-direction.md").read_text(encoding="utf-8")
    assert "Visual thesis" in art_direction
    assert "Meaning-to-form decisions" in art_direction
    assert "Aesthetic anti-patterns" in art_direction


def test_style_template_library_is_complete_and_widescreen() -> None:
    content = (SKILL_DIR / "SKILL.md").read_text(encoding="utf-8")
    reference = (SKILL_DIR / "references" / "style-templates.md").read_text(
        encoding="utf-8"
    )
    asset_dir = SKILL_DIR / "assets" / "style-templates"

    assert "style-templates.md" in content
    assert {path.name for path in asset_dir.glob("*.png")} == STYLE_TEMPLATES

    for name in STYLE_TEMPLATES:
        path = asset_dir / name
        data = path.read_bytes()
        assert data[:8] == b"\x89PNG\r\n\x1a\n"
        width, height = struct.unpack(">II", data[16:24])
        assert width >= 1600
        assert height >= 900
        assert width / height == pytest.approx(16 / 9, rel=0.01)
        assert f"../assets/style-templates/{name}" in reference
