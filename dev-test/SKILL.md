---
name: dev-test
description: >-
  Verify an implementation after coding. Use after a selected Dev implementer finishes to run or add focused tests, acceptance checks, edge-case validation, build, lint, typecheck, migration checks, smoke tests, and standard-mode hands-on app QA for iOS Simulator, macOS local apps, or browser workflows before self-review and PR creation.
---

# Dev: Test

Prove the implementation works technically. This is not PR Product Review; it validates code behavior and engineering quality against the plan.

`$dev-test` owns both automated validation and hands-on QA when the selected `$dev` mode requires it. Fast mode is automated by default. Standard mode starts with the same automated checks, then adds hands-on validation for user-visible app or browser behavior.

## Workflow

1. Read the dev plan, implementation result, acceptance criteria, known validation commands, and any `$dev-debugger` reproduction or validation plan.
2. Confirm the QA mode and touched surface: fast or standard; iOS, macOS, shared Apple code, web, backend, full-stack, CLI/library, docs/config, or mixed.
3. Run the smallest reliable checks first, then broaden when shared behavior or high-risk surfaces changed.
4. Add or update tests when a practical test surface exists and behavior changed.
5. In standard mode, run hands-on QA when the changed behavior is user-visible and has a runnable surface.
6. Record exact commands, environments, app state, evidence, and results.
7. If a check fails, diagnose whether it is caused by the change, pre-existing, flaky, environment-blocked, or out of scope.
8. Route valid implementation failures back to `$dev-implementer` with the selected platform reference(s); route repeated CI/environment failures to `$dev-ci-repair` when appropriate.

## Fast Mode

Run automated, project-appropriate validation:

- Apple app changes: in-scope iOS/macOS build plus relevant unit tests. Use Build iOS Apps / XcodeBuildMCP before choosing iOS `xcodebuild` commands; use relevant Build macOS Apps guidance for macOS build/test diagnostics when available.
- Backend/API/service changes: backend build, lint/typecheck, unit/integration tests, migration/schema checks, service/API smoke checks when available, and `$dev-api-steward` closeout when API behavior changed.
- Website frontend changes: production build, lint/typecheck, unit/component tests, and non-interactive route or E2E smoke checks when available.
- Full-stack changes: relevant backend and frontend automated checks plus a contract or end-to-end smoke path when practical.
- Library/CLI/package/docs/config work: package tests, representative command/API smoke tests, formatting, link, schema, or config validation.

## Standard Hands-On QA

Use this section only in standard mode, when the user explicitly asks for hands-on QA, or when the implementation cannot be responsibly validated without launching the app or driving a live workflow.

1. Build a QA checklist from the issue, dev plan, acceptance criteria, bug repro, UX notes, screenshots, comments, and implementation notes.
   - Extract exact steps, expected copy, expected visual state, data prerequisites, permissions, loading/error/empty states, persistence, navigation, and edge cases.
   - Add adjacent workflow checks implied by the issue, and mark inferred expectations explicitly.
2. Build and launch the actual app or test surface. Do not treat compile-only success as hands-on QA unless the build or signing failure itself blocks QA.
3. Exercise the required workflow first, then nearby user paths. Inspect the live UI before declaring success.
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
- `<command>`: <pass | fail | blocked> - <short evidence>

### Hands-On QA
- <not required | pass | fail | blocked> - <surface, environment, evidence>

### Coverage Notes
- <Acceptance criteria, bug repro, regression check, edge cases, or risk covered>

### Failures / Blockers
- <Failure, likely cause, and owner>

### Recommended Next Step
<`$dev-self-review` if checks pass; otherwise `$dev-implementer`, `$dev-ci-repair`, or stop.>
```
