---
name: review-correctness
description: >-
  Find evidence-backed behavioral defects and regressions in a GitHub PR or explicit base/head diff.
metadata:
  owner: jay1803
  family: review
  maturity: stable
  distribution: review
---

# Review: Correctness

Find concrete correctness defects in one frozen code change. This specialist is
isolated: it does not orchestrate `$review`, judge
other findings, change code, post to GitHub, or replace Product Review or
Design Review.

Read the [Correctness Findings Contract](references/correctness-findings-contract.md)
before reviewing. That contract is the finding bar and output schema for this
skill.

Apply the [mode policy](../review/references/severity-policy.md#review-depth-and-test-expectations)
when selecting depth, including direct invocation (standard by default). Missing
optional edge-case or reverse-red tests alone is not a finding or coverage gap;
retain explicit requirements and concrete changed-behavior defects.

## Inputs

Accept exactly one target shape:

- Pull request: repository path plus a GitHub PR URL or number.
- Immutable diff: explicit `Repository`, `Base`, and `Head` revisions.

For a PR, capture its base and head revisions before inspection. For an
immutable diff, resolve both supplied revisions to full commits. Stop if the
target is ambiguous or cannot be frozen; do not infer a range from the current
branch.

## Workflow

1. Freeze and inspect the exact target. Record the repository, target type,
   base revision, and head revision. Review only that range.
2. Inspect the changed behavior and relevant callers, consumers, conventions,
   and contracts needed to assess this lens. Apply the linked finding contract
   for the evidence bar, exclusions, classifications, and finding shape.
3. Preserve confirmed findings when a separate candidate lacks proof. Record
   that hypothesis under Withheld Items. Use `context insufficient` only when
   a named required part of the review surface cannot be inspected, retaining
   any confirmed findings and the coverage gap together.
4. Return findings and coverage to the caller without editing files, invoking
   reviewers, or posting. A specialist result does not start a repair loop.

## Output

```markdown
## Correctness Review

Repository: <repository>
Target Type: <pull-request | immutable-diff>
PR: <URL/number or none>
Base Revision: <full SHA>
Head Revision: <full SHA>
Decision: <findings | no findings | context insufficient | blocked>

### Findings
<Required finding blocks, or "None observed.">

### Evidence Scope
- <callers, consumers, contracts, tests, or commands inspected>

### Coverage Gaps
- <required surface that could not be inspected, or "None.">

### Withheld Items
- <incomplete context or excluded non-defects, or "None.">

### Recommended Next Step
<caller; or `$dev-implementer` when a Dev-managed caller accepts a finding>
```

A `no findings` result means no candidate satisfied the correctness contract;
it does not claim that the target is fully approved or that other review lenses
passed.
