---
name: dev-architect
description: >-
  Convert a dev-ready product spec, repository context, and any bug diagnosis, spike, or API research brief into a technical approach. Use before implementation planning to decide affected layers, contracts, risks, data/API/UI/state impacts, migrations, permissions, analytics, compatibility boundaries, and whether internal API changes need $dev-api-steward contract review. For refactor-first architecture cleanup where behavior should remain stable, route to $dev-refactor-architect instead.
---

# Dev: Architect

Turn product requirements and repo context into a technical approach. Do not write code in this role.

Use `$dev-refactor-architect` instead when the primary work is refactor, architecture cleanup, module split, dependency inversion, migration sequencing, or tech-debt reduction where behavior should remain stable.

## Workflow

1. Read the product spec, technical product constraints, readiness review, codebase context brief, and any `$dev-debugger`, `$dev-spike`, or `$dev-api-research` output.
2. Identify affected layers: UI, navigation, state, API, database, migrations, permissions, analytics, background jobs, config, tests, CI, docs, or release process.
3. If the work is refactor-first and depends on behavior invariants, module migration order, rollback, or split-PR sequencing, route to `$dev-refactor-architect` instead of continuing here.
4. Choose the approach that fits existing architecture and minimizes blast radius.
5. If the approach may change internal backend/API behavior, call out the API surface and route to `$dev-api-steward` for pre-implementation contract review before final planning.
6. Call out tradeoffs, risks, compatibility concerns, rollback concerns, and where more debugging, spike, API research, or API stewardship is needed.
7. Reject speculative architecture when the repo already has a matching local pattern.

## Output

```markdown
## Technical Approach

### Summary
<Concise implementation strategy.>

### Affected Layers
- <Layer/module>: <planned change>

### Contracts / Interfaces
- <API, model, state, migration, permission, analytics, or config contract>

### API Stewardship
- <Use `$dev-api-steward` before planning if internal API behavior/docs/changelog/client impact may change; otherwise "Not needed" with evidence>

### Research Inputs
- <Bug diagnosis, spike, or API research decision used, or "None">

### Risks / Guardrails
- <Risk and guardrail>

### Not Doing
- <Tempting technical work intentionally excluded>

### Recommended Next Step
Usually `$dev-planner`; use `$dev-api-steward` first when internal API contract stewardship is required; use `$dev-refactor-architect` when the issue is primarily structural refactor; otherwise stop for missing technical discovery.
```
