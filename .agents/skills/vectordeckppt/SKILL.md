---
name: vectordeckppt
description: Create, redesign, improve, and export high-quality editable PowerPoint presentations with a vector-first workflow. Use when the user asks for a PPT, PPTX, PowerPoint, presentation, slides, slide deck, 演示文稿, 答辩 PPT, 汇报 PPT, 路演 PPT, 生成幻灯片, 重新设计 PPT, or 美化 PPT; especially when building a deck from Markdown, PDF, DOCX, spreadsheets, images, screenshots, research, or an existing presentation. Plan the narrative and shared design system, author one structured SVG per slide, validate and render previews, visually review revisions, compile supported elements into native PowerPoint objects, and deliver a validated editable PPTX.
---

# VectorDeckPPT

Create the presentation as the host Agent. Do not call another AI API. Use the bundled scripts only for deterministic validation, rendering, compilation, and PPTX inspection.

## Read references progressively

- Read [workflow.md](references/workflow.md) before every deck task.
- Read [presentation-planning.md](references/presentation-planning.md) when defining the audience, storyline, sections, or slide purposes.
- Read [art-direction.md](references/art-direction.md), [design-system.md](references/design-system.md), and [slide-design.md](references/slide-design.md) before designing slides.
- Read [style-templates.md](references/style-templates.md) when the user asks for a template, redesign, richer aesthetics, a named visual style, or provides no useful art direction. Inspect the selected PNG in `assets/style-templates/` with `view_image` before defining the design system.
- Read [svg-authoring.md](references/svg-authoring.md) before writing or revising any SVG.
- Read [visual-review.md](references/visual-review.md) before inspecting rendered previews.
- Read [svg-to-pptx.md](references/svg-to-pptx.md) before using compiler-specific features or diagnosing editability.
- Read [troubleshooting.md](references/troubleshooting.md) only when a validation, render, font, image, or PPTX problem occurs.

## Required workflow

1. Set the task output root to `./pptoutput/` under the current working directory unless the user explicitly provides another location. Keep every artifact for this deck inside that root.
2. Establish a reliable request contract: audience identity/role and knowledge level, intended outcome, source material, language, approximate slide count, presentation setting, visual direction, brand constraints, required facts, and deliverables. If the request is malformed, self-contradictory, factually suspect, or materially ambiguous, ask focused questions and wait. Infer only harmless omissions that cannot change the narrative or visual direction.
3. Read every relevant source. Extract the core claim, evidence, important numbers, charts, image assets, constraints, contradictions, and narrative opportunities. Never design before reading supplied material.
4. Produce the complete text-only slide draft before authoring SVG. Present it to the user and save `pptoutput/slide-content.md`. For every slide include number, takeaway title, purpose, key message, audience-facing content, evidence/source, and proposed visual form.
5. Ask the user to approve or revise the text-only draft. Stop at this gate. Do not create slide SVGs, PNG previews, or a PPTX until the user explicitly approves the slide content.
6. After content approval, define one visual thesis and one shared design system. Translate the subject and audience into typography, spatial behavior, imagery, color, geometry, and pacing. When using a bundled style template, extract its observable design behavior into tokens and composition rules; never use the reference PNG as a full-slide background or substitute for editable SVG construction.
7. Select exactly three representative slides for visual prototyping: the opening, a representative core-content page, and the most visually demanding evidence/diagram page. For decks shorter than three pages, select every page. State which pages were selected and why.
8. Generate only those sample pages under `pptoutput/sample/slides/`, validate them, render PNGs under `pptoutput/sample/preview/`, inspect the actual previews, and present them to the user. Do not generate the remaining pages or final PPTX yet.
9. Ask the user to approve the three-page visual direction or request changes. Stop at this gate and iterate on the sample pages until the user explicitly approves them. Text approval does not imply visual approval, and silence does not imply either approval.
10. After both approvals, plan each remaining slide immediately before design: purpose, key message, evidence, content hierarchy, dominant visual, composition, required assets, and intended transition from the previous page. Select form from meaning; do not force every page into cards or a repeated template.
11. Author every final `1600x900` slide SVG under `pptoutput/slides/`, reusing approved sample designs where appropriate. Keep visible text as `<text>`/`<tspan>` and remain inside the supported subset in `svg-authoring.md`.
12. Validate each SVG after creation:

   ```bash
   uv run python .agents/skills/vectordeckppt/scripts/validate_svg.py pptoutput/slides/slide_01.svg --json
   ```

13. Render each valid SVG to `pptoutput/preview/`, then inspect the actual PNG:

   ```bash
   uv run python .agents/skills/vectordeckppt/scripts/render_svg.py pptoutput/slides/ --output-dir pptoutput/preview/
   ```

14. Review layout, typography, spacing, alignment, hierarchy, contrast, balance, consistency, density, image quality, overflow, visual character, subject fitness, and narrative function. Revise, validate, and render again until the slide is presentation-ready. Do not equate “no overflow” with visual quality.
15. Compile slides in filename order and keep the JSON compilation report:

    ```bash
    uv run python .agents/skills/vectordeckppt/scripts/compile_pptx.py pptoutput/slides/ --output pptoutput/final.pptx --report pptoutput/compilation-report.json
    ```

16. Validate the result and open or render it when the environment supports PowerPoint/PDF inspection:

    ```bash
    uv run python .agents/skills/vectordeckppt/scripts/validate_pptx.py pptoutput/final.pptx --json
    ```

17. Deliver `pptoutput/final.pptx`, the source SVGs, PNG previews, `slide-content.md`, and `compilation-report.json`, plus any warnings that affect editability. Do not claim full editability when the report contains embedded SVG fallbacks.

## Design decision order

Make visual decisions in this order:

```text
audience outcome -> narrative role -> evidence -> visual thesis
-> composition -> typography -> imagery/data -> color/details
```

Do not begin with a favorite palette, a template, or decorative SVG. Let content determine the dominant visual and let the shared art direction constrain its expression.

For each slide, privately answer:

```text
What should the audience understand in three seconds?
What should they inspect next?
What evidence makes the claim credible?
Why is this visual form better than a sentence or another form?
What can be removed without weakening meaning?
How does this page advance the deck's rhythm?
```

Prefer one memorable visual idea, disciplined typography, and intentional negative space over a collection of polished components. A deck may be restrained, expressive, editorial, technical, cinematic, or documentary, but it must not look accidental or generically AI-produced.

## Non-negotiable constraints

- Treat one SVG as one full slide and as the visual source of truth.
- Default to `./pptoutput/` and never scatter deck artifacts across the repository.
- Treat text approval and three-page visual approval as separate mandatory gates. Never continue full production without both explicit approvals unless the current user explicitly opts out of a named gate.
- When a request is inaccurate, contradictory, incomplete in a material way, or open to meaningfully different interpretations, ask the smallest set of concrete questions needed to resolve it.
- Prefer native PowerPoint text and shapes; use embedded SVG fallback only for visible elements that cannot be converted reliably.
- Never rasterize the whole slide as the default compilation path.
- Never silently omit unsupported elements.
- Keep Chinese and other user-facing text editable whenever possible.
- Preserve image aspect ratio and use local or embedded assets only; never depend on remote URLs.
- Treat bundled style-template PNGs as art-direction references only. Rebuild typography, diagrams, cards, rails, and data views as structured SVG using the user's real content.
- Do not use scripts, `foreignObject`, animation, remote fonts, browser-only CSS, or interactive SVG.
- Do not leave temporary versions or preview artifacts in the final delivery folder.
- Do not default to blue-purple gradients, glowing technology motifs, excessive rounded cards, icon confetti, or stock imagery without a subject-specific reason.

## Completion gate

Finish only when the user explicitly approved the text-only slide draft and the three-page visual sample, every final SVG validates, every preview has been visually inspected, the complete deck compiles, the compilation report has zero failed elements, the PPTX validator passes, slide order/count are correct, and the user receives a readable summary of any intentional fallback.
