# Stateful Flow Planning

Read only when the plan changes a real stateful boundary: a permission, cache,
auth or persisted-session flow, a migration or maintenance procedure, or state
shared by several owners. A stateless patch already proved by focused tests
needs none of this.

## Event Order And Ownership

For changed permission/cache flows, include the relevant event order and
visible-state invariant in the plan: authoritative denial or replacement,
previously cached data, and an older response arriving after that transition.
Select probes from the changed acceptance and reuse sufficient existing tests;
this is not a universal matrix or a requirement to add duplicate tests.

For migration, maintenance, or multi-owner state changes, trace admission,
in-flight work, transition, abort, rollback, and restart across each affected
owner. Distinguish durable state, process-local authority, and startup
configuration. Check alternate exit paths before settling the sequence. Use
actual component modes when lock/journal/runtime semantics determine safety;
a generic substitute is not proof of the required behavior.

## First Runnable Path

When normal tests can bypass the behavior being promised, make the first
relevant implementation slice prove one runnable path through the actual
coordinator/repository and observable completion or routing. The planner
identifies this checkpoint; the implementer/test owner compiles and executes it.
A success flag, mounted success screen or disconnected callback proves only the
harness. Inspect local runtime/seed and provider-seam options before concluding
that the path cannot be tested; a provider substitute must not replace the
changed behavior itself. Keep test-only APIs out of release surfaces and name
the evidence fidelity actually demonstrated.

Choose boundary probes from the changed contract: for auth or persisted session
changes, this may mean native SDK storage/reopen and observable barriers before
and after an identity change, with distinct consumers when isolation matters.
Do not use this slice to reinstate mode-waived live accounts and environment
logistics.
