---
name: dev-repo-context
description: >-
  Research the repository before coding. Use after PM readiness and before technical design to find relevant files, existing patterns, tests, APIs, migrations, constraints, prior implementations, and validation commands.
---

# Dev: Repo Context

Read the codebase before any architecture or implementation decision. Prevent invented architecture by grounding the work in existing files and patterns.

## Workflow

1. Read the dev-ready issue/spec, acceptance criteria, constraints, and known validation expectations.
2. Inspect repository structure, manifests, scripts, CI config, docs, tests, and likely modules.
3. Search with `rg` first. Prefer concrete file reads over assumptions.
4. Identify existing patterns, helpers, APIs, data models, feature flags, migrations, test surfaces, and project conventions.
5. Identify risks and unknowns that must be resolved before architecture or coding.

## Output

```markdown
## Codebase Context Brief

### Relevant Files
- <path>: <why it matters>

### Existing Patterns
- <pattern/helper/API/convention and where it appears>

### Tests / Validation Surface
- <test file, command, build, lint, typecheck, smoke path, or missing surface>

### Constraints
- <API, migration, compatibility, performance, privacy, platform, or tooling constraint>

### Unknowns
- <question that must be resolved before architecture/coding, or "None.">

### Recommended Next Step
Usually `$dev-architect`; otherwise stop with the missing evidence.
```
