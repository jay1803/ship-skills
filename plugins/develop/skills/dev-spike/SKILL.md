---
name: dev-spike
description: "Investigate unresolved technical feasibility or competing implementation paths before architecture. Observed defects belong to dev-debugger first."
metadata:
  owner: jay1803
  family: develop
  maturity: stable
  distribution: develop
---

# Dev: Spike

Reduce uncertainty enough for `$dev-planner` to make a grounded technical approach. Do not build the product solution in this role.

Run when current repository evidence or the approved scope exposes a real feasibility unknown; no separate discovery or architecture document is required.

## Boundaries

- Investigate technical feasibility, risky implementation paths, repo constraints, and option tradeoffs.
- Use `$dev-debugger` first when the starting point is an observed defect, regression, or failed acceptance check whose root cause is unknown. Use this skill after diagnosis only when feasibility or competing fix directions remain unresolved.
- Run small, bounded experiments only when reading code or docs is not enough. Keep experiments scratch-only unless the user explicitly asks to keep them.
- Do not modify production code as the spike output. If a temporary file, branch, or script is needed, clean it up or call it out clearly.
- Do not use this skill for third-party API documentation research as the primary task. Route API or SDK research to `$dev-api-research`.
- Stop and return the exact question for the requester if the uncertainty is product scope, user value, acceptance criteria, or strategic priority rather than engineering feasibility.

## Workflow

State the decision the spike must unlock and the viable options, then gather
only the evidence that discriminates between them. Stop once one direction is
supported or the work is shown risky or blocked. Return the report to the
caller/controller; recommend `$dev-planner` only if a technical decision or
implementation sequence still needs a plan, and name any required API research.

When the current request is investigation only, stop at this report, adding
confidence, the affected boundary and a `conclusive`, `inconclusive`, `blocked`
or `not-applicable` status with one proposed next route; acting on it needs a
new explicit user request or authorization.

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
<The approach $dev-planner should use, or why architecture should stop.>

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
<$dev-api-research | $dev-planner | requester decision | stop>
```

Keep the report decision-oriented. The purpose is to let the next Dev role proceed without guessing.
