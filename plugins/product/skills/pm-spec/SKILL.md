---
name: pm-spec
description: Synthesize confirmed product scope or a diagnosed bug into a concise PRD or canonical issue title and description.
metadata:
  owner: jay1803
  family: product
  maturity: stable
  distribution: product
---

# PM: Spec

Produce the human-reviewable product contract for development. Preserve deep
agent detail in the PM thread or later Dev artifacts instead of using the
canonical issue description as an exhaustive execution plan.

For issue lifecycle work, consume the [working context](../pm/references/working-context.md)
and confirmed delta. Use the [state machine](../pm/references/issue-state-machine.md)
for unresolved decisions or applicable review changes; do not rerun intake or
fetch unchanged history. Standalone invocation remains a direct Spec entry.

For a standalone analysis or draft, follow the
[Product Artifact Contract](../pm/references/artifact-contract.md) and complete
the requested artifact without tracker setup. The tracker steps below apply
only to an issue-bound lifecycle or authorized publication.

Review prerequisites below use the shared state-machine freshness and explicit
user-override rules. A disclosed skip is not an approval and never resolves an
unconfirmed product decision.

## Workflow

1. Consume the current canonical title/description, exact confirmed change and
   relevant provenance from the working context. Read only missing/stale sources;
   attachments, docs and history are conditional. Reuse the verified PM root;
   missing root initialization is a bounded `$pm` operation, not a new PM chain.
   An upstream unresolved decision returns `upstream_blocked` without another
   analysis or tracker comment.
2. Compare the candidate with the exact request, inherited behavior and confirmed
   decisions. Apply the authority gate below. Verify the single Product Decision
   record covers material user answers before writing. A newly discovered
   proposal returns its exact Decision Delta; reuse the existing result record
   only when a durable blocker is needed. Do not write canonical fields or add
   `scoped` while the decision is unresolved.
3. Reuse applicable Solution Review and Design evidence. Missing required inputs
   return to their owner. Load [technical constraints](references/technical-constraints.md)
   only when capability, compatibility or runtime acceptance could change scope.
   Do not add an obligatory review/design/technical phase.
4. Write concise observable behavior, scope and critical acceptance using the
   information contract below. Preserve an accurate title; reconcile obsolete
   active text with confirmed changes. Apply title/description together when
   supported; verify changed fields under the
   [tracker contract](../pm/references/tracker-contract.md). If no delta exists,
   verify the existing contract without a no-op write. Keep detailed mechanics
   and test matrices in source artifacts or the Dev plan.
5. Assign to the current/requesting user when known and authorized. Align
   acceptance labels; add `scoped` only after both canonical fields are verified
   and no material decision remains. An unavailable write produces an unapplied
   draft, never a successful result.
6. Return canonical binding, provenance and actual readback to the same context.
   A successful write/verification advances directly to readiness within an
   existing PM lifecycle; no second intake or routing call. A standalone request
   stops at its specified artifact. Use the combined handoff for the write
   receipt, with a separate compact receipt only when needed before a wait or
   for an independently requested Spec artifact.

## Decision Authority Gate

PM may discover and recommend behavior, but it may not silently decide product
policy for the user.

The following newly introduced rules normally require confirmation: defaults,
limits, caps, timeouts, retention, automatic triggers, fallback, failure or
recovery behavior, visibility or silence, permissions, irreversible effects,
compatibility changes, and scope cuts. Present the recommendation and impact;
do not launder it into authority by repeating it across requirements,
acceptance criteria, edge cases, or technical constraints.

Verified engineering invariants such as atomicity, idempotency, concurrency
safety, restart recovery, and secret handling may be documented without a
product decision when they do not change observable behavior. They usually
belong in the threaded technical artifact or Dev plan.

Read [Decision Provenance](references/decision-provenance.md) when auditing an
existing spec, when a general user request is being converted into exact policy,
or when a broad approval might not cover newly added parameters.

Do not mark a proposal `User confirmed` solely from `继续`, `继续推进`, `下一步`,
`$pm continue`, `proceed`, or similar workflow-control language. Preserve the
proposal as unresolved unless the immediately pending question explicitly asked
the user to approve that exact proposal bundle.

Read [Acceptance Classification](references/acceptance-policy.md) when writing
acceptance: apply its unattended engineering boundary as well as P2/P3
classification. Put real-device/account/environment tests in nonblocking
recommendations or a materially necessary separate human acceptance ticket;
do not turn those tests into implementation acceptance gates.

## Canonical Information Contract

The canonical issue description is the human approval layer. Each line should
carry one of these kinds of information:

- product intent or observable outcome;
- confirmed behavior or a verified inherited contract;
- a meaningful scope boundary;
- a critical acceptance outcome;
- executable human acceptance instructions when separately required.

Avoid repeating the same idea as problem, goal, user story, requirement,
acceptance criterion, edge case, and risk. Combine overlapping context into one
`Outcome` section. Include only non-goals that prevent a plausible scope
misread. Do not impose an arbitrary word or bullet limit; optimize for decision
density and scanability.

Keep these outside the canonical description unless they are themselves the
product promise:

- exhaustive edge-case and error matrices;
- stress, concurrency, replay, restart, and fault-injection cases;
- file paths, code symbols, schemas, snippets, and architecture;
- detailed test seams, fixtures, commands, and evidence formats;
- rollout mechanics, dependency narration, and next-workflow instructions.

## Conversation-to-PRD Mode

- Synthesize the current conversation and directly referenced context without a
  broad interview or filling every possible template section.
- Ask only about a material Decision Delta. Non-material implementation choices
  can remain engineer-owned in the threaded appendix.
- Preserve exact user wording when it defines the product promise.
- If publishing is authorized, apply the title and canonical description only
  after the Decision Authority Gate passes.

## Bug Synthesis Mode

- Read the original report, triage brief, diagnosis evidence, and later product
  decisions.
- Keep root-cause mechanics in the diagnosis comment unless they define an
  externally visible constraint.
- Write the title around the user-visible failure and restoration outcome.
- Keep expected behavior, actual impact, restoration scope, critical guardrails,
  and observable acceptance in the canonical record.
- A diagnosis may suggest a product policy, but it does not authorize that
  policy. Route unresolved behavior back to `$pm-scope`,
  or user confirmation as appropriate.

## Issue Record Write Authority

- Own the final dev-ready issue title and description.
- Read the existing record and relevant PM thread before writing either field.
- Synthesize working notes; do not paste or concatenate stage artifacts.
- Reconcile obsolete active requirements with exact later user-confirmed
  decisions and write the current effective contract. Preserve the old source
  and change provenance in the PM thread. If authority is actually ambiguous,
  surface a Decision Delta rather than selecting a side.
- Apply confirmed project-wide changes only to the assigned issue. Return
  affected sibling/cross-parent drafts to the project controller; that owner
  inventories and routes each canonical update. A later comment must not remain
  the permanent substitute for updating contradictory active text.
- Apply title and description together when tools allow.
- Keep `human-acceptance-required` and the canonical acceptance instructions
  consistent.
- Add or retain `scoped` only after the provenance gate and canonical write both
  pass.
- If tools are unavailable, provide the exact replacement title and description
  and state that they remain unapplied.
- Return a concise verified write summary for the combined handoff. When a
  separate receipt is needed, publish only under the existing root or provide
  the exact draft if reply/edit support is unavailable.
- Reuse an existing `## Spec Write Result` comment ID when a separate receipt
  is needed; do not create one merely to satisfy workflow history.
- The summary is a mutation receipt, not another spec: state only what canonical
  fields changed, whether provenance and `scoped` gates passed, where any
  detailed appendix lives, and the next owner. Do not restate outcome, scope,
  decisions, acceptance, or prior evidence.

## Output

When a material proposal remains unconfirmed, stop with:

```markdown
Issue: <ID>
Decision: blocked on product confirmation

## Decision Delta
| Proposal | Why it came up | User-visible impact | Provenance | Recommendation |
| --- | --- | --- | --- | --- |
| <exact rule> | <evidence or tradeoff> | <what changes> | Agent proposal | <recommended option> |

Canonical write: not applied
Scoped: not applied
Next step: user confirmation, then rerun `$pm-spec`
```

When the gate passes, write this compact shape and omit empty optional sections:

```markdown
Issue title: <concise agreed outcome and scope>

Issue description:

## Product Contract

### Outcome
<Who needs what outcome, why current behavior is insufficient, and what becomes true.>

### Core Behavior
- <Confirmed observable behavior.>

### Scope Boundary
- In: <meaningful included boundary.>
- Out: <only adjacent behavior likely to be misread as included.>

### Confirmed Product Decisions
- <Only a non-obvious decision not already clear from Core Behavior, plus its user-confirmed or inherited source. Omit when unnecessary.>

### Critical Acceptance
- <Small set of observable outcomes that prove the product promise.>

### Nonblocking Recommendations
<Omit when empty; otherwise P2/P3 items, suggested real-environment tests or a separate human acceptance follow-up, with deferred status.>

### Human Acceptance
<Omit unless required. When required, include environment/build, tester or role,
prerequisites, numbered actions, expected results, evidence, and blank Accepted
By / Acceptance Date fields.>
```

The write result carries title/canonical status, provenance, `scoped`, and
supporting links without reproducing the spec. The next owner is readiness or
an exact newly discovered decision gap. Do not call specification alone
`PM complete`, `PM 收口`, or `dev-ready`.
