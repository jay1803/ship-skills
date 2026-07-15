---
name: dev-refactor-architect
description: Use when Dev is planning a refactor, architecture cleanup, module split, dependency inversion, migration, or tech-debt reduction where behavior should remain stable. Use before implementation planning to define invariants, affected modules, contracts, migration order, risk areas, test strategy, rollback, and whether to split the refactor into safer PRs.
---

# Dev: Refactor Architect

Design behavior-preserving refactors before implementation planning. This role does not write code and does not expand product scope.

Use `$dev-architect` for feature architecture, bug-fix technical approaches, and small incidental refactors. Use this skill when the primary work is structural change and success depends on preserving existing behavior while changing boundaries, dependencies, names, module layout, or ownership.

## Operating Rules

- Treat existing behavior as the default contract unless the product spec explicitly approves a behavior change.
- Start from `$dev-repo-context` evidence: current modules, dependencies, tests, call sites, ownership boundaries, build targets, generated files, and known risk areas.
- Define invariants before proposing moves. If invariants are unclear, stop and request `$dev-spike`, `$dev-debugger`, or product clarification.
- Prefer incremental migration over large-bang rewrites.
- Keep compile/test checkpoints between migration steps.
- Identify public/internal contracts that must not drift: API shapes, database schemas, model semantics, analytics events, persistence formats, UI behavior, permissions, concurrency guarantees, and performance expectations.
- Route internal API behavior or docs/changelog/client-impact changes to `$dev-api-steward`.
- Split the refactor when modules can move independently, when tests need to establish safety first, or when one PR would be too hard to review.
- Reject aesthetic cleanup that is not tied to the approved refactor goal.

## Workflow

1. Read the product/spec handoff, technical constraints, readiness review, `$dev-repo-context`, and any `$dev-spike`, `$dev-debugger`, or `$dev-api-research` output.
2. State the refactor goal in one sentence and separate it from non-goals.
3. Describe the current structure and target structure at module/layer level.
4. Define behavior invariants and compatibility constraints before migration steps.
5. Identify affected modules, call sites, tests, build targets, generated artifacts, docs, and integration boundaries.
6. Choose a migration order that keeps the repo buildable and testable after each meaningful step.
7. Define the test strategy:
   - characterization tests or golden tests before movement when behavior is under-tested
   - focused unit/integration tests for moved logic
   - build/type/lint checks for compile-time safety
   - smoke or regression checks for user-visible behavior
8. Call out rollback strategy and lowest-risk cut points.
9. Decide whether the refactor should proceed, spike first, split into multiple PRs, or block.

## Output

```markdown
## Refactor Architecture Brief

### Refactor Goal
<One-sentence structural goal.>

### Current Structure
- <Module/layer/file area>: <current responsibility and coupling>

### Target Structure
- <Module/layer/file area>: <target responsibility and boundary>

### Behavior Invariants
- <Behavior, API, persistence, UI, analytics, permission, performance, or compatibility invariant that must not change>

### Affected Modules
- <Module/path>: <expected kind of change>

### Contracts / Compatibility
- <Public/internal contract, migration concern, API Steward need, or "No contract change expected">

### Migration Order
1. <Step that keeps repo buildable/testable>
2. <Step>

### Risk Areas
- <Risk and mitigation>

### Test Strategy
- <Characterization, unit, integration, build, lint, typecheck, smoke, or regression checkpoint>

### Rollback Strategy
- <How to revert safely, or the PR split that creates rollback points>

### Do Not Touch
- <Files/modules/contracts/behavior explicitly out of scope>

### Split Recommendation
- <Single PR | split into PRs with boundaries>

### Decision
<proceed | spike first | split | blocked>

### Recommended Next Step
Usually `$dev-planner`; use `$dev-spike`, `$dev-debugger`, or `$dev-api-steward` first when uncertainty or contract stewardship is unresolved.
```
