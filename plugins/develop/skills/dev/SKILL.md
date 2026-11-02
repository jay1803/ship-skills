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

Own one coding-ready issue's lifecycle state, phase acceptance and delivery
through the authorized PR, review, CI and merge/test boundary. Workers inherit
available parent permissions; explicit user restrictions, repository policy and
runtime limits remain binding. Delegation does not require renewed approval.

For one independent issue, the invoking task is the persistent **issue worker**.
For a ready issue set or project, continue here as the **project controller**
through `$dev-project-orchestrator`, with one issue worker per assigned issue,
without asking the user to restart. Preserve the
[role boundary](references/execution-ownership.md#controller-issue-worker-and-bounded-agents).

Default execution is unattended `standard`. Resolve delivery decisions through
their existing owners and comment material decisions on affected tickets. Apply
[discovered-work ownership](references/execution-ownership.md#autonomous-decisions-and-discovered-work):
one shared follow-up parent, deferred nonblockers, and only necessary blocking
remediation in the current delivery.

## Entry And Resume

When Dev is only an implicit candidate or the request names no issue, apply
[Direct eligibility and issue resolution](references/entry-readiness.md) before
tracker search, broad research, goals, Git setup or delegation; a Direct route
finishes there without Dev State. Discussing or editing this Skill is not an invocation of `$dev`.

For issue entry/resume, apply [resume preflight](references/resume-preflight.md)
before execution or mutation. It maps every request to its owner and audits
readiness; issue delivery starts only after a passing `dev_new` or `dev_resume`.
Develop needs no Product Skill, router or paid service. When Product is
installed, run its Skills only on the requester's explicit request, as advisory
input.

Record the Resume Receipt in Dev State after a pass. Reconcile and reuse matching
issue, comment, worktree, branch, PR, CI, Review and worker state. Refresh only evidence
invalidated by changed inputs; a resume does not replay completed phases or
create another controller. Missing optional artifacts do not select a stage.
Apply [owner names](references/execution-ownership.md#thread-and-sub-agent-names)
and carry verified naming context into helper handoffs.

## Stage Selection

Apply the [mode contract](references/development-mode-contract.md) for
validation depth, defect thresholds and deferred real-environment acceptance.
Fast prunes only its listed optional stages, with disclosed omissions;
primary-path, protected-boundary, enforced CI and repository authority gates
remain. Small work alone does not select fast mode.

| Stage | Select when |
| --- | --- |
| `$dev-planner` | an unresolved technical choice, task boundary, invariant, migration, cross-module contract, concurrency/security decision, non-obvious sequence or material rework/failure risk needs a plan |
| `$dev-api-steward` | backend/API behavior or contracts may change, including internal APIs, auth, errors, generated clients and compatibility; preserve pre/post stewardship |
| `$dev-verifier` | independent completion evidence is required, implementer evidence is insufficient, or changed-path risk needs verification; refresh a selected verifier when its evidence is invalidated |
| `$review` | every standard/strict PR or an explicit trigger, omitted only under the [Review lifecycle](references/review-lifecycle.md#requesting-review); Review owns risk-selected depth |

Use the [tracked-artifact preset](references/development-mode-contract.md#tracked-artifact-preset)
for a clear artifact that requires tracked delivery. Preserve its protected
escalation and CI/merge policy. Resolve bounded missing facts in the next owner;
unselected discovery/planning stages need no artifact. A passing phase advances
to the next selected owner, not a fixed checklist.

A current complete engineering ticket is the implementation plan. Apply the
[engineering ticket protocol](../dev-planner/references/engineering-ticket-protocol.md)
when preparing assignments. A `single` entry route is not an engineering
`no_split` decision: when new evidence exposes a missing producer contract or
material task boundary, preserve current work, report it to the existing project
controller when present and pause dependent implementation/dispatch for planner
[reassessment](../dev-planner/references/task-decomposition.md#reassessment-handoff).

## Execute And Accept Evidence

Load only the references for the current decision. Reading one does not select
a stage or grant mutation authority.

| Decision | Canonical guidance |
| --- | --- |
| Direct exclusion or a request naming no issue | [Direct eligibility and issue resolution](references/entry-readiness.md) |
| Request owner, entry audit, resume and receipt freshness | [Resume preflight](references/resume-preflight.md) |
| Phase ownership, delegation and repair/capacity recovery | [Execution ownership](references/execution-ownership.md) |
| Delegation routing | [`$agent-routing`](../agent-routing/SKILL.md) |
| Branch/worktree or PR base | [Branch strategy](references/branch-strategy.md) |
| Selected pre-PR work | [Implementation and validation](references/implementation-validation.md) |
| PR, repair and closeout | [PR and closeout](references/pr-closeout.md) |
| Selected technical Review | [Review boundary](references/dev-review-v2-contract.md) and [Review lifecycle](references/review-lifecycle.md) |
| State and reporting | [Dev State](references/dev-state.md) |

Keep one mutating owner per branch/worktree. Implement, validate and repair
inline by default; dispatch a bounded implementer only under
[delegated implementation](references/execution-ownership.md#delegated-implementation).
Preserve independent Review and any explicitly independent verifier in clean
contexts. Other work delegates when isolation, capability or useful parallelism
requires it, not for each phase name.
Reuse inspectable current validation under `$dev-test`'s evidence rules. Recover
the owner and pending handoff before repair or capacity-blocked dispatch.

Dev-managed Review starts on the current PR after traceability and readiness.
Accept only a current, non-stale Review result with complete coverage for the
exact head; a skip is disclosed omission, never approved code. Develop owns the
ledger, re-review selection, triage, round budget and exhaustion under the
[Review lifecycle](references/review-lifecycle.md). Lone specialist output
cannot trigger repair or satisfy this gate.

## Completion Boundary

Continue through the selected authorized lifecycle. Respect plan-only, PR-only,
no-merge and repository human-review boundaries. A required gate remains pending
until evidenced; no Skill grants merge, release or deployment authority. Use goal
tools only when the user or governing tool contract authorizes them; availability
alone does not authorize goal creation. Any permitted Dev goal covers this same
boundary rather than implementation alone.

Real-environment and agent-unavailable checks follow the mode contract's
[precedence](references/development-mode-contract.md#unattended-validation-and-deferred-acceptance);
preserve actual failures, enforced CI and required authority.

Carry mode and `Skipped / Unverified` through state and handoffs. Report concrete
blockers and the next owner. Mode-authorized omissions remain disclosed.

Classify production promotion by repository policy and PR purpose, not the name
`main`; `$release` owns it. Read [production-loop guidance](references/production-loop-contract.md)
only for a required loop or material acceptance risk needing representative
data, scale, an external oracle, rollout/migration conditions or measurable
runtime constraints. Otherwise record `Production Loop: not required`. Preserve
required verifier thresholds; production-only verification belongs to `$release`.
