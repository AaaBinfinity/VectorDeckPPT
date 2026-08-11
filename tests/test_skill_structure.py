import struct
from pathlib import Path

import pytest
import yaml
from lib.typography_audit import audit_typography

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
    "data-forward-clarity.png",
    "dark-engineered-systems.png",
    "editorial-intelligence.png",
    "expressive-cultural.png",
    "dynamic-hero-editorial.png",
    "human-documentary.png",
    "premium-restraint.png",
    "product-storytelling.png",
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
    assert {path.name for path in asset_dir.glob("*.svg")} == {
        Path(name).with_suffix(".svg").name for name in STYLE_TEMPLATES
    }

    for name in STYLE_TEMPLATES:
        path = asset_dir / name
        data = path.read_bytes()
        assert data[:8] == b"\x89PNG\r\n\x1a\n"
        width, height = struct.unpack(">II", data[16:24])
        assert width >= 1600
        assert height >= 900
        assert width / height == pytest.approx(16 / 9, rel=0.01)
        assert f"../assets/style-templates/{name}" in reference
        source_name = Path(name).with_suffix(".svg").name
        source = asset_dir / source_name
        source_text = source.read_text(encoding="utf-8")
        assert source.stat().st_size > 10_000
        assert 'data-role="slide-title"' in source_text
        assert 'data-role="subheading"' in source_text
        assert "ILLUSTRATIVE TEMPLATE" in source_text
        assert f"../assets/style-templates/{source_name}" in reference
        assert audit_typography(source, strict=True).valid


def test_skill_enforces_clarification_and_staged_approval() -> None:
    content = (SKILL_DIR / "SKILL.md").read_text(encoding="utf-8")
    workflow = (SKILL_DIR / "references" / "workflow.md").read_text(encoding="utf-8")
    planning = (SKILL_DIR / "references" / "presentation-planning.md").read_text(
        encoding="utf-8"
    )
    readme = (ROOT / "README.md").read_text(encoding="utf-8")
    interface_path = SKILL_DIR / "agents" / "openai.yaml"
    interface = yaml.safe_load(interface_path.read_text(encoding="utf-8"))["interface"]

    assert "./pptoutput/" in content
    assert "SKILL_ROOT =" in content
    assert "DECK_ROOT =" in content
    assert "DECK_ROOT/slide-content.md" in content
    assert "sample_count = min(3, final_slide_count)" in content
    assert "explicitly approves the slide content" in content
    assert "explicitly approves the representative visual sample" in content
    assert "focused grouped questions" in content
    assert "request-contract approval" in content
    assert content.index("text-only slide draft") < content.index("representative visual")
    assert ".agents/skills/vectordeckppt/scripts/" not in content
    assert "opts out" not in content

    assert "Request completion" in workflow
    assert "Request confirmation" in workflow
    assert "Text approval" in workflow
    assert "Visual approval" in workflow
    assert "Full production" in workflow
    assert "one to three focused grouped questions" in workflow
    assert "SKILL_ROOT =" in workflow
    assert "DECK_ROOT =" in workflow
    assert "DECK_ROOT/sample/slides/" in workflow
    assert "All three confirmation gates are mandatory" in workflow
    assert "deck-work/" not in workflow

    assert "Request accuracy" in planning
    assert "Text-only approval artifact" in planning
    assert "受众知识水平与决策权" in readme
    assert "等待用户明确批准文字内容" in readme
    assert "等待用户明确批准视觉样稿" in readme
    assert "deck-work/" not in readme
    assert "up-to-three-slide" in interface["default_prompt"]
    assert "complete request contract" in interface["default_prompt"]
    assert "pptoutput/" in (ROOT / ".gitignore").read_text(encoding="utf-8")


def test_skill_confirms_complete_request_and_supports_controlled_artistry() -> None:
    content = (SKILL_DIR / "SKILL.md").read_text(encoding="utf-8")
    workflow = (SKILL_DIR / "references" / "workflow.md").read_text(encoding="utf-8")
    planning = (SKILL_DIR / "references" / "presentation-planning.md").read_text(
        encoding="utf-8"
    )
    art_direction = (SKILL_DIR / "references" / "art-direction.md").read_text(
        encoding="utf-8"
    )
    design = (SKILL_DIR / "references" / "design-system.md").read_text(
        encoding="utf-8"
    )
    style_templates = (SKILL_DIR / "references" / "style-templates.md").read_text(
        encoding="utf-8"
    )
    readme = (ROOT / "README.md").read_text(encoding="utf-8")
    prd = (ROOT / "doc" / "PRD.md").read_text(encoding="utf-8")

    assert content.index("request-contract approval") < content.index(
        "text-only slide draft"
    )
    assert "do not synthesize sources" in content
    assert "All three confirmation gates are mandatory" in workflow
    assert "Open questions: none" in planning
    assert "Setting and credibility gate" in art_direction
    assert "Dynamic hero editorial" in art_direction
    assert "hero typography" in design
    assert "Dynamic Hero Editorial" in style_templates
    assert "protected characters" in style_templates
    assert "九套内置视觉方向" in readme
    assert "专业不等于所有页面都横平竖直" in readme
    assert "完整需求合同" in prd


def test_skill_defaults_to_information_rich_evidence_led_slides() -> None:
    content = (SKILL_DIR / "SKILL.md").read_text(encoding="utf-8")
    planning = (SKILL_DIR / "references" / "presentation-planning.md").read_text(
        encoding="utf-8"
    )
    slide_design = (SKILL_DIR / "references" / "slide-design.md").read_text(
        encoding="utf-8"
    )
    workflow = (SKILL_DIR / "references" / "workflow.md").read_text(encoding="utf-8")
    visual_review = (SKILL_DIR / "references" / "visual-review.md").read_text(
        encoding="utf-8"
    )
    readme = (ROOT / "README.md").read_text(encoding="utf-8")
    interface_path = SKILL_DIR / "agents" / "openai.yaml"
    interface = yaml.safe_load(interface_path.read_text(encoding="utf-8"))["interface"]

    assert "information-rich content" in content
    assert "Never invent numbers" in content
    assert "information-rich core-content page" in content
    assert "Content richness plan" in planning
    assert "80–180 Chinese characters" in planning
    assert "roughly two thirds" in planning
    assert "Default content density" in slide_design
    assert "Never invent values" in slide_design
    assert "Supporting explanation or points" in workflow
    assert "default text density" in workflow
    assert "information-rich" in visual_review
    assert "默认内容密度" in readme
    assert "不得为了好看伪造" in readme
    assert "information-rich" in interface["default_prompt"]


def test_skill_locks_typography_roles_and_runs_deck_audit() -> None:
    content = (SKILL_DIR / "SKILL.md").read_text(encoding="utf-8")
    design = (SKILL_DIR / "references" / "design-system.md").read_text(
        encoding="utf-8"
    )
    slide_design = (SKILL_DIR / "references" / "slide-design.md").read_text(
        encoding="utf-8"
    )
    visual_review = (SKILL_DIR / "references" / "visual-review.md").read_text(
        encoding="utf-8"
    )
    workflow = (SKILL_DIR / "references" / "workflow.md").read_text(encoding="utf-8")
    readme = (ROOT / "README.md").read_text(encoding="utf-8")
    docs_index = (ROOT / "doc" / "README.md").read_text(encoding="utf-8")
    prompts = (ROOT / "doc" / "prompt-examples.md").read_text(encoding="utf-8")
    troubleshooting = (SKILL_DIR / "references" / "troubleshooting.md").read_text(
        encoding="utf-8"
    )

    assert "one exact `slide-title` token across the deck" in content
    assert "data-role" in content
    assert "audit_typography.py" in content
    assert "One exact `slide-title` token" in design
    assert "All peer headings" in design
    assert "locked typography role" in slide_design
    assert "inconsistent_peer_size" in visual_review
    assert "audit_typography.py" in workflow
    assert "所有普通页面标题使用同一个精确字号" in readme
    assert "九套内置视觉语法" in docs_index
    assert "字体审计脚本" in docs_index
    assert "同页同级模块标题必须完全一致" in prompts
    assert "Typography audit fails" in troubleshooting
    assert "missing_text_role" in troubleshooting
    assert "inconsistent_peer_size" in troubleshooting
    assert "inconsistent_deck_size" in troubleshooting
    assert "inconsistent_deck_title_family" in troubleshooting
    assert "inconsistent_deck_title_weight" in troubleshooting


def test_v11_documentation_matches_compiler_and_delivery_contract() -> None:
    skill = (SKILL_DIR / "SKILL.md").read_text(encoding="utf-8")
    workflow = (SKILL_DIR / "references" / "workflow.md").read_text(encoding="utf-8")
    design = (SKILL_DIR / "references" / "design-system.md").read_text(encoding="utf-8")
    mapping = (SKILL_DIR / "references" / "svg-to-pptx.md").read_text(encoding="utf-8")
    readme = (ROOT / "README.md").read_text(encoding="utf-8")
    prd = (ROOT / "doc" / "PRD.md").read_text(encoding="utf-8")

    assert "48` compiles to `28.8 pt" in design
    assert "48–56 | 28.8–33.6" in design
    assert "PowerPoint Freeform" in mapping
    assert "straight-segment `polygon`/`polyline`" in mapping
    assert "--report compilation-report.json" in readme
    assert "Bright Tech Systems" in readme
    assert "Human Documentary" in readme
    assert "**文档版本：** V1.1" in prd
    assert "直接在 `main` 维护" in prd
    assert "sample_count = min(3, final_slide_count)" in skill
    assert "sample_count = min(3, final_slide_count)" in workflow
