# Deep Parallelization Planning

Read only for --deep-plan or an explicit request for verified conflict mapping. Resolve agent routing before mapper/verifier dispatch. Run script paths from this Skill directory.

## Deep Parallelization Plan

Use this workflow only for `--deep-plan` or an explicit user request for verified conflict mapping. This mode is intentionally heavier than the default project plan.

1. Intake.
   Resolve each issue, PR, branch, parent issue, or feature slice into a concise implementation hypothesis. For a parent issue, inspect child issues and preserve the user's slicing unless the existing split is unusable. If tracker access is unavailable, state what could not be verified and continue from provided text only when the local implementation surface can still be inspected.
2. Map slices.
   Spawn one `slice_mapper` subagent per issue or slice when subagent tools are available. Route it as `explorer/standard` with `repo-read`, read-only permissions, and the resolved adapter's current binding. Give each mapper one slice, the repo path, relevant base/target branch details, and `references/deep-plan-output-schema.md`. Require read-only repo inspection and JSON-only output.
3. Normalize mapper outputs.
   Save each mapper output as a separate JSON file in a disposable planning directory. Run:

   ```bash
   node scripts/validate_deep_plan_json.ts /path/to/mapper-outputs/*.json
   ```

   If validation fails, ask the responsible mapper for corrected JSON using the reported errors. Do not manually patch mapper findings unless the error is purely formatting and the source answer is unambiguous.
4. Build the conflict graph.
   Run:

   ```bash
   node scripts/build_deep_conflict_graph.ts /path/to/mapper-outputs/*.json
   ```

   Use the graph to detect `same_file_conflict`, `same_symbol_conflict`, `API_contract_dependency`, `schema_or_migration_dependency`, `test_dependency`, and `product_scope_dependency`.
5. Synthesize execution waves.
   - Wave 0: contracts, schemas, migrations, shared fixtures, generated outputs, prerequisites, or decisions that must stabilize first.
   - Wave 1: safe parallel work with disjoint files, symbols, contracts, and validation paths.
   - Wave 2: dependent work that waits for Wave 0 or Wave 1 outputs.
   - Wave 3: integration, regression verification, conflict resolution, end-to-end QA, and final merge sequencing.
6. Verify the draft.
   Spawn one `plan_verifier` subagent as `reviewer/deep` with read-only permissions and the resolved adapter's current binding when subagent tools are available. Ask it to disprove the draft plan using mapper JSON and the conflict graph, focusing on hidden coupling, unsafe parallelism, missing tests, wrong wave ordering, shared generated files, lockfile conflicts, schema/API drift, and product-scope overlap.
7. Finalize.
   Incorporate verifier findings. If subagent tools were unavailable, state that mapping or verification was performed locally rather than independently. Separate verified facts from assumptions and name missing information that could change execution order.

### Mapper Prompt

```markdown
You are a slice_mapper for a read-only deep parallelization plan.

Slice: <issue id, PR, branch, or feature slice>
Repo: <absolute repo path>
Base/target: <branches if known>

Inspect the repo read-only. Do not edit files, create branches, run migrations, or implement anything.
Return JSON only, matching dev-project-orchestrator/references/deep-plan-output-schema.md.

Focus on likely touched files, symbols, contracts, migrations, tests, runtime dependencies, product dependencies, validation commands, and whether this slice is safe to run in parallel.
```

### Verifier Prompt

```markdown
You are a plan_verifier for a read-only deep parallelization plan.

Inputs:
- Mapper JSON outputs: <paths or pasted JSON>
- Conflict graph: <path or pasted JSON>
- Draft wave plan: <draft>

Try to disprove the plan. Identify hidden coupling, unsafe parallelism, missing tests, missing prerequisites, wrong wave ordering, merge-order risks, and cases where a shared API/schema/product contract must be stabilized first.
Return findings ordered by severity and include concrete evidence.
```

For deep planning mode:

```markdown
## Conflict / Dependency Graph
- <edge or dependency summary with issue IDs and reason>

## Wave Plan
### Wave 0 - Contracts / Schema / Prerequisites
- <issue or task> - <why first>

### Wave 1 - Safe Parallel Work
- <issue> - <owner/scope/validation>

### Wave 2 - Dependent Work
- <issue> - <waits for what>

### Wave 3 - Integration / Regression Verification
- <validation and merge sequencing>

## Assignment Recommendations
- <issue> - <parallel/serial/blocked recommendation, expected files, validation>

## Verification Notes
- <verifier finding or "No hidden blockers found">

## Missing Information
- <assumption or unavailable source that could change execution order>
```
