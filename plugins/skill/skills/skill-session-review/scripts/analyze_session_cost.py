#!/usr/bin/env python3
"""Summarize observable Codex/Claude transcript costs without judging necessity."""
from __future__ import annotations

import argparse
from collections import Counter, defaultdict
import hashlib
import json
import os
from pathlib import Path
import re
import sys

import read_sessions as reader

METADATA_NAME = re.compile(r"[A-Za-z0-9_./:-]{1,120}\Z")


def safe_name(value):
    return value if isinstance(value, str) and METADATA_NAME.fullmatch(value) else "unknown"


def bounded_lines(lines, limit=20):
    if len(lines) <= limit:
        return {"lines": lines, "omitted_lines": 0}
    half = limit // 2
    return {"lines": lines[:half] + lines[-half:], "omitted_lines": len(lines) - limit}


def text_chars(content):
    if isinstance(content, str):
        return len(content)
    if isinstance(content, list):
        return sum(len(block.get("text", "")) for block in content
                   if isinstance(block, dict) and isinstance(block.get("text"), str)
                   and block.get("type") not in {"tool_result", "tool_use"})
    return 0


def result_text(content):
    if content is None:
        return ""
    if isinstance(content, str):
        return content
    return json.dumps(content, ensure_ascii=False, sort_keys=True)


def token_fields(usage):
    if not isinstance(usage, dict):
        return {}
    return {key: value for key, value in usage.items()
            if (key == "total_tokens" or key.endswith("_tokens"))
            and isinstance(value, int) and not isinstance(value, bool) and value >= 0}


def codex_usage(records):
    samples = []
    for line, obj, _ in records:
        if obj.get("type") != "event_msg":
            continue
        payload = obj.get("payload", {})
        if not isinstance(payload, dict) or payload.get("type") != "token_count":
            continue
        info = payload.get("info", {})
        usage = token_fields(info.get("total_token_usage")) if isinstance(info, dict) else {}
        if usage:
            samples.append((line, usage))
    if not samples:
        return {"status": "unavailable", "basis": "no cumulative token snapshot"}
    line, usage = samples[-1]
    warnings = []
    if any(previous.get("total_tokens", 0) > following.get("total_tokens", 0)
           for (_, previous), (_, following) in zip(samples, samples[1:])
           if "total_tokens" in previous and "total_tokens" in following):
        warnings.append("nonmonotonic cumulative total; inspect snapshot boundaries")
    return {"status": "observed", "basis": "last observed cumulative snapshot",
            "line": line, "snapshot_count": len(samples), "tokens": usage,
            "warnings": warnings, "model_attribution": "unavailable"}


def claude_usage(records):
    messages = {}
    unkeyed_lines = []
    for line, obj, _ in records:
        if obj.get("type") != "assistant":
            continue
        message = obj.get("message", {})
        if not isinstance(message, dict):
            continue
        usage = token_fields(message.get("usage"))
        if not usage:
            continue
        message_id = message.get("id")
        if not isinstance(message_id, str) or not message_id:
            unkeyed_lines.append(line)
            continue
        model = safe_name(message.get("model")) if isinstance(message.get("model"), str) else None
        if message_id not in messages:
            messages[message_id] = {"tokens": usage, "lines": [line], "model": model}
        else:
            prior = messages[message_id]
            prior["lines"].append(line)
            for key, value in usage.items():
                prior["tokens"][key] = max(prior["tokens"].get(key, 0), value)
            if model and prior["model"] and model != prior["model"]:
                prior["model"] = "ambiguous"
            elif model and not prior["model"]:
                prior["model"] = model
    if not messages:
        return ({"status": "unavailable", "basis": "no keyed message usage",
                 "unkeyed_usage_count": len(unkeyed_lines),
                 "unkeyed_usage_lines": bounded_lines(unkeyed_lines)["lines"],
                 "unkeyed_usage_omitted_lines": bounded_lines(unkeyed_lines)["omitted_lines"]}, [])
    totals = Counter()
    models = defaultdict(Counter)
    for message in messages.values():
        totals.update(message["tokens"])
        models[message["model"] or "unknown"].update(message["tokens"])
    usage = {"status": "partial" if unkeyed_lines else "observed",
             "basis": "maximum observed fields per message ID",
             "message_count": len(messages), "unkeyed_usage_count": len(unkeyed_lines),
             "unkeyed_usage_lines": bounded_lines(unkeyed_lines)["lines"],
             "unkeyed_usage_omitted_lines": bounded_lines(unkeyed_lines)["omitted_lines"],
             "tokens": dict(totals)}
    attributed = [{"model": model, "tokens": dict(tokens)}
                  for model, tokens in sorted(models.items())]
    return usage, attributed


def profile(snapshot):
    records = snapshot["records"]
    provider = snapshot["provider"]
    calls = {}
    results = []
    load_candidates = []
    visible = defaultdict(lambda: {"characters": 0, "lines": []})
    models = defaultdict(list)
    compactions = []
    for line, obj, _ in records:
        kind = obj.get("type")
        if provider == "codex":
            payload = obj.get("payload", {})
            if not isinstance(payload, dict):
                continue
            if kind == "turn_context" and isinstance(payload.get("model"), str):
                models[safe_name(payload["model"])].append(line)
            if kind == "compacted":
                compactions.append(line)
            if kind != "response_item":
                continue
            subtype = payload.get("type")
            if subtype == "message" and payload.get("role") in {"user", "system", "developer"}:
                chars = text_chars(payload.get("content"))
                visible[payload["role"]]["characters"] += chars
                visible[payload["role"]]["lines"].append(line)
            if subtype in {"function_call", "custom_tool_call"}:
                call_id = payload.get("call_id")
                key = call_id if isinstance(call_id, str) and call_id else f"line:{line}"
                calls.setdefault(key, {"name": safe_name(payload.get("name")), "line": line,
                                       "arguments": payload.get("arguments")})
            if subtype in {"function_call_output", "custom_tool_call_output"}:
                call_id = payload.get("call_id")
                call = calls.get(call_id, {})
                content = result_text(payload.get("output"))
                results.append((call.get("name", "unknown"), line, content))
                add_load_candidate(load_candidates, call, line, len(content))
        else:
            message = obj.get("message", {})
            if not isinstance(message, dict):
                continue
            if kind == "assistant" and isinstance(message.get("model"), str):
                models[safe_name(message["model"])].append(line)
            role = message.get("role")
            if role in {"user", "system", "developer"}:
                chars = text_chars(message.get("content"))
                if chars:
                    visible[role]["characters"] += chars
                    visible[role]["lines"].append(line)
            blocks = message.get("content")
            if not isinstance(blocks, list):
                continue
            for index, block in enumerate(blocks):
                if not isinstance(block, dict):
                    continue
                if block.get("type") == "tool_use":
                    call_id = block.get("id")
                    key = call_id if isinstance(call_id, str) and call_id else f"line:{line}:{index}"
                    calls.setdefault(key, {"name": safe_name(block.get("name")), "line": line,
                                           "arguments": block.get("input")})
                elif block.get("type") == "tool_result":
                    call_id = block.get("tool_use_id")
                    call = calls.get(call_id, {})
                    content = result_text(block.get("content"))
                    results.append((call.get("name", "unknown"), line, content))
                    add_load_candidate(load_candidates, call, line, len(content))
    counts = defaultdict(lambda: {"count": 0, "lines": []})
    for call in calls.values():
        counts[call["name"]]["count"] += 1
        counts[call["name"]]["lines"].append(call["line"])
    fingerprints = defaultdict(list)
    result_chars = 0
    for name, line, content in results:
        result_chars += len(content)
        digest = hashlib.sha256(content.encode("utf-8")).hexdigest()
        fingerprints[(name, digest, len(content))].append(line)
    repeated = [{"tool": name, "sha256": digest, "characters": chars,
                 "count": len(lines), **bounded_lines(lines)}
                for (name, digest, chars), lines in sorted(fingerprints.items())
                if len(lines) > 1]
    if provider == "codex":
        usage, model_usage = codex_usage(records), []
    else:
        usage, model_usage = claude_usage(records)
    return {
        "request": snapshot["request"], "status": "ok", "provider": provider,
        "session_ids": sorted(snapshot["session_ids"]),
        "identity_verified": bool(snapshot["session_ids"]),
        "path": str(snapshot["path"]), "aliases": snapshot["aliases"],
        "sha256": snapshot["sha256"], "line_count": len(records),
        "warnings": snapshot["warnings"][:10],
        "warning_count": len(snapshot["warnings"]), "usage": usage,
        "observed_models": [{"model": name, "count": len(lines), **bounded_lines(lines)}
                            for name, lines in sorted(models.items())],
        "message_model_usage": model_usage,
        "visible_input": {"by_role": {role: {"characters": info["characters"],
                                        "message_count": len(info["lines"]),
                                        **bounded_lines(info["lines"])}
                                      for role, info in visible.items()},
                          "coverage": "visible messages only; injected or prior context may be unavailable"},
        "tools": {"calls_by_name": {name: {"count": info["count"],
                                          **bounded_lines(info["lines"])}
                                    for name, info in sorted(counts.items())},
                  "result_count": len(results), "result_characters": result_chars,
                  "identical_result_candidates": repeated,
                  "coverage": "observed calls/results only; repeated output is not proof of waste"},
        "instruction_load_candidates": load_candidates[:20],
        "instruction_load_candidate_count": len(load_candidates),
        "instruction_load_candidates_omitted": max(0, len(load_candidates) - 20),
        "context": {"codex_compaction_count": len(compactions),
                    "codex_compaction_lines": bounded_lines(compactions)["lines"],
                    "coverage": "other compaction and handoff state may be unavailable"},
    }


def add_load_candidate(candidates, call, result_line, result_chars):
    arguments = call.get("arguments")
    if arguments is None:
        return
    argument_text = result_text(arguments)
    if "SKILL.md" in argument_text:
        kind = "skill_core"
    elif "references/" in argument_text or "references\\" in argument_text:
        kind = "reference"
    else:
        return
    candidates.append({"kind": kind, "call_line": call["line"],
                       "result_line": result_line, "result_characters": result_chars,
                       "coverage": "path mention in call arguments; verify actual load in transcript"})


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("sessions", nargs="*")
    parser.add_argument("--file", action="append", default=[])
    parser.add_argument("--codex-home", type=Path,
                        default=Path(os.environ.get("CODEX_HOME", "~/.codex")).expanduser())
    parser.add_argument("--claude-home", type=Path,
                        default=Path(os.environ.get("CLAUDE_CONFIG_DIR", "~/.claude")).expanduser())
    args = parser.parse_args(argv)
    if not args.sessions and not args.file:
        parser.error("supply a session ID or --file")
    args.codex_home = args.codex_home.expanduser().absolute()
    args.claude_home = args.claude_home.expanduser().absolute()
    sources, seen = [], {}
    for request, explicit in [(s, False) for s in args.sessions] + [(f, True) for f in args.file]:
        try:
            snapshot = reader.resolve_snapshot(request, args, explicit)
            if snapshot["status"] == "ok":
                key = (snapshot["provider"], snapshot["sha256"])
                if key in seen:
                    source = {"request": request, "status": "duplicate", "same_as": seen[key]}
                else:
                    seen[key] = request
                    source = profile(snapshot)
            else:
                source = snapshot
        except (OSError, ValueError) as exc:
            source = {"request": request, "status": "error", "error": str(exc)}
        sources.append(source)
    print(json.dumps({"schema_version": 1, "sources": sources}, ensure_ascii=False, indent=2))
    return int(any(source["status"] not in {"ok", "duplicate"} for source in sources))


if __name__ == "__main__":
    sys.exit(main())
