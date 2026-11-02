# Hands-On QA

Read only when hands-on checks are selected. Run applicable automated checks first, then exercise the named surface at the required fidelity. Preserve explicit user requirements and the fast-mode unskippable boundary; strict mode alone does not select it.

1. Build a QA checklist from the issue, dev plan, acceptance criteria, bug repro, UX notes, screenshots, comments, and implementation notes.
   - Extract exact steps, expected copy, expected visual state, data prerequisites, permissions, loading/error/empty states, persistence, navigation, and edge cases.
   - Keep checks within the selected mode and named workflow; standard does not add adjacent edge-case coverage by default.
2. Build and launch the actual app or test surface. Do not treat compile-only success as hands-on QA unless the build or signing failure itself blocks QA.
3. Exercise the selected workflow and only the additional paths selected under the mode contract. Inspect the live UI before declaring hands-on success.
4. Record evidence: screenshots, UI snapshots, logs, terminal output, app state, branch/commit, scheme/target, device or macOS version, account/data/permissions, and repro rate when retested.
5. Decide `Pass`, `Fail`, or `Blocked` and report it in the Test Result's Hands-On QA
   line; list each mismatch under Failures / Blockers.

## iOS

- Prefer Build iOS Apps / XcodeBuildMCP simulator tools. If using XcodeBuildMCP, call `session_show_defaults` before the first build, run, or test call. If project/workspace, scheme, and simulator defaults are set, call `build_run_sim` directly.
- If MCP tools are unavailable, use the repo's documented command or discover schemes with `xcodebuild -list`, choose an available iOS Simulator destination, build with `xcodebuild`, then install and launch with `xcrun simctl`.
- Drive the Simulator through the issue steps, navigation in/out, app restart or re-open flows, retry behavior, and relevant permissions or data states.

## macOS

- Prefer the repo's documented command. Otherwise discover projects, workspaces, packages, schemes, and targets with `rg --files`, `xcodebuild -list`, or `swift package describe`.
- Use Build macOS Apps / XcodeBuildMCP tooling when available for build, run, launch, logs, and debugging. Use Computer Use, AppleScript, Accessibility scripting, screenshots, logs, and shell commands when direct app tooling is not enough.
- Launch the built `.app`, `swift run` executable, or repo-provided run command directly on this Mac. Prefer the actual built product over an installed production copy.
- Track macOS-specific risks: focus, menu and toolbar state, keyboard shortcuts, window restoration, modal/sheet placement, sandbox/entitlement issues, TCC permissions, and stale state after relaunch.

## Browser

- Use the repo's documented dev server, preview server, or E2E test harness when available.
- Prefer automated browser tests when they cover the workflow. Use manual browser validation when the issue requires inspecting interactive UI or visual state that tests do not cover.
- Record the URL, browser, viewport, account/data state, and screenshots or traces when available.
