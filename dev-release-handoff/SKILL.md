---
name: dev-release-handoff
description: >-
  Prepare merge-readiness and land a GitHub PR after dev, review fixes, CI, and PR Product Review are complete. Use before merge, or when asked to squash-merge, auto-merge, land, ship, delete a merged PR branch, or clean up a merged issue worktree. Verifies review/comment/conflict/check gates; routes blockers to $dev-fix or $dev-ci-repair; squash-merges, deletes remote/local branches, removes clean local worktrees, then moves related Linear issues to Done.
---

# Dev: Release Handoff

Own the final merge gate. Summarize merge readiness, enforce merge rules, squash-merge only when safe, clean up merged Git branches/worktrees, and close the tracker loop after a successful merge.

This skill does not write implementation fixes. If unresolved high/medium review comments, new external-review comments, or conflicts block the merge, route the PR to `$dev-fix`, then re-check. If checks are red, route to `$dev-ci-repair`.

## Inputs

- PR number or URL. If none is given, infer the PR from the current branch with `gh pr view --json number,url,headRefName` when unambiguous.
- PR Product Review result when available. If PR Product Review has not passed for a dev workflow PR, route to `$pm-pr-product-review` before merging.
- Dev Git Setup result when available, especially the issue branch and worktree path. If missing, infer from the PR head branch and `git worktree list --porcelain`.
- Operate on exactly one PR per run. Do not bypass branch protection, force-merge, or merge a PR the user only asked to inspect.

## Merge Rules

A PR may be squash-merged only when all rules hold:

1. **PR Product Review is passed or explicitly not required** for the workflow.
2. **No review is still pending**, using Pending Review Handling below.
3. **The latest configured external review has finished when external review is in use.** A start comment or accepted API request is not enough.
4. **All high- and medium-severity review comments are resolved.** Low-severity or nit comments may remain unresolved.
5. **No merge conflicts.** `mergeable` is `MERGEABLE`, and `mergeStateStatus` is not `DIRTY` or `CONFLICTING`.
6. **Required checks are passing or in-flight.** If GitHub rejects the merge because checks are still running, wait or enable auto-merge. If checks are red for real, stop or route to `$dev-ci-repair`.

Never force-merge or work around branch protection.

## Comment Severity

Read severity from each unresolved review thread:

- **High**: marked high, critical, blocking, or clearly about correctness, security, data loss, or a broken contract.
- **Medium**: marked medium, or a real non-blocking issue such as a missing edge case, weak test, or questionable pattern.
- **Low**: marked low, minor, nit, style, or preference.

Use the reviewer's explicit label when present. If uncertain between high and medium, treat it as the higher severity.

Fetch unresolved threads with the existing helper when available:

```bash
python3 "<dev-fix-skill-dir>/scripts/fetch_comments.py" > /tmp/pr-comments.json
jq '.review_threads[] | select(.isResolved | not) | {path,line,comments}' /tmp/pr-comments.json
```

## Pending Review Handling

Do not wait forever for every re-review:

- **First review, with no completed review yet:** wait until it finishes, then re-evaluate.
- **Second review or later:** inspect the most recent completed review round.
  - If it contains any high-severity comment, wait for the current pending review and re-evaluate.
  - If it contains no high-severity comment, continue evaluating the other merge rules.

Poll every 60 seconds for up to 30 minutes unless the user sets a different window. If a first review never completes within the window, stop and report rather than merging unreviewed code.

Use:

```bash
gh pr view <pr> --json number,url,state,headRefName,baseRefName,headRefOid,mergeable,mergeStateStatus,reviewDecision,reviewRequests,latestReviews,reviews,statusCheckRollup
```

## Workflow

1. Resolve the target PR and capture number, URL, head branch, base branch, latest commit, state, remote name, and local worktree path for the head branch when present. Stop if it is closed or not viewable unless the user explicitly wants a closed PR inspected.
2. Verify `gh` access with `gh auth status` when GitHub state or merging is required. If unauthenticated, stop and ask the user to log in.
3. Confirm PR Product Review.
   - If the PR came from the Dev/build flow and `$pm-pr-product-review` has not passed, route to `$pm-pr-product-review` before merging.
   - If PR Product Review is explicitly out of scope, record why.
4. Gather merge status in one pass: mergeability, conflicts, pending/completed reviews, external-review lifecycle comments when present, unresolved review threads and severities, and check status.
5. Evaluate rules in this order: PR Product Review, pending review, external-review finished signal, conflicts, unresolved high/medium comments, checks.
6. Decide:
   - **All rules pass** -> squash-merge.
   - **First review, external review, or live high-severity re-review is pending** -> wait and re-evaluate.
   - **Conflicts, new external-review findings, or unresolved high/medium comments remain** -> route to `$dev-fix`, then re-fetch and re-evaluate.
   - **CI checks fail** -> route to `$dev-ci-repair`, then re-fetch and re-evaluate.
   - **Branch protection or permissions block merge** -> stop and report.
7. Enforce loop caps:
   - Route to `$dev-fix` at most five times for the same PR.
   - Stop if a reviewer has reviewed the PR more than five times without convergence.
   - When a cap trips, report the PR, cap, remaining blockers, and next action.

## Squash Merge

Once all rules pass:

```bash
gh pr merge <pr> --squash --delete-branch
```

- If the merge is rejected only because required checks are still running, wait and retry, or use `gh pr merge <pr> --squash --auto --delete-branch`.
- Capture the squash commit SHA and confirm the remote branch was deleted. If GitHub did not delete the remote head branch, verify the PR is merged before deleting it with `git push <remote> --delete <head-branch>`.
- Report the rule evaluation that allowed the merge.

## Local Cleanup

Only clean local Git state after the PR is confirmed merged. Never clean up a branch or worktree just because a merge command was attempted.

Use the helper for normal cleanup:

```bash
scripts/cleanup_merged_pr_worktree.sh \
  --confirmed-merged \
  --branch feature/AG-1 \
  --base develop \
  --worktree ../Repo-AG-1 \
  --squash-merged \
  --delete-remote
```

Cleanup rules:

- Delete the remote branch only after confirming the PR is merged. Prefer `gh pr merge --delete-branch`; use `git push <remote> --delete <head-branch>` only as a fallback when the remote branch still exists.
- Remove a local issue worktree only when it is clean and not the only usable worktree. If it is dirty, report the exact path and `git status --short`; do not force-remove it.
- Run `git worktree prune` after removing a worktree.
- Delete the local head branch after the worktree is removed or the current checkout has switched away from it.
- For squash merges, `git branch -d <head-branch>` may fail because the branch commits are not ancestors of the base branch. `git branch -D <head-branch>` is allowed only after the merged PR and squash commit are verified.
- Never delete protected base branches such as `main`, `master`, `develop`, or `trunk`.
- If cleanup is blocked after a successful merge, report `merged with cleanup blocker`; do not try destructive cleanup, and do not imply the local workspace is clean.

## After Merge

Only after the squash-merge succeeds, clean local Git state when safe and move related Linear issues to Done:

1. Verify the PR is merged and record the squash commit SHA.
2. Verify the remote head branch is absent, or delete it after the merged PR is confirmed.
3. Remove the clean local issue worktree when one exists.
4. Delete the local head branch. For squash merges, force-delete only after the merge is verified.
5. Run `git worktree prune`.
6. Identify related issue IDs from branch name, PR title/body, commits, and linked issues.
7. Use `$proj-manage` to move only the issues actually covered by the merge to the workspace's Done status. Do not close an umbrella parent just because one child shipped.
8. Add a short Linear comment with the merged PR link when useful for traceability.
9. If tools are unavailable, report that the PR merged but tracker update could not be applied, and provide the exact tracker-ready update.
10. If issue identity is ambiguous, do not guess. Report the successful merge and ask which issue to close.

## Stop Conditions

Stop and report without merging when:

- PR Product Review failed or is required but missing.
- A first review does not finish within the wait window.
- A configured external review has only a start signal, has no finish signal, or produced comments that have not been inspected.
- Five fix loops or more than five review rounds fail to converge.
- High/medium comments, conflicts, red required checks, branch protection, auth, permissions, or external provider failures remain unresolved.
- Local cleanup is requested before the PR is confirmed merged, or the local worktree/branch cleanup would require discarding dirty local changes.
- The PR is closed, not viewable, or not mergeable for reasons outside this skill's repair routes.

## Output

```markdown
## Release Handoff

Decision: <merged | merged with cleanup blocker | waiting | fixing | blocked>
PR: <url>
Base: <base branch>
Head: <head branch>
Commit: <sha>

### Rule Check
- PR Product Review: <passed | not required | blocked>
- Pending review: <clear | waiting | skipped re-review churn>
- External review: <finished | waiting | not configured | blocked>
- High/medium comments: <clear | blocking>
- Conflicts: <clear | blocking>
- Checks / protection: <clear | waiting | blocking>

### What Changed
- <summary>

### Verification
- <tests, builds, lint, CI, review evidence>

### Merge Result
- <squash commit and branch deletion, or "Not merged">

### Cleanup Result
- <remote branch, local worktree, local branch, and worktree prune result>

### Tracker Result
- <Linear issues moved to Done, tracker-ready draft, or "Not applicable">

### Risks / Rollback
- <risk and rollback note, or "None">

### Follow-Ups
- <follow-up issue or "None">
```
