# Decision Brief Contract

A Decision Brief is the stable handoff from research to a decision owner. It
makes the reasoning inspectable without forcing the reader to reconstruct every
search or intermediate artifact.

## Required Shape

Lead with the restated question, any definition needed to understand the
answer, and the current answer or useful options. Put only decisive reasoning
next; method detail supports the answer rather than replacing it. Do not force
an empty definitions section when the question is already clear.

For a **framework-only** request, the answer is an operational rule or candidate
rules with their tradeoffs, known thresholds, and unresolved inputs. Do not
issue a current go/no-go recommendation when it was excluded, but do not use
that exclusion to withhold the requested rule. Distinguish evidence about an
effect from the user's judgment about how much of that effect is acceptable.
Proposed thresholds and priorities remain proposals until accepted; research
must not silently convert a tolerable loss into a zero-tolerance constraint.

When no complete answer is supported, state the partial answer and decisive gap
up front. Separate missing definitions, empirical unknowns, and unmade business
tradeoffs. For each material gap, give the smallest action that could resolve
it and explain how its result changes the answer. Offering these actions is
part of Research; executing an experiment, contacting people, or committing to
a business choice still requires the applicable authorization.

The same shape applies to a first-pass answer and a post-research synthesis.
Keep source and uncertainty distinctions even when a short response replaces
the full template below.

```markdown
# Decision Brief

## Decision or Use
- Question:
- Decision owner:
- Objective:
- Horizon / decision date:
- Scope and constraints:
- Research mode and as-of date:

## Current Answer
- Recommendation, diagnosis, forecast, opportunity, design direction, or
  evaluation judgment:
- Confidence:
- Terminal status:

## Why
- The few findings that materially determine the answer.
- Each material claim cites an evidence-ledger item or source.

## Alternatives and Decision Logic
- Serious alternatives, including status quo where real.
- What must be true for each.
- Hard constraints, criteria, thresholds, and decisive tradeoffs.
- Why the current answer dominates under the accepted model.

## Evidence
- Confirmed observations and derived facts.
- Important inferences.
- Source quality, independence, freshness, and scope.
- Material contradictory or disconfirming evidence.

## Uncertainty and Robustness
- Assumptions.
- Remaining decision-relevant unknowns.
- Sensitivity: what changes the answer and what does not.
- Confidence rationale.
- Evidence that would overturn the conclusion.

## Recommended Action
- Concrete next action.
- Owner and timing when known.
- For an experiment: protocol handoff and decision thresholds.
- For monitoring: signposts and review cadence.

## Revisit Triggers
- Observable events, metrics, thresholds, or dates that require reassessment.

## Sources and Artifacts
- Evidence ledger, datasets, research briefs, and review target revision.
```

Omit sections that are genuinely inapplicable, but preserve the distinction
between evidence, inference, judgment, uncertainty, and action.

## Answer Shape by Question Type

- **Choice**: recommendation and conditional ranking.
- **Diagnosis**: most supported causes, contribution/interaction where known,
  and identification strength.
- **Forecast**: target, probability/range, scenarios, and signposts.
- **Discovery**: prioritized opportunity set and evidence threshold for the next
  investment.
- **Design**: recommended direction, tradeoffs, validation, and handoff.
- **Evaluation**: process/outcome/impact judgment, for whom, conditions, costs,
  harms, and method limits.

## Traceability

Every load-bearing statement must trace to one or more accepted evidence items,
a transparent calculation, or an explicitly labeled assumption. The brief may
compress evidence; it may not erase provenance or disagreement.

A reference list without claim-level linkage is insufficient for a material
recommendation.

## Recommendation Rules

- Recommend at the strength supported by the evidence.
- State conditions when the ranking depends on thresholds or assumptions.
- Preserve the status quo, delay, staged commitment, experiment, and reversible
  pilot as real alternatives when relevant.
- Do not convert “worth testing” into “proven.”
- Do not convert a user preference into an objective fact.
- Do not convert a large market, popular trend, or competitor activity into
  strategic fit without the decision model.
- The researcher recommends; the decision owner commits unless delegation is
  explicit.

## Confidence

Confidence applies to a scoped judgment, not the entire topic.

Use a clear scale or calibrated language and explain:

- Evidence directness and coverage.
- Source independence and freshness.
- Method validity.
- Alternative explanations.
- Sensitivity to assumptions.
- Unresolved decision-relevant uncertainty.

Do not average unrelated confidence scores into a precise overall number unless
a justified quantitative model exists.

## Terminal Status

One of:

- `Decision Ready`
- `Experiment Ready`
- `Monitor`
- `Scan Complete`
- `Inconclusive`
- `Blocked`
- `Stopped`

The terminal status must match the action. An `Experiment Ready` brief cannot
claim that the underlying strategic hypothesis is proven.

## Review Binding

When review is required, record:

- Decision Brief revision or content hash.
- Research State version.
- Evidence-ledger revision.
- Reviewer.
- Review verdict and conditions.
- Repairs and the revision that resolved them.

Any material change after review requires a new review of the changed target.
