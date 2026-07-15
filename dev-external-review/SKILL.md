---
name: dev-external-review
description: >-
  Use when an opened GitHub PR needs a project-configured external technical reviewer, review API, webhook, bot, or command, including Claude Code only when the repo or caller provides an exact integration. Use project-local .agents review config and local env files when present. After the provider accepts the request, leave a PR comment proving the external review started. Do not use when no project-specific review integration is configured.
---

# Dev: External Review

Invoke a project-specific external PR review provider, post a PR comment when the request is accepted, wait for review completion, and return verified evidence to the calling workflow. This skill is an adapter, not a reviewer: it does not invent review commands, perform a duplicate local review, or decide product scope.

## Boundary

- Own discovering and invoking an explicit external review recipe for the exact target PR.
- Accept project-specific APIs, webhooks, bots, CLIs, or Claude Code review services only when the command/API contract is documented or supplied by the caller.
- Do not guess endpoint URLs, request payloads, environment variable names, tokens, reviewer identities, or polling behavior.
- Treat `.agents/dev-external-review.local.env` as the default project-local secret file when it exists. It is per worktree and must stay uncommitted.
- Do not pass PM context, implementation history, suspected risks, or acceptance criteria unless the configured external provider explicitly requires them. Prefer PR URL, repo path, head/base branch, and a concise technical-review prompt.
- After the configured provider accepts the request, post a concise PR comment saying the external review started. This comment is required start evidence for `$dev`.
- Do not treat "request accepted" or "review started" as review completion. Completion requires a verified finished signal plus findings or a clean-review result.

## Configuration Discovery

Use the first explicit source that applies:

1. Caller-provided external review instructions.
2. Repo documentation such as `.codex/dev-external-review.md`, `.agents/dev-external-review.md`, `.github/dev-external-review.md`, `AGENTS.md`, or `CLAUDE.md`.
3. Repo scripts or package tasks only when their name and docs clearly indicate PR review, for example `external-review`, `review-pr`, `claude-review`, or `code-review-bot`.

Search narrowly when no path is provided:

```bash
rg -n "dev-external-review|external review|review API|review webhook|claude.*review|code-review bot|review-pr" .
```

If no explicit integration is found, return `not configured`. Do not fall back to generic Claude, generic curl, `$dev-code-review`, or a local review.

## Environment Loading

- Before invoking a configured provider, load `.agents/dev-external-review.local.env` when it exists or when the recipe points to it.
- Do not print the file contents or echo expanded secrets.
- Preserve already-exported environment variables when possible. A shell-level `TOKEN` is valid for worktrees that do not have a local env file.
- If the recipe requires variables that are still missing after env loading, stop with a blocked result that names only the missing variable names.

## Workflow

1. Confirm inputs.
   - Require repo path, PR URL or PR number, head branch, base branch, and review start time from `$dev` or the calling workflow.
   - Verify the repo is a git repository and the PR matches the provided head/base when possible.
   - Stop if the target PR is ambiguous.

2. Load the external review recipe.
   - Identify provider name, exact command or API call, required environment variables, expected side effects, completion signal, and verification method.
   - Load project-local env from `.agents/dev-external-review.local.env` when present or documented by the recipe.
   - Confirm required environment variables exist without printing their values.
   - Redact tokens, auth headers, cookies, signed URLs, and private webhook payloads from all output.

3. Build the review request.
   - Substitute only documented placeholders such as `<PR_URL>`, `<PR_NUMBER>`, `<REPO_PATH>`, `<HEAD_BRANCH>`, `<BASE_BRANCH>`, and `<REVIEW_START_ISO>`.
   - Use a high-signal technical-review prompt focused on correctness, security, data loss, auth/permissions, edge cases, migrations, concurrency, API compatibility, and missing tests.
   - Include "do not modify files, push commits, create branches, or open a new PR" unless the provider contract already guarantees read-only review behavior.

4. Invoke the configured provider.
   - Run only the documented command/API call.
   - Capture provider response ID, job URL, review URL, GitHub comment/review URL, or other durable evidence.
   - Treat a successful API response as request acceptance only.
   - After request acceptance, post a PR comment that the external review started. The comment must include the provider name, review start time, and non-sensitive durable evidence such as a job URL or response ID when available.
   - Keep the comment concise and do not include tokens, private payloads, prompt text that contains sensitive data, or secret-derived URLs.
   - Use this comment shape unless the repo recipe requires different wording:
     ```markdown
     External review started.

     Provider: <provider>
     Started: <REVIEW_START_ISO>
     Request: <non-sensitive job URL or response ID, if available>
     ```
   - Capture and return the PR comment URL. If the PR comment cannot be posted after request acceptance, report `blocked - external review start comment not posted`.

5. Wait for review completion.
   - Default wait window: poll every 60 seconds for up to 10 minutes unless the recipe or caller sets a different window.
   - Prefer provider-documented status endpoints or commands when available.
   - When the provider posts to GitHub, poll PR comments/reviews after `<REVIEW_START_ISO>`.
   - Expect at least two lifecycle signals when the provider supports them: this skill's "review started" PR comment and a later "review finished"/"review complete" comment, review, or provider artifact.
   - Do not return success after only the start signal. If only the start comment exists at timeout, report `pending` with the start-comment evidence and the next suggested poll time.
   - If no start or finish evidence appears in the wait window, report `blocked - external review not verified`.

6. Inspect the finished review outcome.
   - Prefer GitHub evidence after the captured review start time: PR review, review comments, inline review threads, or PR comment from the configured reviewer/bot.
   - After the finish signal appears, fetch review comments/threads for the target PR and classify actionable findings versus clean/no-blocking summary.
   - If the provider returns findings directly instead of posting to GitHub, record the provider artifact and whether it is final.
   - If the provider reports no findings, require either a verified GitHub no-blocking summary or a final provider result that explicitly says no blocking issues were found.
   - If finish evidence exists but comments cannot be inspected, report `blocked - external review comments not inspected`.

7. Return control to the calling workflow.
   - Actionable findings route through `$dev` to `$dev-fix`.
   - Failing checks still route to `$dev-ci-repair`.
   - A verified clean external review routes back to the normal Dev flow.

## Output

```markdown
## External Review

PR:
Provider:
Mode: <api | webhook | bot | cli | other>
Configuration Source:
Status: <verified findings | verified clean | pending | not configured | blocked>
Verification: <start comment | finish comment/review | GitHub review threads | provider artifact | request accepted only | not verified>
Start Comment: <GitHub PR comment URL, or none>

### Evidence
- <comment/review URL, provider job ID, response ID, or redacted command summary>

### Lifecycle
- Started: <verified | missing | not supported>
- Finished: <verified | pending | missing>

### Findings
- [<severity>] <file/evidence, issue, and requested fix>

### Blocker
- <blocker, or "None">

### Recommended Next Step
<`$dev-fix`, `$dev-ci-repair`, continue `$dev`, or blocked reason.>
```
