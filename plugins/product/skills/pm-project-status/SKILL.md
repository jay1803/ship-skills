---
name: pm-project-status
description: Read current Linear project and roadmap status, milestone health and shipment evidence. Use for a project status report; route scope changes to Product and issue/PR delivery mutations to Develop.
metadata:
  owner: jay1803
  family: product
  maturity: stable
  distribution: product
---

# Product Project Status

Maintain a truthful read-only picture of a product project's roadmap, milestones,
issues, dependencies and shipments. This is the status capability formerly in
Project's `proj-manage`; it belongs to Product. Project documents from proposal
through closeout remain owned by the separate Project plugin.

## Gather the current picture

Bind the named Linear project/initiative or exact issue scope. Use available
configured Linear tools and authentication. Read the relevant full scope before
claiming project-wide status; a single issue does not establish the whole map.
Report inaccessible evidence instead of treating it as current.

Read current milestones, priorities, owners, blockers and dependencies. Where
available, cross-check claimed shipment against PR, release, deployment and
acceptance evidence. Distinguish implemented, merged, deployed, accepted and
measured outcomes; tracker Done alone need not mean shipped to users.

Return a dated snapshot with scope/sources, milestone progress, recently shipped
work, active work, blockers and missing evidence. Recommendations for next work
should respect confirmed priorities and dependencies; label them as advice,
not a newly committed plan. Preserve unresolved conflicts between the roadmap
and actual delivery evidence.

## Ownership and writes

Status/explanation requests end at the report with no mutations. A request that
also authorizes changes goes to the existing owner with the verified evidence:

- Product scope, new/decomposed issues, dependencies and PM readiness:
  [pm](../pm/SKILL.md) or
  [pm-project-orchestrator](../pm-project-orchestrator/SKILL.md), using
  [issue-router](../issue-router/SKILL.md) for a bound delivery request.
- Engineering start, PR traceability, CI, merge and completion status: the
  current Develop lifecycle owner (`dev`, `dev-pr-writer`,
  `dev-merge-handoff`, or `dev-project-orchestrator` as applicable).
- Stakeholder narrative and Entry Page changes: Project's `proj-update` when
  available and requested.

Do not duplicate delivery transition rules here or move issues because a
status report recommends it. Preserve issue acceptance requirements and actual
write authority when handing evidence to another owner. If the target plugin
is unavailable, name the next owner and return the report/handoff; do not claim
execution or bypass its gates. No cross-plugin installation is necessary for
a read-only status report with working source access.
