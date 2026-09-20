# Implement macOS

Use for macOS app code, AppKit, macOS SwiftUI scenes/windows/menus, macOS build/run/debug tasks, packaging, signing, entitlements, SwiftPM GUI apps, and macOS runtime behavior.

## Workflow

1. Load `$build-macos-apps:build-run-debug` when build/run/debug is selected, or narrower `build-macos-apps:*` guidance for the actual platform question. Reuse settled local patterns for a bounded edit that needs neither workflow.
2. Resolve only missing target, package, process, signing/entitlement, or run-script facts needed by the changed behavior or selected operation. Do not repeat a project inventory when the current brief supplies those facts.
3. Inspect target files before editing. Follow existing scene, window, menu, AppKit interop, state, service, and test patterns.
4. Make the smallest coherent macOS code change needed by the plan. Do not force iOS simulator assumptions onto macOS work.
5. Add or update focused tests when the repo has a practical test surface.
6. Validate with the repo's preferred macOS command path, such as `./script/build_and_run.sh`, `xcodebuild`, or `swift build`, and record exact evidence.
7. Stop if the change requires a product decision, entitlement/signing decision, distribution change, or architecture change not covered by the plan.

## Notes To Report

- Project type, run script, signing, entitlement, window/menu, packaging, or deployment constraints.
- Tests added or skipped, with rationale.
- Validation command/tool and exact result or blocker.
