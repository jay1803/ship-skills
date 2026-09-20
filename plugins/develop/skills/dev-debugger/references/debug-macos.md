# Debug macOS

Use for macOS app bugs, AppKit, macOS SwiftUI scenes/windows/menus, sandbox/TCC, signing, entitlements, packaging, crashes, hangs, performance, and runtime behavior.

## Workflow

1. Load `$build-macos-apps:build-run-debug` for selected build/run/debug/log collection, or narrower guidance when signing, entitlements, packaging, AppKit, telemetry, SwiftPM, or test triage is the causal question. Existing sufficient source/log evidence does not require unrelated tool setup.
2. Reuse current project/process evidence. Inspect target, helpers, extensions, sandbox, entitlements, or run scripts when the failure path or evidence collection depends on them.
3. Reproduce with the same macOS version, distribution channel, sandbox state, permissions, file path, account state, and build configuration when those matter.
4. Search from evidence anchors: crash frames, Console logs, assertion text, menu/window names, notification names, entitlement keys, TCC messages, and test names.
5. Prefer a local confirming tool before proposing a fix.

## Symptom Map

- Crash: symbolicated crash report, Exception Breakpoint, app frames, Console around crash time.
- Hang/freeze: sample/spindump, pause debugger, Hangs instrument, main-thread stack.
- Slow launch or UI jank: Time Profiler, signposts, Activity Monitor, Instruments.
- Memory leak/growth: Memory Graph, Allocations, Leaks.
- Sandbox/TCC failure: Console.app filtered to process and `tccd`, entitlement file, usage strings, sandbox profile.
- Signing/notarization/package defect: signing and entitlement inspection, packaging logs, `spctl`, Gatekeeper messages.
- Window/menu/scene bug: AppKit/SwiftUI scene lifecycle, focus/responder chain, notification flow.
- File access bug: sandbox bookmarks, security-scoped resource lifecycle, path normalization.
- Field-only bug: collect logs with `log collect`, compare release vs debug behavior.
- Regression: bisect or compare app version/build settings from last known good release.

## Evidence To Report

- macOS version, hardware, app distribution channel, sandbox/TCC state, and build configuration.
- Crash/log/sample evidence used and whether symbols are available.
- Candidate files and confidence level.
- Exact tool or command that should verify the hypothesis.
