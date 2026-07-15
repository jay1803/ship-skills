# Design Review Checklist

Use only the passes relevant to the requested medium and review mode. Complete every relevant pass before aggregating findings so early fixes do not hide later issues.

## 1. Context and Conformance

- Identify the primary user, task, medium, viewport or device, and delivery context.
- Read the approved product brief, UI specification, design direction, token source, and component guidance.
- Distinguish intentional exceptions from accidental drift.
- Check that visible content is real, sourced, or honestly marked as placeholder content.
- Flag additions that expand product scope or invent claims without approval.

## 2. Accessibility and Inclusive Use

### Visual access

- Measure text and component contrast when colors can be resolved; use the applicable WCAG level and platform requirement.
- Check that state, category, and error meaning are not conveyed by color alone.
- Verify scalable text, zoom behavior, truncation, localization expansion, and readable line length where relevant.
- Check touch or pointer target size against the target platform's convention.

### Structure and semantics

- Verify meaningful heading and landmark structure in web content.
- Use native controls and semantic elements before custom roles.
- Require labels for controls and useful alternatives for meaningful imagery.
- Check accessible names, values, descriptions, error associations, and announcements for changing content.

### Input and motion

- Exercise keyboard or non-pointer access, logical focus order, visible focus, and expected Escape/Enter/Space behavior.
- Check that gestures have discoverable alternatives when required.
- Respect reduced-motion settings and avoid flashing or motion that obscures task completion.
- Verify that validation is specific, recoverable, and associated with the affected field or action.

## 3. Hierarchy, Rhythm, and Responsive Composition

- Identify what should be seen first, second, and third on each screen. Flag ambiguous or reversed hierarchy.
- Check size, weight, color, position, whitespace, and density as a combined system rather than isolated values.
- Confirm one clear primary action per task state unless the product requirement says otherwise.
- Compare spacing, type, sizing, grid, and alignment values with the approved scales.
- Flag near-duplicate patterns that should be identical and repeated patterns that need an intentional break.
- Test representative small, medium, and large viewports or platform sizes.
- Check overflow, clipping, text wrapping, safe areas, pointer and keyboard affordances, and orientation changes when relevant.

## 4. Visual Specificity and Generic-Template Risk

- Ask whether the direction could be applied unchanged to an unrelated product. If so, identify the generic decisions.
- Verify that typography, palette, imagery, structure, and signature details come from the brief or system.
- Flag decorative gradients, emoji, arbitrary card patterns, stock-style illustration, or fashionable type choices when they lack a product reason.
- Do not treat those patterns as universal failures; keep them when the brand or task justifies them.
- Remove filler, repeated copy, fabricated metrics, decorative structure, and controls without a destination.
- Check palette discipline, toned surfaces, icon consistency, image treatment, and content voice.

## 5. Interaction States and Feedback

- Inventory every interactive element and meaningful system state.
- Verify default, hover or pointer-over, pressed, focus, selected, disabled, loading, success, and error states where applicable.
- Ensure state changes are visible and understandable without relying on animation alone.
- Check transition purpose, duration, easing or spring behavior, interruptibility, and reduced-motion fallback.
- Require feedback for submission, saving, deletion, network delay, failure, undo, and destructive confirmation when the flow includes them.
- Check that current location, selection, filters, sorting, and modal or menu state remain legible.
- Verify that async actions resist duplicate submission and recover after failure.

## 6. Design-System and Component Integrity

- Trace colors, typography, spacing, radii, elevation, and motion to canonical tokens or documented exceptions.
- Check component anatomy, composition, variants, sizes, content rules, and state coverage against the system.
- Flag raw values, near-duplicate components, missing semantic aliases, and undocumented variants.
- Verify mode parity across light/dark, platform, density, or brand themes where in scope.
- Confirm that fixes strengthen the shared system instead of adding one-off local patches.

## 7. Verification

- Render or preview the actual artifact when possible; source inspection alone cannot prove visual quality.
- If a preview cannot be opened with the available project or platform tooling, continue with a source-only review and state that limitation instead of waiting indefinitely or inventing a new environment.
- Exercise primary and recovery flows, not only the default static state.
- Record tested devices, viewports, themes, input modes, and accessibility settings.
- Capture measured evidence for contrast, overflow, hit targets, and off-scale values when practical.
- After fixes, rerun the checks that failed and inspect adjacent states for regressions.
- State unverified areas and missing sources explicitly.

## Current Web Guideline Source

When the user asks for the current Vercel Web Interface Guidelines or an up-to-date web-guideline audit, fetch and follow the primary source before reviewing:

`https://raw.githubusercontent.com/vercel-labs/web-interface-guidelines/main/command.md`
