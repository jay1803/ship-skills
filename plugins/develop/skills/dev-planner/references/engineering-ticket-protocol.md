# Engineering Ticket Protocol

Read when planning engineering task boundaries, writing task drafts, or
handing a planned task to an implementation worker. This protocol defines
required information and decision ownership, not a fixed ticket length or a new
workflow gate for every patch.

## Ownership And Planning

The accepted issue sets outcomes, scope and acceptance. The lead planner owns
the technical approach, shared contracts and engineering task boundaries inside
approved product scope. Apply the
[task decomposition criteria](task-decomposition.md) when assessing boundaries;
retain one coherent task when splitting adds only coordination. The caller owns assignment, draft acceptance, tracker authority,
readiness, dispatch and completion; a project controller applies its
[ticket preparation](../../dev-project-orchestrator/references/ticket-preparation.md)
rules. Tickets do not preselect a model.

The lead plan records source/contract revisions, shared decisions, task keys,
`implementation` or `design` kind, each task's outcome and ownership, dependency
edges, safe PR boundaries and parent-acceptance coverage. Reuse current plans,
existing tasks and PRs. Product gaps return as requester questions. Unknown
technical facts remain named gaps; do not invent source paths, contracts or
completed decisions.

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
