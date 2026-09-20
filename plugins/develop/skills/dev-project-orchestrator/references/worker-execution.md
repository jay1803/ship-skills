# Project Worker Execution

Read before dispatching, resuming, or accepting issue execution in any scheduling mode. For sequence scheduling, also read [sequence-mode.md](sequence-mode.md).

## Fresh Thread Handoff

When this skill needs a fresh issue thread:

1. Use the resolved executor's persistent controller/session entry directly.
   - For Codex, discover and use the create-thread tool. For Claude Code, discover the native background-session or configured Axis entry through the [Claude adapter](../../agent-routing/references/claude-code-adapter.md#discover-the-actual-session-surface), and verify its creation and management receipts. Do not launch an ad-hoc provider command that bypasses the selected adapter or worker registry.
   - Create one new user-owned, user-visible controller thread or session per ready issue in the current project scope. Dispatch every member of the same safe wave before waiting.
   - When the user requested execution through this skill, that request already supplies the required authorization for these issue-worker threads; do not pause for redundant confirmation.
   - Classify the whole issue before creation. Choose `controller/standard`, `controller/deep`, or `controller/critical` with `standard` as the minimum; full lifecycle ownership gives every issue controller a `high` reasoning floor but does not force critical capability or `xhigh`. Apply the resolved adapter's permitted model/effort parameters, including its visible-task default-selection rule.
   - Publish the shared routing request before creation. Record queued acceptance as pending; at the first ready/active observation apply the adapter's binding verification and update the resolved notice. Include the actual request, observed binding or explicit unknowns, and required routing receipt in the handoff.
   - Use a local environment unless the user explicitly asks for a new worktree.
   - For an explicit worktree request, use the worktree environment and preserve requested branch or starting-state details when the tool supports them.
2. Include the controller thread/session id and worker callback packet in the initial prompt. Resolve the controller id with the executor's management tools; do not guess when multiple workers could match.
3. Use the worker handoff as the new thread's initial prompt without adding summaries, hidden instructions, or extra commentary.
4. Record the returned worker thread/session id and resolved executor against the issue before creating another worker or yielding.
5. Do not execute a worker payload in the controller thread after its fresh worker was created.
6. After dispatching the complete ready wave, report all worker ids and enter the Controller-Owned Wave Execution workflow.
7. If direct worker callbacks are unavailable, continue with controller heartbeat monitoring instead of decentralizing successor dispatch.
8. If the current project id is unavailable and the thread tool cannot infer it, ask one short question for the target project instead of falling back to a projectless thread.
9. If persistent worker creation remains unavailable after entry discovery or an attempted creation, report the limitation and enter Serial Inline Fallback in the invoking controller. Do not spawn a bounded sub-agent to impersonate a persistent issue controller.

## Serial Inline Fallback

Use this path only after persistent worker creation is confirmed unavailable.
It preserves the complete project queue while limiting execution in the current
session to one issue lifecycle. It takes precedence over dispatching every ready
member of a wave; a free sub-agent slot is not a free issue-controller slot.

Keep this compact record in existing controller state, not a new registry:

- `execution_mode: serial-inline` and the session-creation failure/discovery
  evidence; unresolved creation remains pending instead of entering fallback.
- `active_issue`, the current controller identity, and `worker_session: none`.
- The active issue's phase, branch/worktree, PR and current head, pending gates,
  and bounded helper IDs with their scoped tasks and status.
- Remaining issues and the verified condition that allows the next one to start.

Before starting issue work, dispatching any helper, or resuming after a callback,
interruption or compaction, reconcile that record with current issue, PR and
helper state. Missing state requires read-only reconstruction, not a new issue.
Only the active issue may enter issue-specific research, implementation, review,
repair or validation. Project-wide read-only dependency/status checks remain
allowed; they do not start a successor lifecycle.

Bounded helpers may work on the active issue under the existing one-writer and
review-independence rules. Their completion returns an artifact to the inline
`$dev` owner; it does not complete the issue or authorize successor dispatch.
Waiting for helpers, review, CI, repairs, test deployment or required acceptance
keeps `active_issue` occupied. A green CI result, open PR, or stopped reviewer
cannot release it. Apply the same delivery-mode gates as normal issue workers;
fallback does not combine review roles or waive a gate.

Advance only after the current issue satisfies the existing mode-required merge
and handoff barrier, all its helpers have finished or are confirmed stopped,
and the completion evidence is recorded. Then clear `active_issue` and select
the next eligible issue. A blocker uses the existing retry/stop policy and does
not open a slot for unrelated issue execution. An explicit user scope change
may stop or reassign work; record that transition without calling it completed.

If resume reveals several unfinished inline issue lifecycles, do not launch
more work or erase their branches, PRs, results or review generations. Record
the overlap, preserve returned artifacts, and quiesce outstanding helpers using
supported controls before resuming one issue. Keep other issues explicitly
paused; if a helper cannot be confirmed quiescent, report that blocker. Choose
the active issue from the user's order and verified dependencies, then resume
its pending gate. Do not restart discovery or silently mark paused issues done.

When persistent sessions become available later, verify an accepted session
handoff and stop inline ownership of that issue before switching execution
mode. Do not run both owners for the same issue.

## Controller-Owned Wave Execution

Use this state machine for normal project batches and sequence mode. Treat a sequence as waves containing exactly one issue.

1. Initialize controller state before dispatch:
   - Controller thread id.
   - Project objective and completion criteria. Keep these in controller state by default; project execution is not a request to enable tool-managed goal auto-continuation. Use a goal tool only when explicitly requested and permitted by its active contract. Do not mark an existing goal complete or blocked merely to idle; follow its status rules.
   - If the id is not directly available, give the controller a unique project-specific title, then use the thread listing and reading tools to resolve it unambiguously.
   - Ordered dependency graph and wave membership.
   - Per-issue state: `Pending`, `Dispatched`, `MergedAwaitingTestDeploy`, `MergedAwaitingHumanAcceptance`, `Merged`, `Blocked`, or `Stopped`.
   - Resolved branch strategy: policy source, scope, upstream, issue PR base, temporary branch, promotion target, and aggregate PR state.
   - Delivery mode and project-level skipped/unverified entries.
   - Worker thread id, retry count, requested semantic route/capability/reasoning/profile/model/executor/profile-fallback policy, accepted binding and separate fallbacks, PR URL, merge commit, validation result, escalation, and blocker.
   - A `dispatched` marker for every issue to prevent duplicate thread creation.
2. Dispatch every currently ready issue once. Key the worker registry by Linear issue ID and record the thread id immediately.
3. After the ready wave is dispatched and its wake path is verified, save controller state and end the turn when only external progress remains. A callback wakes the same controller; it does not authorize the worker to dispatch another issue. Ending an idle turn leaves project ownership and unfinished barriers intact.
4. On a callback or a heartbeat, apply Wake Strategy below before expanding reads:
   - Start from compact status and the callback for the affected worker; read detailed history only for an unresolved gate, blocker or health signal. Workers own implementation, tests and review; ordinary progress does not transfer those phases to the controller.
   - For a due recovery check or an actionable signal, inspect the necessary live Linear/GitHub/CI/base evidence. Before accepting a merge or opening a barrier, verify all required live evidence; do not replay the complete merge checklist on every healthy progress-only wake.
   - Update the matching registry entry.
   - Re-evaluate the entire active wave, not only the reporting worker.
5. Open a barrier only when every issue in the active wave is verified `Merged` into the resolved issue PR base under the selected mode. Standard mode applies the unattended validation waiver: real-environment tests and human acceptance labels do not hold engineering barriers open; require the recorded waiver and remaining automated evidence. Separate human acceptance tickets are not coding workers or barrier prerequisites. For a batch child with no required branch deployment, an explicit not-applicable environment result satisfies the environment portion; batch-only verification remains at promotion. Fast mode may treat a base-merged issue as `Merged` after its skipped/unverified scope is recorded in controller state even when optional verification or acceptance was skipped; `MergedAwaitingTestDeploy`, thread completion, an open PR, green CI without merge, or an unsupported claim is never sufficient.
6. Before dispatching unlocked successors, re-read controller state and live issue/PR state. Dispatch only issues still `Pending` with all hard predecessors `Merged` and no existing worker, branch, or PR that represents active work.
7. Dispatch the newly ready wave exactly once, then wait again. Never let workers decide that they were the last finisher.
8. If a worker reports `Blocked` or fails the resolved-base merge/test handoff, keep dependent issues closed. Resume the same worker with its existing branch, worktree, PR, checks, and evidence for up to five total attempts. Mark the project `Stopped` after attempt five and report the blocked downstream issues.
9. For temporary batch integration, run combined validation and the aggregate promotion PR after all required child barriers pass, following the canonical branch strategy. Do not mark batch execution complete before promotion and final handoff gates pass.
10. Complete the project only when all required issues are verified `Merged` under the selected mode and any planned integration checkpoint passes. Fast mode additionally requires project state and final reporting to contain every skipped/unverified item.

### Resume Authority

Carry the actual authorizing instruction and its scope when resuming a worker,
including any changed repair ceiling. Project retry attempts and Review's
accepted-repair count are separate; use the
[Review state contract](../../dev/references/dev-review-v2-contract.md#repair-and-re-review-state)
for the latter. A progress question cannot be forwarded as a cap increase.
Retain the same worker, run and counters; a sent prompt is only a dispatch
receipt until the worker confirms the resumed phase. Report that distinction
without claiming that implementation is already running.

### Wake Strategy

- Use worker-initiated callbacks as the primary wake path: include the controller id, supported messaging tool and Worker Callback Packet in every handoff. Workers report a verified merge or a concrete blocker/decision requiring controller action promptly; ordinary commits, CI transitions and progress commentary do not need a separate wake. Confirm the transport can reach the original controller before relying on it; the heartbeat is backup for missed callbacks, silent exits and external merges.
- Fix the wake predicate before arming recovery, because the rest of this section depends on what counts as actionable. A wake needs controller action when a barrier input changed (a verified merge into the resolved issue base, a received callback, or a worker that exited, stopped, or is blocked), or when missing signals, uncertain worker health, or a due recovery check require reconciliation. Recovery work does not itself open the barrier. A pushed commit, a new PR head, a CI transition, and a changed progress message are worker progress, not controller work; they leave the barrier where it was. When signals are healthy and recovery is not due, record progress-only wakes as quiet, keep the consecutive-quiet count running, and do not treat progress as evidence that the current interval is earning its cost.
- On Claude Code, verify the callback transport before dispatch and always name an external callback record (the assigned Linear issue, or the PR) in the handoff; the worker writes the same packet there as the packet of record and native messaging is only the wake signal. Read the [Claude communication reference](../../agent-routing/references/claude-communication.md#external-callback-record) for the record and heartbeat limits.
- Prefer a terminal-condition watcher to a fixed interval only when the runtime supports background execution, completion notification, and waking the same controller after its turn ends, with verified receipts for that path: the controller dispatches it, ends its turn, and is woken once when the watcher observes a merge, a worker exit, or the callback record. Polling then happens outside the model, so a quiet hour costs no wakes. Keep a long-interval heartbeat as the residual net for the watcher itself dying with its session, and say which mechanism owns which signal in controller state. Shell command execution alone does not establish a wake path. For Codex, read the [controller wake capability boundary](../../agent-routing/references/codex-adapter.md#controller-status-and-wake-capabilities).
- Keep one heartbeat attached to the controller as backup while workers are active. With verified callbacks and healthy workers, start with a 45-minute recovery interval and back off toward 60 minutes after repeated quiet checks, within the recorded maximum missed-event recovery delay. Use a shorter interval when callbacks are unavailable, health is uncertain, or a user deadline requires faster detection; record that reason. A normal progress message does not restore a short interval. Direct callbacks remain immediate regardless of the backup interval. Record the job id, interval, last worker/callback cursor, last external-state check and next recovery check in the existing registry. Arm it per wave rather than once per project: before ending a turn that dispatched a wave, verify a heartbeat is active and re-arm one when an earlier wave's heartbeat was removed. Callbacks alone cannot report a worker that exits without sending one.
- Callbacks, heartbeat, user status requests and any already-authorized goal continuation consume the same saved worker cursor, signal identity and recovery deadline. Reuse a signal already processed in this wake cycle; do not read it again merely because a second wake source fired. A duplicate wake source is not a new recovery deadline or reason to reload unchanged Skills. Reuse loaded instructions and compact controller state unless context loss, a version change or a new pending decision requires the relevant source again. A quiet wake does not reset the recovery deadline: advance it only after the due external check actually completes. Keep freshness/health uncertainty actionable.
- On heartbeat or another reconciliation wake, first request missing compact worker status and callback changes since the recorded cursor, batching independent reads where supported. Follow the executor adapter's required record/status checks. A changed progress message alone need not trigger full thread-history reads. When signals are healthy and non-actionable and the external-state check is not due, save the cursor and end the turn with the runtime's required quiet response. Treat repeated quiet wakes as a wake-configuration defect rather than normal operation: after a few consecutive non-actionable wakes, widen the interval or narrow the wake predicate before ending the turn, and shorten the backup interval only when the recorded recovery need changes, not merely because progress resumed.
- Keep the heartbeat prompt stable: identify the controller, active scope, state location, wake predicate and authority boundaries. Store changing cursors, heads, test counts and logs in existing controller state. Update the automation only when its wave/scope, recovery policy, authority or lifecycle changes, or its recorded configuration is missing/stale; routine progress and quiet cursor updates do not require another automation write. Preserve notification policy; a quiet/DONT_NOTIFY response suppresses notification, not model execution.
- Check compact live PR/CI/issue signals at the recorded recovery interval even when worker status is unchanged: a missed callback or external merge may not change that status. If no reliable change cursor is available, perform bounded recovery reads instead of assuming nothing changed. Missing signals, stopped/failed workers, actionable callbacks, changed external state or expired verification require reconciliation. Two failures look like ordinary silence and need an explicit check: a worker that was accepted but never produced a first turn, because a queued or backgrounded creation receipt is not a running worker; and a worker that exited leaving commits only in its local worktree. Preserve unpushed work on the remote issue branch before resuming or re-dispatching that issue. Read detailed history only for the affected worker or unresolved gate; verify all required live evidence before changing barriers or dispatching successors.
- Prefer one supported wake mechanism for the same pending signal; reuse the existing heartbeat rather than creating one for each goal continuation. If an active goal runtime immediately replays idle turns and offers no supported pause/coalescing control, report that runtime limitation once and preserve the recovery schedule. Do not mark its goal complete/blocked just to suppress wakeups, infer permission to alter its budget, or claim the Skill repaired host scheduling.
- Do not chain short status waits or sleep calls to keep an idle controller turn alive. That ban is about holding the current turn open; it does not forbid a detached watcher that ends the turn and wakes the controller once when its terminal condition is met. A bounded wait is appropriate for a concrete in-flight operation, such as confirming worker creation, but return to the verified callback/heartbeat wake path once only external progress remains. Disable or remove the heartbeat when no workers are active, the project completes, or the project stops. A quiet heartbeat still consumes model tokens; do not describe this strategy as a measured token saving without a comparison.
- If neither callbacks nor heartbeat automation is available, report that automatic continuation is unavailable and ask the user to resume the controller. Do not transfer orchestration ownership to a worker.

### Barrier Example

```text
Wave 1: EX-101, EX-102, EX-103, EX-104
Barrier: all four verified merged
Wave 2: EX-105
Barrier: EX-105 verified merged
Wave 3: EX-106, EX-107
Barrier: both verified merged
Wave 4: EX-108, EX-109
```

## Worker Handoff Shape

For non-sequence project batches, send this shape to each issue-level worker in a fresh controller thread or session on the resolved executor by default:

```markdown
Use $dev.
Mode: <fast | standard | strict; standard by default>.
Skipped / Unverified: <entries or none>.

Project:
Controller thread:
Routing binding: <requested semantic route/capability/reasoning/executor/profile/model/profile-fallback policy plus accepted executor/model/reasoning/profile and separate fallbacks>
Routing receipt required: use the shared agent-routing receipt in the callback
Assigned issue:
Wave / batch:
Branch strategy: <policy source, scope, upstream, issue PR base, temporary branch, promotion target>
Base branch:
Dependencies already satisfied:
Assigned scope:
Accepted engineering ticket / design basis: <content and source/contract revision; reuse settled decisions under the engineering ticket protocol>
Expected touched areas:
Do not touch:
Validation required: <mode-selected checks; source for explicit additions; no automatic standard reverse-red or unrelated edge-case matrix; when the phase plan or repository policy requires technical Review, the combined Review V2 result accepted on the exact PR head to be merged; otherwise carry the mode/preset or explicit exception and its required omission disclosure>
Integration notes:
API Steward expectations:
Stop and report if:

Resolve exactly this issue through the $dev workflow. Commit and push each working step to the issue branch as you reach it; work that exists only in your local worktree is invisible to the controller and is lost if this session exits. After reaching a merged PR against the resolved issue base with its mode-required test handoff, or a concrete blocker, send the Worker Callback Packet to the controller thread. Do not create or dispatch successor issue threads.
```

## Worker Callback Packet

Require every normal-batch and strict-sequence worker to send this packet to the controller with the thread messaging tool:

```markdown
Dev project worker callback
- Project: <project>
- Issue: <issue id>
- Worker thread: <thread id>
- Routing receipt: <shared agent-routing receipt>
- Attempt: <number>
- Status: <merged | merged awaiting test deploy | merged awaiting human acceptance | blocked>
- PR: <number and URL, or none>
- Head branch: <branch>
- Base branch: <verified issue PR base>
- Batch / promotion state: <scope, temporary branch, promotion target, aggregate PR or pending>
- Validation / QA: <result>
- Merge/test handoff: <result>
- Review evidence: <combined Review V2 artifact identifier and the head it was accepted on, or `skipped (fast mode)`, `not selected (tracked-artifact)`, or `waived` with the applicable phase-plan/policy or explicit user authority; never call omitted Review passed>
- Human acceptance: <not required | required steps and evidence status | skipped (fast mode) with closeout disclosure>
- Skipped / Unverified: <entries or none>
- Merge commit: <commit, or none>
- Blocker and attempted fix: <details, or none>
- Integration notes: <notes, or none>

Controller action: verify this result against live Linear, GitHub, CI, and base-branch state; apply the recorded phase plan and repository policy: when Review is required, verify the accepted combined artifact and its binding to the PR head that was merged (not the squash/rebase merge commit), retaining the barrier for missing, stale, or self-assembled evidence; otherwise verify the authorized omission and its disclosure; update the full active-wave barrier; dispatch unlocked successors only if the barrier is satisfied.
```
