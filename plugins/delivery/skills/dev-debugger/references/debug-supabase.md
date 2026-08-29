# Debug Supabase

Use for Supabase database schema, migrations, RLS, Auth, Edge Functions, Storage, Realtime, generated types, backend API behavior, and Supabase client/server integration defects.

## Workflow

1. Load `$supabase:supabase` before diagnosing Supabase work. Follow its current-docs, changelog, CLI, MCP, migration, verification, and security rules.
2. For schema, query, index, RLS, or performance issues, also use `$supabase:supabase-postgres-best-practices` when available.
3. Discover project shape: `supabase/`, migrations, functions, generated types, local config, env expectations, seed data, tests, RLS policies, Auth providers, Storage buckets, Realtime channels, and backend API boundaries.
4. Reproduce with the same role, JWT claims, tenant/user, local/remote project, seed data, migration state, function env, and client query.
5. Search from evidence anchors: SQL error, PostgREST status, policy name, table/column, migration id, function name, log line, generated type, storage bucket, realtime channel, auth provider, and test name.
6. Keep security boundaries intact. Do not weaken RLS, expose service-role secrets, use production data, or bypass policy behavior as a fix direction.

## Symptom Map

- RLS denial or unexpected access: policies, JWT claims, role, tenant predicate, `auth.uid()`.
- Migration failure: order, idempotency, default/nullability, generated types, destructive change.
- Wrong query result: join/filter, RPC behavior, view definition, timezone, nullable column.
- Edge Function failure: env vars, auth header, CORS, dependency, logs, request body parsing.
- Auth issue: provider config, redirect URL, session refresh, role/claim mapping.
- Storage issue: bucket policy, signed URL expiry, upload size/type, path naming.
- Realtime issue: publication, channel filters, replica identity, auth policy.
- Performance issue: query plan, index, RLS predicate cost, row count, N+1 client queries.

## Evidence To Report

- Supabase project/local state, role/JWT claims, table/function/bucket/channel, migration state, and reproduction reliability.
- SQL/log/function/test evidence and candidate files.
- Security/data concerns and whether RLS/privacy boundaries are preserved.
- Exact SQL, CLI command, function invocation, or test that should verify the hypothesis.
