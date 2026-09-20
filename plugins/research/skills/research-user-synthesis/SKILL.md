---
name: research-user-synthesis
description: >-
  Synthesize actual user, customer, stakeholder, operator, expert, survey, diary, observation, usability, or concept-test evidence into decision-relevant findings. Use when real participant materials exist and must be coded, compared, bounded, and traced to evidence. Produces a User Evidence Brief with participant-level provenance, variation, counterexamples, and limitations; does not invent sessions, generalize beyond the sample, or replace behavioral prevalence with anecdote.
metadata:
  owner: jay1803
  family: research
  maturity: stable
  distribution: research
---


# Research: User Evidence Synthesis

Turn actual participant material into bounded findings that can update a
hypothesis or decision criterion. Preserve variation, negative cases, and the
difference between what participants said, did, and what the researcher infers.

Read the [Evidence Contract](../research/references/evidence-contract.md).

## Preconditions

Require actual material such as transcripts, recordings, notes, survey rows,
task outcomes, observation records, diary entries, or concept-test artifacts.
Also require enough provenance to distinguish participants or response groups,
method, date, and study scope.

When the material does not exist, is inaccessible, or cannot be attributed,
return `upstream_blocked` and recommend `$research-user-study`. Never create
synthetic findings to complete the workflow.

## Boundary

- Own data familiarization, coding, case comparison, theme development,
  variation, negative cases, participant-level evidence, survey summary when
  supplied, and decision implications.
- Preserve the study population, sampling method, question wording, session
  context, and data-quality limitations.
- Distinguish participant report, observed behavior, task performance, direct
  quote, researcher interpretation, and strategic judgment.
- Do not claim population prevalence from qualitative evidence.
- Do not report “saturation” without a defined scope, sampling logic, and
  evidence that additional cases stopped adding decision-relevant variation.
- Do not expose unnecessary participant identity or sensitive data.
- Do not decide the final strategy.

## Workflow

1. Validate the assigned question, study plan or provenance, source boundary,
   participant material, and expected output.
2. Inventory the evidence: participants/responses, segments, dates, methods,
   missing sessions, unusable records, and deviations from the plan.
3. Read or inspect the material before adopting a coding frame.
4. Create a provisional codebook tied to the hypotheses and open to emergent,
   disconfirming, and interaction evidence.
5. Code at the case level, preserving the source location for material claims.
6. Compare within and across cases: common patterns, segment differences,
   sequences, workarounds, choice tradeoffs, outcomes, and contradictions.
7. Identify negative cases and evidence that weakens the preferred narrative.
8. Distinguish:
   - what participants explicitly said;
   - what they were observed doing;
   - the researcher's inference;
   - what remains unknown.
9. For surveys, report denominator, missingness, sampling frame, response
   pattern, uncertainty, and question limitations before percentages.
10. Connect findings to the assigned hypotheses or decision criteria without
    extending beyond the sample.
11. Produce evidence-ledger rows and recommend the next route.

## Evidence Rules

- A memorable quote illustrates a finding; it does not establish frequency.
- Several participants repeating a phrase may reflect the instrument or sample.
- Stated preference, intended behavior, and actual behavior are different
  evidence types.
- Absence of a complaint does not prove absence of a problem.
- Explain whether a segment difference was preplanned or found after inspection.
- Do not hide contradictory cases as “outliers” without a defensible reason.
- Use exact short quotes only when wording itself carries evidence; otherwise
  paraphrase with source location.
- Redact or pseudonymize identity unless it is necessary and authorized.
- Record study deviations and low-quality evidence instead of silently dropping
  it.

## Output

```markdown
## User Evidence Brief

Research ID:
Assigned Question:
Study / Source:
Method:
Population and Sample:
Collection Dates:
Material Inspected:
Material Missing / Excluded:

### Findings
| Finding | Evidence Type | Cases / Responses | Scope | Hypothesis / Criterion | Confidence |
| --- | --- | --- | --- | --- | --- |

### Variation and Segments
- <Where experience, behavior, or interpretation differs.>

### Negative Cases and Counterevidence
- <Case that weakens or bounds the finding.>

### Observed Behavior vs Reported Belief
- <Important divergence.>

### Quotes or Source Examples
- <Short, attributed or pseudonymized evidence with location.>

### Survey Results
- <Only when survey data exists: denominator, sampling, uncertainty, missingness.>

### Limitations
- <Sampling, instrument, collection, researcher, missing-data, or transfer limit.>

### Decision Effect
- <How the evidence updates the assigned hypothesis or criterion.>

### Evidence Ledger Rows
- <Structured rows with participant-safe provenance.>

### Recommended Next Route
- <Controller recommendation only.>
```

## Sub-Agent Contract

Default route: `worker/standard`; use `worker/deep` for sensitive, heterogeneous,
large, or methodologically complex material. Use only real authorized evidence.
Return the brief, codebook summary, source locations, limitations, and evidence
rows. Do not contact participants or invent missing material.
