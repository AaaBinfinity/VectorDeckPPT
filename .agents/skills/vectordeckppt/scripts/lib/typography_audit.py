from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

from .svg_parser import iter_render_elements, parse_length, parse_svg

ALLOWED_ROLES = {
    "deck-title",
    "slide-title",
    "section-title",
    "subheading",
    "body",
    "label",
    "metric",
    "caption",
    "source",
    "quote",
    "annotation",
    "page-number",
}

DECK_LOCKED_ROLES = {
    "slide-title",
    "section-title",
    "subheading",
    "body",
    "label",
    "caption",
    "source",
    "annotation",
    "page-number",
}


@dataclass(frozen=True, slots=True)
class TypographyDiagnostic:
    code: str
    message: str
    source: Path | None = None
    line: int | None = None
    role: str | None = None

    def to_dict(self) -> dict[str, Any]:
        result: dict[str, Any] = {"code": self.code, "message": self.message}
        if self.source is not None:
            result["source"] = str(self.source)
        if self.line is not None:
            result["line"] = self.line
        if self.role is not None:
            result["role"] = self.role
        return result


@dataclass(frozen=True, slots=True)
class TypographyObservation:
    source: Path
    line: int | None
    role: str
    text: str
    font_size: float
    font_family: str
    font_weight: str


@dataclass(slots=True)
class TypographyAuditResult:
    sources: list[Path] = field(default_factory=list)
    observations: list[TypographyObservation] = field(default_factory=list)
    errors: list[TypographyDiagnostic] = field(default_factory=list)
    warnings: list[TypographyDiagnostic] = field(default_factory=list)

    @property
    def valid(self) -> bool:
        return not self.errors

    def add_error(self, code: str, message: str, **context: Any) -> None:
        self.errors.append(TypographyDiagnostic(code, message, **context))

    def add_warning(self, code: str, message: str, **context: Any) -> None:
        self.warnings.append(TypographyDiagnostic(code, message, **context))

    def to_dict(self) -> dict[str, Any]:
        tokens: dict[str, list[float]] = {}
        for item in self.observations:
            tokens.setdefault(item.role, [])
            if item.font_size not in tokens[item.role]:
                tokens[item.role].append(item.font_size)
        return {
            "valid": self.valid,
            "sources": [str(path) for path in self.sources],
            "tokens": {
                role: sorted(values)
                for role, values in sorted(tokens.items())
            },
            "errors": [item.to_dict() for item in self.errors],
            "warnings": [item.to_dict() for item in self.warnings],
        }


def discover_svg_sources(source: str | Path) -> list[Path]:
    path = Path(source).expanduser().resolve()
    if path.is_file():
        return [path]
    if path.is_dir():
        return sorted(path.glob("*.svg"), key=lambda item: item.name.casefold())
    return []


def audit_typography(source: str | Path, *, strict: bool = False) -> TypographyAuditResult:
    result = TypographyAuditResult()
    sources = discover_svg_sources(source)
    result.sources.extend(sources)
    if not sources:
        result.add_error(
            "no_svg_sources",
            f"No SVG files found at: {Path(source).expanduser().resolve()}",
        )
        return result

    for path in sources:
        _collect_observations(path, result, strict=strict)

    _check_slide_peer_sizes(result)
    _check_deck_tokens(result)
    return result


def _collect_observations(
    source: Path,
    result: TypographyAuditResult,
    *,
    strict: bool,
) -> None:
    try:
        document = parse_svg(source)
    except ValueError as exc:
        result.add_error("svg_parse_error", str(exc), source=source)
        return

    for item in iter_render_elements(document):
        if item.tag != "text":
            continue
        text = " ".join("".join(item.element.itertext()).split())
        if not text:
            continue
        role = (item.element.get("data-role") or "").strip().lower()
        if not role:
            diagnostic = {
                "source": source,
                "line": item.element.sourceline,
            }
            message = f"Visible text is missing data-role: {text[:60]!r}"
            if strict:
                result.add_error("missing_text_role", message, **diagnostic)
            else:
                result.add_warning("missing_text_role", message, **diagnostic)
            continue
        if role not in ALLOWED_ROLES:
            result.add_error(
                "unknown_text_role",
                f"Unknown data-role {role!r} on text {text[:60]!r}",
                source=source,
                line=item.element.sourceline,
                role=role,
            )
            continue
        try:
            font_size = parse_length(item.styles.get("font-size")) or 16.0
        except ValueError as exc:
            result.add_error(
                "invalid_font_size",
                str(exc),
                source=source,
                line=item.element.sourceline,
                role=role,
            )
            continue
        result.observations.append(
            TypographyObservation(
                source=source,
                line=item.element.sourceline,
                role=role,
                text=text,
                font_size=font_size,
                font_family=item.styles.get("font-family", "").strip(),
                font_weight=item.styles.get("font-weight", "normal").strip().lower(),
            )
        )


def _check_slide_peer_sizes(result: TypographyAuditResult) -> None:
    grouped: dict[tuple[Path, str], list[TypographyObservation]] = {}
    for item in result.observations:
        grouped.setdefault((item.source, item.role), []).append(item)

    for (source, role), items in grouped.items():
        if role in {"deck-title", "metric", "quote"}:
            continue
        sizes = sorted({item.font_size for item in items})
        if len(sizes) > 1:
            result.add_error(
                "inconsistent_peer_size",
                f"Peer texts with role {role!r} use multiple sizes on one slide: {sizes}",
                source=source,
                role=role,
            )


def _check_deck_tokens(result: TypographyAuditResult) -> None:
    grouped: dict[str, list[TypographyObservation]] = {}
    for item in result.observations:
        if item.role in DECK_LOCKED_ROLES:
            grouped.setdefault(item.role, []).append(item)

    for role, items in grouped.items():
        sizes = sorted({item.font_size for item in items})
        if len(sizes) > 1:
            result.add_error(
                "inconsistent_deck_size",
                f"Deck role {role!r} must use one exact size, found: {sizes}",
                role=role,
            )
        if role != "slide-title":
            continue
        families = sorted({item.font_family for item in items})
        weights = sorted({item.font_weight for item in items})
        if len(families) > 1:
            result.add_error(
                "inconsistent_deck_title_family",
                f"Slide titles must use one font family, found: {families}",
                role=role,
            )
        if len(weights) > 1:
            result.add_error(
                "inconsistent_deck_title_weight",
                f"Slide titles must use one font weight, found: {weights}",
                role=role,
            )
