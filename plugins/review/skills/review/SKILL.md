---
name: review
description: >-
  Run one stateless, independent technical review of a frozen PR or base/head diff: lightweight, focused or full by mode and changed risk, with findings verified against the code.
metadata:
  owner: jay1803
  family: review
  maturity: stable
  distribution: review
---

# Review

Produce one independent technical judgment for a frozen PR or base/head diff.
Keep repository contents read-only. Review does not change product
requirements, perform Product/Design acceptance, repair code, count rounds, or
merge. Callers own lifecycle state; Review returns the facts of this run.

## Target and inputs

Accept a PR URL/number with an unambiguous repository (including a current-branch
PR resolved by `gh pr view`), or explicit `Repository`, `Base`, and `Head`.
Resolve revisions to full commits; do not invent a range. Stop only if the
target cannot be resolved unambiguously. Capture branches, base/head SHAs,
URL/number and start time before any reviewer starts. Review the actual remote
PR commits; a tested local commit with the same tree may be recorded as
equivalent. An explicit diff is always standalone and never posts.

Optional caller inputs: mode (`fast`, `standard` or `strict`; default
`standard`), governing requirement and acceptance sources, required claims, an
explicit full-review request, and for a re-review the prior result's open
findings plus the repair diff. Dev callers follow the
[boundary contract](references/dev-review-v2-contract.md).

For a focused structural PR review with comments use `$review-pr`; for a single
requested analysis surface use its specialist. Do not turn a narrow request
into this workflow merely because it mentions a PR.

Read the [severity policy](references/severity-policy.md) and pass the selected
mode to every reviewer, so severity and review depth share one meaning.

## Depth

Choose depth from the request and the diff yourself; no classifier is called.
Read [review depth](references/review-depth.md) for protected boundaries and
each route's packet.

- `focused`: prior findings and a repair diff were supplied. One reviewer
  checks each prior finding's fix, the delta, and implicated callers.
- `lightweight`: the fast/standard default. One reviewer covers requirements,
  correctness and maintainability, then verifies its own candidates.
- `full`: strict, an explicit full request or binding policy, or a change that
  crosses a protected boundary. Run the pipeline below.

A route that discovers a protected boundary escalates to full on the complete
current target. Whether to omit independent Review entirely is the caller's
policy, not Review's.

## Independent execution

Read the [routing contract](references/routing-contract.md), then only the
resolved [Codex](references/codex-adapter.md) or
[Claude Code](references/claude-code-adapter.md) adapter. Give each reviewer a
clean context with the target, diff, requirement sources and mode only; never
implementer reasoning. Only a focused reviewer receives prior findings.
Reviewers cannot delegate, edit files, or post.

If no clean reviewer can be started, run the same route in the current context
and report `Independence: not satisfied` when this context implemented the
change or saw its reasoning. Disclose it; do not present it as blind review.

Full review dispatches two finders in parallel on the same target:

- **Correctness**: the `$review-correctness` contract, including its trust,
  integration and test angles. When requirement sources exist, also apply the
  `$review-spec` finding contract and keep those findings separately classified.
- **Maintainability**: `$review-code-quality` with its thermo-nuclear rubric,
  covering architecture and repository instructions.

Then give both unchanged outputs, the target and read access to the frozen head
to `$review-judge`. The Judge verifies every candidate against the code and
proposes the common action; do not pre-deduplicate or drop withheld items.
A finder that cannot finish leaves its coverage incomplete; rerun only that
finder on the same target.

## Result and completion

Immediately before returning or posting, re-query the PR base and head. Any
change returns `stale` and nothing is posted. Return the result in the
[result contract](references/result-contract.md). Incomplete coverage is
`blocked`; never present incomplete or stale work as clean.

Post only when the user explicitly requested GitHub comments or already
authorized posting to this exact PR; automatic selection and a review-only
request do not grant write authority. Before an authorized write read
[GitHub posting](../review-pr/references/github-review-posting.md), submit one
`COMMENT` review, and verify it by readback. An unverified write is
`blocked - review not verified`. Otherwise return `not posted` without asking
for permission; diff targets are `not applicable`.

Report concise findings and limitations to the user and keep both finder
outputs with the result.
