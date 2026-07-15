---
name: dev-code-review
description: >-
  Run technical review after a pull request opens. Use to resolve the exact target PR, route to a project-configured external review adapter when explicitly configured, optionally spawn an independent no-context Codex reviewer, review correctness, maintainability, architecture, performance, security, error handling, tests, and style before review-fix or CI repair loops, and verify that review comments or a no-blocking-issues summary actually posted. Also use for legacy Claude PR Review, @code-review, or claude -p review requests.
---

# Dev: Code Review

Review the PR technically. This is not PR Product Review and should not rewrite requirements.

Prefer `$dev-external-review` when the caller or repository provides an exact external review integration; otherwise use an independent no-context Codex reviewer for normal Dev PRs.

The main agent must not perform a duplicate local review after delegating to a no-context or external reviewer. It owns target resolution, reviewer selection, prompt quality, GitHub verification, and returning control to the Dev workflow.

## Inputs

- Require a GitHub PR URL, PR number, or a git repository where the current branch has a PR that can be resolved with `gh pr view`.
- Use the exact PR captured by the calling Dev workflow. Do not switch to the newest PR or another branch's PR.
- Use the provided repository path when present; otherwise use the current working directory.

## Workflow

1. Resolve the repo and target PR.
   - `cd` to the repository path when one is provided.
   - Confirm the directory is a git repository.
   - Prefer an explicitly provided PR URL or PR number.
   - If no PR is provided, resolve only the current branch's PR:

     ```bash
     gh pr view --json url,number,headRefName,baseRefName
     ```

   - Capture PR URL, PR number, head branch, base branch, and review start time.
   - Stop with a clear blocker if the PR cannot be resolved confidently.

2. Read review context for orchestration only.
   - Read the PR metadata, diff scope, commits, test evidence, product spec, technical approach, and self-review notes enough to build a correct reviewer prompt.
   - Do not pass the Linear issue, implementation brief, acceptance criteria, suspected risks, prior analysis, or parent thread history to a no-context reviewer.

3. Choose the reviewer mode.
   - Use `$dev-external-review` first when the caller explicitly requests an external provider, the repo documents a project-specific review API/command, or the Dev workflow passes a configured external review requirement.
   - If external review is required but `$dev-external-review` returns `not configured`, stop with `blocked - external review not configured`.
   - If external review is optional and not configured, continue to the no-context Codex reviewer path.
   - Do not invent external APIs, Claude commands, webhooks, tokens, or project conventions inside this skill.

4. Run `$dev-external-review` when selected.
   - Pass repo path, PR URL/number, head branch, base branch, review start time, and any explicit provider/config source.
   - Let `$dev-external-review` invoke the configured project-specific command/API and return evidence.
   - Wait for `$dev-external-review` to finish its configured polling window. Do not treat request acceptance or a "review started" comment as completion.
   - If it returns `pending`, report the provider evidence and stop with the next poll/retry point.
   - If it returns findings or verified clean status, verify the GitHub/provider evidence before claiming review completion.
   - If it returns actionable comments, route to `$dev-fix`; after fixes land, `$dev-release-handoff` owns the final comment/check sweep before merge.

5. Spawn a no-context reviewer when available and no external review path is selected.
   - Use the available multi-agent spawn tool with `fork_context: false`.
   - Pass only the repository path, PR URL, and the review task.
   - Use the default model and agent type unless the user explicitly asks for a different reviewer model.
   - Do not invoke Claude Code, `@code-review`, `claude -p`, or any Claude plugin.

Use this prompt shape for the no-context reviewer:

```text
Review this GitHub pull request from a clean Codex context: <PR_URL>

Repository path: <REPO_PATH>

Goal: produce a high-signal code review, not a general summary.

Review the PR diff and the surrounding code. Focus only on serious issues: correctness bugs, security vulnerabilities, data loss, auth/permission mistakes, broken edge cases, migration risk, concurrency bugs, API compatibility problems, and missing tests for changed behavior.

Do not modify files. Do not push commits. Do not create branches. Do not open a new PR. Do not invoke Claude Code, @code-review, claude -p, or any Claude plugin.

Use only repository state, GitHub PR metadata/diff, and surrounding code. Leave GitHub review comments only when the issue is concrete, reproducible, and tied to changed lines. Ignore pure style comments unless they hide a real correctness or maintainability risk.

If there are no serious findings, post a short GitHub PR summary saying no blocking issues were found.

In your final response, report whether review comments were posted, no blocking issues were found, or review was blocked, including the blocker if blocked.
```

6. Wait for the reviewer result.
   - Wait because the next Dev step depends on whether review comments exist.
   - If the reviewer asks for more context, provide only the PR URL, repo path, or access-error details. Do not provide parent-thread implementation context.
   - If the reviewer cannot access GitHub, cannot inspect the PR, cannot post the required GitHub result, or attempts to invoke Claude tooling, report the review as blocked. Do not substitute an unverified local review as if the independent review completed.

7. Verify the GitHub outcome.
   - If the reviewer says it posted review comments or a no-blocking-issues summary, verify with GitHub before claiming success. Use `gh pr view <PR_URL> --comments` or `gh api` review/comment endpoints as available.
   - Treat the review as verified only when review comments, a PR review, or a PR comment from the reviewer appears after the captured review start time, or when the reviewer returns direct tool evidence that GitHub accepted the posted review.
   - If the reviewer says there are no serious findings, treat the review as complete only when the short no-blocking-issues GitHub summary was posted and verified.
   - If review posting cannot be verified, report `blocked - review not verified`.

8. If no no-context reviewer is available, run a local technical review and say so.
   - Read the PR diff, commits, test evidence, product spec, technical approach, and self-review notes.
   - Prioritize bugs, correctness, maintainability, architecture fit, error handling, performance, security/privacy, and test quality.
   - Post GitHub review comments only when the issue is concrete, reproducible, and tied to changed lines.
   - If local review is used because no sub-agent tooling exists, report that the independent no-context path was unavailable.

9. Separate actionable comments from optional nits.
   - Actionable findings route to `$dev-fix`.
   - Failing checks route to `$dev-ci-repair`.
   - A verified clean review routes to `$dev-release-handoff` or PR Product Review depending on the caller's phase.

## Output

```markdown
## Code Review

PR: <url>
Reviewer Mode: <external adapter | no-context sub-agent | local fallback>
Decision: <approved | comments | pending | blocked | blocked - review not verified>
Verification: <GitHub comment/review verified | direct tool evidence | not verified>

### Findings
- [<severity>] <file/evidence, issue, and requested fix>

### Non-Blocking Notes
- <nit or optional improvement, or "None">

### Blocker
- <blocker, or "None">

### Recommended Next Step
<`$dev-fix` if findings exist; `$dev-ci-repair` if checks are failing; `$dev-release-handoff` if clean.>
```
