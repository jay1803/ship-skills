#!/usr/bin/env bash

set -euo pipefail

repo_root="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"

for plugin_dir in "$repo_root"/plugins/*; do
  [[ -f "$plugin_dir/package.json" ]] || continue
  npm pack --dry-run --json "$plugin_dir" >/dev/null
done

printf 'Package dry-run checks passed.\n'
