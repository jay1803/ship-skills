#!/usr/bin/env python3
"""Read-only quiet-return check over a controller's supplied observations.

Optional aid for the controller recovery contract's quiet-return predicate. It
reads a JSON projection of the existing registry (stdin with `--input -`, or a
file), reads no native tools, trackers or processes, verifies no receipt bytes,
writes no state and performs no recovery or merge. Its result checks the
supplied projection, not the truth or completeness of the observations.

Input:
  {"project_status": "running | complete | stopped",
   "controller_run_status": "succeeded | failed | not-observed",
   "wake_path_verified": true, "adapter_checks_complete": true,
   "targets": [{"id": "ISSUE-1", "kind": "worker | external-gate",
                "resolved": false, "status": "waiting | actionable | failed | unknown",
                "first_turn_observed": true,
                "observed_at": "2026-01-01T10:00:00Z", "evidence_ref": "native-status:cursor-1",
                "next_check_at": "2026-01-01T10:45:00Z", "wait_for": "build run 1",
                "next_action_owner": "worker-1"}]}

Include every unresolved worker, external gate and ready controller action; an
action awaiting controller execution is `actionable`, not healthy waiting.
Resolved targets need only id, kind and resolved. Timestamps need a timezone.
Output: disposition (quiet | reconcile | runtime-unavailable | complete |
stopped), quiet_allowed, wake_required, host_recovery_required and reasons.
"""

from __future__ import annotations

import argparse
import json
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


def timestamp(value: Any, field: str) -> datetime:
    if not isinstance(value, str):
        raise ValueError(f"{field} must be a timezone-aware ISO timestamp")
    try:
        parsed = datetime.fromisoformat(value.replace("Z", "+00:00"))
    except ValueError:
        raise ValueError(f"{field} must be a timezone-aware ISO timestamp") from None
    if parsed.tzinfo is None:
        raise ValueError(f"{field} must include a timezone")
    return parsed.astimezone(timezone.utc)


def choice(value: Any, values: set[str], field: str) -> str:
    if not isinstance(value, str) or value not in values:
        raise ValueError(f"{field} has an unsupported value")
    return value


def nonempty(value: Any) -> bool:
    return isinstance(value, str) and bool(value.strip())


def assess(data: Any, now: datetime) -> dict[str, Any]:
    if not isinstance(data, dict):
        raise ValueError("input must be an object")
    project = choice(data.get("project_status"), {"running", "complete", "stopped"},
                     "project_status")
    run = choice(data.get("controller_run_status"),
                 {"succeeded", "failed", "not-observed"}, "controller_run_status")
    for key in ("wake_path_verified", "adapter_checks_complete"):
        if type(data.get(key)) is not bool:
            raise ValueError(f"{key} must be a boolean")
    targets = data.get("targets")
    if not isinstance(targets, list):
        raise ValueError("targets must be a list")

    reasons: list[dict[str, str]] = []
    unresolved: list[dict[str, Any]] = []
    ids: set[str] = set()

    def add(target: str, reason: str) -> None:
        reasons.append({"target": target, "reason": reason})

    for item in targets:
        if not isinstance(item, dict) or not nonempty(item.get("id")):
            raise ValueError("every target must have a nonempty id")
        identifier = item["id"]
        if identifier in ids:
            raise ValueError("target ids must be unique")
        ids.add(identifier)
        kind = choice(item.get("kind"), {"worker", "external-gate"}, "target.kind")
        if type(item.get("resolved")) is not bool:
            raise ValueError("target.resolved must be a boolean")
        if item["resolved"]:
            continue
        unresolved.append(item)
        status = choice(item.get("status"),
                        {"waiting", "actionable", "failed", "unknown"}, "target.status")
        if project == "stopped":
            continue
        if status != "waiting":
            add(identifier, status)
        first_turn = item.get("first_turn_observed")
        if first_turn is not None and type(first_turn) is not bool:
            raise ValueError("first_turn_observed must be boolean or null")
        if kind == "worker" and first_turn is not True:
            add(identifier, "first-turn-unverified")

        observed = item.get("observed_at")
        if observed is None or not nonempty(item.get("evidence_ref")):
            add(identifier, "observation-missing")
        elif timestamp(observed, "observed_at") > now:
            add(identifier, "observation-in-future")

        next_check = item.get("next_check_at")
        if next_check is None:
            add(identifier, "check-unscheduled")
        elif timestamp(next_check, "next_check_at") <= now:
            add(identifier, "check-due")

        if status == "waiting" and not nonempty(item.get("wait_for")):
            add(identifier, "waiting-object-missing")
        if not nonempty(item.get("next_action_owner")):
            add(identifier, "next-owner-missing")

    if project == "stopped":
        disposition = "stopped"
        wake_required = False
    elif project == "complete" and not unresolved:
        disposition = "complete"
        wake_required = False
    else:
        wake_required = True
        if project == "complete":
            add("controller", "completion-has-unresolved-targets")
        if run != "succeeded":
            add("controller", "controller-run-" + run)
        if not data["adapter_checks_complete"]:
            add("controller", "adapter-checks-incomplete")
        if not data["wake_path_verified"]:
            add("controller", "wake-path-unverified")
        if not unresolved:
            add("controller", "completion-or-admission-unreconciled")
        if run != "succeeded":
            disposition = "runtime-unavailable"
        elif reasons:
            disposition = "reconcile"
        else:
            disposition = "quiet"

    return {
        "schema_version": 1,
        "disposition": disposition,
        "quiet_allowed": disposition == "quiet",
        "wake_required": wake_required,
        "host_recovery_required": disposition == "runtime-unavailable",
        "reasons": reasons,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__,
                                     formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--input", required=True, help="JSON file, or - for stdin")
    parser.add_argument("--now", required=True, help="timezone-aware ISO check time")
    args = parser.parse_args()
    try:
        raw = sys.stdin.read() if args.input == "-" else Path(args.input).read_text()
        result = assess(json.loads(raw), timestamp(args.now, "now"))
    except (OSError, ValueError) as exc:
        # Do not echo raw input, evidence locators or private source contents.
        message = "input is not valid JSON" if isinstance(exc, json.JSONDecodeError) else str(exc)
        print(json.dumps({"schema_version": 1, "error": message}), file=sys.stderr)
        return 2
    print(json.dumps(result, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

