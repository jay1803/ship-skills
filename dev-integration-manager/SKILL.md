---
name: dev-integration-manager
description: >-
  Cross-PR integration controller for multi-issue engineering work. Use when several PRs or branches must merge safely, when merge order matters, when cross-branch conflicts or shared files exist, when API/schema/client contracts must be checked together, when an integration branch is needed, or when combined system validation is required after multiple PRs.
---

# Dev: Integration Manager

Manage cross-PR integration after issue-level `$dev` work creates multiple branches or PRs. This skill owns merge order, integration branch strategy, conflict routing, contract checks, combined validation, and rollback risk across PRs.

## Boundary

- Use this skill for multiple PRs, stacked branches, project batches, shared API/schema/client changes, cross-branch conflicts, or combined validation after several PRs.
- Use `$dev-release-handoff` for a single PR's final merge gate.
- Use `$dev-fix` for valid review comments, merge conflicts, or cross-branch conflict repairs on a PR branch.
- Use `$dev-ci-repair` for red checks or CI failures.
- Use `$dev-project-orchestrator` when the implementation order or branch strategy has not been planned yet.
- Do not add new product scope or feature behavior while integrating. Route scope gaps back to `$pm-pr-product-review`, `$pm`, or the responsible `$dev` issue worker.
- Do not force-merge, bypass branch protection, rewrite another worker's branch, or discard local changes.

## Inputs

- Project or milestone name.
- Base branch.
- PR list with issue IDs, head branches, owners, and dependency order when known.
- Engineering execution plan from `$dev-project-orchestrator` when available.
- Required validation commands or CI checks.
- API, schema, migration, generated-type, feature-flag, rollout, or rollback constraints.

If any input is missing, discover it from GitHub, Linear, branch names, PR metadata, commits, and repo state when tools allow. Ask only when the missing fact changes merge order or integration safety.

## Integration Modes

- **Direct ordered merge**: PRs are independent or dependency-ordered, each passes its own gate, and combined validation risk is low. Merge one PR at a time through `$dev-release-handoff`, refresh the base branch, then re-check remaining PRs.
- **Integration branch**: PRs interact through shared files, APIs, schemas, migrations, generated outputs, clients, or release behavior. Create a temporary integration branch from the base branch, merge candidate PR heads into it for conflict detection and combined validation, then route required fixes back to the affected PR branches.
- **Blocked**: Required PRs are not ready, contracts are unstable, conflicts need owner decisions, checks are red, product review failed, or external dependencies are unavailable.

## Workflow

1. Resolve the PR set and base branch. Capture PR URLs, issue IDs, head branches, latest commits, status checks, review state, mergeability, changed files, and dependency links.
2. Confirm each PR has completed issue-level `$dev` expectations: validation evidence, code review handling, CI state, and PR Product Review when required.
3. Build the integration dependency order:
   - Foundation/schema/API PRs before client PRs.
   - Generated types or shared contracts before dependents.
   - Data migrations before code that assumes migrated state only when rollback is safe.
   - Risky cross-cutting changes before dependent polish only if they have stable validation.
4. Decide the integration mode: direct ordered merge, integration branch, or blocked.
5. Check cross-PR contracts:
   - API request/response shape and error model.
   - Schema, migration, seed, RLS, permission, or data contract.
   - Generated types, SDK clients, feature flags, and backwards compatibility.
   - Auth, privacy, logging, analytics, and rollout/rollback behavior.
6. Check conflicts and shared ownership:
   - File conflicts.
   - Migration order conflicts.
   - Package lock, project file, generated file, or build setting conflicts.
   - Test fixture or snapshot conflicts.
7. If using an integration branch, create it from the base branch, merge PR heads in planned order for validation, and do not push or use it as the final merge vehicle unless the user explicitly wants that branch strategy.
8. Route repairs:
   - Conflicts or review-comment fixes -> `$dev-fix` on the affected PR.
   - Red checks -> `$dev-ci-repair`.
   - Missing product conformance -> `$pm-pr-product-review` or the responsible `$dev` worker.
   - Unstable external/API behavior -> `$dev-api-research` or `$dev-spike`.
9. Run combined validation after the candidate set is conflict-free. Use the narrowest reliable project-level checks first, then broaden for shared contracts, migrations, or user-facing flows.
10. Merge through `$dev-release-handoff` in the planned order. After each merge, update the base branch, re-check remaining PRs, and adjust the plan if conflicts or checks change.
11. Produce rollback and follow-up notes for the combined release.

## Output

```markdown
## Integration Plan

Decision: <direct ordered merge | integration branch | blocked>
Project:
Base branch:
PRs:
Integration branch:

## Merge Order

1. <PR / issue> - <reason>
2. <PR / issue> - <reason>

## Cross-PR Contract Check

- API contracts:
- Schema / migrations:
- Generated types / SDK clients:
- Auth / permissions:
- Analytics / logging:
- Rollout / rollback:

## Conflict Check

- File conflicts:
- Migration conflicts:
- Generated / lockfile / project-file conflicts:
- Test fixture or snapshot conflicts:

## Combined Validation

- Required checks:
- Commands run or required:
- Result:

## Repair Routing

- `$dev-fix`:
- `$dev-ci-repair`:
- `$pm-pr-product-review` / PM:
- `$dev-spike` / `$dev-api-research`:

## Merge Execution

- Merged:
- Waiting:
- Blocked:

## Risks / Rollback

- Risk:
- Rollback:
- Follow-ups:
```
