# Claude Controller Communication

Read when selecting a Claude communication transport, arming the controller
heartbeat, or recovering a failed callback. Apply the controller-session
evidence and the `callback_transport` check in [the adapter](claude-code-adapter.md)
first. A transport changes message delivery, not issue ownership or permission.

## Default And Fallback Selection

The closest match to Codex's user-owned task creation, read/status, continuation
and controller-managed barriers is **native persistent Claude sessions plus
`ListAgents` / `SendMessage`**. Use that by default when the running controller
and worker sessions actually register `SendMessage`. Native messaging is the
wake signal only; the Worker Callback Packet of record is always written to
the [external callback record](#external-callback-record), so a controller
without messaging loses timeliness, not correctness. Preserve a required
configured worker entry such as Axis; this preference does not bypass its
management or authorization boundary.

| Transport | What it supplies | Selection boundary |
| --- | --- | --- |
| External callback record | Durable, runtime-independent delivery of the Worker Callback Packet as a Linear issue comment (PR comment when no issue exists), read by the controller on wake; identical for Codex and Claude workers | Always written by the worker on merge or blocker; the only callback path when the worker or controller registers no native messaging |
| Native cross-session messaging | Peer discovery, delivery to independent sessions, replies and idle wake; native session controls supply stop/resume | Default wake signal for persistent issue controllers once `callback_transport: native-messaging` is verified on both sides |
| Native Agent Teams messaging | `SendMessage` backed by runtime-managed inboxes and team coordination | Preferred for existing team-scoped bounded collaboration; team lifetime is not independent issue persistence |
| Desktop session-management `send_message` | A person-facing hand-off into another desktop session | Ineligible: not for orchestrating background work and cannot reach unattended sessions |
| Direct file mailbox | Plain messages consumed from an existing live session/team inbox; receiver may wake and reply through files | Experimental fallback when native messaging is technically unavailable and the endpoint/schema/receipt checks below pass |
| Native status/read/attach plus [Claude heartbeat](#claude-heartbeat) | Recover evidence and continue the same registered session without a working message transport | Standing recovery path while workers are active; disclose manual resumption if no heartbeat tool can be armed |
| Bounded helper return / serial inline | A scoped artifact or one active issue owned by the invoking controller | Helper return for bounded work; serial inline only when qualifying issue-session creation is unavailable |

Resolve the wake transport in that order **within the required lifecycle**;
the external callback record is not a fallback and is written regardless of
which wake transport is selected. An independent-session assignment must not
silently become a teammate to obtain a mailbox. If its
existing persistent receiver has a verified live team-lead inbox, file transport
may serve that same receiver without replacing its session identity. Otherwise
keep its native read/status/continuation path. For an existing team, prefer its
native send tool, then eligible file delivery, then supported lead intervention.
A missing SendMessage tool is not proof that sessions cannot be created.

Never switch transport to evade a permission denial, inbound refusal/hold,
policy filter, or unavailable authority. Diagnose those outcomes and retain the
pending gate. Permission settings and experimental flags are not silently
changed as part of a fallback. Reuse any authorization already covering the
exact scope; configuration that needs new authority remains separate.

Record `communication_mode`, its selection/fallback reason, sender and receiver
session identities, endpoint evidence and pending message IDs in the existing
worker registry. Test a nonce round trip before relying on a newly selected
channel for automatic continuation. Do not resend a possibly accepted command
through another transport until its receipt/state has been reconciled.

## External Callback Record

Use the assigned Linear issue as the durable carrier for every Worker Callback
Packet on Claude Code, whether or not native messaging is available. This is
the same evidence surface the controller must verify anyway, and it works
identically for a Codex worker, so mixed-executor waves share one callback
path.

1. The controller names the record target in the worker handoff: the Linear
   issue ID, or the PR when no issue exists, plus the controller session ID
   and a per-dispatch correlation ID. The worker writes the complete Worker
   Callback Packet as one issue comment (via the Linear CLI or MCP) on merge,
   awaiting-acceptance, or a concrete blocker. Keep the packet's first line
   (`Dev project worker callback`) as the marker, and include the correlation
   ID, worker session ID and attempt number so repeated writes deduplicate.
2. When `SendMessage` is also registered, the worker sends a short wake message
   carrying only the issue ID and correlation ID. The comment remains the packet
   of record; do not rely on the message body when the two differ.
3. On every wake, the controller reads callback comments newer than the
   registry's `last_callback_seen` for each active issue, keys them by
   correlation ID, and records queued, received and applied as separate facts.
   A comment that arrives through both transports is processed once.
4. A callback comment is a claim, not evidence. Verify live PR, CI, base-branch
   merge and Linear state before updating the wave barrier, exactly as for a
   native message. Do not treat a Linear state change alone as a callback; a
   person can move an issue without the worker having finished.
5. If the worker cannot write the comment (no Linear access, closed issue,
   permission refusal), it must report that blocker through whatever transport
   remains and stop; the controller heartbeat then reads `claude logs` for the
   packet. Do not fall back to a different record target the controller did not
   name.

Probe the record path with a harmless nonce comment on first use in a project,
under the same round-trip rule as any newly selected channel.

## Claude Heartbeat

The orchestrator's heartbeat is the recovery mechanism for missed callbacks,
exited workers and externally merged PRs. On Claude Code it has concrete
limits that decide whether a controller can run unattended:

- The controller must be a live interactive session. A `-p` / print-mode
  controller exits when its turn ends and can neither receive callbacks nor
  fire a heartbeat. `claude --bg` workers are unattended and cannot host the
  heartbeat for their own controller.
- `CronCreate` fires only while the controller is idle, lives in session memory
  only (gone on exit, not restored by `/resume`), and a recurring job expires
  after seven days with one final firing. Keep one heartbeat armed whenever a
  wave is in flight: create it when a wave is dispatched and none is armed,
  use the calling orchestrator's backup interval and recovery deadline
  (Dev defaults to 45 minutes with verified callbacks and healthy workers,
  backing off toward 60; shorten only for a concrete recovery need), delete it with `CronDelete` when no workers are
  active or the project completes or stops, and re-create it after reconciling
  the registry whenever the controller session is resumed or a later wave is
  dispatched.
- `ScheduleWakeup` exists only inside `/loop` dynamic mode. Use it as the
  heartbeat only when the user launched the controller under `/loop`; do not
  assume it is available otherwise.
- `Monitor` supplies event-driven wake from a polling script. It is the better
  choice when a specific external transition is awaited (PR merged, CI
  finished, a new callback comment). The script must emit on every terminal
  state, including a worker that `claude agents --json` reports as stopped or
  failed, poll remote APIs no faster than every 30 seconds, suppress an alert
  whose underlying state has not changed since its last emission, and end with
  the controller session. A monitor that repeats a known condition on a fixed
  cadence wakes the controller at full context for no new information. Bound
  each monitor to a wave; do not leave an unfiltered monitor running.

- Prefer a detached terminal-condition command when the runtime verifies background execution, completion notification, and idle wake of the same controller: the controller ends its turn, the polling runs outside the model, and completion supplies a wake when the command exits. A shell process alone does not prove this notification path. Prefer it to a short cron interval for a bounded wait such as a merge, a check run, or a worker exit, and keep a long-interval cron only as the residual net for a watcher that dies with its session. Avoid unnecessary model wakes as well as redundant reads within each wake. Treat the observed Claude session costs as local evidence; do not claim a measured saving or extrapolate it to Codex without a comparable run.

On each heartbeat or monitor wake, in order: list active workers with
`claude agents --json --all --cwd <directory>`, read `claude logs` for any
exited worker without a recorded callback, read the external callback record,
verify live Linear, GitHub and CI state, then re-evaluate the whole active wave
per the orchestrator's Controller-Owned Wave Execution. Record the heartbeat
tool, interval, creation time and job or monitor ID in controller state.

If no heartbeat tool can be armed and native messaging is absent, report that
automatic continuation is unavailable and ask the user to resume the
controller, as the orchestrator requires. Do not hand orchestration to a worker
or to a bounded sub-agent to work around the limit.

## Direct File Mailbox Fallback

This is a version-sensitive local compatibility path, not a general filesystem
message bus. The receiver must already be a live Claude session whose runtime
has created and is consuming a mailbox. A directory or saved transcript alone
cannot wake an exited process or restore a lost teammate.

1. Resolve the exact target from its accepted session receipt and native status.
   Inspect that runtime-created team's `config.json` read-only to correlate
   `leadSessionId`, member name/ID and the selected receiver. Do not discover by
   guessing a name from an issue, manufacture a team, or edit runtime config.
2. Locate its inbox under `~/.claude/teams/<observed-team>/inboxes/<receiver>.json`.
   A persistent session's own endpoint can be its `team-lead` inbox; that does
   not make another team member an independent issue controller. Keep the
   sender's actual registered identity; do not impersonate a member or user.
3. Verify the installed version's plain-message schema with a harmless native
   message or a disposable probe. Preserve the envelope below only while that
   runtime accepts it. Require an actual correlated receiver response, not just
   a file write, disappearance, or a changed `read` flag.
4. Use the runtime-compatible writer/lock when available. Otherwise confine
   direct writing to a verified drained inbox with one coordinated sender and
   no concurrent native/file writer. Preserve existing data; an unread entry,
   changed snapshot, unknown writer, malformed file or unknown schema stops the
   direct write and selects native status/continuation recovery. A snapshot
   comparison alone is not a shared lock and does not establish concurrency
   safety. Do not replace a busy inbox, append bytes to a JSON array, or claim
   that atomic rename solves concurrent read-modify-write races.
5. Write a complete valid JSON array through a same-directory temporary file
   and atomic replacement only under the preceding serialized conditions.
   Restrict writes to the exact authorized inbox. Do not overwrite unrelated
   paths or follow an unexpected symlink; do not clear or repair a malformed
   runtime inbox as an incidental send operation.
6. Carry a unique message ID and an application correlation ID in plain text,
   and have the receiver echo that correlation with its actual session/issue
   identity. Keep processed IDs in the existing controller/issue state before
   applying a requested transition. Duplicate messages return the previous
   receipt or current state instead of repeating side effects. A retry retains
   the same logical ID; a new ID does not resolve an uncertain earlier send.
7. Wait for the correlated response through the chosen native or file return
   endpoint, or inspect the receiver's conversation through native controls.
   Record queued, received and applied as separate facts. If no live consumer,
   safe writer or response can be verified, retain the same owner and fall back
   to status/attach/heartbeat; do not report automatic continuation as working.

The plain envelope observed on Claude Code 2.1.263 is:

```json
{
  "from": "<actual-sender-identity>",
  "text": "<plain callback or request with logical ID, issue and reply endpoint>",
  "summary": "<short summary>",
  "timestamp": "<ISO-8601 UTC timestamp>",
  "msgV": 1,
  "msg_id": "<unique UUID for this logical message>",
  "type": "message",
  "read": false
}
```

The file is an array of these envelopes, not JSONL. Optional runtime fields may
be present; preserve them. This route sends plain text only, never fabricated
plan approvals, shutdown protocol messages or permission grants. An inbox
sender label is not authenticated user authority. Receiver permissions and
live issue/PR evidence still govern every action.

Direct replay of the same `msg_id` was processed again in the disposable probe;
do not assume the runtime provides exactly-once delivery or deduplication.
Inbox consumption can race with writes, and replies can arrive out of order.
Do not use an unverified file writer as a production command queue. Team loss or
runtime upgrade invalidates the endpoint/schema evidence and requires discovery
and a new harmless round trip before reuse.

## Evidence And Comparison Limits

The native-session probe verified separate identities, bidirectional messages,
idle continuation and original-session resume. A later check on Claude Code
2.1.263 found a desktop-launched worktree session that exposed `ListAgents`
but not `SendMessage`, which is why transport eligibility is verified per
running session and the external callback record is mandatory. The external
record path was not round-trip probed in this change; its first use in a
project must run the nonce probe above. The file probe verified plain
inbox delivery to a teammate and replay behavior; its full observations are
recorded with the change's validation evidence. These checks do not establish
file-queue concurrency safety, crash consistency, exactly-once effects or
cross-machine delivery. Thus native persistent-session messaging remains the
default even when direct file delivery is available.

Use current official [Agent Teams](https://code.claude.com/docs/en/agent-teams),
[cross-session messaging](https://code.claude.com/docs/en/cross-session-messaging)
and [agent view](https://code.claude.com/docs/en/agent-view) documentation with
installed-runtime receipts. Team messaging and direct inbox writing share the
same receiver lifecycle; they are two transports, not two persistence models.
