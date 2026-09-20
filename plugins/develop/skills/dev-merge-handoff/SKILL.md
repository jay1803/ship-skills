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
- Do not write implementation fixes. Route conflicts or review findings to
  `$dev-implementer` and red checks to `$dev-ci-repair`.
- Never bypass branch protection, force-merge, or discard dirty local work.

## Inputs

- PR number or URL, inferred from the current branch only when unambiguous.
- Dev mode: `fast`, `standard`, or `strict`; omitted means standard. Preserve the selected defect threshold and mandatory acceptance/CI gates.
- Skipped/unverified entries and deferred acceptance ticket/draft in every mode.
  Apply the [unattended validation rule](../dev/references/development-mode-contract.md#unattended-validation-and-deferred-acceptance)
  before interpreting old acceptance labels or environment requirements.
- Verification state: **selected and pass** from `$dev-verifier` and the exact
  head revision it verified, or **unselected with receipt-backed current
  evidence** from the Resume Receipt.
- PR Product Review and configured technical-review results.
- Issue branch/worktree information when available.
- Project deploy skill and any required test-environment acceptance contract.

Standalone `verify/*` evidence is not a substitute for this input. It may be a
fresh resume anchor for a later authorized Dev route, but it neither authorizes
a repair/merge/tracker closeout nor proves the selected full-Dev validation,
Review, CI, and Product Review gates.

## Merge Gate

Before merge, fetch live PR state and require the mode-appropriate evidence:

1. Base is the expected integration branch and head is the reviewed commit.
2. Exactly one current verification state is present for the exact PR head:
   **selected and pass** from `$dev-verifier`, or **unselected with
   receipt-backed current evidence**. The unselected state must bind the Resume
   Receipt's route, selected phase plan, validation floor, and current
   validation/verification evidence to the PR head. Missing, stale, blocked, or
   failed verifier evidence is never unselected. A later code, test, config,
   generated-output, or documentation change makes a selected verifier stale
   and requires a fresh verification run; it also requires re-evaluating the
   receipt-backed unselected state.
3. PR Product Review passed or is explicitly not required. Fast mode may carry
   its authorized skip only when the handoff records it under `Skipped / Unverified`.
4. Selected technical Review has a complete, current accepted combined result.
   Every selected run includes the thermo-nuclear code-quality rubric. Fast may record its
   authorized Review skip; an unselected tracked-artifact gate requires the
   matching Resume Receipt rather than fabricated review evidence.
5. No finding crosses the selected [severity threshold](../dev/references/review-severity-policy.md):
   P0/P1 block standard; P0/P1/P2 block strict. Remaining advisories do not
   require an extra repair round. Required acceptance, CI, and branch protection
   remain separate gates; resolve ambiguous native labels through Review's
   source clarification path rather than converting high/medium mechanically.
   Fast retains its unskippable safety and primary-path conditions.
6. No merge conflict remains.
7. Required CI and branch protection checks pass. If they are only in flight,
   wait or use repository-approved auto-merge for the resolved base; never bypass them.
8. Any additional pre-merge external or environment verifier still required after mode waivers passed
   against the exact PR head.

When validation includes baseline failures or filtered alternatives, consume the
same [Test Result records](../dev-test/references/validation-evidence.md) and
check that the exact exception covers this head and the merge stage. An earlier
PR-preparation exception does not waive merge checks. Preserve Failed results,
new failures and independently required CI; do not reinterpret them as clean.

Use live GitHub evidence such as:

```bash
gh pr view <pr> --json number,url,state,headRefName,baseRefName,headRefOid,mergeable,mergeStateStatus,reviewDecision,reviewRequests,latestReviews,reviews,statusCheckRollup
```

Apply the retry limits owned by the enclosing `$dev` workflow. A requested or
started review is not evidence that review finished.

## Merge And Cleanup

Once the gate passes, merge the PR targeting the resolved issue base with the repository's
approved method, normally:

```bash
gh pr merge <pr> --squash --delete-branch
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

Use `scripts/cleanup_merged_pr_worktree.sh` after merge. Cleanup failure after a
confirmed merge is `merged with cleanup blocker`, not a failed merge.

## Test Environment Handoff

Apply the mode waiver first: real-environment deployment/verification and
human acceptance are deferred, not `merged awaiting test deploy` or a reason
to create a deploy skill. Report the exact merged revision and unverified
environment in the handoff, with any separate human follow-up. For remaining
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
a fresh Issue Route receipt grants the applicable authority.

## Tracker And Release-Candidate Handoff

Close only implementation issues actually covered by the merge and whose
remaining mode-required gates are satisfied. Waived acceptance does not block
engineering Done or successors; leave a separate human acceptance ticket pending
and report its evidence as unverified. Never close that ticket from a code merge.
Preserve waits only for gates remaining after the mode waiver.

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

### Gate Evidence
- Dev verification: <selected and pass: verifier/head | unselected with receipt-backed current evidence: receipt route/head/evidence>
- Product Review:
- Technical review:
- Comments/conflicts:
- CI/protection:

### Test Environment
- Project deploy skill:
- Action: <deploy | verify | not run>
- Requested ref:
- Observed ref:
- Health/smoke evidence:

### Cleanup And Tracker
- Remote branch:
- Local worktree/branch:
- Issue state:

### Release Candidate
- Included issues:
- User-facing change:
- Migration/compatibility notes:
- Risks/rollback:
```
