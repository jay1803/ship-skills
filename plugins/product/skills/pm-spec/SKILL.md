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

For issue lifecycle work, apply the shared [Issue PM State Machine](../pm/references/issue-state-machine.md),
including its downstream entry guard, Product Decision record, and single
stage-comment identity.

For a standalone analysis or draft, follow the
[Product Artifact Contract](../pm/references/artifact-contract.md) and complete
the requested artifact without tracker setup. The tracker steps below apply
only to an issue-bound lifecycle or authorized publication.

Review prerequisites below use the shared state-machine freshness and explicit
user-override rules. A disclosed skip is not an approval and never resolves an
unconfirmed product decision.

## Workflow

1. Read the original issue title and description, labels, status, priority,
   assignee, comments, attachments, linked context, and available docs.
2. Read the single `## PM Workflow` root and relevant replies or diagnosis
   evidence. If no PM root exists, use `$pm` intake/root initialization instead of
   creating a separate top-level comment.
   If an upstream stage owns an unresolved Decision Delta or required artifact,
   return `upstream_blocked` to the controller without analysis or a Linear
   comment. Do not create a duplicate Spec Gate for an upstream blocker.
3. Apply Solution Review only when required by the state machine's material
   simplification/rule criteria or an explicit request/policy. Reuse current
   evidence; route an applicable missing/stale review to its owner. A non-Bug
   label does not by itself require review. Check
   [technical constraints](references/technical-constraints.md) before writing
   when capability, compatibility or runtime acceptance could change scope.
4. Establish the intent baseline: the user's exact request, verified inherited
   behavior, and decisions the user explicitly confirmed. A continuation command
   is workflow authorization, not product confirmation, unless it directly
   answered an explicit pending approval request containing the exact proposal.
5. Compare the candidate contract with that baseline. Classify every new
   material rule using [Decision Provenance](references/decision-provenance.md).
6. Verify that every user-confirmed material proposal is recorded in the single
   `## Product Decision` reply with its exact answer and source. If the user has
   answered elsewhere, record or update that reply before canonical writing.
7. If this stage itself discovers a new material `Agent proposal`, do not edit the issue
   title or description, do not add `scoped`, and do not claim readiness. Reply
   by creating or updating the one `## Spec Write Result` comment with a compact
   Decision Delta, enter `unresolved_decision`, and stop for the user's decision.
8. When the delta is empty or confirmed, write observable product behavior and
   only the critical acceptance outcomes needed to preserve the promise. Keep
   detailed edge cases, test matrices, implementation mechanics, and verifier
   procedures in the PM thread or Dev plan.
9. Rewrite a vague, placeholder, or outdated title. Preserve one that already
   reflects the agreed outcome and scope.
10. Update the canonical issue title and description together when tracker tools
   allow. This is the only PM skill in the default chain that rewrites them.
11. When current goal, behavior, constraints and needed Design evidence are
    confirmed, route to `$pm-readiness-review`. Resolve material technical or
    Design choices before canonical writing, not through a mandatory post-spec
    stage. Return a newly discovered product delta to its owner for confirmation.
12. Assign the issue to the current/requesting user when identity is known. Add
    or preserve `human-acceptance-required` when required. Add `scoped` only
    after both canonical fields are written or verified and no material decision
    remains unconfirmed.
13. Return the verified write result to the controller for the combined
    readiness/handoff record. Post a separate compact write receipt only for an
    independently requested spec artifact or evidence needed before a wait;
    reuse its comment ID. Do not repeat the canonical contract.

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
