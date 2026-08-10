from pathlib import Path

from lib.typography_audit import audit_typography


def _write_svg(path: Path, texts: list[str]) -> None:
    content = "\n".join(texts)
    path.write_text(
        f'<svg xmlns="http://www.w3.org/2000/svg" width="1600" height="900" '
        f'viewBox="0 0 1600 900">{content}</svg>',
        encoding="utf-8",
    )


def test_typography_audit_accepts_shared_deck_tokens(tmp_path: Path) -> None:
    for index in (1, 2):
        _write_svg(
            tmp_path / f"slide_{index:02d}.svg",
            [
                '<text data-role="slide-title" x="96" y="100" '
                'font-family="Arial" font-size="52" font-weight="700">Title</text>',
                '<text data-role="subheading" x="96" y="180" '
                'font-family="Arial" font-size="30">Heading A</text>',
                '<text data-role="subheading" x="600" y="180" '
                'font-family="Arial" font-size="30">Heading B</text>',
                '<text data-role="body" x="96" y="240" '
                'font-family="Arial" font-size="24">Body</text>',
            ],
        )

    result = audit_typography(tmp_path, strict=True)

    assert result.valid
    assert result.to_dict()["tokens"]["slide-title"] == [52.0]


def test_typography_audit_rejects_inconsistent_deck_titles(tmp_path: Path) -> None:
    _write_svg(
        tmp_path / "slide_01.svg",
        [
            '<text data-role="slide-title" x="96" y="100" '
            'font-family="Arial" font-size="52" font-weight="700">First</text>'
        ],
    )
    _write_svg(
        tmp_path / "slide_02.svg",
        [
            '<text data-role="slide-title" x="96" y="100" '
            'font-family="Arial" font-size="48" font-weight="600">Second</text>'
        ],
    )

    result = audit_typography(tmp_path, strict=True)

    assert not result.valid
    codes = {item.code for item in result.errors}
    assert "inconsistent_deck_size" in codes
    assert "inconsistent_deck_title_weight" in codes


def test_typography_audit_rejects_peer_heading_mismatch_and_missing_role(
    tmp_path: Path,
) -> None:
    _write_svg(
        tmp_path / "slide_01.svg",
        [
            '<text data-role="subheading" x="96" y="180" font-size="30">A</text>',
            '<text data-role="subheading" x="600" y="180" font-size="28">B</text>',
            '<text x="96" y="260" font-size="24">Unclassified</text>',
        ],
    )

    result = audit_typography(tmp_path, strict=True)

    assert not result.valid
    codes = {item.code for item in result.errors}
    assert "inconsistent_peer_size" in codes
    assert "missing_text_role" in codes
