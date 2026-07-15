---
name: design-prototype
description: >-
  Build and verify a disposable interactive prototype from an approved flow and screen specification. Use when Codex needs a clickable mockup, interaction demo, usability-test artifact, or adjustable design concept with real navigation, state, validation, loading, success, error, keyboard, and responsive behavior. Do not use for production implementation.
---

# Design: Prototype

Turn approved behavior and visual decisions into an interactive artifact that can test a flow before production engineering.

## Boundary

- Require an approved flow and screen specification. Route missing behavior or acceptance decisions to `$pm-ux-state` or `$pm-ui-design`.
- Treat the prototype as disposable design evidence, not production architecture.
- Keep prototype files isolated from the production app unless the user explicitly authorizes using an existing prototype target.
- Route selected behavior and visuals to Dev for production implementation.

## Inputs

- Product promise and target audience.
- Screen sequence, entry, completion, back/cancel, retry, and recovery behavior.
- Selected design direction or existing design system.
- Fidelity, platform frame, target viewport, sample data, and testing question.

## Workflow

1. Choose the lowest-cost medium that can test the question.
   - Use a self-contained HTML/CSS/JavaScript artifact when no scaffold exists and browser interaction is sufficient.
   - Use the supplied prototype stack when one exists.
   - Use a platform-specific prototype tool only when native behavior is the question.
2. Write the screen and state model before building. Include happy path, validation, loading, failure, recovery, and meaningful sub-state.
3. Build screen by screen with realistic content and one clear primary action per step.
4. Wire every visible interaction. Avoid dead buttons, screenshot-only navigation, or state changes that provide no feedback.
5. Model async actions with explicit loading, success, and recoverable error states. Prevent duplicate submission.
6. Preserve relevant state across navigation and reload when persistence affects the test.
7. Add optional tweak controls only when the user wants to compare a small set of visual or content variables. Keep them out of the normal presentation state.
8. Verify the full flow, alternate paths, keyboard operation, focus visibility, responsive layout, reduced motion, and reload behavior.
9. Run `$design-review` before stakeholder delivery when the prototype is intended to represent a finished direction.

## Verification Evidence

- Record the tested viewport or device frames.
- Exercise every primary action and at least one failure/recovery path.
- Confirm Tab, Enter/Space, Escape, and focus order where applicable.
- Confirm no visible overflow, clipped text, or unreachable controls at target sizes.
- Distinguish simulated behavior from real integrations.
- State any behavior that could not be verified.

## Output

```markdown
## Prototype Handoff
- Artifact:
- Testing question:
- Platform and viewports:
- Screens and states covered:
- Interactions verified:
- Simulated integrations:
- Persistence behavior:
- Accessibility checks:
- Known limitations:
- Decisions needed:
- Next route: user test / `$design-review` / Dev
```
