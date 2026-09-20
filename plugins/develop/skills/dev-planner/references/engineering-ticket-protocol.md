# Engineering Ticket Protocol

Read when planning engineering task boundaries, writing or accepting task
drafts, or handing a planned task to an implementation worker. This protocol
defines required information and decision ownership, not a fixed ticket length
or a new workflow gate for every patch.

## Ownership And Planning

Product owns outcomes, scope and acceptance. The lead planner owns the technical
approach, shared contracts and engineering task boundaries inside approved
product scope. Apply the [task decomposition criteria](task-decomposition.md)
when assessing boundaries; retain one coherent task when splitting adds only coordination. The caller
owns assignment, tracker authority, readiness, dispatch and completion.

Prefer a stronger reasoning model for the lead plan and per-task design; prefer
execution-focused models such as Sonnet or GPT Terra for implementation after
material decisions are settled. Supply the actual design/implementation scope
and this preference to the existing agent-routing mechanism. Model examples
are not required runtime IDs or a reason to bypass capability floors, explicit
user bindings or availability. Existing controllers keep their bindings.

The lead plan records source/contract revisions, shared decisions, task keys,
`implementation` or `design` kind, each task's outcome and ownership, dependency
edges, safe PR boundaries and parent-acceptance coverage. Reuse current plans,
existing tasks and PRs. Product gaps return to Product. Unknown technical facts
remain named gaps; do not invent source paths, contracts or completed decisions.

Planning a task normally includes its design without a separate design ticket.
Use a design task only when investigation or unresolved choices are a bounded
deliverable: specify the questions, constraints, evidence to obtain, expected
decision/contract artifact and acceptance. Assign stronger reasoning capability.
Dependent implementation remains deferred until the decision is incorporated
into its ticket and affected boundaries are rechecked. Design completion is not
parent implementation completion. A material gap that prevents a defensible
boundary remains blocked, rather than being disguised by splitting.

## Ticket Body And Detail Boundary

For each implementation task, including a retained no-split task, provide a
clear action/outcome title and a self-contained body covering applicable items:

- **Context and scope:** task key, parent/product reference, outcome and covered
  acceptance, included/excluded behavior, important behavior that stays unchanged.
- **Decided approach:** chosen design and brief rationale, shared contract
  version/source anchors, interfaces, data/state/error semantics and compatibility
  choices that affect this task. Embed essential decisions; links supplement
  the body rather than leaving the implementer to reconstruct conversation state.
- **Concrete changes:** affected modules, existing paths and key symbols, what
  behavior changes at each point, patterns/helpers to reuse, and necessary
  ordering. Identify new files as proposed. Include tests/docs/generated changes
  with the behavior they support, following repository generation rules.
- **Delivery boundary:** owned code/artifacts, input/output contracts, draft-key
  prerequisites, integration checks and safe merge/rollback state. A design-only
  task names its artifact boundary instead of inventing a code PR.
- **Verification:** observable cases with inputs and expected results, relevant
  tests to add/update and verified repository commands. State evidence fidelity,
  unavailable facts and mode-specific omissions honestly. The development-mode
  contract governs validation; a plan is not test evidence.
- **Decision latitude:** local choices the implementer may make, material
  assumptions to check and the concrete return-to-planner conditions.

Settle choices that affect product behavior, shared interfaces, persistent data,
compatibility, migration order, ownership or dependencies before implementation.
Leave local naming, formatting, helper organization and test-code organization
to the implementer within repository conventions and the stated behavior.
If two competent implementers could follow the ticket and produce incompatible
behavior or contracts, resolve that ambiguity. Different equivalent code is fine.

Do not prescribe line counts, every function body or full patches. Add examples,
pseudocode or exact code only when they remove a consequential ambiguity; a
local patch can have a short specific plan. "Implement pagination" or a file
list alone is insufficient. A useful plan identifies the query/helper to change,
cursor and ordering semantics, response contract and cross-page test outcomes.
Do not promote an example choice into policy for unrelated tasks.

## Parallel Ticket Preparation

The controller can assign one bounded planning subagent per task once the lead
plan's shared decisions and ownership are stable. Ten tasks mean ten accountable
assignments, not necessarily ten simultaneous processes; use available slots
in batches. Parallel drafting does not imply parallel implementation. An
explicit serial scope or unresolved shared contract still constrains preparation.
Preserve the supplied dependency edges; capacity batches and task numbering are
not dependencies. Add or remove an edge only as an explicit evidence-backed
proposal for the controller to accept. Do not turn one producer-consumer edge
into a serial chain through unrelated tasks.

Each assignment carries:

- Controller identity, task key and existing ticket ID if any; a unique output
  location, assigned scope/non-goals and source/contract revisions.
- Shared decisions, owned files/artifacts, required inputs, prerequisites,
  remaining task-local design questions and executor capability preference.
- This ticket protocol, expected title/body, acceptance evidence and return
  format: task key, design readiness, draft, gaps/boundary changes and provenance.
- Exact permissions: draft-only by default; any later write grant names the
  target team/project/parent or existing issue, accepted content and allowed
  fields. No sibling, project graph, status or product-spec writes by inference.

The worker uses `$dev-planner` to refine only its assigned task. It does not
create child tasks, dispatch replacements or redesign shared contracts. Return
proposed boundary changes to the same controller; the lead planner resolves
affected design before dependent drafts proceed. Reuse unaffected work.

Before accepting drafts, the controller checks coverage of parent acceptance,
shared-contract agreement, non-conflicting ownership, dependency consistency
and whether implementation still needs design. A design task may be ready for
design; an implementation draft with material choices open is not ready to code.
Use an existing sufficient implementation brief without a ceremonial rewrite.

## Persistence And Execution

Drafting and planning alone authorize no tracker writes. When creation/update is
authorized, the existing tracker owner may apply accepted content or delegate
one exact ticket write to its assigned worker in a separately gated write step.
The planning role itself remains draft-only. Preserve canonical product text;
engineering details supplement it rather than overwriting scope or acceptance.
Use the tracker skill and re-read each write. On an uncertain create response,
reconcile live records before retrying; do not create a duplicate.

The controller maintains task-key -> ticket-ID mapping and owns parent/child
links, dependency edges and readiness/status transitions. Reserve one writer
per ticket/key, verify created records before wiring cross-ticket relations,
and preserve confirmed IDs/drafts on partial failure. An unauthorized write
remains a draft with the named outstanding action. Where the workflow reserves
materialization to Product, return the accepted engineering drafts to that
owner; this protocol does not grant another role its writes.

Refresh the existing readiness/router receipt after materialized scope changes;
do not pass draft keys to issue execution or run a split parent as an extra
implementation task. A single-issue Dev controller that discovers a multi-task
delivery returns the affected plan and existing work to its owning controller.
For accepted engineering tasks under one product outcome, request the PM
controller's engineering-task materialization path with the same issue bound as
the proposed parent. Refresh routing with that parent target and explicit
materialization request; do not reclassify the product outcome as `multi` merely
because it needs multiple engineering PRs. Materialization remains within the
caller's write authority, followed by the normal project handoff for the ready
child inventory. Do not start a nested project controller from
an implementation leaf. Missing Product/route evidence remains a real blocker.

Pass accepted ticket content and design basis to the implementation owner.
Reuse it as the Technical Plan; do not ask an execution-focused worker to choose
the architecture again or automatically rerun planning for an unchanged task.
Local coding and in-scope debugging remain allowed. Source drift, failed
assumptions or a new contract/product/migration/ownership decision returns the
affected work to the controller for planning; preserve existing code and PRs.
Workers do not recursively split or dispatch successors. The controller alone
opens implementation dependency barriers and verifies combined parent acceptance.
