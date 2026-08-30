#!/usr/bin/env bash
set -euo pipefail

usage() {
  cat <<'EOF'
Usage:
  setup_git_issue_branch.sh [options] <feature|fix> <ISSUE_ID>
  setup_git_issue_branch.sh [options] <feature/ISSUE_ID|fix/ISSUE_ID>

Options:
  --remote NAME        Remote to fetch from. Default: origin
  --main NAME          Main branch name. Default: main
  --develop NAME       Develop branch name. Default: develop
  --reuse-existing     Switch to an existing issue branch instead of failing
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
    die "working tree must be clean before branch setup"
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

remote="origin"
main_branch="main"
develop_branch="develop"
reuse_existing=0
positionals=()

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
elif [[ ${#positionals[@]} -eq 2 ]]; then
  branch_type="${positionals[0]}"
  issue_id="${positionals[1]}"
  branch_name="${branch_type}/${issue_id}"
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

if local_branch_exists "$branch_name"; then
  if [[ "$reuse_existing" == "1" ]]; then
    run git switch "$branch_name"
    log "ready on existing branch '$branch_name'"
    exit 0
  fi
  die "branch '$branch_name' already exists locally; pass --reuse-existing to switch to it"
fi

if remote_branch_exists "$branch_name"; then
  if [[ "$reuse_existing" == "1" ]]; then
    run git switch --track -c "$branch_name" "$remote/$branch_name"
    log "ready on existing remote branch '$branch_name'"
    exit 0
  fi
  die "branch '$branch_name' already exists at '$remote/$branch_name'; pass --reuse-existing to track it"
fi

run git switch "$develop_branch"
run git switch -c "$branch_name"
log "ready on new branch '$branch_name'"
