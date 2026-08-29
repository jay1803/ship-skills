#!/usr/bin/env bash

set -euo pipefail

repo_root="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
mode="apply"
targets=()

usage() {
  printf 'Usage: %s [--check] [--target-dir PATH]...\n' "${0##*/}"
}

while [[ $# -gt 0 ]]; do
  case "$1" in
    --check)
      mode="check"
      shift
      ;;
    --target-dir)
      [[ $# -ge 2 ]] || { usage >&2; exit 2; }
      targets+=("$2")
      shift 2
      ;;
    -h|--help)
      usage
      exit 0
      ;;
    *)
      usage >&2
      exit 2
      ;;
  esac
done

if [[ ${#targets[@]} -eq 0 ]]; then
  targets+=("$HOME/.agents/skills" "$HOME/.claude/skills")
fi

skill_dirs=()
while IFS= read -r skill_file; do
  skill_dirs+=("${skill_file%/SKILL.md}")
done < <(find "$repo_root/plugins" -mindepth 4 -maxdepth 4 -name SKILL.md -print)

prepare_target() {
  local target="$1"
  if [[ -L "$target" ]]; then
    local current
    current="$(readlink "$target")"
    if [[ "$current" != "$repo_root" ]]; then
      printf 'Refusing to replace unrelated symlink: %s -> %s\n' "$target" "$current" >&2
      return 1
    fi
    [[ "$mode" == "check" ]] && return 1
    unlink "$target"
  elif [[ -e "$target" && ! -d "$target" ]]; then
    printf 'Target exists and is not a directory: %s\n' "$target" >&2
    return 1
  fi
  [[ "$mode" == "check" ]] || mkdir -p "$target"
}

failures=0
for target in "${targets[@]}"; do
  if ! prepare_target "$target"; then
    failures=$((failures + 1))
    continue
  fi

  for skill_dir in "${skill_dirs[@]}"; do
    name="${skill_dir##*/}"
    destination="$target/$name"
    if [[ -L "$destination" && "$(readlink "$destination")" == "$skill_dir" ]]; then
      continue
    fi
    if [[ -e "$destination" || -L "$destination" ]]; then
      printf 'Refusing to replace existing skill: %s\n' "$destination" >&2
      failures=$((failures + 1))
      continue
    fi
    if [[ "$mode" == "check" ]]; then
      printf 'Missing skill link: %s\n' "$destination" >&2
      failures=$((failures + 1))
    else
      ln -s "$skill_dir" "$destination"
    fi
  done
done

if [[ $failures -ne 0 ]]; then
  exit 1
fi

printf 'Skill links %s successfully.\n' "$mode"
