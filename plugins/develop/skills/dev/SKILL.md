---
name: dev
description: "Deliver one coding-ready issue through its PR, review, CI, merge, and test handoff. Use for the full issue lifecycle, not ordinary bounded edits or multi-issue scheduling."
metadata:
  owner: jay1803
  family: develop
  maturity: stable
  distribution: develop
---

# Dev: Issue Delivery

Deliver one coding-ready issue through its selected implementation, validation,
PR, review, CI, and merge/test handoff. Own lifecycle state and acceptance of
phase results; use narrow Skills for the current decision or artifact. Workers
inherit all available parent permissions by default. Only explicit user
restrictions or enforced runtime limits narrow them; delegation and phase
transitions do not require renewed user approval.

## Entry And Resume

When Dev is only an implicit candidate, read [entry readiness](references/entry-readiness.md)
and resolve Direct Artifact / Direct Patch before tracker search, repository-wide
research, goals, branch/worktree setup, or delegation. Ordinary bounded edits
finish under their own task-specific workflow and repository policy, without
Dev State. Discussing or editing this Skill is not an invocation of `$dev`.

For issue-level entry or resume, read [resume preflight](references/resume-preflight.md)
before repository work, goals, Git/Linear/PR mutations, or downstream delegation.
Use the canonical `$issue-router` receipt for an issue, issue URL, parent,
project, or issue set. Only `dev_new` or `dev_resume` with verified readiness,
`delivery_shape: single`, and `terminal_intent: change` may begin Dev execution.
Continue an existing post-PR route from its exact owner and anchor. Investigation,
verification, PM, Direct, status, release, and blocked routes retain their own
completion and authorization boundaries. Multi/ambiguous delivery shape goes
to `$pm-project-orchestrator`; a project Dev route goes to `$dev-project-orchestrator`.

After a pass, emit the compact Resume Receipt defined by the preflight. Reuse
matching issue, worktree, branch, PR, head, CI, Review and worker state. Refresh
only evidence invalidated by material changes; do not replay completed phases
or create another controller because the session resumed. Missing optional
artifacts do not select a phase or block authorized work.

## Stage Selection

Read the [mode contract](references/development-mode-contract.md) when selecting
or executing the phase plan. Standard is the default unattended mode; use its
simulator/seed/mock validation and deferred-acceptance rule. Explicit fast mode retains
primary-path and enforced gates while disclosing omissions; strict uses the
standard stage-selection rules with deeper risk-selected validation and blocks
P0/P1/P2 rather than P0/P1. Standard focuses on primary flows and ticket-specific
regressions, without automatic reverse-red or unrelated edge-case tests. Specific
QA follows user/repository/acceptance requirements and concrete changed-path risk.
Direct paths are not modes, and small work alone does not select fast mode.

| Stage | Select when |
| --- | --- |
| `$dev-planner` | an unresolved technical choice, engineering task boundary, domain invariant, refactor/migration boundary, cross-module contract, concurrency/security decision, implementation sequence, or high rework/failure risk needs a plan |
| `$dev-api-steward` | backend/API behavior or contract changes, including internal contracts, auth/permissions, errors, pagination, webhooks, generated clients, or compatibility |
| `$dev-verifier` | independent freshness is needed, implementer evidence is insufficient, risk is high, or the head changed |
| `$review` | normal standard/strict phase plan or an explicit trigger selects combined Review V2; tracked-artifact defaults unselected |
| `$pm-pr-product-review` | user/product behavior or approved acceptance criteria change; internal maintenance is `not applicable` |

Use the mode contract's [tracked-artifact preset](references/development-mode-contract.md#tracked-artifact-preset)
when the artifact is clear but the repository/user requires a tracked delivery
lifecycle. Preserve its protected-boundary escalation and required CI/merge
policy. Fast mode prunes optional planning, verifier and reviews; it cannot
prune protected API/schema/auth/security/privacy/migration/destructive/concurrency
work, primary-path validation, enforced CI, or repository authority.

Resolve bounded missing facts in the next selected owner. The implementation
brief supplies scope, acceptance, local patterns, validation floor and relevant
constraints; unselected investigation/planning stages need no artifact.
A passing phase advances to its next selected owner, not a fixed checklist.

When the planner prepares engineering tickets, apply the
[engineering ticket protocol](../dev-planner/references/engineering-ticket-protocol.md)
for task assignments, accepted content and write authority. A current complete
ticket is the implementation plan; do not rerun design merely to hand it to a
smaller model. A discovered split returns through the existing materialization
and project routing boundary before child execution, preserving current work.

## Execution And References

Load the references for the current decision. A reference supplies guidance;
reading it does not select a stage or grant mutation authority.

| Current decision | Read |
| --- | --- |
| Implicit entry, issue resolution, or existing issue without a verified PM handoff | [Entry readiness](references/entry-readiness.md) |
| New/resumed issue lifecycle and receipt freshness | [Resume preflight](references/resume-preflight.md) |
| Planning/executing selected phases after preflight | [Execution ownership](references/execution-ownership.md) |
| Delegation | [Jev executable routing input](../agent-routing/references/jev-input.md); consume the returned packet without reclassification |
| Branch/worktree setup, PR base or merge handoff | [Branch strategy](references/branch-strategy.md); preserve repository policy and inherited batch base |
| Selected discovery, planning, implementation, testing or verification | [Implementation and validation](references/implementation-validation.md) |
| PR, traceability, Review, repair, Product Review or merge/test handoff | [PR and closeout](references/pr-closeout.md) |
| Planning, invoking, repairing or accepting technical Review | [Review V2 boundary](references/dev-review-v2-contract.md) |
| Creating/updating state or reporting | [Dev State and reporting](references/dev-state.md) |

Keep one mutating owner per branch/worktree. Reuse a suitable implementer for
implementation, local testing and scoped repair; delegate when independence,
isolation, capability or useful parallel work requires it. Reuse inspectable
matching validation under `$dev-test`'s evidence rules, preserving selected
independent verification and Review. A phase name alone needs no new agent.

Dev-managed Review uses the current PR after traceability sync and Review
Readiness, and accepts only the complete combined Review V2 result. Preserve
its Review Run and shared repair budget across resumes; an individual review
artifact cannot trigger repair or satisfy the gate.

## Completion Boundary

Continue through the authorized lifecycle rather than stopping after the first
implementation, local pass, or PR creation. Carry the selected mode and
`Skipped / Unverified` through state and handoffs. Respect an explicit plan-only,
PR-only, no-merge or other narrower user boundary and repository human-review
requirements. A required gate remains pending or blocked until evidenced; no
Skill grants merge, release or deployment permission.

After a passing preflight, any permitted Dev goal covers the selected lifecycle:
approved scope, validation, PR to the resolved issue base, review/CI, authorized
merge, cleanup and required test handoff. Do not create a Dev goal for Direct
paths. Report concrete blockers and the next action; mode-authorized omissions
are disclosed rather than converted into blockers or passes.

Classify production promotion by repository policy and PR purpose, not the
branch name `main`. `$release` owns production-promotion decisions and execution.
Apply the mode contract before retaining test-environment or human-acceptance
gates. Waived real-environment tests remain unverified recommendations or a
separate human acceptance ticket; they do not hold engineering closeout open.

Read the [production-loop contract](references/production-loop-contract.md) only
when PM requires it or a material acceptance risk needs representative data,
scale, an external oracle, rollout/migration conditions, or measurable runtime
constraints. Otherwise record `Production Loop: not required`. Dev controls
required test-environment loops; production-only verification goes to `$release`.
Do not weaken a verifier or its threshold to obtain a pass.
