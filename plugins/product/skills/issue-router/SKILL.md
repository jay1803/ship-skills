---
name: issue-router
description: Select one read-only workflow route for a bound Linear issue or project before PM, Dev, investigation, verification, or release.
metadata:
  owner: jay1803
  family: product
  maturity: stable
  distribution: product
---

# Issue Router

Obtain one canonical route through the [Jev-first decision cascade](references/decision-cascade.md)
when Jev is configured.
Consume accepted workflow, delivery-shape, readiness and mode choices without
reclassification; the main model only resolves explicit pending disagreements.

1. Reuse an existing current `issue_route` when its request, evidence, authority
   and target still match. Otherwise gather the minimal bound live facts.
2. Follow the [input contract](references/jev-input.md) and run
   `python3 <this-skill>/scripts/route_issue.py --input <facts.json>`.
3. Accept the returned owner and completion contract without loading the
   [model-consumed policy](references/issue-policy.md) or repeating its decisions.
4. On `blocked`, report the named boundary and stop dependent work. On `routed`,
   hand the unchanged receipt and evidence to the selected workflow. For `pm/*`,
   consume its `pm_action` as the next bounded action; it is not a readiness verdict.
   On `needs-main-model`, follow the [bound-resolution contract](references/decision-cascade.md#main-model-resolution)
   and resume the helper before handing off any workflow.

Jev is optional. Configure `TYPESAFE_API_KEY` (or `JEV_API_KEY`) in the
environment or in `JEV_ENV_FILE` (default `~/.config/jev/.env.local`). Without a
credential the helper returns `blocked` with reason `credential_unavailable`;
then read the [model-consumed policy](references/issue-policy.md), select the
route yourself, and report the result as locally routed rather than Jev-backed.

With a credential, routing performs a primary paid Jev call and, only for low-confidence questions,
an independent Luna call. Explicit adjudication resumes without another API call.
It performs no business writes, agent dispatch,
branch creation or lifecycle transition. It never grants new authority.
`$agent-routing` separately resolves execution resources inside the selected
workflow. Refresh materially changed facts before mutation; preserve existing
owners and anchors instead of creating duplicate work.
