---
name: dev-api-research
description: "Research third-party API or SDK capabilities and integration contracts when external behavior needs clarification."
metadata:
  owner: jay1803
  family: develop
  maturity: stable
  distribution: develop
---

# Dev: API Research

Research external APIs deeply enough for `$dev-planner` to design the integration without guessing.

Run before `$dev-planner` when the implementation depends on third-party APIs, SDKs, OpenAPI specs, webhooks, auth models, provider limits, pricing, data contracts, or sandbox behavior. If the broader technical direction is also unclear, pair this with `$dev-spike`.

## Boundary

- Own external source-of-truth questions whose answer changes the technical approach or feasibility decision.
- Use `$dev-debugger` first when the starting point is an observed defect and the root cause is not yet known. Route here from the diagnosis when provider behavior is the remaining unknown.
- Use `$dev-spike` for local feasibility and competing implementation paths; use this skill for facts that must be verified against the provider or its official contract.
- Do not design our internal API contract or implementation architecture; hand verified constraints to `$dev-api-steward` or `$dev-planner`.

## Source Rules

- Prefer current primary sources: official docs, OpenAPI/Swagger schema, official SDK repository, official examples, changelog, pricing page, limits page, status page, and security/webhook docs.
- Use secondary sources only to compare approaches or fill clearly labeled gaps.
- Browse or otherwise verify current docs when API behavior could have changed; do not rely on memory for limits, pricing, auth, scopes, or endpoint behavior.
- Capture source URLs or local paths. Do not paste long excerpts.
- If docs conflict, identify the contract applicable to the target API/SDK version and call out the conflict. A newer contract for a different version does not establish the target behavior.

## Research Scope And Sufficiency

State the decision or capability question first. Research only topics whose
answers could change that decision, an integration constraint, or a required
validation boundary. Auth, limits, pricing, pagination, webhooks, sandbox behavior,
and data mapping are prompts for relevant questions, not a mandatory checklist.

Reuse source evidence when its provider, version, operation, and scope match the
question and it is still current enough for the claim. Recheck volatile or
uncertain facts and conflicting sources; an old note does not prove current
pricing, limits, permissions, or endpoint behavior. Record the applicable version
and source so the next owner can assess freshness.

When local integration advice is requested, inspect the relevant client, model,
security boundary, or validation pattern. A capability-only request does not
require repository archaeology, object mapping, or comparing every integration
architecture. Missing local fit can remain explicit when it does not prevent
answering the provider question.

Stop when current primary evidence answers the deciding questions and identifies
material constraints, unresolved blockers, and the validation needed for a future
change. Do not keep browsing unrelated provider features to fill a report. If a
required fact cannot be verified, state the uncertainty and its impact instead of
inventing an answer or implying that integration may proceed.

## Workflow

1. Identify the API/use case, applicable version, and decision to resolve.
2. Verify the relevant official contract and record sources and decisive facts.
3. Inspect local fit, map data, or compare integration options only when those
   decisions are part of the request or necessary to answer it.
4. Return the supported conclusion, material constraints and uncertainty, and
   a named next owner or the investigate-only terminal below.

## Investigate-Only Terminal

When the canonical Issue Route receipt selects
`investigate/api-research` with `terminal_intent: diagnosis`, this skill stops
after the primary-source research brief. The brief records sources, facts,
confidence, options, constraints, affected boundary, validation needed for a
future implementation, and `conclusive`, `inconclusive`, `blocked`, or
`not-applicable` status. It may recommend `$dev-planner`, API stewardship,
or a delivery route, but it does not dispatch that owner.

The mutation budget is read-only: do not change provider configuration, secrets,
repository code, tracker state, branch, or PR. Current official sources and
local fit evidence do not authorize an integration. A later request to build,
repair, deploy, or close an issue must receive a fresh Issue Route receipt with
delivery authority and this brief as its resume anchor.

## Output

Lead with the answer or integration decision, then its primary-source evidence.
Include the applicable API/SDK version, source links, decisive constraints,
confidence, unresolved questions, and next action. For an integration assessment,
return `feasible`, `risky`, or `blocked`; for investigate-only work preserve its
terminal status and no-dispatch boundary.

Include local fit, required endpoints, auth/scopes, cost/limits, mapping, errors,
webhooks, retry/idempotency, security, sandbox, rollout or implementation options
when they affect the conclusion. Distinguish an unverified material fact from a
topic that is outside scope. Omit empty or irrelevant sections rather than filling
a provider-wide template. The brief should let the next owner act on verified
constraints without treating research as implementation authorization.
