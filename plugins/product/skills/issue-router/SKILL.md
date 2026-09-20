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

Obtain one canonical route for the bound request. With Jev configured, the
executing model does not classify workflow, delivery shape, readiness or mode
itself.

1. Reuse an existing current `issue_route` when its request, evidence, authority
   and target still match. Otherwise gather the minimal bound live facts.
2. Follow the [input contract](references/jev-input.md) and run
   `python3 <this-skill>/scripts/route_issue.py --input <facts.json>`.
3. Accept the returned owner and completion contract without loading the
   [model-consumed policy](references/issue-policy.md) or repeating its decisions.
4. On `blocked`, report the named boundary and stop dependent work. On `routed`,
   hand the unchanged receipt and evidence to the selected workflow.

Jev is optional. Configure `TYPESAFE_API_KEY` (or `JEV_API_KEY`) in the
environment or in `JEV_ENV_FILE` (default `~/.config/jev/.env.local`). Without a
credential the command exits `credential_unavailable`; then read the
[model-consumed policy](references/issue-policy.md), select the route yourself,
and report the result as locally routed rather than Jev-backed.

With a credential, routing performs one paid API call and no business writes, agent dispatch,
branch creation or lifecycle transition. It never grants new authority.
`$agent-routing` separately resolves execution resources inside the selected
workflow. Refresh materially changed facts before mutation; preserve existing
owners and anchors instead of creating duplicate work.
