# Executor Sessions

Read when creating, resuming or replacing a persistent issue worker, choosing
its callback or wake transport, diagnosing a failed dispatch, or accepting a
model or effort escalation. Follow the actual tool schema: CLI, desktop and
hosted surfaces need not expose the same capabilities. A transport or session
mechanism changes delivery, not issue ownership or permission, and a
cross-session message never grants user approval.

## Escalation Budget

The controller owns each delegated task's adjustment budget: by default one
effort adjustment and one capability escalation, kept with their used counts in
the worker registry and handoffs. Count from the routing result's `adjustment`;
a capability escalation includes its destination's floor effort, and raising
effort beyond it also counts as an effort adjustment. Counters belong to the
task across models, sessions, retries and availability substitutions, so a
stronger model, a renamed task or a new session never resets them. On resume,
recover them from prior evidence; unknown history grants no fresh allowance,
and a stricter supplied limit wins. Neither allowance requires using the other
first.

Verify new evidence before accepting an adjustment and select the required tier
directly. Once the needed allowance is spent, return a concrete blocker; raising
the budget is an explicit controller decision within existing authority and
cost limits. Carry the artifact, attempted checks, failure evidence and open
question into an accepted stronger attempt. Missing credentials, unavailable
infrastructure and ambiguous external-write outcomes need diagnosis, not
escalation. A model or effort choice is the controller's decision from the
routing contract; ask a human only when an explicit user instruction about the
budget or binding requires it.

## Accepted Escalation Handoff

The executing worker reports the evidence and requested adjustment to its owning
controller; it does not rebind itself or dispatch its successor. The controller
accepts a supported route and preserves issue, target, WIP, validation and
Review state, pending operations and ownership.

Prefer a supported stronger next-turn resume of the same persistent issue
session after the current writer reaches a safe checkpoint; active-turn steering
is not a model change. When the control surface cannot rebind the agent, confirm
the old writer and its mutating descendants and background work stopped before
a replacement receives that exact checkpoint. Keep the persistent issue owner
when replacing only a bounded implementer; read-only stronger analysis need not
replace either. A standalone issue owner can use authorized stronger bounded
analysis; changing its own active binding still needs a supported external
resume control or the precise human or runtime action.

- **Codex chat:** when the existing-thread follow-up or resume tool permits
  `model` and `thinking`, end the active execution safely and start the next
  turn on the same chat with the accepted values and checkpoint. A prompt saying
  "use max" is not a changed inference setting.
- **Bounded follow-up without a binding override:** preserve the checkpoint,
  verify the writer, descendants and background mutations stopped, then spawn
  the replacement with explicit permitted model and effort.
- **Unsupported or rejected rebind:** a concrete execution boundary. Use
  single-owner recovery only after proving the old owner quiescent; otherwise
  hold the phase and request the missing control or decision.

Record requested, accepted and observed bindings separately; an unexposed value
remains unknown, not proof the upgrade happened.

## Dispatch Failure Diagnosis

When an assignment fails before the child completes, diagnose the failed layer
before retrying or changing the route, especially across hosts. Read
controller-side acceptance and target-side status separately:
`dispatch_rejected` (the controller or API refused), `transport_unreachable`,
`runtime_unavailable` (the target could not accept the binding),
`provisioning_failed`, `child_failed`, or `observability_gap`. Report the
smallest repair and whether it applies to the controller host, the target or
both. Retrying within the task needs no renewed approval once ambiguous outcomes
are resolved; keep explicit restrictions and the selected binding policy.

## Codex Status And Wake

- `wait_threads`, where available, gives compact status: batch targets and carry
  each returned cursor as `afterCursor`. `timeoutMs: 0` is an immediate
  snapshot; a bounded wait can confirm an in-flight dispatch. A timeout or
  unchanged commentary is not completion. Read detailed history only for the
  affected blocker, missing callback or unresolved gate. For a healthy idle
  reconciliation take at most one compact snapshot per target; do not chain
  45–55 second waits on the same cursor to keep a turn alive.
- A wait does not subscribe anything after the turn ends. Once only external
  progress remains, save cursors and rely on the verified callback and the
  task-attached heartbeat, reusing existing automation instead of adding a
  poller.
- Workers send their completion or blocker packet through the supported task
  messaging tool (for example `send_message_to_thread`). The callback is the
  primary wake and the longer heartbeat the backup; do not ping healthy workers
  because a status wait timed out.
- An authorized goal continuation shares the same cursor and recovery deadline.
  Reuse a signal already checked this cycle and end when no controller action
  remains; do not add a heartbeat or chain waits to fill the goal turn. If the
  host immediately starts another goal turn, report its missing pause or
  coalescing capability once.
- Use a detached terminal-condition watcher only with evidence that its
  completion can wake the same controller after the turn ends; a shell PID,
  exec session or pollable output is not that evidence.
- Without a supported callback or automation, disclose that automatic
  continuation is unavailable; saved state enables later recovery but does not
  schedule it. Never replace a persistent issue task with a bounded agent to get
  different wake behavior. A delivered heartbeat is not proof that its turn or
  health check succeeded; read exposed turn errors.

## Claude Sessions

### Discover The Actual Session Surface

An issue owner needs a runtime-native persistent session or configured worker
entry (such as Axis, under its own contract) that returns a session identity,
appears as a separate user-owned session and supports read, status and
continuation. Check the installed runtime's help and callable tools before
declaring creation unavailable. `claude --bg` is a session entry, not `Agent`
with a background flag. Do not bypass a required executor, host or worker entry
with a local CLI launch.

| Operation | Native entry and evidence |
| --- | --- |
| Create | `claude --bg --name <unique-name> --model <full ID> --effort <level> -- <handoff>` returns a short background ID |
| Identify/status | `claude agents --json --all --cwd <directory>` exposes background ID, full `sessionId`, directory, process and lifecycle state |
| Read | `claude logs <background-id>`; `claude attach <background-id>` opens the conversation |
| Continue live | Native `ListAgents` / `SendMessage` where registered, or the attached conversation |
| Stop | `claude stop <background-id>` keeps the conversation; re-read status before transferring ownership |
| Resume stopped | `claude --bg --resume <session-id> -- <follow-up>`; verify the returned identity |

Record the background ID, full session ID, observed directory, accepted binding
and creation receipt in the registry; a display name is only a label. Pending
creation is not an active controller: resolve it before retrying so an accepted
but unobserved session cannot duplicate ownership. Verify the branch and
worktree before writes; separate sessions do not prove filesystem isolation.
Put `--` before the positional handoff, and treat an empty idle session as
undelivered. Resume with saved options: repeating configuration flags or
resuming a running session can create a copy, which is not an accepted
replacement. A missing transcript or fresh restart is not restored state;
reconstruct issue, branch, PR and pending gates first.

### Callback Transport

Before the first worker, verify the controller session's own callback transport
and record it as `callback_transport`; it depends on how the session started,
not the runtime version.

1. Record `native-messaging` only after confirming `SendMessage` is a callable
   tool in this session through the tool listing or deferred-tool search.
   `ListAgents` alone is not proof.
2. The desktop app's session-management `send_message` is a hand-off for a
   person reading another session and cannot reach unattended sessions; its
   presence is `ineligible` evidence.
3. The worker handoff tells the worker to make the same check at start and, when
   `SendMessage` is missing, to deliver its callback through the
   [external callback record](#external-callback-record). A worker that finishes
   with neither is `callback: undelivered`, which the heartbeat detects.

Discover peers through `ListAgents` and message only assigned workers and the
controller. An accepted send does not prove the recipient processed it.
When messaging is unavailable, held or refused, record that boundary rather than
changing permission settings. Idle, completed, stopped and callback-received
states are not merge or acceptance evidence.

| Transport | Selection boundary |
| --- | --- |
| External callback record | Always written by the worker on merge, held merge or blocker; the only path without native messaging |
| Native cross-session messaging | Default wake once `native-messaging` is verified on both sides |
| Agent Teams messaging | Existing team-scoped bounded collaboration; team lifetime is not issue persistence |
| Desktop `send_message` | Ineligible |
| Direct file mailbox | Experimental fallback when native messaging is technically unavailable and the checks below pass |
| Native status/read/attach plus heartbeat | Standing recovery while workers are active |

Resolve the wake transport in that order within the required lifecycle. Never
switch transport to evade a permission denial, refusal, policy filter or missing
authority, and do not change permission settings or experimental flags as a
fallback. Record the mode, its reason, both session identities and pending
message IDs; test a nonce round trip before relying on a new channel, and do not
resend a possibly accepted command elsewhere before reconciling it.

### External Callback Record

The assigned Linear issue (or the PR when no issue exists) carries every Worker
Callback Packet, for Codex and Claude workers alike.

1. The handoff names the record target, the controller session ID and a
   per-dispatch correlation ID. The worker writes the complete packet as one
   comment, keeping `Dev project worker callback` as its first line and the
   correlation ID, worker session ID and attempt number for deduplication.
2. With `SendMessage` registered, the worker also sends a short wake carrying
   only the issue and correlation IDs; the comment is the packet of record.
3. On every wake the controller reads callback comments newer than the
   registry's `last_callback_seen`, keys them by correlation ID, records queued,
   received and applied separately, and processes each once.
4. A comment is a claim. Verify live PR, CI, base merge and Linear state before
   updating a barrier; a Linear state change alone is not a callback.
5. A worker that cannot write the comment reports that blocker through any
   remaining transport and stops; the heartbeat reads `claude logs`. It never
   writes to a target the controller did not name.

Probe the record path with a harmless nonce comment on first use in a project.

### Claude Heartbeat

- The controller must be a live interactive session; a `-p` controller exits
  before callbacks or heartbeats fire, and `--bg` workers cannot host their
  controller's heartbeat.
- `CronCreate` fires only while the controller is idle, lives only in session
  memory (gone on exit, not restored by `/resume`) and a recurring job expires
  after seven days. Keep one armed while a wave is in flight at the controller's
  recovery interval, delete it with `CronDelete` only when nothing unfinished
  needs this wake, and re-create it after a resume or a later dispatch.
- `ScheduleWakeup` exists only inside `/loop` dynamic mode.
- `Monitor` wakes on events from a polling script: emit on every terminal state
  (including a stopped or failed worker), poll remote APIs no faster than every
  30 seconds, suppress unchanged alerts, bound it to a wave and end it with the
  session.
- Prefer a detached terminal-condition command when the runtime verifies
  background completion can wake the idle controller, keeping a long cron only
  as the net for a watcher that dies.

On each wake: list workers with `claude agents --json --all --cwd <directory>`,
read `claude logs` for any exited worker without a recorded callback, read the
external callback record, verify live Linear, GitHub and CI state, then
re-evaluate the whole active wave. Record the heartbeat tool, interval, creation
time and job or monitor ID. With no heartbeat and no messaging, report that
automatic continuation is unavailable; never hand orchestration to a worker.

### Direct File Mailbox Fallback

A version-sensitive local path, not a message bus. The receiver must already be
a live Claude session whose runtime consumes the mailbox.

1. Resolve the target from its accepted session receipt and status; read the
   runtime-created team's `config.json` only to correlate `leadSessionId` and
   the member. Do not guess names, manufacture a team, edit runtime config or
   write sockets or membership registries.
2. Use `~/.claude/teams/<observed-team>/inboxes/<receiver>.json` under the
   sender's real identity.
3. Verify the installed plain-message schema with a harmless probe and require a
   correlated reply, not just a changed file or `read` flag.
4. Use the runtime's writer or lock when available; otherwise write only to a
   verified drained inbox with one coordinated sender. Stop on an unread entry,
   changed snapshot, unknown writer or malformed file.
5. Write a complete JSON array through a same-directory temporary file and
   atomic rename, only to the exact inbox and never through a symlink.
6. Carry a unique message ID and correlation ID; the receiver echoes them with
   its identity, and processed IDs live in existing state so duplicates repeat
   no side effect.
7. Wait for the correlated reply; without a live consumer, safe writer or reply,
   keep the owner and fall back to status, attach and heartbeat.

The envelope observed on Claude Code 2.1.263 is an array of
`{"from", "text", "summary", "timestamp", "msgV": 1, "msg_id", "type": "message", "read": false}`
objects (not JSONL); preserve optional runtime fields. Send plain text only,
never approvals, shutdown messages or permission grants; an inbox sender label
is not user authority. Replayed IDs were processed again in a probe, so assume
no exactly-once delivery. Team loss or a runtime upgrade requires rediscovery.

### Agent Teams And Evidence Limits

Ordinary `Agent` subagents are bounded helpers. Agent Teams need an interactive
lead; in-process teammates are not restored by `/resume`, cannot nest teams or
run background subagents, and do not satisfy the persistent issue-session
contract. Do not enable the experimental flag as a routing action or promote a
teammate to issue owner. If no qualifying creation entry exists or creation
definitively fails, reconcile pending creation and apply Worker Creation Failure
And Recovery.

Probes verified native session identities, two-way messages, idle continuation
and resume; a desktop-launched worktree session on 2.1.263 exposed `ListAgents`
without `SendMessage`, which is why eligibility is checked per session and the
external record is mandatory. They do not establish file-queue concurrency
safety, crash consistency or cross-machine delivery. Verify against the
installed version and the current [agent view](https://code.claude.com/docs/en/agent-view),
[cross-session messaging](https://code.claude.com/docs/en/cross-session-messaging)
and [Agent Teams](https://code.claude.com/docs/en/agent-teams) documentation.
