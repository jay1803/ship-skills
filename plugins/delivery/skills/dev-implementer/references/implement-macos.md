# Implement macOS

Use for macOS app code, AppKit, macOS SwiftUI scenes/windows/menus, macOS build/run/debug tasks, packaging, signing, entitlements, SwiftPM GUI apps, and macOS runtime behavior.

## Workflow

1. Load the relevant `build-macos-apps:*` skill for the actual surface. Use `$build-macos-apps:build-run-debug` for build/run/debug work unless a narrower macOS skill applies.
2. Discover project shape before editing: `.xcworkspace`, `.xcodeproj`, `Package.swift`, app target, runnable process, signing/entitlement constraints, and project-local run scripts.
3. Inspect target files before editing. Follow existing scene, window, menu, AppKit interop, state, service, and test patterns.
4. Make the smallest coherent macOS code change needed by the plan. Do not force iOS simulator assumptions onto macOS work.
5. Add or update focused tests when the repo has a practical test surface.
6. Validate with the repo's preferred macOS command path, such as `./script/build_and_run.sh`, `xcodebuild`, or `swift build`, and record exact evidence.
7. Stop if the change requires a product decision, entitlement/signing decision, distribution change, or architecture change not covered by the plan.

## Notes To Report

- Project type, run script, signing, entitlement, window/menu, packaging, or deployment constraints.
- Tests added or skipped, with rationale.
- Validation command/tool and exact result or blocker.
