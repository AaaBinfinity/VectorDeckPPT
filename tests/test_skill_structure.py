from pathlib import Path

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
