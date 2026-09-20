# Research Question Type Contract

Question type determines what must be modeled and what counts as completion. It
does not dictate a fixed list of worker skills. Choose one primary type, then
record dependent subquestions only when they are necessary to answer the
primary question.

## Choice

Governing form:

> Which alternative should the decision owner choose under the stated
> objective, constraints, and horizon?

Required structure:

- Alternatives, including the status quo or delay where real.
- Hard constraints and disqualifiers.
- Objectives, criteria, thresholds, and tradeoffs.
- What must be true for each serious alternative to dominate.
- Evidence that can change the ranking.
- Recommendation, conditions, and revisit triggers.

Common failure: collecting descriptive facts about every option without a
decision rule.

## Diagnosis

Governing form:

> What caused or materially contributed to the observed outcome?

Required structure:

- Precisely defined outcome, baseline, timing, population, and comparison.
- Competing causal hypotheses, including measurement error, external changes,
  selection, and interactions.
- Mechanisms and expected observations under each hypothesis.
- Temporal order, confounders, counterfactual, and alternative explanations.
- Strength of causal identification and limits.

Common failure: treating correlation, temporal coincidence, or a plausible
story as root-cause proof.

## Forecast

Governing form:

> What outcome or range is likely by a defined horizon, and what would update
> that belief?

Required structure:

- Resolvable target, unit, population, geography, horizon, and as-of date.
- Reference class or base rate when available.
- Drivers, constraints, dependencies, and scenario branches.
- Probability, interval, or directional confidence appropriate to the evidence.
- Signposts, leading indicators, and update cadence.

Common failure: producing a vivid scenario without a calibrated forecast or
declaring one future inevitable.

## Discovery

Governing form:

> Where is an opportunity, unmet need, risk, or leverage point worth pursuing?

Required structure:

- Search space and deliberate exclusions.
- Target users/actors, jobs, frictions, current substitutes, and willingness or
  ability to change.
- Market, competitive, operational, and capability context.
- Opportunity hypotheses and evidence thresholds for further investment.
- A prioritized opportunity set, not an exhaustive catalog.

Common failure: equating an observed problem, trend, or large market with an
attractive opportunity for this decision owner.

## Design

Governing form:

> What system, policy, product, process, or architecture should be created to
> satisfy the stated requirements and tradeoffs?

Required structure:

- Required outcomes, users/actors, operating environment, invariants, and
  constraints.
- Viable design alternatives and the mechanism by which each creates the
  outcome.
- Tradeoffs, failure modes, reversibility, migration, and validation.
- Evidence or experiments needed before commitment.

Common failure: selecting a familiar solution before the operating constraints
and evaluation criteria are known.

## Evaluation

Governing form:

> Did an intervention produce the intended outcome, for whom, under what
> conditions, and at what cost or harm?

Required structure:

- Intervention, theory of change, target population, baseline, outcomes, and
  timing.
- Process, outcome, impact, and value-for-money questions as applicable.
- Counterfactual or credible comparison for causal impact claims.
- Heterogeneous effects, implementation fidelity, unintended effects, and
  guardrails.
- Method limits and transferability.

Common failure: using post-intervention improvement or participant satisfaction
as proof of attributable impact.

## Mixed Questions

Choose the type that owns the final decision/use. Represent other types as
dependent questions.

Examples:

- “Why did retention fall, and what should we do?” is primarily a choice only
  when the commitment is the deliverable; diagnosis is a prerequisite.
- “Which acquisition channel will be best next year?” is a choice with a
  dependent forecast.
- “Should we build this memory architecture?” is a choice with dependent design
  and evaluation questions.
- “Where should we grow?” is discovery until a concrete opportunity set exists,
  then a choice.

Do not combine several primary questions into one brief when each has a
different decision owner, time horizon, evidence base, or completion condition.
Split them and show the dependency.

## Classification Receipt

```markdown
## Question Classification

Raw question:
Primary type:
Dependent types:
Decision or use:
Decision owner:
Reason this type controls completion:
Nearby type rejected:
Split required: yes / no
```
