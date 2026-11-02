# Execution Ownership

Read after preflight passes, before planning or executing selected Dev phases.

## Controller, Issue Worker And Bounded Agents

Develop has two persistent management layers. The project controller
(`$dev-project-orchestrator`) owns scheduling, dependencies, capacity, worker
dispatch/recovery, progress intervention and project completion. It verifies
delivery receipts and live barriers without repeating Review, and never
implements, repairs code, performs technical Review or takes over an issue's
delivery. One `$dev` issue worker per assigned issue owns that issue's delivery.
A standalone `$dev` task is the issue worker without a project controller;
existing deferred follow-up children do not turn an independent issue into an
execution graph.

- The issue worker owns the issue, branch, worktree, mode, phase sequencing,
  retry counters, blocker decisions, user communication and completion claims,
  and coordinates implementation, validation, Review, PR/CI, authorized merge
  and closeout. It may perform or delegate lifecycle operations such as PR
  creation, tracker updates, eligible merge and cleanup. It never dispatches a
  successor issue or starts a nested project controller.
- By default it applies `$dev-implementer` inline as the one writer for coding,
  local validation and scoped repair, keeping the ticket, plan and evidence in
  one context. It dispatches a bounded implementer only under
  [delegated implementation](#delegated-implementation), and coordinates
  independent Review sub-agents through `$review`. Implementers and reviewers
  are bounded sub-agents, not further delivery threads; Review's internal
  fan-out adds no management layer. Bounded agents return artifacts; the issue
  worker accepts or rejects them and updates Dev State before the next phase.
  Neither layer substitutes its own technical review for the selected
  independent Review gate.
- Independent Review has no inline fallback: reviewers need a clean context
  without implementation reasoning, so missing sub-agent capability blocks that
  gate.

The routing field `lifecycle: controller` covers both persistent layers: issue
workers keep the full-lifecycle capability floors without becoming project
orchestrators, and the routing role `worker` also names bounded artifact
producers. Below, issue-level "controller" means the `$dev` issue worker, never
permission for the project controller to take over its delivery.

### Delegated Implementation

Dispatch a bounded `$dev-implementer` only when one condition holds, and record
it in Dev State:

- the issue worker's context has degraded with length, such as after several
  Review or CI rounds, and a fresh context with the current brief serves better;
- an accepted plan splits the work into slices with disjoint files, contracts
  and validation paths that can run in parallel;
- the change needs an isolated worktree, different permissions or a missing
  capability.

A phase change, repair or Review batch alone keeps implementation inline, with
every gate intact.

## Merge Executor And Handoff Authority

The issue worker merges its own eligible PR unless an explicit user instruction
or applicable repository policy assigns that merge to another executor. Then
record the source, covered action, executor and release condition in Dev State
and stop at an `awaiting authorized merge` gate with the exact PR/base/head,
accepted evidence, next owner and wake condition. Report it as a handoff, not
completion or failed implementation; after live merge verification the same
worker resumes closeout. The exception grants no production authority and
leaves implementation, Review, PR/CI and closeout with the worker. The project
controller records and honors such an assignment under its
[merge-executor rule](../../dev-project-orchestrator/references/worker-execution.md#merge-executor-assignment).

Handoffs carry task facts and source-bound exceptions, not a rewritten copy of
the Skills. Do not invent approval, validation or routing gates from a role,
template or another worker's prompt. Resolve conflicts against the actual user
instruction and applicable policy; a generated summary is not new authority.

## Thread And Sub-Agent Names

Once entry/readiness accepts the scope, name a standalone issue worker
`<issue> Worker` (`EX-101 Worker`). A project issue worker keeps the
`<parent>: <issue> Worker` name its controller assigned under the
[thread naming contract](../../dev-project-orchestrator/references/worker-execution.md#controller-and-worker-thread-names).
Preserve a title the user chose. Names never change routing roles, lifecycle
floors, authority or ownership. Apply the name through the supported title
surface after reconciling and reusing the existing owner on resume; never create
another owner to fix a title. Without title control, keep the intended name in
existing state, disclose the limitation and continue authorized delivery without
claiming a rename.

Name bounded helpers, including Review descendants, by role without issue IDs:
`Implementer`, `Spec Reviewer`, `Judge`. When a native `task_name` requires
lowercase letters, digits and underscores, normalize the role only
(`implementer`, `spec_reviewer`), adding a short area or occurrence suffix only
to distinguish siblings. Every helper handoff carries the verified parent/scope,
assigned issue and owning worker ID, propagated to nested Review agents and
ancestor-brokered helpers; keep the readable role there if the runtime exposes
only a native key. Do not invent title parameters or a persistent thread for a
helper. Reuse suitable helper IDs and names across phases and repairs; a new
phase name alone does not require renaming or replacement.

## Bounded Repair And Capacity Recovery

At a validation failure or accepted Review repair, the current implementation
owner repairs: the issue worker inline by default, or the live delegated
implementer, resumed with the current branch/worktree and head, accepted failure
or triaged Review batch, scope, remaining validation and Review rounds, and
named return gate. Record a delegated agent's identity and mutating ownership in
Dev State; take over or replace it only after reconciling its outstanding
helpers and confirming it stopped, preserving its artifacts and cumulative
budgets. A bounded agent reports a new delivery or capability boundary to the
issue worker; it cannot rebind its running inference or create successor
issues. Apply an accepted model or effort change through the
[accepted escalation handoff](../../dev-project-orchestrator/references/executor-sessions.md#accepted-escalation-handoff),
not a silent switch or budget reset.

Implementation and repair that no delegation condition requires never wait for
capacity; they continue inline. When a phase that needs a sub-agent is
capacity-blocked, distinguish an unavailable capability from occupied slots
using the actual executor receipt. Keep the phase pending with its owner, helper
IDs, exact target, accepted evidence, next dispatch and wake condition. An agent
marked completed may still have active descendants; confirm actual occupancy
before treating its slot as free. Reuse a suitable helper or let a concrete
in-flight operation finish. Release idle agents only through supported controls
after preserving their state and reconciling descendants; do not stop a live
writer merely to admit another. In a project, return the capacity demand to the
controller, which may serialize helper work, defer issue admission or
[broker the helper](../../dev-project-orchestrator/references/worker-execution.md#capacity-scheduling)
while this worker stays the phase and evidence owner. Occupied slots never let
the issue worker code past a live delegated writer or perform independent Review
itself; without a supported dispatch/recovery path, report that concrete
blocker. Saved state alone is not a scheduled wake; use the executor's verified
continuation path rather than repeated idle waits.

## Autonomous Decisions And Discovered Work

Default `standard` execution is unattended for both management layers. The
project controller, or the standalone issue worker acting as its issue-level
controller, resolves delivery choices, phase selection, scheduling, retries and
development-blocker scope decisions within the requested lifecycle. Ask the
requester for product decisions and use the planner for contract decisions,
continuing from the recorded result; an agent handoff is not a human approval
gate. Preserve explicit user restrictions, repository human-only actions and
enforced runtime limits. A Skill cannot grant missing tracker, merge, release
or deployment authority.

Comment material decisions on the affected ticket: the decision, evidence and
reason, scope/dependency consequences and related issue IDs. Product-scope or
shared contract changes also retain the canonical owning artifact. Reuse a
matching decision comment on resume; local naming or formatting needs no
decision log.

For defects or other work discovered outside the accepted scope:

- In a project, the controller owns the shared discovery inventory and its
  tracker writes; an assigned issue worker reports discoveries and proposed
  blocking status to it instead of expanding its ticket or dispatching new work.
  A standalone issue worker owns these decisions for its delivery.
- Deduplicate findings, then create or reuse one follow-up parent for the root
  delivery when the first real discovery needs a ticket. Create newly recorded
  discoveries as its children, including blocking discoveries. Reuse that parent
  across workers, waves and resumes; retain its ID in state and handoffs. Index
  already-existing tickets there without duplicating them or silently changing
  an unrelated hierarchy. Record the originating issue, observed evidence,
  impact and blocking decision in each ticket and the parent's inventory.
- A discovery blocks development when evidence shows that it prevents the
  current issue or an already-included successor from meeting required product
  outcomes, implementation prerequisites, validation, CI or merge gates. A
  change-caused regression remains the current delivery's responsibility.
  Optional polish, broader cleanup or a waived test surface does not become a
  blocker merely because it was discovered during development.
- Leave nonblocking discoveries in backlog. Do not implement them, add them to
  the current repair batch, dispatch workers for them or make engineering
  completion depend on them. The follow-up parent is a tracking bucket, not an
  automatically included implementation issue or successor queue.
- Include the minimum necessary blocking remediation in the current delivery.
  Comment its evidence and scope adjustment on the affected delivery ticket and
  discovery ticket; record any dependency before dependent work continues. Ask
  the requester for new product decisions and route contract or task boundaries
  through `$dev-planner`, refresh affected readiness and dispatch through the
  existing controller once ready. Keep any independent remainder in backlog
  and preserve Review history and retry limits.

Tracker-write unavailability leaves exact drafts and a named persistence action;
do not fabricate tickets or lose the discoveries. It does not make a nonblocking
finding an engineering blocker. A real implementation or authority blocker
still holds its dependent work. Report the shared parent and included/deferred
discoveries at closeout without claiming the backlog was fixed.

## Delegation And Phase Order

Narrow Dev Skills are role boundaries, not agent boundaries: the
[implementation](implementation-validation.md) and [PR/closeout](pr-closeout.md)
workflows decide whether a phase runs in the issue worker or a bounded
sub-agent. Route every delegation with [`$agent-routing`](../../agent-routing/SKILL.md)
and record its requested and accepted binding in Dev State. Existing agents keep
their actual runtime bindings; a blocked route stops that dispatch. Reuse an
existing agent only while its accepted capability, context, tools and
permissions remain suitable.

Select exactly one current phase owner and keep later applicable Skills queued in
Dev State. When several apply, start with the earliest unresolved cause and let
that owner route to the next phase instead of running competing owners in
parallel. The current owner may run independent read-only subtasks in parallel
without transferring phase ownership; parallelize only read-only or independent
discovery/review work. End every phase with an accepted artifact plus a named
next owner, `complete`, or a concrete `blocked` state.

## Operating Rules

- Inspect live repository, branch, worktree, PR, CI and tracker evidence before
  current-state claims or mutations. Preserve unrelated local changes; do not
  discard, stash, overwrite or revert them without explicit user approval.
- Use approved Design artifacts and acceptance criteria as implementation inputs.
  A clear UI proposal needs no new visual artifact. Route a deciding unresolved
  visual choice to `$design` instead of silently redesigning it.
- Attempt the real approval-bearing tool call for an otherwise authorized action
  when the runtime requires it. A role/phase is not a hypothetical human gate;
  an actual denial retains its reason and blocks the affected action.
- Commit with the configured signing when it needs no interaction. When it
  would (a passphrase, unlock or approval prompt), do not trigger it: disable
  signing for that command, such as `git -c commit.gpgsign=false commit ...`,
  and report the unsigned commit, unless the user, repository policy or branch
  protection requires signed commits; then report the commit as blocked on
  signing. Never change 1Password/GPG/SSH/global signing settings.
