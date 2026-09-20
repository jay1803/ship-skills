# TDD Within Implementation

Use TDD as an optional implementation discipline for one already-scoped,
independently verifiable change. It improves the feedback loop when the slice's
outcome can be expressed in a practical executable test; it is not a universal
Dev requirement or a substitute for `$dev-test`.

Read the coherent outcome, acceptance evidence, dependency boundary, and
selected mode from the current brief or selected `$dev-planner` plan. Keep the issue, product contract, and
slice boundary fixed. Do not add a TDD-only slice, promote a fixture into a
product requirement, or use a passing test as proof that a new behavior was
implemented.

## Decide Before Writing a Test

Apply the [mode contract](../../dev/references/development-mode-contract.md#standard-and-strict-modes)
first. In standard mode, TDD is opt-in through an explicit user/repository request;
a testable boundary alone does not select it. Bug tickets still retain a focused
repro/regression test. An ordinary failing repro before its fix is distinct from
reverse-red mutation of a working implementation. Strict may select useful TDD;
neither mode requires a mutation matrix as part of red/green/refactor.

Apply TDD when all of the following are true:

- the planned outcome has an observable result at a public API, user workflow,
  persisted state, protocol boundary, or other owned behavior boundary;
- the repository has (or can safely gain) a focused, runnable test surface;
- a failing test can distinguish the missing behavior or the reported
  regression without relying on timing, a live third party, or incidental
  implementation structure; and
- the test can run often enough to guide the small implementation step.

Otherwise record `TDD Decision: adapt` or `TDD Decision: decline` with the
specific constraint and the strongest practical alternate evidence. Do not
force TDD for visual judgment, exploratory investigation, non-deterministic
provider behavior, hardware/device state, human approval, or a boundary where
the only possible test would be a tautological mock.

For a legacy seam, adapt before declining when a small, behavior-preserving
test seam can expose an owned input/output boundary. Prefer a characterization
test or contract-level test over asserting private calls. State why the seam is
safe, then run the meaningful red/green cycle against the behavior it exposes.

For a non-testable external boundary, test only the owned request construction,
response translation, retry/timeout policy, or persisted result with a
deterministic fixture when that proves an owned contract. A fake provider does
not prove the provider's live behavior. Record the remaining live boundary and
route its verification to `$dev-test` or `$release` when the plan requires it.

## Red, Green, Refactor

For `TDD Decision: apply` or an adapted seam:

1. **Red:** write or adjust one focused test for the planned observable
   outcome. Run the exact command before the production-behavior change and
   preserve the failure: test name, expected-versus-actual result, command, and
   relevant output. For a regression, first demonstrate the supplied
   reproduction through that test or retain an equivalent focused repro.
2. **Green:** make the smallest production change that makes the same test
   pass. Run the exact command again and preserve the passing result. Do not
   broaden the feature, rewrite unrelated code, or weaken the assertion to
   obtain green.
3. **Refactor:** after green, improve duplication, naming, or structure only
   when it preserves the tested behavior; rerun the focused test. If the green
   change is already the clearest small form, record `Refactor: none needed`
   rather than inventing churn.

Test behavior rather than implementation trivia. Assert observable output,
state transition, public contract, error, persistence effect, or user-visible
workflow. Do not make a private helper, internal call count, mock wiring, or
file layout the pass condition unless that mechanism is itself an explicit
public compatibility contract.

In fast mode, the selected slice still needs its focused red/green evidence.
Record optional broader integration, live-provider, hands-on, and exhaustive
edge evidence under `Skipped / Unverified` rather than claiming TDD proves it.
In standard mode, pass the TDD evidence to `$dev-test` as an input;
it does not reduce that skill's required validation bar.

## Output

```markdown
## TDD Result

### Planned Slice
- Outcome: <verifiable-slice outcome>
- Acceptance Evidence: <planner evidence consumed>

### TDD Decision
- <apply | adapt | decline>: <concrete reason tied to the observation point or boundary>
- Alternate Evidence / Remaining Boundary: <test seam, contract fixture, manual/live verifier, or none>

### Red / Green / Refactor
- Red: `<command>` - <meaningful failing expected-versus-actual result, or not run with decision reason>
- Green: `<command>` - <same behavior test passes, or not run with decision reason>
- Refactor: `<command>` - <passes after behavior-preserving cleanup | none needed | not run with decision reason>

### Behavior Boundary
- Asserted: <observable behavior>
- Avoided: <implementation-trivia assertion or artificial mock>

### Skipped / Unverified
- <mode-specific or external-boundary omission, or None>

### Next Evidence
- Keep red/green/refactor in the same implementation owner. Apply `$dev-test` for formal validation and return evidence to the controller; no extra implementer dispatch is required.
```
