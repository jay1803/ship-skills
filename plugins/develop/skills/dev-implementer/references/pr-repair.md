# PR Repair Within Implementation

Use this reference inside `$dev-implementer` for a combined Review repair batch,
technical PR comments, or merge conflicts. Keep the existing implementation
owner where suitable; this is a repair input/validation path, not a new worker.
Preserve the exact PR, approved scope, and current Review Run across the handoff.

Code changes, pushes, replies, and thread resolution require the caller's
existing authorization for those actions. A read-only review never grants
repair or posting authority; return findings or proposed replies when writing
was not requested. PR/issue lifecycle acceptance remains controller-owned.

The default PR target is the last PR referenced in the current conversation, not the newest repository PR. Repository recency is only valid when the user explicitly asks for the latest repo PR.

Resolve `<dev-implementer-skill-root>` from the parent implementer `SKILL.md`, then use `<dev-implementer-skill-root>/scripts/fetch_comments.py` after checking out the selected PR branch to fetch PR conversation comments, reviews, and inline review threads.

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

## Review v2 Handoff Gate

When `$review` is the caller, require its accepted combined artifact for the
current PR/head and the complete repair state: run ID, generation, attempt
count, generation status, previous/current head, base, change evidence, and
prior artifact. Verify `Generation = Attempt Count + 1` and the effective
limit/authority from the [shared state contract](../../dev/references/dev-review-v2-contract.md#repair-and-re-review-state)
before inspecting or changing code. Missing, partial, discontinuous or
ceiling-exhausted unresolved state returns `blocked` without resetting the run,
starting another generation or applying a finding. The default limit remains
five; only an exact verified user override changes it for the named run.

Require the combined artifact to account for all core, signaled conditional,
mode-required external, judge, and final-base/head evidence. Apply the
[severity policy](../../dev/references/review-severity-policy.md): require
`repair-required` and treat all confirmed mode-blocking implementation findings
as one repair batch. Retain nonblocking findings; include small scoped fixes
only in an already-required batch and within explicit user fix permissions.
A record-only/no-fix P2/P3 instruction also excludes acceptance-related items;
do not add them opportunistically alongside a P1 fix. Preserve bound acceptance
exceptions and failed/unverified evidence without converting them to pass. An advisory-only artifact returns without
editing or opening another review round. Mandatory acceptance/CI gaps remain
separate gates. Do not accept an
individual specialist artifact, an early finding, or a partial subset selected
only because it is convenient to fix first.

Before editing, compare the batch with the approved implementation brief. If
the minimum remediation introduces an unplanned product decision, public or
externally consumed contract, persistent model, migration/deployment order,
ownership boundary, or cross-repository surface, stop. Route product changes to
`$pm`; route a new contract, persistent model, migration/deployment order,
ownership, or cross-repository design first to `$dev-planner`; route only a bounded sequencing or slice gap within settled
architecture directly to `$dev-planner`. Do not absorb expansion as ordinary
Review Fix. At attempt `2` or later, also require the caller's passed
convergence checkpoint before accepting another repaired head.

## Merge-Gate Rules

- Resolve every merge conflict when conflicts block merge readiness. Do not hand a PR back to `$dev-merge-handoff` with conflicts remaining.
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

5. Collect the complete repair input.

   - For a Review v2 handoff, verify and retain the accepted combined artifact,
     every confirmed mode-blocking finding, and the repair state before fetching
     any supplemental PR threads.
   - Fetch review comments and inline threads:

   ```bash
   python3 <dev-implementer-skill-root>/scripts/fetch_comments.py > /tmp/pr-comments.json
   jq '.review_threads[] | select(.isResolved | not) | {id,isOutdated,path,line,startLine,comments}' /tmp/pr-comments.json
   ```

   Confirm `/tmp/pr-comments.json` matches the selected PR number. Treat unresolved inline review threads as the target "code comments." Top-level PR conversation comments are context unless the user explicitly asks to handle them too.

6. Evaluate the complete batch and unresolved inline threads.

   - For a Review v2 handoff, plan one bounded repair round covering every
     confirmed mode-blocking implementation finding. Record invalid, already
     resolved, or scope-expanding items rather than silently dropping them.
   - If the user named a specific thread or comment, handle only that target.
   - If `$dev-merge-handoff` routed the PR here for merge-gate repair, handle every unresolved inline thread, applying the selected mode threshold and mandatory gates.
   - Otherwise handle every unresolved inline thread on the selected PR.
   - Read the full thread and identify the latest actionable human or bot review comment.
   - Inspect the referenced file, current code, nearby tests, PR diff, product spec, and technical approach before editing.
   - Apply code fixes only when the comment is technically correct, still relevant to the current diff, and in scope for the PR.
   - Reply with evidence when a comment is invalid, obsolete, already handled, or out of scope.
   - Stop for a product, security, or scope decision if the comment would change approved behavior or cannot be judged from repository evidence.

For stateful repairs, inspect the whole affected sequence and sibling
   abort/rollback paths, including work admitted before the command begins.
   Reuse the planner's owner/state analysis; validate persistent state,
   process-local authority, and restart configuration where affected. Exercise
   the actual component configuration behind the finding, rather than relying
   only on paragraph assertions or a substitute with different lock semantics.

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

   A Review v2 batch may use multiple coherent commits when repository policy
   requires separate generated or migration steps, but return one final repaired
   head. The caller accepts that head once and increments the shared attempt
   count once for the entire batch.

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
   - After a Review v2 repair batch, hand the one repaired head, validation, and
     unchanged repair identity back to `$review` for the next complete
     generation.
   - Otherwise, if conflicts are clear and no mode-blocking or required thread remains unresolved, hand back to `$dev-merge-handoff` with the PR number and a concise summary.
   - If CI checks are red after the fix, route to `$dev-ci-repair`.
   - If conflicts or mode-blocking/required comments remain blocked by a decision, stop with the exact blocker instead of bouncing the PR back.

## Decision Rubric

A comment generally makes sense when it identifies a real bug, user-visible regression, contract mismatch, missing test for changed behavior, unsafe edge case, security risk, performance problem, or maintainability issue directly introduced by the PR.

A comment generally does not make sense when it conflicts with settled product requirements, asks for broader refactoring outside PR scope, relies on an incorrect API or platform assumption, repeats behavior already covered in current code, or only refers to an outdated diff that is no longer present.

When uncertain, inspect the source of truth first: provider docs, API contracts, tests, issue specs, or nearby implementation history. If the answer still depends on a product decision, reply with the blocker and leave the thread unresolved.

## Output

```markdown
## Review Fix Result

### Target PR
- <number, URL, base branch, head branch, and why this PR was selected>

### Review State
- <not applicable, or run ID, generation, attempt count, prior combined artifact, convergence checkpoint, and one repaired head>

### Scope Check
- <within approved brief | replan required | PM decision required, with evidence>

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
<`$review`, `$dev-merge-handoff`, `$dev-ci-repair`, `$dev-planner`, `$pm`, or stop.>
```
