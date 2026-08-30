#!/usr/bin/env python3

from __future__ import annotations

import json
import re
import sys
from pathlib import Path

from build_catalog import REPO_ROOT, build, frontmatter, skill_files


REQUIRED_METADATA = {"owner", "family", "maturity", "distribution"}

# Add machine-specific absolute paths here if they ever leak into a committed
# skill file, so `npm run check` catches them before they ship.
FORBIDDEN_PATHS: set[str] = set()


def main() -> int:
    errors: list[str] = []
    names: dict[str, Path] = {}

    for path in skill_files():
        values, metadata = frontmatter(path)
        name = values.get("name", "")
        if name != path.parent.name:
            errors.append(f"Skill name mismatch: {path} declares {name!r}")
        missing = REQUIRED_METADATA - metadata.keys()
        if missing:
            errors.append(f"Missing metadata {sorted(missing)}: {path}")
        if name in names:
            errors.append(f"Duplicate active skill name {name}: {names[name]} and {path}")
        else:
            names[name] = path

    catalog_path = REPO_ROOT / "catalog" / "skills.json"
    expected_catalog = build()
    if not catalog_path.is_file():
        errors.append("catalog/skills.json is missing")
    else:
        actual_catalog = json.loads(catalog_path.read_text(encoding="utf-8"))
        if actual_catalog != expected_catalog:
            errors.append("catalog/skills.json is stale; run npm run catalog")

    marketplace_path = REPO_ROOT / ".agents" / "plugins" / "marketplace.json"
    marketplace = json.loads(marketplace_path.read_text(encoding="utf-8"))
    entries = {entry["name"]: entry for entry in marketplace.get("plugins", [])}

    for plugin_dir in sorted((REPO_ROOT / "plugins").iterdir()):
        manifest_path = plugin_dir / ".codex-plugin" / "plugin.json"
        package_path = plugin_dir / "package.json"
        manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
        package = json.loads(package_path.read_text(encoding="utf-8"))
        if manifest.get("name") != plugin_dir.name:
            errors.append(f"Plugin name mismatch: {manifest_path}")
        if manifest.get("version") != package.get("version"):
            errors.append(f"Plugin/package version mismatch: {plugin_dir.name}")
        if not re.fullmatch(r"\d+\.\d+\.\d+", manifest.get("version", "")):
            errors.append(f"Plugin version is not strict semver: {plugin_dir.name}")
        if not list((plugin_dir / "skills").glob("*/SKILL.md")):
            errors.append(f"Plugin has no skills: {plugin_dir.name}")
        entry = entries.get(plugin_dir.name)
        if not entry:
            errors.append(f"Marketplace entry missing: {plugin_dir.name}")
        elif entry.get("source", {}).get("path") != f"./plugins/{plugin_dir.name}":
            errors.append(f"Marketplace path mismatch: {plugin_dir.name}")

    text_suffixes = {".md", ".py", ".sh", ".json", ".yaml", ".yml", ".toml"}
    for root_name in ("plugins", "scripts", "wiki"):
        for path in (REPO_ROOT / root_name).rglob("*"):
            if not path.is_file() or path.suffix not in text_suffixes:
                continue
            if path.resolve() == Path(__file__).resolve():
                continue
            try:
                text = path.read_text(encoding="utf-8")
            except UnicodeDecodeError:
                continue
            for forbidden in FORBIDDEN_PATHS:
                if forbidden in text:
                    errors.append(f"Non-portable path {forbidden!r}: {path}")

    if list(REPO_ROOT.glob("*/SKILL.md")):
        errors.append("Active skills must live under plugins/*/skills")

    if errors:
        for error in errors:
            print(f"ERROR: {error}", file=sys.stderr)
        return 1

    print(f"Repository validation passed for {len(names)} active skills and {len(entries)} plugins.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
