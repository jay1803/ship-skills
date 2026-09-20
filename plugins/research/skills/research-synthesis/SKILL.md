---
name: research-synthesis
description: >-
  Synthesize an accepted Research State and Evidence Ledger into a traceable, calibrated draft Decision Brief. Use when evidence work is complete enough to update beliefs, compare alternatives, form a diagnosis or forecast, recommend action, name residual uncertainty, and define revisit triggers. Produces a draft only; does not invent missing evidence, hide contradictions, accept its own brief, or declare the controller complete.
metadata:
  owner: jay1803
  family: research
  maturity: stable
  distribution: research
---


# Research: Synthesis

Apply the accepted Decision Model to the accepted Evidence Ledger. Update
beliefs, explain why the answer changed or remained stable, and produce a draft
Decision Brief whose recommendation is no stronger than the evidence.

Read the [Evidence Contract](../research/references/evidence-contract.md),
[Decision Brief Contract](../research/references/decision-brief-contract.md),
and [Research State Contract](../research/references/research-state-contract.md).

## Preconditions

Require:

- current Research Contract and primary question type;
- accepted Decision Model or an explicit reason it is not applicable;
- accepted Hypothesis Map when alternatives or causes are material;
- closed required evidence-wave barriers;
- accepted Evidence Ledger with provenance;
- current mode, as-of date, source boundary, and stop rules.

For a first-phase brief, accepted supplied context may satisfy the evidence
requirements; no new evidence wave is required. Follow the Decision Brief
Contract when the requested result is options, a framework, or a gap with next
actions. Missing inputs may limit that answer without preventing a useful
conditional brief; do not invent a criterion or claim decision readiness.

Return `upstream_blocked` when a material decision criterion or required
evidence package is missing for the requested judgment (rather than the
limited brief above), or the source boundary has been violated.
Do not repair missing research by relying on memory or a last-minute search.

## Boundary

- Own belief updating, cross-artifact integration, alternative comparison,
  confidence, sensitivity, residual uncertainty, recommendation, next action,
  and draft Decision Brief.
- Use only accepted evidence and clearly labeled assumptions.
- Explain how evidence supports, weakens, rejects, or fails to distinguish
  hypotheses.
- Preserve source quality, independence, freshness, method, scope, and
  contradictions.
- Do not silently discard inconvenient findings.
- Do not create new primary evidence, run new analysis whose method has not been
  accepted, or expand scope.
- Do not accept the draft, mark research complete, or make the final commitment.

## Workflow

1. Re-read the current Research Contract, Decision Model, Hypothesis Map,
   accepted evidence, contradictions, unavailable evidence, and stop rules.
2. Audit every load-bearing claim. Remove or label any claim that lacks accepted
   evidence or a transparent assumption.
3. Group evidence by criterion or hypothesis rather than by source or research
   worker.
4. Assess each hypothesis:
   - supporting evidence;
   - disconfirming evidence;
   - source/method strength;
   - scope;
   - unresolved alternatives;
   - current status.
5. Apply hard constraints and disqualifiers before preference tradeoffs.
6. Compare serious alternatives under the accepted criteria and thresholds.
7. Run sensitivity:
   - plausible threshold changes;
   - alternative definitions;
   - source exclusion;
   - value-weight changes;
   - scenario changes;
   - causal or forecast uncertainty.
8. Identify the smallest set of findings that determines the answer.
9. Form a recommendation, diagnosis, forecast, opportunity priority, design
   direction, or evaluation judgment at the supported strength.
10. Choose the appropriate proposed terminal status:
    `Decision Ready`, `Experiment Ready`, `Monitor`, `Scan Complete`,
    `Inconclusive`, `Blocked`, or `Stopped`.
11. Define action, owner, timing, thresholds/kill criteria, and revisit triggers.
12. Produce the draft and an explicit list of evidence or assumptions that could
    overturn it.

## Belief Updating

Do not count sources as votes. Update belief according to:

- directness to the claim;
- method validity;
- source credibility and independence;
- population and temporal fit;
- consistency with mechanism;
- counterevidence and alternative explanations;
- prior plausibility or base rate;
- sensitivity of the decision to the claim.

Record material changes:

```markdown
Previous judgment:
New judgment:
Evidence causing change:
Why the change is warranted:
What remains unchanged:
```

A stable answer after new evidence can also be informative; state why the
evidence did not cross a decision threshold.

## Question-Type Synthesis

### Choice

Apply constraints, compare alternatives, state conditional ranking, tradeoffs,
and what would reverse it. Preserve staged, pilot, delay, and status-quo options.

### Diagnosis

State the most supported causes or contributors, mechanisms, interactions, and
causal support level. Separate root cause, trigger, enabling condition, and
correlated symptom.

### Forecast

State the resolvable forecast, range/probability, scenarios, drivers,
sensitivity, signposts, and decision implication.

### Discovery

Prioritize opportunities using accepted criteria. Distinguish evidence of a
problem, attractiveness, strategic fit, and readiness for investment.

### Design

Recommend a design direction and tradeoffs, with assumptions, validation,
migration, and downstream owner. Research does not implement it.

### Evaluation

Separate process, output, outcome, attributable impact, heterogeneous effects,
cost/value, and unintended effects. Claim only what the method establishes.

## Confidence

Confidence belongs to the scoped current answer. Explain it through:

- evidence quality and coverage;
- independence and freshness;
- method strength;
- alternative explanations;
- sensitivity;
- unresolved decision-relevant uncertainty.

Use `high`, `medium`, `low`, or `unknown`, or probabilities/ranges when the
question warrants them. Do not average arbitrary scores into a precise number.

## Recommendation Rules

- Recommend action when the evidence crosses the accepted decision threshold.
- Recommend an experiment when a remaining uncertainty can reverse the choice
  and a credible test exists.
- Recommend monitoring when waiting for a signpost is more valuable than further
  immediate research.
- Return inconclusive when the evidence cannot distinguish alternatives within
  the boundary.
- State a blocker when a missing definition, source, access, or method prevents
  a defensible answer.
- Stop when more research has insufficient expected decision value.
- Name what is deliberately not known.

## Output

Follow the shared Decision Brief Contract:

```markdown
# Draft Decision Brief

Research ID:
Research State Version:
Evidence Ledger Revision:
Draft Revision:
Research Mode:
As-Of Date:

## Decision or Use
Question:
Decision Owner:
Objective:
Horizon / Decision Date:
Scope / Constraints:

## Current Answer
Recommendation / Judgment:
Confidence:
Proposed Terminal Status:

## Why
1. <Decisive claim with evidence ID.>
2. <Decisive claim with evidence ID.>
3. <Decisive claim with evidence ID.>

## Alternatives and Decision Logic
| Alternative / Hypothesis | What Must Be True | Supporting Evidence | Counterevidence | Judgment |
| --- | --- | --- | --- | --- |

## Evidence
### Observations and Derived Facts
### Inferences
### Contradictions and Disconfirming Evidence

## Uncertainty and Robustness
Assumptions:
Residual Unknowns:
Sensitivity:
What Would Overturn the Answer:
Confidence Rationale:

## Recommended Action
Action:
Owner:
Timing:
Decision Threshold / Kill Criteria:
Required Handoff:

## Revisit Triggers
- <Observable signal, threshold, event, or date.>

## Sources and Artifacts
- <Evidence ledger and accepted worker artifacts.>

## Synthesis Audit
Unsupported claims removed or labeled:
Evidence excluded and why:
Material belief changes:
Review required: yes / no, with trigger
```

## Sub-Agent Contract

Default route: `worker/deep`. Give the synthesizer the current accepted state,
not every unfiltered raw source by default. Return the draft, traceability audit,
and review trigger. Do not browse, invent evidence, mutate the canonical state,
or claim final completion.
