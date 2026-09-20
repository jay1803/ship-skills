---
name: dev-git-setup
description: "Prepare or reconcile an issue branch and isolated worktree for coding-ready Dev work, preserving existing checkouts and verifying integration bases."
metadata:
  owner: jay1803
  family: develop
  maturity: stable
  distribution: develop
---

# Dev: Git Setup

Read the canonical [branch strategy](../dev/references/branch-strategy.md) before resolving bases or merge direction.

## Overview

Prepare Git state before implementation. This skill owns the branch/worktree decision for Dev workflows, keeps unrelated local work untouched, and uses the bundled scripts for fragile Git operations.

Do not create a branch or worktree without a resolved tracker issue ID. `$dev` normally resolves it through its Issue Resolution Gate. If this skill is invoked directly without an ID, search for a relevant issue first; bind a clear match, ask when candidates are equally plausible, or create the initial issue record when none exists. Route a newly created record through `$pm` and `$pm-readiness-review` before Git setup. If tracker tools are unavailable, provide the search or creation draft and stop.

Default to a separate issue worktree. Use current-checkout branch setup only when the user explicitly asks to work in the current checkout, an existing workflow requires it, or a separate worktree is impossible.

## Decision Rules

- Use `worktree` mode by default for new issue work.
- Use `worktree` mode when the current checkout is busy, shared, or likely to be reused.
- Use `branch` mode only when the user explicitly wants the current checkout, the repository does not support worktrees cleanly, or project instructions require in-place branch work.
- Reuse an existing issue branch/worktree when present and clearly tied to the same issue.
- Stop before destructive cleanup. Do not discard, stash, overwrite, reset, or delete user work without explicit approval.
- Default branch type to `feature`. Use `fix` for defects, regressions, CI repair, review-fix-only branches, and bug tickets.

## Workflow

1. Verify the explicit or resolved issue id, then resolve the repo, base branches, and branch type.
   - Allowed types: `feature`, `fix`
   - Branch format: `[type]/[issue_id]`
   - Examples: `feature/AG-1`, `fix/AG-2`
   - Preserve uppercase tracker keys exactly.

2. Inspect current Git state before changing anything.
   - Repo root and current branch.
   - Existing local branches, remote branches, and worktrees for the issue branch.
   - Current worktree status.
   - Resolve upstream integration and issue PR base from the branch strategy contract; inspect parent/controller state for a batch branch.

3. Protect local work.
   - Do not discard local changes.
   - If branch mode is selected, require a clean current worktree before switching branches.
   - Worktree mode preserves the current branch, index, tracked/untracked edits, and occupied base worktrees. It does not require a clean caller checkout; preserve any dirty existing issue worktree when reusing it.

4. Resolve repository bases.
   - Fetch the remote, usually `origin`. In worktree mode, resolve its main and
     integration refs to immutable commits without switching or moving local
     branches. Missing remote bases or fetch failure block; do not silently
     fall back to stale local refs.
   - If a local base contains commits absent from its remote, stop for explicit
     reconciliation so local-only integration history is not silently excluded.
     Behind local bases may remain unchanged.
   - With no configured remote, use and disclose local base commits only.
   - Branch mode retains the clean-checkout fast-forward procedure.

5. Validate the applicable repository ancestry requirement.
   - The following main/develop check applies to the fallback two-branch setup.
     A repository-defined single-base workflow does not require a second branch.
     For batch work, preserve the recorded fork and reconcile upstream drift
     through the controller; never reset a batch branch to current develop.
   - Validate ancestry between the resolved base commits: main must be an
     ancestor of the integration candidate.
   - If `main` is not an ancestor of `develop`, stop without changing either
     branch. Route the repository through `$release` closeout reconciliation or
     another explicitly approved main-to-develop synchronization procedure.
   - Never delete, recreate, reset, or overwrite `develop` merely to satisfy an
     ancestry check; it may contain unreleased integration history.

6. Create or reuse the issue branch from the resolved issue PR base.
   - For batch work, the controller creates/publishes the shared branch before
     child setup. Use its latest verified remote commit, not develop.
   - Create `feature/ISSUE_ID` or `fix/ISSUE_ID`.
   - Do not push automatically unless the user explicitly asks.

7. Finish in the selected mode.
   - Worktree mode: create or reuse a sibling worktree named `<repo-name>-<issue_id>`, unless a path is provided.
   - Branch mode: switch the current checkout to the issue branch.

## Scripted Path

Prefer the bundled scripts for compatible two-base workflows. They do not
select delivery scope or create a batch branch. Pass the resolved issue PR base
via `--develop`; use `--main` for the applicable ancestry anchor. For a
repository-defined single-base workflow, pass that branch to both flags. If the
repository does not require this ancestry invariant, use the manual fallback
with its verified refs and preservation checks, without imposing the helper
ancestry assumption. The examples below illustrate standalone fallback only.

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

The worktree script creates from verified base commits without switching the
caller checkout or updating local bases. The branch script requires a clean
checkout and updates bases by switching branches. Both preserve unrelated work,
log Git operations, and never push automatically.

## Manual Fallback

Use this only when the script needs adjustment for an unusual repo:

Worktree mode (first apply the same missing-base and local-only-history checks
as the scripted path; execute the add only after all checks pass):

```bash
git status --short
git fetch --prune origin
main_ref=$(git rev-parse --verify refs/remotes/origin/main^{commit})
develop_ref=$(git rev-parse --verify refs/remotes/origin/develop^{commit})
git merge-base --is-ancestor "$main_ref" "$develop_ref"
git worktree add -b feature/AG-1 ../Repo-AG-1 "$develop_ref"
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

If `git merge-base --is-ancestor main develop` fails, stop before creating the
issue branch. Reconcile `main` back into `develop` through the release workflow;
do not recreate or reset either protected branch.

## Output

Return a concise setup result:

```markdown
## Git Setup Result

Repo: <repo root>
Mode: <worktree | branch>
Policy / scope: <source or fallback; standalone or batch identifier>
Base: <resolved issue PR base and commit>
Upstream / promotion target: <branch>
Branch: <feature/ISSUE-ID | fix/ISSUE-ID>
Worktree: <path | current checkout>
Status: <ready | blocked>

### Decisions
- <Why this mode was selected.>
- <Whether an existing branch/worktree was reused.>

### Blockers
- <Only concrete blockers, or "None.">
```
