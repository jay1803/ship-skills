# Dev / Technical Review Boundary Contract

Contract version: `3` (stateless Review)

This is the canonical seam between Develop's delivery lifecycle and independent
technical Review. Review owns this source and Develop carries a byte-identical
package-local mirror.

## Ownership

- Review owns one independent judgment of an exact frozen PR or immutable diff:
  depth selection, reviewer dispatch, verification, the final base/head check
  and any authorized post. It keeps no state between runs.
- Develop owns the issue, plan, branch, code changes, tests, verification, PR
  lifecycle and completion claim, and the whole review loop: the round ledger,
  scope triage of findings, re-review selection, review omission under its mode
  policy, acceptance deferrals, follow-up tickets and the controller disposition
  after exhaustion.
- Review never repairs, tracks rounds, changes tracker state, or merges.
  `$dev-verifier` does not satisfy independent technical Review.

## Request

Dev calls `$review` on the current PR only after verifying PR traceability,
base and dependency identity, and the merge-ready form of generated or
migration artifacts. It supplies the mode, governing requirement and acceptance
sources, required claims, any caller-authorized deferrals with their authority,
and, for a re-review, the prior result's open findings and the repair diff.
A pre-PR diff gives standalone advisory evidence only; it cannot satisfy the
Dev gate or start automatic repair.

## Result

Review returns its result contract: exact target, mode, depth, `Decision`
(`approved`, `comments`, `stale`, `blocked`), common action, `Independence`,
findings with native severity and disposition, coverage gaps, limitations and
posting status. Dev advances only on a current result for the exact head it is
delivering:

- `stale`: reconcile the intended target, then request a new review. No round.
- `blocked` (`coverage-blocked`): obtain the named missing input; never repair
  or approve on partial coverage.
- `comments` with `repair-required`: route the in-scope blockers as one repair
  batch through Develop's review lifecycle.
- `comments` with `advisory`, or `approved`: continue to the remaining gates.
  Advisory items stay visible without another repair loop.

`Independence: not satisfied` does not meet the Dev independent-review gate
unless a Develop policy exception names it. A Review result never substitutes
for Dev verification, CI, Product or Design Review, human acceptance or merge
policy, and applies only to the exact frozen target it names.

## Posting

Posting requires the user's explicit request for GitHub comments or an already
authorized posting action for this exact PR; automatic Skill selection is not
authorization. An immutable-diff review never posts. `$review-pr` owns its
separate structural-comment workflow and is not a Dev gate.

## History

Earlier full Review v2 artifacts, Review Receipt v2 chains and Continuation v1
records remain valid historical evidence with their original labels. New
results are not chained; Develop records them in its own ledger.
