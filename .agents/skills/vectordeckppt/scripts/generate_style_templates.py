# ruff: noqa: E501

from __future__ import annotations

import argparse
from collections.abc import Sequence
from dataclasses import dataclass
from html import escape
from pathlib import Path

from lib.svg_renderer import render_svg


@dataclass(frozen=True, slots=True)
class Theme:
    slug: str
    name: str
    context: str
    field: str
    panel: str
    surface: str
    text: str
    muted: str
    border: str
    accent: str
    accent_2: str
    positive: str
    warning: str
    display_font: str
    body_font: str
    radius: int
    cover_title: str
    cover_subtitle: str
    metrics: tuple[tuple[str, str], ...]
    steps: tuple[tuple[str, str], ...]
    priorities: tuple[tuple[str, str], ...]
    hero_font: str | None = None


COMMON_STEPS = (
    ("Frame", "Define the decision and success signal"),
    ("Read", "Extract facts, constraints, and tensions"),
    ("Design", "Map evidence to the\nclearest visual form"),
    ("Verify", "Review fidelity, meaning, and exceptions"),
    ("Act", "Assign the next move, owner, and timing"),
)

THEMES = (
    Theme(
        "bright-tech-systems",
        "BRIGHT TECH SYSTEMS",
        "PRODUCT & AI OPERATIONS",
        "#DCEBFA",
        "#F8FBFF",
        "#FFFFFF",
        "#0B1F44",
        "#526783",
        "#B9D0EC",
        "#1261D8",
        "#11A9CC",
        "#2E9A62",
        "#E89B24",
        "Arial Black, Arial, sans-serif",
        "Arial",
        18,
        "From capability\nto repeatable\nimpact",
        "A clear operating story connects product mechanics, evidence, and adoption.",
        (("84%", "workflow adoption"), ("2.4x", "faster review"), ("−31%", "handoff time")),
        COMMON_STEPS,
        (("Standardize", "Owner: Platform · Q3"), ("Instrument", "Owner: Data · Q3"), ("Scale", "Owner: Ops · Q4")),
    ),
    Theme(
        "dark-engineered-systems",
        "DARK ENGINEERED SYSTEMS",
        "ARCHITECTURE & RELIABILITY",
        "#07111F",
        "#0B1728",
        "#101F33",
        "#E8F1FA",
        "#8EA1B6",
        "#304259",
        "#20C4E8",
        "#5077FF",
        "#35C477",
        "#F0B33A",
        "Bahnschrift SemiCondensed, Arial Narrow, Arial, sans-serif",
        "Arial",
        4,
        "Reliability is\na system\nproperty",
        "Expose dependencies, failure boundaries, controls, and ownership in one view.",
        (("99.95%", "service objective"), ("−42%", "recovery time"), ("18", "critical controls")),
        COMMON_STEPS,
        (("Contain", "Owner: SRE · Now"), ("Automate", "Owner: Infra · Q3"), ("Harden", "Owner: Security · Q4")),
    ),
    Theme(
        "editorial-intelligence",
        "EDITORIAL INTELLIGENCE",
        "STRATEGY & RESEARCH",
        "#D8D4CC",
        "#F7F3EB",
        "#EEE8DD",
        "#161616",
        "#5E5A54",
        "#BFB7AA",
        "#1746A2",
        "#C94A3A",
        "#326B52",
        "#B37A2D",
        "Georgia",
        "Arial",
        0,
        "Clarity turns\nevidence into\nadvantage",
        "An editorial system gives claims, sources, and implications visible hierarchy.",
        (("3", "decisions reframed"), ("12", "sources synthesized"), ("1", "recommended path")),
        COMMON_STEPS,
        (("Focus", "Decision · This week"), ("Differentiate", "Strategy · Q3"), ("Compound", "Portfolio · Q4")),
    ),
    Theme(
        "expressive-cultural",
        "EXPRESSIVE CULTURAL",
        "BRAND, CULTURE & LAUNCH",
        "#111111",
        "#FFF4DE",
        "#F3E6CC",
        "#0A0A0A",
        "#534C44",
        "#111111",
        "#2449E8",
        "#F44C3A",
        "#1C8B63",
        "#F4B51D",
        "Impact, Arial Black, Arial, sans-serif",
        "Arial",
        0,
        "Make the idea\nimpossible\nto ignore",
        "A bold visual rhythm carries one cultural proposition through proof and action.",
        (("4", "audience moments"), ("62%", "earned reach"), ("3", "launch chapters")),
        COMMON_STEPS,
        (("Reveal", "Story · Week 1"), ("Mobilize", "Community · Week 2"), ("Sustain", "Program · Week 4")),
    ),
    Theme(
        "human-documentary",
        "HUMAN DOCUMENTARY",
        "FIELD RESEARCH & IMPACT",
        "#D8CEBD",
        "#FAF4E9",
        "#EFE3D1",
        "#273129",
        "#6B655B",
        "#BEB09A",
        "#B76038",
        "#55705B",
        "#4C8060",
        "#C28B47",
        "Georgia",
        "Arial",
        8,
        "Start with lived\nexperience,\nthen act",
        "People, place, testimony, and measured outcomes remain visible together.",
        (("24", "field interviews"), ("7", "community sites"), ("81%", "follow-through")),
        COMMON_STEPS,
        (("Listen", "Field team · Now"), ("Co-design", "Community · Q3"), ("Return", "Program · Q4")),
    ),
    Theme(
        "dynamic-hero-editorial",
        "DYNAMIC HERO EDITORIAL",
        "城市响应、品牌战役与高张力叙事",
        "#070A11",
        "#0D111B",
        "#171D28",
        "#F7F8FC",
        "#A6ADBC",
        "#303746",
        "#FF1748",
        "#7ACBFF",
        "#36D399",
        "#FFBF3C",
        "Impact",
        "Arial",
        0,
        "让关键命题\n拥有英雄式\n视觉重量",
        "以叠字、斜切、网点、速度线和原创抽象徽记，建立高张力但仍可读的叙事系统。",
        (("87%", "示例就绪度"), ("04", "关键窗口"), ("24h", "响应周期")),
        (
            ("Frame", "Define the decision"),
            ("Read", "Extract the evidence"),
            ("Design", "Choose the clearest form"),
            ("Verify", "Review fidelity"),
            ("Act", "Set owner and timing"),
        ),
        (("锁定判断", "叙事负责人 · 现在"), ("组织响应", "行动团队 · 第 1 天"), ("验证闭环", "决策人 · 第 2 天")),
    ),
    Theme(
        "data-forward-clarity",
        "DATA-FORWARD CLARITY",
        "ANALYTICS & OPERATING REVIEW",
        "#DFE7E5",
        "#F9FBFA",
        "#FFFFFF",
        "#102C2A",
        "#58716E",
        "#B9CCCA",
        "#087F73",
        "#2D62CC",
        "#21956C",
        "#D28B26",
        "Aptos Display, Arial, sans-serif",
        "Arial",
        10,
        "Show the signal,\nexplain\nthe driver",
        "Direct labels and disciplined comparison turn metrics into operating decisions.",
        (("+18%", "qualified demand"), ("−9d", "sales cycle"), ("3.2x", "retention lift")),
        COMMON_STEPS,
        (("Protect", "Core funnel · Now"), ("Test", "New segment · Q3"), ("Expand", "Winning motion · Q4")),
    ),
    Theme(
        "premium-restraint",
        "PREMIUM RESTRAINT",
        "EXECUTIVE & PORTFOLIO",
        "#151813",
        "#20231D",
        "#292D25",
        "#F1EBDD",
        "#B8B2A5",
        "#55594D",
        "#C7A35A",
        "#8E9B78",
        "#7FA075",
        "#C58D4F",
        "Georgia",
        "Arial",
        2,
        "Fewer priorities.\nStronger\ncompounding.",
        "A restrained system gives the decisive evidence room to carry authority.",
        (("3", "portfolio bets"), ("68%", "capital focused"), ("24m", "value horizon")),
        COMMON_STEPS,
        (("Concentrate", "Capital · FY27"), ("Sequence", "Leadership · Q3"), ("Measure", "Board · Quarterly")),
    ),
    Theme(
        "product-storytelling",
        "PRODUCT STORYTELLING",
        "LAUNCH & EXPERIENCE",
        "#DDE8E3",
        "#F8FBF9",
        "#FFFFFF",
        "#102A25",
        "#60736E",
        "#B7CBC3",
        "#19765F",
        "#E46B4F",
        "#37956D",
        "#D79534",
        "Aptos Display, Arial, sans-serif",
        "Arial",
        22,
        "Make the product\njourney feel\ninevitable",
        "Connect the user's friction, product behavior, proof, and path to adoption.",
        (("42%", "less setup"), ("3", "core moments"), ("1 wk", "time to value")),
        COMMON_STEPS,
        (("Prove", "Pilot · Week 1"), ("Enable", "Teams · Week 2"), ("Expand", "Accounts · Month 2")),
    ),
    Theme(
        "forest-poetic-mosaic",
        "FOREST POETIC MOSAIC",
        "CULTURE, PLACE & BRAND STORY",
        "#D9E1DC",
        "#F5F7F4",
        "#FFFFFF",
        "#0B4B38",
        "#56665F",
        "#C7D2CC",
        "#0B5A42",
        "#8FAA98",
        "#2E765B",
        "#C7A86A",
        "Microsoft YaHei, Noto Sans SC, Arial, sans-serif",
        "Microsoft YaHei, Noto Sans SC, Arial, sans-serif",
        0,
        "林深处\n见新境",
        "Use calligraphic scale, documentary calm, and image-like geometric crops to turn place into evidence.",
        (("08", "story moves"), ("03", "evidence modes"), ("01", "decisive close")),
        COMMON_STEPS,
        (("入境", "Opening · Establish place"), ("见证", "Evidence · Reveal detail"), ("归纳", "Decision · Resolve meaning")),
        hero_font="STXingkai, FZShuTi, KaiTi, serif",
    ),
    Theme(
        "silk-ink-strategy",
        "SILK & INK STRATEGY",
        "BRAND, STRATEGY & CULTURAL LAUNCH",
        "#ECE9E1",
        "#FBFAF6",
        "#FFFFFF",
        "#2F6259",
        "#6F756E",
        "#D8D4C8",
        "#3D6F63",
        "#C39B4B",
        "#557C68",
        "#B77948",
        "Microsoft YaHei, Noto Sans SC, Arial, sans-serif",
        "Microsoft YaHei, Noto Sans SC, Arial, sans-serif",
        0,
        "青岚\n入卷",
        "A calm cultural system pairs brush typography with mist, mountain silhouettes, and evidence-led strategy pages.",
        (("4", "strategy lenses"), ("6", "story chapters"), ("1", "recommended path")),
        COMMON_STEPS,
        (("定势", "Position · This week"), ("成形", "System · Q3"), ("扩散", "Activation · Q4")),
        hero_font="STXingkai, FZShuTi, KaiTi, serif",
    ),
    Theme(
        "museum-cultural-editorial",
        "MUSEUM CULTURAL EDITORIAL",
        "HERITAGE, EXHIBITION & INSTITUTION",
        "#201A17",
        "#2A211D",
        "#F3EBDD",
        "#F5EFE4",
        "#B8ACA0",
        "#5B493F",
        "#A43B2F",
        "#C6A565",
        "#6D8B72",
        "#BC7B46",
        "Microsoft YaHei, Noto Sans SC, Arial, sans-serif",
        "Microsoft YaHei, Noto Sans SC, Arial, sans-serif",
        0,
        "器物\n与时间",
        "A museum-like editorial system gives artifacts, chronology, interpretation, and public action one authored rhythm.",
        (("06", "narrative rooms"), ("12", "key objects"), ("03", "public programs")),
        COMMON_STEPS,
        (("读物", "Object · Evidence"), ("识时", "Context · Meaning"), ("入世", "Program · Action")),
        hero_font="STXingkai, FZShuTi, KaiTi, serif",
    ),
)


def _rect(
    x: float,
    y: float,
    width: float,
    height: float,
    fill: str,
    *,
    stroke: str = "none",
    stroke_width: float = 0,
    radius: float = 0,
) -> str:
    return (
        f'<rect x="{x:g}" y="{y:g}" width="{width:g}" height="{height:g}" '
        f'rx="{radius:g}" fill="{fill}" stroke="{stroke}" '
        f'stroke-width="{stroke_width:g}"/>'
    )


def _line(
    x1: float,
    y1: float,
    x2: float,
    y2: float,
    stroke: str,
    width: float = 2,
) -> str:
    return (
        f'<line x1="{x1:g}" y1="{y1:g}" x2="{x2:g}" y2="{y2:g}" '
        f'stroke="{stroke}" stroke-width="{width:g}"/>'
    )


def _text(
    x: float,
    y: float,
    value: str,
    *,
    size: float,
    fill: str,
    family: str,
    role: str,
    weight: int = 400,
    line_height: float = 1.18,
    anchor: str = "start",
) -> str:
    lines = value.split("\n")
    tspans = []
    for index, line in enumerate(lines):
        dy = 0 if index == 0 else size * line_height
        tspans.append(
            f'<tspan x="{x:g}" dy="{dy:g}">{escape(line)}</tspan>'
        )
    return (
        f'<text data-role="{role}" x="{x:g}" y="{y:g}" font-family="{family}" '
        f'font-size="{size:g}" font-weight="{weight}" fill="{fill}" '
        f'text-anchor="{anchor}">{"".join(tspans)}</text>'
    )


def _panel_frame(theme: Theme, x: int, y: int, page: str, section: str) -> list[str]:
    parts = [
        _rect(x, y, 760, 400, theme.panel, stroke=theme.border, stroke_width=1, radius=theme.radius),
        _rect(x, y, 760, 6, theme.accent, radius=theme.radius),
        _text(
            x + 34,
            y + 34,
            section.upper(),
            size=10,
            fill=theme.accent,
            family=theme.body_font,
            role="label",
            weight=700,
        ),
        _text(
            x + 714,
            y + 34,
            page,
            size=10,
            fill=theme.muted,
            family=theme.body_font,
            role="page-number",
            weight=700,
            anchor="end",
        ),
    ]
    if theme.slug == "dynamic-hero-editorial":
        decorations = [
            f'<polygon points="{x + 524},{y} {x + 760},{y} {x + 760},{y + 210}" fill="#280817"/>',
            f'<polygon points="{x + 650},{y} {x + 760},{y} {x + 760},{y + 96}" fill="{theme.accent}"/>',
            f'<polygon points="{x + 610},{y + 400} {x + 760},{y + 270} {x + 760},{y + 400}" fill="#150710"/>',
        ]
        for offset in range(130, 820, 54):
            decorations.append(
                _line(x + offset, y + 8, x + offset - 208, y + 400, theme.border, 0.8)
            )
        for row in range(6):
            for column in range(9):
                decorations.append(
                    f'<circle cx="{x + 574 + column * 17}" cy="{y + 42 + row * 17}" '
                    f'r="{1.5 + ((row + column) % 3) * 0.7:g}" fill="#7D1B38"/>'
                )
        for index in range(6):
            decorations.append(
                _line(
                    x + 470,
                    y + 226 + index * 19,
                    x + 748,
                    y + 124 + index * 28,
                    "#6C3143",
                    0.8,
                )
            )
        parts[1:1] = decorations
    if theme.slug == "dark-engineered-systems":
        for offset in range(70, 720, 80):
            parts.append(_line(x + offset, y + 58, x + offset, y + 374, theme.border, 0.5))
    if theme.slug == "expressive-cultural":
        parts.extend(
            [
                f'<polygon points="{x + 590},{y} {x + 760},{y} {x + 760},{y + 150}" '
                f'fill="{theme.accent_2}"/>',
                f'<polygon points="{x + 650},{y + 400} {x + 760},{y + 250} '
                f'{x + 760},{y + 400}" fill="{theme.warning}"/>',
            ]
        )
    return parts


def _legacy_dynamic_hero_cover(theme: Theme, x: int, y: int) -> list[str]:
    parts = _panel_frame(theme, x, y, "01", theme.context)
    parts.extend(
        [
            f'<polygon points="{x + 26},{y + 96} {x + 388},{y + 66} {x + 410},{y + 212} '
            f'{x + 54},{y + 244}" fill="#0A0D15" stroke="{theme.accent}" stroke-width="8"/>',
            f'<polygon points="{x + 26},{y + 76} {x + 272},{y + 54} {x + 260},{y + 92} '
            f'{x + 18},{y + 114}" fill="{theme.accent}"/>',
            _text(
                x + 40,
                y + 91,
                "HERO TYPOGRAPHY / CONTROLLED MOTION",
                size=10,
                fill="#FFFFFF",
                family=theme.body_font,
                role="label",
                weight=700,
            ),
            _text(
                x + 48,
                y + 136,
                "MAKE THE\nCENTRAL IDEA\nFEEL HEROIC",
                size=36,
                fill=theme.text,
                family=theme.display_font,
                role="deck-title",
                weight=900,
                line_height=0.96,
            ),
            _rect(x + 38, y + 258, 354, 58, "#090C13", stroke=theme.border, stroke_width=1),
            _rect(x + 38, y + 258, 8, 58, theme.accent),
            _text(
                x + 58,
                y + 282,
                "Art direction becomes credible when visual energy,",
                size=9,
                fill=theme.text,
                family=theme.body_font,
                role="caption",
                weight=700,
            ),
            _text(
                x + 58,
                y + 299,
                "evidence, and hierarchy are visible together.",
                size=9,
                fill=theme.text,
                family=theme.body_font,
                role="caption",
                weight=700,
            ),
            f'<circle cx="{x + 596}" cy="{y + 188}" r="146" fill="{theme.accent}" '
            f'stroke="#05070C" stroke-width="14"/>',
            f'<circle cx="{x + 596}" cy="{y + 188}" r="112" fill="#D81742" '
            f'stroke="#0A0D15" stroke-width="4"/>',
        ]
    )
    for angle_end in (
        (596, 46),
        (704, 94),
        (738, 198),
        (684, 302),
        (576, 330),
        (486, 278),
        (454, 170),
        (500, 76),
    ):
        parts.append(_line(x + 596, y + 188, x + angle_end[0], y + angle_end[1], "#0A0D15", 4))
    parts.extend(
        [
            f'<polygon points="{x + 596},{y + 82} {x + 682},{y + 136} {x + 654},{y + 262} '
            f'{x + 596},{y + 310} {x + 536},{y + 262} {x + 508},{y + 136}" '
            f'fill="#F7F8FC" stroke="#090C13" stroke-width="10"/>',
            f'<polygon points="{x + 596},{y + 106} {x + 650},{y + 144} {x + 626},{y + 224} '
            f'{x + 596},{y + 258}" fill="{theme.accent_2}"/>',
            f'<polygon points="{x + 596},{y + 106} {x + 542},{y + 144} {x + 566},{y + 224} '
            f'{x + 596},{y + 258}" fill="#DDE8F2"/>',
            _rect(x + 622, y + 276, 94, 72, "#0A0D15", stroke=theme.border, stroke_width=1),
            _text(x + 636, y + 296, "SIGNAL", size=10, fill=theme.muted, family=theme.body_font, role="label", weight=700),
            _text(x + 636, y + 327, "87%", size=24, fill=theme.text, family=theme.display_font, role="metric", weight=900),
        ]
    )
    for index, (label, value, fill) in enumerate(
        (("CASE", "#0716", theme.panel), ("STATUS", "ACTIVE", theme.accent), ("MODE", "URGENT", theme.surface))
    ):
        chip_x = x + 38 + index * 124
        parts.extend(
            [
                _rect(chip_x, y + 334, 110, 40, fill, stroke=theme.border, stroke_width=1),
                _text(chip_x + 10, y + 349, label, size=9, fill=theme.muted if index != 1 else "#FFFFFF", family=theme.body_font, role="annotation", weight=700),
                _text(chip_x + 10, y + 368, value, size=10, fill=theme.text if index != 1 else "#FFFFFF", family=theme.display_font, role="label", weight=900),
            ]
        )
    parts.append(
        _text(
            x + 554,
            y + 382,
            "ILLUSTRATIVE TEMPLATE · ORIGINAL ABSTRACT GRAPHICS",
            size=9,
            fill=theme.muted,
            family=theme.body_font,
            role="source",
            weight=700,
            anchor="middle",
        )
    )
    return parts


def _dynamic_hero_cover(theme: Theme, x: int, y: int) -> list[str]:
    parts = _panel_frame(theme, x, y, "01", theme.context)
    parts.extend(
        [
            f'<polygon points="{x + 22},{y + 108} {x + 398},{y + 62} {x + 444},{y + 235} '
            f'{x + 60},{y + 278}" fill="#070910" stroke="#02040A" stroke-width="12"/>',
            f'<polygon points="{x + 30},{y + 104} {x + 402},{y + 72} {x + 424},{y + 220} '
            f'{x + 50},{y + 260}" fill="#D70C37"/>',
            f'<polygon points="{x + 40},{y + 105} {x + 384},{y + 78} {x + 404},{y + 202} '
            f'{x + 66},{y + 241}" fill="#0A0D15"/>',
            f'<polygon points="{x + 18},{y + 76} {x + 246},{y + 54} {x + 236},{y + 96} '
            f'{x + 10},{y + 118}" fill="{theme.accent}" stroke="#02040A" stroke-width="4"/>',
            _text(x + 30, y + 92, "城市韧性行动档案", size=10, fill="#FFFFFF", family="Microsoft YaHei, Arial", role="label", weight=700),
            _text(x + 56, y + 166, "临界", size=54, fill="#02040A", family="Impact, Microsoft YaHei, Arial", role="deck-title", weight=900),
            _text(x + 49, y + 160, "临界", size=54, fill=theme.accent_2, family="Impact, Microsoft YaHei, Arial", role="deck-title", weight=900),
            _text(x + 45, y + 155, "临界", size=54, fill="#F8FAFF", family="Impact, Microsoft YaHei, Arial", role="deck-title", weight=900),
            _text(x + 112, y + 226, "时刻", size=62, fill="#02040A", family="Impact, Microsoft YaHei, Arial", role="deck-title", weight=900),
            _text(x + 105, y + 219, "时刻", size=62, fill=theme.accent_2, family="Impact, Microsoft YaHei, Arial", role="deck-title", weight=900),
            _text(x + 101, y + 213, "时刻", size=62, fill=theme.accent, family="Impact, Microsoft YaHei, Arial", role="deck-title", weight=900),
            f'<polygon points="{x + 224},{y + 240} {x + 410},{y + 226} {x + 402},{y + 254} {x + 228},{y + 266}" fill="#F8FAFF" stroke="#02040A" stroke-width="4"/>',
            _text(x + 244, y + 257, "CRITICAL RESPONSE ARCHIVE", size=10, fill="#090C13", family=theme.display_font, role="label", weight=900),
            _rect(x + 38, y + 282, 386, 52, "#080B12", stroke=theme.border, stroke_width=1),
            _rect(x + 38, y + 282, 8, 52, theme.accent),
            _text(x + 58, y + 302, "系统无法阻止所有意外，但可以让判断更快进入正确轨道。", size=9, fill=theme.text, family="Microsoft YaHei, Arial", role="caption", weight=700),
            _text(x + 58, y + 319, "视觉张力、事实证据与行动层级必须同时成立。", size=9, fill=theme.text, family="Microsoft YaHei, Arial", role="caption", weight=700),
            f'<circle cx="{x + 610}" cy="{y + 196}" r="162" fill="#04060B"/>',
            f'<circle cx="{x + 610}" cy="{y + 196}" r="146" fill="{theme.accent}" stroke="#05070C" stroke-width="8"/>',
            f'<circle cx="{x + 610}" cy="{y + 196}" r="116" fill="#B90B34" stroke="#0A0D15" stroke-width="5"/>',
            f'<circle cx="{x + 610}" cy="{y + 196}" r="72" fill="#101522" stroke="#F8FAFF" stroke-width="5"/>',
        ]
    )
    for angle_end in (
        (610, 40),
        (722, 86),
        (756, 196),
        (720, 306),
        (610, 352),
        (498, 306),
        (464, 196),
        (498, 86),
    ):
        parts.append(_line(x + 610, y + 196, x + angle_end[0], y + angle_end[1], "#0A0D15", 5))
    parts.extend(
        [
            f'<polygon points="{x + 610},{y + 112} {x + 676},{y + 152} {x + 652},{y + 246} '
            f'{x + 610},{y + 288} {x + 566},{y + 246} {x + 544},{y + 152}" fill="#F8FAFF" stroke="#05070C" stroke-width="8"/>',
            f'<polygon points="{x + 618},{y + 130} {x + 576},{y + 196} {x + 606},{y + 196} '
            f'{x + 590},{y + 252} {x + 650},{y + 178} {x + 620},{y + 178}" fill="{theme.accent_2}"/>',
            _text(x + 610, y + 327, "SIGNAL CORE", size=10, fill="#F8FAFF", family=theme.display_font, role="label", weight=900, anchor="middle"),
            _rect(x + 650, y + 282, 82, 74, "#090C13", stroke=theme.border, stroke_width=1),
            _text(x + 662, y + 302, "READINESS", size=10, fill=theme.muted, family=theme.body_font, role="label", weight=700),
            _text(x + 662, y + 333, "87%", size=24, fill=theme.text, family=theme.display_font, role="metric", weight=900),
            _text(x + 662, y + 348, "示例指标", size=9, fill=theme.accent, family="Microsoft YaHei, Arial", role="annotation", weight=700),
        ]
    )
    for index, (label, value, fill) in enumerate(
        (("CASE", "R-0716", theme.panel), ("STATUS", "ACTIVE", theme.accent), ("LEVEL", "CRITICAL", "#F8FAFF"))
    ):
        chip_x = x + 38 + index * 124
        parts.extend(
            [
                _rect(chip_x, y + 344, 110, 36, fill, stroke=theme.border, stroke_width=1),
                _text(chip_x + 10, y + 357, label, size=9, fill=theme.muted if index != 1 else "#FFFFFF", family=theme.body_font, role="annotation", weight=700),
                _text(chip_x + 10, y + 374, value, size=10, fill="#090C13" if index == 2 else "#FFFFFF" if index == 1 else theme.text, family=theme.display_font, role="label", weight=900),
            ]
        )
    parts.append(
        _text(
            x + 588,
            y + 386,
            "ILLUSTRATIVE TEMPLATE · ORIGINAL SIGNAL EMBLEM · REPLACE ALL SAMPLE DATA",
            size=9,
            fill=theme.muted,
            family=theme.body_font,
            role="source",
            weight=700,
            anchor="middle",
        )
    )
    return parts


def _artistic_cover_panel(theme: Theme, x: int, y: int) -> list[str]:
    parts = _panel_frame(theme, x, y, "01", theme.context)
    body = theme.body_font
    display = theme.hero_font or theme.display_font
    if theme.slug == "forest-poetic-mosaic":
        parts.extend(
            [
                _text(x + 36, y + 120, "林深处\n见新境", size=56, fill=theme.text, family=display, role="deck-title", weight=700, line_height=0.9),
                _text(x + 42, y + 242, "FOREST AS A NARRATIVE SYSTEM", size=14, fill="#273B33", family="Georgia, serif", role="subheading", weight=700),
                _text(x + 42, y + 278, "用留白建立信任，用场景切片建立记忆，", size=9, fill=theme.muted, family=body, role="body"),
                _text(x + 42, y + 298, "再让人物、证据与行动在同一叙事中汇合。", size=9, fill=theme.muted, family=body, role="body"),
                f'<polygon points="{x + 392},{y + 58} {x + 744},{y + 58} {x + 744},{y + 370} {x + 520},{y + 322}" fill="#184735"/>',
                f'<polygon points="{x + 498},{y + 58} {x + 744},{y + 58} {x + 744},{y + 208} {x + 638},{y + 250}" fill="#6E907D"/>',
                f'<polygon points="{x + 392},{y + 284} {x + 538},{y + 186} {x + 690},{y + 370} {x + 392},{y + 370}" fill="#0B513B"/>',
                _line(x + 516, y + 58, x + 700, y + 370, theme.panel, 7),
                _line(x + 392, y + 286, x + 632, y + 58, theme.panel, 7),
            ]
        )
        parts.extend(_tree_cluster(x + 432, y + 360, scale=0.34, colors=("#061E16", "#103326", "#214C3A"), count=22))
    elif theme.slug == "silk-ink-strategy":
        parts.extend(
            [
                _text(x + 380, y + 122, "青岚入卷", size=62, fill=theme.text, family=display, role="deck-title", weight=700, anchor="middle"),
                _text(x + 380, y + 166, "STRATEGY IN MOTION", size=14, fill="#333A36", family="Georgia, serif", role="subheading", weight=700, anchor="middle"),
                _text(x + 380, y + 198, "以山水建立文化识别，以证据支撑策略判断。", size=9, fill=theme.muted, family=body, role="body", anchor="middle"),
                f'<polygon points="{x},{y + 400} {x},{y + 310} {x + 104},{y + 252} {x + 212},{y + 326} {x + 318},{y + 236} {x + 424},{y + 326} {x + 536},{y + 242} {x + 650},{y + 320} {x + 760},{y + 268} {x + 760},{y + 400}" fill="#B9CAC2"/>',
                f'<polygon points="{x},{y + 400} {x},{y + 352} {x + 118},{y + 314} {x + 242},{y + 374} {x + 378},{y + 302} {x + 508},{y + 372} {x + 632},{y + 320} {x + 760},{y + 362} {x + 760},{y + 400}" fill="#477365"/>',
            ]
        )
        for offset in range(5):
            y_offset = offset * 10
            path = (
                f'M {x - 8},{y + 320 + y_offset} '
                f'C {x + 134},{y + 266 + y_offset} {x + 248},{y + 292 + y_offset} {x + 358},{y + 334 + y_offset} '
                f'S {x + 566},{y + 256 + y_offset} {x + 768},{y + 322 + y_offset}'
            )
            parts.append(f'<path d="{path}" fill="none" stroke="{theme.accent_2}" stroke-width="{7 - offset * 0.8:g}" opacity="{0.72 - offset * 0.08:g}"/>')
        parts.extend([_rect(x + 696, y + 50, 34, 34, "#A63A2E"), _text(x + 713, y + 74, "策", size=16, fill="#FFFFFF", family=display, role="quote", weight=700, anchor="middle")])
    else:
        parts.extend(
            [
                _text(x + 42, y + 118, "器物\n与时间", size=56, fill=theme.text, family=display, role="deck-title", weight=700, line_height=0.9),
                _text(x + 46, y + 242, "OBJECTS / MEMORY / PUBLIC MEANING", size=14, fill="#D8CABD", family="Georgia, serif", role="subheading", weight=700),
                _text(x + 46, y + 284, "从物证、时间、观点到公共行动，", size=9, fill=theme.muted, family=body, role="body"),
                _text(x + 46, y + 304, "让文化叙事不止于展示。", size=9, fill=theme.muted, family=body, role="body"),
                f'<circle cx="{x + 596}" cy="{y + 210}" r="138" fill="#372923" stroke="{theme.accent_2}" stroke-width="2"/>',
                f'<circle cx="{x + 596}" cy="{y + 210}" r="96" fill="#211816" stroke="#6E5548" stroke-width="10"/>',
                f'<polygon points="{x + 596},{y + 116} {x + 650},{y + 164} {x + 636},{y + 266} {x + 596},{y + 326} {x + 556},{y + 266} {x + 542},{y + 164}" fill="#A43B2F" stroke="#D2AD66" stroke-width="4"/>',
                f'<polygon points="{x + 596},{y + 142} {x + 626},{y + 174} {x + 618},{y + 244} {x + 596},{y + 286} {x + 574},{y + 244} {x + 566},{y + 174}" fill="#CBA158"/>',
            ]
        )
    parts.extend(
        [
            _text(x + 42, y + 374, "ILLUSTRATIVE TEMPLATE · ORIGINAL VECTOR ART DIRECTION", size=9, fill=theme.muted, family=body, role="source", weight=700),
            _text(x + 716, y + 374, "10-PAGE / FULL SYSTEM", size=9, fill=theme.accent_2, family=body, role="annotation", weight=700, anchor="end"),
        ]
    )
    return parts


def _cover(theme: Theme, x: int, y: int) -> list[str]:
    if theme.slug == "dynamic-hero-editorial":
        return _dynamic_hero_cover(theme, x, y)
    if theme.slug in {"forest-poetic-mosaic", "silk-ink-strategy", "museum-cultural-editorial"}:
        return _artistic_cover_panel(theme, x, y)
    parts = _panel_frame(theme, x, y, "01", theme.context)
    parts.extend(
        [
            _text(
                x + 34,
                y + 96,
                theme.cover_title,
                size=36,
                fill=theme.text,
                family=theme.display_font,
                role="deck-title",
                weight=700,
                line_height=1.04,
            ),
            _text(
                x + 34,
                y + 234,
                theme.cover_subtitle,
                size=9,
                fill=theme.muted,
                family=theme.body_font,
                role="caption",
                weight=400,
            ),
            _text(
                x + 34,
                y + 362,
                "ILLUSTRATIVE TEMPLATE · REPLACE WITH SOURCED CONTENT",
                size=9,
                fill=theme.muted,
                family=theme.body_font,
                role="source",
                weight=700,
            ),
        ]
    )
    for index, (value, label) in enumerate(theme.metrics):
        metric_x = x + 418 + index * 105
        parts.extend(
            [
                _rect(metric_x, y + 88, 92, 196, theme.surface, stroke=theme.border, stroke_width=1, radius=theme.radius),
                _text(
                    metric_x + 46,
                    y + 158,
                    value,
                    size=29,
                    fill=theme.accent if index == 0 else theme.text,
                    family=theme.display_font,
                    role="metric",
                    weight=700,
                    anchor="middle",
                ),
                _text(
                    metric_x + 46,
                    y + 186,
                    label,
                    size=9,
                    fill=theme.muted,
                    family=theme.body_font,
                    role="annotation",
                    weight=600,
                    anchor="middle",
                ),
                _line(metric_x + 18, y + 222, metric_x + 74, y + 222, theme.border, 2),
                _line(
                    metric_x + 18,
                    y + 244 - index * 5,
                    metric_x + 74,
                    y + 214 + index * 8,
                    theme.accent_2,
                    4,
                ),
            ]
        )
    for index, label in enumerate(("CLAIM", "PROOF", "ACTION")):
        chip_x = x + 34 + index * 112
        parts.extend(
            [
                _rect(chip_x, y + 286, 98, 34, theme.surface, stroke=theme.border, stroke_width=1, radius=17),
                _text(
                    chip_x + 49,
                    y + 308,
                    label,
                    size=10,
                    fill=theme.text,
                    family=theme.body_font,
                    role="label",
                    weight=700,
                    anchor="middle",
                ),
            ]
        )
    return parts


def _dynamic_hero_workflow(theme: Theme, x: int, y: int, page: str = "02") -> list[str]:
    parts = _panel_frame(theme, x, y, page, "OPERATING MODEL")
    parts.extend(
        [
            _text(
                x + 34,
                y + 82,
                "FIVE MOVES BUILD MOMENTUM",
                size=26,
                fill=theme.text,
                family=theme.display_font,
                role="slide-title",
                weight=700,
            ),
            _text(
                x + 34,
                y + 110,
                "A staggered sequence keeps each decision, handoff, and quality gate visible.",
                size=9,
                fill=theme.muted,
                family=theme.body_font,
                role="caption",
            ),
        ]
    )
    offsets = (12, -4, 18, 2, 14)
    for index, (name, description) in enumerate(theme.steps):
        step_x = x + 34 + index * 138
        step_y = y + 146 + offsets[index]
        fill = theme.accent if index == 0 else theme.surface
        text_fill = "#FFFFFF" if index == 0 else theme.text
        parts.extend(
            [
                f'<polygon points="{step_x},{step_y + 10} {step_x + 112},{step_y} '
                f'{step_x + 126},{step_y + 140} {step_x + 14},{step_y + 152}" '
                f'fill="{fill}" stroke="{theme.border}" stroke-width="1"/>',
                _text(
                    step_x + 18,
                    step_y + 40,
                    f"0{index + 1}",
                    size=20,
                    fill=text_fill if index == 0 else (theme.accent if index < 3 else theme.accent_2),
                    family=theme.display_font,
                    role="metric",
                    weight=700,
                ),
                _text(
                    step_x + 18,
                    step_y + 72,
                    name,
                    size=14,
                    fill=text_fill,
                    family=theme.body_font,
                    role="subheading",
                    weight=700,
                ),
                _text(
                    step_x + 18,
                    step_y + 98,
                    description.replace(", ", "\n").replace(" and ", "\nand "),
                    size=9,
                    fill="#FFFFFF" if index == 0 else theme.muted,
                    family=theme.body_font,
                    role="body",
                    line_height=1.35,
                ),
            ]
        )
        if index < 4:
            parts.append(
                _line(step_x + 124, step_y + 76, step_x + 146, y + 222 + offsets[index + 1], theme.accent, 3)
            )
    parts.extend(
        [
            f'<polygon points="{x + 34},{y + 336} {x + 704},{y + 314} '
            f'{x + 720},{y + 362} {x + 48},{y + 378}" fill="#090C13" '
            f'stroke="{theme.accent}" stroke-width="2"/>',
            _text(x + 64, y + 354, "QUALITY GATE", size=10, fill=theme.accent, family=theme.body_font, role="label", weight=700),
            _text(
                x + 186,
                y + 350,
                "Advance only when evidence, owner, and acceptance are explicit.",
                size=9,
                fill=theme.text,
                family=theme.body_font,
                role="caption",
            ),
        ]
    )
    return parts


def _workflow(theme: Theme, x: int, y: int, page: str = "02") -> list[str]:
    if theme.slug == "dynamic-hero-editorial":
        return _dynamic_hero_process(theme, x, y, page)
    parts = _panel_frame(theme, x, y, page, "OPERATING MODEL")
    parts.extend(
        [
            _text(
                x + 34,
                y + 82,
                "Five moves create an accountable delivery loop",
                size=26,
                fill=theme.text,
                family=theme.display_font,
                role="slide-title",
                weight=700,
            ),
            _text(
                x + 34,
                y + 110,
                "Each phase produces a decision-ready artifact and a visible quality gate.",
                size=9,
                fill=theme.muted,
                family=theme.body_font,
                role="caption",
            ),
        ]
    )
    for index, (name, description) in enumerate(theme.steps):
        step_x = x + 34 + index * 140
        parts.extend(
            [
                _rect(step_x, y + 142, 126, 156, theme.surface, stroke=theme.border, stroke_width=1, radius=theme.radius),
                _text(
                    step_x + 16,
                    y + 174,
                    f"0{index + 1}",
                    size=20,
                    fill=theme.accent if index < 3 else theme.accent_2,
                    family=theme.display_font,
                    role="metric",
                    weight=700,
                ),
                _text(
                    step_x + 16,
                    y + 208,
                    name,
                    size=14,
                    fill=theme.text,
                    family=theme.body_font,
                    role="subheading",
                    weight=700,
                ),
                _text(
                    step_x + 16,
                    y + 234,
                    description.replace(" and ", "\nand "),
                    size=9,
                    fill=theme.muted,
                    family=theme.body_font,
                    role="body",
                    line_height=1.35,
                ),
            ]
        )
        if index < 4:
            parts.append(_line(step_x + 126, y + 220, step_x + 140, y + 220, theme.accent, 2))
    parts.extend(
        [
            _rect(x + 34, y + 320, 686, 48, theme.surface, stroke=theme.border, stroke_width=1, radius=theme.radius),
            _text(
                x + 54,
                y + 350,
                "QUALITY GATE",
                size=10,
                fill=theme.accent,
                family=theme.body_font,
                role="label",
                weight=700,
            ),
            _text(
                x + 170,
                y + 350,
                "No phase advances until its evidence, owner, and acceptance condition are explicit.",
                size=9,
                fill=theme.text,
                family=theme.body_font,
                role="caption",
            ),
        ]
    )
    return parts


def _dynamic_hero_title_panel(
    theme: Theme,
    x: int,
    y: int,
    *,
    page: str,
    section: str,
    title: str,
    caption: str,
) -> list[str]:
    parts = _panel_frame(theme, x, y, page, section)
    parts.extend(
        [
            _rect(x + 34, y + 54, 44, 5, theme.accent),
            _text(x + 34, y + 88, title, size=26, fill=theme.text, family="Impact, Microsoft YaHei, Arial", role="slide-title", weight=900),
            _text(x + 34, y + 116, caption, size=9, fill=theme.muted, family="Microsoft YaHei, Arial", role="caption"),
        ]
    )
    return parts


def _dynamic_hero_section(theme: Theme, x: int, y: int) -> list[str]:
    parts = _panel_frame(theme, x, y, "02", "CHAPTER / RESPONSE LOGIC")
    parts.extend(
        [
            _text(x + 24, y + 178, "02", size=118, fill="#260815", family=theme.display_font, role="metric", weight=900),
            _text(x + 174, y + 151, "先看见风险", size=47, fill="#02040A", family="Impact, Microsoft YaHei, Arial", role="deck-title", weight=900),
            _text(x + 168, y + 145, "先看见风险", size=47, fill=theme.accent_2, family="Impact, Microsoft YaHei, Arial", role="deck-title", weight=900),
            _text(x + 164, y + 140, "先看见风险", size=47, fill="#F8FAFF", family="Impact, Microsoft YaHei, Arial", role="deck-title", weight=900),
            _text(x + 234, y + 207, "再决定行动", size=47, fill="#02040A", family="Impact, Microsoft YaHei, Arial", role="deck-title", weight=900),
            _text(x + 228, y + 201, "再决定行动", size=47, fill=theme.accent_2, family="Impact, Microsoft YaHei, Arial", role="deck-title", weight=900),
            _text(x + 224, y + 196, "再决定行动", size=47, fill=theme.accent, family="Impact, Microsoft YaHei, Arial", role="deck-title", weight=900),
            _text(x + 170, y + 240, "章节任务：把散乱信号组织成可解释、可验证、可负责的响应链。", size=14, fill=theme.text, family="Microsoft YaHei, Arial", role="subheading", weight=700),
            _text(x + 170, y + 270, "英雄式视觉负责建立记忆点；事实、来源与行动条件负责建立可信度。", size=9, fill=theme.muted, family="Microsoft YaHei, Arial", role="body"),
        ]
    )
    for index, (number, label, note) in enumerate(
        (("01", "识别", "看见真正信号"), ("02", "解释", "建立因果关系"), ("03", "决策", "明确下一动作"))
    ):
        chip_x = x + 170 + index * 166
        parts.extend(
            [
                f'<polygon points="{chip_x},{y + 300} {chip_x + 146},{y + 286} {chip_x + 154},{y + 354} {chip_x + 8},{y + 366}" fill="{theme.accent if index == 0 else theme.surface}" stroke="{theme.border}" stroke-width="1"/>',
                _text(chip_x + 16, y + 318, number, size=10, fill="#FFFFFF" if index == 0 else theme.accent, family=theme.display_font, role="label", weight=900),
                _text(chip_x + 16, y + 340, label, size=14, fill="#FFFFFF" if index == 0 else theme.text, family="Microsoft YaHei, Arial", role="subheading", weight=700),
                _text(chip_x + 62, y + 340, note, size=9, fill="#FFFFFF" if index == 0 else theme.muted, family="Microsoft YaHei, Arial", role="body"),
            ]
        )
    return parts


def _dynamic_hero_narrative(theme: Theme, x: int, y: int) -> list[str]:
    parts = _dynamic_hero_title_panel(
        theme,
        x,
        y,
        page="03",
        section="NARRATIVE / INCIDENT STORY",
        title="一条可信叙事必须完成三次推进",
        caption="从具体现场进入问题，用可追溯证据解释机制，再把意义收束为下一步行动。",
    )
    parts.extend(
        [
            _rect(x + 34, y + 144, 382, 208, "#090C13", stroke=theme.border, stroke_width=1),
            f'<polygon points="{x + 34},{y + 352} {x + 34},{y + 268} {x + 94},{y + 226} {x + 148},{y + 266} {x + 214},{y + 206} {x + 286},{y + 258} {x + 350},{y + 196} {x + 416},{y + 244} {x + 416},{y + 352}" fill="#1A2030"/>',
            f'<polygon points="{x + 34},{y + 352} {x + 34},{y + 318} {x + 126},{y + 276} {x + 210},{y + 332} {x + 306},{y + 282} {x + 416},{y + 320} {x + 416},{y + 352}" fill="#B30B34"/>',
            _line(x + 58, y + 176, x + 374, y + 304, theme.accent, 3),
            _line(x + 72, y + 294, x + 362, y + 180, theme.accent_2, 2),
            _text(x + 54, y + 176, "现场不是背景", size=14, fill=theme.text, family="Microsoft YaHei, Arial", role="subheading", weight=700),
            _text(x + 54, y + 198, "它必须显示人物、压力、时间窗口与真实约束。", size=9, fill=theme.muted, family="Microsoft YaHei, Arial", role="body"),
            _rect(x + 54, y + 304, 300, 32, "#080B12", stroke=theme.accent, stroke_width=1),
            _text(x + 70, y + 324, "观察 → 证据 → 含义", size=10, fill=theme.accent, family="Microsoft YaHei, Arial", role="label", weight=700),
        ]
    )
    for index, (title, body, accent) in enumerate(
        (
            ("场景", "谁在何处遭遇什么阻力？\n先让受众进入具体问题。", theme.accent),
            ("证据", "哪些记录、数据或引语\n能够验证这个判断？", theme.accent_2),
            ("意义", "这项发现改变哪项选择，\n谁必须负责下一步？", theme.warning),
        )
    ):
        item_y = y + 146 + index * 74
        parts.extend(
            [
                f'<polygon points="{x + 446},{item_y} {x + 708},{item_y - 8} {x + 720},{item_y + 58} {x + 456},{item_y + 66}" fill="{theme.surface}" stroke="{theme.border}" stroke-width="1"/>',
                _text(x + 464, item_y + 22, f"0{index + 1}", size=10, fill=accent, family=theme.display_font, role="label", weight=900),
                _text(x + 510, item_y + 24, title, size=14, fill=theme.text, family="Microsoft YaHei, Arial", role="subheading", weight=700),
                _text(x + 572, item_y + 18, body, size=9, fill=theme.muted, family="Microsoft YaHei, Arial", role="body", line_height=1.35),
            ]
        )
    parts.extend(
        [
            _text(x + 448, y + 372, "“情绪建立关注，证据建立信任，行动建立价值。”", size=14, fill=theme.text, family="Microsoft YaHei, Arial", role="quote", weight=700),
            _text(x + 708, y + 348, "示例叙事结构 · 请替换为真实现场与来源", size=9, fill=theme.muted, family="Microsoft YaHei, Arial", role="annotation", anchor="end"),
        ]
    )
    return parts


def _dynamic_hero_context(theme: Theme, x: int, y: int) -> list[str]:
    parts = _dynamic_hero_title_panel(
        theme,
        x,
        y,
        page="04",
        section="CONTEXT / PRESSURE MAP",
        title="三个失配，让响应窗口不断收窄",
        caption="把表面症状拆成信号、权责与反馈三个机制问题，再说明它们如何共同放大风险。",
    )
    for index, (name, body) in enumerate(
        (("信号失配", "信息分散在多个入口，\n关键变化无法被及时识别。"), ("权责失配", "判断权、执行权与复核权\n没有落在同一条责任链。"), ("反馈失配", "结果回传缺少统一格式，\n经验无法进入下一轮决策。"))
    ):
        item_y = y + 144 + index * 72
        parts.extend(
            [
                f'<polygon points="{x + 34},{item_y} {x + 270},{item_y - 10} {x + 286},{item_y + 52} {x + 46},{item_y + 64}" fill="{theme.accent if index == 0 else theme.surface}" stroke="{theme.border}" stroke-width="1"/>',
                _text(x + 52, item_y + 22, f"0{index + 1}", size=10, fill="#FFFFFF" if index == 0 else theme.accent, family=theme.display_font, role="label", weight=900),
                _text(x + 92, item_y + 24, name, size=14, fill="#FFFFFF" if index == 0 else theme.text, family="Microsoft YaHei, Arial", role="subheading", weight=700),
                _text(x + 166, item_y + 16, body, size=9, fill="#FFFFFF" if index == 0 else theme.muted, family="Microsoft YaHei, Arial", role="body", line_height=1.35),
            ]
        )
        parts.append(_line(x + 286, item_y + 26, x + 350, y + 236, theme.accent, 2))
    parts.extend(
        [
            f'<circle cx="{x + 392}" cy="{y + 236}" r="72" fill="#070910" stroke="{theme.accent}" stroke-width="7"/>',
            _text(x + 392, y + 220, "24h", size=40, fill=theme.text, family=theme.display_font, role="metric", weight=900, anchor="middle"),
            _text(x + 392, y + 246, "示例响应窗口", size=10, fill=theme.accent_2, family="Microsoft YaHei, Arial", role="label", weight=700, anchor="middle"),
            _text(x + 392, y + 268, "需替换为真实事实", size=9, fill=theme.muted, family="Microsoft YaHei, Arial", role="annotation", anchor="middle"),
        ]
    )
    for index, (title, body, color) in enumerate(
        (("判断变慢", "关键证据到达时已经错过最佳窗口。", theme.accent), ("协同变贵", "团队重复核对，却仍无法形成共同事实。", theme.warning), ("复盘失真", "结果只被记录，没有转化为下一轮规则。", theme.accent_2))
    ):
        item_y = y + 150 + index * 70
        parts.extend(
            [
                _rect(x + 496, item_y, 224, 56, "#101622", stroke=theme.border, stroke_width=1),
                _rect(x + 496, item_y, 7, 56, color),
                _text(x + 518, item_y + 22, title, size=14, fill=theme.text, family="Microsoft YaHei, Arial", role="subheading", weight=700),
                _text(x + 518, item_y + 42, body, size=9, fill=theme.muted, family="Microsoft YaHei, Arial", role="body"),
            ]
        )
    parts.extend(
        [
            f'<polygon points="{x + 34},{y + 364} {x + 698},{y + 346} {x + 720},{y + 382} {x + 50},{y + 396}" fill="#080B12" stroke="{theme.accent}" stroke-width="2"/>',
            _text(x + 58, y + 382, "关键判断", size=10, fill=theme.accent, family="Microsoft YaHei, Arial", role="label", weight=700),
            _text(x + 142, y + 381, "真正要优化的不是‘传得更快’，而是让信号、责任与反馈在同一条链上闭环。", size=9, fill=theme.text, family="Microsoft YaHei, Arial", role="annotation"),
        ]
    )
    return parts


def _dynamic_hero_process(theme: Theme, x: int, y: int, page: str = "05") -> list[str]:
    parts = _dynamic_hero_title_panel(
        theme,
        x,
        y,
        page=page,
        section="OPERATING MODEL / FIVE MOVES",
        title="五个动作，把警报变成可执行响应",
        caption="每一步都产出一个可验证对象，并在进入下一阶段前明确负责人、证据与通过条件。",
    )
    steps = (
        ("01", "定界", "确认问题\n与成功信号", "OWNER · LEAD"),
        ("02", "取证", "提取事实\n与关键约束", "OUTPUT · BRIEF"),
        ("03", "判断", "选择最清晰\n的解释框架", "GATE · REVIEW"),
        ("04", "复核", "验证事实、\n视觉与风险", "PROOF · RECORD"),
        ("05", "行动", "锁定责任人\n与下一节点", "NEXT · OWNER"),
    )
    offsets = (8, -6, 12, -2, 10)
    for index, (number, title, body, meta) in enumerate(steps):
        card_x = x + 34 + index * 138
        card_y = y + 154 + offsets[index]
        fill = theme.accent if index == 0 else "#151B27"
        parts.extend(
            [
                f'<polygon points="{card_x},{card_y} {card_x + 118},{card_y - 10} {card_x + 130},{card_y + 164} {card_x + 12},{card_y + 176}" fill="{fill}" stroke="{theme.border}" stroke-width="1"/>',
                _text(card_x + 18, card_y + 34, number, size=24, fill="#FFFFFF" if index == 0 else theme.accent if index < 3 else theme.accent_2, family=theme.display_font, role="metric", weight=900),
                _text(card_x + 18, card_y + 66, title, size=14, fill=theme.text, family="Microsoft YaHei, Arial", role="subheading", weight=700),
                _text(card_x + 18, card_y + 96, body, size=9, fill="#FFFFFF" if index == 0 else theme.muted, family="Microsoft YaHei, Arial", role="body", line_height=1.35),
                _text(card_x + 18, card_y + 148, meta, size=9, fill="#FFFFFF" if index == 0 else theme.muted, family=theme.body_font, role="annotation", weight=700),
            ]
        )
        if index < len(steps) - 1:
            parts.append(_line(card_x + 128, card_y + 84, card_x + 146, y + 238 + offsets[index + 1], theme.accent, 3))
    parts.extend(
        [
            f'<polygon points="{x + 34},{y + 354} {x + 704},{y + 338} {x + 720},{y + 382} {x + 48},{y + 396}" fill="#080B12" stroke="{theme.accent}" stroke-width="2"/>',
            _text(x + 62, y + 376, "QUALITY GATE", size=10, fill=theme.accent, family=theme.body_font, role="label", weight=700),
            _text(x + 190, y + 375, "证据、责任人、验收条件三项缺一，流程不得进入下一阶段。", size=9, fill=theme.text, family="Microsoft YaHei, Arial", role="annotation"),
        ]
    )
    return parts


def _dynamic_hero_evidence(theme: Theme, x: int, y: int, page: str = "06") -> list[str]:
    parts = _dynamic_hero_title_panel(
        theme,
        x,
        y,
        page=page,
        section="EVIDENCE / SIGNAL BOARD",
        title="证据不是装饰：它必须改变下一步判断",
        caption="以下数字仅用于演示信息层级；实际使用时必须替换为可追溯的真实数据、单位、时间和来源。",
    )
    metrics = (("87%", "示例就绪度", "复核标准明确后，信号强度上升"), ("04", "关键窗口", "需要人工确认的高风险节点"), ("24h", "响应周期", "从识别到责任人确认的示例时间"))
    for index, (value, label, note) in enumerate(metrics):
        metric_y = y + 154 + index * 68
        parts.extend(
            [
                _text(x + 34, metric_y + 24, value, size=28, fill=theme.accent if index == 0 else theme.text, family=theme.display_font, role="metric", weight=900),
                _text(x + 128, metric_y + 16, label, size=10, fill=theme.text, family="Microsoft YaHei, Arial", role="label", weight=700),
                _text(x + 128, metric_y + 38, note, size=9, fill=theme.muted, family="Microsoft YaHei, Arial", role="annotation"),
                _line(x + 34, metric_y + 54, x + 272, metric_y + 54, theme.border, 1),
            ]
        )
    chart_x, chart_y = x + 306, y + 148
    parts.extend(
        [
            _rect(chart_x, chart_y, 414, 174, "#121824", stroke=theme.border, stroke_width=1),
            _text(chart_x + 18, chart_y + 28, "RESPONSE SIGNAL · INDEXED EXAMPLE", size=10, fill=theme.text, family=theme.body_font, role="label", weight=700),
            _text(chart_x + 396, chart_y + 28, "BASE 100", size=9, fill=theme.muted, family=theme.body_font, role="annotation", weight=700, anchor="end"),
        ]
    )
    for index in range(4):
        parts.append(_line(chart_x + 18, chart_y + 54 + index * 30, chart_x + 396, chart_y + 54 + index * 30, theme.border, 1))
    points = [(chart_x + 24, chart_y + 142), (chart_x + 82, chart_y + 126), (chart_x + 140, chart_y + 134), (chart_x + 202, chart_y + 96), (chart_x + 264, chart_y + 84), (chart_x + 326, chart_y + 52), (chart_x + 388, chart_y + 40)]
    parts.append(f'<polyline points="{" ".join(f"{px:g},{py:g}" for px, py in points)}" fill="none" stroke="{theme.accent}" stroke-width="5"/>')
    for px, py in points:
        parts.append(f'<circle cx="{px:g}" cy="{py:g}" r="5" fill="{theme.accent}"/>')
    parts.extend(
        [
            _rect(x + 306, y + 340, 414, 46, "#080B12", stroke=theme.border, stroke_width=1),
            _text(x + 324, y + 360, "INTERPRETATION", size=10, fill=theme.accent_2, family=theme.body_font, role="label", weight=700),
            _text(x + 430, y + 354, "责任人与复核条件同时明确，\n响应信号出现最大改善。", size=9, fill=theme.text, family="Microsoft YaHei, Arial", role="annotation", line_height=1.25),
            _text(x + 324, y + 378, "SOURCE / PERIOD", size=10, fill=theme.warning, family=theme.body_font, role="label", weight=700),
            _text(x + 430, y + 378, "补充真实来源、统计口径、样本范围与时间区间。", size=9, fill=theme.muted, family="Microsoft YaHei, Arial", role="annotation"),
        ]
    )
    return parts


def _dynamic_hero_comparison(theme: Theme, x: int, y: int, page: str = "07") -> list[str]:
    parts = _dynamic_hero_title_panel(
        theme,
        x,
        y,
        page=page,
        section="COMPARISON / TWO RESPONSE MODES",
        title="同一事件，两种组织方式产生完全不同的结果",
        caption="共享同一比较基线：信号入口、判断机制、责任归属和结果回传；示例文案需替换为项目事实。",
    )
    parts.extend(
        [
            f'<polygon points="{x + 34},{y + 146} {x + 354},{y + 132} {x + 330},{y + 358} {x + 34},{y + 372}" fill="#141A26" stroke="{theme.border}" stroke-width="1"/>',
            f'<polygon points="{x + 372},{y + 132} {x + 720},{y + 146} {x + 720},{y + 372} {x + 348},{y + 358}" fill="#0B2630" stroke="{theme.accent_2}" stroke-width="2"/>',
            _text(x + 58, y + 178, "传统响应", size=14, fill=theme.accent, family="Microsoft YaHei, Arial", role="subheading", weight=700),
            _text(x + 396, y + 178, "可视化响应", size=14, fill=theme.accent_2, family="Microsoft YaHei, Arial", role="subheading", weight=700),
            _text(x + 58, y + 202, "依赖个人经验与临时沟通", size=9, fill=theme.muted, family="Microsoft YaHei, Arial", role="body"),
            _text(x + 396, y + 202, "依赖共享证据与明确质量门", size=9, fill=theme.muted, family="Microsoft YaHei, Arial", role="body"),
        ]
    )
    comparisons = (("信号入口", "多个渠道，口径不一", "单一记录，保留来源"), ("判断机制", "先讨论，再寻找证据", "先证据，再形成结论"), ("责任归属", "依赖临时协调", "逐阶段指定负责人"), ("结果回传", "结论停留在会议", "结论进入规则与复盘"))
    for index, (criterion, left, right) in enumerate(comparisons):
        row_y = y + 236 + index * 32
        parts.extend(
            [
                _text(x + 58, row_y, criterion, size=10, fill=theme.text, family="Microsoft YaHei, Arial", role="label", weight=700),
                _text(x + 156, row_y, left, size=9, fill=theme.muted, family="Microsoft YaHei, Arial", role="annotation"),
                _text(x + 396, row_y, criterion, size=10, fill=theme.text, family="Microsoft YaHei, Arial", role="label", weight=700),
                _text(x + 494, row_y, right, size=9, fill=theme.text, family="Microsoft YaHei, Arial", role="annotation"),
                _line(x + 58, row_y + 10, x + 322, row_y + 10, theme.border, 1),
                _line(x + 396, row_y + 10, x + 690, row_y + 10, "#285266", 1),
            ]
        )
    parts.extend(
        [
            f'<polygon points="{x + 320},{y + 138} {x + 376},{y + 132} {x + 348},{y + 366} {x + 296},{y + 372}" fill="{theme.accent}"/>',
            _text(x + 348, y + 266, "VS", size=24, fill="#FFFFFF", family=theme.display_font, role="metric", weight=900, anchor="middle"),
            _text(x + 382, y + 392, "结论：高张力视觉必须服务于更清楚的比较，而不是掩盖比较。", size=9, fill=theme.text, family="Microsoft YaHei, Arial", role="caption", anchor="middle"),
        ]
    )
    return parts


def _dynamic_hero_roadmap(theme: Theme, x: int, y: int) -> list[str]:
    parts = _dynamic_hero_title_panel(
        theme,
        x,
        y,
        page="08",
        section="ROADMAP / READINESS PATH",
        title="四个阶段，逐步把不确定性压缩成行动",
        caption="路线图不仅写时间，还要同时写清产出、负责人、验证信号和进入下一阶段的条件。",
    )
    phases = (
        ("01", "校准", "统一问题与口径", "产出：事件简报", "负责人：策略"),
        ("02", "取证", "补齐事实与边界", "产出：证据清单", "负责人：研究"),
        ("03", "试行", "验证流程与责任", "产出：响应记录", "负责人：运营"),
        ("04", "固化", "进入规则与复盘", "产出：行动标准", "负责人：管理层"),
    )
    parts.append(_line(x + 74, y + 274, x + 690, y + 188, theme.accent, 5))
    for index, (number, title, body, output, owner) in enumerate(phases):
        card_x = x + 46 + index * 166
        card_y = y + 176 - index * 20
        parts.extend(
            [
                f'<polygon points="{card_x},{card_y} {card_x + 144},{card_y - 10} {card_x + 154},{card_y + 150} {card_x + 10},{card_y + 160}" fill="{theme.accent if index == 0 else theme.surface}" stroke="{theme.border}" stroke-width="1"/>',
                _text(card_x + 18, card_y + 30, number, size=24, fill="#FFFFFF" if index == 0 else theme.accent_2, family=theme.display_font, role="metric", weight=900),
                _text(card_x + 18, card_y + 60, title, size=14, fill=theme.text, family="Microsoft YaHei, Arial", role="subheading", weight=700),
                _text(card_x + 18, card_y + 84, body, size=9, fill="#FFFFFF" if index == 0 else theme.muted, family="Microsoft YaHei, Arial", role="body"),
                _text(card_x + 18, card_y + 112, output, size=9, fill="#FFFFFF" if index == 0 else theme.text, family="Microsoft YaHei, Arial", role="annotation", weight=700),
                _text(card_x + 18, card_y + 134, owner, size=9, fill="#FFFFFF" if index == 0 else theme.muted, family="Microsoft YaHei, Arial", role="annotation"),
            ]
        )
    parts.extend(
        [
            _rect(x + 48, y + 356, 672, 32, "#080B12", stroke=theme.border, stroke_width=1),
            _text(x + 64, y + 377, "READINESS CHECK", size=10, fill=theme.accent, family=theme.body_font, role="label", weight=700),
            _text(x + 188, y + 376, "每个阶段必须保留来源、决策、负责人和下一次验证时间，才能形成真正的可追溯闭环。", size=9, fill=theme.text, family="Microsoft YaHei, Arial", role="annotation"),
        ]
    )
    return parts


def _dynamic_hero_synthesis(theme: Theme, x: int, y: int, page: str = "09") -> list[str]:
    parts = _dynamic_hero_title_panel(
        theme,
        x,
        y,
        page=page,
        section="DECISION / PRIORITY FIELD",
        title="优先处理能同时提升速度、可信度和协同的动作",
        caption="把建议放在价值、置信度、依赖与责任的共同坐标中，明确现在做什么、暂缓什么、如何验证。",
    )
    for index, (name, owner, note, color) in enumerate(
        (("锁定事件简报", "负责人：策略 · 现在", "统一问题、来源与成功信号", theme.accent), ("建立复核记录", "负责人：运营 · 第 1 天", "保留修改、意见与决策依据", theme.accent_2), ("固化行动标准", "负责人：管理层 · 第 2 天", "把结果进入规则与下一轮训练", theme.warning))
    ):
        row_y = y + 148 + index * 68
        parts.extend(
            [
                f'<polygon points="{x + 34},{row_y} {x + 410},{row_y - 8} {x + 418},{row_y + 52} {x + 42},{row_y + 60}" fill="#151B27" stroke="{theme.border}" stroke-width="1"/>',
                _rect(x + 34, row_y, 8, 60, color),
                _text(x + 58, row_y + 22, name, size=14, fill=theme.text, family="Microsoft YaHei, Arial", role="subheading", weight=700),
                _text(x + 58, row_y + 42, owner, size=9, fill=theme.muted, family="Microsoft YaHei, Arial", role="annotation"),
                _text(x + 222, row_y + 42, note, size=9, fill=theme.text, family="Microsoft YaHei, Arial", role="body"),
                _text(x + 390, row_y + 30, f"0{index + 1}", size=18, fill=color, family=theme.display_font, role="metric", weight=900, anchor="end"),
            ]
        )
    matrix_x, matrix_y = x + 450, y + 148
    parts.extend(
        [
            _text(matrix_x, matrix_y - 12, "VALUE / CONFIDENCE", size=10, fill=theme.text, family=theme.body_font, role="label", weight=700),
            _rect(matrix_x, matrix_y, 270, 206, "#151B27", stroke=theme.border, stroke_width=1),
            _line(matrix_x + 135, matrix_y + 12, matrix_x + 135, matrix_y + 194, theme.border, 1),
            _line(matrix_x + 12, matrix_y + 103, matrix_x + 258, matrix_y + 103, theme.border, 1),
            _text(matrix_x + 20, matrix_y + 30, "探索", size=10, fill=theme.muted, family="Microsoft YaHei, Arial", role="label", weight=700),
            _text(matrix_x + 158, matrix_y + 30, "规模化", size=10, fill=theme.positive, family="Microsoft YaHei, Arial", role="label", weight=700),
            _text(matrix_x + 20, matrix_y + 132, "暂缓", size=10, fill=theme.muted, family="Microsoft YaHei, Arial", role="label", weight=700),
            _text(matrix_x + 158, matrix_y + 132, "验证", size=10, fill=theme.warning, family="Microsoft YaHei, Arial", role="label", weight=700),
            f'<circle cx="{matrix_x + 202}" cy="{matrix_y + 68}" r="22" fill="{theme.positive}"/>',
            f'<circle cx="{matrix_x + 178}" cy="{matrix_y + 164}" r="14" fill="{theme.warning}"/>',
            f'<circle cx="{matrix_x + 84}" cy="{matrix_y + 74}" r="11" fill="{theme.accent}"/>',
            _rect(x + 34, y + 366, 686, 22, theme.accent, radius=0),
            _text(x + 377, y + 382, "ONE DECISION · THREE OWNERS · ONE VISIBLE NEXT MILESTONE", size=9, fill="#FFFFFF", family=theme.body_font, role="source", weight=700, anchor="middle"),
        ]
    )
    return parts


def _dynamic_hero_closing(theme: Theme, x: int, y: int, page: str = "10") -> list[str]:
    parts = _panel_frame(theme, x, y, page, "RESOLUTION / ACTION")
    parts.extend(
        [
            f'<polygon points="{x + 28},{y + 90} {x + 444},{y + 54} {x + 468},{y + 252} {x + 62},{y + 286}" fill="#D70C37" stroke="#02040A" stroke-width="10"/>',
            f'<polygon points="{x + 44},{y + 96} {x + 428},{y + 66} {x + 450},{y + 234} {x + 70},{y + 268}" fill="#090C13"/>',
            _text(x + 78, y + 142, "让每一次", size=38, fill="#02040A", family="Impact, Microsoft YaHei, Arial", role="deck-title", weight=900),
            _text(x + 72, y + 136, "让每一次", size=38, fill="#F8FAFF", family="Impact, Microsoft YaHei, Arial", role="deck-title", weight=900),
            _text(x + 112, y + 202, "临界时刻", size=52, fill="#02040A", family="Impact, Microsoft YaHei, Arial", role="deck-title", weight=900),
            _text(x + 106, y + 196, "临界时刻", size=52, fill=theme.accent, family="Impact, Microsoft YaHei, Arial", role="deck-title", weight=900),
            _text(x + 180, y + 246, "都有答案", size=38, fill=theme.accent_2, family="Impact, Microsoft YaHei, Arial", role="deck-title", weight=900),
            _text(x + 66, y + 312, "结束页要把整套叙事收束成一个判断、一个负责人和一个可见的下一节点。", size=14, fill=theme.text, family="Microsoft YaHei, Arial", role="subheading", weight=700),
            _text(x + 66, y + 340, "高张力不是终点；让受众记住并采取正确行动，才是视觉系统的最终任务。", size=9, fill=theme.muted, family="Microsoft YaHei, Arial", role="body"),
            f'<circle cx="{x + 610}" cy="{y + 198}" r="142" fill="#04060B"/>',
            f'<circle cx="{x + 610}" cy="{y + 198}" r="124" fill="{theme.accent}" stroke="#05070C" stroke-width="7"/>',
            f'<circle cx="{x + 610}" cy="{y + 198}" r="88" fill="#121824" stroke="#F8FAFF" stroke-width="5"/>',
            f'<polygon points="{x + 618},{y + 122} {x + 568},{y + 198} {x + 606},{y + 198} {x + 588},{y + 272} {x + 658},{y + 178} {x + 620},{y + 178}" fill="{theme.accent_2}"/>',
            _text(x + 610, y + 318, "READY TO ACT", size=18, fill=theme.text, family=theme.display_font, role="metric", weight=900, anchor="middle"),
            _text(x + 720, y + 348, "ILLUSTRATIVE TEMPLATE · ORIGINAL SIGNAL EMBLEM", size=9, fill=theme.muted, family=theme.body_font, role="source", weight=700, anchor="end"),
        ]
    )
    for index, (number, label, note) in enumerate((("01", "DECISION", "批准判断"), ("02", "OWNER", "指定负责人"), ("03", "MILESTONE", "锁定验证点"))):
        chip_x = x + 64 + index * 214
        parts.extend(
            [
                _rect(chip_x, y + 360, 198, 28, theme.accent if index == 0 else theme.surface, stroke=theme.border, stroke_width=1),
                _text(chip_x + 12, y + 379, number, size=10, fill="#FFFFFF" if index == 0 else theme.accent, family=theme.display_font, role="label", weight=900),
                _text(chip_x + 42, y + 379, label, size=10, fill="#FFFFFF" if index == 0 else theme.text, family=theme.body_font, role="label", weight=700),
                _text(chip_x + 116, y + 379, note, size=9, fill="#FFFFFF" if index == 0 else theme.muted, family="Microsoft YaHei, Arial", role="annotation"),
            ]
        )
    return parts


def _evidence(theme: Theme, x: int, y: int, page: str = "03") -> list[str]:
    if theme.slug == "dynamic-hero-editorial":
        return _dynamic_hero_evidence(theme, x, y, page)
    parts = _panel_frame(theme, x, y, page, "EVIDENCE")
    parts.extend(
        [
            _text(
                x + 34,
                y + 82,
                "The signal improves when the handoff becomes visible",
                size=26,
                fill=theme.text,
                family=theme.display_font,
                role="slide-title",
                weight=700,
            ),
            _text(
                x + 34,
                y + 110,
                "Illustrative values demonstrate hierarchy only; replace every number and label.",
                size=9,
                fill=theme.muted,
                family=theme.body_font,
                role="caption",
            ),
        ]
    )
    for index, (value, label) in enumerate(theme.metrics):
        metric_y = y + 158 + index * 66
        parts.extend(
            [
                _text(
                    x + 34,
                    metric_y,
                    value,
                    size=24,
                    fill=theme.accent if index == 0 else theme.text,
                    family=theme.display_font,
                    role="metric",
                    weight=700,
                ),
                _text(
                    x + 132,
                    metric_y - 2,
                    label,
                    size=10,
                    fill=theme.text,
                    family=theme.body_font,
                    role="label",
                    weight=700,
                ),
                _text(
                    x + 132,
                    metric_y + 16,
                    "Observed movement · sample period",
                    size=9,
                    fill=theme.muted,
                    family=theme.body_font,
                    role="annotation",
                ),
                _line(x + 34, metric_y + 28, x + 246, metric_y + 28, theme.border, 1),
            ]
        )
    chart_x, chart_y, chart_w, chart_h = x + 292, y + 148, 428, 158
    parts.extend(
        [
            _rect(chart_x, chart_y, chart_w, chart_h, theme.surface, stroke=theme.border, stroke_width=1, radius=theme.radius),
            _text(
                chart_x + 18,
                chart_y + 28,
                "TREND INDEX · BASE 100",
                size=10,
                fill=theme.text,
                family=theme.body_font,
                role="label",
                weight=700,
            ),
        ]
    )
    for index in range(4):
        grid_y = chart_y + 54 + index * 26
        parts.append(_line(chart_x + 18, grid_y, chart_x + 410, grid_y, theme.border, 1))
    points = [
        (chart_x + 24, chart_y + 126),
        (chart_x + 82, chart_y + 112),
        (chart_x + 140, chart_y + 118),
        (chart_x + 198, chart_y + 88),
        (chart_x + 256, chart_y + 78),
        (chart_x + 314, chart_y + 52),
        (chart_x + 392, chart_y + 38),
    ]
    parts.append(
        f'<polyline points="{" ".join(f"{px:g},{py:g}" for px, py in points)}" '
        f'fill="none" stroke="{theme.accent}" stroke-width="4"/>'
    )
    for px, py in points:
        parts.append(f'<circle cx="{px:g}" cy="{py:g}" r="5" fill="{theme.accent}"/>')
    parts.extend(
        [
            _rect(x + 292, y + 326, 428, 42, theme.surface, stroke=theme.border, stroke_width=1, radius=theme.radius),
            _text(
                x + 310,
                y + 352,
                "INTERPRETATION",
                size=10,
                fill=theme.accent_2,
                family=theme.body_font,
                role="label",
                weight=700,
            ),
            _text(
                x + 430,
                y + 352,
                "The largest gain appears after ownership and review criteria become explicit.",
                size=9,
                fill=theme.text,
                family=theme.body_font,
                role="annotation",
            ),
        ]
    )
    return parts


def _synthesis(theme: Theme, x: int, y: int, page: str = "04") -> list[str]:
    if theme.slug == "dynamic-hero-editorial":
        return _dynamic_hero_synthesis(theme, x, y, page)
    parts = _panel_frame(theme, x, y, page, "SYNTHESIS")
    parts.extend(
        [
            _text(
                x + 34,
                y + 82,
                "Prioritize the changes that compound",
                size=26,
                fill=theme.text,
                family=theme.display_font,
                role="slide-title",
                weight=700,
            ),
            _text(
                x + 34,
                y + 110,
                "Sequence decisions by value, confidence, dependency, and accountable ownership.",
                size=9,
                fill=theme.muted,
                family=theme.body_font,
                role="caption",
            ),
        ]
    )
    for index, (name, owner) in enumerate(theme.priorities):
        row_y = y + 144 + index * 68
        parts.extend(
            [
                _rect(x + 34, row_y, 374, 54, theme.surface, stroke=theme.border, stroke_width=1, radius=theme.radius),
                _rect(x + 34, row_y, 8, 54, theme.accent if index == 0 else theme.accent_2, radius=theme.radius),
                _text(
                    x + 58,
                    row_y + 23,
                    name,
                    size=14,
                    fill=theme.text,
                    family=theme.body_font,
                    role="subheading",
                    weight=700,
                ),
                _text(
                    x + 58,
                    row_y + 42,
                    owner,
                    size=9,
                    fill=theme.muted,
                    family=theme.body_font,
                    role="annotation",
                ),
                _text(
                    x + 384,
                    row_y + 31,
                    f"0{index + 1}",
                    size=18,
                    fill=theme.muted,
                    family=theme.display_font,
                    role="metric",
                    weight=700,
                    anchor="end",
                ),
            ]
        )
    matrix_x, matrix_y = x + 446, y + 144
    parts.extend(
        [
            _text(
                matrix_x,
                matrix_y - 12,
                "VALUE / CONFIDENCE",
                size=10,
                fill=theme.text,
                family=theme.body_font,
                role="label",
                weight=700,
            ),
            _rect(matrix_x, matrix_y, 274, 190, theme.surface, stroke=theme.border, stroke_width=1, radius=theme.radius),
            _line(matrix_x + 137, matrix_y + 12, matrix_x + 137, matrix_y + 178, theme.border, 1),
            _line(matrix_x + 12, matrix_y + 95, matrix_x + 262, matrix_y + 95, theme.border, 1),
            _text(matrix_x + 20, matrix_y + 28, "EXPLORE", size=9, fill=theme.muted, family=theme.body_font, role="annotation", weight=700),
            _text(matrix_x + 157, matrix_y + 28, "SCALE", size=9, fill=theme.positive, family=theme.body_font, role="annotation", weight=700),
            _text(matrix_x + 20, matrix_y + 122, "DEFER", size=9, fill=theme.muted, family=theme.body_font, role="annotation", weight=700),
            _text(matrix_x + 157, matrix_y + 122, "PROVE", size=9, fill=theme.warning, family=theme.body_font, role="annotation", weight=700),
            f'<circle cx="{matrix_x + 204}" cy="{matrix_y + 62}" r="18" fill="{theme.positive}"/>',
            f'<circle cx="{matrix_x + 180}" cy="{matrix_y + 145}" r="13" fill="{theme.warning}"/>',
            f'<circle cx="{matrix_x + 84}" cy="{matrix_y + 70}" r="10" fill="{theme.accent}"/>',
            _rect(x + 34, y + 354, 686, 24, theme.accent, radius=12),
            _text(
                x + 377,
                y + 371,
                "ONE DECISION · THREE OWNERS · VISIBLE NEXT MILESTONE",
                size=9,
                fill="#FFFFFF",
                family=theme.body_font,
                role="source",
                weight=700,
                anchor="middle",
            ),
        ]
    )
    return parts


def _section(theme: Theme, x: int, y: int) -> list[str]:
    if theme.slug == "dynamic-hero-editorial":
        return _dynamic_hero_section(theme, x, y)
    titles = {
        "forest-poetic-mosaic": ("走进场所", "先让受众看见环境，再解释问题与机会。"),
        "silk-ink-strategy": ("从意象到策略", "把文化语言转化为可执行的品牌判断。"),
        "museum-cultural-editorial": ("从物证到公共意义", "一件器物如何连接材料、时间与当下。"),
    }
    title, subtitle = titles.get(theme.slug, ("Turn the evidence\ninto a decision", "A chapter opener creates a deliberate change in pace without changing the design system."))
    parts = _panel_frame(theme, x, y, "02", "SECTION / CHAPTER")
    parts.extend(
        [
            _text(x + 34, y + 154, "02", size=108, fill=theme.accent, family=theme.display_font, role="metric", weight=700),
            _text(x + 210, y + 146, title, size=46, fill=theme.text, family=theme.hero_font or theme.display_font, role="deck-title", weight=700, line_height=1.02),
            _text(x + 214, y + 246, subtitle, size=14, fill=theme.text, family=theme.body_font, role="subheading", weight=700),
            _text(x + 214, y + 282, "The display role may be expressive; ordinary slide titles remain locked and exact.", size=9, fill=theme.muted, family=theme.body_font, role="body"),
            _line(x + 214, y + 314, x + 704, y + 314, theme.border, 2),
        ]
    )
    if theme.slug == "forest-poetic-mosaic":
        parts.extend(
            [
                f'<polygon points="{x + 464},{y + 308} {x + 744},{y + 182} {x + 744},{y + 370} {x + 516},{y + 370}" fill="#1B4B39"/>',
                f'<polygon points="{x + 580},{y + 310} {x + 744},{y + 238} {x + 744},{y + 370} {x + 628},{y + 370}" fill="#6B8D7A"/>',
            ]
        )
        parts.extend(_tree_cluster(x + 498, y + 368, scale=0.25, colors=("#0A2C21", "#15503A", "#2C654C"), count=19))
    elif theme.slug == "silk-ink-strategy":
        for offset in range(5):
            points = f'{x + 216},{y + 334 + offset * 7} {x + 352},{y + 306 + offset * 5} {x + 504},{y + 346 + offset * 4} {x + 624},{y + 300 + offset * 7} {x + 732},{y + 330 + offset * 5}'
            parts.append(f'<polyline points="{points}" fill="none" stroke="{theme.accent_2}" stroke-width="{6 - offset * 0.8:g}" opacity="{0.68 - offset * 0.08:g}"/>')
    elif theme.slug == "museum-cultural-editorial":
        parts.extend(
            [
                f'<circle cx="{x + 630}" cy="{y + 302}" r="68" fill="#372923" stroke="{theme.accent_2}" stroke-width="2"/>',
                f'<polygon points="{x + 630},{y + 242} {x + 666},{y + 274} {x + 656},{y + 338} {x + 630},{y + 366} {x + 604},{y + 338} {x + 594},{y + 274}" fill="{theme.accent}" stroke="{theme.accent_2}" stroke-width="3"/>',
            ]
        )
    else:
        for index in range(6):
            parts.append(_line(x + 446 + index * 42, y + 318, x + 486 + index * 42, y + 366, theme.accent_2 if index % 2 else theme.accent, 5))
    return parts


def _narrative(theme: Theme, x: int, y: int) -> list[str]:
    if theme.slug == "dynamic-hero-editorial":
        return _dynamic_hero_narrative(theme, x, y)
    titles = {
        "forest-poetic-mosaic": "一处场所，需要三层证据",
        "silk-ink-strategy": "意象只是入口，品牌判断才是结论",
        "museum-cultural-editorial": "从细节中读出物件的社会生命",
    }
    title = titles.get(theme.slug, "One story becomes credible through three kinds of proof")
    parts = _panel_frame(theme, x, y, "03", "NARRATIVE / ANNOTATION")
    parts.extend(
        [
            _text(x + 34, y + 82, title, size=26, fill=theme.text, family=theme.display_font, role="slide-title", weight=700),
            _text(x + 34, y + 110, "Combine a concrete scene, an observed detail, and an explicit implication.", size=9, fill=theme.muted, family=theme.body_font, role="caption"),
            _rect(x + 34, y + 142, 420, 214, theme.surface, stroke=theme.border, stroke_width=1, radius=theme.radius),
            f'<polygon points="{x + 34},{y + 356} {x + 34},{y + 248} {x + 146},{y + 178} {x + 246},{y + 266} {x + 350},{y + 196} {x + 454},{y + 266} {x + 454},{y + 356}" fill="{theme.accent_2}" opacity="0.42"/>',
            f'<polygon points="{x + 34},{y + 356} {x + 34},{y + 310} {x + 154},{y + 258} {x + 282},{y + 332} {x + 380},{y + 280} {x + 454},{y + 318} {x + 454},{y + 356}" fill="{theme.accent}" opacity="0.72"/>',
            _text(x + 488, y + 170, "01  SCENE", size=14, fill=theme.accent, family=theme.body_font, role="subheading", weight=700),
            _text(x + 488, y + 194, "Show where the issue becomes visible, who experiences it,\nand what is at stake in that specific setting.", size=9, fill=theme.text, family=theme.body_font, role="body", line_height=1.35),
            _text(x + 488, y + 246, "02  DETAIL", size=14, fill=theme.accent, family=theme.body_font, role="subheading", weight=700),
            _text(x + 488, y + 270, "Annotate an observation, quotation, artifact, or mechanism;\nname the source and the limit of the evidence.", size=9, fill=theme.text, family=theme.body_font, role="body", line_height=1.35),
            _text(x + 488, y + 322, "03  MEANING", size=14, fill=theme.accent, family=theme.body_font, role="subheading", weight=700),
            _text(x + 488, y + 346, "State what the evidence changes, which choice it supports,\nand what the audience should inspect next.", size=9, fill=theme.text, family=theme.body_font, role="body", line_height=1.35),
        ]
    )
    return parts


def _context(theme: Theme, x: int, y: int) -> list[str]:
    if theme.slug == "dynamic-hero-editorial":
        return _dynamic_hero_context(theme, x, y)
    parts = _panel_frame(theme, x, y, "04", "CONTEXT / PROBLEM")
    parts.extend(
        [
            _text(x + 34, y + 82, "Three conditions create the visible symptom", size=26, fill=theme.text, family=theme.display_font, role="slide-title", weight=700),
            _text(x + 34, y + 110, "Separate what is observed, what drives it, and what the audience can change.", size=9, fill=theme.muted, family=theme.body_font, role="caption"),
        ]
    )
    conditions = (
        ("01", "OBSERVED SIGNAL", "Name the concrete symptom,\naffected audience, timing,\nand scale. Keep facts separate\nfrom interpretation."),
        ("02", "UNDERLYING DRIVER", "Explain the mechanism or\nconstraint that repeatedly\ncreates the signal. Show\ndirectional evidence."),
        ("03", "DECISION LEVER", "Identify the choice, owner,\nand boundary the audience\ncan influence now. State\nwhat proof is needed next."),
    )
    for index, (number, heading, description) in enumerate(conditions):
        card_x = x + 34 + index * 230
        parts.extend(
            [
                _rect(card_x, y + 146, 212, 164, theme.surface, stroke=theme.border, stroke_width=1, radius=theme.radius),
                _text(card_x + 18, y + 176, number, size=20, fill=theme.accent if index == 0 else theme.accent_2, family=theme.display_font, role="metric", weight=700),
                _text(card_x + 18, y + 208, heading, size=14, fill=theme.text, family=theme.body_font, role="subheading", weight=700),
                _text(card_x + 18, y + 236, description, size=9, fill=theme.muted, family=theme.body_font, role="body", line_height=1.38),
            ]
        )
        if index < 2:
            parts.append(_line(card_x + 212, y + 228, card_x + 230, y + 228, theme.accent, 3))
    parts.extend(
        [
            _rect(x + 34, y + 330, 686, 48, theme.panel, stroke=theme.border, stroke_width=1, radius=theme.radius),
            _text(x + 52, y + 350, "IMPLICATION", size=10, fill=theme.accent, family=theme.body_font, role="label", weight=700),
            _text(x + 148, y + 350, "The deck should prove the driver before asking the audience to approve the lever.", size=9, fill=theme.text, family=theme.body_font, role="annotation", weight=700),
            _text(x + 148, y + 368, "Replace every illustrative statement with sourced project facts, examples, or clearly marked unknowns.", size=9, fill=theme.muted, family=theme.body_font, role="annotation"),
        ]
    )
    return parts


def _comparison(theme: Theme, x: int, y: int, page: str = "06") -> list[str]:
    if theme.slug == "dynamic-hero-editorial":
        return _dynamic_hero_comparison(theme, x, y, page)
    parts = _panel_frame(theme, x, y, page, "COMPARISON")
    parts.extend(
        [
            _text(x + 34, y + 82, "Make the tradeoff visible before naming the recommendation", size=26, fill=theme.text, family=theme.display_font, role="slide-title", weight=700),
            _text(x + 34, y + 110, "Use shared criteria, direct labels, and sourced observations rather than decorative scores.", size=9, fill=theme.muted, family=theme.body_font, role="caption"),
            _text(x + 248, y + 154, "OPTION A", size=14, fill=theme.text, family=theme.body_font, role="subheading", weight=700, anchor="middle"),
            _text(x + 492, y + 154, "OPTION B", size=14, fill=theme.text, family=theme.body_font, role="subheading", weight=700, anchor="middle"),
            _text(x + 664, y + 154, "IMPLICATION", size=14, fill=theme.accent, family=theme.body_font, role="subheading", weight=700, anchor="middle"),
        ]
    )
    rows = (("Audience fit", 0.86, 0.62, "A leads"), ("Evidence strength", 0.68, 0.84, "B leads"), ("Execution effort", 0.52, 0.78, "A is lighter"))
    for index, (label, score_a, score_b, implication) in enumerate(rows):
        row_y = y + 188 + index * 60
        parts.extend(
            [
                _text(x + 34, row_y + 20, label, size=9, fill=theme.text, family=theme.body_font, role="body", weight=700),
                _rect(x + 168, row_y + 8, 160, 12, theme.surface, stroke=theme.border, stroke_width=1),
                _rect(x + 168, row_y + 8, 160 * score_a, 12, theme.accent),
                _rect(x + 412, row_y + 8, 160, 12, theme.surface, stroke=theme.border, stroke_width=1),
                _rect(x + 412, row_y + 8, 160 * score_b, 12, theme.accent_2),
                _text(x + 664, row_y + 20, implication, size=9, fill=theme.text, family=theme.body_font, role="body", anchor="middle"),
                _line(x + 34, row_y + 42, x + 720, row_y + 42, theme.border, 1),
            ]
        )
    parts.extend(
        [
            _rect(x + 34, y + 354, 686, 24, theme.accent, radius=12),
            _text(x + 377, y + 371, "RECOMMEND ONLY AFTER THE CRITERIA, EVIDENCE, AND CONSEQUENCES ARE EXPLICIT", size=9, fill="#FFFFFF", family=theme.body_font, role="source", weight=700, anchor="middle"),
        ]
    )
    return parts


def _roadmap(theme: Theme, x: int, y: int) -> list[str]:
    if theme.slug == "dynamic-hero-editorial":
        return _dynamic_hero_roadmap(theme, x, y)
    parts = _panel_frame(theme, x, y, "08", "ROADMAP / OWNERSHIP")
    parts.extend(
        [
            _text(x + 34, y + 82, "Sequence work by proof, dependency, and owner", size=26, fill=theme.text, family=theme.display_font, role="slide-title", weight=700),
            _text(x + 34, y + 110, "A useful roadmap shows what becomes true at each milestone, not only a list of activities.", size=9, fill=theme.muted, family=theme.body_font, role="caption"),
            _line(x + 64, y + 214, x + 698, y + 214, theme.border, 4),
        ]
    )
    stages = (
        ("01", "FRAME", "Confirm decision, baseline,\nand success measure", "OWNER A · W1"),
        ("02", "PROVE", "Test the critical mechanism\nwith visible evidence", "OWNER B · W2–3"),
        ("03", "ENABLE", "Document workflow, roles,\nand acceptance criteria", "OWNER C · W4"),
        ("04", "SCALE", "Expand only after quality\nand value signals hold", "OWNER D · Q+1"),
    )
    for index, (number, name, description, owner) in enumerate(stages):
        stage_x = x + 56 + index * 170
        parts.extend(
            [
                f'<circle cx="{stage_x + 18}" cy="{y + 214}" r="18" fill="{theme.accent if index == 0 else theme.surface}" stroke="{theme.accent}" stroke-width="3"/>',
                _text(stage_x + 18, y + 219, number, size=10, fill="#FFFFFF" if index == 0 else theme.accent, family=theme.body_font, role="page-number", weight=700, anchor="middle"),
                _text(stage_x, y + 258, name, size=14, fill=theme.text, family=theme.body_font, role="subheading", weight=700),
                _text(stage_x, y + 284, description, size=9, fill=theme.muted, family=theme.body_font, role="body", line_height=1.4),
                _text(stage_x, y + 338, owner, size=9, fill=theme.accent_2, family=theme.body_font, role="annotation", weight=700),
            ]
        )
    parts.extend(
        [
            _rect(x + 34, y + 354, 686, 24, theme.accent, radius=12),
            _text(x + 377, y + 371, "EACH PHASE ENDS WITH A REVIEWABLE ARTIFACT, A DECISION, AND A NAMED OWNER", size=9, fill="#FFFFFF", family=theme.body_font, role="source", weight=700, anchor="middle"),
        ]
    )
    return parts


def _closing(theme: Theme, x: int, y: int, page: str = "08") -> list[str]:
    if theme.slug == "dynamic-hero-editorial":
        return _dynamic_hero_closing(theme, x, y, page)
    closes = {
        "forest-poetic-mosaic": ("让风景成为证据", "留下一个可被记住、也可被执行的结论。"),
        "silk-ink-strategy": ("山水成势，策略落地", "把文化识别转化为一条可跟踪的行动路径。"),
        "museum-cultural-editorial": ("让物证走向公共", "从收藏、研究、解读到参与，完成叙事的闭环。"),
    }
    title, subtitle = closes.get(theme.slug, ("End with one clear move", "Resolve the argument into an owner, a milestone, and a visible next decision."))
    parts = _panel_frame(theme, x, y, page, "RESOLUTION")
    parts.extend(
        [
            _text(x + 54, y + 142, title, size=46, fill=theme.text, family=theme.hero_font or theme.display_font, role="deck-title", weight=700),
            _text(x + 58, y + 194, subtitle, size=14, fill=theme.text, family=theme.body_font, role="subheading", weight=700),
            _line(x + 58, y + 222, x + 704, y + 222, theme.border, 2),
        ]
    )
    actions = (("01", "DECISION", "Name what must be approved"), ("02", "OWNER", "Make accountability visible"), ("03", "MILESTONE", "Define the next proof point"))
    for index, (number, label, description) in enumerate(actions):
        card_x = x + 58 + index * 216
        parts.extend(
            [
                _text(card_x, y + 274, number, size=24, fill=theme.accent if index == 0 else theme.accent_2, family=theme.display_font, role="metric", weight=700),
                _text(card_x, y + 308, label, size=14, fill=theme.text, family=theme.body_font, role="subheading", weight=700),
                _text(card_x, y + 334, description, size=9, fill=theme.muted, family=theme.body_font, role="body"),
            ]
        )
    return parts


def _full_slide(theme: Theme, name: str, panel_parts: list[str]) -> str:
    source_note = [] if any("ILLUSTRATIVE TEMPLATE" in item for item in panel_parts) else [
        _text(724, 392, "ILLUSTRATIVE TEMPLATE", size=9, fill=theme.muted, family=theme.body_font, role="source", weight=700, anchor="end")
    ]
    parts = [
        '<svg xmlns="http://www.w3.org/2000/svg" width="1600" height="900" viewBox="0 0 1600 900">',
        f'<title>{escape(theme.name)} {escape(name)} template</title>',
        f'<desc>One editable 16:9 {escape(name)} reference page from the {escape(theme.name)} multi-page template family.</desc>',
        _rect(0, 0, 1600, 900, theme.field),
        '<g transform="translate(40 50) scale(2)">',
        *panel_parts,
        *source_note,
        '</g>',
        '</svg>',
    ]
    return "\n".join(parts) + "\n"


def _family_display(theme: Theme) -> str:
    return theme.hero_font or theme.display_font


def _wrap_copy(value: str, limit: int = 48, max_lines: int = 3) -> str:
    words = value.split()
    lines: list[str] = []
    current: list[str] = []
    for word in words:
        candidate = " ".join((*current, word))
        if current and len(candidate) > limit and len(lines) < max_lines - 1:
            lines.append(" ".join(current))
            current = [word]
        else:
            current.append(word)
    if current and len(lines) < max_lines:
        lines.append(" ".join(current))
    return "\n".join(lines)


def _rich_frame(
    theme: Theme,
    x: int,
    y: int,
    page: str,
    section: str,
) -> list[str]:
    """Build family-specific page furniture before content is placed."""
    parts = [
        _rect(
            x,
            y,
            760,
            400,
            theme.panel,
            stroke=theme.border,
            stroke_width=1,
            radius=theme.radius,
        )
    ]
    slug = theme.slug
    page_value = int(page) if page.isdigit() else 1

    if slug == "bright-tech-systems":
        parts.extend(
            [
                f'<polygon points="{x + 496},{y} {x + 760},{y} {x + 760},{y + 118}" fill="#E2F5FF"/>',
                f'<polygon points="{x + 614},{y} {x + 760},{y} {x + 760},{y + 62}" fill="{theme.accent}" opacity="0.12"/>',
                f'<circle cx="{x + 654}" cy="{y + 206}" r="104" fill="none" stroke="{theme.accent}" stroke-width="1" opacity="0.2"/>',
                f'<circle cx="{x + 654}" cy="{y + 206}" r="72" fill="none" stroke="{theme.accent_2}" stroke-width="2" opacity="0.28"/>',
            ]
        )
        for index in range(6):
            parts.append(_line(x + 470, y + 292 + index * 14, x + 744, y + 224 + index * 20, theme.accent_2, 0.7))
    elif slug == "dark-engineered-systems":
        for offset in range(68, 748, 68):
            parts.append(_line(x + offset, y + 52, x + offset, y + 382, theme.border, 0.55))
        for offset in range(92, 382, 58):
            parts.append(_line(x + 18, y + offset, x + 742, y + offset, theme.border, 0.45))
        for index in range(7):
            cx = x + 490 + index * 38
            cy = y + 78 + (index % 3) * 26
            parts.append(f'<circle cx="{cx}" cy="{cy}" r="3" fill="{theme.accent_2}"/>')
            if index:
                parts.append(_line(cx - 38, cy - ((index % 3) - ((index - 1) % 3)) * 26, cx, cy, theme.accent, 1.2))
        parts.extend([_line(x + 22, y + 46, x + 22, y + 20, theme.accent, 3), _line(x + 22, y + 20, x + 92, y + 20, theme.accent, 3)])
    elif slug == "editorial-intelligence":
        parts.extend(
            [
                _rect(x + 18, y + 52, 4, 310, theme.accent_2),
                _line(x + 42, y + 122, x + 730, y + 122, theme.border, 1),
                _line(x + 516, y + 38, x + 516, y + 372, theme.border, 0.8),
                _text(x + 720, y + 320, f"{page_value:02d}", size=94, fill=theme.surface, family=theme.display_font, role="metric", weight=700, anchor="end"),
            ]
        )
    elif slug == "expressive-cultural":
        parts.extend(
            [
                f'<polygon points="{x + 566},{y} {x + 760},{y} {x + 760},{y + 152}" fill="{theme.accent_2}"/>',
                f'<polygon points="{x},{y + 308} {x + 136},{y + 400} {x},{y + 400}" fill="{theme.accent}"/>',
                f'<polygon points="{x + 642},{y + 400} {x + 760},{y + 246} {x + 760},{y + 400}" fill="{theme.warning}"/>',
            ]
        )
        for row in range(4):
            for column in range(8):
                parts.append(f'<circle cx="{x + 520 + column * 18}" cy="{y + 192 + row * 18}" r="2" fill="{theme.accent}" opacity="0.45"/>')
    elif slug == "human-documentary":
        parts.extend(
            [
                f'<circle cx="{x + 642}" cy="{y + 96}" r="54" fill="{theme.warning}" opacity="0.18"/>',
                f'<polygon points="{x},{y + 400} {x},{y + 320} {x + 154},{y + 240} {x + 316},{y + 332} {x + 466},{y + 252} {x + 630},{y + 332} {x + 760},{y + 282} {x + 760},{y + 400}" fill="{theme.accent_2}" opacity="0.11"/>',
                _line(x + 38, y + 356, x + 320, y + 356, theme.accent, 4),
                _line(x + 332, y + 356, x + 430, y + 356, theme.border, 4),
            ]
        )
    elif slug == "data-forward-clarity":
        for offset in range(54, 738, 76):
            parts.append(_line(x + offset, y + 126, x + offset, y + 370, theme.border, 0.6))
        for offset in range(146, 372, 45):
            parts.append(_line(x + 32, y + offset, x + 730, y + offset, theme.border, 0.6))
        parts.extend(
            [
                _rect(x + 718, y + 54, 12, 314, theme.accent, radius=6),
            ]
        )
    elif slug == "premium-restraint":
        parts.extend(
            [
                f'<circle cx="{x + 650}" cy="{y + 206}" r="142" fill="none" stroke="{theme.accent}" stroke-width="1" opacity="0.35"/>',
                f'<circle cx="{x + 650}" cy="{y + 206}" r="102" fill="none" stroke="{theme.accent_2}" stroke-width="1" opacity="0.28"/>',
                _line(x + 42, y + 356, x + 706, y + 356, theme.accent, 1.5),
            ]
        )
    elif slug == "product-storytelling":
        parts.extend(
            [
                _rect(x + 500, y + 82, 222, 244, theme.surface, stroke=theme.border, stroke_width=2, radius=28),
                _rect(x + 518, y + 102, 186, 22, theme.panel, radius=11),
                _rect(x + 518, y + 140, 126, 58, theme.accent, radius=16),
                _rect(x + 654, y + 140, 50, 58, theme.accent_2, radius=16),
                _rect(x + 518, y + 212, 186, 94, theme.panel, stroke=theme.border, stroke_width=1, radius=18),
                f'<polyline points="{x + 532},{y + 278} {x + 568},{y + 246} {x + 610},{y + 262} {x + 650},{y + 226} {x + 690},{y + 238}" fill="none" stroke="{theme.accent_2}" stroke-width="4"/>',
            ]
        )
    elif slug == "forest-poetic-mosaic":
        parts.extend(
            [
                f'<polygon points="{x + 420},{y + 400} {x + 420},{y + 170} {x + 520},{y + 92} {x + 612},{y + 196} {x + 760},{y + 76} {x + 760},{y + 400}" fill="#D6E0DA"/>',
                f'<polygon points="{x + 420},{y + 400} {x + 420},{y + 284} {x + 548},{y + 180} {x + 650},{y + 286} {x + 760},{y + 220} {x + 760},{y + 400}" fill="{theme.accent}" opacity="0.78"/>',
                _line(x + 492, y + 104, x + 746, y + 338, "#FFFFFF", 8),
                _line(x + 612, y + 72, x + 448, y + 260, "#FFFFFF", 6),
            ]
        )
        for index in range(18):
            tx = x + 430 + index * 18
            height = 24 + (index % 5) * 7
            parts.append(f'<polygon points="{tx},{y + 382} {tx + 12},{y + 382} {tx + 6},{y + 382 - height}" fill="#083C2C"/>')
    elif slug == "silk-ink-strategy":
        parts.extend(
            [
                f'<polygon points="{x},{y + 400} {x},{y + 310} {x + 126},{y + 236} {x + 250},{y + 324} {x + 382},{y + 220} {x + 520},{y + 322} {x + 650},{y + 248} {x + 760},{y + 304} {x + 760},{y + 400}" fill="#CBD7D1"/>',
                f'<polygon points="{x},{y + 400} {x},{y + 352} {x + 134},{y + 306} {x + 266},{y + 370} {x + 422},{y + 296} {x + 564},{y + 366} {x + 692},{y + 316} {x + 760},{y + 346} {x + 760},{y + 400}" fill="{theme.accent}" opacity="0.72"/>',
                _rect(x + 690, y + 42, 30, 30, "#A53D32"),
                _text(x + 705, y + 63, "策", size=14, fill="#FFFFFF", family=_family_display(theme), role="quote", weight=700, anchor="middle"),
            ]
        )
        for offset in range(5):
            points = f"{x - 8},{y + 326 + offset * 7} {x + 138},{y + 292 + offset * 6} {x + 286},{y + 338 + offset * 5} {x + 430},{y + 286 + offset * 6} {x + 590},{y + 332 + offset * 6} {x + 768},{y + 300 + offset * 7}"
            parts.append(f'<polyline points="{points}" fill="none" stroke="{theme.accent_2}" stroke-width="{5 - offset * 0.6:g}" opacity="{0.7 - offset * 0.08:g}"/>')
    elif slug == "museum-cultural-editorial":
        parts.extend(
            [
                f'<circle cx="{x + 642}" cy="{y + 210}" r="112" fill="#332722" stroke="{theme.accent_2}" stroke-width="1.5"/>',
                f'<circle cx="{x + 642}" cy="{y + 210}" r="78" fill="#221A17" stroke="#6E5548" stroke-width="8"/>',
                f'<polygon points="{x + 642},{y + 136} {x + 684},{y + 174} {x + 674},{y + 254} {x + 642},{y + 300} {x + 610},{y + 254} {x + 600},{y + 174}" fill="{theme.accent}" stroke="{theme.accent_2}" stroke-width="3"/>',
                _line(x + 42, y + 336, x + 420, y + 336, theme.border, 1),
            ]
        )

    parts.extend(
        [
            _text(x + 34, y + 34, section.upper(), size=10, fill=theme.accent, family=theme.body_font, role="label", weight=700),
            _text(x + 718, y + 34, page, size=10, fill=theme.muted, family=theme.body_font, role="page-number", weight=700, anchor="end"),
        ]
    )
    return parts


def _rich_heading(
    theme: Theme,
    x: int,
    y: int,
    *,
    title: str,
    caption: str,
) -> list[str]:
    wrapped_title = _wrap_copy(title, 50, 2)
    caption_y = y + 136 if "\n" in wrapped_title else y + 110
    return [
        _text(x + 34, y + 82, wrapped_title, size=26, fill=theme.text, family=theme.display_font, role="slide-title", weight=700, line_height=1.05),
        _text(x + 34, caption_y, caption, size=9, fill=theme.muted, family=theme.body_font, role="caption", line_height=1.3),
    ]


def _rich_scene(theme: Theme, x: int, y: int, width: int = 390, height: int = 178) -> list[str]:
    """Draw an original scene/evidence placeholder using the family's own grammar."""
    slug = theme.slug
    parts = [_rect(x, y, width, height, theme.surface, stroke=theme.border, stroke_width=1, radius=min(theme.radius, 12))]
    if slug in {"human-documentary", "forest-poetic-mosaic", "silk-ink-strategy"}:
        parts.extend(
            [
                f'<circle cx="{x + width - 66}" cy="{y + 46}" r="28" fill="{theme.warning}" opacity="0.35"/>',
                f'<polygon points="{x},{y + height} {x},{y + 112} {x + 92},{y + 48} {x + 192},{y + 128} {x + 278},{y + 72} {x + width},{y + 132} {x + width},{y + height}" fill="{theme.accent_2}" opacity="0.55"/>',
                f'<polygon points="{x},{y + height} {x},{y + 144} {x + 112},{y + 96} {x + 230},{y + 158} {x + 330},{y + 114} {x + width},{y + 142} {x + width},{y + height}" fill="{theme.accent}" opacity="0.82"/>',
            ]
        )
        if slug == "human-documentary":
            parts.extend([f'<circle cx="{x + 132}" cy="{y + 92}" r="12" fill="{theme.text}"/>', _rect(x + 124, y + 104, 16, 42, theme.text, radius=8)])
    elif slug == "dark-engineered-systems":
        for row in range(3):
            for column in range(4):
                node_x = x + 46 + column * 90
                node_y = y + 44 + row * 52
                parts.append(_rect(node_x, node_y, 52, 24, theme.panel, stroke=theme.accent if row == 1 else theme.border, stroke_width=1, radius=3))
                if column:
                    parts.append(_line(node_x - 38, node_y + 12, node_x, node_y + 12, theme.accent_2, 1.5))
    elif slug in {"data-forward-clarity", "bright-tech-systems"}:
        for index in range(5):
            bar_h = (42, 72, 56, 104, 132)[index]
            bar_x = x + 34 + index * 66
            parts.append(_rect(bar_x, y + height - 26 - bar_h, 34, bar_h, theme.accent if index == 3 else theme.accent_2, radius=6))
            parts.append(_text(bar_x + 17, y + height - 10, f"0{index + 1}", size=9, fill=theme.muted, family=theme.body_font, role="annotation", anchor="middle"))
    elif slug == "product-storytelling":
        parts.extend(
            [
                _rect(x + 28, y + 24, 132, 130, theme.panel, stroke=theme.border, stroke_width=1, radius=18),
                _rect(x + 46, y + 44, 96, 18, theme.accent, radius=9),
                _rect(x + 46, y + 76, 72, 54, theme.accent_2, radius=12),
                _line(x + 170, y + 90, x + 212, y + 90, theme.accent_2, 4),
                _rect(x + 222, y + 38, 138, 108, theme.surface, stroke=theme.accent, stroke_width=2, radius=18),
                f'<circle cx="{x + 292}" cy="{y + 82}" r="22" fill="{theme.positive}"/>',
                _line(x + 280, y + 82, x + 289, y + 92, "#FFFFFF", 4),
                _line(x + 289, y + 92, x + 306, y + 70, "#FFFFFF", 4),
            ]
        )
    elif slug == "expressive-cultural":
        parts.extend(
            [
                f'<polygon points="{x},{y + height} {x},{y + 26} {x + 148},{y + 68} {x + 246},{y + 18} {x + width},{y + 88} {x + width},{y + height}" fill="{theme.accent}"/>',
                f'<polygon points="{x + 72},{y + height} {x + 122},{y + 48} {x + 270},{y + 126} {x + 330},{y + 42} {x + width},{y + 86} {x + width},{y + height}" fill="{theme.accent_2}" opacity="0.85"/>',
                _text(x + 24, y + 146, "CULTURE / VOICE / MOMENT", size=16, fill="#FFFFFF", family=theme.display_font, role="quote", weight=700),
            ]
        )
    elif slug == "editorial-intelligence":
        parts.extend(
            [
                _text(x + 26, y + 76, "“", size=80, fill=theme.accent_2, family=theme.display_font, role="quote", weight=700),
                _text(x + 92, y + 68, "A scene becomes evidence", size=18, fill=theme.text, family=theme.display_font, role="quote", weight=700),
                _text(x + 92, y + 96, "only when the source, limit,", size=12, fill=theme.muted, family=theme.body_font, role="quote"),
                _text(x + 92, y + 118, "and consequence stay visible.", size=12, fill=theme.muted, family=theme.body_font, role="quote"),
                _line(x + 92, y + 138, x + 352, y + 138, theme.accent, 3),
            ]
        )
    elif slug == "premium-restraint":
        parts.extend(
            [
                f'<circle cx="{x + 194}" cy="{y + 88}" r="64" fill="none" stroke="{theme.accent}" stroke-width="2"/>',
                _text(x + 194, y + 103, "01", size=46, fill=theme.text, family=theme.display_font, role="metric", weight=700, anchor="middle"),
                _line(x + 48, y + 144, x + 340, y + 144, theme.accent, 1),
                _text(x + 194, y + 164, "ONE PRECISE SIGNAL", size=10, fill=theme.muted, family=theme.body_font, role="label", weight=700, anchor="middle"),
            ]
        )
    elif slug == "museum-cultural-editorial":
        parts.extend(
            [
                f'<circle cx="{x + 122}" cy="{y + 88}" r="56" fill="#352722" stroke="{theme.accent_2}" stroke-width="2"/>',
                f'<polygon points="{x + 122},{y + 42} {x + 150},{y + 70} {x + 142},{y + 120} {x + 122},{y + 142} {x + 102},{y + 120} {x + 94},{y + 70}" fill="{theme.accent}"/>',
                _text(x + 208, y + 62, "CATALOG A-017", size=10, fill=theme.accent_2, family=theme.body_font, role="label", weight=700),
                _text(x + 208, y + 92, "Material / Trace / Context", size=14, fill=theme.text, family=theme.body_font, role="subheading", weight=700),
                _text(x + 208, y + 122, "Observe first. Interpret second.", size=10, fill=theme.muted, family=theme.body_font, role="quote"),
            ]
        )
    return parts


def _rich_cover(theme: Theme, x: int, y: int) -> list[str]:
    if theme.slug == "dynamic-hero-editorial":
        return _dynamic_hero_cover(theme, x, y)
    if theme.slug in {
        "forest-poetic-mosaic",
        "silk-ink-strategy",
        "museum-cultural-editorial",
    }:
        return _artistic_cover_panel(theme, x, y)

    parts = _rich_frame(theme, x, y, "01", theme.context)
    title_size = 38 if theme.slug != "expressive-cultural" else 42
    parts.extend(
        [
            _text(x + 34, y + 116, theme.cover_title, size=title_size, fill=theme.text, family=_family_display(theme), role="deck-title", weight=700, line_height=1.01),
            _text(x + 36, y + 248, _wrap_copy(theme.cover_subtitle, 46, 2), size=9, fill=theme.muted, family=theme.body_font, role="body", line_height=1.42),
            _text(x + 36, y + 294, "CLAIM  →  EVIDENCE  →  ACTION", size=10, fill=theme.accent, family=theme.body_font, role="label", weight=700),
        ]
    )
    parts.extend(_rich_scene(theme, x + 430, y + 82, 286, 168))
    for index, (value, label) in enumerate(theme.metrics):
        metric_x = x + 34 + index * 226
        parts.extend(
            [
                _line(metric_x, y + 322, metric_x + 206, y + 322, theme.border, 1),
                _text(metric_x, y + 352, value, size=24, fill=theme.accent if index == 0 else theme.text, family=theme.display_font, role="metric", weight=700),
                _text(metric_x + 82, y + 342, label, size=10, fill=theme.text, family=theme.body_font, role="label", weight=700),
                _text(metric_x + 82, y + 360, "illustrative signal · replace", size=9, fill=theme.muted, family=theme.body_font, role="annotation"),
            ]
        )
    parts.append(_text(x + 714, y + 386, "ORIGINAL VECTOR TEMPLATE · ALL SAMPLE DATA MUST BE REPLACED", size=9, fill=theme.muted, family=theme.body_font, role="source", weight=700, anchor="end"))
    return parts


def _rich_section(theme: Theme, x: int, y: int) -> list[str]:
    if theme.slug == "dynamic-hero-editorial":
        return _dynamic_hero_section(theme, x, y)
    titles = {
        "bright-tech-systems": ("MAKE THE SYSTEM\nVISIBLE", "From isolated capability to one shared operating model."),
        "dark-engineered-systems": ("TRACE THE\nFAILURE BOUNDARY", "Dependencies become actionable when every control has an owner."),
        "editorial-intelligence": ("READ THE\nEVIDENCE AGAIN", "Separate what is known, what is inferred, and what remains undecided."),
        "expressive-cultural": ("TURN ATTENTION\nINTO PARTICIPATION", "A strong cultural idea must give the audience a role, not only a slogan."),
        "human-documentary": ("LISTEN BEFORE\nYOU FRAME", "Lived detail changes the problem definition and the next move."),
        "data-forward-clarity": ("FIND THE\nDECISION SIGNAL", "A metric matters only when its driver and consequence remain visible."),
        "premium-restraint": ("CONCENTRATE\nTHE DECISION", "Fewer priorities create the room required for compounding evidence."),
        "product-storytelling": ("MOVE FROM\nFRICTION TO VALUE", "Show the user moment, the product behavior, and the proof of change."),
        "forest-poetic-mosaic": ("走进场所", "先让受众看见环境，再解释问题、证据与行动。"),
        "silk-ink-strategy": ("从意象到策略", "把文化识别转化为可验证、可执行的品牌判断。"),
        "museum-cultural-editorial": ("从物证到公共意义", "让材料、时间、观点与参与形成完整解释链。"),
    }
    title, subtitle = titles[theme.slug]
    parts = _rich_frame(theme, x, y, "02", "SECTION / CHAPTER")
    parts.extend(
        [
            _text(x + 34, y + 196, "02", size=112, fill=theme.accent, family=theme.display_font, role="metric", weight=700),
            _text(x + 190, y + 142, title, size=44, fill=theme.text, family=_family_display(theme), role="deck-title", weight=700, line_height=1.0),
            _text(x + 194, y + 246, subtitle, size=14, fill=theme.text, family=theme.body_font, role="subheading", weight=700),
            _text(x + 194, y + 274, "The chapter opener changes pace while the ordinary title and evidence tokens stay exact.", size=9, fill=theme.muted, family=theme.body_font, role="body"),
        ]
    )
    beats = (("01", "ORIENT", "name the stakes"), ("02", "PROVE", "show the mechanism"), ("03", "DECIDE", "assign the next move"))
    for index, (number, label, note) in enumerate(beats):
        beat_x = x + 194 + index * 172
        parts.extend(
            [
                _line(beat_x, y + 318, beat_x + 148, y + 318, theme.accent if index == 0 else theme.border, 4),
                _text(beat_x, y + 344, number, size=10, fill=theme.accent, family=theme.body_font, role="label", weight=700),
                _text(beat_x + 34, y + 344, label, size=14, fill=theme.text, family=theme.body_font, role="subheading", weight=700),
                _text(beat_x + 34, y + 364, note, size=9, fill=theme.muted, family=theme.body_font, role="annotation"),
            ]
        )
    return parts


def _rich_narrative(theme: Theme, x: int, y: int) -> list[str]:
    if theme.slug == "dynamic-hero-editorial":
        return _dynamic_hero_narrative(theme, x, y)
    titles = {
        "bright-tech-systems": "A scene earns trust when proof is attached",
        "dark-engineered-systems": "An incident becomes useful when evidence stays linked",
        "editorial-intelligence": "A credible story joins scene, source, and meaning",
        "expressive-cultural": "Culture moves when people can see themselves",
        "human-documentary": "Listen first: lived detail changes the decision",
        "data-forward-clarity": "One story explains what the metric cannot",
        "premium-restraint": "One precise story can reframe the portfolio",
        "product-storytelling": "The product becomes real in one user moment",
        "forest-poetic-mosaic": "一处场所，需要三层证据",
        "silk-ink-strategy": "意象只是入口，品牌判断才是结论",
        "museum-cultural-editorial": "从细节中读出物件的社会生命",
    }
    parts = _rich_frame(theme, x, y, "03", "NARRATIVE / ANNOTATION")
    parts.extend(_rich_heading(theme, x, y, title=titles[theme.slug], caption="Connect a concrete scene, a sourced detail, an interpretation, and the decision it changes."))
    parts.extend(_rich_scene(theme, x + 34, y + 144, 402, 196))
    parts.extend(
        [
            _text(x + 52, y + 316, "FIELD NOTE / ORIGINAL PLACEHOLDER", size=10, fill="#FFFFFF" if theme.slug in {"dark-engineered-systems", "museum-cultural-editorial"} else theme.text, family=theme.body_font, role="label", weight=700),
            _text(x + 468, y + 158, "01  SCENE", size=14, fill=theme.accent, family=theme.body_font, role="subheading", weight=700),
            _text(x + 468, y + 182, "Who experiences the issue,\nwhere it occurs, and what is at stake.", size=9, fill=theme.text, family=theme.body_font, role="body", line_height=1.35),
            _text(x + 468, y + 236, "02  SOURCE", size=14, fill=theme.accent, family=theme.body_font, role="subheading", weight=700),
            _text(x + 468, y + 260, "Name the observation, artifact,\nquotation, date, and evidence limit.", size=9, fill=theme.text, family=theme.body_font, role="body", line_height=1.35),
            _text(x + 468, y + 314, "03  MEANING", size=14, fill=theme.accent, family=theme.body_font, role="subheading", weight=700),
            _text(x + 468, y + 338, "State what changes now, who decides,\nand which proof the audience should inspect.", size=9, fill=theme.text, family=theme.body_font, role="body", line_height=1.35),
            _line(x + 468, y + 366, x + 716, y + 366, theme.border, 1),
            _text(x + 716, y + 384, "SCENE → SOURCE → MEANING → ACTION", size=9, fill=theme.muted, family=theme.body_font, role="source", weight=700, anchor="end"),
        ]
    )
    return parts


def _rich_context(theme: Theme, x: int, y: int) -> list[str]:
    if theme.slug == "dynamic-hero-editorial":
        return _dynamic_hero_context(theme, x, y)
    title_map = {
        "bright-tech-systems": "Three operating signals converge on one delivery decision",
        "dark-engineered-systems": "Three failure conditions converge on one boundary",
        "editorial-intelligence": "Three contradictions are shaping the decision",
        "expressive-cultural": "Three cultural tensions converge on one participation moment",
        "human-documentary": "Three lived constraints produce the visible symptom",
        "data-forward-clarity": "Three drivers explain the headline movement",
        "premium-restraint": "Three portfolio constraints reveal the decisive choice",
        "product-storytelling": "Three friction points delay the first value moment",
        "forest-poetic-mosaic": "三重场景线索，汇成一个叙事判断",
        "silk-ink-strategy": "三条文化线索，汇成一个品牌决策",
        "museum-cultural-editorial": "三层物证关系，汇成一个公共判断",
    }
    title = title_map.get(theme.slug, "Three conditions converge on one decision window")
    parts = _rich_frame(theme, x, y, "04", "CONTEXT / PROBLEM")
    parts.extend(_rich_heading(theme, x, y, title=title, caption="Separate the observed signal, the mechanism beneath it, and the lever the audience can influence."))
    center_x, center_y = x + 382, y + 246
    parts.extend(
        [
            f'<circle cx="{center_x}" cy="{center_y}" r="64" fill="{theme.surface}" stroke="{theme.accent}" stroke-width="3"/>',
            _text(center_x, center_y - 6, "DECISION", size=10, fill=theme.accent, family=theme.body_font, role="label", weight=700, anchor="middle"),
            _text(center_x, center_y + 28, "24h", size=28, fill=theme.text, family=theme.display_font, role="metric", weight=700, anchor="middle"),
            _text(center_x, center_y + 48, "illustrative window", size=9, fill=theme.muted, family=theme.body_font, role="annotation", anchor="middle"),
        ]
    )
    nodes = (
        (x + 126, y + 178, "01", "OBSERVED SIGNAL", "Name the concrete symptom,\naudience, scale, and timing."),
        (x + 126, y + 310, "02", "UNDERLYING DRIVER", "Show the mechanism, constraint,\nor repeated handoff failure."),
        (x + 638, y + 244, "03", "DECISION LEVER", "State the choice, owner, boundary,\nand next proof point."),
    )
    for node_x, node_y, number, heading, body in nodes:
        line_end_x = center_x - 66 if node_x < center_x else center_x + 66
        parts.extend(
            [
                _line(node_x + (88 if node_x < center_x else -88), node_y, line_end_x, center_y, theme.accent_2, 2),
                f'<circle cx="{node_x}" cy="{node_y}" r="46" fill="{theme.surface}" stroke="{theme.border}" stroke-width="1.5"/>',
                _text(node_x, node_y - 14, number, size=18, fill=theme.accent, family=theme.display_font, role="metric", weight=700, anchor="middle"),
                _text(node_x, node_y + 8, heading, size=10, fill=theme.text, family=theme.body_font, role="label", weight=700, anchor="middle"),
                _text(node_x, node_y + 72, body, size=9, fill=theme.muted, family=theme.body_font, role="body", line_height=1.3, anchor="middle"),
            ]
        )
    parts.extend(
        [
            _rect(x + 286, y + 336, 286, 46, theme.surface, stroke=theme.border, stroke_width=1, radius=min(theme.radius, 10)),
            _text(x + 304, y + 356, "IMPLICATION", size=10, fill=theme.accent, family=theme.body_font, role="label", weight=700),
            _text(x + 404, y + 352, "Prove the driver before asking\nfor approval of the lever.", size=9, fill=theme.text, family=theme.body_font, role="annotation", line_height=1.25),
        ]
    )
    return parts


def _rich_process(theme: Theme, x: int, y: int, page: str = "05") -> list[str]:
    if theme.slug == "dynamic-hero-editorial":
        return _dynamic_hero_process(theme, x, y, page)
    title_map = {
        "dark-engineered-systems": "Five controls turn a signal into a reliable response",
        "editorial-intelligence": "Five editorial moves turn sources into a decision",
        "expressive-cultural": "Five beats turn attention into participation",
        "human-documentary": "Five field moves protect voice, evidence, and action",
        "data-forward-clarity": "Five checks keep the metric tied to a decision",
        "premium-restraint": "Five gates concentrate effort on the decisive proof",
        "product-storytelling": "Five moments carry a user from friction to value",
        "forest-poetic-mosaic": "五个叙事动作，让场景走向行动",
        "silk-ink-strategy": "五步成势，让文化识别进入执行",
        "museum-cultural-editorial": "五层解释，让物证进入公共行动",
    }
    title = title_map.get(theme.slug, "Five moves create an accountable delivery loop")
    parts = _rich_frame(theme, x, y, page, "PROCESS / QUALITY GATES")
    parts.extend(_rich_heading(theme, x, y, title=title, caption="Every stage produces an artifact, a named owner, and a visible acceptance condition."))
    offsets = (18, -2, 24, 4, 30)
    for index, (name, description) in enumerate(theme.steps):
        step_x = x + 34 + index * 138
        step_y = y + 154 + offsets[index]
        fill = theme.accent if index == 0 else theme.surface
        text_fill = "#FFFFFF" if index == 0 else theme.text
        parts.extend(
            [
                f'<polygon points="{step_x},{step_y + 10} {step_x + 106},{step_y} {step_x + 124},{step_y + 132} {step_x + 16},{step_y + 144}" fill="{fill}" stroke="{theme.border}" stroke-width="1.2"/>',
                _text(step_x + 18, step_y + 38, f"0{index + 1}", size=22, fill=text_fill if index == 0 else theme.accent, family=theme.display_font, role="metric", weight=700),
                _text(step_x + 18, step_y + 70, name, size=14, fill=text_fill, family=theme.body_font, role="subheading", weight=700),
                _text(step_x + 18, step_y + 94, _wrap_copy(description, 20, 2), size=9, fill="#FFFFFF" if index == 0 else theme.muted, family=theme.body_font, role="body", line_height=1.32),
                _text(step_x + 18, step_y + 130, f"OUTPUT {index + 1:02d}", size=9, fill="#FFFFFF" if index == 0 else theme.accent_2, family=theme.body_font, role="annotation", weight=700),
            ]
        )
        if index < 4:
            parts.append(_line(step_x + 124, step_y + 74, step_x + 146, y + 228 + offsets[index + 1], theme.accent_2, 3))
    parts.extend(
        [
            f'<polygon points="{x + 34},{y + 350} {x + 704},{y + 330} {x + 720},{y + 374} {x + 48},{y + 388}" fill="{theme.surface}" stroke="{theme.accent}" stroke-width="2"/>',
            _text(x + 64, y + 369, "QUALITY GATE", size=10, fill=theme.accent, family=theme.body_font, role="label", weight=700),
            _text(x + 190, y + 366, "Evidence, owner, and acceptance condition must all be explicit before the next stage.", size=9, fill=theme.text, family=theme.body_font, role="source"),
        ]
    )
    return parts


def _rich_evidence(theme: Theme, x: int, y: int, page: str = "06") -> list[str]:
    if theme.slug == "dynamic-hero-editorial":
        return _dynamic_hero_evidence(theme, x, y, page)
    title_map = {
        "bright-tech-systems": "The operating signal improves after the handoff is visible",
        "dark-engineered-systems": "Recovery improves when controls and ownership stay linked",
        "editorial-intelligence": "The recommendation strengthens when sources converge",
        "expressive-cultural": "Participation rises when the audience owns a visible role",
        "human-documentary": "Follow-through improves when the field voice returns",
        "data-forward-clarity": "The headline gain is concentrated in one driver",
        "premium-restraint": "Value compounds after capital and proof align",
        "product-storytelling": "Time to value falls after the first success moment",
        "forest-poetic-mosaic": "证据需要同时显示变化、来源与行动含义",
        "silk-ink-strategy": "策略信号在统一叙事后开始收敛",
        "museum-cultural-editorial": "理解在物证、解释与参与之间逐步增长",
    }
    parts = _rich_frame(theme, x, y, page, "EVIDENCE / INTERPRETATION")
    parts.extend(_rich_heading(theme, x, y, title=title_map[theme.slug], caption="Illustrative values demonstrate visual hierarchy only; replace values, labels, units, source, and period."))

    for index, (value, label) in enumerate(theme.metrics):
        metric_x = x + 34 + index * 142
        parts.extend(
            [
                _text(metric_x, y + 166, value, size=26, fill=theme.accent if index == 0 else theme.text, family=theme.display_font, role="metric", weight=700),
                _text(metric_x, y + 190, label, size=10, fill=theme.text, family=theme.body_font, role="label", weight=700),
                _text(metric_x, y + 210, "sample · replace", size=9, fill=theme.muted, family=theme.body_font, role="annotation"),
                _line(metric_x, y + 222, metric_x + 122, y + 222, theme.border, 1),
            ]
        )

    chart_x, chart_y, chart_w, chart_h = x + 34, y + 244, 448, 104
    parts.extend(
        [
            _rect(chart_x, chart_y, chart_w, chart_h, theme.surface, stroke=theme.border, stroke_width=1, radius=min(theme.radius, 10)),
            _text(chart_x + 18, chart_y + 24, "DIRECTLY LABELED SIGNAL · BASE 100", size=10, fill=theme.text, family=theme.body_font, role="label", weight=700),
        ]
    )
    chart_values = (28, 46, 40, 72, 82, 116, 132)
    line_families = {"bright-tech-systems", "dark-engineered-systems", "data-forward-clarity", "product-storytelling", "silk-ink-strategy"}
    if theme.slug in line_families:
        points: list[tuple[float, float]] = []
        for index, value in enumerate(chart_values):
            px = chart_x + 26 + index * 64
            py = chart_y + 92 - value * 0.46
            points.append((px, py))
        for row in range(3):
            gy = chart_y + 42 + row * 24
            parts.append(_line(chart_x + 18, gy, chart_x + chart_w - 18, gy, theme.border, 0.8))
        parts.append(f'<polyline points="{" ".join(f"{px:g},{py:g}" for px, py in points)}" fill="none" stroke="{theme.accent}" stroke-width="4"/>')
        for px, py in points:
            parts.append(f'<circle cx="{px:g}" cy="{py:g}" r="4.5" fill="{theme.accent}"/>')
    else:
        for index, value in enumerate((36, 54, 48, 76, 86, 112, 128)):
            bar_x = chart_x + 24 + index * 58
            bar_h = value * 0.48
            parts.extend(
                [
                    _rect(bar_x, chart_y + 88 - bar_h, 28, bar_h, theme.accent if index == 5 else theme.accent_2, radius=3),
                    _text(bar_x + 14, chart_y + 100, f"W{index + 1}", size=9, fill=theme.muted, family=theme.body_font, role="annotation", anchor="middle"),
                ]
            )

    parts.extend(
        [
            _rect(x + 508, y + 142, 208, 206, theme.surface, stroke=theme.border, stroke_width=1, radius=min(theme.radius, 10)),
            _text(x + 528, y + 168, "WHAT THE SIGNAL PROVES", size=10, fill=theme.accent, family=theme.body_font, role="label", weight=700),
            _text(x + 528, y + 204, "01  DRIVER", size=14, fill=theme.text, family=theme.body_font, role="subheading", weight=700),
            _text(x + 528, y + 228, "The strongest movement appears after\nownership and review criteria align.", size=9, fill=theme.muted, family=theme.body_font, role="body", line_height=1.35),
            _text(x + 528, y + 278, "02  EXCEPTION", size=14, fill=theme.text, family=theme.body_font, role="subheading", weight=700),
            _text(x + 528, y + 302, "One interval breaks the trend; inspect\ncohort mix before claiming causality.", size=9, fill=theme.muted, family=theme.body_font, role="body", line_height=1.35),
            _rect(x + 34, y + 364, 682, 24, theme.accent, radius=12),
            _text(x + 375, y + 381, "SOURCE · PERIOD · UNIT · SAMPLE · INTERPRETATION · NEXT CHECK", size=9, fill="#FFFFFF", family=theme.body_font, role="source", weight=700, anchor="middle"),
        ]
    )
    return parts


def _rich_comparison(theme: Theme, x: int, y: int, page: str = "07") -> list[str]:
    if theme.slug == "dynamic-hero-editorial":
        return _dynamic_hero_comparison(theme, x, y, page)
    title_map = {
        "editorial-intelligence": "Compare the arguments on the same evidentiary baseline",
        "human-documentary": "Compare what each option changes for people in practice",
        "data-forward-clarity": "Compare the options on the measures that drive the decision",
        "premium-restraint": "The stronger option protects focus and preserves upside",
        "product-storytelling": "The stronger journey removes friction before adding features",
        "forest-poetic-mosaic": "选择不是风格偏好，而是叙事效果的比较",
        "silk-ink-strategy": "在文化识别与执行效率之间明确取舍",
        "museum-cultural-editorial": "比较不同解释路径带来的公共价值",
    }
    title = title_map.get(theme.slug, "Make the tradeoff visible before naming the recommendation")
    parts = _rich_frame(theme, x, y, page, "COMPARISON / SHARED CRITERIA")
    parts.extend(_rich_heading(theme, x, y, title=title, caption="Use direct labels, shared criteria, and sourced observations; illustrative bars are not real evidence."))
    parts.extend(
        [
            f'<polygon points="{x + 34},{y + 144} {x + 370},{y + 132} {x + 346},{y + 344} {x + 34},{y + 358}" fill="{theme.surface}" stroke="{theme.border}" stroke-width="1"/>',
            f'<polygon points="{x + 370},{y + 132} {x + 716},{y + 144} {x + 716},{y + 358} {x + 346},{y + 344}" fill="{theme.panel}" stroke="{theme.border}" stroke-width="1"/>',
            _text(x + 58, y + 176, "OPTION A / CURRENT", size=14, fill=theme.accent_2, family=theme.body_font, role="subheading", weight=700),
            _text(x + 402, y + 176, "OPTION B / RECOMMENDED", size=14, fill=theme.accent, family=theme.body_font, role="subheading", weight=700),
            _text(x + 58, y + 202, "Lower coordination cost\nbut evidence remains fragmented.", size=9, fill=theme.muted, family=theme.body_font, role="body", line_height=1.35),
            _text(x + 402, y + 202, "Higher setup discipline\nbut decisions become reviewable.", size=9, fill=theme.muted, family=theme.body_font, role="body", line_height=1.35),
        ]
    )
    rows = (("Audience fit", 0.72, 0.88), ("Evidence strength", 0.56, 0.86), ("Execution load", 0.74, 0.62))
    for index, (label, score_a, score_b) in enumerate(rows):
        row_y = y + 258 + index * 34
        parts.extend(
            [
                _text(x + 58, row_y, label, size=10, fill=theme.text, family=theme.body_font, role="label", weight=700),
                _rect(x + 156, row_y - 10, 152, 10, theme.border),
                _rect(x + 156, row_y - 10, 152 * score_a, 10, theme.accent_2),
                _text(x + 402, row_y, label, size=10, fill=theme.text, family=theme.body_font, role="label", weight=700),
                _rect(x + 500, row_y - 10, 152, 10, theme.border),
                _rect(x + 500, row_y - 10, 152 * score_b, 10, theme.accent),
            ]
        )
    parts.extend(
        [
            f'<circle cx="{x + 360}" cy="{y + 248}" r="30" fill="{theme.accent}"/>',
            _text(x + 360, y + 255, "VS", size=16, fill="#FFFFFF", family=theme.display_font, role="metric", weight=700, anchor="middle"),
            _rect(x + 228, y + 366, 316, 22, theme.accent, radius=11),
            _text(x + 386, y + 382, "RECOMMEND B AFTER SOURCE AND CONSEQUENCE REVIEW", size=9, fill="#FFFFFF", family=theme.body_font, role="source", weight=700, anchor="middle"),
        ]
    )
    return parts


def _rich_roadmap(theme: Theme, x: int, y: int) -> list[str]:
    if theme.slug == "dynamic-hero-editorial":
        return _dynamic_hero_roadmap(theme, x, y)
    title_map = {
        "dark-engineered-systems": "Sequence reliability work by dependency and control proof",
        "editorial-intelligence": "Sequence the argument from framing to decision",
        "expressive-cultural": "Sequence the campaign from reveal to sustained participation",
        "human-documentary": "Return evidence to the field at every milestone",
        "data-forward-clarity": "Sequence tests by decision value and measurement confidence",
        "premium-restraint": "Sequence only the bets that unlock the next proof",
        "product-storytelling": "Sequence adoption around the user's next success moment",
        "forest-poetic-mosaic": "路线图要显示证据如何逐步变成行动",
        "silk-ink-strategy": "从定势、成形到扩散，逐步验证策略",
        "museum-cultural-editorial": "从建档、解释到参与，形成公共路径",
    }
    title = title_map.get(theme.slug, "Sequence work by proof, dependency, owner, and decision")
    parts = _rich_frame(theme, x, y, "08", "ROADMAP / OWNERSHIP")
    parts.extend(_rich_heading(theme, x, y, title=title, caption="Each phase ends with a reviewable artifact, a named owner, an acceptance condition, and a decision."))
    stages = (
        ("01", "FRAME", "Decision + baseline", "OWNER A · W1"),
        ("02", "PROVE", "Critical mechanism", "OWNER B · W2–3"),
        ("03", "ENABLE", "Workflow + criteria", "OWNER C · W4"),
        ("04", "SCALE", "Value + quality hold", "OWNER D · Q+1"),
    )
    path_points: list[tuple[float, float]] = []
    for index, (number, name, output, owner) in enumerate(stages):
        stage_x = x + 68 + index * 172
        stage_y = y + 196 + (index % 2) * 76
        path_points.append((stage_x + 40, stage_y))
        parts.extend(
            [
                f'<circle cx="{stage_x + 40}" cy="{stage_y}" r="34" fill="{theme.accent if index == 0 else theme.surface}" stroke="{theme.accent}" stroke-width="3"/>',
                _text(stage_x + 40, stage_y + 7, number, size=16, fill="#FFFFFF" if index == 0 else theme.accent, family=theme.display_font, role="metric", weight=700, anchor="middle"),
                _text(stage_x, stage_y + 58, name, size=14, fill=theme.text, family=theme.body_font, role="subheading", weight=700),
                _text(stage_x, stage_y + 82, output, size=9, fill=theme.text, family=theme.body_font, role="body"),
                _text(stage_x, stage_y + 104, owner, size=9, fill=theme.accent_2, family=theme.body_font, role="annotation", weight=700),
            ]
        )
    parts.insert(len(_rich_frame(theme, x, y, "08", "ROADMAP / OWNERSHIP")) + len(_rich_heading(theme, x, y, title=title, caption="Each phase ends with a reviewable artifact, a named owner, an acceptance condition, and a decision.")), f'<polyline points="{" ".join(f"{px:g},{py:g}" for px, py in path_points)}" fill="none" stroke="{theme.border}" stroke-width="5"/>')
    parts.extend(
        [
            _rect(x + 34, y + 364, 682, 24, theme.accent, radius=12),
            _text(x + 375, y + 381, "ARTIFACT · OWNER · ACCEPTANCE · DECISION · NEXT DEPENDENCY", size=9, fill="#FFFFFF", family=theme.body_font, role="source", weight=700, anchor="middle"),
        ]
    )
    return parts


def _rich_decision(theme: Theme, x: int, y: int, page: str = "09") -> list[str]:
    if theme.slug == "dynamic-hero-editorial":
        return _dynamic_hero_synthesis(theme, x, y, page)
    title_map = {
        "editorial-intelligence": "Choose the path with the strongest evidence and clearest consequence",
        "human-documentary": "Choose the path that returns value to the people who shaped it",
        "data-forward-clarity": "Protect the core signal, prove the driver, then expand",
        "premium-restraint": "Concentrate capital on the three moves that compound",
        "product-storytelling": "Approve the adoption path, owner, and first proof point",
        "forest-poetic-mosaic": "让场景、证据与行动收束成一个选择",
        "silk-ink-strategy": "先统一品牌叙事，再扩展内容与渠道",
        "museum-cultural-editorial": "让物证、观点与公共行动形成闭环",
    }
    title = title_map.get(theme.slug, "Prioritize the changes that improve value, trust, and execution")
    parts = _rich_frame(theme, x, y, page, "DECISION / PRIORITY FIELD")
    parts.extend(_rich_heading(theme, x, y, title=title, caption="Illustrative priorities show hierarchy only; replace the recommendation, evidence, owner, milestone, and boundary."))
    for index, (name, owner) in enumerate(theme.priorities):
        row_y = y + 146 + index * 64
        parts.extend(
            [
                f'<polygon points="{x + 34},{row_y + 6} {x + 398},{row_y} {x + 408},{row_y + 50} {x + 44},{row_y + 56}" fill="{theme.surface}" stroke="{theme.border}" stroke-width="1"/>',
                _rect(x + 34, row_y + 6, 8, 50, theme.accent if index == 0 else theme.accent_2),
                _text(x + 58, row_y + 28, name, size=14, fill=theme.text, family=theme.body_font, role="subheading", weight=700),
                _text(x + 58, row_y + 46, owner, size=9, fill=theme.muted, family=theme.body_font, role="annotation"),
                _text(x + 382, row_y + 34, f"0{index + 1}", size=18, fill=theme.accent, family=theme.display_font, role="metric", weight=700, anchor="end"),
            ]
        )
    matrix_x, matrix_y = x + 446, y + 146
    parts.extend(
        [
            _text(matrix_x, matrix_y - 12, "VALUE / CONFIDENCE", size=10, fill=theme.text, family=theme.body_font, role="label", weight=700),
            _rect(matrix_x, matrix_y, 270, 190, theme.surface, stroke=theme.border, stroke_width=1, radius=min(theme.radius, 10)),
            _line(matrix_x + 135, matrix_y + 12, matrix_x + 135, matrix_y + 178, theme.border, 1),
            _line(matrix_x + 12, matrix_y + 95, matrix_x + 258, matrix_y + 95, theme.border, 1),
            _text(matrix_x + 18, matrix_y + 28, "EXPLORE", size=9, fill=theme.muted, family=theme.body_font, role="annotation", weight=700),
            _text(matrix_x + 154, matrix_y + 28, "SCALE", size=9, fill=theme.positive, family=theme.body_font, role="annotation", weight=700),
            _text(matrix_x + 18, matrix_y + 120, "DEFER", size=9, fill=theme.muted, family=theme.body_font, role="annotation", weight=700),
            _text(matrix_x + 154, matrix_y + 120, "PROVE", size=9, fill=theme.warning, family=theme.body_font, role="annotation", weight=700),
            f'<circle cx="{matrix_x + 204}" cy="{matrix_y + 62}" r="20" fill="{theme.positive}"/>',
            f'<circle cx="{matrix_x + 178}" cy="{matrix_y + 145}" r="14" fill="{theme.warning}"/>',
            f'<circle cx="{matrix_x + 76}" cy="{matrix_y + 70}" r="10" fill="{theme.accent}"/>',
            _rect(x + 34, y + 364, 682, 24, theme.accent, radius=12),
            _text(x + 375, y + 381, "ONE DECISION · THREE OWNERS · ONE VISIBLE NEXT MILESTONE", size=9, fill="#FFFFFF", family=theme.body_font, role="source", weight=700, anchor="middle"),
        ]
    )
    return parts


def _rich_closing(theme: Theme, x: int, y: int, page: str = "10") -> list[str]:
    if theme.slug == "dynamic-hero-editorial":
        return _dynamic_hero_closing(theme, x, y, page)
    closes = {
        "bright-tech-systems": ("Make the operating model repeatable", "Approve the standard, name the owners, and verify the first milestone."),
        "dark-engineered-systems": ("Reliability becomes real at the boundary", "Close with the control, owner, dependency, and proof that can be reviewed."),
        "editorial-intelligence": ("Let the evidence carry the recommendation", "Close the argument with one choice, its consequence, and the next source to inspect."),
        "expressive-cultural": ("Make participation the final visual", "Give the audience a role, a moment, and a reason to carry the idea forward."),
        "human-documentary": ("Return the story as action", "Close the loop with the people, places, evidence, and commitments that shaped it."),
        "data-forward-clarity": ("Turn the signal into an operating choice", "Protect the metric definition, assign the owner, and schedule the next check."),
        "premium-restraint": ("Choose fewer moves. Compound the proof.", "Concentrate capital, sequence leadership attention, and keep the review cadence visible."),
        "product-storytelling": ("Make the next user success inevitable", "Approve the pilot, the enablement owner, and the proof required for expansion."),
        "forest-poetic-mosaic": ("让风景成为证据", "留下一个可被记住、也能被执行的结论。"),
        "silk-ink-strategy": ("山水成势，策略落地", "把文化识别转化为一条可跟踪、可验证的行动路径。"),
        "museum-cultural-editorial": ("让物证走向公共", "从收藏、研究、解释到参与，完成文化叙事的闭环。"),
    }
    title, subtitle = closes[theme.slug]
    parts = _rich_frame(theme, x, y, page, "RESOLUTION / NEXT MOVE")
    title_limit = 24 if theme.slug == "premium-restraint" else 30
    wrapped_title = _wrap_copy(title, title_limit, 2)
    two_line_title = "\n" in wrapped_title
    title_y = y + 126 if two_line_title else y + 158
    subtitle_y = y + 220
    parts.extend(
        [
            _text(x + 54, title_y, wrapped_title, size=42, fill=theme.text, family=_family_display(theme), role="deck-title", weight=700, line_height=1.02),
            _text(x + 58, subtitle_y, _wrap_copy(subtitle, 68, 2), size=14, fill=theme.text, family=theme.body_font, role="subheading", weight=700, line_height=1.3),
            _line(x + 58, y + 258, x + 704, y + 258, theme.accent, 2),
        ]
    )
    action_sets = {
        "bright-tech-systems": (("01", "STANDARD", "What becomes repeatable"), ("02", "OWNER", "Who runs the next cycle"), ("03", "MILESTONE", "What proof closes the loop")),
        "dark-engineered-systems": (("01", "CONTROL", "Which boundary is protected"), ("02", "OWNER", "Who responds and reviews"), ("03", "PROOF", "What verifies reliability")),
        "editorial-intelligence": (("01", "CHOICE", "What the evidence supports"), ("02", "CONSEQUENCE", "What changes if approved"), ("03", "NEXT SOURCE", "What remains to inspect")),
        "expressive-cultural": (("01", "ROLE", "What the audience can do"), ("02", "MOMENT", "Where participation begins"), ("03", "REASON", "Why the idea travels")),
        "human-documentary": (("01", "COMMITMENT", "What returns to the field"), ("02", "STEWARD", "Who protects the promise"), ("03", "RETURN", "When people see the result")),
        "data-forward-clarity": (("01", "METRIC", "What signal stays stable"), ("02", "OWNER", "Who watches the driver"), ("03", "NEXT CHECK", "When the claim is reviewed")),
        "premium-restraint": (("01", "BET", "What receives focus"), ("02", "SPONSOR", "Who protects the sequence"), ("03", "REVIEW", "What unlocks more capital")),
        "product-storytelling": (("01", "PILOT", "What user moment to prove"), ("02", "ENABLEMENT", "Who removes the friction"), ("03", "SUCCESS", "What permits expansion")),
        "forest-poetic-mosaic": (("01", "叙事判断", "要留下什么结论"), ("02", "行动责任", "由谁连接场景与行动"), ("03", "验证节点", "何时回看真实反馈")),
        "silk-ink-strategy": (("01", "品牌结论", "要统一什么认知"), ("02", "执行责任", "由谁推动内容落地"), ("03", "验收节点", "用什么证明策略有效")),
        "museum-cultural-editorial": (("01", "公共主张", "物证支持什么解释"), ("02", "项目责任", "由谁组织研究与参与"), ("03", "下一节点", "何时完成公共验证")),
    }
    actions = action_sets[theme.slug]
    if theme.slug in {"forest-poetic-mosaic", "silk-ink-strategy"}:
        for index in range(3):
            card_x = x + 44 + index * 216
            tilt = (8, -4, 6)[index]
            parts.append(
                f'<polygon points="{card_x},{y + 280 + tilt} '
                f'{card_x + 192},{y + 270 - tilt} '
                f'{card_x + 198},{y + 376 - tilt} '
                f'{card_x + 6},{y + 382 + tilt}" '
                f'fill="{theme.panel}" stroke="{theme.border}" stroke-width="1"/>'
            )
    for index, (number, label, note) in enumerate(actions):
        card_x = x + 58 + index * 216
        parts.extend(
            [
                _text(card_x, y + 298, number, size=24, fill=theme.accent if index == 0 else theme.accent_2, family=theme.display_font, role="metric", weight=700),
                _text(card_x, y + 330, label, size=14, fill=theme.text, family=theme.body_font, role="subheading", weight=700),
                _text(card_x, y + 354, note, size=9, fill=theme.muted, family=theme.body_font, role="body"),
                _line(card_x, y + 372, card_x + 178, y + 372, theme.border, 1),
            ]
        )
    return parts


def build_template_pages(theme: Theme) -> dict[str, str]:
    return {
        "slide_01-cover.svg": _full_slide(theme, "cover", _rich_cover(theme, 0, 0)),
        "slide_02-section.svg": _full_slide(theme, "section", _rich_section(theme, 0, 0)),
        "slide_03-narrative.svg": _full_slide(theme, "narrative", _rich_narrative(theme, 0, 0)),
        "slide_04-context.svg": _full_slide(theme, "context", _rich_context(theme, 0, 0)),
        "slide_05-process.svg": _full_slide(theme, "process", _rich_process(theme, 0, 0, "05")),
        "slide_06-evidence.svg": _full_slide(theme, "evidence", _rich_evidence(theme, 0, 0, "06")),
        "slide_07-comparison.svg": _full_slide(theme, "comparison", _rich_comparison(theme, 0, 0, "07")),
        "slide_08-roadmap.svg": _full_slide(theme, "roadmap", _rich_roadmap(theme, 0, 0)),
        "slide_09-decision.svg": _full_slide(theme, "decision", _rich_decision(theme, 0, 0, "09")),
        "slide_10-close.svg": _full_slide(theme, "close", _rich_closing(theme, 0, 0, "10")),
    }


def _artistic_svg_start(theme: Theme, description: str) -> list[str]:
    return [
        '<svg xmlns="http://www.w3.org/2000/svg" width="1600" height="900" viewBox="0 0 1600 900">',
        f'<title>{escape(theme.name)} template contact sheet</title>',
        f'<desc>{escape(description)}</desc>',
        _rect(0, 0, 1600, 900, theme.field),
        _text(1548, 18, "10-PAGE / FULL FAMILY", size=9, fill=theme.accent, family=theme.body_font, role="annotation", weight=700, anchor="end"),
    ]


def _tree_cluster(
    x: float,
    ground_y: float,
    *,
    scale: float,
    colors: tuple[str, str, str],
    count: int,
) -> list[str]:
    parts: list[str] = []
    for index in range(count):
        tree_x = x + index * 34 * scale
        height = (74 + (index % 5) * 18) * scale
        width = (22 + (index % 3) * 6) * scale
        color = colors[index % len(colors)]
        parts.extend(
            [
                f'<polygon points="{tree_x:g},{ground_y:g} {tree_x + width:g},{ground_y:g} '
                f'{tree_x + width / 2:g},{ground_y - height:g}" fill="{color}"/>',
                f'<polygon points="{tree_x + width * 0.12:g},{ground_y - height * 0.28:g} '
                f'{tree_x + width * 0.88:g},{ground_y - height * 0.28:g} '
                f'{tree_x + width / 2:g},{ground_y - height * 0.86:g}" fill="{color}"/>',
                _rect(tree_x + width * 0.44, ground_y - height * 0.12, width * 0.12, height * 0.12, color),
            ]
        )
    return parts


def _forest_poetic_mosaic(theme: Theme) -> str:
    parts = _artistic_svg_start(
        theme,
        "Five coordinated cultural-storytelling slide silhouettes with calligraphic display type, forest-like geometric crops, evidence, and action.",
    )
    display = theme.hero_font or theme.display_font
    body = theme.body_font

    for offset in range(0, 1600, 84):
        parts.append(_line(offset, 0, offset + 230, 900, "#E1E7E3", 0.6))

    parts.extend(
        [
            _rect(24, 24, 842, 852, theme.panel, stroke=theme.border, stroke_width=1),
            _rect(24, 24, 12, 852, theme.accent),
            _text(76, 84, "FOREST POETIC MOSAIC  /  01", size=11, fill=theme.accent, family=body, role="label", weight=700),
            _text(76, 215, "林深处\n见新境", size=112, fill=theme.text, family=display, role="deck-title", weight=700, line_height=0.88),
            _text(82, 445, "FOREST AS A NARRATIVE SYSTEM", size=16, fill="#1D2B26", family="Georgia, Noto Serif SC, serif", role="subheading", weight=700),
            _line(82, 468, 482, 468, theme.border, 2),
            _text(82, 520, "用留白建立信任，用影像切片建立场景，", size=20, fill="#394A43", family=body, role="body"),
            _text(82, 558, "再让证据、人物与行动在同一叙事中汇合。", size=20, fill="#394A43", family=body, role="body"),
            _text(82, 622, "CONTENT KIT", size=11, fill=theme.accent, family=body, role="label", weight=700),
            _text(82, 660, "封面  ·  章节  ·  故事  ·  流程", size=16, fill=theme.text, family=body, role="caption", weight=700),
            _text(82, 694, "证据  ·  比较  ·  决策  ·  结语", size=16, fill=theme.text, family=body, role="caption", weight=700),
            _text(82, 790, "08", size=52, fill=theme.accent, family="Georgia, serif", role="metric", weight=700),
            _text(154, 784, "coordinated story moves", size=14, fill=theme.muted, family=body, role="annotation", weight=700),
            _text(82, 846, "ILLUSTRATIVE TEMPLATE · ORIGINAL VECTOR LANDSCAPE", size=10, fill=theme.muted, family=body, role="source", weight=700),
        ]
    )
    for index in range(8):
        x = 82 + index * 66
        parts.extend(
            [
                _line(x, 730, x + 44, 730, theme.accent if index < 3 else theme.border, 6),
                _text(x, 754, f"0{index + 1}", size=10, fill=theme.muted, family=body, role="page-number", weight=700),
            ]
        )

    parts.extend(
        [
            _rect(890, 24, 686, 412, "#123E30", stroke=theme.border, stroke_width=1),
            '<polygon points="890,24 1240,24 1576,248 1576,436 1340,436 1070,258" fill="#1D5945"/>',
            '<polygon points="1090,24 1576,24 1576,168 1340,238" fill="#6F8F7D"/>',
            '<polygon points="890,292 1110,178 1380,436 890,436" fill="#0B503B"/>',
            '<polygon points="1230,256 1576,168 1576,436 1390,436" fill="#274E3E"/>',
            _line(1108, 24, 1402, 436, "#F5F7F4", 10),
            _line(890, 300, 1334, 24, "#F5F7F4", 10),
            _line(1248, 24, 1576, 234, "#F5F7F4", 10),
        ]
    )
    parts.extend(_tree_cluster(930, 414, scale=0.62, colors=("#071F18", "#0C3226", "#1A4A38"), count=18))
    parts.extend(_tree_cluster(1260, 424, scale=0.48, colors=("#102F25", "#183F31", "#285B46"), count=11))
    parts.extend(
        [
            _rect(918, 64, 390, 102, "#F5F7F4", stroke="#E3E9E5", stroke_width=1),
            _text(944, 102, "把环境变成叙事证据", size=28, fill=theme.text, family=body, role="slide-title", weight=700),
            _text(944, 140, "场景、人物、细节与行动共同回答“为什么”。", size=14, fill=theme.muted, family=body, role="body"),
            _text(1538, 410, "02 / IMAGE-LED STORY", size=10, fill="#E8F0EB", family=body, role="page-number", weight=700, anchor="end"),
        ]
    )

    panel_xs = (890, 1124, 1358)
    panel_titles = (("入境", "一张图建立场所与问题"), ("见证", "让引言、数据与细节相互印证"), ("归纳", "把意义收束为决策与行动"))
    for index, (panel_x, (title, subtitle)) in enumerate(zip(panel_xs, panel_titles, strict=True)):
        parts.extend(
            [
                _rect(panel_x, 460, 218, 416, theme.panel, stroke=theme.border, stroke_width=1),
                _rect(panel_x, 460, 218, 7, theme.accent if index == 0 else (theme.accent_2 if index == 1 else theme.warning)),
                _text(panel_x + 18, 500, f"0{index + 3} / {('OPEN' if index == 0 else 'PROOF' if index == 1 else 'CLOSE')}", size=10, fill=theme.muted, family=body, role="label", weight=700),
                _text(panel_x + 18, 548, title, size=28, fill=theme.text, family=body, role="slide-title", weight=700),
                _text(panel_x + 18, 582, subtitle, size=14, fill=theme.muted, family=body, role="body"),
                _line(panel_x + 18, 610, panel_x + 198, 610, theme.border, 1),
            ]
        )

    parts.extend(
        [
            _text(908, 650, "一句命题", size=16, fill=theme.accent, family=body, role="subheading", weight=700),
            _text(908, 680, "建立叙事起点", size=14, fill=theme.text, family=body, role="body"),
            _text(908, 730, "一个场景", size=16, fill=theme.accent, family=body, role="subheading", weight=700),
            _text(908, 760, "让受众进入问题", size=14, fill=theme.text, family=body, role="body"),
            _text(1142, 650, "“事实不只在表格中，", size=16, fill=theme.text, family=body, role="quote", weight=700),
            _text(1142, 680, "也在被看见的细节中。”", size=16, fill=theme.text, family=body, role="quote", weight=700),
            _text(1142, 730, "03", size=42, fill=theme.accent, family="Georgia, serif", role="metric", weight=700),
            _text(1198, 724, "evidence modes", size=14, fill=theme.muted, family=body, role="annotation", weight=700),
            _text(1376, 648, "优先行动", size=16, fill=theme.text, family=body, role="subheading", weight=700),
            _text(1376, 685, "01  保留场所线索", size=14, fill=theme.text, family=body, role="body"),
            _text(1376, 718, "02  补足人物证言", size=14, fill=theme.text, family=body, role="body"),
            _text(1376, 751, "03  连接可执行下一步", size=14, fill=theme.text, family=body, role="body"),
            _rect(1376, 798, 166, 42, theme.accent),
            _text(1459, 826, "DECIDE / ACT", size=11, fill="#FFFFFF", family=body, role="label", weight=700, anchor="middle"),
            _text(1542, 860, "05", size=10, fill=theme.muted, family=body, role="page-number", weight=700, anchor="end"),
        ]
    )
    parts.append("</svg>")
    return "\n".join(parts) + "\n"


def _silk_ink_strategy(theme: Theme) -> str:
    parts = _artistic_svg_start(
        theme,
        "Five coordinated brand-strategy slide silhouettes with calligraphic hero typography, original mountain abstractions, gold silk motion, metrics, process, comparison, and decision.",
    )
    display = theme.hero_font or theme.display_font
    body = theme.body_font
    parts.extend(
        [
            _rect(24, 24, 1552, 402, theme.panel, stroke=theme.border, stroke_width=1),
            _text(70, 72, "SILK & INK STRATEGY  /  ORIGINAL VECTOR STUDY", size=11, fill=theme.accent, family=body, role="label", weight=700),
            _text(800, 174, "青岚入卷", size=110, fill=theme.text, family=display, role="deck-title", weight=700, anchor="middle"),
            _text(800, 226, "STRATEGY IN MOTION", size=16, fill="#333A36", family="Georgia, Noto Serif SC, serif", role="subheading", weight=700, anchor="middle"),
            _text(800, 262, "以山水建立文化识别，以策略证据支撑每一个结论", size=18, fill=theme.muted, family=body, role="body", anchor="middle"),
            '<polygon points="24,426 24,326 188,244 340,318 498,220 652,328 814,246 964,330 1126,214 1288,312 1434,236 1576,322 1576,426" fill="#B7C9C1"/>',
            '<polygon points="24,426 24,364 210,300 380,368 560,270 742,372 934,294 1112,370 1288,284 1450,356 1576,318 1576,426" fill="#6C9182"/>',
            '<polygon points="24,426 24,390 210,346 402,406 594,338 780,410 978,356 1172,408 1358,344 1576,390 1576,426" fill="#315F53"/>',
        ]
    )
    for offset in range(7):
        y = 304 + offset * 12
        points = f'24,{y} 250,{y - 46 + offset * 3} 504,{y + 10} 748,{y - 54} 996,{y + 14} 1260,{y - 40} 1576,{y + 8}'
        parts.append(f'<polyline points="{points}" fill="none" stroke="{theme.accent_2}" stroke-width="{8 - offset * 0.7:g}" opacity="{0.72 - offset * 0.06:g}"/>')
    parts.extend(
        [
            _rect(1470, 58, 54, 54, "#A63A2E"),
            _text(1497, 94, "策", size=24, fill="#FFFFFF", family=display, role="label", weight=700, anchor="middle"),
            _text(70, 398, "ILLUSTRATIVE TEMPLATE · REPLACE ALL SAMPLE CLAIMS WITH SOURCED CONTENT", size=10, fill="#EEF4F0", family=body, role="source", weight=700),
        ]
    )

    panel_xs = (24, 418, 812, 1206)
    panel_names = (("02", "信号与判断"), ("03", "叙事路径"), ("04", "选择与取舍"), ("05", "决策与行动"))
    for index, (panel_x, (page, title)) in enumerate(zip(panel_xs, panel_names, strict=True)):
        parts.extend(
            [
                _rect(panel_x, 450, 370, 426, theme.panel, stroke=theme.border, stroke_width=1),
                _rect(panel_x, 450, 370, 7, theme.accent_2 if index % 2 else theme.accent),
                _text(panel_x + 24, 488, f"{page} / {('EVIDENCE' if index == 0 else 'FLOW' if index == 1 else 'COMPARE' if index == 2 else 'DECISION')}", size=10, fill=theme.muted, family=body, role="label", weight=700),
                _text(panel_x + 24, 536, title, size=26, fill=theme.text, family=body, role="slide-title", weight=700),
                _line(panel_x + 24, 558, panel_x + 346, 558, theme.border, 1),
            ]
        )

    metrics = (("72%", "核心认知度"), ("+18", "有效触点"), ("03", "增长杠杆"))
    for index, (value, label) in enumerate(metrics):
        y = 604 + index * 82
        parts.extend(
            [
                _text(52, y, value, size=34, fill=theme.accent if index == 0 else theme.text, family="Georgia, serif", role="metric", weight=700),
                _text(162, y - 4, label, size=16, fill=theme.text, family=body, role="subheading", weight=700),
                _text(162, y + 22, "示意指标 · 请换成真实来源", size=12, fill=theme.muted, family=body, role="annotation"),
                _line(52, y + 38, 366, y + 38, theme.border, 1),
            ]
        )

    flow_steps = (("定位", "决定为谁改变什么"), ("成形", "把证据组织成叙事"), ("扩散", "将叙事转换为行动"))
    for index, (name, description) in enumerate(flow_steps):
        y = 606 + index * 88
        parts.extend(
            [
                f'<circle cx="466" cy="{y - 8}" r="22" fill="{theme.accent if index == 0 else theme.surface}" stroke="{theme.accent}" stroke-width="2"/>',
                _text(466, y - 2, f"0{index + 1}", size=12, fill="#FFFFFF" if index == 0 else theme.accent, family=body, role="page-number", weight=700, anchor="middle"),
                _text(504, y - 8, name, size=16, fill=theme.text, family=body, role="subheading", weight=700),
                _text(504, y + 20, description, size=13, fill=theme.muted, family=body, role="body"),
            ]
        )
        if index < 2:
            parts.append(_line(466, y + 16, 466, y + 58, theme.accent_2, 3))

    parts.extend(
        [
            _text(840, 600, "方案 A", size=16, fill=theme.text, family=body, role="subheading", weight=700),
            _text(1022, 600, "方案 B", size=16, fill=theme.text, family=body, role="subheading", weight=700),
        ]
    )
    comparison_rows = (("文化识别", 0.88, 0.62), ("执行速度", 0.58, 0.86), ("资产复用", 0.82, 0.70))
    for index, (label, score_a, score_b) in enumerate(comparison_rows):
        y = 652 + index * 66
        parts.extend(
            [
                _text(840, y, label, size=13, fill=theme.muted, family=body, role="body"),
                _rect(840, y + 14, 130, 9, "#E3E0D6"),
                _rect(840, y + 14, 130 * score_a, 9, theme.accent),
                _rect(1022, y + 14, 130, 9, "#E3E0D6"),
                _rect(1022, y + 14, 130 * score_b, 9, theme.accent_2),
            ]
        )
    parts.extend(
        [
            _text(1234, 604, "建议", size=16, fill=theme.accent, family=body, role="subheading", weight=700),
            _text(1234, 646, "先统一品牌叙事，", size=18, fill=theme.text, family=body, role="body", weight=700),
            _text(1234, 681, "再扩展内容与渠道。", size=18, fill=theme.text, family=body, role="body", weight=700),
            _rect(1234, 724, 316, 2, theme.border),
            _text(1234, 766, "01  锁定一句核心命题", size=13, fill=theme.text, family=body, role="body"),
            _text(1234, 800, "02  统一视觉与证据语法", size=13, fill=theme.text, family=body, role="body"),
            _text(1234, 834, "03  按优先级分配负责人", size=13, fill=theme.text, family=body, role="body"),
        ]
    )
    parts.append("</svg>")
    return "\n".join(parts) + "\n"


def _museum_cultural_editorial(theme: Theme) -> str:
    parts = _artistic_svg_start(
        theme,
        "Seven coordinated museum-editorial slide silhouettes with calligraphic hero type, artifact-like geometry, chronology, interpretation, evidence, comparison, and public action.",
    )
    display = theme.hero_font or theme.display_font
    body = theme.body_font
    parts.extend(
        [
            _rect(24, 24, 610, 852, "#291F1B", stroke=theme.border, stroke_width=1),
            f'<circle cx="330" cy="512" r="208" fill="#392923" stroke="{theme.accent_2}" stroke-width="2"/>',
            '<circle cx="330" cy="512" r="154" fill="#241A17" stroke="#6F584B" stroke-width="14"/>',
            '<polygon points="330,354 414,420 392,584 330,678 268,584 246,420" fill="#A33B30" stroke="#D6B66F" stroke-width="5"/>',
            '<polygon points="330,392 378,438 364,546 330,612 296,546 282,438" fill="#D1A85F"/>',
            _text(62, 78, "MUSEUM CULTURAL EDITORIAL  /  01", size=11, fill=theme.accent_2, family=body, role="label", weight=700),
            _text(76, 218, "器物\n与时间", size=104, fill=theme.text, family=display, role="deck-title", weight=700, line_height=0.9),
            _text(78, 394, "OBJECTS / MEMORY / PUBLIC MEANING", size=16, fill="#D9CCBF", family="Georgia, Noto Serif SC, serif", role="subheading", weight=700),
            _text(78, 736, "不只展示一件物，", size=18, fill=theme.text, family=body, role="body", weight=700),
            _text(78, 770, "而是解释它如何连接过去与当下。", size=18, fill=theme.text, family=body, role="body", weight=700),
            _text(78, 844, "ILLUSTRATIVE TEMPLATE · ORIGINAL ABSTRACT ARTIFACT", size=10, fill=theme.muted, family=body, role="source", weight=700),
        ]
    )
    for index in range(12):
        angle_x = 132 + index * 34
        parts.append(_line(angle_x, 476, 330, 512, "#5D463B", 1))

    parts.extend(
        [
            _rect(658, 24, 918, 232, theme.surface, stroke=theme.border, stroke_width=1),
            _rect(658, 24, 12, 232, theme.accent),
            _text(696, 66, "02 / INTERPRET", size=10, fill=theme.accent, family=body, role="label", weight=700),
            _text(696, 114, "一件器物，承载三层时间", size=26, fill="#291F1B", family=body, role="slide-title", weight=700),
            _text(696, 154, "材料记录工艺，痕迹记录使用，流传记录社会关系。", size=14, fill="#6C5D54", family=body, role="body"),
        ]
    )
    timeline = (("材料", "它由什么被制作"), ("痕迹", "谁使用过它"), ("流传", "它如何进入公共记忆"))
    for index, (name, description) in enumerate(timeline):
        x = 716 + index * 276
        parts.extend(
            [
                f'<circle cx="{x}" cy="206" r="12" fill="{theme.accent if index == 1 else theme.accent_2}"/>',
                _line(x + 16, 206, x + 238, 206, "#D9CFC1", 2),
                _text(x + 24, 198, name, size=16, fill="#291F1B", family=body, role="subheading", weight=700),
                _text(x + 24, 226, description, size=13, fill="#776A61", family=body, role="annotation"),
            ]
        )

    mid_panels = ((658, "03", "物证档案"), (1126, "04", "观点对话"))
    for panel_x, page, title in mid_panels:
        parts.extend(
            [
                _rect(panel_x, 280, 450, 278, theme.panel, stroke=theme.border, stroke_width=1),
                _text(panel_x + 24, 320, f"{page} / EVIDENCE", size=10, fill=theme.accent_2, family=body, role="label", weight=700),
                _text(panel_x + 24, 362, title, size=26, fill=theme.text, family=body, role="slide-title", weight=700),
                _line(panel_x + 24, 384, panel_x + 426, 384, theme.border, 1),
            ]
        )
    parts.extend(
        [
            _rect(686, 408, 132, 116, "#3A2B25", stroke="#6F584B", stroke_width=2),
            '<circle cx="752" cy="466" r="40" fill="#A43B2F" stroke="#D0AD68" stroke-width="4"/>',
            _text(842, 430, "编号", size=16, fill=theme.accent_2, family=body, role="subheading", weight=700),
            _text(842, 458, "A-017 / 金属与漆木", size=13, fill=theme.text, family=body, role="body"),
            _text(842, 490, "观察", size=16, fill=theme.accent_2, family=body, role="subheading", weight=700),
            _text(842, 518, "磨损集中在持握与边缘", size=13, fill=theme.text, family=body, role="body"),
            _text(1154, 420, "“物的价值，", size=18, fill=theme.text, family=body, role="quote", weight=700),
            _text(1154, 456, "不在稀缺本身，", size=18, fill=theme.text, family=body, role="quote", weight=700),
            _text(1154, 492, "而在它让哪段历史可被理解。”", size=18, fill=theme.text, family=body, role="quote", weight=700),
            _text(1154, 532, "— 策展观点示意", size=13, fill=theme.muted, family=body, role="annotation"),
        ]
    )

    bottom_xs = (658, 966, 1274)
    bottom_titles = (("05", "时间线"), ("06", "取舍矩阵"), ("07", "公共行动"))
    for index, (panel_x, (page, title)) in enumerate(zip(bottom_xs, bottom_titles, strict=True)):
        parts.extend(
            [
                _rect(panel_x, 582, 284, 294, theme.panel, stroke=theme.border, stroke_width=1),
                _rect(panel_x, 582, 284, 7, theme.accent if index == 2 else theme.accent_2),
                _text(panel_x + 20, 620, f"{page} / {('TIME' if index == 0 else 'CHOICE' if index == 1 else 'ACTION')}", size=10, fill=theme.muted, family=body, role="label", weight=700),
                _text(panel_x + 20, 662, title, size=26, fill=theme.text, family=body, role="slide-title", weight=700),
            ]
        )
    for index, (year, note) in enumerate((("1932", "制作"), ("1986", "收藏"), ("2026", "再诠释"))):
        y = 714 + index * 52
        parts.extend(
            [
                _text(682, y, year, size=16, fill=theme.accent_2, family="Georgia, serif", role="subheading", weight=700),
                _line(740, y - 7, 796, y - 7, theme.border, 2),
                _text(812, y, note, size=13, fill=theme.text, family=body, role="body"),
            ]
        )
    matrix_labels = (("稀缺", 1010, 718), ("共鸣", 1140, 718), ("研究", 1010, 808), ("公共", 1140, 808))
    parts.extend(
        [
            _rect(994, 694, 228, 146, "#332722", stroke=theme.border, stroke_width=1),
            _line(1108, 704, 1108, 830, theme.border, 1),
            _line(1004, 767, 1212, 767, theme.border, 1),
        ]
    )
    for label, x, y in matrix_labels:
        parts.append(_text(x, y, label, size=13, fill=theme.text, family=body, role="body", weight=700))
    parts.extend(
        [
            f'<circle cx="1166" cy="738" r="13" fill="{theme.accent_2}"/>',
            f'<circle cx="1142" cy="794" r="10" fill="{theme.accent}"/>',
            _text(1294, 718, "01  建立物证档案", size=13, fill=theme.text, family=body, role="body"),
            _text(1294, 758, "02  开放多方解读", size=13, fill=theme.text, family=body, role="body"),
            _text(1294, 798, "03  连接教育项目", size=13, fill=theme.text, family=body, role="body"),
            _rect(1294, 828, 238, 30, theme.accent),
            _text(1413, 849, "OWNER · PROGRAM · DATE", size=10, fill="#FFFFFF", family=body, role="source", weight=700, anchor="middle"),
        ]
    )
    parts.append("</svg>")
    return "\n".join(parts) + "\n"


def build_contact_sheet(theme: Theme) -> str:
    if theme.slug == "forest-poetic-mosaic":
        return _forest_poetic_mosaic(theme)
    if theme.slug == "silk-ink-strategy":
        return _silk_ink_strategy(theme)
    if theme.slug == "museum-cultural-editorial":
        return _museum_cultural_editorial(theme)
    parts = [
        '<svg xmlns="http://www.w3.org/2000/svg" width="1600" height="900" '
        'viewBox="0 0 1600 900">',
        f'<title>{escape(theme.name)} template contact sheet</title>',
        f'<desc>Four information-rich slide references with locked typography roles for {escape(theme.name)}.</desc>',
        _rect(0, 0, 1600, 900, theme.field),
    ]
    parts.extend(_rich_cover(theme, 24, 24))
    parts.extend(_rich_process(theme, 816, 24, "05"))
    parts.extend(_rich_evidence(theme, 24, 460, "06"))
    parts.extend(_rich_decision(theme, 816, 460, "09"))
    parts.append("</svg>")
    return "\n".join(parts) + "\n"


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Regenerate VectorDeckPPT style templates")
    parser.add_argument("output_dir", type=Path, help="Directory for SVG and PNG assets")
    return parser


def main(argv: Sequence[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    output_dir = args.output_dir.expanduser().resolve()
    output_dir.mkdir(parents=True, exist_ok=True)
    for theme in THEMES:
        theme_dir = output_dir / theme.slug
        theme_dir.mkdir(parents=True, exist_ok=True)
        overview_path = theme_dir / "overview.svg"
        overview_path.write_text(build_contact_sheet(theme), encoding="utf-8")
        render_svg(overview_path, theme_dir / "overview.png")
        slides_dir = theme_dir / "slides"
        slides_dir.mkdir(parents=True, exist_ok=True)
        for filename, svg in build_template_pages(theme).items():
            svg_path = slides_dir / filename
            svg_path.write_text(svg, encoding="utf-8")
            render_svg(svg_path, svg_path.with_suffix(".png"))
        print(f"generated {theme.slug}/overview and ten slide pairs")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
