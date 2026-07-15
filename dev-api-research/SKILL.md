---
name: dev-api-research
description: >-
  Research third-party APIs, SDKs, external docs, OpenAPI specs, auth, permissions, rate limits, pricing, webhooks, pagination, errors, sandbox behavior, data mapping, security, and integration examples before Dev architecture. Use before $dev-architect when a Dev task depends on an external service or API behavior. Produces an API research brief and feasible, risky, or blocked decision.
---

# Dev: API Research

Research external APIs deeply enough for `$dev-architect` to design the integration without guessing.

Run before `$dev-architect` when the implementation depends on third-party APIs, SDKs, OpenAPI specs, webhooks, auth models, provider limits, pricing, data contracts, or sandbox behavior. If the broader technical direction is also unclear, pair this with `$dev-spike`.

## Source Rules

- Prefer current primary sources: official docs, OpenAPI/Swagger schema, official SDK repository, official examples, changelog, pricing page, limits page, status page, and security/webhook docs.
- Use secondary sources only to compare approaches or fill clearly labeled gaps.
- Browse or otherwise verify current docs when API behavior could have changed; do not rely on memory for limits, pricing, auth, scopes, or endpoint behavior.
- Capture source URLs or local paths. Do not paste long excerpts.
- If docs conflict, prefer the newest official version and call out the conflict.

## Project Fit

When a target repo is available, inspect its integration patterns before recommending an approach:

- Existing API clients, generated clients, HTTP helpers, auth storage, secret management, environment config, retry/backoff, pagination helpers, logging/redaction, and observability.
- Existing data models, provider abstractions, migrations, background jobs, webhook handlers, tests, fixtures, mocks, and CI commands.
- Privacy, data retention, rate-limit, timeout, cost, and support constraints implied by the project.

Fit the recommendation to those patterns. Mark file names as speculative unless the repo evidence supports them.

## Workflow

1. Resolve the API, use case, required user flow, target repo, and decision needed.
2. Read official docs for auth, endpoints, permissions/scopes, limits, pricing/quota, SDKs, webhooks, pagination, errors, sandbox/test mode, and examples.
3. Inspect the repo's existing integration patterns when implementation guidance depends on local architecture.
4. Map external objects, identifiers, lifecycle states, and errors to our system.
5. Compare implementation options such as direct client integration, generated client, backend proxy, webhook-first sync, polling, batch import, or staged rollout.
6. Decide whether the integration is feasible, risky, or blocked, and name the next Dev step.

## Output

Start with sources and project fit, then produce the brief in this shape:

```markdown
## API Research Brief

Sources read:
- <official docs URL or local path> - <what it covered>

Project fit:
- <repo patterns inspected, or "not inspected / not applicable">

API:
Use case:
Required endpoints:
Auth model:
Permissions / scopes:
Rate limits:
Pricing / quota:
SDK availability:
Webhook support:
Pagination model:
Error model:
Sandbox / test mode:
Data mapping to our system:
Security / privacy concerns:
Known limitations:
Implementation options:
Recommended approach:
Open questions:
Decision: feasible / risky / blocked
```

Add these fields only when they materially affect the integration:

- Versioning / changelog:
- Retry / idempotency:
- Observability / support:
- Compliance / terms:
- Rollout / migration notes:

Keep the brief implementation-oriented. The recommendation should tell `$dev-architect` which integration shape to design and what constraints cannot be violated.
