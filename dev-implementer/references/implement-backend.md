# Implement Backend

Use for backend/API/service code that is not primarily Supabase: server routes, workers, jobs, queues, persistence, API clients, auth, permissions, migrations, service contracts, generated clients, and backend integration tests.

## Workflow

1. Discover runtime, framework, package manager, service entrypoints, API routing, persistence layer, migration tool, queue/job system, auth/permission model, config/secrets pattern, and test commands before editing.
2. Inspect target files before editing. Reuse existing request/response models, validation, error types, logging/redaction, dependency injection, transaction boundaries, and retry/idempotency patterns.
3. Make the smallest coherent backend change needed by the plan. Keep API contracts, migrations, generated types, and clients aligned.
4. Add or update focused unit, integration, contract, fixture, or migration tests when the repo has a practical surface.
5. Preserve security boundaries: do not expose secrets, weaken auth/permissions, log sensitive data, skip tenant scoping, or use production data.
6. Validate with the repo's backend commands when practical: build, lint/typecheck, unit/integration tests, migration/schema checks, API smoke checks, or representative CLI commands.
7. Stop if the change requires external credentials, production data access, product scope changes, security exceptions, provider contract decisions, or architecture changes not covered by the plan.

## Notes To Report

- API contract, auth/permission, migration, data model, queue/job, config, retry/idempotency, or observability constraints.
- Tests, fixtures, migrations, generated types, or docs added or skipped, with rationale.
- Security/data concerns and exact validation evidence.
