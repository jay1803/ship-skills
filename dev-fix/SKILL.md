---
name: dev-fix
description: >-
  Resolve technical PR review comments and merge conflicts after code review or merge-gate feedback. Use to target an explicit PR, the current Dev-state PR, or by default the most recent PR referenced in the current conversation; check out the PR branch, resolve merge conflicts, inspect unresolved inline review threads, apply narrow in-scope fixes, reply to invalid or out-of-scope comments, resolve handled threads, rerun relevant checks, commit, push, and hand the PR back to $dev-release-handoff when conflicts and blocking comments are clear.
---

# Dev: Fix

Fix merge-gate blockers narrowly and keep the PR inside the approved scope. Own PR review-comment fixes and PR merge-conflict resolution directly; do not route to a separate conflict/comment skill.

The default PR target is the last PR referenced in the current conversation, not the newest repository PR. Repository recency is only valid when the user explicitly asks for the latest repo PR.

Use `scripts/fetch_comments.py` after checking out the selected PR branch to fetch PR conversation comments, reviews, and inline review threads.

## Target Resolution

Resolve exactly one PR in this order:

1. Use a PR URL or PR number explicitly provided by the user.
2. Use the PR recorded in the current Dev state or calling workflow handoff.
3. If no PR is provided, scan the current conversation and use the most recent PR reference, including:
   - a full URL such as `https://github.com/OWNER/REPO/pull/123`
   - a `PR #123` reference clearly tied to the current repository
   - a prior `gh pr create` result
   - a Codex create-pr directive containing a PR URL
4. If no unambiguous PR exists in the conversation, ask for the PR number or URL. Do not substitute the newest open PR.

Stop if the resolved PR is closed, merged, not viewable, or not writable for required code changes, unless the user explicitly asks to inspect it only.

## Merge-Gate Rules

- Resolve every merge conflict when conflicts block merge readiness. Do not hand a PR back to `$dev-release-handoff` with conflicts remaining.
- Fix a review comment only when it makes sense against the actual code, tests, issue/spec context, and current diff.
- Reply to comments that do not need code changes, then resolve the thread when the rationale is complete.
- Leave a thread unresolved only when it needs a product, security, maintainer, permission, or scope decision.
- Stage only files changed for valid review fixes or conflict resolution. Do not sweep up unrelated dirty work.

## Workflow

1. Confirm repo and auth state.

   ```bash
   git status --short --branch
   gh auth status
   gh repo view --json owner,name,url
   ```

   If the worktree is dirty, inspect the paths. Continue only when the dirty changes are unrelated and will not be touched.

2. Verify the selected PR.

   ```bash
   gh pr view <pr-number-or-url> --json number,title,url,state,headRefName,baseRefName,headRepositoryOwner,headRepository,isCrossRepository,author,mergeable,mergeStateStatus
   ```

   Capture PR number, URL, head branch, base branch, author, fork status, writability, mergeability, and merge state.

3. Check out the PR branch when code changes may be needed.

   ```bash
   gh pr checkout <pr-number-or-url>
   git status --short --branch
   ```

   If checkout fails because the PR is from a fork or non-writable branch, inspect comments when possible but do not promise updates.

4. Resolve merge conflicts first when requested or when mergeability is dirty/conflicting.
   - Fetch the base branch: `git fetch origin <base-branch>`.
   - Bring the PR branch up to date using the repo's convention: merge `origin/<base-branch>` or rebase onto it when that is clearly the local pattern.
   - Resolve each conflict deliberately by understanding both sides' intent. Never use blanket `ours`/`theirs`, force checkout, reset, or broad destructive git commands.
   - If a conflict cannot be resolved without a product, architecture, security, or maintainer decision, stop and report the exact files and decision needed.
   - Resolving conflicts refreshes the diff that review comments refer to, so do this before comment handling.

5. Fetch review comments and inline threads.

   ```bash
   python3 "<dev-fix-skill-dir>/scripts/fetch_comments.py" > /tmp/pr-comments.json
   jq '.review_threads[] | select(.isResolved | not) | {id,isOutdated,path,line,startLine,comments}' /tmp/pr-comments.json
   ```

   Confirm `/tmp/pr-comments.json` matches the selected PR number. Treat unresolved inline review threads as the target "code comments." Top-level PR conversation comments are context unless the user explicitly asks to handle them too.

6. Evaluate each unresolved inline thread.

   - If the user named a specific thread or comment, handle only that target.
   - If `$dev-release-handoff` routed the PR here for merge-gate repair, handle every unresolved inline thread, prioritizing high- and medium-severity blockers.
   - Otherwise handle every unresolved inline thread on the selected PR.
   - Read the full thread and identify the latest actionable human or bot review comment.
   - Inspect the referenced file, current code, nearby tests, PR diff, product spec, and technical approach before editing.
   - Apply code fixes only when the comment is technically correct, still relevant to the current diff, and in scope for the PR.
   - Reply with evidence when a comment is invalid, obsolete, already handled, or out of scope.
   - Stop for a product, security, or scope decision if the comment would change approved behavior or cannot be judged from repository evidence.

7. Validate changed code.

   Always run:

   ```bash
   git diff --check
   ```

   Also run the smallest useful test, lint, typecheck, or build command for the touched area. If broad validation fails on unrelated existing issues, report the exact blocker and include the focused validation that did run.

8. Commit and push when code changed.

   Stage only the files changed for valid review fixes and conflict resolution.

   ```bash
   git status --short
   git diff --stat
   git add <changed-files>
   git commit -m "fix: address PR merge blockers"
   git push
   ```

   Use the repository's commit style when one is evident. If commit signing blocks progress, create the commit unsigned with `git -c commit.gpgsign=false commit ...` and report that signing was skipped. Do not commit unrelated dirty files.

9. Reply to handled threads.

   Use `addPullRequestReviewThreadReply`:

   ```bash
   gh api graphql \
     -f query='mutation($threadId: ID!, $body: String!) { addPullRequestReviewThreadReply(input: { pullRequestReviewThreadId: $threadId, body: $body }) { comment { url } } }' \
     -F threadId="$THREAD_ID" \
     -F body="$(cat /tmp/review-reply.md)"
   ```

   For code fixes, include what changed and the validation command. For no-code replies, explain why no code change is needed.

10. Resolve handled threads only when complete.

   ```bash
   gh api graphql \
     -f query='mutation($threadId: ID!) { resolveReviewThread(input: { threadId: $threadId }) { thread { id isResolved } } }' \
     -F threadId="$THREAD_ID"
   ```

   Leave a thread unresolved when it needs a product decision, maintainer confirmation, unavailable permission, or work you could not complete.

11. Re-check mergeability and hand back.
   - Re-fetch `mergeable`, `mergeStateStatus`, and unresolved threads for the same PR.
   - If the base moved and re-conflicted while you worked, resolve again within the caller's retry cap.
   - If conflicts are clear and no high/medium thread remains unresolved, hand back to `$dev-release-handoff` with the PR number and a concise summary.
   - If CI checks are red after the fix, route to `$dev-ci-repair`.
   - If conflicts or high/medium comments remain blocked by a decision, stop with the exact blocker instead of bouncing the PR back.

## Decision Rubric

A comment generally makes sense when it identifies a real bug, user-visible regression, contract mismatch, missing test for changed behavior, unsafe edge case, security risk, performance problem, or maintainability issue directly introduced by the PR.

A comment generally does not make sense when it conflicts with settled product requirements, asks for broader refactoring outside PR scope, relies on an incorrect API or platform assumption, repeats behavior already covered in current code, or only refers to an outdated diff that is no longer present.

When uncertain, inspect the source of truth first: provider docs, API contracts, tests, issue specs, or nearby implementation history. If the answer still depends on a product decision, reply with the blocker and leave the thread unresolved.

## Output

```markdown
## Review Fix Result

### Target PR
- <number, URL, base branch, head branch, and why this PR was selected>

### Conflicts
- <resolved / none / blocked, with files and rationale>

### Fixed
- <comment/thread and change made>

### Replied / Not Changed
- <comment/thread and rationale>

### Commit / Push
- <commit hash and push status, or "No code changes">

### Validation
- `<command>`: <result>

### Remaining
- <unresolved comment, conflict, blocker, or "None">

### Recommended Next Step
<`$dev-release-handoff`, `$dev-ci-repair`, `$dev-code-review`, or stop.>
```
