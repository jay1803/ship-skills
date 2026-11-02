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
2. Without an explicit repository policy for the delivery shape, the fallback
   base is the remote `develop` when it exists, otherwise the remote default
   branch:
   - A standalone ticket branches from and targets the fallback base.
   - A batch of tickets, a project, or a parent issue with sub-issues gets one
     temporary integration branch per repository for that delivery scope,
     created from the current fallback base. Ordinary batch children branch from
     and target that branch. A selected native stack keeps it as the trunk;
     upper layers branch from and target their recorded predecessor instead.
   - A child executed alone still inherits its recorded batch branch. Scheduling
     in sequence rather than parallel does not remove batch isolation. Mere
     membership in a tracker project does not expand a standalone ticket request
     into project execution.
3. Persist and pass the resolved strategy through setup, PR writing, merge
   handoff, callbacks, and resumes. Record repository and policy source (or
   fallback), scope/parent identifier, upstream integration branch, issue PR
   base, temporary branch if any, final promotion target, and controller owner.
   For a stack, also record its ordered PR set, trunk, immediate bases, exact
   predecessor heads, branch owners, update/merge executor and dependency gate.
   Reuse a verified existing branch for the same batch instead of creating one
   per child or per wave. A caller's branch must agree with repository policy;
   resolve a conflict before mutation rather than silently retargeting a PR.

## Delivery Shape

Select native stacks for same-repository dependency chains when GitHub support
is verified and repository policy permits intermediate PR bases. Read
[stack integration](stacked-prs.md) before stack setup, admission, updates or
merge. Explicit all-PRs-to-one-base or merge-before-next rules retain their
authority; selecting a stack does not silently waive them. Keep the fallback
batch branch and final promotion target unless policy resolves another shape.

Independent projects or issues keep independent PRs/stacks. Where available and
configured, a merge queue can validate them against the changing shared target;
it requires its own CI support and authorized merge executor. Do not manufacture
dependencies for batching. Cross-repository work uses separate branches/stacks
with controller-owned contract, deployment and release dependencies.

## Batch Lifecycle

The project controller resolves the strategy before worker dispatch. For an
execution request, create and push the temporary branch so child PRs have a
remote base; plan-only records the strategy without creating branches. Follow
repository naming conventions; otherwise an example is
`integration/<parent-or-project-id>`. Verify branch ownership before reuse and
preserve existing local work. A fetch failure, unresolved remote default or
ambiguous existing history needs explicit reconciliation, not an invented
replacement base or reset.

Issue workers apply normal review, CI and applicable acceptance gates to their
recorded PR base. Ordinary children merge into the batch branch. Native stack
layers land together on the recorded trunk through the assigned integration
executor; the immediate upper-layer base is its predecessor branch, not the
landing destination. Callbacks identify both and exact reviewed/merged revisions.
A merge dependency can open on a verified child merge into the batch branch;
selected stack development may use the separate stack-ready gate. Neither
requires promoting the unfinished batch upstream. Preserve
explicit child-level runtime/acceptance requirements. Do not invent a develop
or test deployment mapping for a temporary branch: use a configured preview or
batch environment, or report a required environment gate as pending. Checks
that apply only to the complete batch remain at final promotion.

After every required issue is integrated, the controller assigns a designated
worker `$dev-integration-manager` for combined validation and one aggregate PR from the
temporary branch to the upstream integration branch (fallback base).
The assigned worker reconciles upstream changes and validates the candidate
before promotion; the project controller verifies the returned result and does
not implement, technically review or merge the aggregate PR itself. Apply repository review, CI and merge authority to the aggregate PR;
route repairs to the responsible implementation or CI owner and revalidate changed evidence. Keep a
human-only merge pending for human review. Do not promote a partial batch just
to unblock another feature. Unrelated standalone work can continue on the
upstream base.

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
