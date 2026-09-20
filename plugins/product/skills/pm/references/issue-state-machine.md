# Issue PM State Machine

The PM controller owns issue state and tracker coordination. Skills contribute
missing decisions or evidence; they are not mandatory process stations.

## Entry and resume

Read the current issue, verified PM root and relevant decisions, dependency and
handoff evidence. Classify actual gaps in goal/scope, canonical specification,
and readiness. Reuse equivalent current evidence regardless of comment headings.
Do not reread full history between uninterrupted steps. Refresh affected objects
after writes, transport errors, concurrent changes or revised requirements.

Carry the issue and root IDs, canonical revision, current gap/owner, any exact
unresolved proposal bundle, applicable review and its input binding, and IDs of
material comments already present. Preserve linked implementations, branches,
PRs and predecessor evidence; a missing handoff does not mean no work exists.
Do not create comments for satisfied, unchanged or inapplicable stages.

A new authorized issue receives faithful intake through `$pm`; an existing
complete issue can enter readiness directly. If there is no PM root, `$pm` or an
authorized direct-entry readiness run initializes the one root with existing
classification and source links under the tracker contract. Root initialization
is a bounded operation, not a new PM chain.

## Unresolved product decision

When a material rule is not covered by user confirmation, verified inherited
behavior or bounded delegated discretion, record the exact proposal, its owner
and source. Obtain the decision before dependent canonical writing, readiness,
status advancement or Dev continuation. Independent authorized analysis may
continue. Dependent workers return the earliest gap/owner without a duplicate
blocked comment.

After an answer, verify it resolves the presented bundle. Record the proposal,
exact answer and source in the single `## Product Decision` reply before
canonical writing; preserve earlier decision entries there. Update any existing
owning artifact and continue from the affected gap. A status request or generic
continuation does not grant an unasked product choice or a larger execution
allowance. See [decision provenance](../../pm-spec/references/decision-provenance.md).

## Solution Review applicability and freshness

Use `$pm-solution-review` when the user or binding policy requests it, or a
confirmed candidate presents a material simplification question: new product
rules/defaults/exceptions, several competing mechanisms for the same outcome,
or adjacent/generalized scope with a plausible smaller solution. Resolve
unconfirmed product choices before this review; the reviewer cannot approve
policy for the user. The number of files or a non-Bug label alone is not a
trigger. Restoring established Bug behavior does not need this gate.

A straightforward change preserving established mechanisms can proceed to spec
and readiness without a Solution Review. Carry a short applicability reason in
the handoff rather than posting a not-applicable review. Where review applies,
reuse evidence for unchanged goal, scope, rules and provenance; rerun only after
material input changes. `simplify` routes to the scope owner and the exact
needed user decision, then review of the revised candidate.

An explicit user omission may override this advisory review unless a binding
repository policy requires it. Record `skipped by user`, its source and scope;
never call it approved or use it to clear product ambiguity. Mode alone does
not override a required review. Readiness checks applicable review evidence,
not a second full simplification audit.

## Canonical updates and affected scope

Before a handoff, `$pm-spec` reconciles the current product contract with exact
confirmed changes. Update obsolete active requirements; preserve history and
source provenance in the PM thread. Comments should not become permanent patches
that every consumer must manually reconcile with contradictory active text.
Uncertain/conflicting authority remains a decision gap, not permission to choose.

When a project decision affects several active issues, the project controller
identifies affected members from the authorized inventory, including cross-parent
prerequisites. Route each canonical change through its issue's `$pm-spec` owner,
serializing same-issue writes. A child worker returns affected-sibling proposals
to the controller rather than editing siblings. Uncovered write scope produces
an exact unapplied draft, not an expansion of authority.

A changed shared contract invalidates dependent readiness/integration evidence,
not unrelated completed work. Refresh affected dependencies and final integration
order through the project owner, preserving independent preparation that can
safely continue. A changed comment or a new PM invocation alone does not require
replaying every gate.

Apply [unattended acceptance](../../pm-spec/references/acceptance-policy.md#unattended-engineering-acceptance)
to older requirements immediately. Carry a verified mode waiver and its source
while canonical paperwork is repaired; deferred human/device/live testing does
not block engineering. The product promise and failed automated observations
remain unchanged. Do not retrospectively relabel older failures or skips.

## Readiness and completion

PM-to-Dev completion requires:

- stable scope and no unresolved material product decision;
- a current canonical title/description with confirmed behavior and critical
  acceptance, including start-relevant dependencies and product constraints;
- applicable Solution Review evidence or an authorized disclosed omission;
- Readiness `ready` for that canonical revision;
- verified authorized tracker sync and a single current `## PM Handoff` result.

Readiness supplies the gate result and handoff payload in one record. The PM
controller completes actual tracker sync and next dispatch in that same reply.
For a direct readiness request, return its assessment without assuming authority
to launch Dev. If a legacy separate `## Readiness Review` / `## PM Handoff` pair
exists, consume both as evidence, update the existing Handoff with the current
combined result, and leave the old review as history; do not create another pair.
A new blocked assessment may use the same result record but is never a valid
Dev handoff. Drafts and failed writes do not establish applied readiness.

Use [Develop handoff](develop-handoff-contract.md) for conditional mode/runtime
fields and [tracker contract](tracker-contract.md) for writer and thread rules.
Writing a spec or adding `scoped` alone is not PM completion.
