#!/usr/bin/env bash

set -euo pipefail

usage() {
  echo "Usage: $0 (--apply | --check) [--target-dir PATH]"
}

mode=""
target_dir="${CODEX_HOME:-$HOME/.codex}"

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
source_path="$script_dir/../assets/codex-profiles/deepseekv41flash.config.toml"
target_path="$target_dir/deepseekv41flash.config.toml"

if [[ ! -f "$source_path" ]]; then
  echo "Missing Codex profile: $source_path" >&2
  exit 1
fi

if [[ -f "$target_path" ]] && [[ ! -L "$target_path" ]] && cmp -s "$source_path" "$target_path"; then
  echo "current $target_path"
  exit 0
fi

if [[ "$mode" == "check" ]]; then
  if [[ -e "$target_path" || -L "$target_path" ]]; then
    echo "outdated $target_path" >&2
  else
    echo "missing $target_path" >&2
  fi
  exit 1
fi

mkdir -p "$target_dir"
if [[ -e "$target_path" || -L "$target_path" ]]; then
  backup_path="$target_path.backup.$(date +%Y%m%d%H%M%S)"
  mv "$target_path" "$backup_path"
  echo "backup  $target_path -> $backup_path"
fi

install -m 600 "$source_path" "$target_path"
echo "copied  $source_path -> $target_path"
