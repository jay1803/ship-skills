---
name: dev-merge-handoff
description: "Gate and complete one issue PR merge into the resolved integration base, cleanup, and test-revision handoff. Production promotion belongs to release."
metadata:
  owner: jay1803
  family: develop
  maturity: stable
  distribution: develop
---

# Dev: Merge Handoff

Own the final issue-PR merge gate into the resolved issue PR base. This skill completes Dev's
integration lifecycle; it does not create production tags, GitHub Releases, or
deploy to production.

Read the canonical [branch strategy](../dev/references/branch-strategy.md) before resolving bases or merge direction.

## Boundary

- Operate on exactly one issue PR whose base matches the recorded branch strategy, including a temporary batch branch.
- Route a production-promotion PR to `$release`. Repository-defined ordinary
  issue PRs to main retain their issue workflow and merge-authority rules.
- Reject an unrecognized or mismatched base until the strategy is reconciled.
- Aggregate batch promotion is owned by `$dev-integration-manager`, which
  applies the same merge gates to the combined candidate.
- For native stacks, read the [stack contract](../dev/references/stacked-prs.md)
  before a merge or cleanup. This Skill can return one layer's gate evidence;
  a command including other unmerged issues goes to the assigned integration
  executor for the exact authorized group. Stack-ready is not merged or Done.
- Do not write implementation fixes. Route conflicts or review findings to
  `$dev-implementer` and red checks to `$dev-ci-repair`.
- Never bypass branch protection, force-merge, or discard dirty local work.

## Inputs

- PR number or URL, inferred from the current branch only when unambiguous.
- Dev mode: `fast`, `standard`, or `strict`; omitted means standard.
- The controller's accepted gate record for the exact PR head: verification
  (`$dev-verifier` selected and passed, or unselected with current evidence),
  technical Review (an accepted result, identical-tree reuse, or a recorded
  permitted skip), open findings against the mode threshold, acceptance
  deferrals with their follow-up, validation exceptions, and `Skipped /
  Unverified` entries.
- Issue branch/worktree information when available.
- Project deploy skill and any required test-environment acceptance contract.

## Merge Gate

The controller has already adjudicated verification, Review, findings and
deferrals. Gate on its accepted record plus live PR facts; do not re-derive
those decisions. Fetch live state first:

```bash
gh pr view <pr> --json number,url,state,headRefName,baseRefName,headRefOid,mergeable,mergeStateStatus,reviewDecision,statusCheckRollup
```

Merge only when all of these hold:

1. The live base is the recorded issue PR base and the live head is the head
   the record names. For a native stack, also verify immediate base,
   membership/order and trunk; repository merge requirements apply to the trunk.
2. The accepted record covers every gate listed under Inputs for that head and
   shows no open blocking finding. A missing gate, a record for another head, standalone verify-only evidence offered in its place,
   or a record that contradicts a current user or repository requirement (such
   as a required independent Review) blocks: return it to the controller.
3. Any validation exception in the record names this head and the merge stage.
   A PR-preparation exception does not cover merge, and a Failed command stays
   Failed ([validation evidence](../dev-test/references/validation-evidence.md)).
4. No merge conflict or independently required unresolved review thread remains.
5. Required CI and branch protection pass on the live head. If they are only in
   flight, wait or use repository-approved auto-merge for the resolved base;
   for a native stack, only with verified provider support and repository
   authority for the exact group. Never bypass them.
6. Any pre-merge external or environment verifier still required after mode
   waivers passed against the live head.
7. The user's request or applicable repository policy authorizes this executor
   to merge this exact PR: a full-lifecycle `$dev` request does; a CI or review
   repair request relayed here does not unless it named the merge. A user
   restriction, an unmet human review/merge rule or another recorded merge
   executor withholds it. Otherwise return `waiting (human merge)` with the
   exact PR, head, accepted evidence and next owner.

Apply the retry limits owned by the enclosing `$dev` workflow.

## Merge And Cleanup

Once the gate passes, merge the PR targeting the resolved issue base with the repository's
approved method. Apply the stack contract before native stack mutations; the
ordinary single-PR example below is not an upper-layer group-merge instruction:

```bash
gh pr merge <pr> --squash
```

Capture the resulting integration commit and confirm the PR is `MERGED` before any
cleanup. Then:

- confirm or delete the remote issue branch only after merge is proven;
- remove an issue worktree only when it is clean and not the only usable
  worktree;
- prune worktree metadata;
- delete the local issue branch, allowing force-delete after a verified squash
  merge only;
- preserve and report any dirty or ambiguous state instead of forcing cleanup;
- never delete `develop`, `main`, `master`, `trunk`, the current PR base, or a
  temporary batch branch still receiving child work. Only clean this issue head.
- retain a stack head/worktree still needed by a layer or active owner. Verify
  automatic retarget/rebase and dependency release before cleanup; unknown
  membership/retention state stays retained with its reconciliation owner.

Run the cleanup helper from a surviving checkout once `MERGED` is verified:

```bash
"<dev-merge-handoff-skill-dir>/scripts/cleanup_merged_pr_worktree.sh" \
  --confirmed-merged --branch <issue-head> \
  --base <base> --worktree <issue-worktree> [--delete-remote] [--squash-merged]
```

`--confirmed-merged` is required and asserts the verified merge; add
`--delete-remote` for issue-head deletion and `--squash-merged` only for a
verified squash merge. Use the surviving checkout for subsequent commands if the
issue worktree is removed. Check the head/worktree identity and the protections
above before invocation; the helper is not a substitute for those checks. Cleanup failure after a confirmed merge
is `merged with cleanup blocker`, not a failed merge.

Before any remote deletion the helper queries the exact remote head's effective
deletion rules through `gh api`: `repos/{owner}/{repo}/rules/branches/{branch}`
and, when present, classic `repos/{owner}/{repo}/branches/{branch}/protection`.
It deletes only when a deletion rule is absent and classic protection is absent
or reports `allow_deletions` enabled. A deletion rule, classic protection that
disallows deletion, a failed or unavailable query, an unparseable response, a
remote that does not name an owner/repo, or a push target that differs from the
configured URL (`pushurl` or an `insteadOf` rewrite) all retain the remote head.
A pass by the account's bypass permission is not evidence of permission; the
helper never uses `--force` or `--admin`, and it never deletes under a
restriction. Local branch and worktree cleanup proceed under their own
conditions regardless of the remote result.

The helper exits 0 for a retained remote head. Read its stdout key-value lines:
`remote_branch` (`deleted`, `already_absent`, `retained` or `not_applicable`),
`remote_branch_reason` and `remote_branch_evidence` (the queried host, repository,
branch, rule types, ruleset ids and classic status). A non-zero exit, or no
`remote_branch` line, means the remote head is unknown: retain it and report
`merged with cleanup blocker` when deletion was requested. `retained` without
`--delete-remote` is an intentional retention; record it with the owner who
accepts any follow-up. Map `retained` under a requested `--delete-remote` to
`merged with cleanup blocker`. Do not delete a retained head with a manual
command, `gh api` or another path. Deletion under a restriction needs a separate
explicit user authorization that names this exact branch and rule, and must be
recorded as that exception.

### Cleanup Evidence

Before tracker closeout or a terminal callback, record the exact repository,
PR/head and worktree plus a separate outcome for the remote issue branch, local
issue branch and issue worktree: `deleted`, `already absent`, or `retained`
with reason. Verify post-operation state through a successful remote ref query,
local refs, and worktree inventory/path checks. Remote-tracking refs, a helper
success message, or an unavailable/failed query do not prove remote absence.
An already deleted remote head needs no repeated delete or attribution guess.
Helper `remote_branch=deleted` and `already_absent` map to those outcomes.
`retained` carries the helper's reason and evidence unchanged. `not_applicable`
means no remote is configured; report it with its reason, not as a deletion.
A helper success exit or a `retained` result with rule evidence is never
treated as the remote head being gone.

A required deletion that is unsafe, fails or cannot be verified stays pending
with the retained/unknown resource, evidence, next action and responsible owner;
report `merged with cleanup blocker`. Do not claim full lifecycle completion or
silently drop it from the handoff. For intentional retention (such as a primary
checkout or an explicit user instruction), record the applicable boundary and
who accepts any remaining follow-up. Preserve the existing tracker policy;
issue Done or a verified merge is not itself cleanup evidence. Carry these
outcomes unchanged into Dev State and project callbacks; project controllers
accept cleanup separately from dependency readiness.

## Test Environment Handoff

Waived real-environment deployment/verification and human acceptance are
follow-ups, not `merged awaiting test deploy` or a reason to create a deploy
skill; report the exact merged revision and unverified environment. For remaining
required or explicitly requested deployment work, resolve the environment
mapping from repository policy after merge. A temporary
batch branch has no implicit develop/test mapping. For a child with no required
branch deployment, report integrated-to-batch with deployment not applicable;
keep explicit required preview/runtime/acceptance gates pending until verified.
For a base with a configured test environment, resolve the project deploy skill:

- If deployment from the resolved base is automatic, invoke `verify` for `environment:
  test` and the exact merged integration commit.
- If it is manual and the user's Dev request authorizes test deployment, invoke
  `deploy` for that commit.
- If manual deployment was not authorized, return `merged awaiting test deploy`
  with the exact next action.
- Require runtime evidence that the observed test revision matches the merged
  integration commit or a documented immutable equivalent.

If the project deploy skill is missing, route to `$deploy-skill-creator`. Do not
invent project deployment commands. Fast mode may record optional test
deployment/verification under `Skipped / Unverified`, but the result must
say `test unverified`; it must not claim the environment passed.

When a standalone deploy or live-outcome verification returns `fail`, `blocked`,
or `unverified`, stop at that evidence boundary. Do not retry a side-effecting
deployment, mutate tracker completion, or transform it into merge handoff until
a new explicit user request or authorization covers that action.

## Tracker And Release-Candidate Handoff

Close only implementation issues actually covered by the merge whose remaining
gates are satisfied; acceptance moved to a follow-up follows the
[Done rule](../dev/references/development-mode-contract.md#done-while-acceptance-is-pending).
Never close a follow-up acceptance ticket from a code merge. Valid three-round
acceptance deferrals likewise permit engineering closeout with the original
unmet criterion and follow-up disclosed; keep the follow-up open.

Return the exact base and integration commit, linked issues, test receipt, user-facing change
summary, migrations/compatibility notes, and rollback risk. This is the input to
a later `$release` only after the batch is promoted when applicable. Child
integration evidence returns to the project controller; it is not a complete
batch release candidate or a production release.

## Output

```markdown
## Dev Merge Handoff

Decision: <waiting | fixing | blocked | merged | merged awaiting test deploy | merged awaiting human acceptance | merged with cleanup blocker>
PR: <URL>
Base: <resolved issue PR base>
Head: <branch>
Reviewed head: <SHA>
Integration commit: <SHA or pending>
Mode: <fast | standard | strict>
Skipped / Unverified: <entries or none>

### Gate Evidence
- Accepted record: <source and head; verification, technical Review, deferrals>
- Comments/conflicts:
- CI/protection:
- Merge authority:

### Test Environment
- Project deploy skill:
- Action: <deploy | verify | not run>
- Requested ref:
- Observed ref:
- Health/smoke evidence:

### Cleanup And Tracker
- Remote issue branch: <exact ref, outcome, verification>
- Local issue branch: <exact ref, outcome, verification>
- Issue worktree: <exact path, outcome, verification>
- Cleanup follow-up: <none | retained/unknown resources, reason, next action, owner>
- Issue state:

### Release Candidate
- Included issues:
- User-facing change:
- Migration/compatibility notes:
- Risks/rollback:
```
