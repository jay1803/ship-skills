---
name: review-spec
description: >-
  Compare a frozen implementation with its governing requirements for specification compliance.
metadata:
  owner: jay1803
  family: review
  maturity: stable
  distribution: review
---

# Review: Specification Compliance

Determine whether an implementation satisfies the governing product contract.
This specialist reports only requirement compliance; it does not grade code
style, maintainability, test quality, architecture, product desirability, or
visual design.

Apply the [mode policy](../review/references/severity-policy.md#review-depth-and-test-expectations)
when selecting depth, including direct invocation (standard by default). Missing
optional edge-case or reverse-red tests alone is not a finding or coverage gap;
retain explicit requirements and concrete changed-behavior defects.

## Inputs

Require an implementation target that can be inspected at a stable revision and
one or more source-authority candidates: an issue, PRD, specification, or
acceptance contract. Capture the target revision and the exact source locations
used as evidence.

Read [the Finding contract](references/finding-contract.md) before producing
findings. Use its four classifications and evidence fields exactly.

## Authority Resolution

1. Prefer an explicitly designated governing source. Otherwise, use the most
   specific versioned acceptance contract or specification that directly covers
   the target; use an issue or PRD only for requirements not superseded there.
2. When candidate sources conflict, lack a version or scope relationship, or do
   not identify a governing authority, return `blocked - governing authority
   ambiguous`. State the conflicting sources and the narrowest clarification
   needed; do not select a rule or invent a requirement.
3. When no accessible source contains a requirement for the target, return
   `blocked - governing authority missing`. State the sources checked and the
   authority needed. Do not turn inferred intent, code behavior, or test names
   into a specification.

## Review Method

1. Extract the governing requirements as small, checkable statements, retaining
   each requirement's identifier or exact wording and source location.
2. Inspect the frozen implementation, tests, and observable behavior only as
   evidence for those requirements.
3. For each requirement, report a Finding when behavior is missing, incorrect,
   extra, or cannot be verified from the available implementation evidence.
   A complete match returns `compliant` with the requirement-to-evidence mapping.
4. Treat ambiguous implementation evidence as `unverifiable`, not as a guessed
   pass or failure. Treat behavior as `extra` only when it is outside an
   explicit scope boundary; do not call an implementation detail extra merely
   because the source is silent.
5. Do not add technical-review or style findings. Route those concerns to
   `$review`; route product or design acceptance questions to their owning
   reviews.

## Output

```markdown
## Specification Compliance Review

Target: <repository/PR or immutable revision>
Governing Authority: <source and exact location, or missing/ambiguous>
Requirements Evaluated: <identifiers or exact statements>
Decision: <compliant | findings | blocked>

### Findings
- <Finding-contract entry, or "None">

### Blocker
- <bounded missing/ambiguous-authority explanation, or "None">

### Scope Boundary
- Code-quality/style review: not performed
- Product Review: not performed
- Design Review: not performed
```

For a blocked authority resolution, do not emit speculative requirement
findings. Return only the bounded blocker and the source needed to continue.
