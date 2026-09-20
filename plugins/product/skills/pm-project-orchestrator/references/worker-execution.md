# Project Worker Execution

Read only when dispatching or resuming authorized issue workers.

## Worker Delegation

Run plan-only analysis inline or as a bounded project sub-agent. Keep execution-mode project control in the invoking user-owned thread so its worker registry, callbacks, waits, questions, and successor dispatch persist. When plan-only work is delegated, require the project brief, issue assignment plan, tracker writes applied or drafts, blockers, and open questions.

Use a fresh user-owned controller thread or session on the resolved executor for each persistent issue worker. It must be visible in that executor's supported task/session surface and recorded in the worker registry; an internal bounded sub-agent is not an equivalent substitute. For Codex, use the create-thread tool and set the Codex adapter binding explicitly. For Claude Code, use the configured runtime-native persistent session or Axis worker entry and set the Claude Code adapter binding explicitly. Check actual user authorization and the active creation tool contract for new
threads/sessions. Reuse valid existing authorization without asking again.
When new tasks are not authorized, execute serially inline with the same
issue-level ownership and verification boundaries. Use bounded agents only for disposable analysis, execution, or review, not as the owner of a long-running issue workflow; route each through the canonical contract and resolved adapter.

Each issue worker must receive one child issue ID, relevant project context, its earliest missing PM skill, hard predecessors, allowed child-issue writes, forbidden project writes, terminal states, and the controller callback target. The worker runs its own `$pm` chain serially and must not dispatch successors.

Start workers at the earliest missing prerequisite proven by issue evidence. Queue apparent specialist routes such as UX, UI, analytics, or technical boundary after that prerequisite; do not skip intake or another missing stage merely because the issue title reveals its eventual specialty.

When creation is authorized, consider persistent worker creation unavailable only after the resolved executor's controller/session entry cannot be found or an actual creation attempt fails. Then report that persistent parallel execution is unavailable and run issue workflows serially inside the invoking user-owned controller thread. Never use a bounded sub-agent or serial sub-agent as the persistent owner of an issue workflow, and never claim that the inline fallback is parallel execution.

### Worker Handoff

```markdown
Use $pm for <ISSUE-ID> as one worker in <PROJECT>.

Routing:
  semantic_route: <controller/standard | controller/deep | controller/critical>
  lifecycle: controller
  role: worker
  capability_tier: <standard | deep | critical>
  reasoning_depth: <high | xhigh>
  requirements: <tracker-read, tracker-write, network, and any others>
  permissions: external-write
  write_scope: <this child issue only>
  profile_fallback: <allowed | forbidden>
  executor_policy:
    mode: <auto | prefer | required>
    executor: <any | codex | claude-code>
    fallback: <allowed | forbidden>
    independent_from: none
Runtime binding: <requested and accepted executor, model, reasoning, and profile plus separate fallbacks from the active adapter>
Routing receipt required: use the shared agent-routing receipt in the callback
Start at: <$pm-next-skill>
Read: <project context and source links>
Hard predecessors: <IDs or none>
Allowed writes: <this child issue only>
Forbidden writes: project description, milestones, issue membership, project-level dependencies, or any other child issue

Continue the issue's required PM chain serially until one terminal result:
Ready | Done | Blocked | Split | Deferred | Rejected.

Return the PM Worker Callback to <controller thread>. Do not create or dispatch successor issue workers.
```

## Controller-Owned PM Waves

These dispatch steps apply only when persistent worker creation is authorized.
Otherwise use the invoking controller's serial inline path: retain per-issue state
and verify each result before advancing; do not call thread creation tools.

1. Initialize controller state before dispatch:
   - Project identifier and controller thread identifier.
   - Active goal, selection evidence, completion criteria, and successor goal when applicable.
   - Verified project brief, cutline, dependency/conflict graph, and ordered waves.
   - Per-issue route, controller state, terminal target, hard predecessors, and evidence.
   - Worker registry keyed by issue ID with worker thread/session ID, attempt, requested semantic route/capability/reasoning/executor/profile/model/profile-fallback policy, accepted binding and separate fallbacks, last callback, escalation, blocker, and handoff link.
   - A `dispatched` marker that prevents duplicate worker creation.
2. For authorized persistent dispatch, start every currently ready issue in
   the active wave once. Create one user-owned, user-visible controller thread
   or session per issue and record its worker ID immediately.
   - Resolve the controller thread or session identifier with the resolved executor's management tools; do not guess when several workers could match.
   - Create workers in the current saved project when possible and use a local environment unless the user explicitly requests isolation.
   - Classify the whole issue before creation. Choose `controller/standard`, `controller/deep`, or `controller/critical` with `standard` as the minimum; full lifecycle ownership gives every issue controller a `high` reasoning floor but does not force the critical model tier. Set model and reasoning explicitly from the resolved adapter.
   - Publish the shared routing request before creation and the resolved routing notice immediately after the thread tool accepts each worker. Include the accepted binding and required routing receipt in the handoff.
   - Include the exact Worker Handoff and controller callback target in the worker's initial prompt.
   - If persistent worker creation remains unavailable after entry discovery or an attempted creation, report the limitation and switch to the inline serial fallback in the invoking controller. Do not spawn a bounded sub-agent to impersonate a persistent issue controller.
3. Dispatch the complete safe wave before waiting. Never execute a dispatched worker payload again in the controller thread.
4. Wait for callbacks or use bounded thread-status waits. A callback wakes the controller; it never authorizes the worker to dispatch a successor.
5. On every callback:
   - Read the worker result and verify live child-issue state and artifacts.
   - Update the worker registry and issue state.
   - Apply only controller-owned project writes or accepted split/dependency changes.
   - Re-evaluate the full active wave and all newly affected successors.
6. Open the wave barrier when every issue in the active wave reaches a verified terminal state. Keep successors of `Blocked` or unresolved `Split` issues closed, while allowing unrelated branches of the graph to continue.
7. Before dispatching the next wave, re-read live project and child-issue state. Reuse an existing worker thread for recoverable continuation; never create a duplicate worker for active work.
8. Batch blocking user questions at the controller when possible. Do not let multiple workers ask overlapping questions about the same project decision.
9. Complete only when every in-scope issue is `Ready`, `Done`, `Blocked`, `Deferred`, or `Rejected`, and every `Split` issue's accepted children have been inventoried and scheduled or explicitly deferred.
10. Hand the ready set to `$dev-project-orchestrator` with PM dependencies and execution constraints. If required v1 issues remain blocked, label the handoff partial or keep Dev handoff blocked instead of claiming project readiness.

### PM Worker Callback

```markdown
PM project worker callback

Project: <project>
Issue: <ISSUE-ID>
Worker: <thread/session id and resolved executor>
Agent routing: <requested route and executor policy plus actual executor/model/reasoning/profile binding>
Routing receipt: <shared agent-routing receipt>
Starting route: <$pm-skill>
Terminal state: <Ready | Done | Blocked | Split | Deferred | Rejected>
PM route completed: <skills run in order>
Sources read: <links or issue comments>
Artifacts produced: <links or concise list>
Tracker writes: <applied or drafts>
New/split issues: <IDs, drafts, or none>
Blocker or open decision: <specific blocker or none>
Project-level recommendation: <controller-owned update or none>
Controller action: <verify, update graph, dispatch next wave, or stop>
```

