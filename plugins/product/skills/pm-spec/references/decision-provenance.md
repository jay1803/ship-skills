# Decision Provenance

Use this reference when a PM stage discovers behavior that was not explicit in
the user's request, verified current behavior, or an already-approved decision.
It defines the regression boundary for silent product-policy invention.

## Provenance Classes

- **User confirmed**: the user explicitly approved this exact behavior or an
  explicitly presented bundle containing it.
- **Inherited behavior**: a verified current product or external contract already
  requires the behavior. Cite the source and state whether preserving it is in
  scope.
- **Agent proposal**: PM recommends the behavior to close an ambiguity. It is not
  a requirement until the user confirms it.
- **Engineering invariant**: implementation correctness such as atomicity,
  idempotency, retry safety, secret handling, or deterministic recovery. Keep it
  in the PM technical thread or Dev plan unless it changes observable product
  behavior.

Do not infer confirmation from a general desired outcome. Approval applies only
to the decisions that were visible in the approval request. A later broad
approval such as "looks good" may confirm the explicitly listed proposal bundle,
but not parameters or rules that were absent from that bundle.

## User-delegated discretion

When the user explicitly delegates a bounded choice, record the delegation as
User confirmed authority and the selected choice as an agent selection within
that authority; do not claim the user personally chose the detail. Verify the
choice stays inside the delegated scope. General requests to continue do not
delegate new product policy. A material choice outside that scope still needs
a Decision Delta. This applies to routine layout choices already delegated by
the user as well as other explicitly bounded product decisions.

## Confirmation Semantics

`User confirmed` requires semantic approval of the exact decision, not merely
permission to continue the workflow. Commands such as `继续`, `继续推进`, `下一步`,
`开始`, `$pm continue`, `proceed`, or `keep going` authorize process progression;
by themselves they do not approve a proposed scope expansion, default, limit,
fallback, visibility rule, or other product policy.

A short answer such as `可以`, `同意`, or `继续` may confirm a decision only when
it directly answers a pending approval question that:

- explicitly labels the proposal or selectable bundle as requiring a decision;
- shows every material user-visible rule included in that bundle; and
- asks the user to approve, reject, or choose it before the workflow advances.

If the previous message merely recommended a solution, summarized findings, or
named a next PM stage, treat a continuation response as workflow authorization
and keep the product proposal unconfirmed. Record the approval prompt and the
answer together; quoting a continuation command alone is insufficient
provenance.

## Material Product Decision Test

Treat a newly introduced rule as a material product decision when it changes any
of the following:

- what a user or operator can see, do, configure, recover, or understand;
- a default, limit, cap, timeout, retention period, rate, ranking, or threshold;
- automatic triggering, fallback, failure, retry, escalation, or recovery behavior;
- visibility, hiding, deletion, summarization, notification, or silence;
- permissions, roles, data access, privacy, or irreversible effects;
- included scope, excluded scope, compatibility, or release behavior.

When uncertain, present the delta instead of silently promoting it.

## Decision Delta Shape

Keep the request compact and decision-oriented:

| Proposal | Why it came up | User-visible impact | Provenance | Status |
| --- | --- | --- | --- | --- |
| <exact proposed rule> | <evidence or tradeoff> | <what changes> | Agent proposal | needs confirmation |

Recommend an option when useful, but do not hide the alternative. If one answer
would materially change several coupled rules, present them as one explicit
bundle. Otherwise keep them separately confirmable.

## Behavioral Regression Scenarios

### Bounded activity feed

Input intent: replace repetitive internal progress with useful user-facing
commentary.

The following are not implied by that intent: a five-message cap, a 30-second
window, a 512-character bound, silence when no commentary exists, dropping a
pending update at terminal, or hiding an entire class of conversation. PM may
recommend any of them, but must expose each material rule or an explicit coupled
bundle as `Agent proposal` before canonicalizing it.

Expected behavior:

- The canonical record may state the confirmed outcome: meaningful commentary
  replaces internal event spam.
- Numerical limits and silence/visibility rules remain in `Decision Delta` until
  confirmed.
- Detailed sanitization, deduplication, replay, and test cases stay in the PM
  technical thread or Dev plan unless they alter the product decision.

### Cross-executor implementation and review

Input intent: implementation uses one executor and review uses another.

The following are separate product decisions: whether review starts
automatically, whether it is a new task, whether it is read-only, whether a
missing reviewer route fails or falls back, whether legacy routing remains,
whether findings may trigger fixes, and whether v1 permits multiple reviewers.

Expected behavior:

- PM presents the unconfirmed decisions as a compact delta rather than filling
  them in as edge-case resolutions.
- Atomic route capture, idempotent handoff creation, restart recovery, and secret
  safety may be recorded as engineering invariants without expanding the human
  canonical description.
- Readiness cannot return `ready` while any material proposal remains
  unconfirmed.

### Bug continuation after diagnosis

Input intent: fix a missing legacy avatar. Diagnosis also discovers legacy cover
records affected by the same migration gap and recommends repairing both. The
user then says `$pm 继续推进这个 issue` without answering an explicit avatar-only
versus avatar-and-cover approval question.

Expected behavior:

- Treat the continuation as permission to keep running PM, not confirmation of
  the expanded cover scope.
- Keep the avatar restoration tied to the original report. Classify cover scope
  as an `Agent proposal` until the user explicitly approves it or a verified
  inherited contract proves it is already required.
- Keep exact-path matching, idempotency, and non-overwrite as engineering
  invariants when they do not alter observable product policy.
- Stop before canonicalizing avatar-and-cover scope and ask the smallest explicit
  product question.

## Regression Assertions

- `Open Questions: None` or an equivalent ready claim is invalid when a material
  agent proposal remains unconfirmed.
- Repeating one proposal in requirements, acceptance criteria, edge cases, and
  technical constraints does not increase its authority.
- A workflow-continuation command is not decision confirmation unless it directly
  answers an explicit pending approval request containing the exact proposal.
- PM detail may be extensive in the threaded appendix; the canonical issue must
  remain a high-density statement of intent, confirmed behavior, scope, and
  critical acceptance.
