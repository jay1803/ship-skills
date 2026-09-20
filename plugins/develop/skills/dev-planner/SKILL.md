---
name: dev-planner
description: "Design approved engineering work, decide task boundaries, and prepare implementation-ready ticket plans. Use for technical choices, decomposition, or concrete implementation planning; not execution scheduling."
metadata:
  owner: jay1803
  family: develop
  maturity: stable
  distribution: develop
---

# Dev: Technical Plan

Own the technical approach and engineering task boundaries for approved product
work or a caller-assigned bounded issue set. Return one plan at the depth needed
for the decision; a settled
local change does not need separate discovery, architecture, or slice documents.
Do not write production code or choose missing product behavior in this role.

Use for a feature/fix with meaningful technical alternatives, a structural
refactor, an ambiguous domain boundary, or non-obvious sequencing/handoff. For
an already-clear local patch, let the implementer use the current brief. A
bounded multi-task design request stays here; project scheduling and execution
belong to `$dev-project-orchestrator`; explicit multi-PR integration belongs to
`$dev-integration-manager`.

## Inputs And Context

Use approved scope, acceptance criteria, current source evidence, selected mode,
and relevant diagnosis/API/Design inputs. A current implementation brief is
sufficient; do not demand artifacts from intentionally unselected stages.
Resolve only missing ownership, local-pattern, constraint, or validation facts:
search from relevant files/symbols/errors with `rg`, follow dependencies when
needed, and return source anchors and material unknowns. Stop discovery once
the next decision is supported; reuse facts still current for the target.

Read the [development-mode contract](../dev/references/development-mode-contract.md)
when planning mode-dependent checks. Missing evidence that changes product
scope, safety, a critical acceptance criterion, or dependency blocks coding and
returns to `$pm-readiness-review`. Missing live credentials, environment access,
or acceptance logistics may remain `blocked - may begin development` when they
do not change safe implementation; keep that gap through outcome completion.

## Conditional Design

| Unresolved decision | Read or route |
| --- | --- |
| Domain vocabulary, invariant, state transition, or boundary ownership would change the implementation | [Domain modeling](references/domain-modeling.md); retain source anchors in this plan |
| Primarily behavior-preserving restructuring needs invariants, migration order, compatibility, or rollback decisions | [Refactor design](references/refactor.md) |
| Observed defect has no confirmed cause | `$dev-debugger` before choosing a repair |
| Local feasibility or competing paths cannot be settled from current evidence | `$dev-spike` |
| Third-party behavior is the deciding unknown | `$dev-api-research` |
| Owned backend/API behavior or compatibility may change | `$dev-api-steward` pre-implementation contract review, then finalize affected parts of this plan |

Read only a selected reference. Do not create a modeling/bypass report for a
simple presentation or stateless change. Domain/refactor analysis is part of
this technical plan, not another mandatory owner or document handoff.

## Technical Approach

1. Name the technical decision, affected boundaries, and current local pattern.
   Compare alternatives only when they are viable and materially different;
   prefer an established fitting pattern over speculative architecture.
2. Settle contracts, responsibilities, compatibility, and failure behavior from
   evidence. Preserve source-anchored vocabulary, state transitions, invariants,
   and ownership when domain analysis is needed. Name unresolved decisions and
   their owner instead of choosing product behavior or redesigning the domain.
3. For a refactor, establish invariants before migration design; retain
   incremental build/test checkpoints, safe cut points, and rollback.
4. Identify API stewardship, provider research, validation fidelity, and
   external dependencies that change the approach. Contract review may refine
   the plan; it does not require a second architecture artifact.

For migration, maintenance, or multi-owner state changes, trace admission,
in-flight work, transition, abort, rollback, and restart across each affected
owner. Distinguish durable state, process-local authority, and startup
configuration. Check alternate exit paths before settling the sequence. Use
actual component modes when lock/journal/runtime semantics determine safety;
a generic substitute is not proof of the required behavior. Keep this analysis
conditional on a real stateful boundary, not a template for every patch.

## Implementation Slices When Needed

When task boundaries or ticket handoff need planning, read the
[engineering ticket protocol](references/engineering-ticket-protocol.md).
Settle shared design and retain or propose engineering tasks in this Technical
Plan. For split/no-split decisions or reassessment, apply the
[task decomposition criteria](references/task-decomposition.md) within this
plan, not as a separate gate or owner. Classify tasks as
implementation/design, preserve parent acceptance and existing dependencies,
and give the caller stable keys and bounded per-task planning assignments.
By default expand only ready parents; future dependent plans remain provisional.

Prefer stronger reasoning for design and execution-focused models for settled
implementation under the protocol. A caller can parallelize independent ticket
preparation within runtime limits; this planner returns assignments/artifacts
and does not become their controller. A worker assigned one fixed leaf refines
only that leaf. Return material boundary changes to its owner instead of
recursively splitting or dispatching. Do not write tracker records here.

Create ordered slices only when sequencing, dependency handoff, migration, or
rework risk needs them. Otherwise a concise approach with scope and acceptance
evidence is enough. A slice is one coherent, independently verifiable outcome,
not a file list or a ceremonial "add tests" step.

For each selected slice record the outcome, relevant scope, dependency order,
observable acceptance evidence, rollback point (or justified not applicable),
and a concrete stop/escalation boundary. For refactors retain invariant checks;
for bugs retain the original repro and regression proof. Mark slices parallel
only when contracts are stable, rollback scopes do not overlap, and ownership
permits it; project-wide scheduling stays with the project controller.

Use verified repository commands, generated-artifact rules, and platform
reference(s) for `$dev-implementer`. If no platform reference fits, name the
actual surface and repository guidance. API-changing work needs a
post-implementation stewardship checkpoint before formal testing. For a
cross-repository issue, plan only the assigned repo slice and named external
contracts; do not create sibling work or choose a multi-PR merge strategy.

Keep implementation readiness separate from outcome-verification readiness.
Fast records authorized omissions; standard/strict retain required checks and
outcome evidence. Strict's severity threshold alone adds no stage. Preserve
required production-loop verifier, fidelity, timing, and stop limits.

For a changed stateful flow whose normal tests can bypass the behavior being
promised, make the first relevant implementation slice prove one runnable path
through the actual coordinator/repository and observable completion or routing.
The planner identifies this checkpoint; the implementer/test owner compiles and
executes it. A success flag, mounted success screen or disconnected callback
proves only the harness. Inspect local runtime/seed and provider-seam options
before concluding that the path cannot be tested; a provider substitute must
not replace the changed behavior itself. Keep test-only APIs out of release
surfaces and name the evidence fidelity actually demonstrated.

Choose boundary probes from the changed contract: for auth or persisted session
changes, this may mean native SDK storage/reopen and observable barriers before
and after an identity change, with distinct consumers when isolation matters.
Do not require this slice for a stateless patch already proved by focused tests,
or use it to reinstate mode-waived live accounts and environment logistics.

## Repair Boundary

Record the bounded behavior, contracts, modules, and generated artifacts a
repair may touch, plus the repository-defined merge-ready representation.
A new product decision, externally consumed contract, persistent model,
migration/deployment order, ownership, or cross-repository surface re-enters
planning or PM; it is not ordinary repair. Reuse unaffected decisions when
replanning instead of restarting all investigation.

## Output And Handoff

Return one **Technical Plan**, with only applicable sections:

- Decision/approach and source anchors; affected boundaries and non-goals.
- Implementation readiness and separate outcome-verification readiness.
- Selected domain invariants or refactor migration/rollback decisions.
- Ordered verifiable slices when needed; otherwise the bounded change and proof.
- Implementation/platform ownership, API and external-dependency checkpoints.
- When engineering tasks are assessed: per-parent split/no-split/blocked result,
  task keys/kinds and design readiness, dependencies, parent-acceptance mapping,
  and protocol-complete ticket bodies or named missing design inputs. Include
  per-task planning assignments when the caller needs parallel preparation.
- Validation commands, required evidence/fidelity, and skipped/unverified work.
- In-plan repair scope, merge-ready representation, and escalation conditions.

Return to the caller/controller for the next selected phase, normally
`$dev-implementer` once required decisions are settled. Plan-only requests stop
at the plan; a recommendation does not dispatch workers or authorize mutation.
