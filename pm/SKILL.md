---
name: pm
description: >-
  PM orchestrator for product-management work and issue kickoff. Use when the user asks for PM help, says "pm", gives a Linear issue ID to clarify or prepare for dev, asks to start/ship an issue, or needs product strategy, roadmap planning, project orchestration, intake, bug triage, requirement clarification, scoping, specs, UX/UI routing, technical constraints, readiness review, analytics, backlog decomposition, product PR review, or release learning.
---

# PM Orchestrator

Route product work to the narrow PM skill that owns the next artifact. The default workflow turns an ambiguous issue into a dev-ready issue:

`$pm-intake` -> `$pm-problem-framing` -> `$pm-scope` -> `$pm-spec` -> `$pm-technical-boundary` -> `$pm-readiness-review`

Bug workflow:

`$pm-intake` -> `$pm-bug-triage` -> `$dev-debugger` or the relevant engineering diagnosis workflow

Project workflow:

`$pm-project-orchestrator` -> per-issue `$pm` / narrow PM skills -> `$pm-readiness-review`

Strategy workflow:

`$pm-strategy` -> shaped roadmap projects to `$pm-project-orchestrator` -> child issues to `$pm` / `$pm-readiness-review`

If the primary question is whether to commit to a project at all, use `$proj-bet` before roadmap/project orchestration.

Issue kickoff workflow:

`$pm <Linear issue ID>` -> classify issue -> PM/bug path -> optional `$pm-ux-state` / `$pm-ui-design` routing -> optional `$design` artifact route -> `$project-manager` pre-dev status sync -> handoff packet for `$dev` or `$dev-project-orchestrator`

Do not load every PM worker skill by default. Load the next skill in the chain, carry forward its artifact, and stop only when a blocking decision needs user input or the issue is ready for engineering.

## Delegation Model

The PM orchestrator stays in the main agent. It owns sequence, accumulated context, tracker-write coordination, and the decision to stop for user input.

Narrow PM skills must be sub-agent compatible, but they are not sub-agent required.

- Run a PM skill inline for short routing, simple comments, a single tracker update, or tightly sequential context.
- Delegate a PM skill to a sub-agent for fresh independent judgment, complex artifacts, long analysis, reviews, gates, or bounded read-heavy work.
- Do not run multiple PM sub-agents in parallel when they may write to the same tracker item, project, PR, or parent issue. Use serial delegation so later PM skills can read earlier PM comments.
- Every delegated PM prompt must include the target artifact, source links or issue IDs, allowed tracker writes, and stop conditions.
- Delegated PM skills must return sources read, the produced artifact, tracker writes applied or drafts, blockers, and open questions.
- `$pm-spec` remains the canonical issue-description writer. Do not delegate `$pm-spec` concurrently with other PM writers for the same issue.

## PM Layer Boundaries

- `PM: Product Strategy` (`$pm-strategy`) owns the roadmap loop: product thesis, product principles, portfolio balance, strategic approach, priority order, sequencing, and strategic memory.
- `PM: Project Orchestrator` (`$pm-project-orchestrator`) owns the project decomposition loop: project brief, milestones, issue tree, dependencies, risk map, v1/deferred/rejected cutline, and PM assignment plan.
- `PM: Product Readiness` (`$pm-readiness-review`) owns the single-issue clarity gate: ready, blocked, split, reject, or defer before Dev.
- Do not use project orchestration to approve strategy, and do not use readiness review to settle roadmap priority. Route upward when the decision is at a higher layer.

## Operating Rules

- Gather avoidable context first: read referenced Linear issues, comments, labels, attachments, PRs, docs, branch names, or product surfaces when tools and local context are available.
- When the user gives a bare Linear issue ID, says to start/build/ship an issue, or asks for issue kickoff, start from the issue immediately. Normalize the issue ID exactly, use the current repo unless another path is given, and do not set up git or implement code during PM.
- Start or reuse one active goal for full kickoff-to-dev handoff when goal tools are available and the user is asking to move an issue toward delivery. Do not create a delivery goal for a narrow PM-only artifact request.
- Separate facts, assumptions, decisions needed, and non-goals.
- Preserve user intent and exact wording when it defines the product promise.
- Stay at the product, behavior, scope, acceptance-criteria, and release-learning layer. Do not design implementation unless a product constraint requires it.
- Ask the smallest useful batch of questions only when the answer changes scope, readiness, ticket split, or product risk.
- For existing Linear issues, do not re-scope a `scoped` issue or an issue with a structured PM record unless the user explicitly asks to refresh, redo, update, or requirements changed.
- For ambiguous issues, follow the full default dev-ready workflow unless the intake result exits early to bug triage, a non-PM owner, or an already-ready engineering handoff.
- In fast kickoff mode (`--fast`, `--faster`, "faster", or "ship faster"), classify before PM work, skip `$pm-ui-design`, use `$pm-ux-state` only when journey, task-flow, state, or recovery decisions materially affect scope, and hand off to `$dev` in fast mode.
- In standard kickoff mode, route UX state and UI design before Dev when they affect the work. Use `$pm-ux-state` for journeys, navigation, permissions, onboarding, recovery, cross-screen behavior, states, or product copy direction. Use `$pm-ui-design` for new/changed visible screens, UI elements, layout, hierarchy, controls, UI copy placement, or platform UI decisions.
- Route from `$pm-ui-design` to `$design` only when the user requests a visual artifact, design alternatives, a prototype, design-system work, or a design quality gate. A clear textual UI proposal is sufficient for ordinary Dev handoff.
- When a Design artifact is required for readiness, complete and approve it before `$pm-readiness-review` so the readiness gate can evaluate the actual artifact and unresolved design decisions.
- For product vision, portfolio, roadmap, quarterly/monthly priorities, sequencing, strategic approach, or product-principle tradeoffs, route to `$pm-strategy` before project or issue work.
- For project go/no-go, commitment, opportunity-cost, or kill/continue decisions, route to `$proj-bet`.
- For projects, epics, milestones, roadmap slices, or groups of related issues, route to `$pm-project-orchestrator` before processing individual child issues.
- If a Linear issue is labeled `Bug`, treat that as a hard classifier signal and route to `$pm-bug-triage` before diagnosis/dev workflows unless a product decision is explicitly needed.
- When creating or clarifying Linear issues, assign them to the current/requesting user when identity is known.
- When writing a product record into an existing issue, add the `scoped` label when tools allow.
- Keep child tickets as end-to-end product slices; do not split one outcome into design, implementation, and QA phase tickets.
- Surface material edge cases with recommended resolutions, not a generic checklist.

## Issue Kickoff

Use kickoff mode when the user supplies a Linear issue ID and asks to start, ship, build, prepare, or move it toward engineering.

1. Confirm the target issue and repo context.
   - Read the Linear issue title, description, labels, status, project, comments, attachments, linked PRs, and linked docs.
   - Do not create branches, worktrees, commits, PRs, or technical implementation plans in PM.
2. Classify the issue.
   - `Feature/UX`: new capability, user-visible behavior, workflow, requirements, or acceptance criteria.
   - `Bug`: crash, hang, regression, wrong behavior, performance defect, data loss, broken setting, or failing expected behavior.
   - `Project/multi-issue`: parent issue, milestone, project, or several dev-ready child issues.
   - `Unclear`: missing facts that change the route.
3. Route by classification.
   - Feature/UX: run the default PM chain until `$pm-readiness-review` says ready, inserting `$pm-ux-state`, `$pm-ui-design`, `$pm-data-analytics`, or `$pm-strategy` only when they materially affect acceptance criteria.
   - Bug: use `$pm-bug-triage`; if confirmed as an app bug, route to `$dev-debugger` with the triage brief before Dev handoff. Skip the full PM chain unless expected behavior is a product decision.
   - Project/multi-issue: route to `$pm-project-orchestrator`; when child issues are ready, hand execution to `$dev-project-orchestrator`.
   - Unclear: ask only the blocking questions needed to choose a route.
4. Decide design routing before Dev handoff.
   - Record `UX needed`, `UI needed`, both, or neither.
   - In fast kickoff mode, record `UI skipped: fast mode` and do not call `$pm-ui-design`.
   - Record whether a Design artifact is needed after the PM UI proposal. Do not make artifact creation mandatory for ordinary feature work.
   - If design is skipped, include the skip rationale in the handoff.
5. Sync active tracker status before Dev handoff.
   - Use `$project-manager` to verify related Linear issues and move only confirmed in-scope active work to `In Progress`.
   - Do not move blocked, future, speculative, or dependency-heavy issues just because they are related.
   - If Linear tools are unavailable, produce the exact tracker-ready status update draft.
6. Produce a Dev handoff packet.
   - Use `$dev` for exactly one dev-ready issue.
   - Use `$dev-project-orchestrator` for projects, parent issues, milestones, multiple issues, or dependency sequences.
   - Include Linear issue ID, related issue IDs, repo path, mode, PM artifacts, UX/UI outputs or skip rationale, approved Design artifacts when present, non-goals, acceptance criteria, technical product constraints, validation expectations, tracker status result, and open risks.

## Tracker Write Authority

- `$pm-intake`: post an intake comment and update tracker metadata when tools allow, including assignee, labels, priority, status, and type. Do not edit the issue description.
- `$pm-project-orchestrator`: own the project description, milestones, project-level dependency notes, issue membership, and project-level issue setup. Do not rewrite existing child issue descriptions except when creating new issues.
- `$pm-bug-triage`: post a bug-triage comment and update bug metadata when tools allow, including labels, priority/severity, owner, assignee, status, affected platform, and bug type. Do not edit the issue description.
- `$pm-problem-framing`: post a problem-framing comment only. Do not edit the issue description or tracker metadata.
- `$pm-scope`: post a scope comment only. Do not edit the issue description or tracker metadata.
- `$pm-spec`: own the canonical issue description. Before writing, read the original issue description and prior PM comments, then synthesize them into the final dev-ready product record.
- `$pm-ux-state`: post a UX flow and state comment only. Do not edit the issue description or tracker metadata.
- `$pm-ui-design`: post a UI proposal comment only. Do not edit the issue description or tracker metadata.
- `$pm-technical-boundary`: post a technical-constraints comment only unless creating a separate discovery issue. Do not edit the issue description.
- `$pm-readiness-review`: post a readiness-review comment and update readiness/status fields only when tracker semantics are clear. Do not edit the issue description.
- No PM skill except `$pm-spec` should edit an existing issue description. If tools are unavailable, produce the exact comment, metadata update, or description update draft instead of pretending it was applied.

## Routing

- Raw idea, bug, request, or Linear issue classification: use `$pm-intake`.
- Project, epic, milestone, roadmap slice, or multi-issue product initiative: use `$pm-project-orchestrator`.
- Newly created or unclear bug report after intake, including Bug-labeled Linear issues: use `$pm-bug-triage`.
- Vague request or unclear user problem: use `$pm-problem-framing`.
- Product thesis, roadmap shape, portfolio balance, strategic approach, priority order, sequencing, or product-principle tradeoffs: use `$pm-strategy`.
- Project go/no-go, commitment, opportunity-cost, or kill/continue decision: use `$proj-bet`.
- MVP boundary, non-goals, deferred work, split recommendation: use `$pm-scope`.
- PRD, conversation-to-PRD synthesis, user story, requirements, acceptance criteria, decision record: use `$pm-spec`.
- User workflows, involved screens, navigation behavior, permissions, recovery, empty/loading/error/permission/offline states, copy direction, user-facing edge cases: use `$pm-ux-state`.
- Visible screen layout, hierarchy, sections, controls, UI copy placement, design states, or platform UI decisions: use `$pm-ui-design`.
- Metrics, events, failure signals, learning questions: use `$pm-data-analytics`.
- Platform, API behavior, compatibility, migration, performance, privacy constraints: use `$pm-technical-boundary`.
- Linear issue tree, child tickets, dependencies, milestones, follow-ups, or skill-building backlog slices: use `$pm-backlog`.
- Pre-dev gate for ready/blocked/split/reject: use `$pm-readiness-review`.
- Implemented PR review against product intent: use `$pm-pr-product-review`.
- Post-release learning, metrics to watch, feedback, follow-up issues: use `$pm-release-learning`.

## Common Paths

- Ambiguous issue to dev-ready issue: `$pm-intake` -> `$pm-problem-framing` -> `$pm-scope` -> `$pm-spec` -> `$pm-technical-boundary` -> `$pm-readiness-review`.
- Bug report to diagnosis-ready issue: `$pm-intake` -> `$pm-bug-triage`; if confirmed as an app bug, route to `$dev-debugger` with the bug triage brief.
- Feature or UX issue with known user-facing states: run the default path and insert `$pm-ux-state` before `$pm-spec` only when states, copy, permissions, errors, or edge cases materially change acceptance criteria.
- Visual artifact path: `$pm-ux-state` / `$pm-ui-design` -> `$design` -> `$pm-readiness-review` -> return the approved artifact and decisions in the PM handoff -> `$dev`.
- Conversation already contains enough PRD context: route directly to `$pm-spec` to synthesize the discussion into the canonical product record, asking only for decisions that would change scope, product promise, or validation seams.
- Project or large initiative: `$pm-project-orchestrator`, then route each child issue to the next needed PM skill.
- Roadmap or portfolio strategy: `$pm-strategy`, then route shaped project proposals to `$pm-project-orchestrator`. Use `$proj-bet` first when commitment is unsettled.
- Coding-ready check: `$pm-readiness-review`, then hand off to `$dev` for one issue or `$dev-project-orchestrator` for a project/multi-issue execution plan. `$dev` defaults to fast mode; use `$dev --standard` only when hands-on QA is required.
- Product review after implementation: `$pm-pr-product-review`.
- Issue kickoff to dev-ready handoff: classify the Linear issue, run the relevant PM or bug path, route design only when needed, sync confirmed active issues to `In Progress` with `$project-manager`, then hand one issue to `$dev` or several issues to `$dev-project-orchestrator`.
- Fast issue kickoff: classify first; feature/UX work uses PM plus optional UX, skips UI by design, and hands off with `Mode: fast`; bug work uses `$pm-bug-triage` -> `$dev-debugger` before Dev.

## Output

Lead with the selected route and why it is the right next PM step. Then produce or delegate the requested artifact. If the work spans multiple PM skills, keep the chain explicit and stop when the next unresolved decision needs user input.

For kickoff handoffs, include:

```markdown
## PM Handoff

Issue:
Repo:
Mode: <fast | standard>
Classification: <feature/UX | bug | project/multi-issue | unclear>
PM Route:
Design Route: <UX/UI needed or skipped, with rationale>
Design Artifact: <none required | requested route | approved artifact links>
Tracker Sync: <issues moved to In Progress, draft update, or blocker>
Dev Route: <$dev | $dev-project-orchestrator | blocked>

### Ready Package
- Problem / goal:
- In scope:
- Non-goals:
- Acceptance criteria:
- Technical product constraints:
- Validation expectations:
- Open risks / questions:
```
