---
name: research-review
description: >-
  Independently review a frozen Research State, Evidence Ledger, and Decision Brief for decision alignment, source quality, traceability, alternatives, counterevidence, method validity, causal or forecast strength, uncertainty calibration, robustness, and actionability. Use for deep research, high-stakes or hard-to-reverse decisions, conflicting evidence, weak identification, explicit verification, or review-only requests. Returns pass, conditional, fail, or unknown without repairing the target.
metadata:
  owner: jay1803
  family: research
  maturity: stable
  distribution: research
---


# Research: Review

Judge whether a frozen research result is reliable and decision-ready. Review
the argument and evidence at their actual strength; do not reward polished prose
or a large bibliography.

Read the [Evidence Contract](../research/references/evidence-contract.md),
[Decision Brief Contract](../research/references/decision-brief-contract.md),
and [Research Depth Contract](../research/references/research-depth-contract.md).

## Frozen Target

Before review, bind:

- Research ID and State version.
- Decision Brief revision or content hash.
- Evidence Ledger revision.
- Research mode and as-of date.
- Primary question type, decision owner, and source boundary.
- Accepted worker artifacts and required raw material.

If the target changes during review, stop and require a new frozen revision.
Do not review a moving draft.

## Independence

Prefer a reviewer that did not author the synthesis and receives the accepted
state, evidence, and target without the synthesis author's hidden reasoning.
Independence is an assurance mechanism, not proof of correctness. Record the
reviewer and any unavoidable overlap.

## Boundary

- Own observations, findings, severity, verdict, remediation owner, and review
  evidence.
- Inspect cited sources or raw artifacts when needed to test load-bearing claims.
- Distinguish target defects from missing access or review uncertainty.
- Do not edit the Decision Brief, rewrite evidence rows, run repairs, change the
  decision model, or dispatch new research.
- Do not make a fail disappear by weakening the review standard.
- Do not infer that an uncited claim is supported because it sounds plausible.

## Review Lenses

### 1. Decision Alignment

- Does the brief answer the accepted decision/use?
- Are owner, objective, horizon, scope, constraints, and as-of date preserved?
- Does the recommended action match the terminal status?
- Has the research drifted into a broader or easier question?
- Does the opening give an answer, useful options, or the decisive gap, rather
  than substitute a method discussion? For framework-only work, does it supply
  the requested rule without applying it beyond the user's scope?

### 2. Decision Model

- Are serious alternatives, status quo, constraints, criteria, thresholds, and
  tradeoffs represented?
- Are value judgments distinguished from empirical claims?
- Could arbitrary weights, duplicated criteria, or omitted guardrails reverse
  the answer?

### 3. Evidence Quality

- Do load-bearing claims trace to accepted evidence?
- Are source quality, independence, lineage, freshness, population, period, and
  method appropriate?
- Are company or interested claims treated as such?
- Does the brief cite a stronger conclusion than the source supports?
- Was a supplied-source boundary respected?

### 4. Alternatives and Counterevidence

- Are plausible competing hypotheses and disconfirming evidence present?
- Did the synthesis cherry-pick confirming examples?
- Were contradictions reconciled honestly or preserved?
- Is the null/status quo or a combined explanation missing?

### 5. Method Validity

- Can the method support the claim strength?
- Are quantitative definitions, coverage, missingness, selection, and
  uncertainty represented?
- Are participant findings bounded to the sample?
- Are causal claims supported by a credible counterfactual or appropriately
  scoped mechanism/contribution evidence?
- Is a forecast resolvable, base-rate-informed, and calibrated?

### 6. Synthesis and Confidence

- Does the recommendation follow logically from evidence and the model?
- Are facts, inferences, assumptions, judgments, and forecasts separable?
- Is confidence calibrated to limitations and serious alternatives?
- Does sensitivity show what changes the answer?
- Is the change from any previous judgment explained?

### 7. Actionability

- Is the next action concrete, authorized, and owned?
- Are thresholds, kill criteria, experiment handoff, monitoring signposts, or
  revisit triggers present?
- Is remaining uncertainty represented rather than hidden?
- Is further research justified by decision value?
- Does each proposed evidence task resolve a named gap that could change the
  answer? Are definitions and business tradeoffs distinguished from empirical
  unknowns instead of being assigned indiscriminately to more research?

## Severity

| Severity | Meaning |
| --- | --- |
| `critical` | The recommendation answers the wrong question, crosses authorization/source boundary, fabricates evidence, or could cause a materially unsafe/invalid decision |
| `major` | A load-bearing claim lacks support; a serious alternative is omitted; method cannot support the conclusion; confidence or causal/forecast claim is materially overstated |
| `moderate` | A limitation, definition, sensitivity, traceability link, or action condition could change interpretation but does not currently overturn the core answer |
| `minor` | Local clarity, metadata, or presentation defect that does not affect judgment |
| `unknown` | The reviewer lacks necessary source, data, or method access to assess a material point |

Findings cite exact evidence, section, claim, source, dataset, or missing artifact.

## Verdict

### Pass

No unresolved critical or major finding. The answer, confidence, terminal state,
and action are supported. Moderate findings are either non-blocking or carried
as explicit conditions.

### Conditional

The core answer may stand, but named moderate or bounded major conditions must
be resolved or carried into action. State whether the controller can complete
as conditional or must repair and rereview.

### Fail

One or more critical or material major findings invalidate the recommendation,
assurance floor, source boundary, or terminal claim. Route findings to their
artifact owners.

### Unknown

Review cannot judge a material load-bearing point because required evidence,
access, provenance, or target identity is unavailable. Do not convert unknown
into pass.

## Remediation Ownership

| Finding | Owner |
| --- | --- |
| Wrong or incomplete decision/use | `$research-question-framing` |
| Alternatives, criteria, thresholds, or tradeoffs defective | `$research-decision-model` |
| Competing explanations or falsification missing | `$research-hypothesis-map` |
| Method, priority, or stop rule defective | `$research-evidence-plan` |
| External source or claim problem | `$research-desk` or relevant evidence worker |
| Market or competitor interpretation problem | `$research-market-landscape` / `$research-competitive` |
| Participant study or synthesis problem | `$research-user-study` / `$research-user-synthesis` |
| Quantitative definition or analysis problem | `$research-data-analysis` |
| Causal attribution problem | `$research-causal-analysis` |
| Experiment protocol problem | `$research-experiment-design` |
| Forecast target or calibration problem | `$research-forecasting` |
| Cross-evidence reasoning or brief problem | `$research-synthesis` |
| State, scope, routing, or completion problem | `$research` |

The reviewer names the owner; the controller dispatches the repair. After a
material repair, review a new frozen target.

## Output

```markdown
## Research Review

Research ID:
Research State Version:
Decision Brief Revision / Hash:
Evidence Ledger Revision:
Mode:
As-Of:
Reviewer:
Independence Note:

### Verdict
Pass / Conditional / Fail / Unknown

### Findings
| ID | Severity | Lens | Finding | Evidence | Impact | Owner | Required Resolution |
| --- | --- | --- | --- | --- | --- | --- | --- |

### Decision Alignment
- <Assessment.>

### Evidence and Method
- <Assessment of traceability, quality, independence, freshness, and validity.>

### Alternatives and Counterevidence
- <Assessment.>

### Confidence and Robustness
- <Assessment.>

### Actionability
- <Assessment.>

### Residual Unknowns
- <What the reviewer cannot establish.>

### Completion Judgment
- Decision-ready / conditionally decision-ready / not decision-ready / unknown
- Conditions:
- Rereview required: yes / no
```

## Sub-Agent Contract

Default route: fresh `worker/deep`. Receive the frozen target and minimum raw
evidence needed to test it. Return findings and verdict only. Do not repair,
rewrite, browse beyond review necessity, or accept the final state.
