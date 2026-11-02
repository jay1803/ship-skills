---
name: dev-implementer
description: "Implement approved changes and repair PR review findings or conflicts, preserving scoped ownership and current validation evidence."
metadata:
  owner: jay1803
  family: develop
  maturity: stable
  distribution: develop
---

# Dev: Implementer

Own scoped code changes from an implementation brief or selected Technical Plan,
including authorized PR repair. Reuse the current implementation worker while
scope, context, tools, permissions, and capability remain suitable; a switch
between coding, testing, and a bounded repair does not by itself need a new
agent. In a Dev lifecycle the `$dev` issue worker applies this Skill inline by
default, or runs it as a bounded sub-agent under
[delegated implementation](../dev/references/execution-ownership.md#delegated-implementation);
it is never a separate persistent issue thread. The issue worker accepts
evidence and owns lifecycle transitions, PR management and authorized merge;
return results there, not to the project orchestrator. Direct bounded edits
outside Dev keep their caller's workflow.

## Select The Work

- **Implementation:** use the current brief and applicable platform guidance.
- **PR comments, a combined Review batch, or merge conflicts:** read
  [PR repair](references/pr-repair.md) before changing a PR branch or replying
  to threads. Resolve the exact PR and repair state; ordinary implementation
  instructions do not bypass that gate. Review-only input does not authorize
  repair or GitHub posting.
- **TDD is explicitly requested by the user or required by the repository:**
  read [TDD](references/tdd.md). Keep red/green/refactor in this implementation
  owner; it does not add a separate phase or require a planner document.
- **Red PR checks or repeated CI/environment failures:** `$dev-ci-repair`
  owns diagnosis and the bounded CI repair route. Do not start competing writers.
- **Unknown cause or unsettled technical choice:** return the evidence to
  `$dev-debugger` or `$dev-planner`; do not invent a repair outside the brief.

## Platform Hazards

Follow local patterns; load a specialist only when the change needs its workflow.

- **Apple:** `build-ios-apps:*` / `build-macos-apps:*` for build, run or debug;
  signing, entitlement, deployment-target or build-setting changes need the plan.
- **SwiftUI:** specialist guidance for state, identity, navigation or
  availability; previews or runtime checks, not source text, prove rendering.
  For lists, tab roots, always-mounted screens or frequent updates, follow
  [SwiftUI performance](references/swiftui-performance.md).
- **Web:** `$build-web-apps:frontend-app-builder` for new or substantial UI; no
  unrequested redesign.
- **Backend/Supabase:** contracts before clients; keep migrations, generated
  types and clients aligned; Supabase guidance for schema, RLS, Auth or Edge
  Functions; never weaken auth, RLS or tenant scoping, expose secrets, or use
  production data.

## Implementation And Test Order

Use these defaults in every mode. An explicit user/repository TDD requirement
takes precedence; the mode selects validation depth, not test-first feature work.

- **Features and enhancements:** settle acceptance criteria, then implement the
  smallest coherent slice. Use existing checks during implementation. Afterward,
  apply the [test authoring gate](../dev-test/references/test-authoring.md) to
  missing coverage and add only tests with distinct regression value. Derive
  expected outcomes from the accepted requirements or an independent contract,
  rather than copying the behavior of the implementation just written.
- **Bug fixes:** establish the reported failure before repairing production
  behavior. Reuse an existing test that reproduces it; otherwise extend the
  owning test or add one minimal regression that fails on the target behavior,
  not setup or a missing dependency. Repair the code and rerun the same test to
  show the failure is fixed. This focused repro does not select a broader TDD
  phase or extra test suite.
- **Bugs without a reliable automated observation point:** retain a repeatable
  reproduction and compare before/after evidence at that boundary when runnable.
  Use available checks and report any unexecuted reproduction or missing required
  proof under the mode contract. Do not substitute source-string or
  self-fulfilling mock assertions for evidence of the bug.

## Workflow

Consume a planner-prepared engineering ticket's settled design as the current
Technical Plan. Check relevant source assumptions, then implement within its
stated latitude; do not repeat architecture selection. A missing material
decision returns to the controller, not a guess or recursive task split. A
design task is not authorization to code.

Read the [mode contract](../dev/references/development-mode-contract.md#standard-and-strict-modes)
before choosing test depth. Standard reuses primary-flow coverage and retains
focused regression proof for a bug ticket; do not automatically select TDD, mutation
experiments or unrelated edge cases. Strict selects additional risk-based checks.

1. Read approved scope, acceptance criteria, selected Technical Plan or current
   brief, relevant research, and the Resume Receipt when supplied. Missing
   material decisions return to the controller; unselected stages need no
   separate documents. PR repair uses its exact target and authorized batch as
   the input rather than reconstructing a new issue lifecycle.
2. Resolve only missing repository ownership, local patterns, constraints, and
   validation commands. Search from relevant files, symbols, or errors with
   `rg`; follow a dependency only to answer a concrete gap. Reuse current
   source-anchored facts and stop discovery once this change is supported.
3. Confirm the changed platform and apply only its hazards. Correct a wrong
   platform selection in place when scope, architecture, permissions, and
   validation stay unchanged; otherwise escalate the changed boundary.
4. Inspect target code/tests and make the smallest coherent approved change.
   Preserve non-goals, local conventions, selected domain invariants, migration
   order, and contract checkpoints. Add tests, generated files, migrations,
   fixtures, previews, or docs only for a practical required surface. Before
   writing or changing tests, apply the test authoring gate.
5. Validate while implementing. Keep focused reproduction/red/green results
   when relevant, then apply `$dev-test` for formal validation. The same worker
   may execute both responsibilities under the controller's selected scope.
   Carry actual command, result, revision or immutable input, environment,
   dependencies, and coverage so testing can assess safe evidence reuse.
6. Attribute a local failure under
   [failure attribution](../dev-test/references/validation-evidence.md#failure-attribution)
   before repair. Fix a known in-scope cause here;
   escalate unknown behavior to diagnosis or repeated CI/environment failures
   to `$dev-ci-repair`. Preserve retry limits and all failed/missing evidence.
7. Stop for newly discovered product, safety, contract, persistent-model,
   migration, ownership, or cross-repository choices. A retained worker never
   gains permission to expand scope, reset a Review Run, or accept its own
   independent Review. Use PR repair's scope check when applicable.

## Result

Before handoff, apply the test authoring gate to this change's test diff. Remove
new duplicate or weak assertions and retain the smallest useful regression
proof. State when existing validation is sufficient and no test changes are
needed; no new tests is a normal outcome, not an omitted validation phase.

Return changed files and resulting behavior, the platform applied, any
invariant/API/migration notes, and validation evidence with provenance. Mark
each check as executed here, reused from an identified current result, failed,
blocked, or skipped; a named command alone is not proof. Include required
follow-up and the next selected gate: `$dev-test` while formal validation is
pending, then `$dev-verifier` when selected, otherwise `$dev-pr-writer`. For PR
repair also return the authorized batch, one final repaired head,
handled/remaining threads, and verified push/reply status from the repair
reference.

The controller accepts formal test evidence and any selected verifier before PR
or completion gates advance. A head repaired from a Review batch returns to the
controller, which selects any re-review; it is not implementation completion.
