# Skill Catalog

A map of every skill in this repository: what each one does and when to reach
for it. Skills are grouped by domain. Within a group, the **orchestrator** (if
any) is the entry point — start there and let it route to the narrower skills.

Invoke a skill with `$name` in Codex or `/name` in Claude Code, or just describe
the task and let the agent match it against the skill's description.

> 中文版见 [`CATALOG.zh-CN.md`](CATALOG.zh-CN.md)。

## Quick index

| Group | Skills |
| --- | --- |
| [PM workflow](#pm-workflow) | `pm` + 15 sub-skills |
| [Dev workflow](#dev-workflow) | `dev` + 20 sub-skills |
| [Design](#design) | `design` + 5 sub-skills |

---

## PM workflow

Product-management pipeline: an orchestrator plus single-purpose stages. **Start
with `pm`** for any PM request — it routes one issue to the right stage, while
`pm-project-orchestrator` inventories project issue sets and controls safe
serial/parallel PM worker waves through readiness.

See [`PM_DEV_WORKFLOW.md`](PM_DEV_WORKFLOW.md) for the full pipeline, stage
order, and routing logic across all `pm-*` sub-skills.

## Dev workflow

Engineering pipeline mirroring PM. **Start with `dev`** for a single dev-ready
issue; use `dev-project-orchestrator` for multi-issue work or
`dev-integration-manager` for cross-PR integration.

See [`PM_DEV_WORKFLOW.md`](PM_DEV_WORKFLOW.md) for the full pipeline, stage
order, and routing logic across all `dev-*` sub-skills.

## Design

Visual execution between approved product intent and production engineering.
**Start with `design`** when the required design artifact or phase is unclear.

- `design` — Route clear product intent through direction, exploration, prototypes, system work, and review.
- `design-direction` — Define a concrete visual language: type, color, density, hierarchy, shape, imagery, and motion.
- `design-explore` — Produce comparable wireframes, visual alternatives, component options, or flow storyboards.
- `design-prototype` — Build and verify a disposable interactive prototype with real state and feedback.
- `design-system` — Extract, create, refine, and document foundations, tokens, components, and consistency gaps.
- `design-review` — Review accessibility, hierarchy, interaction states, system conformance, responsiveness, and polish; report by default and fix only when asked.

Product behavior and screen requirements remain in `pm-ux-state` and
`pm-ui-design`; production implementation remains in `dev` and platform skills.
