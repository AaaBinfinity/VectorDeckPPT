# Changelog

All notable changes to VectorDeckPPT are documented in this file.

## [Unreleased]

### Documentation

- Redesigned the README as a visual product overview with real generated slide previews, quick navigation, capability boundaries, and a shorter getting-started path.
- Added a documentation index and moved reusable request templates into a dedicated prompt examples guide.

## [1.1.0] - 2026-08-09

### Added

- Mandatory staged approvals for the complete text-only deck and a representative visual sample before full production.
- Five bundled 16:9 art-direction references for bright technology, editorial research, dark engineering, human documentary, and expressive cultural work.
- Information-rich default slide planning with evidence-led charts, diagrams, comparisons, and explanatory copy without invented data.
- Editable PowerPoint freeform conversion for straight-segment SVG `polygon` and `polyline` elements.
- A locked `requirements.txt` workflow for standard `pip install -r requirements.txt` environments.
- A ten-slide editable project-introduction example.
- A tag-driven GitHub Actions workflow that publishes reviewed release notes with the repository-scoped `GITHUB_TOKEN`.

### Changed

- Deck artifacts now default to `./pptoutput/`, with explicit `SKILL_ROOT` and `DECK_ROOT` resolution for repository and global Skill installs.
- Presentation requests with material ambiguity now pause for focused clarification.
- SVG-to-PPTX output and report paths are preflighted for required extensions, resolved aliases, and hard-link collisions.
- Documentation now reflects the compiler's viewBox-based font scaling and current editable SVG support matrix.

### Fixed

- Corrected SVG font-size conversion so text follows the same viewBox-to-slide scale as geometry.
- Removed pretty-print-only SVG whitespace from compiled PowerPoint text while preserving `xml:space="preserve"` content.
- Preserved supported SVG `stroke-linecap` and `stroke-linejoin` styling in native PowerPoint shapes.
- Routed unsupported non-alphabetic text baselines through explicit Office SVG fallback instead of silently changing their appearance.
- Recompiled tracked example decks with the current typography and compiler behavior.

### Quality

- Added regression coverage for font scaling, freeform conversion, output path safety, dependency export, template assets, approval gates, content density, text whitespace, line styling, and PPTX behavior.

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

[Unreleased]: https://github.com/AaaBinfinity/VectorDeckPPT/compare/v1.1.0...HEAD
[1.1.0]: https://github.com/AaaBinfinity/VectorDeckPPT/compare/v1.0.0...v1.1.0
[1.0.0]: https://github.com/AaaBinfinity/VectorDeckPPT/releases/tag/v1.0.0
