# Implement Supabase

Use for Supabase database schema, migrations, RLS, Auth, Edge Functions, Storage, Realtime, cron, queues, generated types, backend API behavior, and Supabase client/server integration.

## Workflow

1. Load `$supabase:supabase` before implementing Supabase work. Follow its current-docs, changelog, CLI, MCP, migration, verification, and security rules.
2. For database design or performance-sensitive changes, also use `$supabase:supabase-postgres-best-practices` when available.
3. Discover project shape before editing: `supabase/`, migrations, functions, generated types, local config, env expectations, tests, seed data, and backend API boundaries.
4. Inspect target files before editing. Keep migrations, generated types, Edge Functions, server code, and tests aligned.
5. Make the smallest coherent backend change needed by the plan. Do not weaken RLS, expose service-role secrets, invent migration filenames, or bypass existing backend contracts.
6. Add or update focused tests, fixtures, generated types, and docs when the repo requires them.
7. Validate with the repo's preferred Supabase/backend commands and record exact evidence.
8. Stop if the change requires external credentials, production data access, product scope changes, security exceptions, or API contract decisions not covered by the plan.

## Notes To Report

- Schema, RLS, Auth, function, storage, generated-types, API-contract, privacy, secrets, or migration concern.
- Tests, fixtures, migrations, generated types, or docs added or skipped, with rationale.
- Validation command/tool and exact result or blocker.
