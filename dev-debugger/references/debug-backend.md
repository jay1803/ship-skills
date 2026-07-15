# Debug Backend

Use for backend/API/service bugs that are not primarily Supabase: routes, workers, jobs, queues, persistence, API clients, auth, permissions, migrations, generated clients, and backend integration tests.

## Workflow

1. Discover runtime, framework, package manager, service entrypoints, API routing, persistence layer, migration tool, queue/job system, auth/permission model, config/secrets pattern, logging, observability, and test commands.
2. Reproduce with the same request, tenant/user, auth scope, data fixture, environment variables, feature flags, queue state, time window, and external dependency behavior when those matter.
3. Search from evidence anchors: error string, status code, request id, endpoint, job name, queue name, migration name, model field, log key, test name, provider object id, and stack trace.
4. Trace request or job flow from entrypoint to failure point. Check validation, auth, tenant scoping, persistence, external calls, retries, idempotency, and serialization.
5. Prefer failing test, representative request, or local script reproduction before proposing a fix.

## Symptom Map

- 4xx/validation bug: schema, input normalization, auth scope, tenant/user permission.
- 5xx/crash: stack trace, error boundary, missing config, dependency failure, null/undefined data.
- Wrong data: query/filter/join, cache invalidation, serialization, timezone, stale fixture.
- Race/flaky behavior: transaction boundary, idempotency key, lock, retry, queue ordering.
- Migration failure: schema drift, generated types, default/nullability, destructive migration.
- Slow endpoint/job: query plan, N+1, missing index, external dependency latency, batch size.
- Webhook bug: signature verification, duplicate delivery, idempotency, event ordering.
- External API bug: route primary unknowns to `$dev-api-research` if docs/provider behavior decide the fix.

## Evidence To Report

- Endpoint/job/test, request id, tenant/user scope, env/config, data fixture, and reproduction reliability.
- Logs, stack traces, SQL/query evidence, failing tests, and candidate files.
- Security/data concerns such as secrets, PII logging, tenant isolation, and production-data access.
- Exact command, request, test, or smoke check that should verify the hypothesis.
