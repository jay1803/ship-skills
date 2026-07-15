---
name: pm-readiness-review
description: >-
  Run the pre-development product gate. Use to decide whether an issue is ready for coding, blocked by ambiguity, too large, strategically weak, duplicate, should be split, or should be rejected; leaves a readiness comment and updates status only when clear.
---

# PM: Readiness Review

Decide whether product work is ready to hand to engineering.

## Workflow

1. Read the issue, spec, comments, labels, linked PRs, docs, and relevant context.
2. Check for a clear problem, target user, goal, scope, non-goals, acceptance criteria, edge-case handling, constraints, dependencies, owner, and labels.
3. Do not re-scope a `scoped` issue unless requirements changed or the user asks for a refresh.
4. Decide ready, blocked, split, reject, or defer.
5. Name the exact missing artifact or next route.
6. For the default dev-ready workflow, treat the required upstream artifacts as intake classification, problem statement, scope, product spec, and technical product constraints.
7. Post the readiness decision as an issue comment when tracker tools are available.

## Gate Criteria

- Problem and desired outcome are explicit.
- Scope and non-goals are testable.
- Acceptance criteria cover the core behavior and material edge cases.
- UX flow, states, and UI design artifacts are sufficient for user-facing work.
- Product-level technical constraints are explicit where they affect behavior, compatibility, privacy, migration, performance, or rollout.
- Dependencies and issue order are clear.
- The work is small enough to build and validate without hiding separate outcomes.
- The issue has completed the default PM chain or has equivalent content already present in the issue.

## Tracker Writes

- Do not edit the issue description.
- Leave the readiness decision as an issue comment when tools allow.
- Update status/readiness fields only when the workspace semantics are clear, for example ready, blocked, split, rejected, or deferred.
- Do not change assignee, labels, priority, or scope metadata unless the readiness decision requires a clearly supported blocker/status update.
- If tracker tools are unavailable, provide the exact readiness comment and status update draft.

## Sub-Agent Contract

This skill is safe to run inline or as a bounded sub-agent. When delegated:

- Use only the request, provided sources, and directly referenced tracker context.
- Produce the readiness decision and any allowed tracker comment, status update, or draft.
- Follow this skill's tracker-write rules; do not edit issue descriptions unless this skill explicitly owns that write.
- Return sources read, writes applied or drafts, blockers, and open questions.

## Output

```markdown
## Readiness Review

Decision: <ready | blocked | split | reject | defer>
Confidence: <high | medium | low>

### Findings
- <Readiness finding and evidence.>

### Required Before Build
- <Missing decision, spec, scope split, UX state, UI design, constraint, or dependency.>

### Recommended Route
<Use $dev, $dev --standard, or $dev-project-orchestrator; or route back to a PM skill.>
```
