# PR, Review, Repair And Closeout

Read before PR preparation, traceability, Review readiness, review/CI repair, Product Review, or merge/test handoff. Apply the root phase plan and development-mode contract; resume the pending gate.

### Dev-Managed Review Transition Gate

Apply this gate before starting `$review`, before any review/CI repair mutation,
and before accepting a repaired head.

- Dev-managed Review starts only for the current PR after PR traceability sync.
  A pre-PR immutable diff is standalone advisory evidence; it cannot create or
  resume the Dev Review Run, consume its budget, trigger automatic repair, or
  satisfy the Dev technical-review gate.
- Record Review Readiness before dispatch: current PR/base/head identity;
  dependency or stacked-PR state; and evidence that repository-required
  generated, schema, migration, and packaging artifacts are in their
  merge-ready representation. Return incomplete preparation to its owning Dev
  phase instead of asking Review to inspect known process artifacts.
- Route the earliest failed preparation invariant to one owner: unfinished
  repository-required artifacts to `$dev-implementer` followed by the selected
  validation gate; missing or stale validation to `$dev-test` / `$dev-verifier`;
  an unresolved multi-branch dependency or stack to
  `$dev-integration-manager`; and an otherwise ready branch without its current
  PR to `$dev-pr-writer`. Re-evaluate Review Readiness after that owner returns;
  do not dispatch preparation owners concurrently.
- Persist the Review Run ID, generation, attempt count, frozen head, prior
  combined artifact, generation status, effective repair limit/authority and
  derived remaining budget in Dev State. Validate the Repair State Machine before reviewer dispatch or code
  mutation. Missing or discontinuous state blocks; never infer fields, reset a
  counter, or start a replacement run for the same logical PR.
- Accept repair instructions only from one current combined artifact produced
  after the complete core, signaled conditional, judge,
  and final-base/head sequence. Collect every confirmed mode-blocking finding into one
  repair batch; an individual specialist result cannot trigger a fix.
- Before a third or later repaired head across the issue/PR history, run the convergence checkpoint from
  the Review contract. Re-enter architecture/planning, split the work, or route
  to PM when the repair shows a repeated root cause or an unplanned contract,
  persistent-model, migration-order, ownership, cross-repository, or product
  expansion. A changed product decision routes to `$pm`; a new contract,
  persistent model, migration/deployment order, ownership, or cross-repository
  design routes to `$dev-planner`; a bounded
  sequencing or slice gap within settled architecture routes directly to
  `$dev-planner`. Do not use changed-line or file-count thresholds.
- At the effective repair limit, an unresolved result blocks before further
  fixes or reviewer dispatch. Use the [shared state contract](dev-review-v2-contract.md#repair-and-re-review-state)
  for exact user overrides; default attempt `5` still blocks generation `7`.

## PR And Closeout Workflow

9. Open or reuse the PR with `$dev-pr-writer`.
   - Owner: controller-coordinated mutation, inline or delegated with inherited permissions (`$dev-pr-writer`).
   - Resolve the PR base through [branch strategy](branch-strategy.md), including the inherited batch branch.
   - Before opening the PR, satisfy repository-defined completion rules for
     generated, schema, migration, and packaging artifacts. Verify that the
     selected base/dependency is available remotely or record the explicit
     stacked-PR dependency; do not carry an implicit local-only base into Review.
   - Capture PR number, URL, head branch, base branch, and latest commit.
   - Do not merge the PR.

9. Sync PR traceability and review status in the controller.
   - Owner: controller-coordinated mutation, inline or delegated with inherited permissions (controller-owned PR traceability/status sync).
   - Verify related Linear IDs from the PM handoff, issue relationships, branch name, PR title/body, commits, and linked issues.
   - Ensure the PR visibly references every confirmed related Linear issue ID in the title, body, or one concise PR comment.
   - Move confirmed related issues to `In Review` or the workspace's equivalent review state.
   - Do not move unrelated parents, blocked work, future work, or speculative follow-ups into review.
   - Use the active authorized GitHub and tracker tools directly; no separate Skill is required. Re-read the exact PR and issue states after writes, and reuse already-complete links/status updates.
   - If tools are unavailable, produce the exact PR comment and tracker update draft, preserve traceability as pending, and do not claim sync or advance the dependent Review gate.

10. Run the phase-plan-selected technical review gate.
   - Owner: `$review` as the sole selected technical-review gate, with authorized GitHub posting coordinated by the controller.
   - Require the PR captured by this workflow, not repo recency. Do not start a
     Dev-managed Review Run for a local immutable diff.
   - In fast mode, do not invoke `$review`. Record `technical review: skipped (fast mode)` and continue.
   - Normal standard/strict plans select Review Contract Version 2 and start one `$review` generation only after PR traceability sync and a passing Review Readiness record. A tracked-artifact plan defaults it unselected in standard/strict unless an existing trigger applies. Pass repo path, PR URL or number, head branch, base branch, immutable head/base revisions, dependency state, merge-ready artifact evidence, mode, governing authority, and review start time whenever selected.
   - Pass the effective required engineering claims and mode-waived evidence
     separately, with the source and unverified status. A waived real-world
     test must not reappear as a mandatory missing-evidence Review finding.
   - `$review` owns core and signaled conditional fan-out, judge, final-base/head validation, and authorized final posting.
   - Every selected Review run requires `Review Lens: thermo-nuclear` for the code-quality core lens in the same run. Stale, blocked, or unsuccessful required coverage remains a gate.
   - Consume only `$review`'s complete combined Contract Version 2 result. Do
     not mutate from an individual core or conditional artifact.
     Route its complete confirmed mode-blocking implementation batch to `$dev-implementer`, its
     complete failing-check/CI batch to `$dev-ci-repair`, stop on
     `coverage-blocked`, and advance only from a current accepted result whose
     common action permits it.
   - If `$review` is unavailable, returns a missing/incompatible contract version, or cannot run the core gate, return `blocked - Review Contract Version 2 unavailable or incompatible`. Do not fall back to Review v1 or a local generic reviewer.

11. Repair review comments, conflicts, and CI failures.
   - Owner: the current suitable implementation worker using `$dev-implementer`'s PR-repair reference for comments/conflicts; `$dev-ci-repair` owns failing checks, still with one writer.
   - Before dispatch or mutation, validate the Review Run state and hard
     ceiling and its authority. Missing/discontinuous state or unresolved work
     at the effective limit blocks without resetting the run or applying a
     partial fix.
   - Send one accepted combined artifact and all of its confirmed mode-blocking
     items as one repair batch. Accept one resulting repaired head and increment
     the shared attempt count once, regardless of the number of findings or
     coherent commits in that batch.
   - Before a third or later repaired head across the issue/PR history, record the convergence checkpoint.
     If remediation expands the approved contract, persistent model, migration
     order, ownership, cross-repository surface, or product behavior, re-enter
     the explicitly owned `$pm` / `$dev-planner` route above
     before editing; ordinary `$dev-implementer` does not absorb that scope.
   - Use `$dev-implementer`'s [PR-repair reference](../../dev-implementer/references/pr-repair.md) for merge conflicts and Review batches. In standard/strict mode, use it for findings crossing the selected severity threshold or mandatory acceptance failures; retain other comments as advisories. In fast mode, fix only unskippable critical/primary-path findings and record other known findings as skipped or unverified.
   - Nonblocking fixes may join an already-required scoped repair batch; an advisory-only result advances without a new repair/review loop.
   - Use `$dev-ci-repair` for failing PR checks.
   - When both are present, finish `$dev-implementer` and focused revalidation first, then inspect and repair any CI checks that remain red.
   - Rerun relevant validation after every fix commit.
   - Treat every relevant code, test, config, generated-output, or documentation
     change as invalidating prior verification evidence. Rerun `$dev-verifier`
     against the latest exact PR head only when its phase-plan gate was selected
     or a new trigger selects it; otherwise preserve the tracked-artifact
     validation floor and record the current focused rerun before returning to
     Review or merge handoff.
   - Whenever an accepted repair batch creates one new head, invalidate prior
     evidence and return to one complete `$review` generation with
     the default thermo-nuclear rubric.

12. Run `$pm-pr-product-review`.
    - Owner: sub-agent artifact by default (`$pm-pr-product-review`).
    - In fast mode, do not run PR Product Review. Record `PR Product Review: skipped (fast mode)` and the unverified acceptance/edge-case scope.
    - In standard/strict mode, PR Product Review is required after review comments are resolved or explicitly handled and before merge handoff when user/product behavior or approved acceptance criteria changed. Record internal maintenance as `not applicable`; do not use an out-of-scope assertion to bypass an applicable product gate.
    - If PR Product Review reports `Failed - Different` or `Failed - Incomplete`, treat it as required product feedback. Fix valid gaps, rerun focused validation and the mode-appropriate QA bar, handle any new review comments, then rerun `$pm-pr-product-review`.
    - If PR Product Review is blocked because Linear, GitHub, review state, diff, or access evidence is unavailable, report the blocker and do not claim product-scope pass.

13. Run `$dev-merge-handoff`.
    - Owner: controller-coordinated mutation, inline or delegated with inherited permissions (`$dev-merge-handoff`).
    - Pass mode and all skipped/unverified entries. In standard/strict mode, hand off only after applicable PR Product Review passes or internal maintenance is recorded `not applicable`. In fast mode, hand off after the reduced validation contract passes and the omissions are current in Dev State.
   - `$dev-merge-handoff` owns merge readiness, final conflict/comment/check gates, resolved-base merge, remote/local branch cleanup, local worktree cleanup, test-environment handoff, release-candidate evidence, risk/rollback notes, and tracker closeout.
   - If merge handoff returns an environment or human-acceptance wait, apply
     the mode contract first. A waived surface belongs in `Skipped / Unverified`
     with any separate acceptance follow-up; it does not keep engineering active.
     Preserve waits only for remaining enforced or explicitly authorized gates.
