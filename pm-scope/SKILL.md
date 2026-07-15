---
name: pm-scope
description: >-
  Define the smallest coherent version of a product change worth building. Use for MVP boundaries, in-scope and out-of-scope decisions, deferred work, dangerous areas, and split recommendations; leaves a comment-only PM artifact for later spec synthesis.
---

# PM: Scope

Turn a framed problem into a buildable product boundary.

## Workflow

1. Confirm the problem, target user, and desired outcome.
2. Identify the smallest version that creates a complete user-visible or operator-visible outcome.
3. Name what is in scope, out of scope, deferred, and dangerous to touch.
4. Split work only when release timing, owner, risk, dependency, or acceptance criteria differ.
5. Post the scope artifact as an issue comment when tracker tools are available.
6. For the default dev-ready workflow, route next to `$pm-spec` after scope is stable. Insert UX state, UI design, backlog, strategy, or research work only when it materially changes requirements or readiness.

## Scope Rules

- Prefer end-to-end vertical slices over architecture-layer or phase tickets.
- Do not split one outcome into "Design X", "Implement X", and "QA X" tickets.
- Keep research/spike work separate only when it resolves a standalone uncertainty before build scope can be trusted.
- Add explicit non-goals so adjacent features do not enter the current release silently.
- Call out dangerous areas when touching them could create data loss, privacy risk, migration risk, performance regression, or user-trust failure.

## Tracker Writes

- Do not edit the issue description.
- Do not update assignee, labels, priority, status, or other tracker metadata.
- Leave the scope artifact as an issue comment when tools allow.
- If tracker tools are unavailable, provide the exact comment text for the user or `$pm-spec` to consume.

## Sub-Agent Contract

This skill is safe to run inline or as a bounded sub-agent. When delegated:

- Use only the request, provided sources, and directly referenced tracker context.
- Produce the scope artifact and any allowed tracker comment or draft.
- Follow this skill's tracker-write rules; do not edit issue descriptions unless this skill explicitly owns that write.
- Return sources read, writes applied or drafts, blockers, and open questions.

## Output

```markdown
## Scope

### In Scope
- <Included behavior or deliverable.>

### Out of Scope
- <Explicit non-goal.>

### Deferred
- <Follow-up that is valuable but not needed now.>

### Dangerous To Touch
- <Area, risk, and guardrail.>

### Split Recommendation
<One ticket, child tickets, spike first, or defer. Explain why.>

### Recommended Next Step
<Usually `$pm-spec` for the default dev-ready workflow; otherwise route to UX state, UI design, backlog, strategy, research, or readiness review and explain why.>
```
