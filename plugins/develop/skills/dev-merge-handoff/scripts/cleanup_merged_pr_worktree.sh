#!/usr/bin/env bash
set -euo pipefail

usage() {
  cat <<'EOF'
Usage:
  cleanup_merged_pr_worktree.sh --confirmed-merged --branch BRANCH [options]

Options:
  --branch NAME          PR head branch to clean up. Required.
  --base NAME            Base branch to switch to if the head branch is current.
  --worktree PATH        Known issue worktree path. If omitted, infer from branch.
  --remote NAME          Remote to inspect/delete from. Default: origin.
  --delete-remote        Delete the remote branch if it still exists.
  --squash-merged        Allow local branch force-delete after confirmed squash merge.
  --confirmed-merged     Required acknowledgement that the PR is merged.
  -h, --help             Show this help.

Stdout reports the remote head as key=value lines: remote_branch (deleted,
already_absent, retained or not_applicable), remote_branch_reason and
remote_branch_evidence. Deletion is refused, and the head retained, unless the
remote's deletion rules positively allow it.
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

# Prints present, absent or unknown. ls-remote exits 2 only for a missing ref;
# any other failure leaves the remote head unverified.
remote_branch_state() {
  local status=0
  git ls-remote --exit-code --heads "$remote" "$1" >/dev/null 2>&1 || status=$?
  case "$status" in
    0) printf 'present\n' ;;
    2) printf 'absent\n' ;;
    *) printf 'unknown\n' ;;
  esac
}

# Sets remote_host, remote_owner and remote_repo for scp-like, URL and
# hostname-with-port remotes. Returns 1 unless the path is exactly owner/repo.
parse_remote_slug() {
  local rest="$1" path
  case "$rest" in
    *://*) rest="${rest#*://}" ;;
    *:*) rest="${rest%%:*}/${rest#*:}" ;;
    *) return 1 ;;
  esac
  remote_host="${rest%%/*}"
  remote_host="${remote_host##*@}"
  remote_host="${remote_host%%:*}"
  path="${rest#*/}"
  path="${path%.git}"
  path="${path%/}"
  remote_owner="${path%%/*}"
  remote_repo="${path#*/}"
  [[ -n "$remote_host" && -n "$remote_owner" && -n "$remote_repo" && "$path" == */* && "$remote_repo" != */* ]]
}

# Sets guard_decision, guard_reason and guard_evidence for the exact remote
# head. Returns 0 only when deletion is proven allowed; every other outcome,
# including a failed or unavailable query, retains the head.
remote_deletion_decision() {
  local remote_url push_url encoded_branch tmp_dir err_file classified
  remote_url="$(git config --get "remote.$remote.url" || true)"
  push_url="$(git remote get-url --push "$remote" 2>/dev/null || true)"
  if [[ "$push_url" != "$remote_url" ]]; then
    guard_decision=retained
    guard_reason="push URL differs from the configured URL (pushurl or insteadOf rewrite); the deletion target cannot be verified"
    guard_evidence="remote=$remote push target not verified"
    return 1
  fi
  if ! parse_remote_slug "$remote_url"; then
    guard_decision=retained
    guard_reason="remote '$remote' URL does not name an owner/repo; deletion rules cannot be verified"
    guard_evidence="remote=$remote URL not recorded"
    return 1
  fi

  tmp_dir="$(mktemp -d)"
  err_file="$tmp_dir/err"
  encoded_branch="$(python3 -c 'import sys, urllib.parse; print(urllib.parse.quote(sys.argv[1], safe="/"))' "$branch" 2>/dev/null)" || encoded_branch=""
  guard_evidence="host=$remote_host repo=$remote_owner/$remote_repo branch=$branch"

  if [[ -z "$encoded_branch" ]]; then
    guard_decision=retained
    guard_reason="could not encode branch name for the rules query"
  elif ! gh api --hostname "$remote_host" --paginate "repos/$remote_owner/$remote_repo/rules/branches/$encoded_branch" \
      >"$tmp_dir/rules.json" 2>"$err_file"; then
    guard_decision=retained
    guard_reason="deletion rules query failed: $(tr '\n' ' ' <"$err_file")"
  elif gh api --hostname "$remote_host" "repos/$remote_owner/$remote_repo/branches/$encoded_branch/protection" \
      >"$tmp_dir/protection.json" 2>"$err_file" || grep -q 'Branch not protected' "$err_file"; then
    # An unprotected branch has an empty protection file, which the classifier reads as no classic rule.
    classified="$(python3 "$classifier" "$tmp_dir/rules.json" "$tmp_dir/protection.json" 2>/dev/null)" || classified=$'retained\tdeletion rules classifier failed\t'
    IFS=$'\t' read -r guard_decision guard_reason guard_evidence_rules <<<"$classified"
    guard_evidence="$guard_evidence; $guard_evidence_rules"
  else
    guard_decision=retained
    guard_reason="classic branch protection query failed: $(tr '\n' ' ' <"$err_file")"
  fi

  rm -rf "$tmp_dir"
  [[ "$guard_decision" == allowed ]]
}

clean_worktree() {
  local path="$1"
  git -C "$path" diff --quiet &&
    git -C "$path" diff --cached --quiet &&
    [[ -z "$(git -C "$path" ls-files --others --exclude-standard)" ]]
}

absolute_path() {
  local path="$1"
  if [[ "$path" = /* ]]; then
    printf '%s\n' "$path"
  else
    printf '%s/%s\n' "$initial_cwd" "$path"
  fi
}

canonical_path() {
  local path="$1"
  (cd "$path" && pwd -P)
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

first_non_target_worktree() {
  local target="$1"
  local current_path=""

  while IFS= read -r line || [[ -n "$line" ]]; do
    if [[ -z "$line" ]]; then
      if [[ -n "$current_path" && "$(canonical_path "$current_path")" != "$target" ]]; then
        printf '%s\n' "$current_path"
        return 0
      fi
      current_path=""
    elif [[ "$line" == worktree\ * ]]; then
      current_path="${line#worktree }"
    fi
  done < <(git worktree list --porcelain)

  if [[ -n "$current_path" && "$(canonical_path "$current_path")" != "$target" ]]; then
    printf '%s\n' "$current_path"
    return 0
  fi

  return 1
}

first_worktree_path() {
  local line

  while IFS= read -r line || [[ -n "$line" ]]; do
    if [[ "$line" == worktree\ * ]]; then
      printf '%s\n' "${line#worktree }"
      return 0
    fi
  done < <(git worktree list --porcelain)

  return 1
}

branch=""
base_branch=""
provided_worktree=""
remote="origin"
delete_remote=0
squash_merged=0
confirmed_merged=0
initial_cwd="$(pwd -P)"
classifier="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd -P)/classify_branch_deletion.py"
remote_outcome="not_applicable"
remote_reason=""
remote_evidence=""

while [[ $# -gt 0 ]]; do
  case "$1" in
    --branch)
      [[ $# -ge 2 ]] || die "--branch requires a value"
      branch="$2"
      shift 2
      ;;
    --base)
      [[ $# -ge 2 ]] || die "--base requires a value"
      base_branch="$2"
      shift 2
      ;;
    --worktree)
      [[ $# -ge 2 ]] || die "--worktree requires a value"
      provided_worktree="$2"
      shift 2
      ;;
    --remote)
      [[ $# -ge 2 ]] || die "--remote requires a value"
      remote="$2"
      shift 2
      ;;
    --delete-remote)
      delete_remote=1
      shift
      ;;
    --squash-merged)
      squash_merged=1
      shift
      ;;
    --confirmed-merged)
      confirmed_merged=1
      shift
      ;;
    -h|--help)
      usage
      exit 0
      ;;
    *)
      die "unknown argument '$1'"
      ;;
  esac
done

[[ "$confirmed_merged" == "1" ]] || die "--confirmed-merged is required before deleting branch/worktree state"
[[ -n "$branch" ]] || die "--branch is required"
git check-ref-format --branch "$branch" >/dev/null || die "invalid branch name '$branch'"

case "$branch" in
  main|master|develop|trunk)
    die "refusing to clean protected branch '$branch'"
    ;;
esac

repo_root="$(git rev-parse --show-toplevel 2>/dev/null)" || die "not inside a Git repository"
cd "$repo_root"

target_worktree=""
if [[ -n "$provided_worktree" ]]; then
  provided_abs="$(absolute_path "$provided_worktree")"
  if [[ -d "$provided_abs" ]]; then
    target_worktree="$(canonical_path "$provided_abs")"
  else
    log "worktree path '$provided_abs' is already absent"
  fi
else
  inferred_path="$(branch_worktree_path "$branch" || true)"
  if [[ -n "$inferred_path" ]]; then
    target_worktree="$(canonical_path "$inferred_path")"
  fi
fi

if [[ -n "$target_worktree" ]]; then
  primary_worktree="$(canonical_path "$(first_worktree_path)")"
  if [[ "$target_worktree" == "$primary_worktree" ]]; then
    if [[ -n "$provided_worktree" ]]; then
      die "refusing to remove primary worktree '$target_worktree'"
    fi
    log "branch '$branch' is checked out in the primary worktree; will switch branches instead of removing the worktree"
    target_worktree=""
  fi
fi

if [[ -n "$target_worktree" ]]; then
  if ! clean_worktree "$target_worktree"; then
    git -C "$target_worktree" status --short >&2
    die "worktree '$target_worktree' is not clean; refusing to remove it"
  fi

  controller="$(first_non_target_worktree "$target_worktree" || true)"
  [[ -n "$controller" ]] || die "no alternate worktree is available to remove '$target_worktree'"
  run git -C "$controller" worktree remove "$target_worktree"
  cd "$controller"
fi

run git worktree prune

checked_out_path="$(branch_worktree_path "$branch" || true)"
if [[ -n "$checked_out_path" ]]; then
  checked_out_path="$(canonical_path "$checked_out_path")"
  current_root="$(canonical_path "$(git rev-parse --show-toplevel)")"

  if [[ "$checked_out_path" == "$current_root" && -n "$base_branch" ]]; then
    clean_worktree "$current_root" || die "current worktree is dirty; cannot switch from '$branch' to '$base_branch'"
    run git switch "$base_branch"
  else
    die "branch '$branch' is still checked out at '$checked_out_path'"
  fi
fi

if local_branch_exists "$branch"; then
  branch_delete_log="$(mktemp)"
  if git branch -d "$branch" >"$branch_delete_log" 2>&1; then
    cat "$branch_delete_log" >&2
    rm -f "$branch_delete_log"
    log "deleted local branch '$branch'"
  elif [[ "$squash_merged" == "1" ]]; then
    rm -f "$branch_delete_log"
    run git branch -D "$branch" >&2
    log "force-deleted local branch '$branch' after confirmed squash merge"
  else
    cat "$branch_delete_log" >&2
    rm -f "$branch_delete_log"
    die "local branch '$branch' is not merged; pass --squash-merged only after verifying squash merge"
  fi
else
  log "local branch '$branch' is already absent"
fi

if git remote get-url "$remote" >/dev/null 2>&1; then
  run git fetch --prune "$remote"
  remote_state="$(remote_branch_state "$branch")"
  case "$remote_state" in
    absent)
      remote_outcome="already_absent"
      log "remote branch '$remote/$branch' is absent"
      ;;
    unknown)
      remote_outcome="retained"
      remote_reason="remote head state could not be verified"
      log "remote branch '$remote/$branch' retained: $remote_reason"
      ;;
    present)
      if [[ "$delete_remote" != "1" ]]; then
        remote_outcome="retained"
        remote_reason="--delete-remote not requested"
        log "remote branch '$remote/$branch' still exists; rerun with --delete-remote if the merged PR should remove it"
      elif remote_deletion_decision; then
        remote_evidence="$guard_evidence"
        if run git push "$remote" --delete "$branch"; then
          case "$(remote_branch_state "$branch")" in
            absent)
              remote_outcome="deleted"
              log "deleted remote branch '$remote/$branch'"
              ;;
            present)
              remote_outcome="retained"
              remote_reason="git push --delete did not remove the remote head"
              log "remote branch '$remote/$branch' retained: $remote_reason"
              ;;
            *)
              remote_outcome="retained"
              remote_reason="remote head state could not be verified after git push --delete"
              log "remote branch '$remote/$branch' retained: $remote_reason"
              ;;
          esac
        else
          remote_outcome="retained"
          remote_reason="git push --delete failed"
          log "remote branch '$remote/$branch' retained: $remote_reason"
        fi
      else
        remote_outcome="retained"
        remote_reason="$guard_reason"
        remote_evidence="$guard_evidence"
        log "remote branch '$remote/$branch' retained: $remote_reason"
      fi
      ;;
  esac
else
  remote_reason="remote '$remote' not found"
  log "$remote_reason; skipped remote branch cleanup"
fi

log "cleanup complete for '$branch'"

# Machine-readable remote outcome for callers. Local cleanup above is never
# gated on it; a retained remote head is reported, not treated as a failure.
printf 'remote_branch=%s\n' "$remote_outcome"
printf 'remote_branch_reason=%s\n' "$remote_reason"
printf 'remote_branch_evidence=%s\n' "$remote_evidence"
