---
name: pm-ux-state
description: >-
  Define product-level UX flow, involved screens, user-facing states, edge cases, copy, and interaction behavior for a product change. Use when Codex needs to clarify journeys, navigation, permissions, onboarding, recovery, cross-screen behavior, empty/loading/error/offline states, cancellation, lifecycle behavior, or acceptance criteria before design or engineering.
---

# PM: UX State

Make the user journey and user-facing state model complete enough for design, engineering, and QA.

## Boundary

- Own workflow shape, involved screens, state behavior, recovery paths, product copy direction, and state-level acceptance criteria.
- Stay at the product behavior layer. Do not choose component styling, detailed layout, or visual hierarchy unless needed to explain behavior.
- Route to `$pm-ui-design` when screen layout, visual hierarchy, controls, or UI copy placement need a concrete screen spec.
- Do not implement code, write architecture, or redesign unrelated surfaces.

## Input Routing

- Linear issue: read the issue, comments, labels, acceptance criteria, linked docs, and relevant product context before proposing UX.
- Raw requirement: clarify scope through `$pm` or `$pm-problem-framing` when the user problem or promise is unclear.
- Existing feature improvement: inspect the current workflow through repo files, screenshots, docs, running app behavior, or recent context when available.

If current workflow cannot be inspected, state the gap and proceed only with clear assumptions or ask for the missing context when it changes scope or user trust.

## Workflow

1. Confirm the core user promise, target user, and success criteria.
2. Map the existing workflow when the feature exists or is being extended.
3. Identify every involved screen, including unchanged entry points and recovery destinations.
4. Define the smallest coherent user flow that satisfies the promise.
5. Identify states that affect trust, completion, recovery, privacy, accessibility, or acceptance criteria.
6. Decide which states are in scope, deferred, or intentionally ignored.
7. Write expected user-facing behavior and product copy direction.
8. Add acceptance criteria for behavior and states that must be testable.

## Flow Checklist

- Entry point, primary path, completion moment, and exit path.
- New screens and existing screens that change.
- Navigation, handoff, deep link, back/cancel, retry, and recovery behavior.
- Permissions, authentication, privacy, access denied, onboarding, and first-run moments.
- Backgrounding, lifecycle, multi-device, cross-platform, localization, accessibility, and offline behavior.

## State Checklist

- Empty or first-run state.
- Loading, progress, long-running, retry, cancellation, and partial completion.
- Error, network failure, provider failure, stale data, quota, billing, or rate limit.
- Permission, authentication, privacy, and access-denied states.
- Offline, backgrounding, multi-device, cross-platform, localization, accessibility, and lifecycle behavior.
- Destructive actions, data loss, abuse, recovery, support, and rollback.

Only include states that can actually occur. Mark speculative states as deferred or ignored instead of inflating scope.

## Tracker Write Authority

Only post tracker comments after the user approves the UX flow and state brief, unless the user explicitly asks for a draft only. Do not edit issue descriptions; `$pm-spec` owns canonical description updates.

When live tracker tools are unavailable, produce exact comment text and metadata suggestions instead of claiming updates were applied.

## Sub-Agent Contract

This skill is safe to run inline or as a bounded sub-agent. When delegated:

- Use only the request, provided sources, and directly referenced tracker or product context.
- Produce the UX flow and state brief plus any allowed tracker comment or draft.
- Follow this skill's tracker-write rules; do not edit issue descriptions.
- Return sources read, writes applied or drafts, blockers, and open questions.

## Output

```markdown
## UX Flow & State Brief

### Requirement Clarity
- Status: Clear / Needs clarification
- Notes: <confirmed facts, assumptions, or remaining blockers>

### Design Goal
<The user outcome this workflow must create.>

### Existing Workflow
<Current flow summary, or "Not inspected" with assumptions.>

### Screens Involved
New screens:
- <Screen name>: <purpose and key content/actions>

Existing screens to update:
- <Screen name>: <what changes and why>

### User Workflow
1. <User step>
2. <User step>
3. <User step>

### UX State Checklist
| State | Trigger | User-Facing Behavior | Copy | Recovery | Scope |
| --- | --- | --- | --- | --- | --- |
| <state> | <condition> | <behavior> | <copy or copy direction> | <recovery path> | <in scope | deferred | ignored> |

### Acceptance Criteria
- Given <state trigger>, when <user action/system event>, then <observable result>.

### Open Decisions
- <Only decisions that change scope or user trust.>
```
