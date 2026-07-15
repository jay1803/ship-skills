---
name: design-review
description: >-
  Review design artifacts, prototypes, design-system definitions, or implemented UI for visual quality and conformance. Use for accessibility, hierarchy and rhythm, generic AI-template aesthetics, interaction states and feedback, responsive behavior, token and component consistency, or a final polish gate. Report findings by default; modify files only when the user explicitly asks to fix or polish them.
---

# Design: Review

Produce an evidence-based design verdict against the approved brief, direction, system, platform conventions, and accessibility floor.

Read [references/review-checklist.md](references/review-checklist.md) completely before any multi-pass review or final gate. For a narrowly targeted review, read the relevant checklist section plus its Context and Verification sections.

## Boundary

- Review visual and interaction craft. Do not replace `$pm-pr-product-review`, `$dev-self-review`, tests, security review, or architecture review.
- Default to report-only for requests to inspect, audit, critique, or review.
- Apply changes only when the user asks to fix, polish, improve, or complete delivery and the target files are in scope.
- Route product-behavior disagreements to PM and production implementation work to Dev.

## Review Modes

- **Targeted:** one axis such as accessibility, hierarchy, states, motion, or design-system conformance.
- **Conformance:** compare an artifact or implementation with an approved direction, token source, component system, or platform convention.
- **Final gate:** run all relevant passes, aggregate findings, and return a delivery verdict.

## Workflow

1. Identify the target, medium, approved sources, intended audience, and requested review mode.
2. Inspect the artifact end to end. For code-backed UI, read the relevant source and render it at representative sizes when possible. If no usable preview path exists, continue with source inspection, record the limitation, and do not block on bootstrapping unrelated tooling.
3. Establish authority order: explicit user constraints, approved PM/UI artifacts, approved design direction/system, platform conventions, then general craft guidance.
4. Run the relevant checklist passes. Independent read-only passes may be delegated in parallel; keep aggregation and any fixes serial.
5. Deduplicate findings and rank them:
   - **Blocker:** prevents access, task completion, comprehension, or safe use.
   - **Major:** breaks hierarchy, system conformance, interaction feedback, responsiveness, or trust.
   - **Polish:** improves coherence or craft without blocking use.
6. Cite concrete evidence. Use file and line references for code, component or screen names for design artifacts, and measured values when available.
7. In report mode, stop after findings and recommendations.
8. In fix mode, apply approved fixes, render or exercise the changed surface, and rerun the failed checks.
9. Return a verdict and open decisions. Do not claim a pass for checks that could not be run.

## Specialist Bridges

- For current external Web Interface Guidelines, fetch the latest primary guideline source before reviewing rather than relying on a stale embedded copy.
- For motion-only code review, route to `review-animations`; for codebase-wide motion planning, use `improve-animations`; for Apple-like physical interaction principles, use `apple-design`.
- Use the platform's dedicated UI skill when a review depends on framework-specific implementation details.

## Output

```markdown
## Design Review
- Target:
- Mode:
- Sources of truth:
- Verification performed:
- Verdict: pass / pass with decisions / changes required / not verifiable

### Findings
| Severity | Area | Evidence | Impact | Recommendation |
| --- | --- | --- | --- | --- |

### Fix Verification
- <Only in fix mode.>

### Open Decisions
- <Judgment calls the user must approve.>
```
