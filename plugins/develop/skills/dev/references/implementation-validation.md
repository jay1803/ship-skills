# Implementation And Validation

Read for selected pre-PR work. The Resume Receipt selects stages; resume at the pending owner without replaying completed work.

## Implementer Platform Selection

Use `$dev-implementer` for coding with the [platform hazards](../../dev-implementer/SKILL.md#platform-hazards)
of every changed surface; sequence backend/API contracts before clients by default.

Project defaults are allowed when the repo clearly documents one, but they are
advisory. If the actual issue touches a different surface, route by the issue
and repo evidence. Return material architecture or product-scope choices to the
controller for the planner or a requester decision under the
[autonomous decision rule](execution-ownership.md#autonomous-decisions-and-discovered-work).

## Project Classification And QA

Before implementation and before QA, classify the project and touched surface from repo files, package manifests, workspace/project files, framework conventions, scripts, CI config, and changed code:

- iOS app
- macOS app
- shared Apple-platform app code
- backend/API/service
- website frontend
- full-stack web
- library/CLI/package
- docs/config-only
- mixed

Use the [mode contract](development-mode-contract.md#standard-and-strict-modes)
for validation depth and selected hands-on QA. Project type helps locate the
smallest sufficient test surface; available suites are not all mandatory.
Use the relevant Apple build target, backend API/schema check, web component/route
test, or CLI/package/config check. API changes retain API Steward closeout.

Carry a compact validation brief into implementation: required checks and their
source, target/suite selectors, changed regression, and any required UI component,
interaction and evidence fidelity. Resolve a missing input/harness prerequisite
at that boundary before expensive execution; a display fixture does not prove
an input-control requirement. Use `$dev-test`'s
[target and harness readiness](../../dev-test/references/validation-evidence.md#target-and-harness-readiness)
guidance without adding optional suites to the selected floor.

Apply the development-mode contract, including its [real-environment precedence](development-mode-contract.md#unattended-validation-and-deferred-acceptance), before classifying QA as required. For other QA surfaces, record why they are not applicable when the repo/change has no runnable surface or does not touch the behavior; missing required automated evidence remains blocked. In fast mode, apply the [fast-mode rules](development-mode-contract.md#fast-mode) instead.

## Selected Pre-PR Work

The issue worker accepts state and artifacts under
[execution ownership](execution-ownership.md) and keeps the objective in Dev
State.

### Preparation And Missing Decisions

Reconcile Git/worktree/base state only when the receipt requires
`$dev-git-setup`. Build one compact brief from current canonical evidence:
objective, scope/non-goals, acceptance, relevant design/contract constraints,
project surface, validation floor and material risks. Link applicable outcome
or human-acceptance requirements with their mode disposition. Missing readiness
returns to the preflight's [entry audit](resume-preflight.md#entry-audit) before
Git mutations.

Resolve only deciding unknowns: `$dev-debugger` for an unexplained defect,
`$dev-spike` for local feasibility, `$dev-api-research` for third-party facts,
and `$dev-planner` for approach, invariants, task boundaries or sequencing.
Reuse an accepted root cause/plan; no separate discovery or architecture artifact
is needed for clear work. A new material boundary requires the planner's explicit
`split`, `no_split` or `blocked` assessment before dependent dispatch, under the
root Skill's reassessment protocol.

For backend/API changes, `$dev-api-steward` locks intended contracts before
implementation and compares the resulting diff afterward. Carry its constraints
into the brief and update required docs, generated clients, compatibility and
migration guidance. Contract disagreement returns to implementation. Cross-issue
execution belongs to `$dev-project-orchestrator`; its explicit multi-PR integration
checkpoint belongs to `$dev-integration-manager`.

### Implementation And Validation

Apply `$dev-implementer` inline with the brief, selected platform guidance,
prerequisites and return gate, or dispatch it as a bounded agent only under
[delegated implementation](execution-ownership.md#delegated-implementation).
The same owner handles coding, local tests and scoped fixes. It returns unresolved scope/contract decisions to their owner
and commits only scoped changes. Follow its
[implementation/test order](../../dev-implementer/SKILL.md#implementation-and-test-order).
TDD follows an explicit user request or repository requirement; its
red/green/adapt/decline evidence needs no extra worker or plan.

Apply `$dev-test` at the selected mode's QA bar. Assess existing evidence before
rerunning and use its test-authoring gate before adding tests. Preserve primary
paths, ticket regressions and required checks; select extra integration or
hands-on coverage from explicit requirements or concrete changed-path risk.
Apply unattended waivers before classifying unavailable evidence as blocking.
Keep unavailable remaining required proof blocked/unverified, not passed.
After three failed implementation/test repair attempts for the same blocker,
stop that loop with evidence. Review-managed repair uses its separate cumulative
round budget; do not reset either counter on resume.

### Selected Completion Verification

Select `$dev-verifier` for required independent evidence, insufficient implementer
proof or material changed-path risk. A new head alone does not select it.
When already selected, invalidate evidence affected by changed code, inputs,
config or dependencies and verify the current exact target before advancing.
Use its claim ledger and evidence-freshness rules rather than duplicating test
summaries. Each required acceptance/test/runtime claim and material scope boundary
needs an explicit outcome; implementation intent cannot establish completion.
Proceed from a current overall pass, or route failures/gaps to their owning Skill.
When unselected, retain the selected validation floor and continue without
manufacturing a verifier artifact.
