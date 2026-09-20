#!/usr/bin/env python3

from __future__ import annotations

import argparse
import json
from pathlib import Path
import sys
import tomllib


SKILL_DIR = Path(__file__).resolve().parent.parent
ROLE_DIR = SKILL_DIR / "assets" / "roles"
CODEX_DIR = SKILL_DIR / "assets" / "codex-agents"
CLAUDE_DIR = SKILL_DIR / "assets" / "claude-agents"


def load_roles() -> list[dict[str, str]]:
    roles: list[dict[str, str]] = []
    for path in sorted(ROLE_DIR.glob("*.toml")):
        with path.open("rb") as handle:
            role = tomllib.load(handle)
        required = {"name", "description", "default_permissions", "instructions"}
        missing = required.difference(role)
        if missing:
            raise ValueError(f"{path} is missing: {', '.join(sorted(missing))}")
        if path.stem != role["name"]:
            raise ValueError(f"{path}: filename must match role name {role['name']!r}")
        if role["default_permissions"] not in {"inherit", "read-only"}:
            raise ValueError(f"{path}: unsupported default_permissions")
        if '"""' in role["instructions"]:
            raise ValueError(f"{path}: instructions cannot contain TOML triple quotes")
        roles.append(role)
    if not roles:
        raise ValueError(f"no role definitions found in {ROLE_DIR}")
    return roles


def render_codex(role: dict[str, str]) -> str:
    lines = [
        f"name = {json.dumps(role['name'])}",
        f"description = {json.dumps(role['description'])}",
    ]
    if role["default_permissions"] == "read-only":
        lines.append('sandbox_mode = "read-only"')
    lines.extend(
        [
            'developer_instructions = """',
            role["instructions"].strip(),
            '"""',
            "",
        ]
    )
    return "\n".join(lines)


def render_claude(role: dict[str, str]) -> str:
    lines = [
        "---",
        f"name: {role['name']}",
        f"description: {json.dumps(role['description'])}",
    ]
    if role["default_permissions"] == "read-only":
        lines.extend(
            [
                "permissionMode: plan",
                "tools: Read, Grep, Glob, Bash, WebFetch, WebSearch",
            ]
        )
    lines.extend(["---", "", role["instructions"].strip(), ""])
    return "\n".join(lines)


def expected_outputs() -> dict[Path, str]:
    outputs: dict[Path, str] = {}
    for role in load_roles():
        outputs[CODEX_DIR / f"{role['name']}.toml"] = render_codex(role)
        outputs[CLAUDE_DIR / f"{role['name']}.md"] = render_claude(role)
    return outputs


def main() -> int:
    parser = argparse.ArgumentParser(description="Render Codex and Claude Code agent profiles")
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument("--write", action="store_true", help="write generated profiles")
    mode.add_argument("--check", action="store_true", help="verify generated profiles are current")
    args = parser.parse_args()

    outputs = expected_outputs()
    status = 0
    for path, expected in outputs.items():
        if args.write:
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(expected, encoding="utf-8")
            print(f"wrote {path.relative_to(SKILL_DIR)}")
            continue
        actual = path.read_text(encoding="utf-8") if path.exists() else None
        if actual != expected:
            print(f"stale {path.relative_to(SKILL_DIR)}", file=sys.stderr)
            status = 1
        else:
            print(f"valid {path.relative_to(SKILL_DIR)}")
    return status


if __name__ == "__main__":
    raise SystemExit(main())
