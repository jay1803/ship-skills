---
name: dev-test
description: "Run post-implementation validation under the selected Dev mode and classify failures before PR preparation."
metadata:
  owner: jay1803
  family: develop
  maturity: stable
  distribution: develop
---

# Dev: Test

Prove the implementation works technically. This is not PR Product Review; it validates code behavior and engineering quality against the plan.

`$dev-test` owns mode-appropriate validation. Read [`../dev/references/development-mode-contract.md`](../dev/references/development-mode-contract.md) before selecting checks. Standard uses focused primary-flow and ticket-specific regression coverage; strict adds risk-selected failure/recovery checks. Fast retains its reduced lifecycle. Apply the contract before adding tests or extra checks.

## Boundary

- Own the initial post-implementation validation before PR creation, including build, test, lint, typecheck, schema/migration, smoke, acceptance, and mode-appropriate hands-on QA.
- When Dev State marks a production loop required or active, own execution of the contract's verifier and the evidence record for each run. `$dev` remains the loop controller and `$dev-implementer` owns code changes.
- Keep ownership of the first failure discovered during this phase long enough to classify it and preserve evidence.
- Route change-caused implementation failures to `$dev-implementer`; do not turn initial validation into CI repair merely because a local command is red.
- Route to `$dev-debugger` only when the failure represents wrong behavior, a regression, or a failed acceptance check whose root cause is still unknown after initial classification. Include the failing command, reproduction, expected/actual behavior, and relevant evidence.
- Route to `$dev-ci-repair` when a PR check is red or when repeated CI/environment behavior cannot be resolved within this validation phase and the handoff includes the exact failing command and evidence.
- Do not own PR review comments, merge conflicts, or product-requirement conformance; route those to `$dev-implementer` or `$pm-pr-product-review`.
- Do not treat standalone `verify/*` as post-implementation test work. A
  verify-only request is owned by `$dev-verifier`, freezes its exact target, and
  stops with evidence; a failed verification does not authorize this skill to
  repair or rerun a deploy.

## Evidence Reuse And Execution

Formal testing is a responsibility, not a requirement for a different agent.
The current implementation worker may perform it when the controller's scope,
tools, permissions, and independence requirements allow. The controller still
accepts the Test Result and keeps required verification and Review separate.

Before running a check, assess existing evidence against the selected validation
floor. Reuse an actual, inspectable result only when all relevant inputs match:

- exact command, check configuration, assertions/fixtures, and observed result;
- implementation/test/config/generated inputs and relevant dependency versions;
- revision or immutable worktree-input identity, scope, and acceptance coverage;
- environment, role/account, runtime state, and required fidelity/freshness.

Record the source and matching basis, not just an earlier agent's claim or the
same Git SHA. A matching revision alone does not establish current live state.
Rerun affected checks when inputs or environment change, results are missing or
unverifiable, or the user/repository/acceptance contract requires new execution.
Do not rerun an unchanged sufficient check solely because the phase owner
changed. If required evidence cannot be gathered, retain valid partial results
and report the missing boundary; partial coverage is never an overall pass.

Reuse does not waive a required external verifier, authorize a remote action or
deployment, weaken mode-specific coverage, or let the implementer approve an
independent Review. Preserve its source, input, environment, and authorization.

For mixed framework results, baseline failures or authorized exceptions, read
[validation evidence](references/validation-evidence.md). Keep command truth,
attribution and gate effect together in the existing Test Result for downstream
reuse; a green final summary does not replace the command's failed exit.

## Workflow

1. Read the current implementation brief or selected Dev plan, implementation result, acceptance criteria, known validation commands, and Resume Receipt when supplied. Consume diagnosis/planning artifacts only when their stages were selected; do not require documents for intentionally unselected stages. Read the production-loop contract when present. For a required loop, read [`../dev/references/production-loop-contract.md`](../dev/references/production-loop-contract.md).
2. Confirm the QA mode and touched surface: fast, standard, or strict; iOS, macOS, shared Apple code, web, backend, full-stack, CLI/library, docs/config, or mixed. Omitted mode means standard.
3. Assess reusable evidence, then run the smallest missing, invalidated, or explicitly fresh checks first. Cover the complete selected mode and changed risk surface.
4. Reuse or add tests for the selected mode coverage. Standard does not expand into unrelated edge cases or reverse-red/mutation testing by default; bug tickets retain focused regression coverage.
5. Apply the mode contract's unattended validation waiver before selecting hands-on QA. Select remaining simulator/local QA when requested or needed to prove a concrete changed-path risk that automated evidence cannot cover. Name the surface and expected result; user-visible change alone does not require a full manual QA pass.
6. Record exact commands, environments, app state, evidence, and results, distinguishing checks executed in this phase from verified reused evidence.
7. For a production loop, first apply the unattended validation waiver. Run remaining required simulator/seed/fixture verifiers at their stated fidelity and preserve the measured observation and verifier independence before repair. Waived real-environment evidence is `Skipped / Unverified`, not a failed engineering gate. In fast mode, skip optional production evidence and return it under `Skipped / Unverified` unless it is an enforced pre-merge or unskippable gate.
8. If a check fails, diagnose whether it is caused by the change, pre-existing, flaky, environment-blocked, or out of scope.
9. Route obvious implementation failures back to `$dev-implementer` with the selected platform reference(s); route unexplained behavior/regression failures to `$dev-debugger`; route repeated CI/environment failures to `$dev-ci-repair` only with an explicit evidence-bearing handoff.

After passing checks, return evidence to the controller and name the next
selected gate. Use `$dev-verifier` when selected; otherwise continue toward
`$dev-pr-writer` with current receipt-backed evidence. If a new material risk
or evidence gap triggers verification, return that trigger to the controller
for a phase-plan update before dispatch. A passing test does not waive a
selected or newly required verifier.

## Fast Mode

Run only focused unit tests for the primary path plus the minimum build, typecheck, lint, schema, or enforced CI checks needed for the code and PR to progress. Do not automatically run broad integration/E2E/smoke suites, hands-on QA, exhaustive acceptance checks, or listed edge cases.

- Return every skipped command, acceptance criterion, edge case, hands-on surface, and production verifier under `Skipped / Unverified`; do not create a dedicated risk ticket merely to record it.
- Mark omissions `skipped (fast mode)`, never passed or not required.
- Stop only for an unskippable condition in the development-mode contract, including a failing primary-path test, a structurally required build/check, or a known critical correctness/security/data-loss issue.

## Standard And Strict Modes

Select the smallest sufficient checks under the mode contract and evidence
reuse rules; the platform is a way to find checks, not a mandatory bundle:

- Standard: primary flow, ticket-specific regression, necessary build/typecheck,
  and enforced repository/CI checks. Use an existing component, integration or
  E2E test when it is the simplest adequate proof; do not run every layer merely
  because commands exist. No automatic reverse-red/mutation or unrelated edge
  coverage. Preserve existing tests and classify observed failures honestly.
- Strict: extend to relevant failure, recovery, concurrency and integration
  boundaries. Select targeted reverse-red checks only where they add evidence;
  do not require a mutant for every assertion.
- Choose the relevant Apple build/test target, backend API/schema check, web
  component/route test, or CLI/package/config check from the touched surface.
  API changes still retain the selected `$dev-api-steward` closeout.

Use simulator/local runtime, seed accounts and suitable mock E2E for the changed
behavior. Carry waived real-environment or human checks under `Skipped /
Unverified`; only remaining mode-required production-loop/QA evidence gates
engineering. Missing real-account credentials is not a reason to hold PR creation.

## Production Loop Evidence

Use only when the production-loop contract is required:

```markdown
Production Loop: <iteration N | passed | blocked>
Environment Fidelity: <fixture | representative | production-scale | live>
Verifier Independence: <agent-authored | repository-controlled | external/immutable>
Command / Surface: <exact command, harness, service, or metric>
Observation: <measured result or failure symptom>
Threshold Result: <pass | fail | blocked>
Evidence: <logs, report, artifact, URL, trace, or other durable evidence>
```

Do not report an agent-authored test, repository-controlled CI, external verifier, and production-scale run as interchangeable evidence. Do not modify or weaken an external verifier to make the implementation pass. On failure, return the observation to `$dev`; do not independently change the contract or choose a broader product scope.

## Required Hands-On QA

Use this section only for selected hands-on checks. Run applicable automated checks first, then exercise the named surface at the required fidelity. Preserve explicit user requirements and the fast-mode unskippable boundary; strict mode alone does not select this section.

1. Build a QA checklist from the issue, dev plan, acceptance criteria, bug repro, UX notes, screenshots, comments, and implementation notes.
   - Extract exact steps, expected copy, expected visual state, data prerequisites, permissions, loading/error/empty states, persistence, navigation, and edge cases.
   - Keep checks within the selected mode and named workflow; standard does not add adjacent edge-case coverage by default.
2. Build and launch the actual app or test surface. Do not treat compile-only success as hands-on QA unless the build or signing failure itself blocks QA.
3. Exercise the selected workflow and only the additional paths selected under the mode contract. Inspect the live UI before declaring hands-on success.
4. Record evidence: screenshots, UI snapshots, logs, terminal output, app state, branch/commit, scheme/target, device or macOS version, account/data/permissions, and repro rate when retested.
5. Decide `Pass`, `Fail`, or `Blocked`.

### iOS

- Prefer Build iOS Apps / XcodeBuildMCP simulator tools. If using XcodeBuildMCP, call `session_show_defaults` before the first build, run, or test call. If project/workspace, scheme, and simulator defaults are set, call `build_run_sim` directly.
- If MCP tools are unavailable, use the repo's documented command or discover schemes with `xcodebuild -list`, choose an available iOS Simulator destination, build with `xcodebuild`, then install and launch with `xcrun simctl`.
- Drive the Simulator through the issue steps, navigation in/out, app restart or re-open flows, retry behavior, and relevant permissions or data states.

### macOS

- Prefer the repo's documented command. Otherwise discover projects, workspaces, packages, schemes, and targets with `rg --files`, `xcodebuild -list`, or `swift package describe`.
- Use Build macOS Apps / XcodeBuildMCP tooling when available for build, run, launch, logs, and debugging. Use Computer Use, AppleScript, Accessibility scripting, screenshots, logs, and shell commands when direct app tooling is not enough.
- Launch the built `.app`, `swift run` executable, or repo-provided run command directly on this Mac. Prefer the actual built product over an installed production copy.
- Track macOS-specific risks: focus, menu and toolbar state, keyboard shortcuts, window restoration, modal/sheet placement, sandbox/entitlement issues, TCC permissions, and stale state after relaunch.

### Browser

- Use the repo's documented dev server, preview server, or E2E test harness when available.
- Prefer automated browser tests when they cover the workflow. Use manual browser validation when the issue requires inspecting interactive UI or visual state that tests do not cover.
- Record the URL, browser, viewport, account/data state, and screenshots or traces when available.

## Reporting

Summarize selected coverage and material limitations; do not generate per-assertion
matrices or an exhaustive list of hypothetical edge cases.

For each command include its actual exit/completion state and all framework
summaries, with the source and target binding. Carry any baseline comparison,
exact exception and allowed next stages under the same result using the
validation-evidence reference; keep failed and filtered runs distinct.

When anything fails or blocks QA, list each mismatch separately:

- Step or workflow area
- Expected behavior
- Actual behavior
- Evidence
- Environment
- Repro rate when tested more than once

Leave a Linear issue comment only when the active workflow has a Linear-write tool and Dev State allows it. Otherwise provide exact comment text in chat and state that it was not posted.

For failures or blockers, use:

```markdown
QA result: <Failed | Blocked>

Environment
- Branch/commit:
- App/scheme/target:
- Device/OS/browser:
- Build configuration:

Findings
1. <Step or area>
   Expected: <expected behavior>
   Actual: <actual behavior>
   Evidence: <screenshot/log/UI snapshot/command output>

Notes
- <Setup, permissions, repro rate, blockers, or scope notes>
```

For passes, keep the response concise:

```markdown
QA passed

Verified <issue id or workflow> using <checks/app/scheme/target/device>. No mismatches found.
```

## Output

```markdown
## Test Result

### Commands
- `<command>`: <pass | fail | blocked> - <exit/completion; all framework summaries> - <executed here | reused: source and matching inputs/environment>

### Hands-On QA
- <not required | pass | fail | blocked> - <surface, environment, evidence>

### Coverage Notes
- <Acceptance criteria, bug repro, regression check, edge cases, or risk covered>

### Skipped / Unverified
- <skipped test/gate/edge case plus risk and recommended human follow-up, or none>

### Production Loop
- <not required | iteration/result plus environment fidelity, verifier independence, threshold, and evidence>

### Failures / Blockers
- <Actual failure, attribution/base evidence, owner; exact exception and permitted stages if applicable>

### Recommended Next Step
<After pass: controller-owned next selected gate (`$dev-verifier` when selected, otherwise `$dev-pr-writer` with current receipt-backed evidence); return new verification triggers to the controller. After failure: `$dev-implementer`, `$dev-debugger`, `$dev-ci-repair`, or stop.>
```
