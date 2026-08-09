# Presentation Planning

## Contents

1. Communication job
2. Source synthesis
3. Narrative construction
4. Presentation-type patterns
5. Slide plan contract
6. Planning quality checks

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

## Planning quality checks

- Does each slide have one narrative job and primary claim?
- Are important claims sourced or clearly framed as proposals?
- Does the sequence accumulate instead of repeat?
- Is the opening relevant to the audience and the close a real resolution?
- Are data, diagrams, screenshots, and images assigned a specific explanatory role?
- Can any slide be removed without harming the narrative? If yes, remove or merge it.
- Does the planned density fit the requested delivery time and readable type sizes?
