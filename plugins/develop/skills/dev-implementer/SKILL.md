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
agent. The controller still accepts evidence and owns lifecycle transitions.

## Select The Work

- **Implementation:** use the current brief and applicable platform guidance.
- **PR comments, a combined Review batch, or merge conflicts:** read
  [PR repair](references/pr-repair.md) before changing a PR branch or replying
  to threads. Resolve the exact PR and repair state; ordinary implementation
  instructions do not bypass that gate. Review-only input does not authorize
  repair or GitHub posting.
- **TDD is explicitly requested, or selected under the mode contract:**
  read [TDD](references/tdd.md). Keep red/green/refactor in this implementation
  owner; it does not add a separate phase or require a planner document.
- **Red PR checks or repeated CI/environment failures:** `$dev-ci-repair`
  owns diagnosis and the bounded CI repair route. Do not start competing writers.
- **Unknown cause or unsettled technical choice:** return the evidence to
  `$dev-debugger` or `$dev-planner`; do not invent a repair outside the brief.

## Reference Selection

Start from the changed surface or diagnostic evidence, not the repository label. Reuse current context that matches the target files, version, environment, and acceptance boundary. Read or load a specialist only when its workflow or an unresolved platform question is needed for the selected task; inspect additional project areas when a concrete dependency or evidence gap reaches them. Repository instructions and required validation still apply. If none of the listed platforms applies, use the shared workflow and repository guidance rather than forcing a match.

Read the shared workflow, then the matching reference(s) from `references/` when applicable:

- iOS app, iOS simulator workflow, Xcode iOS target, UIKit, iOS SwiftUI screen, App Intent, or iOS runtime behavior: [implement-ios.md](references/implement-ios.md)
- macOS app, AppKit, macOS SwiftUI scene/window/menu, signing, entitlement, packaging, or macOS runtime behavior: [implement-macos.md](references/implement-macos.md)
- SwiftUI view, state, layout, navigation, sheet, animation, accessibility, preview, performance, or Liquid Glass work: [implement-swiftui.md](references/implement-swiftui.md)
- Frontend web, React, Next.js, Vite, dashboard UI, browser behavior, responsive layout, accessibility, client state, or web tests: [implement-web.md](references/implement-web.md)
- Backend/API/service work that is not primarily Supabase: [implement-backend.md](references/implement-backend.md)
- Supabase schema, migration, RLS, Auth, Edge Functions, Storage, Realtime, generated types, or Supabase client/server integration: [implement-supabase.md](references/implement-supabase.md)

Multiple references are allowed when the plan crosses surfaces. Sequence backend/API contracts before clients by default, and pair `implement-swiftui.md` with `implement-ios.md` or `implement-macos.md` when app-level build/run/debug behavior matters.

## Workflow

For an engineering ticket prepared by the planner, read the
[engineering ticket protocol](../dev-planner/references/engineering-ticket-protocol.md)
and consume its settled design as the current Technical Plan. Check relevant
source assumptions, then implement within its stated latitude; do not repeat
architecture selection. A missing material decision returns to the controller,
not a guess or recursive task split. A design task is not authorization to code.

Read the [mode contract](../dev/references/development-mode-contract.md#standard-and-strict-modes)
before choosing test depth. Standard reuses primary-flow coverage and adds a
focused regression for a bug ticket; do not automatically select TDD, mutation
experiments or unrelated edge cases. Strict selects additional risk-based checks.

1. Read approved scope, acceptance criteria, selected Technical Plan or current
   brief, relevant research, and the Resume Receipt when supplied. Missing
   material decisions return to the controller; unselected stages need no
   separate documents. PR repair uses its exact target and accepted batch as
   the input rather than reconstructing a new issue lifecycle.
2. Resolve only missing repository ownership, local patterns, constraints, and
   validation commands. Search from relevant files, symbols, or errors with
   `rg`; follow a dependency only to answer a concrete gap. Reuse current
   source-anchored facts and stop discovery once this change is supported.
3. Confirm the changed platform and read only the matching references. Correct
   a wrong reference in place when scope, architecture, permissions, and
   validation stay unchanged; otherwise escalate the changed boundary.
4. Inspect target code/tests and make the smallest coherent approved change.
   Preserve non-goals, local conventions, selected domain invariants, migration
   order, and contract checkpoints. Add tests, generated files, migrations,
   fixtures, previews, or docs only for a practical required surface.
5. Validate while implementing. Keep focused reproduction/red/green results
   when relevant, then apply `$dev-test` for formal validation. The same worker
   may execute both responsibilities under the controller's selected scope.
   Carry actual command, result, revision or immutable input, environment,
   dependencies, and coverage so testing can assess safe evidence reuse.
6. Classify a local failure before repair. Fix a known in-scope cause here;
   escalate unknown behavior to diagnosis or repeated CI/environment failures
   to `$dev-ci-repair`. Preserve retry limits and all failed/missing evidence.
7. Stop for newly discovered product, safety, contract, persistent-model,
   migration, ownership, or cross-repository choices. A retained worker never
   gains permission to expand scope, reset a Review Run, or accept its own
   independent Review. Use PR repair's scope/convergence gate when applicable.

## Result

Return changed files and resulting behavior, selected references, any
invariant/API/migration notes, and validation evidence with provenance. Mark
each check as executed here, reused from an identified current result, failed,
blocked, or skipped; a named command alone is not proof. Include required
follow-up and the next selected gate. For PR repair also return the unchanged
Review Run identity, one final repaired head, handled/remaining threads, and
verified push/reply status from the repair reference.

The controller accepts formal test evidence and any selected verifier before PR
or completion gates advance. A Review-managed repaired head returns to Review
for its next complete generation; it is not implementation completion.
