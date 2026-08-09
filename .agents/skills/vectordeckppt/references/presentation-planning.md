# Presentation Planning

## Contents

1. Communication job
2. Source synthesis
3. Narrative construction
4. Narrative pressure and pacing
5. Presentation-type patterns
6. Slide plan contract
7. Planning prompt
8. Planning quality checks

## Communication job

Start with one sentence:

> By the end, **[audience]** should **[understand, believe, choose, approve, or do X]** because **[central takeaway]**.

Use this sentence to decide what belongs in the deck. For neutral teaching or reference material, state the questions the audience should be able to answer.

## Source synthesis

For each source, capture:

- the claim or topic it supports;
- exact metrics, dates, labels, and units;
- evidence quality and caveats;
- figures or images that can be reused;
- required attribution;
- conflicts with other sources.

Do not distribute source paragraphs evenly across slides. Convert evidence into audience meaning: what it proves, why it matters, and what it changes.

## Narrative construction

Choose an arc that matches the job:

- context → stakes → evidence → implications → action;
- question → analysis → answer;
- problem → causes/options → recommendation;
- current state → change → future state;
- chronology or learning progression;
- claim → evidence → consequence.

An agenda is not a storyline. Each slide should answer a question raised by the previous slide or create the need for the next one.

Use takeaway titles that communicate the point. Prefer “Three bottlenecks delay inspection feedback” over “Current Pain Points.”

Build a chain of audience questions. A useful test is to write the implicit question above each slide:

```text
Why should I care?
What is actually happening?
Why is it happening?
What does the evidence prove?
What are the realistic choices?
Why this recommendation?
What changes next?
```

The questions do not need to appear on the slide, but their order should make the storyline feel inevitable.

## Narrative pressure and pacing

Control what the audience knows, expects, and needs at each moment.

- **Opening**: establish relevance, tension, promise, or a clear decision—not background for its own sake.
- **Orientation**: provide only the context required to understand the central problem or opportunity.
- **Development**: alternate explanation and proof. Do not stack five conceptual pages before showing evidence.
- **Peak**: give the most decisive finding, demonstration, or recommendation enough visual and temporal space.
- **Resolution**: convert the argument into implications, a decision, an action, or a durable synthesis.

Use pacing deliberately:

- statement slides create emphasis and a pause;
- diagrams slow the audience down to understand relationships;
- data slides create credibility and consequence;
- image-led pages create empathy, scale, or memory;
- summary pages compress what has been earned, not what has merely been shown.

Avoid a mechanical rhythm where every slide contains the same amount of text and the same three-column structure. Vary density while keeping the design system stable.

## Presentation-type patterns

### Graduation defense

Typical logic: research context → problem and objectives → method/system → data and experiment design → results → contribution → limitations/future work → conclusion.

Allocate more slides to method and evidence than to background. State novelty only after the audience understands the baseline.

### Business report

Typical logic: decision context → performance signal → drivers → risks/opportunities → recommendation → owners and next steps.

Lead with the decision or operating implication. Do not make leaders wait through a chronological activity log.

### Product launch

Typical logic: audience problem → product promise → experience/workflow → differentiators → proof → availability/action.

Keep the product visible. Avoid a long market preamble that delays the experience.

### Sales pitch

Typical logic: buyer situation → cost of status quo → solution → credible proof → implementation → commercial next step.

Address buyer risk and adoption effort, not only product features.

### Teaching deck

Typical logic: learning goal → prior knowledge → concept → worked example → guided practice → synthesis/application.

Use progressive disclosure. Give each page one teaching move.

### Technical talk

Typical logic: problem boundary → constraints → architecture → critical mechanisms → evidence/tradeoffs → operational lessons.

Prefer a few clear system views over repeated component inventories.

### Project update

Typical logic: objective → current status → delivered outcomes → blockers/risks → decisions needed → next milestone.

Separate completed work from activity. Make requests and owners explicit.

### Research report

Typical logic: research question → method → evidence → interpretation → uncertainty → conclusion/next investigation.

Never present correlation or model output as stronger evidence than the method supports.

## Slide plan contract

Record at least:

```json
{
  "slide": 5,
  "title": "The pipeline separates detection from review",
  "purpose": "Explain the system architecture",
  "key_message": "Three layers keep model iteration independent from operator workflow",
  "visual_type": "architecture",
  "evidence": ["system specification section 3"],
  "assets": ["assets/operator-screen.png"]
}
```

Slide count is an output constraint, not a reason to spread content evenly. Combine weak slides and give decisive evidence enough space.

For each planned slide, add one rhetorical role:

```text
orient / frame / reveal / explain / compare / prove / challenge /
recommend / demonstrate / synthesize / transition / resolve
```

Adjacent slides should not perform the same role repeatedly unless a deliberate evidence sequence requires it.

## Planning prompt

Use this internal prompt after reading the source material:

```text
Act as an editor and presentation strategist, not a document summarizer.

1. State the audience decision, belief, or capability this deck must create.
2. Identify the central tension and the strongest defensible takeaway.
3. Separate sourced facts, interpretations, proposals, and unknowns.
4. Choose a narrative arc appropriate to the presentation type.
5. Build a sequence of audience questions and answers.
6. Give every slide one rhetorical role, one claim, and one evidence need.
7. Assign the best visual proof: typography, data, diagram, image, comparison,
   process, timeline, or demonstration.
8. Remove slides that only repeat a topic heading or source paragraph.
9. Create an opening promise, a peak evidence moment, and a resolved close.
10. Check that the sequence fits the speaking time and audience knowledge.
```

## Planning quality checks

- Does each slide have one narrative job and primary claim?
- Are important claims sourced or clearly framed as proposals?
- Does the sequence accumulate instead of repeat?
- Is the opening relevant to the audience and the close a real resolution?
- Are data, diagrams, screenshots, and images assigned a specific explanatory role?
- Can any slide be removed without harming the narrative? If yes, remove or merge it.
- Does the planned density fit the requested delivery time and readable type sizes?
- Does the plan contain a meaningful change in pace and visual mode?
- Is the most important conclusion given the strongest evidence and visual emphasis?
- Does each proposed visual have a reason beyond making the page less textual?
