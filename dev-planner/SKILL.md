---
name: dev-planner
description: >-
  Create an ordered implementation plan from an approved technical approach or refactor architecture brief, any bug diagnosis, and any API Steward contract review. Use after architecture and before coding to define step sequence, selected $dev-implementer platform reference(s), API Steward checkpoints for API-changing work, dependencies, ownership boundaries, file areas, validation checkpoints, and stop conditions.
---

# Dev: Planner

Build the implementation plan that the coding agent will execute. Keep it ordered, narrow, and verifiable.

Use this skill for one coding issue or one already-selected implementation slice. For multiple issues, parent issues, project batches, or parallelization decisions across slices, route to `$dev-project-orchestrator`. For verified read-only mapper/graph/verifier analysis, use `$dev-project-orchestrator --deep-plan`; do not run that heavier mode from `$dev-planner`.

## Workflow

1. Read the technical approach or `$dev-refactor-architect` brief, repo context, product spec, acceptance criteria, any `$dev-debugger` bug diagnosis brief, and any `$dev-api-steward` pre-implementation contract review.
2. Break work into ordered implementation steps with dependencies and validation checkpoints.
3. Select `$dev-implementer` platform reference(s): `implement-ios.md`, `implement-macos.md`, `implement-swiftui.md`, `implement-web.md`, `implement-backend.md`, `implement-supabase.md`, or a sequence of them for cross-layer work.
4. For API-changing work, include a post-implementation `$dev-api-steward` checkpoint before `$dev-test` so docs, OpenAPI/Swagger, changelog, examples, versioning, and client-impact notes are updated before PR creation.
5. For refactor plans, preserve the behavior invariants, migration order, rollback points, split recommendation, and do-not-touch boundaries from the refactor architecture brief.
6. Identify files/modules expected to change and areas not to touch.
7. Mark steps that can be parallelized only when contracts are stable and file ownership does not overlap.
8. Define stop conditions for ambiguity, API contract mismatch, behavior invariant risk, failing validation, merge conflicts, or scope drift.

## Output

```markdown
## Dev Plan

### Sequence
1. <Step, expected files/modules, and why it comes now>
2. <Step>

### Implementation Owners
- `$dev-implementer` using <`implement-ios.md` | `implement-macos.md` | `implement-swiftui.md` | `implement-web.md` | `implement-backend.md` | `implement-supabase.md`>: <owned steps/files and why these reference(s) fit>

### Dependencies
- <Dependency and evidence/status>

### API Stewardship
- <Pre-implementation contract review used, post-implementation `$dev-api-steward` checkpoint needed, docs/changelog artifacts expected, or "Not needed">

### Refactor Invariants
- <Behavior invariants, migration order constraints, rollback points, split boundaries, or "Not a refactor-first plan">

### Verification Checkpoints
- <Command, test, build, lint, typecheck, smoke path, API docs/schema validation, manual check, original repro, or regression check>

### Do Not Touch
- <Out-of-scope files, modules, contracts, or behavior>

### Stop Conditions
- <Condition that should stop implementation and escalate>

### Recommended Next Step
Usually `$dev-implementer` with the selected reference(s).
```
