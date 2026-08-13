# Changelog

All notable changes to VectorDeckPPT are documented in this file.

## [Unreleased]

## [1.2.0] - 2026-08-13

### Added

- Added a deterministic deck typography audit with strict semantic text roles and diagnostics for inconsistent slide titles or same-page peer headings.
- Added Data-Forward Clarity, Premium Restraint, Product Storytelling, Dynamic Hero Editorial, Forest Poetic Mosaic, Silk & Ink Strategy, and Museum Cultural Editorial art-direction families.
- Added ten full-size SVG/PNG reference pages per bundled family, organized in a dedicated family directory alongside an overview, including cover, section, narrative, context, process, evidence, comparison, roadmap, decision, and close.

### Changed

- Rebuilt the style references as multi-page, information-rich template families instead of one-image contact sheets or sparse placeholder lines.
- Strengthened the default content contract around claim, explanation, evidence/example, and implication/action, with meaningful visuals on roughly two thirds of core slides when sources permit.
- Locked recurring typography roles to exact deck tokens and prohibited one-off font-size changes used only to make text fit.
- Added an explicit complete-request confirmation gate before source synthesis or slide planning, and made controlled asymmetry, hero typography, crop, overlap, arcs, and diagonals part of the optional art-direction vocabulary without weakening professional defaults.
- Added a required visual-source choice: select a bundled family, upload a PPT/PPTX/PDF/image/screenshot/brand reference, approve a two-source hybrid, or explicitly delegate selection to the Agent. Without a reference, the Agent presents three curated candidates with tradeoffs.
- Separated artistic `deck-title`/`section-title` roles from ordinary slide titles and body typography so calligraphic or display treatments remain expressive without weakening professional readability.

### Documentation

- Redesigned the README as a visual product overview with real generated slide previews, quick navigation, capability boundaries, and a shorter getting-started path.
- Added a documentation index and moved reusable request templates into a dedicated prompt examples guide.
- Synchronized the PRD, documentation index, prompt examples, and usage guide with the twelve-family multi-page library, visual-source confirmation, information-rich content contract, artistic-type roles, and strict typography audit.
- Added a task-oriented user guide and contributor guide covering installation modes, approval gates, quality commands, documentation synchronization, dependency export, and release checks.
- Corrected pip CLI guidance and aligned the documented requirements export command with the generated file header.

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

[Unreleased]: https://github.com/AaaBinfinity/VectorDeckPPT/compare/v1.2.0...HEAD
[1.2.0]: https://github.com/AaaBinfinity/VectorDeckPPT/compare/v1.1.0...v1.2.0
[1.1.0]: https://github.com/AaaBinfinity/VectorDeckPPT/compare/v1.0.0...v1.1.0
[1.0.0]: https://github.com/AaaBinfinity/VectorDeckPPT/releases/tag/v1.0.0
