#!/usr/bin/env python3

from __future__ import annotations

import json
import re
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
OUTPUT = REPO_ROOT / "catalog" / "skills.json"


def frontmatter(path: Path) -> tuple[dict[str, str], dict[str, str]]:
    lines = path.read_text(encoding="utf-8").splitlines()
    if not lines or lines[0] != "---":
        raise ValueError(f"Missing frontmatter: {path}")
    end = lines.index("---", 1)
    values: dict[str, str] = {}
    metadata: dict[str, str] = {}
    in_metadata = False
    for line in lines[1:end]:
        if line == "metadata:":
            in_metadata = True
            continue
        if in_metadata:
            match = re.match(r"^\s{2}([a-zA-Z0-9_-]+):\s*[\"']?(.*?)[\"']?$", line)
            if match:
                metadata[match.group(1)] = match.group(2)
                continue
            if line and not line.startswith((" ", "\t")):
                in_metadata = False
        match = re.match(r"^([a-zA-Z0-9_-]+):\s*[>|]?-?\s*(.*)$", line)
        if match and not in_metadata:
            values[match.group(1)] = match.group(2).strip().strip("\"'")
    return values, metadata


def skill_files() -> list[Path]:
    return sorted(REPO_ROOT.glob("plugins/*/skills/*/SKILL.md"))


def build() -> dict[str, object]:
    skills = []
    for path in skill_files():
        values, metadata = frontmatter(path)
        skills.append(
            {
                "name": values.get("name", path.parent.name),
                "description": values.get("description", ""),
                "path": path.parent.relative_to(REPO_ROOT).as_posix(),
                "owner": metadata.get("owner", ""),
                "family": metadata.get("family", ""),
                "maturity": metadata.get("maturity", ""),
                "distribution": metadata.get("distribution", ""),
            }
        )
    return {"schemaVersion": 1, "skills": skills}


def main() -> None:
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT.write_text(json.dumps(build(), indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(f"Wrote {OUTPUT.relative_to(REPO_ROOT)}")


if __name__ == "__main__":
    main()
