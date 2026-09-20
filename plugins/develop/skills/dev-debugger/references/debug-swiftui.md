# Debug SwiftUI

Use for SwiftUI state, layout, navigation, sheet, animation, accessibility, preview, performance, identity, lifecycle, and rendering bugs across iOS and macOS.

## Workflow

1. Load available SwiftUI specialist guidance when the leading hypothesis involves framework state, identity, layout, navigation, accessibility, or performance semantics. A defect already isolated to ordinary local data transformation does not require a framework-wide review.
2. Pair with `debug-ios.md` or `debug-macos.md` when the bug depends on app runtime, OS version, windowing, simulator/device behavior, logs, or build/run/debug tools.
3. Trace the state owner, identity, lifecycle, presentation, async lifetime, or availability boundary implicated by the evidence. Preserve the root diagnosis sufficiency gate; narrower context is not permission to guess a cause.
4. Search for UI copy, view names, state properties, bindings, environment keys, model fields, route names, and preview/test names.
5. Prefer a targeted reproduction or minimal view path over broad visual redesign.

## Symptom Map

- View does not update: wrong source of truth, missing observation, stale derived state, identity reuse.
- View updates too often: broad observable object, identity churn, expensive work in `body`.
- Navigation/sheet bug: duplicate presentation owners, stale route binding, dismissal race.
- Layout bug: invalid geometry assumptions, missing constraints, platform-specific container behavior.
- List/reorder bug: unstable ids, duplicate ids, model mutation during update.
- Async state bug: `.task` lifetime, cancellation, actor isolation, stale captures.
- Animation bug: implicit animation scope, transaction mismatch, state mutation timing.
- Accessibility bug: missing labels, hidden actionable controls, focus order, dynamic type clipping.
- Preview-only bug: missing environment/dependency injection, preview data mismatch.

## Evidence To Report

- Platform and OS version, view path, state owner, reproduction trigger, and whether app-level debug reference was used.
- Useful probes: `Self._printChanges()`, targeted logging around state mutation, breakpoints/watchpoints, Instruments SwiftUI template, View Debugger, accessibility inspector.
- Candidate files and confidence level.
- Fix direction that preserves local architecture and component style.
