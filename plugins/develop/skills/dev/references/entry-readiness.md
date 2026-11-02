# Direct Eligibility And Issue Resolution

Read during implicit entry or to resolve a request that names no issue. Return to the root preflight before Dev execution.

## Direct Exclusion Gate

Apply this gate before the Issue Resolution Gate whenever `$dev` is only an
implicit or automatic candidate. Its purpose is to avoid turning a bounded edit
into issue-level orchestration.

An explicit command-like `$dev` invocation, or a request for the full issue,
PR, review, CI, merge, tracker-closeout, or release-candidate lifecycle, bypasses
this exclusion and enters Dev.

### Direct Artifact

Route ordinary Skill authoring, documentation, and simple configuration work to
Direct Artifact when the requested artifact and intended result are already
clear. Use the matching task-specific skill, such as `$skill-creator`, and let
the current agent perform the work inline:

`locate -> edit -> targeted validation -> inspect diff -> scoped commit`

- Do not create a Dev goal or Dev State, resolve or mutate a tracker issue,
  create a Dev branch/worktree, or start Dev repository discovery, technical planning,
  implementation, verification, Review, or merge
  handoff merely because the artifact lives in a code repository.
- Validate proportionately. For Skill work, run the skill validator and any
  repository, catalog, link, package, or behavior checks affected by the
  actual change.
- Ordinary artifact edits do not require independent review. Add a focused
  behavioral evaluation or independent review only when the change affects
  routing, permissions, external writes, destructive actions, security rules,
  or Dev/Review/Release orchestration, or when the user explicitly requests it.
- Do not create `Skipped / Unverified` entries for work that is outside Dev.
  Report only validation actually performed and any concrete remaining limit.

### Direct Patch

Route a code change to Direct Patch only when all of these are true:

- the requested outcome is explicit and requires no missing product decision;
- repository evidence identifies one bounded local behavior or mechanical
  change with no competing implementation direction;
- the change does not affect an API or schema contract, authentication,
  authorization, security, privacy, data migration, destructive behavior,
  concurrency semantics, cross-module ownership, or generated-client contract;
- it needs no cross-repository coordination, deployment, release, or production
  verification;
- the user did not request `$dev` or the issue/PR/review/merge/tracker lifecycle;
  and
- repository policy does not require a stronger process.

Let the current agent perform Direct Patch inline:

`read local context -> edit -> focused test/check -> inspect diff -> scoped commit`

Do not use changed-line or file-count thresholds as the decision rule. A
two-line auth or schema change can be high risk, while a larger mechanical edit
can remain bounded.

### Escalation

Stop the Direct path and enter `$dev` or a narrower specialist workflow when
scope expands, root cause is unclear, multiple plausible designs appear,
focused validation exposes a broader failure, a high-risk boundary above is
touched, repository policy requires more, or the user requests the full
lifecycle. Carry forward the evidence already gathered so Dev does not repeat
repository discovery, diagnosis, or planning without need.

When either Direct path applies, return that route immediately. Do not continue
into the Issue Resolution Gate or any numbered Dev lifecycle step.

## Issue Resolution Gate

Resolve one tracker record before creating a branch, researching code, or changing files.

1. Bind an explicitly supplied Linear ID exactly.
2. For an unnumbered issue-level request, search the tracker for a relevant issue before doing Dev work. Search by the requested outcome or defect, affected code/product surface, repo/project context, labels, and recent related issues; read promising matches.
3. Reuse a clearly relevant issue and state its ID. Do not create a duplicate. If several candidates are materially plausible, stop for the smallest question needed to choose the target.
4. If no relevant issue exists, draft and create it yourself: a concise outcome-oriented title, the raw request, repo/product context, objective, expected behavior, scope, acceptance criteria, and explicit unknowns, using only requester-stated or cited product rules (`$pm-spec` may draft it when installed and the requester asks). Assign the current/requesting user when known. The record is not automatically dev-ready.
5. For the bound, reused or new issue, the preflight's [entry audit](resume-preflight.md#entry-audit) decides readiness and asks the requester for any missing decision.
6. If tracker tools are unavailable, provide the exact search result or creation draft and stop before branch/worktree setup or implementation.

This gate applies to unnumbered bugs, features, regressions, and follow-ups. A
project, milestone, parent issue, issue set, or multi-issue request keeps its
complete scope for its [request owner](resume-preflight.md#request-owner)
rather than collapsing into one duplicate issue record.
