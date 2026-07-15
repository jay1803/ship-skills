# Implement SwiftUI

Use for SwiftUI view code, state management, layout, navigation, sheets, animations, accessibility, previews, performance, Liquid Glass, and Instruments trace-driven SwiftUI work for iOS or macOS.

## Workflow

1. Load `$swiftui-expert-skill` before editing SwiftUI code. Follow its topic router and correctness checklist for the relevant area.
2. If app-level build/run/debug is required, also load `implement-ios.md` or `implement-macos.md` according to the target platform.
3. Identify owned versus injected state, view boundaries, navigation/sheet ownership, accessibility requirements, preview expectations, and platform/version availability gates.
4. Inspect target files before editing. Preserve local architecture and component style instead of imposing a new pattern.
5. Make the smallest coherent SwiftUI change needed by the plan. Avoid unrelated visual redesigns, architecture rewrites, and broad state migration.
6. Add or update previews/tests when the repo has a practical surface and the plan calls for it.
7. Stop if the change requires product scope, visual design, platform availability, or data-flow decisions not covered by the plan.

## Notes To Report

- State, layout, navigation, accessibility, performance, preview, and version-gate constraints.
- Whether app-level iOS/macOS reference guidance was also used.
- Tests/previews added or skipped, with rationale.
