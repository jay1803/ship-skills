#!/usr/bin/env python3
"""Print context for drafting release notes from the latest main commit."""

from __future__ import annotations

import argparse
import subprocess
import sys


def run_git(args: list[str], *, check: bool = True) -> str:
    result = subprocess.run(
        ["git", *args],
        check=False,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
    )
    if check and result.returncode != 0:
        message = result.stderr.strip() or result.stdout.strip()
        raise SystemExit(f"git {' '.join(args)} failed: {message}")
    return result.stdout.rstrip()


def ref_exists(ref: str) -> bool:
    result = subprocess.run(
        ["git", "rev-parse", "--verify", "--quiet", ref],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )
    return result.returncode == 0


def resolve_ref(preferred: str) -> str:
    candidates = [
        preferred,
        f"origin/{preferred}",
        "main",
        "origin/main",
        "master",
        "origin/master",
    ]
    for candidate in candidates:
        if ref_exists(candidate):
            return candidate
    raise SystemExit(
        "Could not find main branch. Pass --ref <branch> from inside a git repository."
    )


def print_section(title: str, content: str) -> None:
    print(f"\n## {title}")
    print(content if content.strip() else "(none)")


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Collect latest main commit context for user-friendly release notes."
    )
    parser.add_argument(
        "--ref",
        default="main",
        help="Primary branch or ref to inspect. Defaults to main.",
    )
    parser.add_argument(
        "--fetch",
        action="store_true",
        help="Run git fetch before inspecting the ref.",
    )
    parser.add_argument(
        "--diff-lines",
        type=int,
        default=600,
        help="Maximum diff lines to print. Use 0 for no diff.",
    )
    args = parser.parse_args()

    run_git(["rev-parse", "--show-toplevel"])
    if args.fetch:
        run_git(["fetch", "--prune"])

    ref = resolve_ref(args.ref)
    commit = run_git(["rev-parse", ref])

    print(f"# Latest release-note context for {ref}")
    print(f"Commit: {commit}")
    print_section("Commit Message", run_git(["log", "-1", "--format=%B", commit]))
    print_section(
        "Changed Files",
        run_git(["show", "--format=", "--name-status", "--find-renames", commit]),
    )
    print_section("Stats", run_git(["show", "--format=", "--stat", commit]))

    if args.diff_lines != 0:
        diff = run_git(["show", "--format=", "--find-renames", commit, "--"])
        lines = diff.splitlines()
        if len(lines) > args.diff_lines:
            diff = "\n".join(lines[: args.diff_lines])
            diff += f"\n\n[truncated after {args.diff_lines} lines]"
        print_section("Diff", diff)

    return 0


if __name__ == "__main__":
    sys.exit(main())
