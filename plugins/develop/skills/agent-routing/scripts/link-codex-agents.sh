#!/usr/bin/env bash

set -euo pipefail

usage() {
  echo "Usage: $0 (--apply | --check) [--target-dir PATH]"
}

mode=""
target_dir="${CODEX_HOME:-$HOME/.codex}/agents"

while [[ $# -gt 0 ]]; do
  case "$1" in
    --apply)
      mode="apply"
      shift
      ;;
    --check)
      mode="check"
      shift
      ;;
    --target-dir)
      if [[ $# -lt 2 || -z "$2" ]]; then
        usage >&2
        exit 2
      fi
      target_dir="$2"
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

if [[ -z "$mode" ]]; then
  usage >&2
  exit 2
fi

if [[ -z "$target_dir" || "$target_dir" == "/" || "$target_dir" == "$HOME" ]]; then
  echo "Refusing unsafe target directory: $target_dir" >&2
  exit 2
fi

script_dir="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd -P)"
source_dir="$(cd "$script_dir/../assets/codex-agents" && pwd -P)"

shopt -s nullglob
profiles=("$source_dir"/*.toml)
shopt -u nullglob

if [[ ${#profiles[@]} -eq 0 ]]; then
  echo "No Codex agent profiles found in $source_dir" >&2
  exit 1
fi

if [[ "$mode" == "apply" ]]; then
  mkdir -p "$target_dir"
fi

status=0
timestamp="$(date +%Y%m%d%H%M%S)"

for source_path in "${profiles[@]}"; do
  profile_name="$(basename "$source_path")"
  target_path="$target_dir/$profile_name"

  if [[ -f "$target_path" ]] && [[ ! -L "$target_path" ]] && cmp -s "$source_path" "$target_path"; then
    echo "current $target_path"
    continue
  fi

  if [[ "$mode" == "check" ]]; then
    if [[ -e "$target_path" || -L "$target_path" ]]; then
      echo "outdated $target_path" >&2
    else
      echo "missing $target_path" >&2
    fi
    status=1
    continue
  fi

  if [[ -e "$target_path" || -L "$target_path" ]]; then
    backup_path="$target_path.backup.$timestamp"
    mv "$target_path" "$backup_path"
    echo "backup  $target_path -> $backup_path"
  fi

  install -m 600 "$source_path" "$target_path"
  echo "copied  $source_path -> $target_path"
done

exit "$status"
