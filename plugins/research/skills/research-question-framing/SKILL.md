---
name: research-question-framing
description: >-
  Convert a vague or overloaded research request into a current Research Contract. Use when the decision or intended use, primary question type, decision owner, objective, horizon, scope, constraints, stakes, reversibility, source boundary, or required output is unclear. Produces framing only; does not gather broad evidence or recommend an answer.
metadata:
  owner: jay1803
  family: research
  maturity: stable
  distribution: research
---


# Research: Question Framing

Define the question well enough that later research can be relevant, bounded,
and falsifiable. Preserve the user's real uncertainty instead of prematurely
turning it into a familiar research template.

Read the shared
[Question Type Contract](../research/references/question-type-contract.md) and
[Evidence Contract](../research/references/evidence-contract.md).

## Boundary

- Own the Research Contract and question classification.
- Identify what decision, action, prediction, explanation, opportunity,
  design, or evaluation the research must support.
- Separate the raw question from a proposed answer or method.
- Split questions only when they have materially different owners, horizons,
  evidence bases, or completion conditions.
- Do not collect a broad evidence corpus, rank alternatives, or write the final
  recommendation.
- Do not invent a decision owner, budget, metric definition, source permission,
  or deadline. Use explicit assumptions only when the result can remain useful
  and the controller can carry them forward.

## Workflow

1. Read the raw request, supplied sources, prior decisions, product/project
   context, known constraints, and existing Research State.
2. State the intended use. Ask: what will be chosen, changed, explained,
   forecast, discovered, designed, or evaluated after this research?
3. Classify one primary question type and any dependent types.
4. Identify the decision owner or audience, objective, horizon, decision date,
   scope, exclusions, and baseline/status quo.
5. Record hard constraints, stakes, reversibility, and the cost of delay.
6. Establish the source boundary and which external, internal, participant, or
   experimental evidence is available or authorized.
7. Define the required answer form and what observable result would make the
   framing complete.
8. Ask only questions whose answers materially change the contract. First use
   available context; do not ask the user to repeat information already present.
9. Return the contract, explicit assumptions, unresolved framing blockers, and
   next route.

This is framing within the controller's first phase, not automatic entry into
evidence collection. Separate undefined terms from missing facts and unmade
business tradeoffs. Return a focused clarification or candidate interpretations
when the user must settle the meaning; name evidence work only when it can
resolve a specific ambiguity. Reuse definitions already supplied.

## Classification Checks

### Choice

What alternatives or class of alternatives are being chosen? What objective and
constraints determine better?

### Diagnosis

What outcome changed, relative to what baseline, for whom, when, and where?
Does the user need an explanation only or also an intervention choice?

### Forecast

What exactly will resolve, by what date, in what unit, population, and
geography? What decision depends on the forecast?

### Discovery

What search space is in scope, what counts as an opportunity, and what
capability or strategic fit matters to the decision owner?

### Design

What outcome must the system create, in what operating environment, under what
invariants and constraints?

### Evaluation

What intervention, population, outcomes, baseline, timing, and intended use must
be evaluated? Is the question about process, outcome, attributable impact,
value, or several of these?

## Framing Rules

- Prefer a decision-relevant question over a topic label.
- Include the status quo, delay, or no-action baseline when it is a real option.
- Specify an as-of date for volatile questions.
- Distinguish decision horizon from research deadline.
- Preserve consequential ambiguity as an open field; do not hide it with a
  generic phrase such as “business value” or “high quality.”
- A metric name without a definition, population, and window is not a complete
  objective.
- A wide question can remain wide in scan mode. Standard or deep decision
  research requires a bounded decision or explicit decomposition.
- “Find everything” is not a completion criterion. State the use and boundary.

## Completion

The artifact is complete when the controller can determine:

- what the research must help someone do;
- which question type owns completion;
- what is in and out of scope;
- what time, population, and context the answer covers;
- what constraints and stakes matter;
- what evidence sources are permitted;
- what output and terminal state are possible;
- which unresolved question still blocks modeling, if any.

## Output

```markdown
## Research Contract

Raw Question:
Decision or Intended Use:
Decision Owner / Audience:
Primary Question Type:
Dependent Question Types:
Objective:
Horizon:
Decision Date:
As-Of Date:
Scope:
Exclusions:
Baseline / Status Quo:
Hard Constraints:
Stakes:
Reversibility:
Cost of Delay:
Source Boundary:
Available Evidence:
Unavailable or Unauthorized Evidence:
Required Output:
Possible Terminal States:

### Explicit Assumptions
- <Assumption and why it is temporarily acceptable.>

### Framing Blockers
- <Only a missing item that prevents a useful model.>

### Recommended Next Route
<Return to the controller to answer from existing information, clarify a
material definition/decision, or select bounded modeling/evidence work for a
named gap.>
```

## Sub-Agent Contract

Default bounded route: `worker/deep`. Use only the assigned request and
authorized context. Return the contract, sources/context read, assumptions,
blockers, and next route. Do not browse widely or make the final decision.
