---
name: research-causal-analysis
description: >-
  Assess whether evidence supports a causal explanation or attributable effect. Use when a diagnosis, evaluation, intervention, growth change, policy, product change, or observational relationship depends on what caused what, and confounding, selection, timing, mediation, spillovers, or counterfactual choice could alter the conclusion. Produces a Causal Analysis Brief and identification judgment; does not turn correlation into causation or execute an experiment.
metadata:
  owner: jay1803
  family: research
  maturity: stable
  distribution: research
---


# Research: Causal Analysis

Judge how strongly the available design and evidence support a causal claim.
Make the estimand, mechanism, counterfactual, assumptions, and alternative
explanations explicit.

Read the [Evidence Contract](../research/references/evidence-contract.md) and
[Question Type Contract](../research/references/question-type-contract.md).

## Boundary

- Own causal question definition, theory/mechanism, estimand, treatment or
  exposure, outcome, population, timing, comparison, confounders, mediators,
  selection, spillovers, identification assumptions, method strength, and
  causal confidence.
- Evaluate randomized, quasi-experimental, observational, qualitative,
  process-tracing, and mixed evidence at the strength each can support.
- Use `$research-data-analysis` for data preparation and descriptive estimates.
- Use `$research-experiment-design` when a prospective test is the best next
  method.
- Do not claim causation merely because an effect is plausible, precedes the
  outcome, correlates with it, survives a regression, or appears after a change.
- Do not repair the underlying product, policy, or system.

## Causal Question

Define:

```text
For population P,
what is the effect of treatment/exposure X
relative to counterfactual C
on outcome Y
over time window T,
under implementation conditions I?
```

For diagnosis, the estimand may be contribution rather than a clean treatment
effect. State whether the goal is:

- necessary cause;
- sufficient cause;
- average effect;
- effect for a segment;
- contribution among interacting causes;
- mechanism confirmation;
- root cause of a specific incident;
- attributable impact of an intervention.

## Workflow

1. Read the Research Contract, outcome definition, Hypothesis Map, available
   data, intervention history, and assigned causal claim.
2. Verify temporal order and define exposure, outcome, population, unit,
   comparison, and time.
3. Draw or describe the causal structure: common causes, mediators, moderators,
   selection, measurement, feedback, interference, and external events.
4. State the counterfactual: what would likely have happened without the
   exposure or under the nearest alternative?
5. Inventory evidence designs and their identification assumptions.
6. Test alternative explanations, including:
   - regression to the mean;
   - seasonality and secular trend;
   - concurrent changes;
   - composition or selection change;
   - measurement/instrumentation change;
   - reverse causality;
   - survivorship and attrition;
   - anticipation or lag;
   - spillovers and interference.
7. Assess whether adjustment variables are pre-treatment confounders rather
   than mediators or colliders.
8. Evaluate robustness, placebo/negative controls, pre-trends, dose-response,
   mechanism evidence, and heterogeneous effects when applicable.
9. Grade the causal support and name the strongest remaining threat.
10. Recommend the next method only when it could materially change the decision.

## Evidence Designs

### Randomized

Check assignment integrity, compliance, attrition, interference, outcome
measurement, power, implementation fidelity, and whether the estimate applies
to the decision population.

### Quasi-Experimental

For difference-in-differences, interrupted time series, regression
discontinuity, instrumental variables, synthetic control, matching, or related
designs, state the identifying assumption and testable implications. Method
label alone does not establish validity.

### Observational

Use adjustment, longitudinal structure, matching, or modeling as evidence under
explicit assumptions. Report residual confounding and selection. Predictive
accuracy is not causal identification.

### Qualitative and Process Evidence

Use temporal sequence, mechanism traces, actor evidence, documents, negative
cases, and pattern matching to assess contribution and plausibility. Bound the
claim; absence of a counterfactual may limit effect size or attribution.

### Incident Root Cause

For a specific technical or operational incident, require reproduction or
event evidence, causal mechanism, distinction between trigger and enabling
conditions, and proof that the proposed cause explains the observed behavior.
Route implementation to the proper Dev workflow.

## Causal Confidence

Use one:

- `strong`: design and assumptions support a scoped causal claim; major threats
  are weak or tested.
- `moderate`: causal interpretation is useful but depends on material,
  defensible assumptions.
- `weak`: evidence supports association or mechanism plausibility, not reliable
  attribution.
- `unsupported`: the available evidence cannot distinguish the causal claim
  from serious alternatives.
- `unknown`: required evidence or design information is unavailable.

## Output

```markdown
## Causal Analysis Brief

Research ID:
Causal Question:
Population:
Exposure / Intervention:
Comparator / Counterfactual:
Outcome:
Time Window:
Estimand:
Theory / Mechanism:

### Causal Structure
- Confounders:
- Mediators:
- Moderators:
- Selection:
- Spillovers / Interference:
- Measurement:

### Evidence Designs
| Evidence | Design | Estimate / Finding | Identification Assumption | Strength | Limitation |
| --- | --- | --- | --- | --- | --- |

### Alternative Explanations
- <Threat, evidence for/against, residual risk.>

### Robustness / Falsification
- <Pre-trend, placebo, negative control, sensitivity, mechanism, negative case.>

### Causal Judgment
Support Level:
Scoped Claim:
Strongest Remaining Threat:
What Cannot Be Claimed:

### Decision Effect
- <How causal uncertainty changes the action or confidence.>

### Evidence Ledger Rows
- <Structured rows.>

### Recommended Next Route
- <Experiment design, more data, user/process evidence, synthesis, or stop.>
```

## Sub-Agent Contract

Default route: `worker/deep`. Causal attribution is method-sensitive; preserve
the distinction between association, contribution, mechanism, and effect.
Return assumptions, threats, scoped judgment, and next method. Do not execute
the intervention.
