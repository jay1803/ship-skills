# GitHub Review Posting

Read this procedure only after `$review-pr` has frozen an exact GitHub pull
request and prepared its complete set of findings. GitHub review creation sends
notifications, so prefer one batched review and verify live state before any
retry.

## Inspect And Freeze

Use `gh` against the exact repository rather than relying on the current
checkout's remote:

```bash
gh pr view <PR> --repo <OWNER/REPO> \
  --json url,number,state,isDraft,baseRefName,baseRefOid,headRefName,headRefOid
gh pr diff <PR> --repo <OWNER/REPO> --patch
gh api --paginate "repos/<OWNER>/<REPO>/pulls/<PR>/files?per_page=100"
```

The files endpoint supplies the GitHub patch representation used to determine
whether a line is commentable. Keep the captured `headRefOid` as `commit_id`.
Use production line numbers with `side: RIGHT` for added or current head lines;
use `side: LEFT` only when the finding truly targets a deleted base-side line.
For a multi-line comment, add `start_line` and `start_side` and keep the range
inside one diff hunk. Prefer `line` and `side`; do not use the closing-down
`position` parameter for new review logic.

## Build One Review

Create one JSON payload outside the repository with these fields:

```json
{
  "commit_id": "<CAPTURED_HEAD_SHA>",
  "body": "<concise review summary and any cross-file findings>",
  "event": "COMMENT",
  "comments": [
    {
      "path": "path/to/file",
      "line": 42,
      "side": "RIGHT",
      "body": "<evidence-backed structural finding>"
    }
  ]
}
```

An empty `comments` array is valid for a clean or summary-only review. Keep
`event` as `COMMENT` unless the user explicitly authorizes `APPROVE` or
`REQUEST_CHANGES` for this exact PR.

Immediately before submission, rerun the metadata query and compare
`headRefOid` byte-for-byte with `commit_id`. Then submit the complete payload:

```bash
gh api --method POST \
  -H "Accept: application/vnd.github+json" \
  "repos/<OWNER>/<REPO>/pulls/<PR>/reviews" \
  --input <PAYLOAD_JSON>
```

Do not fall back to separate timeline comments when an inline location fails.
First determine whether the line is outside the diff, the head became stale, or
the payload is invalid. Move a still-valid cross-file concern into the single
review body only before a verified successful post; never create a second
review merely to compensate for an uncertain first response.

## Verify

Capture the returned review `id`, `commit_id`, `state`, `user.login`, and
`html_url`, then read it back:

```bash
gh api "repos/<OWNER>/<REPO>/pulls/<PR>/reviews/<REVIEW_ID>"
gh api --paginate \
  "repos/<OWNER>/<REPO>/pulls/<PR>/reviews/<REVIEW_ID>/comments?per_page=100"
```

Confirm every returned comment has `pull_request_review_id == <REVIEW_ID>` and
matches the expected path, line or range, body, commit, and `html_url`. A
successful command without this readback is not verified posting evidence.

If the submit command times out or returns an ambiguous error, list reviews and
review comments first and match the captured head, author, body, and start time.
Retry only when that read proves the intended review was not created.
