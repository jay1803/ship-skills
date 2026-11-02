#!/usr/bin/env python3
"""
Fetch all PR conversation comments + reviews + review threads (inline threads)
for one PR by shelling out to:

  gh api graphql

The PR is the optional argument (number or URL), otherwise the PR associated
with the current git branch. Owner/repo come from the PR URL, which names the
base repository, so fork PRs are queried where their threads live. Each
connection, and each thread's comments, is paginated independently.

Requires:
  - `gh auth login` already set up

Usage:
  python fetch_comments.py [PR] > pr_comments.json
"""

from __future__ import annotations

import json
import re
import subprocess
import sys
from typing import Any

COMMENT_FIELDS = "id body createdAt updatedAt author { login }"

CONNECTIONS = {
    # Top-level "Conversation" comments (issue comments on the PR)
    "comments": COMMENT_FIELDS,
    # Review submissions (Approve / Request changes / Comment), with body if present
    "reviews": "id state body submittedAt author { login }",
    # Inline review threads (grouped), includes resolved state
    "reviewThreads": f"""
          id isResolved isOutdated path line diffSide startLine startDiffSide
          originalLine originalStartLine resolvedBy {{ login }}
          comments(first: 100) {{
            pageInfo {{ hasNextPage endCursor }}
            nodes {{ {COMMENT_FIELDS} }}
          }}""",
}

PR_QUERY = """\
query($owner: String!, $repo: String!, $number: Int!, $cursor: String) {
  repository(owner: $owner, name: $repo) {
    pullRequest(number: $number) {
      number url title state
      %s(first: 100, after: $cursor) {
        pageInfo { hasNextPage endCursor }
        nodes { %s }
      }
    }
  }
}
"""

THREAD_COMMENTS_QUERY = """\
query($id: ID!, $cursor: String) {
  node(id: $id) {
    ... on PullRequestReviewThread {
      comments(first: 100, after: $cursor) {
        pageInfo { hasNextPage endCursor }
        nodes { %s }
      }
    }
  }
}
""" % COMMENT_FIELDS

PR_URL = re.compile(r"^https?://[^/]+/(?P<owner>[^/]+)/(?P<repo>[^/]+)/pull/(?P<number>\d+)")


def _run(cmd: list[str], stdin: str | None = None) -> str:
    p = subprocess.run(cmd, input=stdin, capture_output=True, text=True)
    if p.returncode != 0:
        raise RuntimeError(f"Command failed: {' '.join(cmd)}\n{p.stderr}")
    return p.stdout


def _run_json(cmd: list[str], stdin: str | None = None) -> dict[str, Any]:
    out = _run(cmd, stdin=stdin)
    try:
        return json.loads(out)
    except json.JSONDecodeError as e:
        raise RuntimeError(f"Failed to parse JSON from command output: {e}\nRaw:\n{out}") from e


def _ensure_gh_authenticated() -> None:
    try:
        _run(["gh", "auth", "status"])
    except RuntimeError:
        print("run `gh auth login` to authenticate the GitHub CLI", file=sys.stderr)
        raise RuntimeError("gh auth status failed; run `gh auth login` to authenticate the GitHub CLI") from None


def get_pr_ref(pr: str | None = None) -> tuple[str, str, int]:
    """Resolve owner/repo/number of the PR's base repository from its URL."""
    cmd = ["gh", "pr", "view", *([pr] if pr else []), "--json", "number,url"]
    view = _run_json(cmd)
    match = PR_URL.match(view["url"])
    if not match:
        raise RuntimeError(f"Cannot parse owner/repo from PR URL: {view['url']}")
    return match["owner"], match["repo"], int(view["number"])


def gh_api_graphql(query: str, **variables: str | int | None) -> dict[str, Any]:
    """
    Call `gh api graphql` using -F variables, omitting unset ones.
    Query is passed via stdin using query=@- to avoid shell newline/quoting issues.
    """
    cmd = ["gh", "api", "graphql", "-F", "query=@-"]
    for name, value in variables.items():
        if value is not None:
            cmd += ["-F", f"{name}={value}"]
    payload = _run_json(cmd, stdin=query)
    if payload.get("errors"):
        raise RuntimeError(f"GitHub GraphQL errors:\n{json.dumps(payload['errors'], indent=2)}")
    return payload["data"]


def _paginate(fetch_page) -> list[dict[str, Any]]:
    nodes: list[dict[str, Any]] = []
    cursor: str | None = None
    while True:
        page = fetch_page(cursor)
        nodes.extend(page.get("nodes") or [])
        if not page["pageInfo"]["hasNextPage"]:
            return nodes
        cursor = page["pageInfo"]["endCursor"]


def fetch_all(owner: str, repo: str, number: int) -> dict[str, Any]:
    pr_meta: dict[str, Any] = {}
    collected: dict[str, list[dict[str, Any]]] = {}

    for connection, fields in CONNECTIONS.items():
        query = PR_QUERY % (connection, fields)

        def fetch_page(cursor: str | None, connection: str = connection, query: str = query) -> dict[str, Any]:
            pr = gh_api_graphql(query, owner=owner, repo=repo, number=number, cursor=cursor)["repository"]["pullRequest"]
            pr_meta.setdefault("pull_request", {
                "number": pr["number"],
                "url": pr["url"],
                "title": pr["title"],
                "state": pr["state"],
                "owner": owner,
                "repo": repo,
            })
            return pr[connection]

        collected[connection] = _paginate(fetch_page)

    for thread in collected["reviewThreads"]:
        first = thread["comments"]
        nodes = list(first.get("nodes") or [])
        if first["pageInfo"]["hasNextPage"]:
            start = first["pageInfo"]["endCursor"]

            def fetch_thread_page(cursor: str | None, thread_id: str = thread["id"], start: str = start) -> dict[str, Any]:
                return gh_api_graphql(THREAD_COMMENTS_QUERY, id=thread_id, cursor=cursor or start)["node"]["comments"]

            nodes.extend(_paginate(fetch_thread_page))
        thread["comments"] = {"nodes": nodes}

    return {
        "pull_request": pr_meta["pull_request"],
        "conversation_comments": collected["comments"],
        "reviews": collected["reviews"],
        "review_threads": collected["reviewThreads"],
    }


def main() -> None:
    _ensure_gh_authenticated()
    pr = sys.argv[1] if len(sys.argv) > 1 else None
    owner, repo, number = get_pr_ref(pr)
    result = fetch_all(owner, repo, number)
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
