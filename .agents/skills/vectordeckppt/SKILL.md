---
name: vectordeckppt
description: Create, redesign, improve, and export high-quality editable PowerPoint presentations with a vector-first workflow. Use when the user asks for a PPT, PPTX, PowerPoint, presentation, slides, slide deck, 演示文稿, 答辩 PPT, 汇报 PPT, 路演 PPT, 生成幻灯片, 重新设计 PPT, or 美化 PPT; especially when building a deck from Markdown, PDF, DOCX, spreadsheets, images, screenshots, research, or an existing presentation. Plan the narrative and shared design system, author one structured SVG per slide, validate and render previews, visually review revisions, compile supported elements into native PowerPoint objects, and deliver a validated editable PPTX.
---

# VectorDeckPPT

Create the presentation as the host Agent. Do not call another AI API. Use the bundled scripts only for deterministic validation, rendering, compilation, and PPTX inspection.

## Read references progressively

- Read [workflow.md](references/workflow.md) before every deck task.
- Read [presentation-planning.md](references/presentation-planning.md) when defining the audience, storyline, sections, or slide purposes.
- Read [design-system.md](references/design-system.md) and [slide-design.md](references/slide-design.md) before designing slides.
- Read [svg-authoring.md](references/svg-authoring.md) before writing or revising any SVG.
- Read [visual-review.md](references/visual-review.md) before inspecting rendered previews.
- Read [svg-to-pptx.md](references/svg-to-pptx.md) before using compiler-specific features or diagnosing editability.
- Read [troubleshooting.md](references/troubleshooting.md) only when a validation, render, font, image, or PPTX problem occurs.

## Required workflow

1. Understand the request. Determine purpose, audience, language, presentation type, approximate slide count, visual preference, source material, and required assets. Infer safe defaults instead of blocking on non-critical omissions.
2. Read every relevant source. Extract the core claim, evidence, important numbers, charts, image assets, constraints, and narrative opportunities. Never design before reading supplied material.
3. Write a presentation plan. Record the title, audience, purpose, language, slide count, storyline, sections, and one sentence describing the purpose and key message of every slide.
4. Define one art direction and one shared design system before authoring slides. Lock the canvas, colors, typography, spacing, shape language, imagery, icon treatment, and density.
5. Plan each slide immediately before design: purpose, key message, content hierarchy, visual structure, and required assets.
6. Author one complete `1600x900` SVG for each 16:9 slide. Keep visible text as `<text>`/`<tspan>` and remain inside the supported subset in `svg-authoring.md`.
7. Validate each SVG after creation:

   ```bash
   uv run python .agents/skills/vectordeckppt/scripts/validate_svg.py slide_01.svg --json
   ```

8. Render each valid SVG, then inspect the actual PNG:

   ```bash
   uv run python .agents/skills/vectordeckppt/scripts/render_svg.py slide_01.svg
   ```

9. Review layout, typography, spacing, alignment, hierarchy, contrast, balance, consistency, density, image quality, and overflow. Revise, validate, and render again until the slide is presentation-ready. Do not equate “no overflow” with visual quality.
10. Repeat steps 5–9 for every slide while maintaining the shared design system.
11. Compile slides in filename order and keep the JSON compilation report:

    ```bash
    uv run python .agents/skills/vectordeckppt/scripts/compile_pptx.py slides/ --output final.pptx --report compilation-report.json
    ```

12. Validate the result and open or render it when the environment supports PowerPoint/PDF inspection:

    ```bash
    uv run python .agents/skills/vectordeckppt/scripts/validate_pptx.py final.pptx --json
    ```

13. Deliver the `.pptx`, the source slide SVGs, and any compilation warnings that affect editability. Do not claim full editability when the report contains embedded SVG fallbacks.

## Non-negotiable constraints

- Treat one SVG as one full slide and as the visual source of truth.
- Prefer native PowerPoint text and shapes; use embedded SVG fallback only for visible elements that cannot be converted reliably.
- Never rasterize the whole slide as the default compilation path.
- Never silently omit unsupported elements.
- Keep Chinese and other user-facing text editable whenever possible.
- Preserve image aspect ratio and use local or embedded assets only; never depend on remote URLs.
- Do not use scripts, `foreignObject`, animation, remote fonts, browser-only CSS, or interactive SVG.
- Do not leave temporary versions or preview artifacts in the final delivery folder.

## Completion gate

Finish only when every SVG validates, every preview has been visually inspected, the complete deck compiles, the compilation report has zero failed elements, the PPTX validator passes, slide order/count are correct, and the user receives a readable summary of any intentional fallback.
