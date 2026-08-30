# Mapper Output Schema

Return one JSON object per issue or slice. Do not wrap the JSON in Markdown.

## Required Shape

```json
{
  "schema_version": "dev-project-orchestrator.deep-plan.mapper.v1",
  "slice_id": "ISSUE-123",
  "title": "Short title",
  "source": {
    "type": "issue",
    "id": "ISSUE-123",
    "url": "https://example.test/ISSUE-123"
  },
  "implementation_hypothesis": "One or two sentences describing the likely implementation.",
  "scope": {
    "included": ["Behavior or files likely in scope"],
    "excluded": ["Explicit non-goals"],
    "unknowns": ["Unresolved details that may change implementation"]
  },
  "touchpoints": [
    {
      "path": "src/example.ts",
      "symbols": ["ExampleService.update"],
      "operations": ["modify"],
      "reason": "Likely place for the behavior change.",
      "risk": "medium"
    }
  ],
  "contracts": [
    {
      "name": "PATCH /api/example/:id",
      "kind": "api",
      "provider": "ISSUE-123",
      "consumers": ["ISSUE-124"],
      "status": "changed",
      "reason": "Dependent slice consumes the updated response shape."
    }
  ],
  "migrations": [
    {
      "path": "db/migrations/20260609_example.sql",
      "operation": "create",
      "entities": ["example_table"],
      "reason": "Adds storage needed by this slice."
    }
  ],
  "tests": [
    {
      "path": "src/example.test.ts",
      "kind": "unit",
      "operation": "modify",
      "covers": ["src/example.ts"],
      "depends_on": ["ISSUE-123"]
    }
  ],
  "runtime_dependencies": [
    {
      "slice_id": "ISSUE-122",
      "kind": "api",
      "description": "Needs the new API contract before this can be completed."
    }
  ],
  "product_dependencies": [
    {
      "slice_id": "ISSUE-125",
      "kind": "ux",
      "description": "Both slices must use the same empty-state behavior."
    }
  ],
  "shared_resources": [
    {
      "name": "package-lock.json",
      "kind": "lockfile",
      "reason": "Dependency changes may create merge conflicts."
    }
  ],
  "execution": {
    "can_start_without": ["ISSUE-122"],
    "must_wait_for": ["ISSUE-120"],
    "estimated_wave": 2,
    "parallel_safety": "conditional",
    "parallel_safety_reason": "Safe after the API response shape is finalized.",
    "validation": ["npm test -- src/example.test.ts"]
  },
  "evidence": [
    {
      "source": "src/example.ts",
      "detail": "Existing service owns the behavior."
    }
  ],
  "confidence": "medium"
}
```

## Field Rules

- `schema_version` must be `dev-project-orchestrator.deep-plan.mapper.v1`.
- `slice_id`, `title`, and `implementation_hypothesis` must be non-empty strings.
- `source.type` should be one of `issue`, `pr`, `branch`, `feature_slice`, `parent_issue`, or `unknown`.
- `touchpoints[].operations` may include `read`, `create`, `modify`, `delete`, `rename`, or `generate`.
- `touchpoints[].risk` and `confidence` may be `low`, `medium`, or `high`.
- `contracts[].kind` may be `api`, `schema`, `migration`, `event`, `ui`, `config`, `data`, or `other`.
- `contracts[].status` may be `existing`, `new`, `changed`, or `unknown`.
- `migrations[].operation` may be `create`, `modify`, `delete`, or `unknown`.
- `tests[].kind` may be `unit`, `integration`, `e2e`, `manual`, `contract`, or `other`.
- `runtime_dependencies[].kind` may be `api`, `schema`, `migration`, `test`, `runtime`, `build`, `config`, or `other`.
- `product_dependencies[].kind` may be `scope`, `ux`, `copy`, `rollout`, `analytics`, `permissions`, or `other`.
- `execution.estimated_wave` must be `0`, `1`, `2`, or `3`.
- `execution.parallel_safety` must be `safe`, `conditional`, or `unsafe`.
- Use empty arrays when no values are found. Do not omit required arrays.

## Mapping Guidance

Prefer concrete repo evidence over broad guesses. Include likely files even when the change is not certain, but lower `confidence` and explain the uncertainty. Treat lockfiles, generated files, migrations, API schemas, shared test fixtures, build settings, package manifests, and project files as high-conflict touchpoints.
