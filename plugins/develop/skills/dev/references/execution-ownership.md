# Execution Ownership

Read after preflight passes, before planning or executing selected Dev phases. These ownership and operating rules apply throughout the active lifecycle.

## Execution Model

Every worker inherits all available parent permissions for the authorized Dev
lifecycle by default. Only explicit user instructions (including applicable
repository policy) restrict access; enforced runtime limits remain binding.
Controller ownership below is state coordination, not a requirement for human
approval or a prohibition on delegating tools and mutations. Phase transitions,
PR creation, CI repair, eligible merge and cleanup proceed automatically within
the requested lifecycle. Name the actual user restriction or runtime denial if
one blocks execution; never invent a permission gate from a role or phase.

`$dev` is the state owner. Narrow Dev skills are role boundaries; use the [implementation workflow](implementation-validation.md) or [PR/closeout workflow](pr-closeout.md) ownership rules to decide whether each phase runs in the main thread, a bounded sub-agent, or a serial worker.

Before any delegation, run the executable `$agent-routing` helper using its [input contract](../../agent-routing/references/jev-input.md). Supply observed task, authority and runtime facts; accept its envelope and binding without loading classification policies or repeating the decisions. Existing controllers retain their actual runtime bindings. Fresh issue threads keep their returned controller route. A blocked packet stops dispatch. Routing does not change the ownership and serialization rules below.

For every bounded agent or fresh Dev worker thread, publish the shared routing
request before dispatch and the resolved routing notice after the runtime
accepts it. Include the accepted binding in the handoff, require the shared
routing receipt in the returned artifact or callback, and verify it before
advancing Dev State.

- Sub-agents produce artifacts. `$dev` accepts or rejects artifacts and owns Dev State transitions.
- `$dev` owns issue, PR, branch, worktree, mode, phase sequencing, retry counters, blocker decisions, user communication, and final completion claims.
- `$dev` coordinates and may delegate external mutations: branch/worktree setup, tracker status changes, PR creation against the resolved issue PR base, eligible issue-base merges, branch cleanup, worktree cleanup, and authorized test-environment handoff. `$release` owns production promotion and resolves its merge executor from the repository release policy.
- Delegate when independent judgment, context/tool isolation, meaningful parallel
  investigation, capability, or an explicit user request needs it. Otherwise a
  bounded phase may run inline when its scope, context, tools, and permissions
  are clear. A new Skill or phase name alone is not a reason to create an agent.
- Keep one mutating or validation owner per branch/worktree. The same
  implementation worker may apply `$dev-test`, classify local failures, and
  execute a scoped implementation or PR repair; report each selected phase's
  evidence for controller acceptance. Do not start competing writers; retaining
  the worker across phases requires no renewed user permission.
- Preserve explicit independence and delegation requirements. `$review` still
  runs isolated reviewers; a required independent verifier or Product Review
  cannot be replaced by implementer self-approval. Delegate useful independent
  investigations rather than making inline execution universal.
- When dispatching a worker, use the runtime adapter and capability rules:
  `worker/fast` requires every shared fast-tier gate; otherwise use at least
  `worker/standard` and raise depth/capability for the actual task. Reuse an
  existing worker only while its accepted capability, context, tools, and
  permissions remain suitable. A new capability need returns to the controller.
- Coordinate high-impact state mutations under one owner, executing inline or
  delegating with inherited permissions: `$dev-git-setup`, `$dev-pr-writer`, controller-owned PR traceability/status sync, `$review`, `$dev-merge-handoff`, the issue-base merge, test-environment handoff, and cleanup. `$dev` never operates a production-promotion merge; only `$release` may do so when the repository policy and current authorization allow it.
- An `operator/fast` agent may apply a controller-decided mechanical tracker update only after the controller provides the exact target and mutation; the controller still verifies the resulting live state.
- Parallelize only read-only or independent discovery/review work. After every delegated phase, update Dev State from the returned artifact before starting the next phase.

## Routing And Ownership Contract

Treat Dev skills as ordered owners of the current state, not as an exclusive taxonomy. A task may need diagnosis, API research, architecture, testing, and review, but only one phase owns the next mutation or decision.

- Select exactly one current phase owner and keep later applicable skills queued in Dev State. The current owner may coordinate independent read-only subtasks in parallel without transferring phase ownership.
- Resolve work cardinality before issue-level execution:
  - One dev-ready issue with `delivery_shape: single`: `$dev`.
  - One provisional umbrella issue with `delivery_shape: multi` or
    `ambiguous`: `$pm-project-orchestrator` before any
    Dev lifecycle mutation.
  - Multiple issues, a project, milestone, parent issue, or dependency sequence:
    `$dev-project-orchestrator`. The project controller may own the entire graph
    and dispatch multiple issue workers; every issue worker remains scoped to
    exactly one issue.
  - Multiple PRs or branches requiring merge order, contract checks, conflict handling, or combined validation: `$dev-integration-manager` for that integration checkpoint.
- Resolve overlapping Dev roles by the current question:

| Current question or evidence | Primary owner |
| --- | --- |
| A pre-implementation defect, regression, crash, or wrong behavior needs a root cause, or `$dev-test` explicitly escalated an unexplained validation failure | `$dev-debugger` |
| No defect is being diagnosed, but technical feasibility or the implementation direction is unknown | `$dev-spike` |
| Third-party API, SDK, provider, pricing, auth, or external contract behavior is the deciding unknown | `$dev-api-research` |
| Technical approach, domain invariants, refactor migration, or implementation sequence needs a decision | `$dev-planner`, with its selected domain/refactor reference |
| Initial post-implementation validation before PR creation, including first failures discovered in that phase | `$dev-test` |
| A PR check is red, or `$dev-test` explicitly escalated a repeated CI/environment failure | `$dev-ci-repair` |
| PR review comments or merge conflicts need changes | `$dev-implementer` with its PR-repair reference and current batch gate |
| Implementation completion claims need fresh pre-PR evidence | `$dev-verifier` |
| Standard technical review after PR creation, or explicit standalone/local/no-context technical review | `$review`; use the default `Review Lens: thermo-nuclear` |
| Product intent and acceptance-criteria conformance | `$pm-pr-product-review` |
| One issue PR needs final issue-merge gates, cleanup, and test handoff | `$dev-merge-handoff` |
| Verified integration candidate needs production promotion | `$release` |

- When several rows apply, start with the earliest unresolved cause. Let that owner route to the next phase instead of running competing owners in parallel.
- Preserve lifecycle ownership when new evidence appears inside a phase. `$dev-test` classifies its first validation failure and routes an obvious change-caused failure to `$dev-implementer`; route to `$dev-debugger` only when root-cause investigation remains necessary.
- When review comments or merge conflicts and red CI checks coexist on one PR, run `$dev-implementer` first, rerun focused validation, then route any remaining red checks to `$dev-ci-repair`.
- Keep one mutating owner per branch/worktree and one controller for issue, PR, tracker, merge, and cleanup state.
- End every phase with an accepted artifact plus a named next owner, `complete`, or a concrete `blocked` state. Do not silently drop an unresolved branch.

## Operating Rules

- When `$dev` was not explicitly invoked, apply the Direct Exclusion Gate before tracker search, goal creation, branch/worktree setup, repository-wide research, or delegation. Return immediately when Direct Artifact or Direct Patch applies.
- Require a dev-ready issue, spec, or Linear ID. For an existing record without a verified PM handoff, run the Direct Dev Entry Audit; proceed when equivalent evidence is present. For an unnumbered issue-level request, run the Issue Resolution Gate first; if no relevant issue exists, create the record and route it through PM readiness before any Dev mutation. If readiness is unclear, route back to `$pm-readiness-review`.
- Read approved Design artifacts, selected directions, token sources, and design-review findings when present. Treat them as implementation inputs alongside the PM acceptance criteria; do not silently redesign the selected direction.
- Do not require a visual artifact for ordinary UI implementation when the PM UI proposal is already clear. If implementation depends on an unresolved visual decision or missing prototype, route that decision to `$design` before coding rather than inventing it inside Dev.
- If the input is a project, milestone, parent issue with multiple child issues,
  multiple dev-ready issues, or an ordered dependency chain, route the full
  supplied scope to `$dev-project-orchestrator`. Do not silently keep only one
  issue or require the caller to restart the chain issue by issue.
- If the input is one issue whose Router Delivery Shape receipt is `multi` or
  `ambiguous`, route the full provisional umbrella to
  `$pm-project-orchestrator`. `$dev-project-orchestrator` begins only after PM
  materializes the child issue set and each included issue has current
  readiness.
- If the input is multiple PRs/branches, cross-branch conflicts, merge order, integration branch work, API/schema/client contract verification across PRs, or combined validation after several PRs, route to `$dev-integration-manager`.
- Read live repo, branch, PR, CI, and tracker state before making current-state claims.
- After a passing Resume Receipt, run `$dev-git-setup` only when branch, worktree, or base reconciliation is required. Otherwise reuse the matching current state and continue from its validated pending lifecycle gate; `$dev-git-setup` defaults to a separate worktree and uses current-checkout branch mode only when explicitly required.
- Normalize Linear issue IDs exactly, preserving uppercase project keys. Default branch type to `feature/ISSUE-ID`; use `fix/ISSUE-ID` for defects, regressions, or repair work.
- Inspect repo root, current branch, existing worktrees, target branch, base branch, and worktree status before changing anything. Reuse existing issue branches/worktrees when present.
- Do not discard, stash, overwrite, or revert local changes unless the user explicitly approves.
- Diagnose bugs before fixing them. For defects, regressions, crashes, hangs, wrong behavior, flaky behavior, and failed acceptance checks, run `$dev-debugger` after repo context unless the issue already contains a concrete root cause and verification plan.
- Reduce real unknowns before architecture. Use `$dev-spike` for unclear technical feasibility or competing implementation paths, and `$dev-api-research` for third-party API or SDK behavior that could change the architecture.
- Use `$dev-planner` when an unresolved technical approach, domain invariant,
  refactor migration, or non-obvious sequence needs a plan. It selects its
  domain/refactor references and returns one Technical Plan; a clear local
  change may use the brief without any design document.
- Use `$dev-api-steward` for our own backend/API contract stewardship whenever implementation may change internal API behavior, request/response shapes, OpenAPI/Swagger, generated clients, examples, changelog, versioning, migration guidance, errors, pagination, auth, webhooks, or client compatibility.
- Run `$dev-api-steward` twice for API-changing work: pre-implementation using the current approach/brief to lock contract intent and post-implementation before `$dev-test` to update docs/changelog/examples and produce a contract review.
- Select `$dev-implementer` platform reference(s) from repo evidence and the dev plan. Record selected reference(s) in Dev State before coding starts.
- Keep one active owner per phase. Do not let implementation, review fixes, and CI repair all change scope independently.
- Keep product scope fixed. If a requested code change would alter product behavior beyond the approved spec, stop and route back to PM.
- Do not equate tests, CI, PR Product Review, merge, or deployment with a required production-loop pass. Use the contract's environment, verifier, and threshold, and keep human acceptance separate.
- Enforce at most three implementation/test repair attempts for the same
  failing check. Apply the [Dev-Managed Review Transition Gate](pr-closeout.md) and its shared
  state machine for review/CI repair limits.
- Keep `$pm-pr-product-review` separate from Dev testing. Dev proves technical correctness; PR Product Review proves requirement conformance when user/product behavior or approved acceptance criteria change. Record internal maintenance as `not applicable`; skip it in fast mode and record the skip in Dev State and closeout reporting.
- When the phase plan selects `$review`, pass the current target and required coverage. Post to GitHub only when that exact PR posting action is explicitly authorized; otherwise retain the review artifact without blocking analysis. Fast mode records `technical review: skipped (fast mode)`.
- Use only the Dev-Managed Review Transition Gate to enter `$review`; it is the
  sole technical-review gate and fails closed when Review v2 or its complete
  combined artifact is missing or incompatible.
- When the runtime requires a tool approval for an otherwise authorized workflow action, make the approval-bearing tool call and continue if it is granted. Do not replace the real tool approval with a hypothetical conversational blocker before attempting the action.
- Do not mark the Dev workflow complete after implementation or PR creation alone. Completion requires the mode-appropriate issue-base merge and test-environment lifecycle in the development-mode contract. In fast mode, skipped gates must be recorded before completion. Applicable Product Review and test/outcome gates remaining after mode waivers remain blocking. Required review and selected QA remain blocking.
- Apply the mode contract to legacy `human-acceptance-required` labels. After an eligible issue-base merge, waived human/real-environment evidence does not prevent implementation `Done`; preserve the skip and any separate acceptance ticket without claiming human acceptance.
- After PR creation, ensure PR traceability before combined technical Review or Product Review: have the controller verify related Linear IDs, make sure the PR visibly references every confirmed related issue, and move confirmed related issues to `In Review` or the workspace equivalent unless that exact update is already complete.
- If branch names, commits, PR metadata, PM handoff, and Linear relationships imply different issue IDs, pause before mutating tracker status and ask which issue set is in scope.
- In fast, standard, and strict modes, create every Dev commit unsigned with per-command signing disabled, such as `git -c commit.gpgsign=false commit ...`, and report that commits were unsigned. Do not prompt for, unlock, configure, or troubleshoot 1Password, GPG, SSH, or global signing settings.
- Strict uses the same signing rule; preserve any explicit user signing requirement without changing global settings.
