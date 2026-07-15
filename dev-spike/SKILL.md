---
name: dev-spike
description: >-
  Reduce technical uncertainty before architecture in the Dev workflow. Use before $dev-architect when the solution is unclear, feasibility is unknown, risky repo behavior must be tested, alternatives need comparison, or blockers must be identified before planning. Produces a spike report, feasibility decision, recommended direction, architecture implications, validation plan, risks, and open questions.
---

# Dev: Spike

Reduce uncertainty enough for `$dev-architect` to make a grounded technical approach. Do not build the product solution in this role.

Run after `$dev-repo-context` and before `$dev-architect` when the repo context or product spec exposes a real unknown.

## Boundaries

- Investigate technical feasibility, risky implementation paths, repo constraints, and option tradeoffs.
- Run small, bounded experiments only when reading code or docs is not enough. Keep experiments scratch-only unless the user explicitly asks to keep them.
- Do not modify production code as the spike output. If a temporary file, branch, or script is needed, clean it up or call it out clearly.
- Do not use this skill for third-party API documentation research as the primary task. Route API or SDK research to `$dev-api-research`.
- Stop and route back to PM if the uncertainty is product scope, user value, acceptance criteria, or strategic priority rather than engineering feasibility.

## Workflow

1. State the decision the spike must unlock.
2. Read the product spec, readiness notes, `$dev-repo-context` brief, and relevant local files.
3. List the viable technical options or hypotheses.
4. Gather evidence through code inspection, local commands, focused experiments, official docs, or comparable local implementations.
5. Compare options by feasibility, blast radius, complexity, migration risk, compatibility, performance, testability, and rollback.
6. Choose a recommended direction or mark the work risky/blocked.
7. Hand the report to `$dev-architect`; include any API research dependency if `$dev-api-research` is still needed.

## Output

```markdown
## Spike Report

Decision: <feasible | risky | blocked>

Question:
<The uncertainty this spike resolved.>

Context:
- <Issue/spec/repo facts that shaped the investigation.>

Options Considered:
- <Option>: <why it was plausible and what evidence supports/rejects it>

Experiments / Evidence:
- <Command, file, doc, prototype, or observed behavior>

Recommended Direction:
<The approach $dev-architect should use, or why architecture should stop.>

Architecture Implications:
- <Layer, contract, migration, dependency, permission, or compatibility impact>

Implementation Notes:
- <Concrete constraints or likely files/modules for the future implementation>

Validation Plan:
- <Tests, builds, smoke checks, or manual checks needed after implementation>

Risks / Blockers:
- <Known risk, unknown, or blocker>

Open Questions:
- <Only questions the spike could not resolve>

Next Step:
<$dev-api-research | $dev-architect | $pm-readiness-review | stop>
```

Keep the report decision-oriented. The purpose is to let the next Dev role proceed without guessing.
