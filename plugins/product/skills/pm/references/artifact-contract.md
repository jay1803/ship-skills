# Product Artifact Contract

Use for standalone Product analysis, drafts, and bounded workers. For authorized
issue lifecycle writes, also read [tracker-contract.md](tracker-contract.md).

## Intent and completion

Honor the requested artifact and endpoint. Classification, framing, a PRD,
analytics, reviews, and release notes can be completed from
provided evidence without creating a tracker record or invoking the full PM
chain. UX/UI artifacts route to Design without requiring PM lifecycle setup.
A named next owner is a recommendation unless continued execution is
requested. Do not require a PM root for an unbound document or chat artifact.

For tracker-backed work, preserve the exact target and existing authorization.
Read access or the availability of a write tool does not authorize publishing.
If the request authorizes a write, complete it and verify the result; a draft is
not a substitute for an available, authorized mutation. When a required tool is
unavailable, still complete independent analysis and return the unapplied draft.

Use confirmed intent, verified inherited behavior, and engineering invariants.
Do not silently adopt a material product proposal. Consult
[decision provenance](../../pm-spec/references/decision-provenance.md) when a new
rule or a scope change requires a decision. Preserve user-delegated discretion
within its exact stated bounds; do not ask again for decisions already settled.
A pending decision blocks dependent work, not independent evidence gathering or
the remainder of an already-authorized artifact. Do not publish unresolved
policy as accepted scope or claim dependent readiness.

For small changes, include only the screens, states, metrics, and evidence that
change the decision. Templates are examples: omit irrelevant fields and empty
sections. Existing behavior need not be redesigned to fill a checklist.

## Bounded delegation

Inline execution retains the current runtime. Delegate only when independent
judgment or a bounded parallel task adds value and delegation is authorized.
Before dispatch, use the package-local Jev routing command under the
[input contract](jev-input.md). Consume its envelope and binding directly;
do not load the PM map or adapter classification tables.
Pass the request, relevant sources, target artifact, exact write scope, existing
PM root when applicable, and stopping condition. Return the artifact, sources,
routing receipt, applied writes or drafts, evidence, and unresolved decisions.
A bounded worker does not acquire controller ownership or dispatch successors.
