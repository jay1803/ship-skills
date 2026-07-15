---
name: pm-intake
description: >-
  Classify raw product ideas, bugs, user requests, vague asks, and Linear issues. Use when PM work needs an issue type, urgency, owner, labels, confidence, tracker metadata updates, and next PM or non-PM route before deeper planning.
---

# PM: Intake

Classify the request before assigning deeper PM work. Intake decides what kind of work this is and what should happen next.

## Workflow

1. Read the raw request and any referenced issue, labels, comments, screenshots, PRs, or docs available through tools.
2. Classify the work type: feature, bug, UX polish, tech debt, growth experiment, research question, analytics gap, design debt, support/ops, or unclear.
3. Identify urgency from evidence, not vibes: user harm, revenue risk, data loss, regression, release blocker, strategic deadline, or routine backlog.
4. Recommend owner and route. Product behavior and feature scope can continue through PM; bugs should route to `$pm-bug-triage` before diagnosis or build work.
5. Post the intake classification as an issue comment when tracker tools are available.
6. Update tracker metadata when supported by available context: assignee, labels, priority, status, type, and owner. Assign to the current/requesting user when identity is known.
7. For the default dev-ready workflow, hand feature, UX polish, growth, analytics, design debt, and unclear product requests to `$pm-problem-framing` next unless the issue is already dev-ready or must exit to a non-PM route. Hand bug reports to `$pm-bug-triage`.

## Classification Rules

- If a Linear issue is labeled `Bug`, treat that as a hard signal for the bug route unless the user explicitly says to reclassify it.
- If bug evidence is unclear, route to `$pm-bug-triage` so expected behavior, actual behavior, affected platform, severity, user impact, and missing evidence are handled in the bug triage brief.
- For ambiguous issues that should become dev-ready, route next to `$pm-problem-framing` by default, even when the request already hints at a solution.
- Skip ahead to `$pm-scope`, `$pm-spec`, or `$pm-readiness-review` only when the earlier artifacts are already explicit in the issue or the user explicitly asks to skip.
- If the request is already implementation-ready, route to `$pm-readiness-review` or the engineering workflow instead of adding PM process.

## Tracker Writes

- Do not edit the issue description.
- Always leave the intake result as a comment on the issue when tools allow.
- Auto-update assignee, labels, priority, status, type, and owner when the target fields exist and the evidence supports the change.
- If tracker tools are unavailable, provide the exact intake comment and metadata update list.
- Do not ask before applying obvious metadata from the classification unless the update is ambiguous, destructive, or workspace-specific semantics are unclear.

## Sub-Agent Contract

This skill is safe to run inline or as a bounded sub-agent. When delegated:

- Use only the request, provided sources, and directly referenced tracker context.
- Produce the intake classification and any allowed tracker comment, metadata updates, or drafts.
- Follow this skill's tracker-write rules; do not edit issue descriptions unless this skill explicitly owns that write.
- Return sources read, writes applied or drafts, blockers, and open questions.

## Output

```markdown
## Intake Classification

Type: <feature | bug | UX polish | tech debt | growth experiment | research | analytics gap | design debt | support/ops | unclear>
Urgency: <critical | high | medium | low> - <why>
Owner: <PM | design | engineering | data | support | unclear>
Suggested Labels: <labels>
Confidence: <high | medium | low>

### Evidence
- <Fact from request, issue, label, comment, or linked context.>

### Next Step
<For the default dev-ready workflow, usually `$pm-problem-framing`; for bugs, usually `$pm-bug-triage`; otherwise name the early exit route and why.>

### Questions
- <Only questions required to classify or route safely.>

### Tracker Updates
- Assignee: <applied / recommended / unchanged and why>
- Labels: <applied / recommended / unchanged and why>
- Priority: <applied / recommended / unchanged and why>
- Status: <applied / recommended / unchanged and why>
```
