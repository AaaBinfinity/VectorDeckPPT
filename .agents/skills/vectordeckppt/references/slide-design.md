# Slide Design Rules

## Contents

1. General composition
2. Cover
3. Two-column explanation
4. Architecture and flow
5. Timeline
6. Data and evidence
7. Summary and close
8. Anti-patterns

## General composition

Give each slide one primary claim and one dominant visual hierarchy. Vary silhouettes to fit the content while keeping the shared design system. Use equal outer margins by default and intentionally align internal elements.

Prefer a single composition over a dashboard of small cards. When a slide feels empty, strengthen the focal element or evidence rather than adding decorative widgets.

## Cover

- Keep the title slide minimal: title, essential subtitle/context, and one restrained visual move.
- Use the largest type in the deck and protect clear negative space.
- Do not add agenda chips, fake metrics, or production metadata.
- If a hero image is used, ensure its subject placement supports the title area.

## Two-column explanation

- Use columns only when two bodies of content have a real relationship: comparison, explanation + evidence, or text + media.
- Start with an intentional ratio such as 40/60 or 50/50; do not split by habit.
- Align the first meaningful baseline across columns.
- Let one column dominate. Equal visual weight often creates indecision.

## Architecture and flow

- State the system-level takeaway in the title.
- Limit layers or phases to the smallest set needed for understanding.
- Draw connectors before nodes so edges remain behind labels and shapes.
- Keep connector direction, arrow meaning, and line weight consistent.
- Avoid crossed connectors. If topology is genuinely complex, use a dedicated diagram tool or a carefully prepared image.
- Use native basic shapes when editability is important; path-heavy decorative connectors will enter SVG fallback.

## Timeline

- Choose a time axis that matches the decision: chronological dates, phases, or maturity stages.
- Make duration, overlap, and milestones visually accurate.
- Use concise event labels and put detail in notes or adjacent evidence.
- Avoid equal spacing when time intervals are materially unequal unless the timeline is explicitly ordinal.

## Data and evidence

- Lead with the implication, not “Data Analysis.”
- Show only values that support the claim and keep units/denominators explicit.
- Use direct labels when practical; avoid remote legends and unnecessary 3D effects.
- Do not fake a chart with decorative bars when the numbers need analytical accuracy.
- For a small number of values, native SVG shapes and text are appropriate. Complex charts may remain an image or embedded SVG; disclose the editability tradeoff.
- Give screenshots a clear crop, readable scale, and one explanatory annotation layer.

## Summary and close

- Resolve the opening question or decision.
- Synthesize two to four implications; do not repeat every slide title.
- End with the appropriate outcome: recommendation, decision request, next action, application, or productive question.
- Do not default to a generic “Thank you” slide unless the setting requires it.

## Anti-patterns

- Repeating centered-title-plus-three-cards on every page.
- Dense UI-like panels, pills, tabs, badges, or buttons without product meaning.
- Shrinking copy to fit instead of editing it.
- Large decorative shapes that compete with the message.
- Changing palette, radius, type scale, or icon family between slides.
- Using diagrams when a sentence or image would communicate faster.
- Keeping a weak slide only to reach a requested page count.
- Treating “no overflow” as the definition of visual quality.
