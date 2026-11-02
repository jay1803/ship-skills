# Native Stack Integration

Read for a selected GitHub native PR stack. The [branch strategy](branch-strategy.md)
owns policy precedence, batch isolation and final promotion. GitHub's maintained
[stack rules](https://docs.github.com/en/pull-requests/reference/stacked-pull-requests)
and [merge procedure](https://docs.github.com/en/pull-requests/how-tos/merge-and-close-pull-requests/merging-stacked-pull-requests)
own provider semantics; check current support/help before an operation.

## Identity And Ownership

A stack is a same-repository dependency chain. Its bottom PR targets the trunk;
each upper PR targets the previous layer's branch and shows its own layer diff.
Keep the controller's temporary batch branch as trunk when batch isolation
applies. Native stacks do not merge across repositories.

Record the ordered issue/PR/branch set, trunk and promotion target, immediate
bases and base/head SHAs, per-branch owners, accepted Review references and
selected validation, active dependents, and update/merge executor in existing
controller/worker state. Capture actual GitHub membership; branch naming or
retargeting alone does not establish a native stack.

Issue workers own their layer's implementation, validation, Review and closeout.
The controller owns scheduling and assigns the explicit stack checkpoint to
`$dev-integration-manager`. Before cascading updates or a group merge, obtain
the existing owners' accepted handoffs for the exact branches/actions, quiesce
competing writers and carry original mutation/merge authority. The integration
assignment coordinates that authority; it does not grant it. Reconcile an
unavailable owner before rewriting its branch. Preserve human-only merge and
production-release boundaries.

## Development Admission

`StackReady` is an unmerged development checkpoint, not issue completion or a
merge barrier. The controller can admit a dependent layer when stack scheduling
is selected and the predecessor has a verified remote PR/head, stable required
contract/artifacts, current accepted selected validation/Review evidence, and an accepted
branch-retention/update handoff. Pin the dependent to that exact head and record
which edge uses this checkpoint. Green CI or an open PR alone is insufficient.

Explicit merge-before-next scheduling, a required deployed artifact, unresolved
product/API decisions or another required predecessor gate still holds that
edge. Cross-repository dependencies use their actual contract/availability
evidence; they cannot use branch ancestry as a substitute.

A stack-ready callback retains the issue worker and branch, names pending merge
and acceptance gates, and identifies the integration owner/wake condition. If a
predecessor changes, invalidate affected pins/readiness, reconcile descendants
with their owners and refresh only impacted evidence before further admission.
Already-started work stays owned; do not create duplicate successor workers.

## Updates And Review Continuation

Coordinate a planned stack update before freezing an expensive Review target.
Use GitHub's server-side Rebase stack or the supported `gh stack` extension for
cascading updates; inspect installed help and worktree support. Do not install
or upgrade tools without existing authorization. Handle conflicts through the
owning implementer, preserve local changes and never force-push the trunk.

After an update or partial merge, re-read membership, immediate bases and heads,
and trunk; compare old/new layer diffs and inspect affected callers, shared
contracts, generated artifacts and integration behavior. Apply the
[re-review rules](review-lifecycle.md#requesting-review) with that evidence,
the unchanged per-issue ledger and current validation: an identical head tree
reuses the prior result; otherwise request focused re-review of the delta,
which escalates to full when it crosses a protected boundary or a governing
full minimum applies. SHA changes alone do not select full review. Preserve
findings, prior results and cumulative budgets.

GitHub may retain approvals when a stack rebase leaves the diff unchanged.
That is provider approval state, not a current agent Review result or passing
CI. Refresh required checks on the actual candidate, including merge-group
checks when queued. A changed target during Review is still stale.

## Landing And Closeout

Resolve the exact contiguous merge group starting at the lowest unmerged layer.
A native merge of an upper layer also merges every unmerged layer below it;
never treat that command as a one-issue mutation. The integration executor
checks each included issue through `$dev-merge-handoff`'s gate without triggering
individual upper-layer merges, plus current stack linearity, trunk protections,
combined validation and authority covering the entire group. A blocked layer
holds it and higher layers; a ready lower prefix may land when the recorded
scope permits. The provider's asynchronous merge API is required for API stack
merges; verify the installed CLI/API surface rather than assuming ordinary
`gh pr merge` has one-PR effects. Queue acceptance or a merge request is pending.

Immediately before mutation, refresh every included target and gate. After
landing, verify each PR is MERGED and its resulting commit is on the trunk;
return per-issue evidence to the existing workers. Re-read and reconcile the
remaining stack's automatic rebase/retarget before further acceptance or merge.
Retain any branch/worktree needed by an active layer, worker or unresolved
retarget, including after squash merges. Report unknown dependency state as
retained pending reconciliation. Cleanup needs its own accepted handoff.

Only verified landing and remaining issue gates permit tracker closeout. A
stack landing on a temporary batch trunk still needs combined validation, the
aggregate promotion PR and final handoff before project completion. Production
publication and consumer installation remain separately authorized.
