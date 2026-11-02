---
name: dev-pr-writer
description: "Prepare, push, and open or reuse a GitHub PR from implemented work with validation evidence; supports explicitly requested drafts."
metadata:
  owner: jay1803
  family: develop
  maturity: stable
  distribution: develop
---

# Dev: PR Writer

Open the PR with enough context for reviewers and downstream gates. Own GitHub PR creation directly.

Read the canonical [branch strategy](../dev/references/branch-strategy.md) before resolving bases or merge direction.

## Workflow

1. Confirm readiness.
   - Verify branch, base branch, committed changes, any linked issue ID, and the
     validation results the caller supplies or the repository requires. Run
     `git status --short --branch`, `git diff --stat`, and a commit range such
     as `git log <base>..HEAD --oneline`.
   - Stop if required changes are uncommitted or required validation is
     missing or failing, unless the caller explicitly allows a draft that
     discloses it.
   - **Dev phase plan:** only when a Dev caller supplies one, also require one
     current verification state for this head: `$dev-verifier` selected and
     passed, or verifier unselected in the plan with current validation
     evidence. A missing, stale, blocked or failed selected verifier is not
     "unselected": stop, or, when the caller explicitly asks for the PR now,
     open a **draft** whose `## Verification Exception` section records the
     request and the exact missing evidence without calling it passed. That
     draft never permits uncommitted changes, ready-for-review status,
     auto-merge, merge or a production-promotion PR.
2. Resolve PR direction.
   - Verify the caller's recorded strategy against repository policy; otherwise resolve the canonical branch-strategy fallback.
   - Use the recorded issue PR base, including a temporary batch branch, rather than independently defaulting to develop.
   - For a selected native stack, use the immediate predecessor base and apply
     the [stack contract](../dev/references/stacked-prs.md). Record trunk,
     layer dependency and exact revisions in the PR; do not retarget it to the
     batch trunk merely to fit the ordinary child shape.
   - Ordinary issue PRs must target the resolved issue PR base. If the
     requested PR matches the repository's production-promotion shape, route it
     to `$release`; do not create it as an issue-level Dev PR.
   - Use the current branch as the head unless the caller provided a head branch.
3. Avoid duplicate PRs.
   - Run `gh pr list --state open --base "<base>" --head "<head>" --json number,title,url`.
   - If an open PR already exists for the same head and base, reuse it and capture its metadata instead of creating a duplicate.
4. Write the PR title.
   - Follow verified repository conventions, including required issue IDs,
     capitalization, conventional prefixes, and breaking-change notation.
   - Otherwise use a concise title that states the resulting behavior. Do not
     impose a ticket-ID exclusion or a universal capitalization rule.
5. Write the PR body.
   - Follow the repository template when present. Explain the problem and
     resulting behavior, link the confirmed issue, and report relevant validation
     with exact commands/results and any concrete missing evidence.
   - Scale implementation detail to what reviewers need. Include risk/rollback,
     screenshots, migration notes, or follow-ups when applicable or required by
     repository policy; do not invent empty sections for a bounded change.
6. Push the branch if needed.
   - If no upstream exists, run `git push -u origin HEAD`.
   - Otherwise push only when local commits are not on the remote branch.
7. Open the PR with `gh`.
   - For a native stack, use the supported stack submission/UI/API surface and
     verify actual membership/order after creation. Inspect installed help;
     an ordinary PR against a predecessor branch is not proof of native stack
     registration. Reuse the existing PR rather than creating a duplicate.
   - Use `gh pr create --base "<base>" --head "<head>" --title "<title>" --body-file "<body-file>"`.
   - Open ready for review once step 1 passes; add `--draft` only for a draft
     allowed there or explicitly requested, keeping its disclosure.
8. Capture metadata.
   - Run `gh pr view --json number,url,title,headRefName,baseRefName,headRefOid`.
   - Record PR number, URL, title, head branch, base branch, and latest commit.

## Output

```markdown
## Pull Request

PR: <url or blocked>
Title: <title>
Base: <base branch>
Head: <head branch>
Commit: <sha>

### Summary
- <what changed>

### Test Evidence
- <commands/results>

### Risks / Notes
- <risk, rollback note, screenshot need, or "None">

### Recommended Next Step
Usually `$review`.
```
