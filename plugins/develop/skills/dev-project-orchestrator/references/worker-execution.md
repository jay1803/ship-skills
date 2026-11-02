# Project Worker Execution

Read before dispatching, resuming, or accepting issue execution in any scheduling mode. For sequence scheduling, also read [sequence-mode.md](sequence-mode.md).

## Fresh Thread Handoff

When this skill needs a fresh issue thread:

1. Use the resolved executor's persistent controller/session entry directly.
   - For Codex, discover and use the create-thread tool. For Claude Code, discover the native background-session or configured Axis entry through [executor sessions](executor-sessions.md#discover-the-actual-session-surface), and verify its creation and management receipts. Do not launch an ad-hoc provider command that bypasses the selected adapter or worker registry.
   - Create one new user-owned, user-visible controller thread or session per ready issue in the current project scope. Dispatch every member of the same safe wave before waiting.
   - Route the issue under [Issue-Worker Routing](#issue-worker-routing) before creation, and apply the binding through the actual tool's permitted model/effort parameters, including its visible-task default-selection rule.
   - Publish the requested binding before creation. Record queued acceptance as pending; at the first ready/active observation apply the adapter's binding verification and update the resolved notice. Keep runtime acceptance separate from the routing result.
   - Apply the [thread naming contract](#controller-and-worker-thread-names): supply the worker title through the supported creation field and carry verified naming context in its handoff. Record the requested name and observed title separately; reconcile queued creation before renaming.
   - Use a local environment unless the user explicitly asks for a new worktree.
   - For an explicit worktree request, use the worktree environment and preserve requested branch or starting-state details when the tool supports them.
2. Include the controller thread/session id and worker callback packet in the initial prompt. Resolve the controller id with the executor's management tools; do not guess when multiple workers could match. Use the callback triggers in the Worker Handoff Shape; do not add a separate ordinary-progress callback request.
3. Use the worker handoff as the new thread's initial prompt without adding summaries, hidden instructions, or extra commentary.
4. Record the returned worker thread/session id (or queued creation handle) and resolved executor against the issue before creating another worker or yielding. A queued handle reserves that issue: reconcile its creation instead of creating a duplicate, and do not pass it to tools requiring a ready thread id.
5. After dispatching the complete ready wave, report all worker ids and enter the Controller-Owned Wave Execution workflow.
6. If direct worker callbacks are unavailable, continue with controller heartbeat monitoring.
7. If the current project id is unavailable and the thread tool cannot infer it, ask one short question for the target project instead of falling back to a projectless thread.
8. If persistent worker creation remains unavailable after entry discovery or an attempted creation, report the limitation and apply Worker Creation Failure And Recovery below.

## Issue-Worker Routing

The project controller routes each fresh issue worker, in wave and sequence
mode, deciding from that issue's complete scope with `lifecycle: controller`.
Record the routed envelope and binding in the issue-keyed registry and pass them
in the handoff; the worker consumes them without rerouting. Keep creation
handles, worker IDs, observed binding and fallbacks separate: queued is not
active and unexposed values remain unknown.

An ordinary resume of the same worker keeps its route while task, authority and
runtime inventory are materially unchanged. After compaction or a heartbeat,
recover the route and any pending creation before acting. A material change
reroutes with the prior envelope as `previous_route`; an accepted adjustment
follows the [escalation handoff](executor-sessions.md#accepted-escalation-handoff)
within the [escalation budget](executor-sessions.md#escalation-budget), never a
silent switch or duplicate owner. A fresh worker needs its own route after any
previous creation or owner is reconciled. This does not waive the worker's
readiness audit or its routing of its own bounded helpers.

## Controller And Worker Thread Names

Once execution is accepted, name this controller and its workers:

| Owner | Name | Example |
| --- | --- | --- |
| Project controller for a parent issue | `<parent_issue> Controller` | `EX-100 Controller` |
| Persistent issue worker in that delivery | `<parent_issue>: <issue> Worker` | `EX-100: EX-101 Worker` |

For a project or issue set without a parent issue, use its verified concise
scope/project label in place of `<parent_issue>`; do not invent a tracker parent
for naming. Apply the name to this controller through the supported title
surface, and supply a fresh worker's title at creation when supported. Record
the requested name and observed title separately in the registry; use
thread/session IDs for identity and callbacks, since titles need not be unique.
A queued creation handle is not a ready thread ID: wait for its actual identity
before using rename tools. User-chosen titles, resume, missing title control and
bounded-helper names follow the
[Dev naming rule](../../dev/references/execution-ownership.md#thread-and-sub-agent-names).

## Worker Creation Failure And Recovery

The project controller remains a scheduler when persistent worker creation is
unavailable. Record `execution_mode: dispatch-blocked`, the exact discovery or
creation failure, affected issue IDs and next recovery action, preserving
pending gates, helper state and artifacts for that recovery. Do not start the
issue inline or substitute a bounded agent for its persistent delivery owner.
Other accepted workers may continue within their existing dependencies; an
explicit sequence still waits for its current issue.

Reconcile pending or accepted-but-unobserved creation before retrying. Reuse a
verified existing issue worker and its state. If replacement is necessary,
confirm the prior owner and its mutating helpers have stopped before assigning
another owner; preserve branch/worktree, PR, current head, validation, Review
history and cumulative budgets. An inaccessible owner is not confirmed stopped.
Do not reset counters or restart delivered phases to recover a session.

## Progress Intervention

Record each substantial phase's expected observable proof, last meaningful
progress and next reassessment time in existing worker/controller state. A
closed causal question, supported contract decision, representative passing
path or independently reviewable delivery is progress for its phase. Activity,
new logs/source bundles and ordinary commits do not indefinitely renew an unmet
checkpoint. Known build/CI or external waiting is separate from active work.

Use compact current phase, proof, pending operation and blocker signals first.
Intervene immediately for a material boundary change or repeated failure with
no new discriminating evidence. For sustained implementation, use 30–60 minute
proof checkpoints as a starting window, a substantive reassessment around two
hours when the expected proof remains absent, and stop scope expansion around
four hours in the same unclosed phase pending a bounded revised plan. These are
soft review points, not automatic kill/merge/model-switch timers. Record a
phase-specific exception and next review point when known runtime duration,
useful evidence or an inseparable core justifies it; external waits do not
consume this active-work window. Reuse the existing callback/heartbeat and
[recovery state](controller-recovery.md), not a new short-poll supervisor.

1. Send the intervention to the owning issue worker: stop new expansion/retries
   at the earliest safe operation boundary, preserve WIP/commits and failures,
   coordinate affected mutating helpers, and return one compact checkpoint.
2. Verify the old writer, mutating descendants and background operations are
   stopped or safely handed off before admitting another writer. An interrupted
   model turn or inaccessible owner does not prove terminal/DB work stopped.
   Use only supported interruption/recovery controls; otherwise retain the exact
   execution blocker instead of duplicating ownership or bypassing the runtime.
3. Read the checkpoint: issue/owner and current target, verified outcomes and
   remaining acceptance, blocker/hypotheses and attempts, current WIP/resource
   ownership, independently deliverable parts and the next discriminating proof.
   Keep full sources at existing immutable locators; do not copy the full history.
4. Record one disposition, its owner, evidence, remaining budgets, next proof,
   stop condition and reassessment time in existing state:

| Evidence | Disposition |
| --- | --- |
| Selected gates and authorized merge/closeout are ready, only optional expansion remains | Stop optional work and prioritize the pending delivery through its assigned executor |
| Bounded scope, meaningful progress and a finite remaining proof | Resume the same worker with that proof and deadline |
| A bounded judgment exceeds current reasoning | Accept the existing escalation route; use stronger analysis or a safe supported binding handoff |
| New producer/state ownership or independent delivery invalidates the leaf | Return to [task reassessment](../../dev-planner/references/task-decomposition.md#reassessment-handoff); accept the plan, materialize/readiness-check children, then dispatch |
| Known build/CI/external dependency is pending | Save the operation/cursor and resume condition; use existing recovery |
| A product or authority decision, or a human decision an explicit user budget/binding instruction requires, is unresolved | Prepare the exact decision/options for its owner or human; hold only dependent work |

For task reassessment, assign the bounded question to the lead planner; a
missing product choice goes to the requester. On `no_split`, resume the same
worker with the planner's next proof and stop condition. On `split`, persist
the accepted drafts under [ticket preparation](ticket-preparation.md), verify
real child IDs, relations and readiness, and stop the old parent writer before
any overlapping child write; keep its PR until that work has an explicit
preserved or replacement disposition. A new issue never resets the failed
repair or Review loop. On `blocked`, hold dependent work for the named decision
owner.

Routine engineering disposition, including a model or effort choice within
existing authority and budget, needs no renewed human approval. A clearer task
boundary takes precedence over raising effort on an expanding assignment.

Make existing callbacks/heartbeat consume the recorded disposition, so an old
continue signal cannot reopen paused expansion. A phase dispatch hold is not
permission to change a tool-managed Goal's pause/budget state. Preserve selected
validation, independent Review, CI, permissions, merge authority and cumulative
history; elapsed pressure never waives them. A changed HEAD/intervention alone
need not repeat full Review. A merge here still requires the recorded
[explicit executor assignment](#merge-executor-assignment).

## Capacity Scheduling

Use the executor's observed limits and active-owner/helper receipts before
admitting more issues. Persistent sessions and bounded helpers may use different
pools; do not assume a fixed slot count or infer occupancy from visible issue
count. Plan room for the next required implementer or independent reviewer.
Review lenses can run serially against the same frozen target when parallel
capacity is unavailable; all selected coverage and independence still apply.

Reassess admission after a verified merge, freed resource or changed conflict.
An earlier planning group, one slow worker or a stale capacity estimate does not
hold an independent ready issue. Carry the actual scarce resource and evidence
for serialization; recheck it when that evidence changes, without assuming
extra slots or overlapping a shared simulator or a recorded conflict.

When a helper cannot start, preserve the issue worker and its exact pending
phase under [bounded repair and capacity recovery](../../dev/references/execution-ownership.md#bounded-repair-and-capacity-recovery).
Adjust admission or serialize helper demand before making another dispatch.
Use supported state-preserving release/recovery only after reconciling active
descendants. A completed parent label or a wait timeout is not a free-slot
receipt.

If the runtime permits helper creation only from an ancestor, the controller may
broker the issue worker's exact bounded handoff through an already-authorized
dispatch path. The issue worker remains phase and evidence owner: it records the
helper and its binding in its state and accepts the returned artifact before
continuing. Brokering creates no other issue owner and never lets the controller
implement, judge or merge; a helper artifact does not complete the issue or open
its merge barrier. Without a supported dispatch/recovery path, report that
concrete blocker.

Coordinate already-planned updates to a PR's base before its worker freezes an
expensive Review target. Record the pending merge/dependency and the next review
start condition in existing worker state. This is scheduling, not permission to
accept an old target: drift during Review still returns stale. Do not wait for
an indefinitely quiet base or hold unrelated work without a concrete update.

## Merge Executor Assignment

Issue workers merge their eligible PRs by default. Change the executor only for
an explicit user instruction or applicable repository policy: record the source,
covered issues/action, executor and release condition in the registry and the
worker handoff. A user-assigned controller may perform that exact eligible issue
merge while the worker holds its
[awaiting authorized merge](../../dev/references/execution-ownership.md#merge-executor-and-handoff-authority)
gate; the assignment moves only that action. Only the recorded executor attempts
the merge. Apply a later authorized change to its stated scope, without racing
the old executor or spreading a one-issue exception to siblings.

## Controller-Owned Wave Execution

Use this state machine for normal project waves and sequence mode. In normal
mode a wave is an admitted cohort, not a dependency edge. Admit another ready
issue whenever its own predecessors and conflicts are resolved and capacity
is verified. Treat an explicit sequence as waves containing exactly one issue.
Record a whole-wave barrier only for an explicit user instruction or a named
shared contract/integration gate with its actual members and reason.

1. Initialize controller state before dispatch:
   - Controller thread id.
   - Project objective and completion criteria. Keep these in controller state by default; project execution is not a request to enable tool-managed goal auto-continuation. Use a goal tool only when explicitly requested and permitted by its active contract. Do not mark an existing goal complete or blocked merely to idle; follow its status rules.
   - If the id is not directly available, use supported thread listing/reading and creation context to resolve it unambiguously. Apply the canonical naming contract when title control is available; a matching title alone does not establish identity.
   - Dependency graph with edge reasons, admitted cohort, and any explicit sequence or shared barrier with its authority/reason and members.
   - Per-issue state: `Pending`, `Dispatched`, `StackReady`, `AwaitingAuthorizedMerge`, `MergedAwaitingTestDeploy`, `MergedAwaitingHumanAcceptance`, `Merged`, `Blocked`, or `Stopped`.
   - Resolved branch strategy: policy source, scope, upstream, issue PR base, temporary branch, promotion target, and aggregate PR state; selected stack trunk/layers, exact predecessor pins, owners and per-edge development gate.
   - Delivery mode and project-level skipped/unverified entries.
   - Issue route (envelope and requested binding), worker thread id or queued creation handle, retry count, observed binding and separate fallbacks, escalation budget and used counts, PR URL, merge commit, validation result, and blocker.
   - Per-worker closeout: `pending`, `complete`, or `retained with accepted handoff`, with the cleanup evidence and any follow-up owner below; independent of per-issue merge state.
   - Per-issue merge executor and any source-bound exception, including exact target, next owner/action and wake condition for `AwaitingAuthorizedMerge`; that state does not satisfy a merge barrier.
   - Worker/external-gate health and due checks under [controller recovery](controller-recovery.md#existing-state-and-check-results), separate from merge evidence and capacity.
   - Naming context: verified parent issue or scope label, assigned issue, requested worker name and observed title (or unknown). Preserve it on resume and in bounded descendant handoffs.
   - A `dispatched` marker for every issue to prevent duplicate thread creation.
2. Dispatch every currently ready issue once through Fresh Thread Handoff and its routing step. Key the worker registry by Linear issue ID and record the creation receipt immediately; a routing result alone does not mark the issue `Dispatched`.
3. After the ready wave is dispatched and its wake path is verified, save controller state and end the turn when only external progress remains. A callback wakes the same controller. Ending an idle turn leaves project ownership and unfinished barriers intact.
4. On a callback or a heartbeat, apply Wake Strategy below before expanding reads:
   - Start from compact status and the callback for the affected worker; read detailed history only for an unresolved gate, blocker or health signal. Workers own implementation, tests and review; ordinary progress does not transfer those phases to the controller.
   - For a due recovery check or an actionable signal, inspect the necessary live Linear/GitHub/CI/base evidence. Before accepting a merge or opening a barrier, verify all required live evidence; do not replay the complete merge checklist on every healthy progress-only wake.
   - Update the matching registry entry.
   - Re-evaluate all pending issues against their own predecessors, recorded conflicts/barriers and observed capacity, not only the reporting worker or its cohort.
5. Mark each issue's merge barrier satisfied only when it is verified `Merged`
   on the recorded landing destination under the selected mode: the resolved
   issue PR base for ordinary work, or the native stack trunk for a stack layer.
   Verify each layer's reviewed head, merged PR and resulting trunk commit under
   the stack contract; do not require an upper layer to land on its predecessor
   branch. A recorded whole-wave barrier requires all its named members; other
   ready issues need not wait for that cohort. Apply the mode contract's
   [unattended validation precedence](../../dev/references/development-mode-contract.md#unattended-validation-and-deferred-acceptance):
   require the recorded waiver and remaining automated evidence; separate human
   acceptance tickets are not coding workers or barrier prerequisites. For a
   batch child with no required
   branch deployment, an explicit not-applicable environment result satisfies
   the environment portion; batch-only verification remains at promotion. Fast
   mode may accept verified landing after its skipped/unverified scope is
   recorded in controller state even when optional verification or acceptance
   was skipped; `MergedAwaitingTestDeploy`, thread completion, an open PR, green
   CI without merge, or an unsupported claim is never sufficient.
6. Before dispatching unlocked successors, re-read controller state and live
   issue/PR state. Ordinary merge edges require `Merged`; a selected native
   stack development edge can use a verified `StackReady` predecessor under
   the [stack contract](../../dev/references/stacked-prs.md). Keep explicit
   sequence, deployment and other required gates. Dispatch only `Pending`
   issues whose actual edges pass and which have no existing active owner/PR.
7. Admit the newly ready issues exactly once through the same Fresh Thread Handoff and per-issue routing step, then wait again.
8. A Review scope/budget handoff follows the [controller disposition after exhaustion](../../dev/references/review-lifecycle.md#controller-disposition-after-exhaustion), keeping its plan identity, counts and references in the registry; the retry allowance below cannot restart that loop. For other recoverable failures, if a worker reports `Blocked` or fails the resolved-base merge/test handoff, keep dependent issues closed. Resume the same worker with its existing branch, worktree, PR, checks, and evidence for up to five total attempts; waiting on deployment, outcome verification or human acceptance is not an attempt. Mark the project `Stopped` after attempt five and report the blocked downstream issues.
9. Run the integration checkpoint at the time the
   [branch strategy's row](../SKILL.md#integration-checkpoints) sets. Record its
   explicit PR set, ownership and callback, and verify its outcome. Do not mark
   batch execution complete before promotion and final handoff gates pass.
10. Complete the project only when all required issues are verified `Merged` under the selected mode, each worker closeout is accepted under Cleanup Acceptance below, and any planned integration checkpoint passes.

### Cleanup Acceptance

For a merged callback, consume the per-resource
[cleanup evidence](../../dev-merge-handoff/SKILL.md#cleanup-evidence) and verify
it against the exact issue head/worktree on the owning executor. An inaccessible
executor is unverified, not evidence of absence. Keep the result in the existing
worker registry rather than creating a second tracking artifact.

A callback containing only `merged`, issue Done or a merge SHA leaves closeout
`pending`. Resume the same worker at cleanup to supply missing evidence; do not
restart implementation, reviews or merge. A concrete unsafe/failed cleanup
keeps `merged with cleanup blocker` and its next action/owner visible. Accept
closeout as `complete` only with verified cleanup, or as `retained with accepted
handoff` when the retention boundary, remaining resources, reason and follow-up
owner are explicit and accepted by that owner. Merely naming an owner is not
acceptance and does not grant deletion authority.

Verified code integration may still satisfy the existing mode-required
wave/sequence dependency barrier while cleanup is pending; it does not complete
the worker or project. Carry cleanup follow-up alongside successors without
consuming implementation-repair attempts or creating another issue worker.
Respect an explicit user ordering requirement that includes cleanup. During worker replacement, transfer retained
follow-up explicitly; never leave competing mutators on its branch/worktree.

### Resume Authority

Carry the actual authorizing instruction and its scope when resuming a worker,
including any changed repair ceiling. Project retry attempts and Review's
accepted-repair count are separate; use the
[Review lifecycle ledger](../../dev/references/review-lifecycle.md#ledger)
for the latter. A progress question cannot be forwarded as a cap increase.
Retain the same worker, run and counters; a sent prompt is only a dispatch
receipt until the worker confirms the resumed phase. Report that distinction
without claiming that implementation is already running.

Use a delta handoff to the same owner: issue/thread, actual authority or changed
restriction and scope, current PR/base/head/worktree, accepted failure or changed
fact, next phase/action, cumulative attempts/Review history and evidence locators.
Retain unchanged routing and completed gates; do not send the initial handoff
again or repeat its full route. Name the callback destination and trigger if
changed. A correction supersedes only its stated scope; reconcile the old owner
before any transfer. No forwarded progress question expands a repair ceiling.

### Wake Strategy

Read [controller recovery](controller-recovery.md) before arming a wake path,
handling a callback/heartbeat or returning quietly. It owns stable prompts,
successful-check deadlines, worker/external-gate reconciliation and the host
failure boundary. Use one saved cursor/signal/deadline across all wake sources;
recovery alone does not open a merge barrier or transfer issue ownership.

### Barrier Example

For an explicitly requested whole-wave barrier or a recorded shared gate:

```text
Wave 1: EX-101, EX-102, EX-103, EX-104
Barrier: all four verified merged
Wave 2: EX-105
Barrier: EX-105 verified merged
Wave 3: EX-106, EX-107
Barrier: both verified merged
Wave 4: EX-108, EX-109
```

In normal mode, if only EX-101 is a predecessor of EX-105, its verified merge
can unlock EX-105 while another admitted worker remains active, provided actual
conflicts and capacity allow it. Planning them in adjacent waves adds no edge.

## Worker Handoff Shape

Use the same compact contract for waves and sequences; scheduling changes
dependencies, not delivery ownership. Put task-specific facts, source-bound
exceptions and source locators in the prompt. Keep shared Skill instructions,
other workers' history and changing project progress in their existing sources.
Do not impose an arbitrary length limit or omit a necessary environment boundary.

Pass the shared discovery inventory under the
[discovered-work rule](../../dev/references/execution-ownership.md#autonomous-decisions-and-discovered-work).
Workers return new findings to the controller for grouping and scope decisions;
they do not start out-of-scope work. Report a development blocker promptly;
nonblocking discoveries can accompany the next normal callback.

```markdown
Use $dev.
Mode: <fast | standard | strict; standard by default>.
Skipped / Unverified: <entries or none>.

Identity: <project/parent, issue, controller ID, naming context and worker ID when ready>
Target: <repository/worktree/branch, resolved base and branch-strategy policy/scope>
Scope/design: <accepted issue/spec/design revision and readable locators; settled decisions>
Dependencies/integration: <satisfied prerequisites, remaining gates, shared-area coordination>
Environment/boundaries: <owned resources, protected targets and task-specific restrictions>
Authority/merge: <source and covered scope; issue worker by default or explicit executor/release condition>
Validation/API: <mode-selected gates and source-bound additions; API Steward if applicable>
Routing: <routed envelope and requested binding for this issue>
Runtime acceptance: <pending/observed/unknown, separate fallbacks>
Discovery inventory: <existing shared parent/locator, or none>
Completion/callback: <verified merge plus closeout, stack-ready checkpoint or source-bound held merge gate;
  controller ID, supported transport, durable packet destination and concrete blocker triggers>

Own this issue through $dev, preserving its implementation/Review boundaries,
cumulative budgets and the recorded merge executor. Commit and push working
steps to the issue branch; report a risk of unpreserved local work. Send the
callback after verified merge/closeout, a recorded external merge handoff, a
selected stack-ready checkpoint, or a blocker/decision requiring controller
action. Keep ordinary progress in this worker.
```

## Worker Callback Packet

Require every issue worker to send this packet to the controller through the
handoff's transport and packet destination:

```markdown
Dev project worker callback
- Issue / worker / attempt: <issue ID, worker session ID, correlation ID and attempt number>
- Status: <stack-ready | merged | merged with cleanup blocker | merged awaiting test deploy | merged awaiting human acceptance | awaiting authorized merge | blocked>
- PR / head / merge: <PR URL, base, reviewed head and merge commit, or none; for a stack layer its immediate base and pinned predecessor>
- Evidence: <locators for validation, the Review result bound to that head (or the authorized omission and its source), the merge/test handoff and per-resource cleanup>
- Skipped / Unverified: <entries or none>
- Blocker or next action: <blocker and attempted fix; or the held gate's owner, action, authority and release condition; Review recovery state when active; retained cleanup and its owner; none when complete>
- Discoveries: <originating issue, evidence, proposed blocking status and ticket/comment anchors, or none>
```

Treat the packet as a claim. Verify it against live Linear, GitHub, CI and
base-branch state before updating the registry. When Review is required, the
accepted result must cover the policy minimum and bind to the PR head that was
merged, not a squash or rebase merge commit; retain the barrier for missing,
stale or self-assembled evidence, and otherwise verify the authorized omission
and its disclosure. Apply Cleanup Acceptance separately from the merge barrier,
then re-evaluate pending issues under Controller-Owned Wave Execution. A
stack-ready callback opens only its development gate: it has no merge commit,
leaves closeout pending and never marks the issue Done.
