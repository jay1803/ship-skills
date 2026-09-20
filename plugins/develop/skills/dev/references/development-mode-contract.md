# Development Mode Contract

Effective modes are `fast`, `standard`, and `strict`; omitted mode resolves to
`standard`. Strict is a distinct threshold, not an alias. Preserve the selected
mode through PM, Router, Dev workers, Review, and merge handoff. Existing
historical artifacts retain their original labels and hashes; a new explicit
strict request changes pending gate policy, not historical evidence.

Standard blocks confirmed P0/P1 defects; strict blocks P0/P1/P2. Both retain the
independent Review, required product outcomes, enforced CI, authorization, and
exact-target requirements. Their validation depth differs below. Strict alone does
not select extra agents, stronger models, manual QA, or exhaustive checks.
Read the package-local [severity policy](review-severity-policy.md) when deciding
whether findings require repair or a complete review can advance.

Branch selection follows [branch strategy](branch-strategy.md) in every mode;
mode never changes the repository-policy precedence or batch isolation.

## Mode Matrix

| Mode | Intent | Required validation and gates | Skipped by default |
| --- | --- | --- | --- |
| `fast` | Unattended delivery focused on getting the primary path landed quickly | Primary-path implementation, focused unit tests, checks structurally required to build/open/merge the issue PR, enforced CI and repository policy, merge-conflict resolution, tracker/PR traceability, and merge handoff | Technical Review, hands-on QA, exhaustive acceptance/edge-case validation, PR Product Review, human acceptance waiting, optional broad integration/E2E/smoke suites, and optional test deployment or verification |
| `standard` | Default unattended delivery; P0/P1 defects block | Focused primary-flow tests, ticket-specific regression coverage, necessary build/typecheck and enforced repository/CI checks, Resume-Receipt-selected Dev verification when its trigger applies, one combined Review v2 technical gate when selected by the phase plan, PR Product Review when user/product behavior or approved acceptance criteria change, CI, issue-base merge, and mode-appropriate test handoff | Physical-device, real-account, live-environment testing and human acceptance waiting under the unattended validation rule below; optional hands-on QA; Product Review is `not applicable` for internal maintenance |
| `strict` | P0/P1/P2 defects block; P3 may remain | Standard lifecycle gates plus risk-selected failure, recovery, concurrency and integration coverage; targeted reverse-red checks when useful | Exhaustive checks, per-assertion mutation matrices and extra reviewers or manual QA solely because strict was selected |


## Resume-First And Stage Selection

The [resume preflight](resume-preflight.md) owns readiness, route and receipt
freshness before Dev mutations or delegation. The [Dev entrypoint](../SKILL.md#stage-selection)
owns stage triggers. A mode changes thresholds and optional scope, not the
preflight, repository authority, or completed-evidence identity.

### Tracked-Artifact Preset

`tracked-artifact` is a phase-plan preset, not a delivery mode, new
controller, or Direct-route replacement. Select it only when the artifact is already
clear and either the user or repository policy requires the issue, isolated
branch/worktree, PR, CI, applicable merge, and tracker lifecycle. It keeps
those lifecycle gates and uses an inline implementation brief, task-specific
authoring/implementer ownership, and artifact-specific validation.

By default the preset does not dispatch technical planning, verifier, combined
technical Review, or Product Review; optional TDD remains inside implementation. Each can
still be selected by its existing trigger or an explicit Review request.
Strict alone does not override the preset's stage-selection rules. API/schema/auth/security/
privacy/migration/destructive/concurrency work, a complex cross-component
contract, or high failure cost exits the preset to the normal Dev phase plan;
an `artifact` label never suppresses that escalation. The preset never skips
required CI, merge policy, tracker traceability, one-writer ownership, or a
human-only/release boundary.

## Fast Mode

Fast mode is an explicit unattended optimization, not a claim that skipped work passed.

- Validate the primary user or system path with focused unit tests. Run the minimum build, typecheck, lint, schema, or CI commands needed to prove the change can structurally progress through the repository's delivery path.
- Do not expand validation merely because the acceptance criteria list many edge cases. Record unverified edge cases in Dev State and the final result.
- Do not launch simulators, apps, devices, or browsers for manual inspection. Do not invoke `$review`, or PR Product Review. Do not wait for human acceptance. Skip optional test deployment and post-deploy verification.
- An automatic deployment caused by merge is allowed. Do not wait for or claim its result unless the repository makes that result an enforced merge gate.
- Mark every omitted gate as `skipped (fast mode)`, never `passed`, `clean`, `approved`, `accepted`, or `not required`.
- Continue past known non-critical findings only after recording them as skipped or unverified. Stop when a finding meets an unskippable condition below.
- After a issue-base merge, an implementation issue may move to `Done` even when human acceptance is labeled as required, but the closeout comment must say acceptance was not performed and list the skipped or unverified scope.

### Unskippable Conditions

Fast mode still stops for anything that makes forward progress impossible or the primary path unsafe:

- focused unit tests for the primary path do not pass;
- the code cannot compile/build to the level required to create or merge the PR;
- required CI, branch protection, repository policy, authentication, permissions, or merge conflicts block progress;
- a known critical correctness, security, privacy, authorization, data-loss, destructive-migration, or primary-path defect remains;
- a required pre-merge deployment or test-environment verifier is technically enforced and cannot be bypassed;
- the issue PR is a repository-defined production promotion: stop Dev and route
  the production promotion to `$release`.

Do not broaden “unskippable” to include optional quality gates merely because they are documented. If skipping the step still permits safe primary-path delivery under enforced policy, disclose it in existing workflow state and continue. Fast mode does not create a dedicated risk ticket merely to record skipped work.

## Standard And Strict Modes

`$dev --strict` keeps the same stage-selection rules, with deeper risk-selected validation and a stricter finding threshold. Standard mode is the default. `$dev`, `$dev --standard`, and a PM handoff with no mode all resolve to the same workflow and reporting semantics.

- Standard validates the primary flow and the failure explicitly addressed by a
  bug ticket. Reuse relevant existing tests; add a focused regression test for a
  bug when runnable, or record the concrete limit and equivalent repro evidence.
  Do not automatically add unrelated edge cases, broad suites, reverse-red
  experiments (deliberately breaking a working implementation), mutation testing,
  or per-assertion proof matrices. A normal bug repro is not a mutation campaign.
- Strict additionally selects relevant failure, recovery, concurrency and
  integration checks from the changed behavior and concrete risk. It may use
  targeted reverse-red checks for critical mechanisms; it does not require
  every assertion to have a mutant or every possible edge case to be tested.
- In either mode preserve existing coverage, investigate relevant test failures,
  and run enforced repository/CI checks. Mode reduces optional validation, not
  required product behavior. An explicit user/repository testing requirement
  remains binding unless its owner changes it; report the source of any exception
  to the default scope. Explicit TDD remains available without a mutation matrix.
- Controller handoffs carry the selected scope and its source. Do not silently
  upgrade standard by copying strict checklists or adding generic security,
  edge-case, TDD or reverse-red requirements. Known credential exposure,
  cross-account access or irreversible data damage directly introduced by the
  change still require focused attention, even for a personal project.
- When the phase plan selects Review, require Review Contract Version 2 as the
  minimum compatible technical-review surface. Run `$review` once per frozen
  generation as the sole technical-review gate; it owns core and signaled
  conditional coverage, judge/final-head acceptance, and authorized GitHub posting.
  Use the thermo-nuclear maintainability rubric on the code-quality core lens
  in every generation, without adding reviewers or requiring a finding.
- Fail closed when Review v2 is missing or incompatible. Do not fall back to a
  Review v1 surface, a local generic reviewer, or a partial Review result.
- Run PR Product Review when user/product behavior or approved acceptance
  criteria change; record it `not applicable` for internal maintenance. Run
  normal CI/issue-merge gates in every case.
- Apply the unattended validation rule below before selecting test-environment or human-acceptance gates. Hand production-only verification to `$release` or the separate acceptance owner; it does not hold engineering delivery open.
- Create Dev commits unsigned with per-command signing disabled and report that signing was skipped.
- Add hands-on, material edge-case, or representative-runtime checks when the
  user requests them, the repository/acceptance contract requires them, or a
  concrete changed-path risk cannot be proved by automated evidence. Name the
  surface, reason, expected result, and sufficient evidence in the receipt.
  A UI change or strict mode alone does not select a full QA bundle.
  Apply mode waivers first. A remaining required check that cannot run stays
  blocked/unverified, never passed.
- Consume only the current combined Review result. After an accepted blocking repair
  and fresh required validation, run a complete new generation; preserve the
  existing isolation, coverage, freshness, and shared repair ceiling (default
  five; exact user overrides follow the Review state contract).

## Unattended Validation And Deferred Acceptance

Standard is unattended with focused automated validation and its selected
Review/product gates, not a synonym for fast. Strict inherits the unattended
environment boundary while applying its deeper risk-selected validation.
A request for unattended execution alone does not select fast.

- Prove required product behavior with simulators or local test runtimes, seed
  accounts, and deterministic fixtures. Use mock E2E where it adequately exercises
  the selected flow; apply the mode-specific failure coverage above.
- Physical-device, real-account/real-SDK-account, live-provider/live-environment
  tests, and waiting for a named human tester are waived from engineering delivery.
  This includes such tests written as mandatory in an existing ticket, Human
  Acceptance section, production-loop plan, or worker handoff. Do not stop before
  PR, merge, engineering closeout, or successor dispatch to obtain devices,
  credentials, a real deployment, or human sign-off solely for those tests.
- Keep the product outcomes and automated checks. Record each waived surface as
  `skipped (standard mode)` (or the effective strict mode) under `Skipped /
  Unverified`, with the available simulator/seed/mock evidence and its limits.
  A simulated pass is not real-environment evidence; retain observed failures.
- Treat useful real-environment tests as nonblocking recommendations. When they
  are materially necessary for later human acceptance, reuse or draft a separate
  acceptance ticket and hand authorized creation to `$pm-project-orchestrator`.
  Include why real evidence is needed, the candidate/build, human owner or role,
  safe account/access prerequisites, steps, expected results and evidence fields.
  The acceptance ticket may depend on implementation; implementation and its
  successors must not depend on that ticket. No ticket is needed merely to log
  every skipped check. Missing follow-up logistics or tracker-write authority
  leaves a draft/recommendation, not an engineering blocker.
- On resume, carry the superseded requirement and effective waiver through the
  receipt, verification ledger, Review, merge handoff and project state. A stale
  label or old mandatory wording cannot reinstate the waived gate. An eligible
  merged implementation can become `Done`; separate acceptance stays pending.
  Report engineering completion separately from real-world acceptance.

This waives test surfaces, not known defects, required automated checks, actual
implementation dependencies, branch protection, human-only merge policy, or
release/deployment authority. If CI technically enforces a waived surface, report
that enforcement as the blocker; do not bypass it or pretend it passed. A later
explicit request to perform real-environment acceptance or a standalone
`verify/live-outcome` task owns that evidence separately and is not auto-waived.

## Reporting Invariants

Every Dev State, worker handoff, callback, test result, and merge handoff carries:

```markdown
Mode: <fast | standard | strict>
Skipped / Unverified: <entries or none>
```

Reports must distinguish performed evidence from skipped work. A fast-mode completion claim means the primary path landed in the resolved issue PR base under the reduced contract; it does not imply full acceptance, edge-case coverage, test or production verification, production release, or human sign-off.

Keep completion reports concise: performed checks and results, the selected
coverage, and material skipped/unverified boundaries. Group optional omitted
edge cases; do not invent an exhaustive omission list or per-assertion report.
Required outcome/acceptance and authority clauses apply to both modes; validation
depth follows the distinct rules above.
