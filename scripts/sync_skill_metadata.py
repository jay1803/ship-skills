#!/usr/bin/env python3

from __future__ import annotations

import re
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]


def active_skills() -> list[tuple[Path, dict[str, str]]]:
    skills: list[tuple[Path, dict[str, str]]] = []
    for plugin_dir in sorted((REPO_ROOT / "plugins").iterdir()):
        skills_dir = plugin_dir / "skills"
        if not skills_dir.is_dir():
            continue
        for skill_dir in sorted(skills_dir.iterdir()):
            skill_file = skill_dir / "SKILL.md"
            if skill_file.is_file():
                skills.append(
                    (
                        skill_file,
                        {
                            "owner": "jay1803",
                            "family": plugin_dir.name,
                            "maturity": "stable",
                            "distribution": plugin_dir.name,
                        },
                    )
                )
    return skills


def update_frontmatter(path: Path, fields: dict[str, str]) -> bool:
    text = path.read_text(encoding="utf-8")
    lines = text.splitlines(keepends=True)
    if not lines or lines[0].strip() != "---":
        raise ValueError(f"Missing YAML frontmatter: {path}")

    end = next(
        (index for index, line in enumerate(lines[1:], start=1) if line.strip() == "---"),
        None,
    )
    if end is None:
        raise ValueError(f"Unclosed YAML frontmatter: {path}")

    metadata_index = next(
        (index for index in range(1, end) if lines[index].rstrip("\r\n") == "metadata:"),
        None,
    )
    changed = False

    if metadata_index is None:
        addition = ["metadata:\n"] + [f"  {key}: {value}\n" for key, value in fields.items()]
        lines[end:end] = addition
        changed = True
    else:
        block_end = metadata_index + 1
        while block_end < end:
            line = lines[block_end]
            if line.strip() and not line.startswith((" ", "\t")):
                break
            block_end += 1

        existing = set()
        for line in lines[metadata_index + 1 : block_end]:
            match = re.match(r"^\s{2}([a-zA-Z0-9_-]+):", line)
            if match:
                existing.add(match.group(1))

        addition = [
            f"  {key}: {value}\n" for key, value in fields.items() if key not in existing
        ]
        if addition:
            lines[block_end:block_end] = addition
            changed = True

    if changed:
        path.write_text("".join(lines), encoding="utf-8")
    return changed


def main() -> None:
    changed = 0
    for path, fields in active_skills():
        if update_frontmatter(path, fields):
            changed += 1
    print(f"Updated metadata in {changed} skill files.")


if __name__ == "__main__":
    main()
