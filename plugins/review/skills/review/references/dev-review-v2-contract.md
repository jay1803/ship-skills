# Dev / Technical Review Boundary Contract

Contract version: `2`

This is the canonical contract for the seam between implementation-owned
verification and independent technical review. Review owns this source and
Develop carries a byte-identical package-local mirror.

## Adopted Surface

Review exposes these authoritative entrypoints:

- `$review` freezes the target, runs isolated review lenses, invokes the judge,
  owns the final current-base/head check, and owns final posting within a Review v2 run;
- `$review-spec` compares the frozen implementation with a governing product
  contract;
- `$review-correctness` finds high-confidence behavioral defects in the frozen
  change;
- `$review-code-quality` finds material maintainability risks and bounded
  simplifications in the frozen change;
- `$review-judge` validates source artifacts and proposes the combined decision.

The three core lenses are exactly specification compliance, correctness, and
code quality. Their semantic and finding contracts remain authoritative; this
contract changes orchestration, not what those specialists judge.

Dev callers use `$review` directly. Product Review remains
owned by Product and Design Review remains owned by Design.

Effective Dev modes are `fast`, `standard`, and `strict`; preserve the mode
through new handoffs. Standard blocks confirmed P0/P1; strict blocks P0/P1/P2.
Named validation and mandatory acceptance requirements remain independent gates. Every new selected Review uses the thermo-nuclear code-quality
rubric. Historical envelopes retain their original mode and lens labels.

## Lifecycle Ownership

- Dev owns the issue, implementation plan, branch/worktree, code mutations,
  tests, self-verification, repair sequencing, PR lifecycle, and completion
  claim.
- Review owns independent observation and judgment of an exact GitHub PR or an
  explicit immutable repository diff.
- `$review` owns target freezing, shared run state, fan-out, source-artifact
  collection, judge invocation, the final current-base/head check, and any
  authorized final GitHub post.
- Specialists, conditional reviewers, `$review-judge`, and
  an immutable-diff run never post a final GitHub result.
- Review does not own implementation fixes, tracker state, merge state,
  product acceptance, design acceptance, or release acceptance.
- `$dev-verifier` owns implementation completion verification and does not
  satisfy independent technical Review.

## Frozen Target

Every Review generation freezes one target before any reviewer runs.

### Pull request

Capture repository, PR URL/number, head/base branches, immutable head SHA,
immutable base SHA when available, and review start time. All reviewers and the
judge receive the same captured target. Immediately before accepting or
posting the combined result, `$review` fetches the current PR head SHA again.
If it differs from the captured head, the generation is `stale`; do not accept
or post its result and do not charge a repair attempt.

### Explicit diff

Require all of `Repository`, `Base`, and `Head`. Resolve both revisions to full
commit SHAs before review and inspect exactly that immutable range. A diff-only
run returns the final Review artifact to its caller and never claims that a
GitHub comment or review was posted.

An explicit diff is always a standalone Review target. Dev-managed Review
accepts only the current PR after Dev has verified PR traceability, base and
dependency identity, and the repository-defined merge-ready representation of
generated or migration artifacts. A pre-PR diff may provide standalone advisory
evidence, but it cannot create or resume the Dev Review Run, consume its repair
budget, trigger automatic Dev repair, or satisfy the Dev technical-review gate.

## Generation Completion

Each generation runs exactly three isolated core lenses: specification,
correctness, and code quality. Collect them all and every concretely signaled
one-shot architecture, test, security, or integration result before judgment.
No source may trigger repair directly or cause a recursive conditional wave.
A head repaired for blocking findings requires a complete new generation, not
reused old findings. Advisory-only generations advance without a new repair
round; small advisory fixes may join an already-required repair batch. Mandatory
acceptance/CI gaps still require current proof through their owning gates.

Source artifacts preserve native Markdown, labels, provenance, exact target,
UTF-8 byte length, and SHA-256. The judge quarantines invalid sources and keeps
specification judgments separate from engineering judgments. Artifact fields
and successful native decisions are owned by Review's Artifact Contract; Dev
consumes the accepted combined result rather than constructing source artifacts.

A withheld hypothesis alone does not block coverage. An inaccessible required
surface does: preserve proven findings, but do not repair or approve until
required coverage is complete. Missing specification authority blocks Dev or
explicitly spec-required review. Standalone review records `Specification not
assessed` and returns at least advisory while engineering lenses finish.

Common actions, in precedence order, are `coverage-blocked`, `repair-required`,
`advisory`, and `none`. They map to `blocked`, `comments`, `comments`, and
`approved`. Only a current accepted combined artifact can advance Dev.

## Final Acceptance and Posting

The judge returns a compact proposed decision. Review deterministically assembles
it with immutable source files into the lossless combined artifact. `$review` alone:

1. verifies the judge envelope and that every accepted source is bound to the
   current generation's frozen target;
2. re-queries a PR's current base and head SHAs;
3. marks the result `stale` without posting when either revision is unexpected; and
4. when both revisions are unchanged and posting is authorized, publishes concrete
   findings or one concise combined summary and verifies GitHub accepted it.

Specialists, conditional reviewers, and the judge never
publish the final post. An immutable-diff review never posts. If an authorized
PR post cannot be verified, return `blocked - review not verified`.

The final artifact includes the target envelope (including Review Mode and
Started At), source verification table, and a lossless quarantine section. For
each quarantined source it retains an Artifact ID field (the received value, or
`none - missing`), the exact validation reason, provenance when
available, and verbatim raw Markdown; if
the judge artifact itself is invalid, it retains the complete judge artifact.
It also includes judge
dispositions/groups, common action, overall decision, posting evidence, and
next owner.

Posting requires the user's explicit request for GitHub comments or an already
authorized posting action for this exact PR. Automatic Skill selection is not
authorization. Without it, return the completed review artifact as not posted;
do not block analysis or require an approval question. `$review-pr` owns its
separate structural-comment workflow and is not a Review v2 gate.

## Repair and Re-Review State

The logical repair loop carries this immutable/history state on every handoff:

```text
Contract Version: 2
Review Run ID: unchanged across generations
Generation: current positive integer
Attempt Count: accepted repaired heads so far; starts at 0
Repair Limit: 5 unless an exact user override is verified
Repair Limit Authority: default contract | exact instruction source, quote and scope
Generation Status: collecting | judged | stale | resolved
Repository: unchanged
PR: unchanged when target type is pull-request
Base Revision: unchanged unless the caller starts a new Review run
Previous Head Revision: head reviewed before repair, or none for generation 1
Head Revision: current accepted frozen head
Change Evidence: commits, diff, tests, or CI evidence supplied for this repair
Prior Combined Artifact: durable reference to the preceding generation
```

For one uninterrupted run, `Generation` must equal `Attempt Count + 1`.
`Repair Budget Remaining` is derived as `Repair Limit - Attempt Count`, not
maintained as an independent counter. The default last valid state is generation
`6`, attempt `5`.

A user may explicitly change the numeric ceiling for a named issue/PR/run.
Verify the actual instruction, its exact scope and any higher-priority limit;
record its source and quote with the effective limit in the existing run state.
An update such as “any progress?”, “continue until clean”, restored capability,
a worker dispatch receipt or a controller's paraphrase is not a cap override.
The changed limit does not reset attempts, start a replacement run, authorize
scope expansion, or waive convergence, validation or review requirements.
A limit of 7 after attempt 5 permits at most two further accepted repair heads,
not seven fresh attempts. The worker validates the same source and state before
mutation; do not report repair started until its actual progress is observed.

Before reviewer dispatch, repair routing or mutation, and repaired-head
acceptance, validate the complete state. Generation `1` has no previous head or
prior artifact. Every later generation requires both, and the prior artifact
must bind the immediately preceding generation and previous head. Missing,
discontinuous, reset, contradictory, or ceiling-exceeding state returns
`blocked - invalid review repair state` without reviewer dispatch or code
mutation.

Only an accepted combined artifact for the current head may route repair. It
must account for all core, signaled conditional, judge,
and final-head evidence. Treat all confirmed findings crossing the selected mode threshold in that
artifact as one repair batch; retain lower-priority advisories without requiring
repair. Do not let nonblocking optional work prolong a passing generation. The repair worker may create the coherent commits
the repository requires, but Review accepts one new repaired head and increments
the attempt count once for the complete batch.

An expected repaired head is accepted only after it is bound to the same
repository, PR, base, and Review Run ID and accompanied by change evidence.
Every accepted new head increments the shared `Attempt Count`, increments the
generation, and reruns the full core fan-out. The count is shared across
`$dev-implementer`, `$dev-ci-repair`, and all Review findings; it is not reset per
finding, reviewer, or repair route.

An unexpected head makes the in-flight result `stale`; it does not consume an
attempt and must not be silently adopted. At the effective Repair Limit, unresolved `repair-required` or
`coverage-blocked` work returns `blocked - review repair ceiling reached`
before any new repair mutation or reviewer dispatch. Without a verified user
override, no sixth repair attempt or generation `7` is routed.

Maintain an issue/PR convergence history across Review Run IDs: prior run and
base/head identities, cumulative accepted repair heads, recurring root causes,
mandatory-evidence gaps, and base-drift reasons. A base change starts a new
target Run, not a new issue history. Before another expensive generation after
repeated base drift, Dev checks the latest base and coordinates integration
order through the existing project owner when applicable. Do not change other
PRs or freeze shared branches without authorization.

Before a third or later repaired head across that issue/PR history, Dev records
a convergence checkpoint. Per-run counters still obey their existing equation.
Continuation requires confirmed blocking findings that remain within the
approved scope, a bounded remediation and named proof, and no repeated root
cause or unplanned contract, persistent-model, migration-order, ownership, or
cross-repository expansion. Otherwise Dev re-enters architecture/planning,
splits the work, or routes a changed product decision to PM. This checkpoint
does not increase the effective repair limit.

Standalone Review returns the combined artifact to the caller and never
requires `$dev`. A Dev-managed result routes confirmed implementation findings
to `$dev-implementer`, failing-check or CI findings to `$dev-ci-repair`, and a verified
clean/current result to `$dev-merge-handoff` or the caller's separate Product
Review phase.

## Completion Boundary

Review Contract Version 2 is the minimum compatible technical-review surface
for Develop standard and strict workflows. Develop fails closed when the Review v2
core gate is missing or incompatible; it never silently falls back to Review
v1 or a local generic reviewer.

- Repository contents remain read-only throughout Review.
- Review evidence never substitutes for Dev verification, Product Review,
  Design Review, human acceptance, release acceptance, or merge policy.
- A Review result applies only to the exact frozen target and generation named
  in its artifact.
