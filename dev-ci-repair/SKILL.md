---
name: dev-ci-repair
description: >-
  Diagnose and repair failing CI after implementation, PR creation, review fixes, or merge-gate repair. Use when local builds, tests, lint, typecheck, migrations, GitHub Actions PR checks, or other CI/CD checks fail and need scoped repair, log inspection, revalidation, or a failure diagnosis. Do not handle review comments or merge conflicts except when a branch update required for CI repair itself produces a narrow conflict to resolve.
---

# Dev: CI Repair

Fix failing checks without changing product scope. Own GitHub Actions PR check inspection directly; do not route to a separate GH CI skill.

Review comments and merge conflicts are owned by `$dev-fix`. Use `$dev-ci-repair` after `$dev-fix` when comments/conflicts are clear but checks are red, or when `$dev-release-handoff` identifies failing checks as the remaining merge blocker.

## Inputs

- Repo path, defaulting to the current repository.
- PR number or URL when available; otherwise resolve the PR from the current branch.
- Failed local command, CI check name, or GitHub Actions run URL when supplied.

## Workflow

1. Resolve the target repo, branch, PR, failed check, and latest commit.
   - Prefer explicit PR input.
   - Otherwise run `gh pr view --json number,url,headRefName,headRefOid,baseRefName` from the current branch.
   - If no PR exists yet, repair the failing local command from `$dev-test` and report that PR checks cannot be inspected.
2. Verify GitHub CLI access when GitHub checks are involved.
   - Run `gh auth status`.
   - If unauthenticated, stop and ask the user to log in.
3. Inspect failing GitHub Actions checks with the bundled script when a PR exists:
   - `python "<dev-ci-repair-skill-dir>/scripts/inspect_pr_checks.py" --repo "." --pr "<number-or-url>"`
   - Add `--json` when machine-readable output helps diagnosis.
   - The script handles `gh pr checks` field drift, extracts run/job IDs, fetches GitHub Actions logs, and returns non-zero while failures remain.
4. Use manual GitHub Actions fallback only when the script cannot run:
   - `gh pr checks <pr> --json name,state,bucket,link,startedAt,completedAt,workflow`
   - If fields are rejected, rerun using the available fields reported by `gh`.
   - For GitHub Actions run URLs, inspect with `gh run view <run_id> --json name,workflowName,conclusion,status,url,event,headBranch,headSha` and `gh run view <run_id> --log`.
   - If run logs are pending but a job id is known, fetch job logs with `gh api "/repos/<owner>/<repo>/actions/jobs/<job_id>/logs"`.
5. Scope non-GitHub checks.
   - If a failed check's details URL is not a GitHub Actions run, mark it external, report the URL, and do not attempt provider-specific repair unless another active skill covers that provider.
6. Diagnose the failure.
   - Classify it as change-caused, pre-existing, flaky, environment-blocked, dependency/service outage, credentials/secrets, external-provider, or unknown.
   - Preserve the smallest useful failure snippet, check URL, run URL, branch, and commit evidence.
7. Repair only valid, change-caused failures.
   - Apply narrow fixes in the issue branch.
   - If updating the PR branch against its base is required to reproduce or repair CI and a merge conflict appears, resolve only the conflict needed for the CI repair using `$dev-fix` conflict rules: understand both sides, avoid blanket `ours`/`theirs`, never discard unrelated work, and stop when a product, security, architecture, or maintainer decision is required.
   - Do not change product scope, broaden architecture, weaken tests, bypass security checks, or hide failing checks.
   - Stop for user/product input if a fix requires secrets, external access, release policy, broad refactor, or product behavior change.
8. Revalidate.
   - Rerun the failing local command or the closest reliable repo command.
   - Commit and push the repair when the branch is PR-backed.
   - Recheck `gh pr checks <pr>` or rerun the bundled script after push when practical.
9. Enforce retry limits.
   - Retry the same failing check at most three times before stopping with a concrete diagnosis and the evidence gathered.

## Bundled Resource

### `scripts/inspect_pr_checks.py`

Fetch failing PR checks, pull GitHub Actions logs, and extract a failure snippet.

Usage:

```bash
python "<dev-ci-repair-skill-dir>/scripts/inspect_pr_checks.py" --repo "." --pr "123"
python "<dev-ci-repair-skill-dir>/scripts/inspect_pr_checks.py" --repo "." --pr "https://github.com/org/repo/pull/123" --json
python "<dev-ci-repair-skill-dir>/scripts/inspect_pr_checks.py" --repo "." --max-lines 200 --context 40
```

## Output

```markdown
## CI Repair Result

PR: <url or "None">
Check: <name/url/command>
Status: <passing | still failing | blocked | external | pre-existing | flaky>

### Diagnosis
- <cause and evidence>

### Failure Evidence
- <small log snippet, run URL, details URL, branch/sha, or "None">

### Fixes Applied
- <file/change or "None">

### Validation
- `<command>`: <result>

### Remaining / Escalation
- <next action, `$dev-fix` for comments/conflicts, `$dev-release-handoff` when checks pass, or "None">
```
