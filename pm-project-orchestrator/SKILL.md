---
name: pm-project-orchestrator
description: >-
  Product/project orchestrator for Linear projects, epics, initiatives, roadmap slices, or groups of related product issues. Use when the input is a project rather than one issue, and the work needs a project brief, valuable milestones, issue setup, dependency map, risk map, v1/deferred/rejected cutline, and an assignment plan for which narrow PM skills should process which issues.
---

# PM: Project Orchestrator

Turn a product project into a structured product execution surface. The input is a project, initiative, epic, milestone, or issue family; the output is an updated project description plus milestone and issue setup that lets single-issue PM work proceed cleanly.

## Boundary

- Own the project-level product shape: outcome, audience, milestones, issue decomposition, dependencies, risks, cutline, and PM assignment.
- Do not write every child issue's final PRD/spec. Route child issues to `$pm`, `$pm-spec`, `$pm-ux-state`, `$pm-ui-design`, `$pm-data-analytics`, `$pm-technical-boundary`, or `$pm-readiness-review` when they need per-issue artifacts.
- Use `$pm-backlog` when the project needs a clean issue tree, follow-up issues, duplicate checks, dependencies, or milestone assignment.
- Use `$pm-strategy` when product direction, roadmap fit, segment focus, sequencing, or product-principle tradeoffs need shaping.
- Use `$proj-bet` when the open question is whether the project should exist, continue, or be stopped.
- Use `$pm-readiness-review` only after a child issue has enough PM artifacts to judge dev readiness.
- If the request is one ordinary issue, route to `$pm` instead of this skill.

## Workflow

1. Identify the project source: Linear project, epic, parent issue, roadmap item, milestone, document, or user-provided brief.
2. Read current project state before changing it: description, goals, status, milestones, linked issues, child issues, labels, owners, comments, docs, designs, analytics context, and known technical constraints when available.
3. Separate existing commitments from assumptions. Preserve useful project description content rather than overwriting it blindly.
4. Write the project brief: what is being built, why now, for whom, user/business outcome, success signal, non-goals, and decision context.
5. Build the dependency map. Represent dependencies as issue-to-issue relationships and call out unknown or missing source-of-truth links.
6. Build the risk map across product, technical, UX, data, privacy, analytics, migration, rollout, external dependency, and operational risk.
7. Set the cutline:
   - **v1**: must ship to deliver the core outcome.
   - **Deferred**: valuable but not needed for the first coherent version.
   - **Rejected**: not aligned, duplicate, too risky, or not worth carrying.
8. Create the assignment plan. For each issue or missing issue, choose the next PM skill and state why.
9. Set up milestones and issues when tools allow and the destination is clear. Otherwise, produce tracker-ready drafts.
10. Update the project description with the canonical project orchestration record. Do not edit child issue descriptions except when creating new child issues; per-issue description authority remains `$pm-spec`.

## Assignment Rules

- Use `$pm-intake` for raw or unclassified issues.
- Use `$pm-bug-triage` for bug-labeled or bug-shaped issues.
- Use `$pm-problem-framing` when the user/problem is vague.
- Use `$pm-strategy` when product direction, priority order, roadmap fit, segment focus, or business goal needs strategic shaping.
- Use `$proj-bet` when the open question is go/no-go commitment rather than project decomposition.
- Use `$pm-scope` when v1 boundaries, non-goals, or split decisions are unclear.
- Use `$pm-spec` when the issue is ready for canonical PRD/requirements/acceptance criteria.
- Use `$pm-ux-state` when workflows, states, edge cases, permissions, offline/error/loading behavior, recovery, or product copy direction materially affect acceptance.
- Use `$pm-ui-design` when visible screen layout, hierarchy, controls, UI copy placement, or platform UI decisions materially affect implementation readiness.
- Use `$pm-data-analytics` when success metrics, events, learning questions, or failure signals are missing.
- Use `$pm-technical-boundary` when platform, API behavior, compatibility, migration, privacy, or performance constraints affect product scope.
- Use `$pm-backlog` when the issue tree, milestones, dependencies, duplicates, or follow-ups need cleanup.
- Use `$pm-readiness-review` when a child issue appears dev-ready and needs a final product gate.

## Sub-Agent Delegation

This skill can be run inline or as a bounded project sub-agent. When delegated, it must return the project brief, issue assignment plan, tracker writes applied or drafts, blockers, and open questions.

When this skill delegates child issue work to narrow PM skills, keep writes to the same project or issue family serial. Do not run parallel PM sub-agents that may update the same project description, issue tree, milestone, or child issue.

Child PM sub-agents should receive the child issue ID, relevant project context, the exact artifact requested, allowed tracker writes, and stop conditions. Per-issue description authority still belongs to `$pm-spec`.

## Tracker Write Authority

- This skill may update the project description, project status fields, milestone definitions, project-level dependency notes, and issue membership when tools allow.
- This skill may create child issues, follow-up issues, research issues, and rejected/closed issue recommendations when the project cutline requires them.
- Do not rewrite an existing child issue's canonical product spec. Route that to `$pm-spec`.
- When live tracker tools are unavailable, produce exact project-description, milestone, issue, and dependency drafts instead of claiming updates were applied.

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

| Issue | Next PM skill | Reason | Owner/status |
| --- | --- | --- | --- |
| <issue> | <$pm-...> | <why this is the next artifact> | <owner/status> |

## Open Questions

- <only questions that change milestone, scope, dependency order, or readiness>
```

## Output

```markdown
## PM Project Orchestration

Project:
Decision: <updated | draft only | blocked>

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
- <Issue>: <next PM skill> - <reason>

### Tracker Updates
- Project description: <updated | draft>
- Milestones: <created/updated/draft>
- Issues: <created/updated/draft>
- Dependencies: <created/updated/draft>

### Open Questions
- <question or "None.">
```
