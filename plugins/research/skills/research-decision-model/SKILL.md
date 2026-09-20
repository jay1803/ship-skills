---
name: research-decision-model
description: >-
  Build an explicit model of how a research question will be judged. Use when alternatives, baseline, hard constraints, objectives, criteria, thresholds, causal or value drivers, tradeoffs, or sensitivity are unclear. Produces a Decision Model that says what must be true for an answer to be preferred; does not collect the full evidence or decide from unsupported scores.
metadata:
  owner: jay1803
  family: research
  maturity: stable
  distribution: research
---


# Research: Decision Model

Make the logic of the eventual answer explicit before evidence collection.
Define what “better,” “likely,” “causal,” “valuable,” or “successful” means in
this decision.

Read the [Question Type Contract](../research/references/question-type-contract.md)
and [Evidence Contract](../research/references/evidence-contract.md).

## Boundary

- Own alternatives, baseline, hard constraints, objectives, criteria,
  thresholds, causal/value drivers, tradeoffs, and sensitivity.
- Translate vague standards into observable or at least testable conditions.
- Preserve the difference between user values, objective constraints, empirical
  claims, and analyst judgment.
- Do not invent quantitative weights or multiply ordinal ratings into a false
  precision score.
- Do not collect the full evidence corpus or produce the final recommendation.
- Do not optimize for one metric while silently discarding guardrails,
  reversibility, strategic fit, or distributional effects.

## Workflow

1. Read the accepted Research Contract and existing evidence relevant to the
   model.
2. Enumerate serious alternatives at the right level. Include status quo,
   delay, staged commitment, or combined approaches when real.
3. Separate hard constraints and disqualifiers from preferences and tradeoffs.
4. Define the objective hierarchy: primary outcome, supporting outcomes,
   guardrails, and unacceptable harms.
5. Select the smallest set of criteria that can distinguish alternatives.
6. For each criterion, define meaning, measurement or observable signal,
   direction, threshold if known, and affected population/time window.
7. Map causal or value drivers: how would each alternative produce the
   objective?
8. State what must be true for each alternative to dominate and what would
   disqualify it.
9. Identify dependencies and interactions; avoid assuming criteria are
   independent.
10. Run a qualitative sensitivity check: which assumptions, thresholds, or
    value judgments could reverse the current ranking?
11. Return the model, unsupported inputs, and hypotheses that need evidence.

## Question-Type Shapes

### Choice or Design

Use alternatives, constraints, objectives, criteria, thresholds, tradeoffs, and
what-must-be-true claims.

### Diagnosis

Model the outcome, baseline, potential causal pathways, contribution, timing,
and what evidence would distinguish mechanisms. A full causal judgment belongs
to `$research-causal-analysis`.

### Forecast

Define the resolvable target, reference class, key drivers, constraints,
scenarios, and decision thresholds. Probability estimation belongs to
`$research-forecasting`.

### Discovery

Define opportunity criteria: user pain or unmet job, reachable demand,
willingness/ability to adopt, strategic fit, capability advantage, economics,
timing, and risk. Do not equate market size with opportunity quality.

### Evaluation

Define theory of change, process/output/outcome/impact/value questions,
population, timing, guardrails, and the standard required for causal attribution.

## Model Rules

- Keep criteria decision-relevant. A fact that cannot change the action does not
  need a criterion.
- A hard constraint should eliminate an option; a soft preference should not be
  disguised as one.
- Use explicit thresholds when the decision genuinely has them. Mark proposed
  thresholds as assumptions until confirmed.
- If weights matter, elicit or infer them only from explicit tradeoffs and test
  multiple plausible weight sets.
- Avoid double-counting correlated criteria, such as “audience size” and
  “available impressions,” without explaining the relationship.
- Separate expected outcome from execution capability. A theoretically strong
  channel can be weak for this team.
- Include path dependence and option value when early action builds or closes
  future capabilities.
- Record value conflict instead of forcing a single ranking when the decision
  owner has not resolved the tradeoff.

## Output

```markdown
## Decision Model

Research ID:
Question Type:
Decision or Use:
Objective:

### Alternatives
| Alternative | Mechanism | What Must Be True | Disqualifiers |
| --- | --- | --- | --- |

### Baseline / Status Quo
- <Current path and expected consequence.>

### Hard Constraints
- <Constraint, source, affected alternatives.>

### Objectives and Guardrails
| Objective / Guardrail | Definition | Population / Window | Direction / Threshold | Source |
| --- | --- | --- | --- | --- |

### Decision Criteria
| Criterion | Why It Matters | Observable Signal | Tradeoff / Interaction | Current Evidence |
| --- | --- | --- | --- | --- |

### Decision Rule
- <How evidence will support, eliminate, condition, or rank alternatives.>

### Sensitivity
- <Assumption, threshold, or value judgment capable of reversing the answer.>

### Unsupported Inputs
- <Unknown that must not be treated as fact.>

### Hypotheses to Test
- <What-must-be-true or causal claim for `$research-hypothesis-map`.>
```

## Sub-Agent Contract

Default bounded route: `worker/deep`. Preserve the accepted Research Contract
and source boundary. Return a model and its unsupported inputs; do not browse
broadly, manufacture weights, or issue the final recommendation.
