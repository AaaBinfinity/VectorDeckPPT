# VectorDeckPPT Repository Guide

## Architecture invariants

- VectorDeckPPT is an Agent Skill, not an AI API application.
- Do not introduce AI provider SDKs unless the product requirements explicitly change.
- `SKILL.md` and `references/` define Agent behavior; `scripts/` contain deterministic utilities only.
- One SVG represents one slide, and SVG is the visual source of truth.
- Preserve editability when compiling PPTX. Prefer native PowerPoint objects, then embedded SVG fallback.
- Never silently drop a visible unsupported SVG element. Convert it, fall back, or fail with a clear report.
- Keep the supported SVG subset intentionally constrained and document compiler behavior truthfully.
- Centralize SVG-to-PowerPoint coordinate conversion in `scripts/lib/coordinates.py`.
- Keep source reading, presentation planning, art direction, and visual review in the host Agent workflow.

## Development workflow

1. Read `doc/PRD.md` and the relevant Skill references before changing behavior.
2. Work directly on `main` by default. Do not create another local or remote branch unless the user explicitly requests one.
3. Inspect `git status` and preserve unrelated user changes.
4. Use `uv` to maintain `uv.lock`, and keep `requirements.txt` synchronized so a standard `pip install -r requirements.txt` environment remains supported.
5. Add or update tests with every deterministic behavior change.
6. Before each commit, run:

   ```bash
   git diff --check
   uv run ruff check .
   uv run pytest
   ```

7. Use small Conventional Commits with an English type/scope/summary.

Do not use destructive Git commands, rewrite unrelated history, commit generated `output/` artifacts, or force-push without an explicit request.

## Code conventions

- Target Python 3.12+ and keep public functions type annotated.
- Keep CLI entry files thin; reusable logic belongs in `scripts/lib/`.
- Resolve user paths explicitly and report failures with actionable context.
- Parse XML with network access and entity expansion disabled.
- Keep JSON CLI output stable enough for Agent consumption.
- Prefer deterministic fixtures over brittle pixel-perfect assertions.

## Testing expectations

Cover XML parsing, validation diagnostics, unsupported tags, remote/image paths, coordinate conversion, text and shape parsing, SVG rendering, editable PPTX generation, multi-slide order, compilation reports, and PPTX package validation. The end-to-end example must validate, render, compile, reopen with `python-pptx`, and pass PPTX validation.
