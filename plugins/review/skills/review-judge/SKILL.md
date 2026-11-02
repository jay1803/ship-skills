---
name: review-judge
description: >-
  Verify and combine the correctness and maintainability finder outputs of one full review against the frozen code.
metadata:
  owner: jay1803
  family: review
  maturity: stable
  distribution: review
---

# Review: Finding Judge

Verify each supplied candidate against the frozen code and combine the two
finder outputs of one full review. Do not search for new findings or replace a
specialist's semantic judgment.

Read the [Judge Contract](references/judge-contract.md) and the shared
[severity policy](../review/references/severity-policy.md) before judging.

## Inputs

Require the frozen target, the selected mode, both unchanged finder outputs,
any required claims and caller-marked deferrals with their authority, and read
access to the frozen head. Stop when the target itself is ambiguous.

## Workflow

1. Check that each output names the frozen target and a native completion
   decision, and account for every candidate, including withheld items.
2. Check each candidate against its cited code, then assign one disposition.
3. Group only findings that satisfy every deduplication key. Never collapse
   specification and engineering judgments.
4. Account for finder, specification and required-claim coverage, then select
   exactly one common action.
5. Return the proposal to `$review`. Do not modify files, invoke reviewers or
   providers, route repairs, or post to GitHub.

## Output

Return the frozen target, each candidate's disposition and reason, groups,
claim outcomes, clarification requests and the proposed common action.
Reference finding IDs; do not reproduce source text. This is a proposal, not a
current-head verdict: only `$review` may accept it after the final target check.
