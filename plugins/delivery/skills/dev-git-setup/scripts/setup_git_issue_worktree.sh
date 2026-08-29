#!/usr/bin/env bash
set -euo pipefail

usage() {
  cat <<'EOF'
Usage:
  setup_git_issue_worktree.sh [options] <feature|fix> <ISSUE_ID> [WORKTREE_PATH]
  setup_git_issue_worktree.sh [options] <feature/ISSUE_ID|fix/ISSUE_ID> [WORKTREE_PATH]

Options:
  --remote NAME        Remote to fetch from. Default: origin
  --main NAME          Main branch name. Default: main
  --develop NAME       Develop branch name. Default: develop
  --path PATH          Worktree path. Default: sibling '<repo>-<ISSUE_ID>'
  --reuse-existing     Reuse an existing issue branch or worktree instead of failing
  -h, --help           Show this help
EOF
}

die() {
  printf 'error: %s\n' "$*" >&2
  exit 1
}

log() {
  printf '%s\n' "$*" >&2
}

run() {
  log "+ $*"
  "$@"
}

local_branch_exists() {
  git show-ref --verify --quiet "refs/heads/$1"
}

remote_branch_exists() {
  git show-ref --verify --quiet "refs/remotes/$remote/$1"
}

require_clean_worktree() {
  if ! git diff --quiet || ! git diff --cached --quiet || [[ -n "$(git ls-files --others --exclude-standard)" ]]; then
    git status --short >&2
    die "working tree must be clean before worktree setup"
  fi
}

sync_branch() {
  local branch="$1"

  if remote_branch_exists "$branch"; then
    if local_branch_exists "$branch"; then
      run git switch "$branch"
      run git merge --ff-only "$remote/$branch"
    else
      run git switch --track -c "$branch" "$remote/$branch"
    fi
    return
  fi

  if local_branch_exists "$branch"; then
    run git switch "$branch"
    return
  fi

  die "branch '$branch' does not exist locally or at '$remote/$branch'"
}

branch_worktree_path() {
  local target_branch="$1"
  local current_path=""
  local current_branch=""

  while IFS= read -r line || [[ -n "$line" ]]; do
    if [[ -z "$line" ]]; then
      if [[ "$current_branch" == "refs/heads/$target_branch" ]]; then
        printf '%s\n' "$current_path"
        return 0
      fi
      current_path=""
      current_branch=""
    elif [[ "$line" == worktree\ * ]]; then
      current_path="${line#worktree }"
    elif [[ "$line" == branch\ * ]]; then
      current_branch="${line#branch }"
    fi
  done < <(git worktree list --porcelain)

  if [[ "$current_branch" == "refs/heads/$target_branch" ]]; then
    printf '%s\n' "$current_path"
    return 0
  fi

  return 1
}

path_is_empty_or_absent() {
  local path="$1"

  if [[ ! -e "$path" ]]; then
    return 0
  fi

  if [[ ! -d "$path" ]]; then
    return 1
  fi

  [[ -z "$(find "$path" -mindepth 1 -maxdepth 1 -print -quit)" ]]
}

default_worktree_path() {
  local repo_root="$1"
  local issue_id="$2"
  local repo_name
  local parent_dir
  local safe_issue_id

  repo_name="$(basename "$repo_root")"
  parent_dir="$(dirname "$repo_root")"
  safe_issue_id="$(printf '%s' "$issue_id" | tr '/[:space:]' '--' | tr -c 'A-Za-z0-9._-' '-')"
  printf '%s/%s-%s\n' "$parent_dir" "$repo_name" "$safe_issue_id"
}

absolute_path_from_initial_cwd() {
  local path="$1"

  if [[ "$path" = /* ]]; then
    printf '%s\n' "$path"
  else
    printf '%s/%s\n' "$initial_cwd" "$path"
  fi
}

set_positional_worktree_path() {
  local path="$1"

  if [[ -n "$provided_worktree_path" ]]; then
    die "worktree path specified both with --path and a positional argument"
  fi

  provided_worktree_path="$path"
}

remote="origin"
main_branch="main"
develop_branch="develop"
reuse_existing=0
provided_worktree_path=""
positionals=()
initial_cwd="$(pwd -P)"

while [[ $# -gt 0 ]]; do
  case "$1" in
    --remote)
      [[ $# -ge 2 ]] || die "--remote requires a value"
      remote="$2"
      shift 2
      ;;
    --main)
      [[ $# -ge 2 ]] || die "--main requires a value"
      main_branch="$2"
      shift 2
      ;;
    --develop)
      [[ $# -ge 2 ]] || die "--develop requires a value"
      develop_branch="$2"
      shift 2
      ;;
    --path)
      [[ $# -ge 2 ]] || die "--path requires a value"
      provided_worktree_path="$2"
      shift 2
      ;;
    --reuse-existing)
      reuse_existing=1
      shift
      ;;
    -h|--help)
      usage
      exit 0
      ;;
    --)
      shift
      while [[ $# -gt 0 ]]; do
        positionals+=("$1")
        shift
      done
      ;;
    -*)
      die "unknown option '$1'"
      ;;
    *)
      positionals+=("$1")
      shift
      ;;
  esac
done

if [[ ${#positionals[@]} -eq 1 && "${positionals[0]}" == */* ]]; then
  branch_name="${positionals[0]}"
  branch_type="${branch_name%%/*}"
  issue_id="${branch_name#*/}"
elif [[ ${#positionals[@]} -eq 2 && "${positionals[0]}" == */* ]]; then
  branch_name="${positionals[0]}"
  branch_type="${branch_name%%/*}"
  issue_id="${branch_name#*/}"
  set_positional_worktree_path "${positionals[1]}"
elif [[ ${#positionals[@]} -eq 2 ]]; then
  branch_type="${positionals[0]}"
  issue_id="${positionals[1]}"
  branch_name="${branch_type}/${issue_id}"
elif [[ ${#positionals[@]} -eq 3 ]]; then
  branch_type="${positionals[0]}"
  issue_id="${positionals[1]}"
  branch_name="${branch_type}/${issue_id}"
  set_positional_worktree_path "${positionals[2]}"
else
  usage >&2
  exit 2
fi

case "$branch_type" in
  feature|fix) ;;
  *) die "branch type must be 'feature' or 'fix'" ;;
esac

[[ -n "$issue_id" ]] || die "issue id is required"
git check-ref-format --branch "$branch_name" >/dev/null || die "invalid branch name '$branch_name'"

repo_root="$(git rev-parse --show-toplevel 2>/dev/null)" || die "not inside a Git repository"
cd "$repo_root"

require_clean_worktree

if [[ -n "$provided_worktree_path" ]]; then
  worktree_path="$(absolute_path_from_initial_cwd "$provided_worktree_path")"
else
  worktree_path="$(default_worktree_path "$repo_root" "$issue_id")"
fi

if git remote get-url "$remote" >/dev/null 2>&1; then
  run git fetch --prune "$remote"
else
  log "remote '$remote' not found; using local branches only"
fi

sync_branch "$main_branch"
sync_branch "$develop_branch"

if git merge-base --is-ancestor "$main_branch" "$develop_branch"; then
  log "'$develop_branch' contains '$main_branch'"
else
  log "'$develop_branch' does not contain '$main_branch'; recreating '$develop_branch' from '$main_branch'"

  unique_count="$(git rev-list --count "${main_branch}..${develop_branch}")"
  if [[ "$unique_count" != "0" ]]; then
    backup_branch="${develop_branch}-backup-$(date +%Y%m%d%H%M%S)"
    run git branch "$backup_branch" "$develop_branch"
    log "preserved previous '$develop_branch' as '$backup_branch'"
  fi

  run git switch "$main_branch"
  run git branch -D "$develop_branch"
  run git switch -c "$develop_branch" "$main_branch"
fi

existing_worktree_path="$(branch_worktree_path "$branch_name" || true)"
if [[ -n "$existing_worktree_path" ]]; then
  if [[ "$reuse_existing" == "1" ]]; then
    log "ready in existing worktree '$existing_worktree_path' on branch '$branch_name'"
    exit 0
  fi
  die "branch '$branch_name' is already checked out at '$existing_worktree_path'; pass --reuse-existing to use it"
fi

if ! path_is_empty_or_absent "$worktree_path"; then
  die "worktree path '$worktree_path' already exists and is not empty"
fi

if local_branch_exists "$branch_name"; then
  if [[ "$reuse_existing" == "1" ]]; then
    run git worktree add "$worktree_path" "$branch_name"
    log "ready in new worktree '$worktree_path' on existing branch '$branch_name'"
    exit 0
  fi
  die "branch '$branch_name' already exists locally; pass --reuse-existing to create a worktree for it"
fi

if remote_branch_exists "$branch_name"; then
  if [[ "$reuse_existing" == "1" ]]; then
    run git worktree add -b "$branch_name" "$worktree_path" "$remote/$branch_name"
    run git -C "$worktree_path" branch --set-upstream-to "$remote/$branch_name" "$branch_name"
    log "ready in new worktree '$worktree_path' on existing remote branch '$branch_name'"
    exit 0
  fi
  die "branch '$branch_name' already exists at '$remote/$branch_name'; pass --reuse-existing to track it"
fi

run git switch "$develop_branch"
run git worktree add -b "$branch_name" "$worktree_path" "$develop_branch"
log "ready in new worktree '$worktree_path' on branch '$branch_name'"
