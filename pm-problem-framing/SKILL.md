---
name: pm-problem-framing
description: >-
  Convert vague product ideas, requests, and issues into a clear user or business problem. Use when the affected user, job, blocker, impact, current behavior, or desired outcome is unclear; leaves a comment-only PM artifact for later spec synthesis.
---

# PM: Problem Framing

Turn a request into a problem statement before scoping or writing requirements.

## Workflow

1. Gather available context from the request, tracker, docs, screenshots, current product behavior, or linked discussion.
2. Identify who is affected, what they are trying to do, what blocks them, why it matters, and what changes if solved.
3. Separate the problem from the proposed solution. Keep the user's proposed solution as an option, not the framing itself.
4. Ask only questions that change the problem statement or make the target user materially different.
5. Post the problem statement as an issue comment when tracker tools are available.
6. For the default dev-ready workflow, route next to `$pm-scope` once the problem statement is clear. Route elsewhere only when strategy, research, or a non-PM owner is blocking.

## Framing Checks

- User: who is affected, and in what situation?
- Job: what are they trying to accomplish?
- Current blocker: what fails, slows down, confuses, or creates risk today?
- Impact: what user, business, trust, support, or operational outcome changes?
- Desired outcome: what would be observably better after solving it?
- Evidence: what facts support the problem, and what is still an assumption?

## Tracker Writes

- Do not edit the issue description.
- Do not update assignee, labels, priority, status, or other tracker metadata.
- Leave the problem-framing artifact as an issue comment when tools allow.
- If tracker tools are unavailable, provide the exact comment text for the user or next PM step to post.

## Sub-Agent Contract

This skill is safe to run inline or as a bounded sub-agent. When delegated:

- Use only the request, provided sources, and directly referenced tracker context.
- Produce the problem statement and any allowed tracker comment or draft.
- Follow this skill's tracker-write rules; do not edit issue descriptions unless this skill explicitly owns that write.
- Return sources read, writes applied or drafts, blockers, and open questions.

## Output

```markdown
## Problem Statement

For <target user>, when <situation>, they are trying to <job>. Today, <current blocker>. This matters because <impact>. Solving it should make <desired outcome> true.

### Evidence
- <Confirmed fact or source.>

### Assumptions
- <Working interpretation that needs validation.>

### Open Questions
- <Only questions that change the problem or target user.>

### Recommended Next Step
<Usually `$pm-scope` for the default dev-ready workflow; otherwise route to strategy, research, backlog, or stop and explain why.>
```
