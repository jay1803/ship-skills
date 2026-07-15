---
name: dev
description: >-
  Dev-stage orchestrator for one coding-ready issue after PM approval. Use when a single Linear issue or product spec is dev-ready and needs controlled repository context, optional bug diagnosis, optional technical spike or API research, technical design or refactor architecture, API contract stewardship for backend/API changes, implementation planning, selected Dev Implementer references, coding, fast-default automated QA, PR creation, PR-to-Linear traceability/status sync, external technical review, review-fix loops, CI repair, PR Product Review, merge, and release handoff. For projects or multiple issues, route to $dev-project-orchestrator; for cross-PR merge/integration control, route to $dev-integration-manager. Defaults to fast/faster mode unless the user explicitly asks for standard/slow hands-on QA.
---

# Dev: Orchestrator

Own the workflow after `$pm-readiness-review` says one issue is ready for engineering. Control the dev-stage state, call the narrow Dev skills in order, and prevent uncontrolled agent wandering.

`$dev` defaults to **fast mode**. Fast mode replaces the legacy fast build path: automated build/test/lint/typecheck/smoke validation, no simulator/live-app/browser hands-on QA unless explicitly required, and unsigned commits by default. Use standard mode only when the user asks for `--standard`, `--slow`, full QA, simulator/device/live-app/manual browser QA, or when the issue genuinely needs hands-on validation.

Default dev workflow:

`$dev-git-setup` -> `$dev-repo-context` -> optional `$dev-debugger` / `$dev-spike` / `$dev-api-research` -> `$dev-architect` or `$dev-refactor-architect` -> optional `$dev-api-steward` pre-implementation contract review -> `$dev-planner` -> `$dev-implementer` with selected platform reference(s) -> optional `$dev-api-steward` post-implementation docs/contract closeout -> `$dev-test` -> `$dev-self-review` -> `$dev-pr-writer` -> `$project-manager` PR traceability/status sync -> `$dev-external-review` -> `$dev-fix` / `$dev-ci-repair` loop -> `$pm-pr-product-review` -> `$dev-release-handoff`

## Goal Contract

The default `$dev` goal is to address the approved feature or bug and land the PR. In repositories where merge triggers CI/CD deployment, the merged PR is the default delivery boundary.

- When goal tools are available, create or reuse one goal for the full lifecycle: implement the approved scope, validate it, open/reuse the PR, pass external technical review and CI, pass Product Review, merge through `$dev-release-handoff`, clean up, and report the release handoff.
- Do not mark the goal complete when code is written, tests pass locally, a PR is opened, external review is requested, or CI is still pending.
- Narrow the goal only when the user explicitly says plan-only, PR-only, no merge, do not merge, stop before merge, or when merge/release handoff is concretely blocked.
- If merge is blocked by permissions, failing checks, unresolved comments, conflicts, product review, or repo policy, mark/report the goal blocked with the exact blocking evidence and next action.

## Execution Model

`$dev` is the state owner. Narrow Dev skills are role boundaries; use the End-To-End Workflow ownership rules to decide whether each phase runs in the main thread, a bounded sub-agent, or a serial worker.

- Sub-agents produce artifacts. `$dev` accepts or rejects artifacts and owns Dev State transitions.
- `$dev` owns issue, PR, branch, worktree, mode, phase sequencing, retry counters, blocker decisions, user communication, and final completion claims.
- `$dev` owns or explicitly gates external mutations: branch/worktree setup, tracker status changes, PR creation, external review triggers, merge, branch cleanup, and worktree cleanup.
- Use sub-agents by default for bounded read/report phases: `$dev-repo-context`, `$dev-debugger`, `$dev-spike`, `$dev-api-research`, `$dev-architect`, `$dev-refactor-architect`, `$dev-planner`, `$dev-self-review`, and `$pm-pr-product-review` when suitable tools exist. Do not run these phases inline in the main thread merely because the main thread has enough context; inline execution is only for unavailable sub-agent tooling, explicit user override, or a concrete blocker that requires main-thread ownership.
- Run mutating or validation-worker phases serially on the active branch/worktree: `$dev-implementer`, `$dev-test`, `$dev-fix`, and `$dev-ci-repair`. Do not run two mutating workers against the same branch/worktree at the same time.
- Keep high-impact state mutation main-owned or tightly gated: `$dev-git-setup`, `$dev-pr-writer`, `$project-manager` PR traceability/status sync, `$dev-external-review`, `$dev-release-handoff`, merge, and cleanup.
- Parallelize only read-only or independent discovery/review work. After every delegated phase, update Dev State from the returned artifact before starting the next phase.

## Mode Selection

- **Fast mode is default** for `$dev`, `$dev --fast`, `$dev --faster`, and requests that say speed matters, the change is non-visual, or build-plus-tests are enough.
- **Standard mode** is selected only for `$dev --standard`, `$dev --slow`, or explicit requests for hands-on simulator/device/live-app/manual browser QA.
- In fast mode, do not boot a simulator, launch a live app, or drive a browser manually unless the user explicitly overrides the mode or the feature cannot be responsibly validated without hands-on QA.
- In standard mode, run the same automated checks first, then add project-appropriate hands-on QA for user-visible iOS, macOS, or browser behavior.
- Record `Mode: fast` or `Mode: standard` in Dev State and pass it to every narrow Dev skill that validates, fixes, commits, or reports QA.

## Operating Rules

- Require a dev-ready issue, spec, or Linear ID. If readiness is unclear, route back to `$pm-readiness-review`.
- Read approved Design artifacts, selected directions, token sources, and design-review findings when present. Treat them as implementation inputs alongside the PM acceptance criteria; do not silently redesign the selected direction.
- Do not require a visual artifact for ordinary UI implementation when the PM UI proposal is already clear. If implementation depends on an unresolved visual decision or missing prototype, route that decision to `$design` before coding rather than inventing it inside Dev.
- If the input is a project, milestone, parent issue with multiple child issues, or multiple dev-ready issues, route to `$dev-project-orchestrator` instead of trying to manage the whole project inside `$dev`.
- If the input is multiple PRs/branches, cross-branch conflicts, merge order, integration branch work, API/schema/client contract verification across PRs, or combined validation after several PRs, route to `$dev-integration-manager`.
- Read live repo, branch, PR, CI, and tracker state before making current-state claims.
- Claim the issue and create or reuse the branch/worktree before repository research and implementation. Use `$dev-git-setup`; it defaults to a separate worktree and uses current-checkout branch mode only when explicitly required.
- Normalize Linear issue IDs exactly, preserving uppercase project keys. Default branch type to `feature/ISSUE-ID`; use `fix/ISSUE-ID` for defects, regressions, or repair work.
- Inspect repo root, current branch, existing worktrees, target branch, base branch, and worktree status before changing anything. Reuse existing issue branches/worktrees when present.
- Do not discard, stash, overwrite, or revert local changes unless the user explicitly approves.
- Diagnose bugs before fixing them. For defects, regressions, crashes, hangs, wrong behavior, flaky behavior, and failed acceptance checks, run `$dev-debugger` after repo context unless the issue already contains a concrete root cause and verification plan.
- Reduce real unknowns before architecture. Use `$dev-spike` for unclear technical feasibility or competing implementation paths, and `$dev-api-research` for third-party API or SDK behavior that could change the architecture.
- Use `$dev-refactor-architect` instead of `$dev-architect` when the approved work is primarily refactor, architecture cleanup, module split, dependency inversion, migration, or tech-debt reduction where behavior should remain stable.
- Use `$dev-api-steward` for our own backend/API contract stewardship whenever implementation may change internal API behavior, request/response shapes, OpenAPI/Swagger, generated clients, examples, changelog, versioning, migration guidance, errors, pagination, auth, webhooks, or client compatibility.
- Run `$dev-api-steward` twice for API-changing work: pre-implementation after `$dev-architect` or `$dev-refactor-architect` to lock contract intent and post-implementation before `$dev-test` to update docs/changelog/examples and produce a contract review.
- Select `$dev-implementer` platform reference(s) from repo evidence and the dev plan. Record selected reference(s) in Dev State before coding starts.
- Keep one active owner per phase. Do not let implementation, review fixes, and CI repair all change scope independently.
- Keep product scope fixed. If a requested code change would alter product behavior beyond the approved spec, stop and route back to PM.
- Enforce retry limits: at most three implementation/test repair attempts for the same failing check, and at most five review/CI repair loops before stopping with a blocker.
- Keep `$pm-pr-product-review` separate from Dev testing. Dev proves technical correctness; PR Product Review proves requirement conformance.
- Do not mark the Dev workflow complete after implementation or PR creation alone. Completion requires implementation, technical validation, self-review, PR creation, external technical review, review/CI repair handling, PR Product Review, merge, and release handoff to be complete or explicitly blocked/skipped by the user.
- After PR creation, ensure PR traceability before external technical review or Product Review: use `$project-manager` to verify related Linear IDs, make sure the PR visibly references every confirmed related issue, and move confirmed related issues to `In Review` or the workspace equivalent unless that exact update is already complete.
- If branch names, commits, PR metadata, PM handoff, and Linear relationships imply different issue IDs, pause before mutating tracker status and ask which issue set is in scope.
- In fast mode, create every Dev commit unsigned with per-command signing disabled, such as `git -c commit.gpgsign=false commit ...`, and report that commits were unsigned. Do not prompt for, unlock, configure, or troubleshoot 1Password, GPG, SSH, or global signing settings.
- In standard mode, use the repo's normal commit behavior, but if signing blocks progress, create the required commit unsigned with per-command signing disabled and report that signing was skipped. Do not change global signing configuration unless the user explicitly asks.

## Implementer Reference Selection

Use `$dev-implementer` for coding, and choose the narrowest platform reference(s) that match the changed surface. Multiple references are allowed when the issue crosses layers; sequence backend/API contracts before clients by default.

- `implement-ios.md`: iOS app code, Xcode iOS targets, iOS simulator/device build-run-debug, UIKit, iOS SwiftUI screens, App Intents, iOS runtime behavior.
- `implement-macos.md`: macOS app code, AppKit, macOS SwiftUI scenes/windows/menus, macOS build-run-debug, signing, entitlements, packaging, SwiftPM GUI apps.
- `implement-swiftui.md`: SwiftUI-specific view, state, layout, navigation, animation, accessibility, preview, performance, Liquid Glass, or Instruments trace work across iOS/macOS. Pair with `implement-ios.md` or `implement-macos.md` when platform build/run support is also needed.
- `implement-web.md`: frontend web app code, React, Next.js, Vite, dashboards, responsive browser UI, client state, browser tests.
- `implement-backend.md`: backend/API/service code, workers, jobs, queues, persistence, migrations, auth, permissions, service contracts, and backend integration tests.
- `implement-supabase.md`: Supabase backend code, migrations, RLS, Auth, Edge Functions, Storage, Realtime, cron, queues, generated types, backend API behavior.

Project defaults are allowed when the repo clearly documents one, but they are advisory. If the actual issue touches a different surface, route by the issue and repo evidence. Ask only when two implementers would make materially different architecture or product-scope decisions.

## Project Classification And QA

Before implementation and before QA, classify the project and touched surface from repo files, package manifests, workspace/project files, framework conventions, scripts, CI config, and changed code:

- iOS app
- macOS app
- shared Apple-platform app code
- backend/API/service
- website frontend
- full-stack web
- library/CLI/package
- docs/config-only
- mixed

In fast mode, the QA bar is automated and project-appropriate:

- Apple app changes: in-scope iOS/macOS build plus relevant unit tests. Use `@build-ios-apps` before choosing iOS `xcodebuild` commands; use relevant `build-macos-apps:*` guidance for macOS build/test diagnostics.
- Backend/API/service changes: backend build, lint/typecheck, unit/integration tests, migration/schema checks, service/API smoke checks when available, and `$dev-api-steward` contract/docs closeout when API behavior changed.
- Website frontend changes: production build, lint/typecheck, unit/component tests, and non-interactive route or E2E smoke checks when available.
- Full-stack changes: relevant backend and frontend automated checks plus a contract or end-to-end smoke path when practical.
- Library/CLI/package/docs/config work: package tests, representative command/API smoke tests, formatting, link, schema, or config validation.

In standard mode, run the fast automated bar first, then add hands-on QA when the touched behavior is user-visible:

- `$dev-test` must run hands-on iOS Simulator validation for user-visible iOS behavior after a clean build.
- `$dev-test` must run hands-on local-app validation for user-visible macOS behavior after a clean build.
- `$dev-test` must run browser/manual E2E validation for user-visible web behavior when the repo supports it.

Skip a QA surface only when the repo/change has no runnable surface for it or the work does not touch that behavior. State the skip rationale. A failing build, lint/typecheck, automated test, migration/schema check, smoke check, or valid hands-on QA finding is a QA failure; fix it or report it as blocked.

## End-To-End Workflow

Delegation legend for the numbered workflow:

- **Main thread**: `$dev` orchestrator owns Dev State, goal lifecycle, branch/worktree setup, PR creation, tracker/PR mutations, external review requests, merge/release handoff, user communication, and blocker decisions.
- **Sub-agent artifact**: run the named skill in a bounded sub-agent by default. The sub-agent returns an artifact; `$dev` updates Dev State and decides the next phase.
- **Serial worker**: run on the active branch/worktree with one mutating or validation owner at a time. Do not parallelize serial workers against the same branch/worktree.
- **Conditional**: choose sub-agent artifact for read/report-only work; choose serial worker or main-thread ownership when the phase must edit files, push commits, mutate tracker/PR state, or use gated external credentials.

1. Start or reuse one active goal for the full Dev lifecycle when goal tools are available.
   - Owner: main thread (`$dev` orchestrator).
   - Default goal: address the approved feature or bug and merge the PR through release handoff.
   - Cover branch/worktree setup, issue/spec reading, implementation, validation, QA, PR creation, external technical review, review/comment/CI repairs, PR Product Review, merge, cleanup, and release handoff.
   - Do not create a second implementation-only goal.
   - Do not mark the goal complete at PR creation unless the user explicitly set a PR-only boundary.

2. Resolve the issue/spec, repo, mode, base branch, and branch/worktree with `$dev-git-setup`.
   - Owner: main thread gated mutation (`$dev-git-setup`).
   - Read Linear title, description, comments, attachments, linked context, status, labels, and acceptance criteria when tools are available.
   - Build a compact implementation brief: objective, in-scope work, non-goals, acceptance criteria, project classification, validation expectations, QA mode, and known risks.
   - If the issue is not dev-ready, stop with the missing decision and route to `$pm-readiness-review`.

3. Run `$dev-repo-context`, optional `$dev-debugger` / `$dev-spike` / `$dev-api-research`, `$dev-architect` or `$dev-refactor-architect`, optional pre-implementation `$dev-api-steward`, and `$dev-planner`.
   - Owner: sub-agent artifact by default for `$dev-repo-context`, `$dev-debugger`, `$dev-spike`, `$dev-api-research`, `$dev-architect`, `$dev-refactor-architect`, and `$dev-planner`.
   - Owner: conditional for pre-implementation `$dev-api-steward`; use a sub-agent artifact for contract review, but keep any contract-doc/generated-client/changelog edits serial and gated.
   - Use `$dev-debugger` when the issue is a bug, regression, crash, hang, wrong behavior, flaky behavior, or failed acceptance check.
   - Use `$dev-spike` when repo context exposes a feasibility unknown, risky local behavior, or multiple plausible implementation paths.
   - Use `$dev-api-research` when the work depends on third-party API, SDK, webhook, auth, rate-limit, pricing, sandbox, or data-model behavior.
   - Use `$dev-refactor-architect` when the primary work is structural refactor with behavior invariants, module migration order, rollback, or split-PR decisions.
   - Use `$dev-api-steward` pre-implementation when the planned work may change our API contract. Pass the contract review into `$dev-planner`.
   - Pass any bug diagnosis brief, spike report, API research brief, refactor architecture brief, or API Steward contract review into `$dev-architect` / `$dev-refactor-architect` / `$dev-planner` as appropriate.
   - The plan must include `$dev-implementer` reference selection, API Steward follow-up when needed, ordered steps, validation commands, QA mode, and PR/release expectations.

4. Implement with `$dev-implementer` and the selected platform reference(s).
   - Owner: serial worker on the active branch/worktree (`$dev-implementer`).
   - Inspect existing code and tests before editing.
   - Keep changes tied to the issue/spec and implementation brief.
   - Add or update focused tests when practical.
   - Commit only issue-related changes before PR creation. Leave unrelated dirty work untouched.

5. Run post-implementation `$dev-api-steward` when API behavior changed or may have changed.
   - Owner: conditional. Use a sub-agent artifact for implementation-vs-contract review; use a serial worker or main-thread gated edit path for docs, generated clients, changelog, examples, or migration-guide changes.
   - Compare the implementation diff to the intended contract.
   - Update OpenAPI/Swagger, API docs, examples, changelog, versioning notes, and migration guidance when needed.
   - If implementation and contract disagree, route back to `$dev-implementer` before PR creation.
   - If client-impact work spans multiple PRs or repos, route to `$dev-project-orchestrator` or `$dev-integration-manager`.

6. Run `$dev-test` with the selected mode and project QA bar.
   - Owner: serial worker on the active branch/worktree (`$dev-test`).
   - Run the smallest reliable checks first, then broaden when shared behavior, cross-platform code, API contracts, persistence, or user-facing flows are affected.
   - In fast mode, do not use hands-on QA unless explicitly overridden.
   - In standard mode, add required hands-on QA after automated checks.
   - Fix valid QA findings before PR creation. After three failed repair attempts for the same blocker, stop or mark that QA surface blocked with evidence.

7. Run `$dev-self-review`.
   - Owner: sub-agent artifact by default (`$dev-self-review`).
   - Review the local diff like a strict senior engineer before opening the PR.
   - Fix valid self-review findings, rerun focused validation, and commit.

8. Open or reuse the PR with `$dev-pr-writer`.
   - Owner: main thread gated mutation (`$dev-pr-writer`).
   - Default PR base to `develop` unless the repo clearly uses another integration branch.
   - Capture PR number, URL, head branch, base branch, and latest commit.
   - Do not merge the PR.

9. Sync PR traceability and review status with `$project-manager`.
   - Owner: main thread gated mutation (`$project-manager` PR traceability/status sync).
   - Verify related Linear IDs from the PM handoff, issue relationships, branch name, PR title/body, commits, and linked issues.
   - Ensure the PR visibly references every confirmed related Linear issue ID in the title, body, or one concise PR comment.
   - Move confirmed related issues to `In Review` or the workspace's equivalent review state.
   - Do not move unrelated parents, blocked work, future work, or speculative follow-ups into review.
   - If tools are unavailable, produce the exact PR comment and tracker update draft.

10. Run `$dev-external-review`.
   - Owner: main thread gated external mutation (`$dev-external-review`).
   - Prefer the PR captured by this workflow, not repo recency.
   - Start `$dev-external-review` immediately after PR traceability sync. Pass repo path, PR URL or number, head branch, base branch, and review start time.
   - Do not run `$dev-code-review`, a no-context Codex reviewer, or a local technical review as the default `$dev` workflow.
   - If `$dev-external-review` returns `not configured`, missing configuration, or missing required secrets, stop with a concrete external-review blocker instead of falling back to local review.
   - When the external provider accepts the request, require `$dev-external-review` to leave a concise PR comment saying the external review started, with non-sensitive provider/job evidence when available.
   - Wait for the external review's finished signal before deciding whether the PR is clean. A request-accepted response or start comment alone is not completion.

11. Repair review comments, conflicts, and CI failures.
   - Owner: serial worker on the active branch/worktree (`$dev-fix` for review comments/conflicts, `$dev-ci-repair` for failing checks).
   - Use `$dev-fix` for valid review comments and merge conflicts on the captured PR.
   - Use `$dev-ci-repair` for failing PR checks.
   - Rerun relevant validation after every fix commit.
   - Stop after five review/CI repair loops for the same PR with a concrete blocker.

12. Run `$pm-pr-product-review`.
    - Owner: sub-agent artifact by default (`$pm-pr-product-review`).
    - PR Product Review is required after review comments are resolved or explicitly handled and before release handoff, unless the user explicitly says PR Product Review is out of scope.
    - If PR Product Review reports `Failed - Different` or `Failed - Incomplete`, treat it as required product feedback. Fix valid gaps, rerun focused validation and the mode-appropriate QA bar, handle any new review comments, then rerun `$pm-pr-product-review`.
    - If PR Product Review is blocked because Linear, GitHub, review state, diff, or access evidence is unavailable, report the blocker and do not claim product-scope pass.

13. Run `$dev-release-handoff`.
    - Owner: main thread gated mutation (`$dev-release-handoff`).
    - Hand off only after PR Product Review passes or is explicitly not required.
    - `$dev-release-handoff` owns merge readiness, final conflict/comment/check gates, squash merge, remote/local branch cleanup, local worktree cleanup, risk/rollback notes, and tracker closeout.

## Routing

- Project, milestone, parent issue, or multi-issue engineering execution: `$dev-project-orchestrator`.
- Multiple PRs, integration branches, merge ordering, cross-branch conflicts, API/schema/client contract checks across PRs, or combined validation: `$dev-integration-manager`.
- Branch/worktree preparation for one issue: `$dev-git-setup`.
- Repository research: `$dev-repo-context`.
- Bug diagnosis and root-cause brief: `$dev-debugger`.
- Technical uncertainty or feasibility reduction: `$dev-spike`.
- External API or SDK research: `$dev-api-research`.
- Internal backend/API contract stewardship, docs, changelog, versioning, client impact, and migration guidance: `$dev-api-steward`.
- Technical approach: `$dev-architect`.
- Refactor architecture, invariants, migration order, rollback, and split recommendation: `$dev-refactor-architect`.
- Ordered implementation plan: `$dev-planner`.
- Code changes: `$dev-implementer` with selected `implement-*` reference(s).
- Tests, build, lint, typecheck, and acceptance validation: `$dev-test`.
- Pre-PR senior-engineer review: `$dev-self-review`.
- Pull request creation: `$dev-pr-writer`.
- PR-to-Linear traceability and review status updates: `$project-manager`.
- Technical PR review in the default `$dev` workflow: `$dev-external-review`.
- Local or no-context PR review outside the default `$dev` workflow: `$dev-code-review`.
- Review-comment fixes: `$dev-fix`.
- CI/build/lint/test repair: `$dev-ci-repair`.
- Product requirement conformance: `$pm-pr-product-review`.
- Merge-readiness, branch/worktree cleanup, risk, rollback, and release notes: `$dev-release-handoff`.

## Existing Skill Bridge

During migration, reuse existing delivery primitives instead of duplicating fragile tool behavior:

- Branch/worktree setup is owned by `$dev-git-setup`.
- Refactor-heavy technical design is owned by `$dev-refactor-architect`; feature and bug-fix technical design remains `$dev-architect`.
- API contract docs, changelog, examples, versioning notes, and client impact review are owned by `$dev-api-steward` for API-changing work.
- PR creation is owned by `$dev-pr-writer`, including title/body preparation and `gh pr create`.
- PR traceability and `In Review` tracker status are owned by `$project-manager` immediately after PR creation.
- Project-specific external PR review APIs, webhooks, bots, or Claude Code review services are owned by `$dev-external-review`. The default `$dev` workflow blocks when that external path is not configured instead of falling back to local review.
- CI repair is owned by `$dev-ci-repair`, including GitHub Actions PR checks.
- Review-comment fixes and merge-conflict cleanup are owned by `$dev-fix`.
- Merge gating is owned by `$dev-release-handoff`, including squash merge, remote/local branch cleanup, local worktree cleanup, and tracker closeout.
- Requirements conformance remains `$pm-pr-product-review`.

## Output

Keep a concise dev-stage state:

```markdown
## Dev State

Issue: <id/title>
Goal: <address feature/fix bug and merge PR | explicit narrower boundary>
Branch: <branch/worktree>
Mode: <fast | standard>
Phase: <git-setup | repo-context | debug | spike | api-research | architecture | refactor-architecture | api-steward | planning | implementation | test | self-review | PR | pr-traceability | external-review | fix | CI | pr-product-review | release-handoff>
Owner: <$dev orchestrator | sub-agent artifact: <skill> | serial worker: <skill> | conditional: <skill>>
Implementer(s): <$dev-implementer: implement-ios | implement-macos | implement-swiftui | implement-web | implement-backend | implement-supabase | multiple | not selected yet>
PR/Merge: <not opened | open | review/CI pending | blocked | merged>
Status: <ready | running | blocked | retrying | complete>

### Current Artifact
- <The artifact just produced or required next.>

### Next Action
<Next Dev skill or escalation route.>

### Blockers
- <Only concrete blockers, or "None.">
```

Final Dev reports must include the mode, project classification, bug diagnosis decision when used, spike/API research decision when used, refactor architecture decision when used, API Steward result when used, validation commands, QA result, PR URL, PR traceability/status sync result, external-review result, review/CI repair result, PR Product Review result, and release handoff outcome.
