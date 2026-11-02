---
name: dev-test
description: "Run post-implementation validation under the selected Dev mode and classify failures before PR preparation."
metadata:
  owner: jay1803
  family: develop
  maturity: stable
  distribution: develop
---

# Dev: Test

Prove the implementation works technically: validate code behavior and engineering quality against the plan.

`$dev-test` owns mode-appropriate validation. Read the [mode contract](../dev/references/development-mode-contract.md) before selecting checks; it owns each mode's validation floor, waivers, unskippable conditions and `Skipped / Unverified` reporting. Omitted mode means standard.

## Boundary

- Own the initial post-implementation validation before PR creation, including build, test, lint, typecheck, schema/migration, smoke, acceptance, and mode-selected hands-on QA.
- When Dev State marks a production loop required or active, own execution of the contract's verifier and the evidence record for each run. `$dev` remains the loop controller and `$dev-implementer` owns code changes.
- Keep ownership of the first failure discovered during this phase long enough to classify it and preserve evidence.
- Route change-caused implementation failures to `$dev-implementer`; do not turn initial validation into CI repair merely because a local command is red.
- Route to `$dev-debugger` only when the failure represents wrong behavior, a regression, or a failed acceptance check whose root cause is still unknown after initial classification. Include the failing command, reproduction, expected/actual behavior, and relevant evidence.
- Route to `$dev-ci-repair` when a PR check is red or when repeated CI/environment behavior cannot be resolved within this validation phase and the handoff includes the exact failing command and evidence.
- Do not own PR review comments, merge conflicts, or requirement conformance; route those to `$dev-implementer` or `$dev-verifier`.
- Do not treat a standalone verify-only request as post-implementation test
  work. It is owned by `$dev-verifier`, freezes its exact target, and
  stops with evidence; a failed verification does not authorize this skill to
  repair or rerun a deploy.

## Evidence Reuse And Execution

Formal testing is a responsibility, not a requirement for a different agent.
The current implementation worker may perform it when the controller's scope,
tools, permissions, and independence requirements allow. The controller still
accepts the Test Result and keeps required verification and Review separate.

Before running a check, assess existing evidence against the selected validation
floor. Reuse an actual, inspectable result only when all relevant inputs match:

- exact command, check configuration, assertions/fixtures, and observed result;
- implementation/test/config/generated inputs and relevant dependency versions;
- revision or immutable worktree-input identity, scope, and acceptance coverage;
- environment, role/account, runtime state, and required fidelity/freshness.

Record the source and matching basis, not just an earlier agent's claim or the
same Git SHA. A matching revision alone does not establish current live state.
Rerun affected checks when inputs or environment change, results are missing or
unverifiable, or the user/repository/acceptance contract requires new execution.
Do not rerun an unchanged sufficient check solely because the phase owner
changed. If required evidence cannot be gathered, retain valid partial results
and report the missing boundary after applying the mode contract's unattended
validation rule; a pass covers only the checks actually run.

Reuse does not waive a required external verifier, authorize a remote action or
deployment, weaken mode-specific coverage, or let the implementer approve an
independent Review. Preserve its source, input, environment, and authorization.

Before adding or changing a durable test, apply the
[test authoring gate](references/test-authoring.md); zero new tests is a
complete result when existing coverage proves the selected behavior. For suite
selection, UI/fixture fidelity, mixed framework results, failure attribution,
baseline failures or authorized exceptions, read
[validation evidence](references/validation-evidence.md). Keep command truth,
attribution and gate effect together in the Test Result for downstream reuse; a
green final summary does not replace the command's failed exit.

## Workflow

1. Read the current implementation brief or selected Dev plan, implementation result, acceptance criteria, known validation commands, and Resume Receipt when supplied. Consume diagnosis/planning artifacts only when their stages were selected; do not require documents for intentionally unselected stages. For a required production loop, read the [production-loop contract](../dev/references/production-loop-contract.md).
2. Confirm the mode and touched surface (iOS, macOS, shared Apple code, web, backend, full-stack, CLI/library, docs/config, or mixed). Pick checks from that surface: the Apple build/test target, backend API/schema check, web component/route test, or CLI/package/config check; available suites are not all mandatory, and API changes keep the selected `$dev-api-steward` closeout. Resolve target/suite selectors and evidence fidelity before launch under [target and harness readiness](references/validation-evidence.md#target-and-harness-readiness).
3. Assess reusable evidence, then run the smallest missing, invalidated, or explicitly fresh checks the mode contract requires for the changed risk surface. Reuse or add tests under the test authoring gate.
4. Run hands-on QA only when the mode contract selects it, following [hands-on QA](references/hands-on-qa.md) for the named surface and expected result.
5. For a required production loop, run its remaining verifiers at the stated fidelity and record each run with the contract's evidence record. Do not modify or weaken an external verifier to pass; on failure, return the observation to `$dev`.
6. Record exact commands, environments, app state, evidence, and results, distinguishing checks executed in this phase from verified reused evidence.
7. Attribute any failure under [failure attribution](references/validation-evidence.md#failure-attribution) and route it as the Boundary section states, with the selected platform context.

After passing checks, return evidence to the controller and name the next
selected gate. Use `$dev-verifier` when selected; otherwise continue toward
`$dev-pr-writer` with current receipt-backed evidence. If a new material risk
or evidence gap triggers verification, return that trigger to the controller
for a phase-plan update before dispatch. A passing test does not waive a
selected or newly required verifier.

## Reporting

Summarize selected coverage and material limitations; do not generate per-assertion
matrices or an exhaustive list of hypothetical edge cases. For each command include
its actual exit/completion state and all framework summaries, with the source and
target binding. Carry any baseline comparison, exact exception and allowed next
stages under the same result; keep failed and filtered runs distinct.

Post the result as a Linear comment only when the active workflow has a
Linear-write tool and Dev State allows it; otherwise return the exact comment text
and state that it was not posted.

```markdown
## Test Result

Mode: <fast | standard | strict>

### Commands
- `<command>`: <pass | fail | blocked> - <exit/completion; all framework summaries> - <executed here | reused: source and matching inputs/environment>

### Hands-On QA
- <not selected | pass | fail | blocked> - <surface, branch/commit, app/scheme/target, device/OS/browser, evidence>

### Coverage Notes
- <Acceptance criteria, bug repro, regression check, or risk covered>

### Skipped / Unverified
- <skipped test/gate/edge case plus risk and recommended human follow-up, or none>

### Production Loop
- <not required | iteration N or passed/blocked, with the contract's evidence record>

### Failures / Blockers
- <step or check: expected vs actual, evidence, environment, repro rate when retested; attribution and owner; exact exception and permitted stages if applicable>

### Recommended Next Step
<After pass: controller-owned next selected gate (`$dev-verifier` when selected, otherwise `$dev-pr-writer` with current receipt-backed evidence); return new verification triggers to the controller. After failure: `$dev-implementer`, `$dev-debugger`, `$dev-ci-repair`, or stop.>
```
