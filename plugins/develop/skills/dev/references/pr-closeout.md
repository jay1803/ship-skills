# PR, Review, Repair And Closeout

Read for the pending PR, Review, repair or merge/test boundary. Apply the
selected phase plan and mode contract; do not replay completed preparation.

## Dev-Managed Review Transition Gate

Apply before selected `$review`, repair within an active Review history, and
acceptance of its changed target. Ordinary authorized CI/comment/conflict repair
without a Review Run follows the repair section below; it needs no invented run.

- Start only on the current PR after traceability sync. A pre-PR immutable diff
  is standalone advisory evidence; it cannot create a Dev Run, consume budget,
  trigger automatic Review repair or satisfy this gate.
- Bind readiness to PR/base/head, dependency/stack state and repository-required
  generated/schema/migration/packaging artifacts in merge-ready form. Carry the
  producing decisions' accepted semantic capability tier into judgment routing;
  an incidental runtime model is not that tier. Recover missing provenance.
- Return incomplete preparation to the earliest owner: artifacts to the implementer
  and selected validation gate; missing/stale proof to Test/selected Verifier;
  unresolved stacks to Integration Manager; missing PR to PR Writer. Re-evaluate
  readiness after it returns, without competing preparation writers. Coordinate
  an already scheduled base update before freezing the target.
- Read and validate the Review ledger under the
  [Review lifecycle](review-lifecycle.md#ledger). Preserve current target,
  actual coverage, findings, cumulative rounds and limit authority through
  resumes, splits and base changes. Missing/discontinuous state blocks
  Review-dependent dispatch, mutation or acceptance.
- Repair Review findings only from a current Review result after
  [triage](review-lifecycle.md#triage). Batch in-scope mode blockers, never
  lone specialist output. Route mixed/out-of-scope work through
  [grouped discovery ownership](execution-ownership.md#autonomous-decisions-and-discovered-work).
  Change-caused defects and required acceptance/CI gaps retain their gates.
- Reserve the verification round before repair under the
  [Review budget](review-lifecycle.md#budget); at exhaustion apply the
  lifecycle's [controller disposition](review-lifecycle.md#controller-disposition-after-exhaustion).

## PR And Traceability

Use `$dev-pr-writer` to open or reuse the PR against the
[resolved base](branch-strategy.md). Satisfy repository-defined artifact completion
and remote base availability, or record an explicit stacked dependency. Capture
PR URL/number, branches and exact revisions. PR creation grants no merge authority.

The issue worker verifies related Linear IDs from accepted scope, relationships,
branch/commits and PR metadata. Make each confirmed ID visible in the PR and move
only confirmed related issues to `In Review` or its workspace equivalent. Re-read
exact PR/issue states after writes; reuse complete links and updates. Unavailable
tools leave exact drafts and traceability pending, not a claimed sync or passed
Review prerequisite. Conflicting IDs require scope resolution before status writes.

## Selected Technical Review

When the phase plan selects `$review`, call it after readiness with the current
PR target, dependency/artifact evidence, mode, governing authority and effective
engineering claims. Carry mode-waived surfaces separately with their source and
unverified status, so they do not return as mandatory missing-evidence findings.
Consume the result under the [boundary contract](dev-review-v2-contract.md#result)
and the [Review lifecycle](review-lifecycle.md); no fabricated result satisfies
the selected gate. Retain the result without GitHub posting when that exact
action is unauthorized.

## Scoped Repair

Repair through the current implementation owner, inline by default, under
[repair/capacity recovery](execution-ownership.md#bounded-repair-and-capacity-recovery).
It uses the [PR-repair reference](../../dev-implementer/references/pr-repair.md)
for comments/conflicts; `$dev-ci-repair` owns remaining failing checks. Keep one
writer. Finish comment/conflict repair and focused validation before addressing
checks that remain red.

For a Review-supplied finding batch, apply the transition gate and effective
cumulative ceiling before dispatch or mutation. Send the current result, its
triage and all confirmed in-scope mode blockers as one batch. Count one accepted repaired head
once, even across several coherent commits. An advisory-only result advances
without a repair/review loop. Nonblocking fixes already in accepted scope may
join a required batch; out-of-scope nonblockers stay in the follow-up backlog.

Ordinary authorized CI/comment/conflict repair uses its observed failure and
scope, existing writer, focused validation and owner-specific retry limit; it
needs no Review finding or triage to authorize that distinct repair. When a
Review history exists, validate/preserve its ledger and reserve its verification
round before mutation. When none exists, record Review state as `not applicable`.
Do not invent a run or introduce technical Review solely for another head.
A new protected boundary or selected trigger still returns to phase selection.

Before any repair that expands product behavior, contracts, persistent models,
migration/ownership or cross-repository scope, obtain the requester's decision
or the planner's assessment. Preserve mode severity and mandatory
acceptance/CI requirements. After each fix commit, refresh affected validation. Reuse proven unaffected
checks under Test's evidence rules; rerun a selected Verifier when its proof is
invalidated. New risk may select it, but another head alone does not.

When Review is selected or active, request the next review under the
lifecycle's [re-review rules](review-lifecycle.md#requesting-review) and accept
only a current result after its final live-target check. Otherwise continue to
the next selected gate without a fabricated Review.

## Requirement Conformance And Merge/Test Handoff

Requirement conformance comes from the verifier's claim ledger and Review's
requirement coverage; no Product review is a Dev stage or merge input. Run
`$pm-pr-product-review` only when the requester asks for it; its result is
advisory and never holds merge or restarts a Review count.

Execute [`$dev-merge-handoff`](../../dev-merge-handoff/SKILL.md) at the authorized
closeout boundary, including an already merged PR. Pass mode, current gate results
and omissions. A selected native stack uses the
[stack checkpoint](stacked-prs.md): return stack-ready evidence to the controller,
retain the worker/branch and wait for its assigned landing executor. This is
pending delivery, not tracker closeout; resume post-landing handoff on this same
issue after live merge verification. It owns final merge gates, eligible resolved-base merge,
branch/worktree cleanup, test handoff, release-candidate/rollback evidence and
tracker closeout. Accept its cleanup evidence before full lifecycle completion;
a merge command alone is insufficient. Apply mode waivers to environment/human
waits while retaining remaining enforced or explicitly authorized gates.
