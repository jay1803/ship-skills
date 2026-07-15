# Debug macOS

Use for macOS app bugs, AppKit, macOS SwiftUI scenes/windows/menus, sandbox/TCC, signing, entitlements, packaging, crashes, hangs, performance, and runtime behavior.

## Workflow

1. Load the relevant `build-macos-apps:*` skill. Use `$build-macos-apps:build-run-debug` for build/run/debug/log work, and narrower skills for signing, entitlements, packaging, AppKit interop, telemetry, SwiftPM, or test triage.
2. Discover project shape: `.xcworkspace`, `.xcodeproj`, `Package.swift`, app target, runnable process, helper apps, extensions, sandbox, entitlements, and project run scripts.
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
