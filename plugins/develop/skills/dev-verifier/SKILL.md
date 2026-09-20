---
name: dev-verifier
description: "Audit completion claims against fresh tests, runtime evidence, acceptance criteria, and an exact revision. Independent technical review belongs to review."
metadata:
  owner: jay1803
  family: develop
  maturity: stable
  distribution: develop
---

# Dev: Verifier

Decide whether Dev can make a current, evidence-backed completion claim for the
exact implementation target. Implementation intent, a plausible diff, and a
list of tests that ought to pass are inputs, not proof.

Read the shared
[`Dev / Technical Review Boundary Contract`](../dev/references/dev-review-v2-contract.md)
to preserve the ownership seam. `$dev-verifier` is implementation-owned and
must remain separate from the later independent `$review` gate.

## Boundary

- Verify claims and evidence; do not independently review code quality or
  approve the implementation as a technical reviewer.
- Treat the repository as read-only during one verification run. Route fixes
  to the owning Dev skill, then verify the changed target again.
- Do not replace `$dev-test`. Testing produces engineering observations;
  verification maps current observations to every required acceptance and
  scope claim.
- Do not replace Product Review, Design Review, human acceptance, deployment,
  or production verification. Preserve each distinct gate and its status.
- Never edit, weaken, or substitute an external verifier to obtain a pass.

## Verify-Only Terminal

When the canonical Issue Route receipt selects `verify/repo`, `verify/pr`,
`verify/deploy`, or `verify/live-outcome` with `terminal_intent: verification`,
this skill is a standalone evidence owner rather than a selected full-Dev
completion gate. Freeze the exact target before any check:

- `repo`: repository path plus immutable revision or explicit worktree patch;
- `pr`: PR number/URL, base, and exact head SHA;
- `deploy`: named environment, requested revision, observed revision, and
  deploy-status claim; or
- `live-outcome`: the existing Production Loop or Human Acceptance contract,
  named environment, verifier, threshold, and immutable candidate.

Default state is read-only and no-repair. Execute a smoke, remote query, or
other external verification action only when the receipt or existing contract
authorizes that exact target, action, and side-effect envelope. Missing,
ambiguous, stale, inaccessible, skipped, or mismatched-environment evidence is
`blocked` or `unverified`, never `pass`. Do not alter implementation,
configuration, deployment, tracker completion, or PR state; do not retry a
side-effecting action merely because it failed.

Return a claim ledger and overall `pass`, `fail`, `blocked`, `unverified`, or
`not-applicable`, then stop. On a non-pass, return the smallest failure
boundary and proposed repair/authority route only. A later fix or resume needs
a fresh Issue Route receipt with explicit authorization and this ledger as its
resume anchor; verify-only evidence never satisfies a Dev merge or tracker
closeout gate by itself.

For this standalone terminal, the required inputs below mean the frozen target,
specific claim, requested freshness, exact authorized verification action (if
any), and the applicable deploy/outcome contract. It does not require an
implementation plan or post-implementation test result that does not exist.

## Required Inputs

- Issue or specification, acceptance criteria, approved scope, and non-goals.
- Current implementation brief or selected Dev plan, implementation result,
  mode, and all `Skipped / Unverified` entries. Use the Resume Receipt to
  identify selected stages; an intentionally unselected planner, architecture,
  or discovery stage needs no separate document. The brief must still establish
  approved scope, acceptance criteria, constraints, and the validation floor.
- Repository, base revision, head revision, working-tree state, and diff.
- `$dev-test` result plus relevant build, lint, typecheck, schema, package,
  runtime, or API Steward evidence.
- Any required external-verifier contract: exact input, environment,
  independence, threshold, and durable result.

If a required input is missing, return `blocked`; do not reconstruct product
requirements or claim completion from implementation prose.

## Evidence And Freshness

Freeze the verification target before evaluating evidence:

```text
Repository: <identity/path>
Base Revision: <full SHA>
Head Revision: <full SHA>
Working Tree: <clean | explicit patch identity>
Mode: <fast | standard | strict>
Verification Started At: <timestamp>
```

Evidence is current only when all of these are true:

- it identifies the command, inspection, runtime surface, or external artifact
  and its actual result;
- it is tied to the exact target revision or an explicit immutable input and
  environment relevant to the claim;
- no later code, test, configuration, generated-output, or documentation change
  invalidated the observation;
- the evidence source is available and credible for the claim it supports.

A timestamp alone does not establish freshness. Before returning, resolve the
target again. If it changed, mark affected evidence stale and rerun it through
the owning skill or return `blocked`. A fix after verification always makes the
affected result stale.

For mixed results or baseline exceptions, consume the existing Test Result's
[validation facts and gate effects](../dev-test/references/validation-evidence.md).
Retain failed observations in the ledger with their exact exception, if valid;
judge the remaining required claims separately. A baseline cause is not a waiver,
and a permitted filtered run cannot cover a new failure or an independent CI
gate. Do not rebuild a second test summary or request the same approval again.

## Mandatory Evidence Before Review

For selected full-Dev verification, first read and apply the
[unattended validation rule](../dev/references/development-mode-contract.md#unattended-validation-and-deferred-acceptance).
Keep waived physical-device, real-account, live-environment and human checks as
`unverified` ledger rows with their waiver and follow-up, outside the required
engineering claim set. Current simulator/seed/mock evidence can satisfy the
remaining engineering claims without proving the waived fidelity. These rows
do not block an engineering pass or the route to `$dev-pr-writer`. Standalone
verify-only tasks retain their requested evidence contract.

Keep defect priority separate from acceptance completion. If the approved
contract still requires local real-database, reopen/replay, or other evidence
fidelity, separate unit tests or source inspection do not substitute for that
proof. Record the exact requirement, available evidence, and missing fidelity
before the first technical Review; P2/P3-only policy cannot turn a mandatory
evidence gap into pass. Return the smallest test/implementation owner, not an
automatically added Product Review stage.

## Claim Outcomes

Build one ledger row for every acceptance criterion, required test/runtime
claim, and material scope boundary. When identity, cardinality, or environment
fidelity changes what evidence proves, retain that distinction in the claim
and identify the concrete fixture/runtime entities that witness it. Two requests
to one entity do not establish isolation between two distinct entities; inspect
the fixture bindings as well as the assertions before accepting that claim.
Use exactly these outcomes:

- `pass`: current evidence directly supports the claim.
- `fail`: current evidence contradicts the claim, a required check failed, or
  confirmed scope drift remains.
- `blocked`: required evidence is missing, stale, inaccessible, or cannot be
  collected at the required fidelity.
- `unverified`: a full-Dev evidence surface waived by the selected mode, or a
  standalone verify-only claim not executed because its required action,
  freshness, target, or authority envelope is absent. It is never a pass and does not imply the claim is false.
- `not-applicable`: the cited requirement or source proves that this surface
  does not apply. Never use this for skipped work, missing access, or an
  inconvenient check.

The overall result is:

- `fail` when any required claim fails;
- otherwise `blocked` when any required claim is blocked or freshness cannot be
  established;
- `pass` only when every required claim passes or is validly not applicable,
  scope is controlled, and no completion-critical uncertainty remains;
- `unverified` only for standalone verify-only work when no required claim has
  failed or blocked but one or more claims lack an authorized fresh observation;
- `not-applicable` only when no implementation-completion claim is being
  advanced. Docs/config-only work still requires appropriate structural and
  content evidence and is not automatically not applicable.

## Workflow

1. Freeze the target and inspect status plus the complete base-to-head diff.
2. Convert the approved acceptance criteria, planned outcomes, non-goals, and
   required mode gates into the claim ledger. Do not silently drop a criterion.
3. Attach current evidence to each claim. Distinguish test, runtime, inspection,
   external, and not-applicable evidence; record source, target/input,
   environment, result, and observation time.
4. Verify scope separately: every changed path belongs to the approved outcome,
   every expected generated or contract artifact is present, and unrelated
   behavior remains outside the diff.
5. Evaluate remaining uncertainty. A partially completed implementation cannot
   pass; return `fail` for disproved work or `blocked` for unavailable proof and
   name the next owner.
6. Re-resolve the target and freshness immediately before deciding.
7. Return the ledger and overall outcome. For standalone `verify/*`, every
   outcome stops after the ledger; a pass does not dispatch `$dev-pr-writer` or
   mutate PR/Dev state. Only a verifier selected inside an already-authorized
   full-Dev receipt may route a current pass to `$dev-pr-writer`; fixes or new
   evidence then route through `$dev-implementer`, `$dev-test`,
   `$dev-api-steward`, or the named external owner before a fresh verifier run.

## Surface Guidance

- **Code:** require current focused or mode-required test/build evidence and any
  required runtime observation. Source inspection alone does not prove behavior.
- **Docs/config-only:** use content inspection plus applicable link, schema,
  formatter, package, catalog, or configuration checks. Record application
  runtime as `not-applicable` only with a concrete rationale.
- **External verifier:** record verifier identity/version, immutable input or
  target revision, environment fidelity, independence, threshold, output, and
  durable artifact. An inaccessible or stale result is `blocked`, not a pass.
- **Partial completion:** retain the passing claim rows, mark the incomplete
  rows `fail` or `blocked`, list remaining uncertainty, and prohibit an overall
  pass or completion claim.

## Output

```markdown
## Dev Verification

Decision: <pass | fail | blocked | unverified | not-applicable>
Mode: <fast | standard | strict>
Repository: <identity/path>
Base Revision: <full SHA>
Head Revision: <full SHA>
Working Tree: <clean | explicit patch identity>
Verification Started At: <timestamp>
Verification Finished At: <timestamp>
Target Recheck: <unchanged | changed; stale evidence named>

### Claim Ledger
| Claim | Outcome | Evidence | Freshness | Notes |
| --- | --- | --- | --- | --- |
| <acceptance criterion, test/runtime claim, or scope boundary> | <pass/fail/blocked/unverified/not-applicable> | <command, result, artifact, or source> | <current/stale/unknown> | <rationale> |

### Scope
- <in scope, confirmed drift, or uncertainty with diff evidence>

### Tests And Runtime
- <current evidence, failure, blocker, or justified not-applicable surface>

### External Evidence
- <verifier provenance and result, blocker, or not applicable>

### Remaining Uncertainty
- <unknown and completion impact, or "None.">

### Skipped / Unverified
- <mode-authorized omission, never represented as passed, or "None.">

### Recommended Next Step
<For standalone `verify/*`: `stop` after reporting the ledger, with a proposed repair/authority route only when non-pass. For selected full-Dev verification: `$dev-pr-writer` only for a current pass; otherwise the exact Dev or external owner, followed by a fresh `$dev-verifier` run.>
```
