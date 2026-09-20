# Direct Eligibility And Issue Readiness

Read during implicit entry, issue resolution, or the audit of an existing issue without a verified PM handoff. Return to the root preflight before Dev execution.

## Direct Exclusion Gate

Apply this gate before the Issue Resolution Gate whenever `$dev` is only an
implicit or automatic candidate. Its purpose is to avoid turning a bounded edit
into issue-level orchestration.

An explicit command-like `$dev` invocation, or a request for the full issue,
PR, review, CI, merge, tracker-closeout, or release-candidate lifecycle, bypasses
this exclusion and enters Dev. Merely discussing, creating, or editing the Dev
skill does not count as invoking `$dev`.

### Direct Artifact

Route ordinary Skill authoring, documentation, and simple configuration work to
Direct Artifact when the requested artifact and intended result are already
clear. Use the matching task-specific skill, such as `$skill-creator`, and let
the current agent perform the work inline:

`locate -> edit -> targeted validation -> inspect diff -> scoped commit`

- Do not create a Dev goal or Dev State, resolve or mutate a tracker issue,
  create a Dev branch/worktree, or start Dev repository discovery, technical planning,
  implementation, verification, Review, Product Review, or merge
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
4. For an existing issue, run the Direct Dev Entry Audit below. A prior PM
   handoff remains sufficient evidence, but it is not the only valid entry.
5. If no relevant issue exists, create the initial issue record first with a concise outcome-oriented title, the raw request, repo/product context, and explicit unknowns. Assign the current/requesting user when known, then route it through `$pm` and `$pm-readiness-review` before Dev starts. The record is not automatically dev-ready.
6. If tracker tools are unavailable, provide the exact search result or creation draft and stop before branch/worktree setup or implementation.

This gate applies to unnumbered bugs, features, regressions, and follow-ups. A
project, milestone, parent issue, issue set, or multi-issue request routes to
`$dev-project-orchestrator` rather than collapsing the scope into one duplicate
issue record.

## Direct Dev Entry Audit

An explicit `$dev <existing issue>` request may begin without replaying PM when
the issue itself is already a high-density engineering contract. Perform this
read-only audit before branch/worktree creation or repository research:

- confirm it is one coherent buildable outcome, not a project or hidden issue
  sequence, and bind this finding to `delivery_shape: single` in the current
  Router receipt;
- identify the objective, current/expected behavior, in-scope work, meaningful
  non-goals, and critical acceptance criteria from the issue and linked evidence;
- verify material product rules are user-authored, inherited from cited current
  behavior, or otherwise explicitly confirmed; no unresolved product choice may
  be invented by Dev;
- confirm dependencies, repository ownership, and execution order are clear
  enough to start;
- distinguish implementation inputs from human/device/credential/deployment or
  production-only proof that can remain pending until outcome completion.

If these checks pass, record `Readiness Basis: existing canonical issue` in Dev
State, build the implementation brief from those sources, and continue in the
requested Dev mode. Do not create filler PM comments, invoke PM workers, rewrite
the issue, or add `scoped` merely to reproduce an already-sufficient record.
Issue status, assignee/delegate, labels, description length, or an existing
branch are supporting context, never sufficient proof by themselves.

If the receipt is `multi` or `ambiguous`, stop this
audit before branch/worktree creation, repository research, goals, or
delegation. Return the entire provisional umbrella to
`$pm-project-orchestrator`; Dev must not choose child boundaries or treat an
existing Ready label/status as a waiver. Multiple files, layers, technologies,
commits, expected PRs, estimate, or ordinary synchronous QA alone do not prove
`multi` and must not cause a mechanical split.

If only outcome-verification logistics are pending and they do not affect the
implementation choice, record `Outcome Verification Readiness: blocked - may
begin development`, preserve the exact requirement through merge/test handoff,
and do not claim overall outcome completion. Route to `$pm-readiness-review`
before Dev mutation when a missing product decision, scope boundary, critical
acceptance criterion, human-safety instruction, or dependency would change what
gets built. Newly created or genuinely ambiguous issues never use this shortcut.
