---
name: pm-technical-boundary
description: >-
  Clarify product-level technical constraints without designing architecture. Use for platform support, API behavior, backwards compatibility, migration risk, performance expectations, privacy rules, and provider limitations; leaves a comment-only PM artifact unless creating separate discovery work.
---

# PM: Technical Boundary

Name the product constraints engineering must respect. Do not solve the architecture.

## Workflow

1. Confirm the product behavior and user promise.
2. Identify constraints that affect scope, acceptance criteria, rollout, compatibility, privacy, performance, or data safety.
3. Verify external provider, API, platform, or policy constraints when available. Do not invent unsupported capabilities.
4. Mark each constraint as required now, deferred, unknown, or engineer-owned.
5. Post technical product constraints as an issue comment when tracker tools are available.
6. For the default dev-ready workflow, route next to `$pm-readiness-review` after constraints are explicit. Route to discovery only when a product-level constraint cannot be stated safely.

## Boundary Areas

- Platform and version support.
- API behavior, provider capability, rate limits, auth, quotas, and fallback behavior.
- Backwards compatibility, migration, existing data, upgrade, and rollback.
- Performance, latency, storage, battery, offline, and reliability expectations.
- Privacy, security, retention, permissions, and user consent.
- Operational, support, observability, and release constraints.

## Tracker Writes

- Do not edit the issue description.
- Do not update assignee, labels, priority, status, or other tracker metadata unless creating a separate discovery issue requested by the workflow.
- Leave the technical-boundary artifact as an issue comment when tools allow.
- If tracker tools are unavailable, provide the exact comment text for readiness review to consume.

## Sub-Agent Contract

This skill is safe to run inline or as a bounded sub-agent. When delegated:

- Use only the request, provided sources, and directly referenced tracker, docs, API, or provider context.
- Produce the technical product constraints and any allowed tracker comment, discovery issue, or draft.
- Follow this skill's tracker-write rules; do not edit issue descriptions unless this skill explicitly owns that write.
- Return sources read, writes applied or drafts, blockers, and open questions.

## Output

```markdown
## Technical Product Constraints

| Constraint | Product Impact | Requirement | Owner | Status |
| --- | --- | --- | --- | --- |
| <constraint> | <why it matters> | <must/should behavior> | <PM/eng/design/data> | <required | deferred | unknown> |

### Required Product Decisions
- <Decision needed before engineering can proceed.>

### Discovery Needed
- <Question for engineering, API docs, provider validation, or spike.>

### Recommended Next Step
<Usually `$pm-readiness-review` for the default dev-ready workflow; otherwise route to spec, backlog, or technical discovery and explain why.>
```
