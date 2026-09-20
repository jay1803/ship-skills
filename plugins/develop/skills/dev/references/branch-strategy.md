# Branch Strategy Contract

Read before choosing a branch base, creating a PR, accepting a merge, or
scheduling issue workers. This is the canonical Develop branch-selection rule.

## Precedence And Scope

1. Follow explicit repository branch policy first, including its integration,
   release, merge-authority, and naming rules. Read AGENTS.md and its linked
   branch/release guidance. A branch merely existing or being the hosting
   default is not an explicit policy. Apply fallback defaults only to decisions
   the repository leaves unspecified; never impose a develop branch on a
   repository that explicitly sends issue PRs to main or another branch.
2. Without an explicit repository policy for the delivery shape:
   - A standalone ticket branches from and targets `develop`.
   - A batch of tickets, a project, or a parent issue with sub-issues gets one
     temporary integration branch per repository for that delivery scope,
     created from the current `develop`. Each issue branches from the latest
     batch branch and opens its PR against that same batch branch.
   - A child executed alone still inherits its recorded batch branch. Scheduling
     in sequence rather than parallel does not remove batch isolation. Mere
     membership in a tracker project does not expand a standalone ticket request
     into project execution.
3. Persist and pass the resolved strategy through setup, PR writing, merge
   handoff, callbacks, and resumes. Record repository and policy source (or
   fallback), scope/parent identifier, upstream integration branch, issue PR
   base, temporary branch if any, final promotion target, and controller owner.
   Reuse a verified existing branch for the same batch instead of creating one
   per child or per wave. A caller's branch must agree with repository policy;
   resolve a conflict before mutation rather than silently retargeting a PR.

## Batch Lifecycle

The project controller resolves the strategy before worker dispatch. For an
execution request, create and push the temporary branch so child PRs have a
remote base; plan-only records the strategy without creating branches. Follow
repository naming conventions; otherwise an example is
`integration/<parent-or-project-id>`. Verify branch ownership before reuse and
preserve existing local work. Missing develop, fetch failure, or ambiguous
existing history needs explicit reconciliation, not an invented replacement
base or reset.

Issue workers merge only into their recorded PR base, with normal review, CI,
and applicable acceptance gates. Callbacks identify that base and exact merge
commit. A dependency barrier can open on a verified child merge into the batch
branch; it does not require promoting the unfinished batch to develop. Preserve
explicit child-level runtime/acceptance requirements. Do not invent a develop
or test deployment mapping for a temporary branch: use a configured preview or
batch environment, or report a required environment gate as pending. Checks
that apply only to the complete batch remain at final promotion.

After every required issue is integrated, the controller uses
`$dev-integration-manager` for combined validation and one aggregate PR from the
temporary branch to the upstream integration branch (fallback: `develop`).
Reconcile current upstream changes and validate the resulting candidate before
promotion. Apply repository review, CI and merge authority to the aggregate PR;
route repairs to the responsible implementation or CI owner and revalidate changed evidence. Keep a
human-only merge pending for human review. Do not promote a partial batch just
to unblock another feature. Unrelated standalone work can continue to develop.

Keep child completion, batch promotion, and production release distinct. Report
child integration separately from any still-pending acceptance/tracker gate;
do not close the parent/project merely because its children merged into the
batch branch. Batch execution completes after verified aggregate merge and
applicable final handoff gates. Preserve the temporary branch through all child
cleanup and until aggregate merge is verified and no active worker or remaining
PR depends on it. Production publication remains a separate authorized release.

## Production Boundary

Classify promotion from repository policy and PR purpose, not the literal name
`main`. A repository that explicitly targets ordinary issue PRs to main keeps
that issue workflow and its human-review rules. A production-promotion PR goes
to `$release`; fallback defaults never authorize production merge or deployment.
