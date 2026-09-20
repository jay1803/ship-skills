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
- Stop and route back to PM if the uncertainty is product scope, user value, acceptance criteria, or strategic priority rather than engineering feasibility.

## Workflow

1. State the decision the spike must unlock.
2. Read the approved scope, current brief, relevant local files, and any selected investigation evidence.
3. List the viable technical options or hypotheses.
4. Gather evidence through code inspection, local commands, focused experiments, official docs, or comparable local implementations.
5. Compare options by feasibility, blast radius, complexity, migration risk, compatibility, performance, testability, and rollback.
6. Choose a recommended direction or mark the work risky/blocked.
7. Return the report to the caller/controller; recommend `$dev-planner` only if a technical decision or implementation sequence still needs a plan, and name any required API research.

## Investigate-Only Terminal

When the canonical Issue Route receipt selects
`investigate/technical-spike` with `terminal_intent: diagnosis`, stop at the
spike report instead of handing work to `$dev-planner`. The report must state
the decision, evidence, options, recommendation, confidence, affected boundary,
validation needed to prove a future change, and one proposed next route with
status `conclusive`, `inconclusive`, `blocked`, or `not-applicable`.

Reading and ephemeral scratch experiments are the default budget. Keep scratch
work out of the durable repository unless the receipt or user explicitly
authorizes an exact retained experiment and validation. Do not create an
implementation branch/PR, update tracker completion, dispatch planner or
implementer work, or treat a recommended approach as delivery authorization.
A later request to build or fix requires a new router receipt and may reuse this
still-fresh spike report as its resume anchor.

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
<$dev-api-research | $dev-planner | $pm-readiness-review | stop>
```

Keep the report decision-oriented. The purpose is to let the next Dev role proceed without guessing.
