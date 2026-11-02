#!/usr/bin/env python3
"""Read requested Codex/Claude JSONL snapshots without executing their content."""
from __future__ import annotations

import argparse
from collections import Counter
import hashlib
import json
import os
from pathlib import Path
import re
import sys

ID = re.compile(r"[A-Za-z0-9][A-Za-z0-9_-]{7,127}\Z")
CODEX_TYPES = {"session_meta", "turn_context", "response_item", "event_msg", "compacted"}
SECRET_KEY = re.compile(r"(?i)^(?:api[_-]?key|access[_-]?token|refresh[_-]?token|password|authorization|secret)$")
SECRET_TEXT = [
    (re.compile(r"(?i)\bBearer\s+[A-Za-z0-9._~+/=-]+"), "Bearer [REDACTED]"),
    (re.compile(r"\b(?:sk-[A-Za-z0-9_-]{12,}|gh[pousr]_[A-Za-z0-9]{12,}|github_pat_[A-Za-z0-9_]{12,})"), "[REDACTED]"),
    (re.compile(r"(?i)\b(api[_-]?key|access[_-]?token|refresh[_-]?token|password|secret)\s*[:=]\s*[^\s,;]+"), r"\1=[REDACTED]"),
]


def sanitize(value):
    if isinstance(value, dict):
        return {k: "[REDACTED]" if SECRET_KEY.fullmatch(k) else sanitize(v) for k, v in value.items()}
    if isinstance(value, list):
        return [sanitize(v) for v in value]
    if isinstance(value, str):
        for pattern, replacement in SECRET_TEXT:
            value = pattern.sub(replacement, value)
    return value


def read_snapshot(path):
    """Hash and parse the same byte stream, retaining locators for malformed rows."""
    records, warnings = [], []
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        before = os.fstat(handle.fileno())
        for line, raw in enumerate(handle, 1):
            digest.update(raw)
            try:
                obj = json.loads(raw)
                if not isinstance(obj, dict):
                    raise ValueError("record is not an object")
            except (ValueError, UnicodeError):
                warnings.append({"line": line, "warning": "invalid JSON object; content omitted"})
                obj = {"type": "unparsed"}
            records.append((line, obj, hashlib.sha256(raw).hexdigest()))
        after = os.fstat(handle.fileno())
    if (before.st_size, before.st_mtime_ns) != (after.st_size, after.st_mtime_ns):
        warnings.append({"warning": "file changed during read; snapshot may be incomplete"})
    return records, digest.hexdigest(), warnings


def source_identity(records):
    providers, identities = set(), set()
    for _, obj, _ in records:
        kind = obj.get("type")
        payload = obj.get("payload")
        if isinstance(kind, str) and kind in CODEX_TYPES and isinstance(payload, dict):
            providers.add("codex")
            if kind == "session_meta" and isinstance(payload.get("id"), str):
                identities.add(payload["id"])
        if isinstance(obj.get("sessionId"), str):
            providers.add("claude")
            identities.add(obj["sessionId"])
        elif isinstance(obj.get("message"), dict) and isinstance(kind, str) and kind in {"user", "assistant"}:
            providers.add("claude")
    return providers, identities


def discover(request, codex_home, claude_home):
    provider, sid = request.split(":", 1) if ":" in request else (None, request)
    if provider not in {None, "codex", "claude"} or not ID.fullmatch(sid):
        raise ValueError("expected [codex:|claude:]session-id (8-128 letters, digits, _ or -)")
    paths = []
    if provider in {None, "codex"}:
        for root in (codex_home / "sessions", codex_home / "archived_sessions"):
            paths.extend(("codex", p) for p in root.rglob(f"*{sid}.jsonl")
                         if p.stem == sid or p.stem.endswith("-" + sid))
    if provider in {None, "claude"}:
        paths.extend(("claude", p) for p in (claude_home / "projects").rglob(f"{sid}.jsonl"))
    return sid, sorted(set(paths), key=lambda item: str(item[1]))


def describe(line, obj, digest):
    payload = obj.get("payload")
    body = payload if isinstance(payload, dict) else obj
    kind = body.get("type", obj.get("type", "unknown"))
    message = obj.get("message")
    blocks = message.get("content", []) if isinstance(message, dict) else []
    tools = [b.get("name") for b in blocks if isinstance(b, dict) and b.get("type") == "tool_use"] if isinstance(blocks, list) else []
    if body.get("name"):
        tools.append(body["name"])
    return sanitize({
        "line": line, "record_sha256": digest,
        "type": kind, "envelope": obj.get("type", "unknown"),
        "timestamp": obj.get("timestamp", body.get("timestamp")),
        "role": body.get("role", message.get("role") if isinstance(message, dict) else None),
        "event_id": obj.get("uuid", body.get("id")),
        "parent_id": obj.get("parentUuid"), "call_id": body.get("call_id"),
        "tools": tools,
    })


def render(path, records, digest, warnings, args, provider, identities, aliases):
    selected = set()
    for i, (line, obj, _) in enumerate(records):
        if args.lines and not args.lines[0] <= line <= args.lines[1]:
            continue
        if args.match and args.match.casefold() not in json.dumps(obj, ensure_ascii=False).casefold():
            continue
        selected.update(range(max(0, i - args.context), min(len(records), i + args.context + 1)))
    chosen = sorted(selected)
    page = chosen[args.offset:args.offset + args.limit]
    events = []
    for index in page:
        line, obj, record_hash = records[index]
        entry = describe(line, obj, record_hash)
        if args.mode == "excerpts":
            excerpt = json.dumps(sanitize(obj), ensure_ascii=False)
            entry.update(excerpt=excerpt[:args.max_chars], excerpt_chars=len(excerpt),
                         truncated=len(excerpt) > args.max_chars)
        events.append(entry)
    return {
        "status": "ok", "provider": provider, "session_ids": sorted(identities),
        "identity_verified": bool(identities), "path": str(path), "aliases": aliases,
        "sha256": digest, "line_count": len(records), "warnings": warnings,
        "type_counts": dict(Counter(str(obj.get("type", "unknown")) for _, obj, _ in records)),
        "selected_count": len(chosen), "offset": args.offset,
        "next_offset": args.offset + len(page) if args.offset + len(page) < len(chosen) else None,
        "events": events,
    }


def resolve_snapshot(request, args, explicit=False):
    """Resolve one requested snapshot for bounded readers and analyzers."""
    sid, candidates = (None, [(None, Path(request).expanduser().absolute())]) if explicit else discover(
        request, args.codex_home, args.claude_home)
    if not candidates:
        return {"request": request, "status": "missing", "error": "no matching local transcript"}
    groups = {}
    for expected_provider, path in candidates:
        records, digest, warnings = read_snapshot(path)
        providers, identities = source_identity(records)
        if len(providers) != 1 or len(identities) > 1:
            raise ValueError(f"unsupported or mixed transcript identity at {path}")
        provider = next(iter(providers))
        if expected_provider and provider != expected_provider:
            raise ValueError(f"provider mismatch at {path}")
        if sid and identities and sid not in identities:
            raise ValueError(f"embedded session ID does not match requested ID at {path}")
        if not identities:
            warnings.append({"warning": "embedded session identity unavailable; filename identity only"})
        key = (provider, digest)
        if key in groups:
            groups[key][-1].append(str(path))
        else:
            groups[key] = (path, records, digest, warnings, provider, identities, [])
    if len(groups) > 1:
        return {"request": request, "status": "ambiguous", "candidates": [
            {"path": str(g[0]), "provider": g[4], "sha256": g[2], "aliases": g[6]}
            for g in groups.values()]}
    path, records, digest, warnings, provider, identities, aliases = next(iter(groups.values()))
    return {"request": request, "status": "ok", "path": path, "records": records,
            "sha256": digest, "warnings": warnings, "provider": provider,
            "session_ids": identities, "aliases": aliases}


def resolve(request, args, explicit=False):
    snapshot = resolve_snapshot(request, args, explicit)
    if snapshot["status"] != "ok":
        return snapshot
    result = render(snapshot["path"], snapshot["records"], snapshot["sha256"],
                    snapshot["warnings"], args, snapshot["provider"],
                    snapshot["session_ids"], snapshot["aliases"])
    result["request"] = request
    return result


def line_range(value):
    try:
        start, end = map(int, value.split(":"))
        if 0 < start <= end:
            return start, end
    except ValueError:
        pass
    raise argparse.ArgumentTypeError("expected inclusive START:END with 1 <= START <= END")


def positive(value):
    number = int(value)
    if number < 1:
        raise argparse.ArgumentTypeError("must be positive")
    return number


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("sessions", nargs="*")
    parser.add_argument("--file", action="append", default=[])
    parser.add_argument("--codex-home", type=Path, default=Path(os.environ.get("CODEX_HOME", "~/.codex")).expanduser())
    parser.add_argument("--claude-home", type=Path, default=Path(os.environ.get("CLAUDE_CONFIG_DIR", "~/.claude")).expanduser())
    parser.add_argument("--mode", choices=["index", "excerpts"], default="index")
    parser.add_argument("--offset", type=int, default=0)
    parser.add_argument("--limit", type=positive, default=80)
    parser.add_argument("--max-chars", type=positive, default=3000)
    filters = parser.add_mutually_exclusive_group()
    filters.add_argument("--lines", type=line_range)
    filters.add_argument("--match")
    parser.add_argument("--context", type=int, default=0)
    args = parser.parse_args(argv)
    if not args.sessions and not args.file:
        parser.error("supply a session ID or --file")
    if args.offset < 0 or args.context < 0:
        parser.error("offset and context must be nonnegative")
    args.codex_home = args.codex_home.expanduser().absolute()
    args.claude_home = args.claude_home.expanduser().absolute()
    results, seen = [], {}
    for request, explicit in [(s, False) for s in args.sessions] + [(f, True) for f in args.file]:
        try:
            result = resolve(request, args, explicit)
        except (OSError, ValueError) as exc:
            result = {"request": request, "status": "error", "error": str(exc)}
        if result["status"] == "ok":
            key = (result["provider"], result["sha256"])
            if key in seen:
                result = {"request": request, "status": "duplicate", "same_as": seen[key]}
            else:
                seen[key] = request
        results.append(result)
    print(json.dumps({"schema_version": 1, "sources": sanitize(results)}, ensure_ascii=False, indent=2))
    return int(any(r["status"] not in {"ok", "duplicate"} for r in results))


if __name__ == "__main__":
    sys.exit(main())
