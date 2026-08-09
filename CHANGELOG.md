# Changelog

All notable changes to VectorDeckPPT are documented in this file.

## [1.0.0] - 2026-08-09

### Added

- Agent Skill workflow for source reading, narrative planning, art direction, slide authoring, visual review, and delivery.
- Dedicated aesthetic guidance covering visual theses, meaning-to-form decisions, composition, typography, color, imagery, pacing, and anti-patterns.
- Deterministic SVG parsing, safety validation, rendering, and structured diagnostics.
- Editable SVG-to-PowerPoint conversion for text, basic shapes, lines, images, groups, style inheritance, and coordinate mapping.
- Office SVG fallback with compatibility previews for visible elements that cannot be converted natively.
- Multi-slide compilation reports and PPTX package validation.
- A five-slide editable example deck and end-to-end validation coverage.

### Quality

- SVG remains the visual source of truth, with one SVG per slide.
- Unsupported visible elements are converted, preserved through explicit fallback, or reported as failures; they are never silently dropped.
- The example workflow validates, renders, compiles, reopens, and validates the final PPTX.

[1.0.0]: https://github.com/AaaBinfinity/VectorDeckPPT/releases/tag/v1.0.0
