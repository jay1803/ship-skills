---
name: review
description: >-
  Coordinate independent specification, correctness, and maintainability review of a GitHub PR or explicit base/head diff.
metadata:
  owner: jay1803
  family: review
  maturity: stable
  distribution: review
---

# Review

Produce one independent technical judgment for a frozen PR or base/head diff.
Keep repository contents read-only. This workflow does not change product
requirements, perform Product/Design acceptance, or merge a PR.

## Target and routes

Accept a PR URL/number with an unambiguous repository (including a current-branch
PR resolved by `gh pr view`), or explicit `Repository`, `Base`, and `Head`.
Resolve revisions to full commits; do not invent a diff range. Stop only if the
target cannot be resolved unambiguously. Capture PR branches, base/head SHAs,
URL/number, and start time before dispatch.

- New standalone review: generation 1, attempt 0; return evidence to the caller.
- Dev-managed or supplied repair history: read the
  [lifecycle contract](references/dev-review-v2-contract.md) before dispatch.
  Require current PR traceability and Review Readiness. An explicit diff is
  always standalone and cannot satisfy the Dev gate or start automatic repair.
- Every run uses the thermo-nuclear maintainability rubric owned by
  `$review-code-quality`, including standalone runs. Omitted Dev mode is
  standard; preserve explicit strict as a distinct severity threshold in the
  new envelope. Preserve the caller's selected phase plan and explicit checks.
  Do not relabel or rewrite historical source artifacts.

For a focused structural PR review with comments use `$review-pr`; for a single
requested analysis surface use its specialist. Do not turn a narrow request
into this complete workflow merely because it mentions a PR.

Read [severity policy](references/severity-policy.md) before evaluating a
mode gate or constructing reviewer prompts. Pass it to each lens so severity
has a shared meaning without changing its evidence bar. Its review-depth rules
also constrain test/security scope and conditional signals; do not turn standard
omissions into findings or incomplete coverage.

## Independent review

Read the [routing contract](references/routing-contract.md), then only the
resolved executor adapter: [Codex](references/codex-adapter.md) or
[Claude Code](references/claude-code-adapter.md). Preserve explicit executor,
fallback, and independence requirements and record actual runtime receipts.

Read the [artifact contract](references/artifact-contract.md) when building the
frozen envelope and wrapping source outputs. Prepare its per-lens capability
and evidence ownership packet before dispatch. Dispatch exactly `$review-spec`,
`$review-correctness`, and `$review-code-quality` in clean isolated contexts
against that envelope. Pass only their task, target, and relevant authority;
exclude implementation reasoning, prior findings, and sibling outputs. Core
reviewers cannot delegate, edit files, or post. Preserve each complete native
output byte-for-byte and calculate its UTF-8 length and SHA-256.

Collect all three results even if one reports a defect or missing authority.
Then read [conditional signals](references/conditional-reviewers.md), evaluate
them once, and finish all signaled one-shot reviewers on the same target.
Conditional output cannot trigger another wave. Preserve required coverage
gaps for judgment; no partial source set may start repair.

## Judgment and completion

Before dispatching Judge, use the [assembly preflight](references/assembly-contract.md)
on the immutable manifest/files for declared bindings, hashes, byte ranges and
coverage. Then compare the native receipts, complete candidate index (including
withheld items) and exact authority quotes with their sources. Verify every
required claim has its assigned evidence or an explicit gap. Repair only bad
transport or obtain the affected source's additive correction on the same
target; preserve valid lenses and failed originals. A script pass does not
establish semantic completeness, authority or finding validity.

Pass the envelope, coverage requirements/signals, and all source artifacts to
`$review-judge`. Do not pre-deduplicate, paraphrase, or discard withheld items.
The judge owns dispositions, semantic source validation, grouping, and coverage.
Use the [assembly contract](references/assembly-contract.md) for deterministic
byte/envelope checks and lossless assembly. Pass immutable files plus their
manifest; the judge returns compact decisions, not copied source text.
Resolve gate-relevant source-level questions through the severity clarification
path before acceptance; preserve all original artifacts and additive replies.

Assemble and validate the returned decision plus immutable sources, then validate
the combined envelope and accepted target bindings; retain
an invalid judge artifact in quarantine. Immediately re-query the PR base and head.
A changed base or head returns `stale`, without posting or charging an attempt.

Post only when the user explicitly requested GitHub comments or already
authorized posting to this exact PR. Automatic selection and a review-only
request do not grant write authority. Read
[GitHub posting](../review-pr/references/github-review-posting.md) before an
authorized write, submit one `COMMENT` review, and verify it by readback.
An unverified write is `blocked - review not verified`. Without posting
authorization, return the completed artifact with `not posted`; no permission
question is needed to finish the review. Diff posting is `not applicable`.

Standalone returns to its caller. Dev-managed review follows the lifecycle
contract: only an accepted, complete current-generation judgment may route
the full repair batch; incomplete coverage blocks, and clean/current evidence
returns to the merge handoff or separate Product Review.

Use the [result contract](references/result-contract.md) when returning the
artifact. Report concise findings and limitations to the user while retaining
the complete source evidence in the durable artifact.
