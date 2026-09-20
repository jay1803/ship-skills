# Engineering Task Decomposition

Use inside the Technical Plan when deciding or reassessing task boundaries.
Keeping one task is a valid result; a fixed-task implementation plan does not
need another decomposition assessment. Product owns outcomes and acceptance;
planning returns drafts, never tracker writes or worker dispatch.

## Evidence And Scope

Read assigned scope, acceptance, existing tasks/PRs, parent and dependency
relations, and relevant repository instructions/source/tests. Record source
anchors and contract revisions; separate facts, assumptions and missing evidence.
Issue titles or estimates alone cannot establish independent execution.

Retain supplied parents and dependency edges. By default expand only currently
ready parents: for A -> B -> C, assess A now and defer B/C with prerequisites;
reassess successors against delivered contracts. An explicit whole-scope request
may plan future work provisionally without satisfying its prerequisites.
Inspect neighbors only for contracts, duplicates and ownership conflicts.
Propose evidence-backed dependency deltas explicitly; do not flatten the graph,
release successors early or turn capacity batches into dependency edges.

## Boundary Decision

Record a disposition and concrete rationale per assessed parent:

- **no_split:** one coherent task/PR can implement and verify the outcome;
  splitting adds mostly coordination or artificial phases.
- **split:** distinct ownership, stable contracts, independent validation or
  safe merge points provide a concrete delivery benefit.
- **blocked:** missing product decisions, technical facts or contradictory
  dependencies prevent a defensible boundary. Name the gap and its owner;
  splitting is not a workaround for unresolved scope.

Use meaningful change, verification and safe merge/rollback boundaries, not
line/file counts, durations or task-size quotas. Include tests, docs and generated
artifacts with the behavior they support. A task need not expose an entire user
feature, but intermediate states must remain compatible or use an established
feature flag. Keep inseparable changes together or name their prerequisite and
safe intermediate state. Account for integration and handoff overhead.

Parallel implementation requires stable shared contracts, non-conflicting code
and artifact ownership, compatible migrations and independently usable checks.
Different files or absent tracker edges are insufficient. Where appropriate,
settle a contract prerequisite before conditional consumers; mocks do not prove
real integration. A bounded design task can resolve technical uncertainty under
the [ticket protocol](engineering-ticket-protocol.md), without making dependent
implementation ready prematurely.

Map every parent acceptance criterion to task evidence and combined verification.
Merged child PRs alone do not establish parent completion. Apply the
[development-mode contract](../../dev/references/development-mode-contract.md),
including unattended validation and deferred acceptance; retain actual rollout
authority and unverified real-world outcomes without inventing live/human gates.

## Assessment Record And Reuse

Keep the assessment in the Technical Plan: reference, scope/acceptance/contract
basis, assessed and deferred parents, dispositions, stable task keys, task kinds,
design readiness, dependencies, acceptance mapping and named missing decisions.
Use the ticket protocol for concrete task bodies and caller assignments.
Propose `container` for a split parent and `executable` for a settled no-split or
derived task. Blocked/deferred work is not executable; a design task can be
executable only for its bounded decision artifact. These proposals do not replace
current Product readiness or authorize implementation.

Reuse an assessment while its outcome, acceptance, shared contracts, ownership,
chosen design and migration boundary remain valid. Ordinary comments, unrelated
commits or additional implementation steps alone do not invalidate it. A label
or parent link without matching evidence is not a valid prior assessment.
Reassess only the materially affected boundary.

A fixed leaf may refine its implementation steps, not create children or dispatch
replacement workers. New shared migration/ownership or other material boundary
changes return to the same owning controller with evidence, proposed changes
and existing code/PRs to preserve. A revised plan does not add a controller level.
