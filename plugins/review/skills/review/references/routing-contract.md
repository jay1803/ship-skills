# Agent Routing Contract

Use this contract when `$review` needs an independent no-context reviewer.
Routing chooses an executor; it does not change Review's read-only role,
immutable target, posting authority, or stale-result rules.

## Request

Classify and record:

```yaml
lifecycle: bounded
role: reviewer
depth: standard | deep
requirements: [repo-read, github-read, github-review-write]
permissions: read-only-repository | github-review-write
write_scope: exact target PR review surface | none
executor_policy:
  executor: any | codex | claude-code
  fallback: allowed | forbidden
independent_from: <execution id and executor, or none>
```

Use `standard` for ordinary bounded review and `deep` for cross-cutting,
security-sensitive, contract-heavy, or high-risk review. The default
thermo-nuclear rubric does not by itself raise runtime depth; route from
actual task complexity and preserve an explicit depth request. An
explicit executor request is `required` unless the caller also authorizes a
fallback. Cross-executor independence fails closed when the resolved executor
matches `independent_from`; a fresh context alone is not cross-executor
independence.

## Runtime Boundary

- Spawn a clean reviewer with no inherited implementation or issue context.
- Pass only the repository path, immutable target envelope, and review task.
- The reviewer must not delegate to another provider, plugin, bot, or reviewer.
- A runtime inability to inspect the target is `blocked`; do not reinterpret a
  local inspection as completed independent review.
- Resolve provider-neutral role/depth here, then bind model and reasoning from
  exactly one executor adapter.

## Receipt

Return both the requested route and resolved binding:

```yaml
requested_route:
  lifecycle: bounded
  role: reviewer
  depth: standard | deep
  requirements: [...]
  permissions: ...
  write_scope: ...
  executor_policy: ...
resolved_route:
  executor: codex | claude-code | unknown
  model: <adapter model or unknown>
  reasoning: <adapter effort or unknown>
  runtime_role: reviewer
  executor_fallback: <none or applied fallback>
  profile_fallback: <none or applied fallback>
  independence: not-required | satisfied | blocked
```
