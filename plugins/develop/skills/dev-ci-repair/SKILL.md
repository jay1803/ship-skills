---
name: dev-ci-repair
description: "Repair red PR checks or repeated CI/environment failures escalated by dev-test. Initial implementation validation belongs to dev-test."
metadata:
  owner: jay1803
  family: develop
  maturity: stable
  distribution: develop
---

# Dev: CI Repair

Fix failing checks without changing product scope. Own GitHub Actions PR check inspection directly; do not route to a separate GH CI skill.

Review comments and merge conflicts are owned by `$dev-implementer`. Use `$dev-ci-repair` after `$dev-implementer` when comments/conflicts are clear but checks are red, or when `$dev-merge-handoff` identifies failing checks as the remaining merge blocker.

## Boundary

- Own red PR/CI checks and explicit `$dev-test` escalations for repeated CI or environment behavior.
- Do not own the first local build, test, lint, typecheck, migration, or acceptance failure after implementation. `$dev-test` classifies it and routes change-caused failures to `$dev-implementer`.
- Before a PR exists, require an evidence-bearing `$dev-test` handoff naming the repeated command, environment, attempts, and why the failure is CI/environment-shaped.
- Route review comments and merge conflicts to `$dev-implementer`; route product behavior or scope decisions back through `$dev`.

When the PR has a Review history, repair only the CI batch the controller
authorized for the exact PR and head: the complete in-scope failing-check set,
never a convenient subset. The controller owns the Review ledger, triage and
round budget; do not recount, reset or extend them here. A missing or
mismatched authorization, or out-of-scope or mixed remediation, returns to the
controller without repair. Ordinary failing-CI work without a Review history
keeps its own authorization and needs no Review state. Required failing CI
stays blocking even when ticketed separately.

## Inputs

- Repo path, defaulting to the current repository.
- PR number or URL when available; otherwise resolve the PR from the current branch.
- Failed local command, CI check name, or GitHub Actions run URL when supplied.

## Workflow

1. Resolve the target repo, branch, PR, failed check, and latest commit.
   - Prefer explicit PR input.
   - Otherwise run `gh pr view --json number,url,headRefName,headRefOid,baseRefName` from the current branch.
   - If no PR exists yet, proceed only from an explicit `$dev-test` escalation, repair the handed-off command or environment failure, and report that PR checks cannot be inspected.
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
   - Classify it under the shared [failure attribution](../dev-test/references/validation-evidence.md#failure-attribution).
   - Preserve the smallest useful failure snippet, check URL, run URL, branch, and commit evidence.
7. Repair only valid, change-caused failures.
   - Apply narrow fixes in the issue branch.
   - If updating the PR branch against its base is required to reproduce or repair CI and a merge conflict appears, resolve only the conflict needed for the CI repair using `$dev-implementer`'s [PR-repair conflict rules](../dev-implementer/references/pr-repair.md): understand both sides, avoid blanket `ours`/`theirs`, never discard unrelated work, and stop when a product, security, architecture, or maintainer decision is required.
   - Do not change product scope, broaden architecture, weaken tests, bypass security checks, or hide failing checks.
   - Stop for user/product input if a fix requires secrets, external access, release policy, broad refactor, or product behavior change.
8. Revalidate.
   - Rerun the failing local command or the closest reliable repo command.
   - Commit and push the repair when the branch is PR-backed.
   - Recheck `gh pr checks <pr>` or rerun the bundled script after push when practical.
   - Return one final repaired head and validation to the caller. After a
     Review batch the controller selects any re-review; ordinary CI repair does
     not start or select Review.
9. Enforce retry limits.
   - Retry the same failing check at most three times before stopping with a concrete diagnosis and the evidence gathered.
   - This diagnostic limit is separate from the controller's Review budget and
     never resets it.

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

### Review Batch
- <not applicable, or the authorized batch and head, and the one repaired head>

### Scope Check
- <within approved brief | replan required | requester decision required, with evidence>

### Failure Evidence
- <small log snippet, run URL, details URL, branch/sha, or "None">

### Fixes Applied
- <file/change or "None">

### Validation
- `<command>`: <result>

### Remaining / Escalation
- <next action: return to the controller for re-review after a Review batch; otherwise
  `$dev-implementer` for comments/conflicts, `$dev-merge-handoff` when checks pass, or "None">
```
