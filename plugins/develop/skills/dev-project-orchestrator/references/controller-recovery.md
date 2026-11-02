# Controller Recovery

Read on callback/heartbeat, uncertain worker health, or an external gate that
needs automatic follow-up. This contract applies to batch and sequence scheduling.
Recovery verifies state; it does not waive merge gates, expand authority, dispatch
successors from a worker or take over implementation/technical Review.

## Existing State And Check Results

Keep one source of current facts in the existing controller/worker registry.
Add missing fields there rather than creating another tracker or copying state
into the automation prompt. Recover current authority, routes and queued
creation receipts after context loss; every fresh issue still needs its own
route, while unchanged same-worker continuation reuses its route.

For each unfinished worker or external gate, retain:

- Phase, exact pending target and waiting operation/condition, with its evidence
  locator and next action owner.
- Last meaningful progress and actual status/error observation, distinguishing
  creation accepted, first turn observed, running, idle, failed and unknown.
  A generic active label or an unchanged message cannot alone establish health.
- Last successfully completed check, observed source/cursor, next check time and
  any unresolved callback/decision. Set the check interval from the pending
  operation, adapter and required recovery delay; elapsed time alone is not a stall.
- Callback/wake transport and its verified receipt. Keep merge evidence, cleanup
  and scarce-resource occupancy separate from health.

A check that failed, was merely scheduled, or returned unavailable data is not
successful. Keep the failure and due check pending; advance a deadline only
after the corresponding actual check succeeds. A changed progress message or
duplicate wake cannot reset it. Record received/applied callbacks separately,
deduplicate correlation IDs and reuse a fresh check for the same wake cycle.

## Reconcile Before A Quiet Return

1. Read missing compact worker status/error and changed callback records since
   saved cursors, batching independent reads. Apply the selected adapter's
   required record/live-state reads even when a generic deadline is in the future.
2. Reconcile missing first-turn evidence, a worker error/exit/unknown health,
   actionable callbacks, a due check or a changed external gate. At the recovery
   interval read live PR/CI/issue/base signals even if worker status is unchanged.
   No reliable change cursor means bounded recovery reads, not assumed silence.
3. Expand history only for that worker or unresolved gate. Distinguish a known
   long build/helper operation from a failed or absent owner. Before recovery or
   replacement preserve unpushed work and reconcile mutating helpers; an
   inaccessible owner is not confirmed stopped. Resume the same worker at its
   pending phase with original evidence and cumulative budgets.
4. Apply verified delivery evidence under the worker execution/cleanup contract,
   then reconsider the whole pending graph and actual capacity. An externally
   assigned merge remains held until its source-bound release condition and all
   gates pass; green CI or healthy workers do not open its barrier.
5. Save actual check results/cursors and the next action/owner for every unfinished
   target. Quiet return requires healthy known waiting, no unhandled actionable
   signal or due check, adapter reads satisfied, and a verified future wake path.
   Unknown/failed checks need reconciliation or an explicit limitation, not a
   healthy/DONT_NOTIFY claim. An unfinished project with no unresolved target
   needs completion or admission reconciliation. This is not a reason to chain
   idle waits; follow unsupported/failed runtime recovery without holding the
   turn open.

Optionally apply step 5 mechanically with the read-only
`scripts/check_recovery.py` (see its `--help`) over a projection of the
registry. It checks only the projection you supply, not the truth or
completeness of your observations, and replaces none of the reads above.

## Stable Wake Prompt And Lifecycle

Use worker merge/blocker callbacks as the primary wake path; include the
controller ID, supported messaging transport and packet destination in each
handoff. A recorded external merge handoff is actionable too. Ordinary commits,
heads, CI transitions and progress stay in the worker. Confirm callback reachability;
on Claude use the [external callback record](executor-sessions.md#external-callback-record).

Prefer a terminal-condition watcher only when background completion can verifiably
wake this same idle controller. A shell PID/pollable exec result is not that proof.
Retain one backup heartbeat for silent exits, missed callbacks, external changes
and watcher failure. With healthy workers and verified callbacks start at the
existing 45-minute recovery default, widening toward 60 after repeated quiet checks
within the recorded maximum recovery delay. Shorten for uncertain health,
unavailable callbacks or a real deadline; ordinary progress does not restore a
short interval. Repeated non-actionable wakes require widening/narrowing the wake
configuration rather than repeating full context checks.

Keep identity, scope, state/authority locators, recovery predicate and material
boundaries in the stable prompt; changing heads, test counts, worker inventory
and logs stay in state. For example:

> Resume this controller from its existing state and current authority sources,
> using the controller recovery contract. Reconcile worker status/errors and
> callback changes; perform due live checks even without new messages. Recover
> through the same owners and budgets. Record successful checks and pending
> actions, preserve a verified wake path for unfinished observable gates, and
> return quietly only when no controller action/check remains. Fresh issue
> dispatch needs its own route; unchanged continuation reuses it.

Update the automation for scope/authority, recovery policy, lifecycle or missing/
stale configuration, not routine progress. Preserve notification policy; quiet
response suppresses notification, not model execution. Callbacks, heartbeat,
status questions and authorized goal continuations share one signal/cursor/
deadline, not duplicate pollers or repeated unchanged Skill loads.

Before yielding a newly dispatched wave or resumed session, verify its future
wake path is armed; re-arm if an earlier wave removed it. No active worker does
not imply no unfinished work: an external merge/deployment/dependency/decision
gate may still require observation. Retain the applicable monitor/heartbeat
until those automatic-follow-up conditions resolve, project completion/stop is
verified, or another verified transport owns them. A human-held gate's wake
path follows its actual communication capability; never claim a nonexistent one.

Use bounded waits for concrete in-flight operations, not chained short waits/
sleeps to hold idle turns open. If no supported wake path exists, preserve state,
report that automatic continuation is unavailable and identify manual resumption.
Do not transfer orchestration to a worker. If a goal host immediately replays
idle turns without pause/coalescing, disclose that limit once; never mark a goal
complete/blocked, change its budget or claim repaired scheduling just to suppress wakes.

## Controller Runtime Failure

Track wake scheduled/delivered, controller turn started, check succeeded and
turn failed as different facts where the host exposes them. Quota, authentication
or runtime failure before model execution cannot be detected by that failed
controller's prompt. A future surviving controller can read the failure and
reconcile unfinished workers; a host supervisor is needed to observe failures
while the model cannot run.

Use only an actually supported, authorized host failure notification/recovery
path. If absent or unknown, report that gap with the preserved state and recovery
condition; do not claim this Skill schedules retries, heals credentials, switches
models or provides independent supervision. A runtime-unavailable wake is not
a quiet healthy check and cannot move check deadlines or reset delivery budgets.

