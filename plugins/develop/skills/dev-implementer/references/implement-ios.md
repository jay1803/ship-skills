# Implement iOS

Use for iOS app code, Xcode iOS targets, iOS simulator workflows, UIKit, iOS SwiftUI screens, App Intents, iOS runtime bugs, and iOS build/run/debug tasks.

## Workflow

1. Load `$build-ios-apps:ios-debugger-agent` when simulator build/run/debug is needed; select narrower `build-ios-apps:*` guidance for a needed App Intents, performance, UI-pattern, memory, or trace workflow. An iOS file alone does not select those workflows.
2. Reuse current target and validation context. Resolve project/workspace, scheme, device, bundle id, configuration, and signing details when the changed behavior or selected build/run operation depends on them; investigate missing or stale inputs before that operation.
3. Inspect target files before editing. Follow existing module, state, dependency, concurrency, and testing patterns.
4. Make the smallest coherent iOS code change needed by the plan. Do not broaden product behavior, redesign unrelated UI, or touch unrelated build settings.
5. Add or update focused tests when the repo has a practical test surface.
6. Use XcodeBuildMCP or repo commands for build/run/debug validation when needed, and record exact evidence.
7. Stop if the change requires a product decision, platform support change, entitlement/signing decision, or architecture change not covered by the plan.

## Notes To Report

- Scheme, simulator/device, bundle id, signing, entitlement, deployment target, or build setting constraints.
- Tests added or skipped, with rationale.
- Validation command/tool and exact result or blocker.
