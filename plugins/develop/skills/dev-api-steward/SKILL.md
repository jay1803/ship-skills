---
name: dev-api-steward
description: "Maintain owned backend/API contracts and client-facing documentation when implementation may change API behavior or compatibility."
metadata:
  owner: jay1803
  family: develop
  maturity: stable
  distribution: develop
---

# Dev: API Steward

Keep API contracts and API documentation aligned with implementation. Use this for our own backend/API surface; use `$dev-api-research` for third-party API or SDK research.

## When To Run

Run this skill whenever a Dev task may change backend/API behavior:

- New, removed, renamed, or changed endpoint.
- Request body, response body, query parameter, header, auth, permission, webhook, pagination, or error behavior changes.
- Database/schema changes that alter externally visible API data.
- OpenAPI/Swagger, generated client, SDK example, curl example, integration guide, or API docs may need updates.
- Client behavior may change for iOS, macOS, web, backend consumers, partners, or scripts.

## Timing

Use two gates for API work:

1. **Pre-implementation contract review** before implementation, using the current approved approach or brief. When technical planning is selected, return contract constraints to the same `$dev-planner` plan; do not require a separate architecture artifact or replay settled planning.
   - Decide the intended contract, compatibility risk, docs targets, changelog need, client impact, and migration/versioning expectations.
   - Do not commit docs yet unless the repo is explicitly contract-first and implementation is generated from docs/OpenAPI.
2. **Post-implementation contract closeout** after `$dev-implementer` and before `$dev-test` / `$dev-verifier`.
   - Compare the actual diff to the intended contract.
   - Update OpenAPI/Swagger/docs/examples/changelog/versioning notes as needed.
   - Produce the contract evidence that `$dev-test`, `$dev-verifier`, `$dev-pr-writer`, and `$pm-pr-product-review` can use.

This timing avoids stale speculative docs while settling the contract before implementation.

## Responsibilities

- **API contract review**: check whether request/response behavior, endpoint semantics, auth, permissions, pagination, webhooks, or generated contracts changed.
- **Docs update**: update OpenAPI/Swagger, API docs, endpoint docs, integration guides, generated docs, or examples when the API surface changed.
- **Changelog entry**: record what changed, why, compatibility, migration notes, and whether it is breaking.
- **Client impact analysis**: identify affected iOS, macOS, web, backend, script, partner, or generated-client consumers.
- **Versioning judgment**: decide whether the change is backwards-compatible, additive, breaking, deprecated, or migration-required.
- **Error model consistency**: ensure status codes, error shapes, messages, retryability, and validation errors follow existing conventions.
- **Example maintenance**: update curl examples, sample payloads, SDK examples, fixtures, docs snippets, or integration notes.

## Workflow

1. Read the current scope/approach, relevant technical constraints, repository evidence, and implementation diff for the selected gate. Reuse existing briefs and selected-stage outputs; stop for unresolved contract facts rather than demanding documents from unselected stages.
2. Locate the API source of truth:
   - OpenAPI/Swagger spec, route definitions, controller/service handlers, schema files, generated clients, docs, examples, changelog, migrations, tests, and fixtures.
3. Determine whether the change affects external or internal API behavior.
   - If no API contract changed, record `No API Steward changes required` with evidence.
4. Run the relevant gate:
   - Pre-implementation: return the intended contract and stewardship tasks to the caller/controller for the next selected phase, including `$dev-planner` when planning is selected.
   - Post-implementation: update docs/changelog/examples and produce the final contract review.
5. Check compatibility.
   - Additive nullable fields, optional request fields, or new endpoints are usually backwards-compatible.
   - Required request fields, removed/renamed fields, changed meaning, stricter validation, auth/scope changes, status-code changes, pagination changes, or error-shape changes may be breaking.
6. Check clients.
   - Identify affected client repos/modules when visible from the current repo, docs, generated clients, PRs, or PM handoff.
   - If client updates are required, name the client work. Route multi-issue or
     cross-repository execution to `$dev-project-orchestrator`; use
     `$dev-integration-manager` for the explicit PR/branch set and integration
     strategy produced by that controller.
7. Update the API artifacts when required.
   - Keep docs and examples consistent with existing style and source-of-truth direction.
   - If generated artifacts are present, use the repo's generator command when available instead of hand-editing generated files.
8. Route implementation problems back to Dev.
   - If implementation does not match the intended contract, route to `$dev-implementer`, using its PR-repair reference after review/PR.
   - Do not silently change product behavior to match docs.

## Output

```markdown
## API Steward Review

Phase: <pre-implementation | post-implementation>
API surface:
Contract changed: <yes | no>
Compatibility: <backwards-compatible | breaking | deprecated | migration-required | unknown>

### Contract Review
- Request changes:
- Response changes:
- Auth / permission changes:
- Error model changes:
- Pagination / webhook / async behavior changes:

### Docs / Changelog
- OpenAPI / Swagger:
- API docs:
- Examples / SDK snippets:
- Changelog:
- Migration / versioning notes:

### Client Impact
- iOS:
- macOS:
- Web:
- Backend / scripts / partners:

### Files Updated
- <path or "None">

### Required Follow-Up
- <client work, migration, generated client update, product decision, or "None">

Decision: <contract accepted | update docs before PR | fix implementation | blocked>
```
