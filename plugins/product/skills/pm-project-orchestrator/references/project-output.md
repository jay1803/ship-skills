# Project Output Examples

Read when writing a project brief or formal execution plan. Include only
fields relevant to the requested scope; do not repeat the project description
in the final response.

## Project Description Shape

Use this structure when updating or drafting the project description:

```markdown
## Project Brief

What:
Why:
For whom:
Outcome:
Success signal:
Non-goals:

## Milestones

| Milestone | Outcome | Included issues | Exit criteria |
| --- | --- | --- | --- |
| <name> | <user/business outcome> | <issue IDs or draft titles> | <observable done state> |

## Dependency Map

- <Issue A> -> <Issue B>: <B depends on A because...>

## Risk Map

- Product:
- Technical:
- UX:
- Data / analytics:
- Privacy / security:
- External dependencies:
- Rollout / operations:

## Cutline

### v1
- <issue or capability>

### Deferred
- <issue or capability>

### Rejected
- <issue or capability and reason>

## Assignment Plan

| Issue | PM state | Next PM skill | Execution | Hard predecessors | Owner/status |
| --- | --- | --- | --- | --- | --- |
| <issue> | <earliest missing artifact> | <$pm-...> | <direct/parallel/serial/blocked> | <IDs/none> | <owner/status> |

## PM Execution Waves

- Wave 0: <controller-owned project setup>
- Wave 1: <parallel issue IDs and why safe>
- Wave 2: <serial/dependent issue IDs and unlock conditions>
- Blocked: <issue, blocker, affected successors>

## Open Questions

- <only questions that change milestone, scope, dependency order, or readiness>
```

## Output

```markdown
## PM Project Orchestration

Project:
Delivery Shape: <materialized project/issue-set | provisional umbrella: multi/ambiguous>
Mode: <plan only | execute>
Decision: <updated | running | complete | partial | blocked | draft only>

### Active Goal
- Type: <Project Structured | PM Ready | Project Plan Verified>
- Source: <inferred from live state | user provided>
- Objective:
- Completion criteria:
- Successor goal: <goal or none>

### Project Brief
<brief>

### Dependency Map
- <Issue A> -> <Issue B>: <reason>

### Risk Map
- Product:
- Technical:
- UX:
- Data / analytics:
- Privacy / security:
- External:

### Cutline
- v1:
- Deferred:
- Rejected:

### Assignment Plan
- <Issue>: <state> -> <next PM skill> - <direct/parallel/serial/blocked reason>

### PM Execution Waves
- Wave 0:
- Active wave:
- Later waves:
- Blocked branches:

### Controller Status
- Goal status:
- Worker registry:
- Verified terminal issues:
- Waiting issues:
- Next controller action:

### Tracker Updates
- Project description: <updated | draft>
- Milestones: <created/updated/draft>
- Issues: <created/updated/draft>
- Dependencies: <created/updated/draft>

### Open Questions
- <question or "None.">

### Dev Project Handoff
- Ready issues:
- PM dependency order:
- Deferred/rejected issues:
- Remaining blockers:
```
