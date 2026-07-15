---
name: dev-pr-writer
description: >-
  Create a GitHub pull request after implementation, tests, and self-review are complete. Use to inspect branch state, prepare a repository-conformant PR title and body, link issues, include implementation notes, test evidence, risks, screenshots when needed, push the branch, open or reuse the PR with gh, and capture PR metadata.
---

# Dev: PR Writer

Open the PR with enough context for reviewers and downstream gates. Own GitHub PR creation directly.

## Workflow

1. Confirm readiness.
   - Verify branch, base branch, committed changes, issue ID, validation results, and self-review approval.
   - Run `git status --short --branch`, `git diff --stat`, and a commit range such as `git log <base>..HEAD --oneline`.
   - Stop if required changes are uncommitted, validation is missing, or self-review is not approved unless the caller explicitly allows a blocked PR.
2. Resolve PR direction.
   - Use the caller's base branch when provided.
   - Default to `develop` for Dev/build workflows unless the repository clearly uses another integration branch.
   - Use the current branch as the head unless the caller provided a head branch.
3. Avoid duplicate PRs.
   - Run `gh pr list --state open --base "<base>" --head "<head>" --json number,title,url`.
   - If an open PR already exists for the same head and base, reuse it and capture its metadata instead of creating a duplicate.
4. Write the PR title.
   - Prefer the repository's documented PR title convention, such as `.github/pull_request_title_conventions.md`, existing PR history, or CI title validation.
   - If no convention is known, use a concise imperative title that describes the user-facing or technical outcome.
   - For conventional-title repositories, use `<type>(<scope>): <Summary>` with type `feat`, `fix`, `perf`, `test`, `docs`, `refactor`, `build`, `ci`, `chore`, or `revert`.
   - Keep summaries imperative, capitalized, without ticket IDs, and without a trailing period. Use `!` before `:` for breaking changes when required.
5. Write the PR body.
   - Start from `.github/pull_request_template.md` when present and fill it honestly instead of leaving placeholder text.
   - Always include summary, linked Linear/GitHub issue, implementation notes, test evidence with exact commands/results, risk or rollback notes, screenshots/videos for UI changes, and follow-ups.
   - Keep the body concise but sufficient for `$dev-code-review`, `$dev-ci-repair`, `$pm-pr-product-review`, and merge handoff.
6. Push the branch if needed.
   - If no upstream exists, run `git push -u origin HEAD`.
   - Otherwise push only when local commits are not on the remote branch.
7. Open the PR with `gh`.
   - Default to a draft PR unless the caller or repository convention requires ready-for-review.
   - Use `gh pr create --base "<base>" --head "<head>" --title "<title>" --body-file "<body-file>" --draft`.
   - If ready-for-review is required, omit `--draft`.
8. Capture metadata.
   - Run `gh pr view --json number,url,title,headRefName,baseRefName,headRefOid`.
   - Record PR number, URL, title, head branch, base branch, and latest commit.

## PR Body Shape

```markdown
## Summary
- <what changed and why>

## Linked Issue
- <Linear/GitHub issue URL or ID>

## Implementation Notes
- <important code path, migration, API, UI, or compatibility note>

## Test Evidence
- `<command>`: <pass | fail | blocked> - <short evidence>

## Risks / Rollback
- <risk, rollback note, or "None">

## Screenshots / Video
- <link/path or "Not applicable">

## Follow-Ups
- <follow-up issue or "None">
```

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
Usually `$dev-code-review`.
```
