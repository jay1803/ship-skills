# Codex Adapter

Use this adapter only after the Review routing contract resolves Codex.

## Binding

- Runtime role: `reviewer`.
- Standard depth: select the current balanced Codex coding/review model and its
  normal reasoning effort.
- Deep depth: select the current strongest available Codex coding/review model
  and a high reasoning effort.
- Set model and reasoning explicitly in the spawn request when the runtime
  supports those fields. If the requested binding is unavailable, apply only
  the fallback authorized by the routing request.
- Create a clean context with no implementation-thread history. The assigned
  reviewer may inspect the exact repository target and surrounding code but may
  not dispatch another reviewer or provider.

Record the actual model, reasoning effort, runtime role, any fallback, and
independence result in the routing receipt. Never infer a runtime binding that
the environment did not report.

## Capability And Output Recovery

Use the shared Artifact Contract dispatch evidence ownership packet.
Before dispatch, verify that the selected execution surface can read its exact
repository target and required authority. When clean contexts lack tracker or
GitHub access, supply a source-identified, timestamped immutable snapshot via
the authorized controller; do not copy credentials or implementation history.
Required live rechecks remain with the controller. Missing runnable dependencies
are evidence limitations, not passing tests.

Distinguish active concurrency from a cumulative thread quota using the actual
runtime error. Wait for active slots only when that can release capacity. A
cumulative quota is not repaired by changing parent nodes or creating user-owned
sidebar tasks. Use an available clean ephemeral executor only within the existing
executor/fallback authority, with the same target and isolation; otherwise return
the capability blocker. Preserve explicit cross-executor independence.

Silent stdout is not proof of a stall. Check process termination, observable
progress and artifact completeness against the executor's real deadline. Keep a
healthy long-output process running; do not impose an arbitrary short quiet-time
kill. On an actual runtime failure, retain partial output and retry only the
failed judge against the same immutable sources within the existing retry
allowance. Do not rerun successful reviewers or publish incomplete artifacts.
