# Implementation And Validation

Read when preparing or running selected pre-PR phases. The numbered lifecycle preserves ownership; the Resume Receipt selects stages and may resume later without replaying completed work.

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

Use the [mode contract](development-mode-contract.md#standard-and-strict-modes)
for validation depth. Standard selects primary-flow and ticket-specific regression
coverage plus necessary build/typecheck and enforced repository/CI checks. Strict
adds risk-selected failure/recovery and integration coverage. Project type helps
locate the smallest sufficient test surface; available suites are not all mandatory.
Use the relevant Apple build target, backend API/schema check, web component/route
test, or CLI/package/config check. API changes retain API Steward closeout.

In fast mode, validate only the primary path with focused unit tests and the minimum build/typecheck/lint/schema/CI checks required to create and merge the PR. Do not exhaustively validate listed edge cases or run optional integration, E2E, smoke, hands-on, review, acceptance, deployment, or production-verification work; record every skip and unknown in Dev State and closeout reporting without opening a dedicated risk ticket merely for the omission.

Select additional hands-on QA from explicit user/repository/acceptance requirements
or a concrete changed-path risk not covered by automated checks. Name the
required iOS device/simulator, macOS app, browser, or runtime surface and expected
result in the receipt. `$dev-test` performs only that selected scope; a UI change
or strict mode alone does not require every platform or adjacent flow.

Apply the development-mode contract before classifying QA as required. In standard/strict mode, real-environment and human test surfaces are waived even when an old ticket requires them. For other QA surfaces, record why they are not applicable when the repo/change has no runnable surface or does not touch the behavior; missing required automated evidence remains blocked. In fast mode, apply the unskippable conditions from the development-mode contract and record every other omitted surface as skipped or unverified.

## End-To-End Workflow

Delegation legend for the numbered workflow:

- **Main thread**: `$dev` orchestrator owns Dev State, goal lifecycle, branch/worktree setup, resolved-base PR creation, tracker/PR mutations, issue-base merge/test handoff, user communication, and blocker decisions. `$release` alone owns production promotion and applies the repository's configured merge executor.
- **Read/report artifact**: delegate when the execution-ownership contract selects isolation, independence, capability, or useful parallelism; otherwise bounded inline work is allowed. `$dev` accepts the evidence and decides the next phase.
- **Serial worker**: keep one mutating/validation owner at a time. Reuse a suitable implementation worker for testing and scoped repair; selected responsibilities and evidence remain explicit without a new agent per phase.
- **Conditional**: apply execution-ownership to read/report work; keep edits and externally mutating actions serial and within the controller's authorized scope.

Before the numbered lifecycle, apply the Resume-First Preflight. When
Dev was not explicitly invoked, its first decision is the Direct Exclusion Gate;
Direct Artifact and Direct Patch return immediately and do not enter this
lifecycle. Otherwise it applies the Issue Resolution Gate and, for an existing
record without a verified PM handoff, the Direct Dev Entry Audit. An unnumbered
issue-level request that enters Dev must be connected to an existing issue or
recorded in a newly created one; no goal, branch, worktree, code investigation,
implementation, tracker/PR mutation, or downstream delegation may begin first.
`pm_required` and `blocked` stop here with zero downstream Dev roles.

1. After `dev_new` or `dev_resume` preflight and its Resume Receipt, start or reuse one active goal for the full Dev lifecycle when goal tools are available.
   - Owner: main thread (`$dev` orchestrator).
   - Default goal: address the approved feature or bug, merge the PR into the resolved issue PR base, and complete the mode-required test handoff.
   - Cover branch/worktree setup, issue/spec reading, implementation, mode-appropriate validation/review gates, PR creation against the resolved issue PR base, review/comment/CI repairs, issue-base merge, cleanup, and test-environment/release-candidate handoff.
   - Do not create a second implementation-only goal.
   - Do not mark the goal complete at PR creation unless the user explicitly set a PR-only boundary.

2. Reconcile issue/spec, repo, mode, base branch, and branch/worktree only when the Resume Receipt requires `$dev-git-setup`.
   - Owner: controller-coordinated mutation, inline or delegated with inherited permissions (`$dev-git-setup`) only for required reconciliation; otherwise continue directly from the validated pending lifecycle gate without duplicate branch/worktree state.
   - The read-only preflight already reads Linear title, description, comments, attachments, linked context, status, labels, and acceptance criteria when tools are available.
   - Build a compact implementation brief: objective, in-scope work, non-goals, acceptance criteria, human-acceptance label/steps when present, production-loop contract/readiness when present, project classification, validation expectations, QA mode, and known risks.
   - Record the readiness basis: verified PM handoff or existing canonical issue audit.
   - If the issue is not dev-ready, stop before any git action with the missing decision and route to `$pm-readiness-review`.

3. Resolve only the missing repository facts, and run selected investigation or
   `$dev-planner` when a real technical decision remains.
   - The current owner gathers source-anchored context; no separate discovery
     artifact is required. Use `$dev-debugger` for an unexplained defect,
     `$dev-spike` for local feasibility, and `$dev-api-research` for third-party
     facts that change the decision.
   - `$dev-planner` owns approach and sequencing in one Technical Plan. It reads
     domain/refactor references only for material invariant, state, ownership,
     or migration decisions. Clear changes use the brief without planning.
   - Run pre-implementation `$dev-api-steward` for backend/API behavior or
     contract changes using the current approach/brief. Feed its constraints
     into the plan when selected; no separate architecture artifact is needed.
   - Preserve selected platform guidance, required verification/fidelity,
     production-loop thresholds, compatibility, and escalation boundaries.

4. Implement with `$dev-implementer` and relevant platform guidance.
   - Keep one suitable implementation owner for code, local validation, and
     bounded fixes. TDD, when selected or requested, is its conditional
     reference; preserve meaningful red/green/adapt/decline evidence without
     another worker or planner-only document requirement.
   - Inspect current code/tests and keep changes within the approved brief.
     Add practical required tests/artifacts, preserve domain/refactor rules,
     and commit only scoped changes before PR creation.
   - Return unresolved scope or technical decisions to the controller, not a
     speculative patch. Reuse sufficient current context rather than repeating
     discovery, architecture, and planning after each local failure.

5. Run post-implementation `$dev-api-steward` when API behavior changed or may have changed.
   - Owner: conditional. Apply execution-ownership for implementation-vs-contract review; use a serial worker or controller-coordinated edit path for docs, generated clients, changelog, examples, or migration-guide changes.
   - Compare the implementation diff to the intended contract.
   - Update OpenAPI/Swagger, API docs, examples, changelog, versioning notes, and migration guidance when needed.
   - If implementation and contract disagree, route back to `$dev-implementer` before PR creation.
   - If client-impact work spans multiple issues, PRs, or repos, route planning
     and issue execution to `$dev-project-orchestrator`; use
     `$dev-integration-manager` for the explicit PR/branch integration
     checkpoint it produces.

6. Apply `$dev-test` with the selected mode and project QA bar.
   - Owner: formal test responsibility on the active branch/worktree; the same suitable implementation worker may execute it. Assess existing evidence under `$dev-test` before rerunning; preserve the complete selected validation bar.
   - In fast mode, run focused primary-path unit tests and structurally required checks only; return skipped tests, acceptance criteria, edge cases, and production evidence under `Skipped / Unverified`.
   - In standard mode, validate the primary flow and ticket-specific regression; do not add reverse-red/mutation or unrelated edge-case coverage by default. Strict extends coverage under the mode contract.
   - Add the receipt's required hands-on and material acceptance/edge-case checks after automated checks; report unavailable required evidence as blocked or unverified.
   - Apply the mode contract's unattended waiver before selecting a production-loop verifier; simulator/seed/fixture checks still run, while real-environment evidence is deferred without blocking engineering. Fast mode records optional production verification as skipped unless it is an enforced pre-merge or unskippable safety/primary-path gate.
   - Fix valid QA findings before PR creation. After three failed repair attempts for the same blocker, stop or mark that QA surface blocked with evidence.

7. Run `$dev-verifier` only when independent freshness is needed, implementer evidence is insufficient, risk is high, or the head changed.
   - Owner: completion-evidence verification under execution-ownership; preserve any explicit independent verifier requirement.
   - Freeze the exact base/head target and map every acceptance criterion,
     required test or runtime claim, scope boundary, and remaining uncertainty
     to current evidence.
   - Require an explicit `pass`, `fail`, `blocked`, or `not-applicable` outcome
     for each claim and for the overall result. Implementation intent is never
     completion evidence.
   - When selected, proceed only from a current overall pass. Route failures or
     evidence gaps to their owning Dev skill, then rerun verification against
     the changed target before PR creation. When not selected, preserve the
     receipt's validation floor and continue from the current validated gate.

Required outcomes and authority remain shared; select validation depth from the
mode contract rather than treating standard and strict coverage as identical.
