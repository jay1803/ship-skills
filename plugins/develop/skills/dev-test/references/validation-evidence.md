# Validation Evidence And Gate Effects

Use when selecting targets/fidelity, reporting mixed check results, attributing
or comparing a failure, or carrying an exception through Test, Verifier and merge. Extend the existing Test Result;
do not create a second acceptance ledger or ask later owners to reconstruct logs.

## Target And Harness Readiness

Before an expensive suite, resolve the required check's target/scheme, suite or
test selectors, configuration and environment from its governing source. Choose
the smallest sufficient invocation; an app scheme may include unrelated UI tests.
Keep every explicitly required suite in the validation brief even when a focused
run comes first. An interrupted broad run supplies only observed partial evidence;
it neither passes the unrun remainder nor proves a focused run replaces that floor.

For selected UI evidence, name the changed component and interaction before
building a harness. Exercise the actual input control when input behavior is the
claim; a read-only display row does not prove typing, focus or editing. Record
the head, component/harness, data and state with inspected screenshots or other
required observations. A component fixture proves that component at fixture
fidelity; full navigation or end-to-end claims need their own selected evidence.

When a fixture run fails before reaching the intended boundary, check the
cheapest observable prerequisite before another full run: the injected client,
query entry, seed result or callback actually reaches the component under test.
Zero observed calls/data is a harness-readiness symptom, not proof of an app
defect or a confirmed injection root cause. Preserve the observation, repair
setup through its existing owner or escalate unknown behavior, then retry the
targeted path within the existing budget. Do not weaken assertions or expand
product scope to make the harness pass. This conditional check adds no universal
smoke phase to checks whose inputs are already established.

## One observation, separate conclusions

For each executed or reused command retain its source artifact, exact invocation,
head/base or immutable inputs, environment, actual command exit/completion state,
and summaries from every test framework or phase that ran. Capture the check's
exit, not only a log formatter or `tee` process. Keep failed test identities and
any truncated/missing summary explicit; prefer an existing structured report
when available. No particular test framework or new parser is required.

- A nonzero completed test command is Failed even if the last framework is green.
- Exit zero does not erase a reported failing test. Contradictory or incomplete
  evidence cannot support an all-passed claim; inspect the retained report.
- A timeout/interruption is incomplete or blocked, with observed failures kept.
  It is not a completed suite pass or proof that only known failures remain.
- A later successful rerun is a separate observation; it does not rewrite the
  earlier failure. Record which result supports the current gate and why.

Keep three facts together: **observation**, [failure attribution](#failure-attribution), and
**permitted next stage**. For example, exit 1 with three XCTest failures and a
green Swift Testing summary is Failed overall. Reproducing the same three on
the base supports a baseline attribution; it does not authorize excluding them.

## Failure attribution

Attribute each failure as change-caused, pre-existing (reproduced on the
base), flaky (differs across identical reruns), environment or external
(runner, dependency or service outage, credentials/secrets, third-party
provider), out of scope, or unknown until evidence decides. Attribution selects
the owner; it never turns a failed observation into a pass.

## Baseline and exact exception

Compare baseline evidence only with matching command/configuration, dependency,
environment and failure identities. Reuse a current inspectable comparison
rather than repeating a broad suite just because the next owner changed.
Unknown attribution remains unknown; do not repair unrelated baseline code or
expand the approved scope merely to make the suite green.

If the applicable user/repository authority explicitly permits an exception,
carry its actual source, exact quoted instruction, affected failure identities,
revision/input applicability, permitted stages and required alternative evidence
in the same Test Result. Baseline attribution alone, a P2 label, or a waiver of
live-environment tests is not this authorization. A failure exception cannot
bypass independently required CI, protection, permissions or safety gates.

The original command stays Failed. An authorized filtered command is a distinct
Passed/Failed observation with its exclusions, current inputs and coverage
limits. State whether PR preparation, review, merge or only a narrower action
is permitted; do not infer merge permission from permission to create a PR.
A fourth failure, changed failure identity or uncovered head invalidates that
exception's application to the new observation. Preserve still-valid evidence
and route only the new gap to its owner.

Downstream Verifier and merge consume these same records. They recheck freshness,
authority and their own gates, without turning Failed into Passed or demanding
that an already-resolved exception be approved again. In the claim ledger,
retain an exempt observation's actual outcome and explicit nonblocking effect;
assess completion against the remaining required claim set. Report engineering
gate eligibility separately from an unqualified all-tests-passed statement.
