# Debug iOS

Use for iOS app bugs, iOS simulator/device behavior, Xcode iOS targets, UIKit, App Intents, iOS SwiftUI runtime behavior, crashes, hangs, memory leaks, performance, and field-only defects.

## Workflow

1. Select specialist guidance for the needed evidence operation: `$build-ios-apps:ios-debugger-agent` for build/run/debug/log work, `ios-memgraph-leaks` for memory graphs, `ios-ettrace-performance` for traces, or narrower App Intents/SwiftUI guidance. Reading an already-sufficient symbolicated report does not itself require build/run setup.
2. Preserve the affected OS/app/configuration and reproduction boundary. Resolve project, scheme, device, bundle id, or signing details when they distinguish a hypothesis or are required to collect the selected evidence.
3. Search from evidence anchors: crash frames, exception text, assertion strings, UI copy, feature names, notification names, App Intent identifiers, logs, and test names.
4. Prefer the cheapest confirming tool before proposing a fix.
5. Distinguish simulator-only, device-only, debug-only, release-only, and OS-version-specific behavior.

## Symptom Map

- Crash `EXC_BAD_ACCESS` / `SIGSEGV`: Address Sanitizer, Zombies for ObjC, Memory Graph.
- `NSException` or assertion crash: Exception Breakpoint, search assertion text.
- Swift trap or fatal error: Swift Error Breakpoint, read trap message and app frames.
- Watchdog kill, freeze, or spinner: Hangs instrument, Time Profiler, pause debugger and inspect main thread.
- Intermittent crash: Thread Sanitizer, repeated repro, ordering assumptions.
- Memory growth or jetsam: Memory Graph, Allocations generations, Leaks.
- Wrong UI layout: Debug View Hierarchy, constraint logs, accessibility tree.
- Wrong state/data: breakpoints/watchpoints at mutation sites, logs around model mapping and cache invalidation.
- Slow scrolling or jank: Time Profiler, Core Animation, SwiftUI performance tools when relevant.
- Network issue: request/response capture, offline/bad-network repro, retry/backoff logs.
- Core Data issue: concurrency debug launch arg, SQL debug when query behavior matters.
- Field-only crash: symbolicate `.ips` with matching dSYM, inspect MetricKit/Crashlytics breadcrumbs.
- Regression: bisect from last known good version when repro is stable.

## Evidence To Report

- Device/simulator, OS, app version, build configuration, and repro reliability.
- Crash/log/test evidence used and whether symbols are available.
- Candidate files and confidence level.
- Exact tool or command that should verify the hypothesis.
