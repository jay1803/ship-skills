# Ticket Preparation

Read when the accepted scope needs technical decomposition, engineering ticket
drafts or their persistence. `$dev-planner` owns the technical approach, task
boundaries and ticket bodies under its
[ticket protocol](../../dev-planner/references/engineering-ticket-protocol.md);
this controller owns assignment, acceptance, tracker writes and dispatch.

## Planning Assignments

Route the lead plan and unsettled task design through
[`$agent-routing`](../../agent-routing/SKILL.md) as `unresolved` work and the
implementation of a settled task as `settled` work. Once the lead plan's shared
decisions and ownership are stable, assign one bounded planning subagent per
task in capacity-limited batches. Ten tasks mean ten accountable assignments,
not ten simultaneous processes. Parallel drafting does not imply parallel
implementation, and capacity batches or task numbers are not dependency edges;
change an edge only on an evidence-backed proposal you accept.

Each assignment carries the task key and any existing ticket ID, a unique output
location, scope and non-goals, source/contract revisions, shared decisions,
owned files/artifacts, prerequisites, remaining task-local questions, the
expected return (task key, design readiness, draft, gaps or boundary changes,
provenance) and its permissions: draft-only unless a later write grant names the
exact target and fields.

Before accepting drafts, check parent-acceptance coverage, shared-contract
agreement, non-conflicting ownership, dependency consistency and whether
implementation still needs design. A design task may be ready for design while
an implementation draft with material choices open is not ready to code. Reuse
an existing sufficient brief without a ceremonial rewrite.

## Persistence And Materialization

Planning authorizes no tracker writes. When creation or update is authorized,
the existing tracker owner applies accepted content. Keep one writer per
ticket, re-read every write, reconcile an uncertain create against live records
before retrying, preserve confirmed IDs and drafts on a partial failure, and
keep canonical product text intact. Maintain the task-key to ticket-ID mapping
and wire relations only between verified records.

Execution receives only materialized issues that pass the
[entry audit](../../dev/references/resume-preflight.md#entry-audit): never
draft keys, and never a split parent as an extra implementation task. Pass
accepted ticket content to its implementation owner as the Technical Plan;
drift, a failed assumption or a new contract, product, migration or
ownership decision returns the affected work here for planning, preserving
existing code and PRs. The controller verifies combined parent acceptance after
the child merges.
