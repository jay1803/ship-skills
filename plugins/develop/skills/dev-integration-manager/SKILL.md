---
name: dev-integration-manager
description: "Coordinate integration of an explicit PR or branch set when merge order, cross-branch contracts, conflicts, or combined validation need a shared checkpoint."
metadata:
  owner: jay1803
  family: develop
  maturity: stable
  distribution: develop
---

# Dev: Integration Manager

Manage cross-PR integration after issue-level `$dev` work creates multiple
branches or PRs. This skill owns only the supplied merge order or integration
branch strategy, conflict routing, contract checks, combined validation, and
rollback risk across that explicit set.

Read the canonical [branch strategy](../dev/references/branch-strategy.md) before resolving bases or merge direction.

## Boundary

- Use this skill for an explicit PR or branch set with an explicit order or
  integration-branch strategy, shared API/schema/client changes, cross-branch
  conflicts, or combined validation after several PRs.
- Use `$dev-merge-handoff` for a single issue PR's final merge gate into the resolved issue PR base.
- Production promotion from the integrated candidate belongs to `$release`. Do
  not use issue PR integration to bypass that boundary; `$release` resolves the
  production branches and merge executor from the repository release policy.
- Use `$dev-implementer` for valid review comments, merge conflicts, or cross-branch conflict repairs on a PR branch.
- Use `$dev-ci-repair` for red checks or CI failures.
- Do not infer a PR set, implementation order, or branch strategy inside this
  integration phase. If the caller supplied a project, issue set, or dependency
  sequence instead, route it to `$dev-project-orchestrator`. Otherwise return
  `input-required` with the exact missing PR/branch inputs.
- Do not add new product scope or feature behavior while integrating. Route scope gaps back to `$pm-pr-product-review`, `$pm`, or the responsible `$dev` issue worker.
- Do not force-merge, bypass branch protection, rewrite another worker's branch, or discard local changes.

## Inputs

- Base branch.
- Explicit PR or branch list with issue IDs, head branches, and owners.
- Explicit ordered-merge or integration-branch strategy.
- Required validation commands or CI checks.
- API, schema, migration, generated-type, feature-flag, rollout, or rollback constraints.

If the base branch, explicit candidate set, or explicit order strategy is
missing, return `input-required` with the missing fields. When the available
input is project or issue scope, hand it to `$dev-project-orchestrator`, which
may discover the dependency graph and dispatch issue workers. For a complete
explicit set, inspect the supplied branches and PR metadata only to validate the
stated strategy.

## Integration Modes

- **Direct ordered merge**: PRs are independent or dependency-ordered, each passes its own gate, and combined validation risk is low. Process one resolved-base PR at a time through `$dev-merge-handoff`; after live merge confirmation, refresh the resolved base and re-check remaining PRs.
- **Batch integration branch**: consume the controller-resolved branch strategy, including the default isolated batch. Child PRs target that branch and pass their own merge gates; validate the complete branch before one aggregate promotion PR.
- **Scratch validation branch**: when only conflict detection/combined validation is requested, merge candidate heads into a disposable local branch. This does not mark PRs merged or authorize publishing that scratch branch.
- **Blocked**: Required PRs are not ready, contracts are unstable, conflicts need owner decisions, checks are red, product review failed, or external dependencies are unavailable.

## Workflow

1. Confirm the supplied PR/branch set, base branch, and stated order strategy.
   If any is absent, return `input-required`; route project, issue-set, or
   dependency-sequence scope to `$dev-project-orchestrator`. Capture PR URLs,
   issue IDs, head branches, latest commits, status checks, review state,
   mergeability, and changed files for the supplied set.
2. Confirm each PR has completed issue-level `$dev` expectations: validation evidence, code review handling, CI state, and PR Product Review when required.
3. Validate the supplied integration order:
   - Foundation/schema/API PRs before client PRs.
   - Generated types or shared contracts before dependents.
   - Data migrations before code that assumes migrated state only when rollback is safe.
   - Risky cross-cutting changes before dependent polish only if they have stable validation.
4. Decide the supplied strategy's integration mode: direct ordered merge,
   batch integration branch, scratch validation branch, or blocked.
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
7. For a batch branch, reuse the controller-recorded remote branch and land child PRs through their normal gates. For scratch validation only, keep the branch local unless publication is authorized; scratch merges are not delivery evidence.
8. Route repairs:
   - Conflicts or review-comment fixes -> `$dev-implementer` on the affected PR.
   - Red checks -> `$dev-ci-repair`.
   - Missing product conformance -> `$pm-pr-product-review` or the responsible `$dev` worker.
   - Unstable external/API behavior -> `$dev-api-research` or `$dev-spike`.
9. Run combined validation after the candidate set is conflict-free. Use the narrowest reliable project-level checks first, then broaden for shared contracts, migrations, or user-facing flows.
10. Land issue PRs through `$dev-merge-handoff` in the planned order. If any
    issue PR is a repository-defined production promotion, stop and route the
    production-promotion decision to `$release`. After each live-confirmed
    resolved-base merge, update the base branch, re-check remaining PRs, and adjust
    the plan if conflicts or checks change.
11. After every required batch issue is integrated, reconcile upstream drift,
    run combined validation, and open/reuse one aggregate PR to the recorded
    promotion target. Include the exact child PR set and validation evidence.
    Apply the [merge gate](../dev-merge-handoff/SKILL.md#merge-gate) to its current
    head, including repository review, CI and merge authority. Verify the merged
    aggregate commit and applicable final environment/acceptance handoff before
    reporting batch completion. Preserve human-review waits and active branch
    dependencies before cleanup.
12. Produce rollback and follow-up notes for the combined release candidate,
    then hand the verified upstream state to `$release` only when production
    promotion is requested.

## Output

```markdown
## Integration Plan

Decision: <direct ordered merge | batch integration branch | scratch validation branch | blocked>
Base branch:
PRs:
Integration branch:
Input status: <complete | input-required | routed to dev-project-orchestrator>

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

- `$dev-implementer`:
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
