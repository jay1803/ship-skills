---
name: research-desk
description: >-
  Collect and organize current external, documentary, academic, official, or supplied-source evidence for one bounded research question. Use when claims must be verified against primary or credible sources, source conflicts or freshness matter, or an evidence brief with claim-level citations is required. Produces evidence-ledger rows and a Desk Research Brief; does not answer an unframed topic, cross a supplied-source boundary, or declare the final decision.
metadata:
  owner: jay1803
  family: research
  maturity: stable
  distribution: research
---


# Research: Desk Research

Resolve a bounded external or documentary evidence question with current,
traceable sources. Search to discriminate hypotheses, not to accumulate
interesting facts.

Read the [Evidence Contract](../research/references/evidence-contract.md).

## Boundary

- Own source discovery, source inspection, claim extraction, freshness,
  lineage, contradiction, and evidence-ledger rows for the assigned question.
- Use supplied files and named sources as the basis when the assignment requires
  them. Use public external research only when authorized.
- Prefer original records, official documents, primary research, standards,
  laws, datasets, specifications, filings, and direct artifacts for claims they
  can establish.
- Use secondary sources to contextualize, compare, challenge, or locate primary
  material.
- Do not redesign the Decision Model, expand the topic, or write the final
  recommendation.
- Do not cite search snippets, AI summaries, or unread source titles as evidence.
- Do not fabricate access, publication details, statistics, quotes, or source
  agreement.

## Source Strategy

1. Restate the assigned question, claim, hypothesis, time scope, and decision
   use.
2. Identify the closest source class capable of establishing each needed fact.
3. Search broadly enough to locate serious primary and disconfirming sources,
   then inspect narrowly.
4. Record source lineage so several derivative articles are not counted as
   independent evidence.
5. Check dates, version, definitions, population, geography, incentives, and
   method before comparing findings.
6. Preserve conflicting evidence when definitions or methods do not reconcile.
7. Stop when the assigned evidence need is satisfied or the source boundary has
   been exhausted.

## Source Priority

Use claim-dependent precedence:

- Laws, regulations, standards, official specifications, filings, and original
  public records for formal rules and disclosed facts.
- Direct measurements, datasets, original papers, and method appendices for
  empirical claims.
- Official product documentation, changelogs, pricing, and terms for the
  provider's current published contract.
- Company statements for what the company states; do not make them independent
  proof of performance or comparative superiority.
- Independent high-quality analysis and journalism for synthesis, scrutiny, and
  external context.
- Reviews, communities, social posts, and expert commentary for leads,
  experiences, edge cases, and hypotheses; bound the inference.
- Aggregators and search snippets only to navigate to inspectable sources.

## Workflow

1. Validate the worker assignment. Return `upstream_blocked` if question,
   source boundary, as-of date, or expected artifact is missing.
2. Build a concise query plan using the hypotheses and decision criteria.
3. Gather current sources, prioritizing primary material and disconfirming
   evidence.
4. Inspect the actual source content, including method, definitions, caveats,
   and date.
5. Extract only decision-relevant claims. Record unsupported requested points
   explicitly.
6. Compare sources and resolve apparent conflicts when definitions, scope, or
   lineage explain them.
7. Assess relevance, directness, credibility, independence, freshness,
   coverage, and method validity.
8. Produce evidence-ledger rows with statement types and limitations.
9. State how the evidence affects the assigned hypothesis or criterion.
10. Recommend a next route only; do not dispatch it.

## Supplied-Source Mode

When the assignment says “use these files,” “based on this report,” or otherwise
limits sources:

- Use only the supplied or named materials.
- Preserve their terminology, framing, organization, and level of detail when
  summarizing them.
- Do not silently fill gaps, correct them with outside knowledge, or reconcile
  conflicts from memory.
- State which requested points the material does not support.
- Label any permitted interpretation as inference.
- Ask the controller to revise the boundary before external research.

## Freshness and Volatility

Verify current claims when they can change: product behavior, pricing, market
conditions, law, policy, schedules, leadership, API limits, technical
standards, and public statistics. Record the as-of and access dates. Older
sources can establish history or trend but cannot silently stand in for current
state.

## Contradiction Rules

- Compare like with like before declaring a conflict.
- Check whether one result is a subset, later version, different metric, or
  derivative source.
- Do not average incompatible estimates without a model.
- Do not choose the most convenient source.
- When unresolved disagreement can change the decision, mark it as a critical
  uncertainty and recommend the next discriminating method.

## Output

```markdown
## Desk Research Brief

Research ID:
Assigned Question:
Decision Use:
Source Boundary:
As-Of Date:
Search / Inspection Scope:

### Findings
| Finding | Statement Type | Source | Scope / Date | Quality | Supports / Contradicts | Confidence |
| --- | --- | --- | --- | --- | --- | --- |

### Source Notes
- <Source, what it can establish, method, incentives, limitations.>

### Conflicts and Counterevidence
- <Conflict, attempted reconciliation, remaining effect.>

### Unsupported or Unavailable Evidence
- <Requested point the inspected sources do not establish.>

### Decision Effect
- <How this changes or does not change the assigned criterion or hypothesis.>

### Evidence Ledger Rows
- <Structured rows following the Evidence Contract.>

### Recommended Next Route
- <Controller recommendation only.>
```

## Sub-Agent Contract

Default route: `worker/standard`; use `worker/deep` for contested, regulated,
technical, legal, or high-stakes evidence. Return sources inspected, queries or
selection logic, evidence rows, contradictions, and limitations. Remain
read-only and within the source boundary.
