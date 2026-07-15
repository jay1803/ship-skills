---
name: dev-git-setup
description: "Use when Dev needs to prepare Git state for a coding-ready issue: inspect repo/worktrees, update main and develop, verify develop contains main, create or reuse a feature/ISSUE_ID or fix/ISSUE_ID branch, and choose a separate worktree by default or current-checkout branch setup when explicitly required."
---

# Dev: Git Setup

## Overview

Prepare Git state before `$dev-repo-context` and implementation. This skill owns the branch/worktree decision for Dev workflows, keeps unrelated local work untouched, and uses the bundled scripts for fragile Git operations.

Default to a separate issue worktree. Use current-checkout branch setup only when the user explicitly asks to work in the current checkout, an existing workflow requires it, or a separate worktree is impossible.

## Decision Rules

- Use `worktree` mode by default for new issue work.
- Use `worktree` mode when the current checkout is busy, shared, or likely to be reused.
- Use `branch` mode only when the user explicitly wants the current checkout, the repository does not support worktrees cleanly, or project instructions require in-place branch work.
- Reuse an existing issue branch/worktree when present and clearly tied to the same issue.
- Stop before destructive cleanup. Do not discard, stash, overwrite, reset, or delete user work without explicit approval.
- Default branch type to `feature`. Use `fix` for defects, regressions, CI repair, review-fix-only branches, and bug tickets.

## Workflow

1. Resolve the repo, base branches, branch type, and issue id.
   - Allowed types: `feature`, `fix`
   - Branch format: `[type]/[issue_id]`
   - Examples: `feature/AG-1`, `fix/AG-2`
   - Preserve uppercase tracker keys exactly.

2. Inspect current Git state before changing anything.
   - Repo root and current branch.
   - Existing local branches, remote branches, and worktrees for the issue branch.
   - Current worktree status.
   - Default base branches: `main` and `develop`, unless repo instructions clearly say otherwise.

3. Protect local work.
   - Do not discard local changes.
   - If branch mode is selected, require a clean current worktree before switching branches.
   - If worktree mode is selected but the setup script cannot safely update bases because the current checkout is dirty or occupied, reuse an existing clean issue worktree/control checkout when available; otherwise stop with a concrete blocker instead of forcing cleanup.

4. Update repository bases.
   - Fetch the remote, usually `origin`.
   - Fast-forward `main` from the remote when possible.
   - Fast-forward `develop` from the remote when possible.

5. Validate `develop` against `main`.
   - `develop` is valid when `main` is an ancestor of `develop`.
   - If `develop` is behind `main`, delete/recreate local `develop` from `main`.
   - If local `develop` has commits not in `main`, preserve a timestamped backup branch before replacing it.

6. Create or reuse the issue branch from `develop`.
   - Create `feature/ISSUE_ID` or `fix/ISSUE_ID`.
   - Do not push automatically unless the user explicitly asks.

7. Finish in the selected mode.
   - Worktree mode: create or reuse a sibling worktree named `<repo-name>-<issue_id>`, unless a path is provided.
   - Branch mode: switch the current checkout to the issue branch.

## Scripted Path

Prefer the bundled scripts for normal use.

Worktree mode:

```bash
scripts/setup_git_issue_worktree.sh feature AG-1
scripts/setup_git_issue_worktree.sh fix AG-2
scripts/setup_git_issue_worktree.sh feature/AG-1
```

Useful options:

```bash
scripts/setup_git_issue_worktree.sh --remote upstream feature AG-1
scripts/setup_git_issue_worktree.sh --main trunk --develop develop feature AG-1
scripts/setup_git_issue_worktree.sh --path ../AngleApp-AG-1 feature AG-1
scripts/setup_git_issue_worktree.sh --reuse-existing feature AG-1
```

Branch mode:

```bash
scripts/setup_git_issue_branch.sh feature AG-1
scripts/setup_git_issue_branch.sh fix AG-2
scripts/setup_git_issue_branch.sh feature/AG-1
```

Useful options:

```bash
scripts/setup_git_issue_branch.sh --remote upstream feature AG-1
scripts/setup_git_issue_branch.sh --main trunk --develop develop feature AG-1
scripts/setup_git_issue_branch.sh --reuse-existing feature AG-1
```

Both scripts require a clean current worktree because they update `main` and `develop` by switching branches. They log each Git command, stop on non-fast-forward base updates instead of merging, and never push automatically.

## Manual Fallback

Use this only when the script needs adjustment for an unusual repo:

Worktree mode:

```bash
git status --short
git fetch --prune origin
git switch main
git merge --ff-only origin/main
git switch develop
git merge --ff-only origin/develop
git merge-base --is-ancestor main develop
git worktree add -b feature/AG-1 ../Repo-AG-1 develop
```

Branch mode:

```bash
git status --short
git fetch --prune origin
git switch main
git merge --ff-only origin/main
git switch develop
git merge --ff-only origin/develop
git merge-base --is-ancestor main develop
git switch -c feature/AG-1 develop
```

If `git merge-base --is-ancestor main develop` fails, recreate `develop` from `main` before creating the issue branch. Back up `develop` first when it has commits not reachable from `main`.

## Output

Return a concise setup result:

```markdown
## Git Setup Result

Repo: <repo root>
Mode: <worktree | branch>
Base: <develop or repo-specific base>
Branch: <feature/ISSUE-ID | fix/ISSUE-ID>
Worktree: <path | current checkout>
Status: <ready | blocked>

### Decisions
- <Why this mode was selected.>
- <Whether an existing branch/worktree was reused.>

### Blockers
- <Only concrete blockers, or "None.">
```
