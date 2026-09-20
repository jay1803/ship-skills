# Domain Modeling Within A Technical Plan

Read when vocabulary, lifecycle, invariants, state transitions, or ownership
ambiguity would materially change a technical choice. Start by naming that
choice. If no such ambiguity exists, omit modeling and continue the current
plan; no separate bypass artifact or architecture handoff is required.

Use the approved source spec, acceptance criteria, current implementation, and
contract tests. Anchor every rule to a source statement or observed behavior.
Do not invent product rules, API fields, retention policy, or permissions.
A missing product decision returns to `$pm-readiness-review`; a technical
unknown stays explicit in the plan or routes to investigation.

Resolve only what affects the decision:

- **Vocabulary:** define the necessary concepts in their product/contract sense,
  distinguishing persistence and UI representations only when it matters.
- **Invariants:** name the source, enforcement boundary, and verification path
  for each rule across writes, retries, and concurrent actors.
- **State:** model relevant states, allowed transitions, triggers, guards,
  terminal/recovery behavior, and ownership. Omit state machinery where no
  meaningful lifecycle exists. Do not collapse independent state/authority
  dimensions into a convenient single success flag.
- **Ownership:** identify who decides, validates, persists, retries, acknowledges,
  or emits side effects at the caller/service/storage/worker/provider boundary.
  Preserve idempotency and error responsibilities when they affect correctness.
- **Unknowns:** keep only decisions that would change implementation, with their
  owner and whether they block coding or later verification.

Use compact tables or prose inside the Technical Plan. Reuse repository names
and boundaries. Do not add an aggregate, repository, event taxonomy, domain
layer, or diagram merely to demonstrate modeling. Translate these rules into
affected-layer responsibilities and acceptance evidence; carry their source
anchors into any slices and the implementer's brief.
