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
   - Verify branch, base branch, committed changes, issue ID, validation results,
     and one exact current verification state: **selected and pass** from
     `$dev-verifier` against the current head, or **unselected with
     receipt-backed current evidence** from the Resume Receipt.
   - The unselected state must name the matching route/head, selected phase plan,
     validation floor, and current validation/verification evidence. Missing,
     stale, blocked, or failed verifier evidence is never equivalent to
     unselected.
   - Run `git status --short --branch`, `git diff --stat`, and a commit range such as `git log <base>..HEAD --oneline`.
   - Stop if required changes are uncommitted, validation is missing, the
     selected verifier is failed/blocked/stale, or the unselected state lacks
     receipt-backed current evidence, unless the caller explicitly allows a
     blocked draft PR.
   - **Direct-PR exception:** when the caller explicitly requests that the PR be
     created now, a committed head and resolved base are still required, but a
     missing, blocked, or stale selected `$dev-verifier` result may produce a
     **draft** PR. Capture every available validation result and the exact
     missing or blocked evidence in the PR body. Do not describe that evidence
     as passed.
     This exception does not permit uncommitted changes, ready-for-review
     status, auto-merge, merge, or a production-promotion PR. A known failing
     validation remains a blocker unless the caller explicitly authorizes a
     draft that discloses the failure.
2. Resolve PR direction.
   - Verify the caller's recorded strategy against repository policy; otherwise resolve the canonical branch-strategy fallback.
   - Use the recorded issue PR base, including a temporary batch branch, rather than independently defaulting to develop.
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
   - Preserve `Verification Basis: selected and pass` with the verified head, or
     `Verification Basis: unselected with receipt-backed current evidence` with
     the matching receipt route/head and validation evidence. Missing, stale,
     blocked, or failed evidence cannot be relabeled as unselected.
   - Under the Direct-PR exception, include `## Verification Exception` after
     test evidence. Record the caller's direct-draft request, exact missing,
     blocked, or stale verifier evidence, and draft-only status. Do not claim
     completion or ready-for-review status from this exception.
6. Push the branch if needed.
   - If no upstream exists, run `git push -u origin HEAD`.
   - Otherwise push only when local commits are not on the remote branch.
7. Open the PR with `gh`.
   - A normal standard PR with either current verification state
     (**selected and pass** or **unselected with receipt-backed current
     evidence**) opens ready for review; omit `--draft`.
   - Use `gh pr create --base "<base>" --head "<head>" --title "<title>" --body-file "<body-file>"`.
   - Use `--draft` only for the Direct-PR exception or when the user explicitly
     requests a draft PR; retain the required disclosure in either case.
8. Capture metadata.
   - Run `gh pr view --json number,url,title,headRefName,baseRefName,headRefOid`.
   - Record PR number, URL, title, head branch, base branch, and latest commit.

## PR Body Shape

Use repository structure first. Without a required template, a short description
plus linked issue, test evidence, and Verification Basis can be sufficient. Add
only the explanation needed to assess behavior, compatibility, risk, or a concrete
remaining boundary. The conditional Verification Exception disclosure remains
required for the Direct-PR draft path.

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
