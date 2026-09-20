---
name: research-experiment-design
description: >-
  Design a credible, proportionate experiment, pilot, test-and-learn intervention, or quasi-experimental measurement plan for a decision-critical uncertainty. Use when passive research cannot distinguish hypotheses and the next step requires an intervention, comparison, counterfactual, decision threshold, guardrails, instrumentation, duration, analysis, and stop rules. Produces an Experiment Protocol; does not launch the test, spend money, recruit participants, or alter production without separate authorization.
metadata:
  owner: jay1803
  family: research
  maturity: stable
  distribution: research
---


# Research: Experiment Design

Design the cheapest credible test that can change the decision. Connect the
hypothesis, intervention, comparison, measurement, analysis, and action
threshold before execution.

Read the [Evidence Contract](../research/references/evidence-contract.md),
[Research Depth Contract](../research/references/research-depth-contract.md),
and [Decision Brief Contract](../research/references/decision-brief-contract.md).

## Boundary

- Own experimental question, hypothesis, intervention, comparison,
  counterfactual, unit, assignment or allocation, population, metrics,
  guardrails, instrumentation, duration, sample rationale, analysis,
  implementation fidelity, stopping, ethics, risks, and decision thresholds.
- Design randomized tests, staged pilots, switchbacks, holdouts, natural or
  quasi-experiments, prototypes, fake-door tests, operational trials, and
  structured tests when appropriate.
- Prefer a reversible test that produces decision information while limiting
  user, business, privacy, and operational harm.
- Do not launch campaigns, change production, recruit participants, spend
  money, send messages, or modify accounts without explicit execution authority.
- Do not use a low-fidelity proxy when it cannot discriminate the hypothesis.
- Do not promise statistical power, sample size, or causal validity without the
  required inputs and assumptions.

## Preconditions

Require:

- accepted Research Contract;
- Decision Model or causal/forecast frame;
- decision-critical hypothesis and alternative;
- observable success and failure signals;
- population and operating context;
- risk and source/authorization boundary.

Return `upstream_blocked` if a value judgment, product scope, metric definition,
or ethical boundary must be decided first.

## Workflow

1. State the decision and the exact uncertainty the test must resolve.
2. Define the primary hypothesis, competing/null hypothesis, mechanism, and
   expected divergence in outcomes.
3. Choose the minimum viable intervention and credible comparison.
4. Define unit of assignment/exposure and unit of analysis. Check contamination,
   interference, network effects, carryover, and spillovers.
5. Define target population, eligibility, segmentation, sample rationale, and
   generalization boundary.
6. Select one primary outcome tied to the decision, plus guardrails and
   diagnostic measures. Predefine metric formulas and windows.
7. Establish baseline, instrumentation, logging, data-quality, and
   implementation-fidelity checks.
8. Choose allocation, randomization, rollout, holdout, crossover, switchback, or
   quasi-experimental design. State the identifying assumptions.
9. Estimate sample/duration only when baseline rate, minimum meaningful effect,
   variance, traffic, and acceptable error are available. Otherwise provide the
   inputs and calculation method needed.
10. Predefine analysis, exclusions, missing-data handling, segment analysis, and
    multiple-comparison treatment.
11. Set decision thresholds:
    - evidence to commit or scale;
    - evidence to iterate;
    - evidence to stop or reject;
    - inconclusive result handling.
12. Define safety, ethics, privacy, consent, rollback, monitoring, and early-stop
    conditions.
13. Provide an execution handoff and evidence package required after the test.

## Design Selection

- Use a randomized controlled test when assignment is feasible and spillovers
  are manageable.
- Use a switchback or time-based design for shared systems where simultaneous
  randomization is impractical and carryover can be controlled.
- Use a staged pilot for operational feasibility and harm discovery; do not
  overclaim causal effect without a comparison.
- Use a prototype or concept test for comprehension and behavior hypotheses,
  recognizing fidelity limits.
- Use a fake-door test only with transparent, ethical user treatment and a plan
  for unmet expectations.
- Use quasi-experimental methods when assignment is not feasible and a credible
  natural comparison exists.
- Use monitoring rather than an experiment when intervention would be
  unethical, disproportionate, or incapable of answering before the decision
  expires.

## Metric Rules

- Primary metric represents the decision objective, not the easiest measurable
  click.
- Guardrails capture quality, retention, trust, harm, cost, latency, complaints,
  or downstream effects.
- Diagnostic metrics explain mechanism but do not replace the primary outcome.
- Predefine denominators, attribution window, cohort maturity, and exposure.
- Do not optimize short-term acquisition while ignoring activation, retained
  value, or cost when the decision concerns high-quality users.
- A statistically significant result can be too small to matter. Use a minimum
  decision-relevant effect.
- A null result can be underpowered, poorly implemented, or genuinely
  unpromising; the protocol must distinguish these cases.

## Output

```markdown
## Experiment Protocol

Research ID:
Decision:
Critical Uncertainty:
Primary Hypothesis:
Competing / Null Hypothesis:
Mechanism:
Generalization Boundary:

### Design
Intervention:
Comparator / Counterfactual:
Population / Eligibility:
Assignment / Exposure Unit:
Analysis Unit:
Allocation:
Duration:
Sample / Power Rationale:
Fidelity:

### Measurement
Primary Metric:
Minimum Decision-Relevant Effect:
Guardrails:
Diagnostic Metrics:
Baseline:
Instrumentation:
Data Quality:

### Analysis
Primary Analysis:
Exclusions:
Missing Data:
Segments:
Multiple Comparisons:
Causal Assumptions:
Robustness Checks:

### Decision Rules
Commit / Scale:
Iterate:
Stop / Reject:
Inconclusive:
Early Stop:

### Risk, Ethics, and Operations
User Risk:
Business / Operational Risk:
Privacy / Consent:
Rollback:
Monitoring:
Authorization Required:
Execution Owner:

### Evidence Handoff
Artifacts Required:
As-Of / Test Window:
Result Reviewer:
Next Research Route:
```

## Completion

The protocol is acceptable when another authorized owner can execute it without
inventing the hypothesis, metric, comparison, threshold, safety boundary, or
analysis. Completion is `Experiment Ready`; it is not proof of the hypothesis.

## Sub-Agent Contract

Default route: `worker/deep` for causal or consequential tests and
`worker/standard` for low-risk prototypes or pilots. Return a protocol and
authorization needs. Do not execute side effects.
