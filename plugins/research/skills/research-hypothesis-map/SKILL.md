---
name: research-hypothesis-map
description: >-
  Create a competing, falsifiable map of explanations or what-must-be-true claims. Use when an open question has plausible alternatives, causal mechanisms, strategic assumptions, or hidden dependencies that need supporting, disconfirming, and decisive signals before evidence collection. Produces a Hypothesis Map; does not confirm a preferred story or perform the final causal judgment.
metadata:
  owner: jay1803
  family: research
  maturity: stable
  distribution: research
---


# Research: Hypothesis Map

Turn uncertainty into competing claims that evidence can distinguish. Make
disconfirmation and generalization boundaries visible before collecting
supportive examples.

Read the [Evidence Contract](../research/references/evidence-contract.md) and
[Question Type Contract](../research/references/question-type-contract.md).

## Boundary

- Own the issue tree, hypotheses, mechanisms, scope, supporting signals,
  disconfirming signals, decisive tests, and dependencies.
- Include plausible null, status-quo, measurement, external, interaction, and
  combined explanations where they matter.
- Represent the preferred answer as one hypothesis among alternatives until the
  evidence supports it.
- Do not claim that a hypothesis is true from plausibility, expert consensus,
  or the number of supporting anecdotes.
- Do not conduct the complete evidence search or final causal analysis.

## Workflow

1. Read the Research Contract, Decision Model, accepted evidence, and known
   contradictions.
2. Identify the top-level drivers that would determine the answer. Use MECE as a
   coverage aid, not a false claim that real causes never overlap.
3. Create serious competing hypotheses at a comparable level of abstraction.
4. For each hypothesis, state the mechanism, scope, preconditions, and expected
   observations.
5. State what would support it, what would weaken or falsify it, and which
   evidence most cleanly distinguishes it from the nearest alternative.
6. Identify shared causes, interactions, lag effects, selection, measurement,
   and reverse causality when relevant.
7. Mark assumptions that are value judgments or definitions rather than
   empirical hypotheses.
8. Estimate prior plausibility qualitatively only when there is a basis such as
   a base rate, existing evidence, or mechanism. Record the basis.
9. Identify hypotheses whose truth would not change the decision and
   deprioritize them.
10. Return the map and the decision-critical uncertainties for
    `$research-evidence-plan`.

## Hypothesis Forms

### What-Must-Be-True

Useful for choices and designs:

> Alternative A should be preferred only if audience fit, economics, execution
> capability, and scale conditions are sufficiently strong.

Break the statement into independently testable claims without assuming every
dimension deserves equal weight.

### Causal

Useful for diagnosis and evaluation:

> Change X caused or materially contributed to outcome Y through mechanism M,
> in population P, during period T.

Include competing causes, common causes, measurement change, selection, and
timing.

### Forecast Driver

Useful for forecasting:

> By horizon H, outcome Y will be in range R because drivers D1–Dn outweigh
> constraints C1–Cn.

Include base-rate and regime-change alternatives.

### Opportunity

Useful for discovery:

> Segment S has a valuable unresolved job, can be reached, will change behavior,
> and fits the decision owner’s capabilities better than current alternatives.

Include substitute adequacy and willingness/ability to adopt.

## Quality Rules

- Every hypothesis must have a condition under which belief should decrease.
- A “signal” should be observable and scoped; “strong demand” is incomplete.
- Do not use absence of evidence as evidence of absence without considering the
  method’s ability to observe the effect.
- Distinguish necessary from sufficient conditions.
- Distinguish an alternative explanation from a subcomponent of the same
  explanation.
- Preserve interaction hypotheses when several factors must combine.
- Do not explode the map into every imaginable cause. Prioritize plausible,
  consequential, and discriminable hypotheses.
- State where a hypothesis may hold: population, segment, geography, product
  state, channel, and time.

## Output

```markdown
## Hypothesis Map

Research ID:
Primary Question:
Decision Use:

### Issue Tree
- <Driver>
  - <Sub-question>

### Competing Hypotheses
| ID | Claim | Mechanism / Preconditions | Scope | Supporting Signal | Disconfirming Signal | Decisive Evidence | Prior Basis | Decision Leverage | Status |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |

### Interactions and Shared Causes
- <Relationship that prevents naive one-cause reasoning.>

### Definitions / Value Judgments
- <Important premise that must be decided rather than empirically discovered.>

### Critical Uncertainties
1. <Unknown most likely to change the decision and why.>

### Recommended Next Route
`$research-evidence-plan`
```

## Sub-Agent Contract

Default bounded route: `worker/deep`. Use the accepted model and evidence
without favoring the sponsor's preferred answer. Return the map, coverage gaps,
and decision-critical unknowns. Do not dispatch evidence workers.
