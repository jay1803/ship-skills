# Validation Evidence And Gate Effects

Use when reporting mixed check results, comparing a baseline failure, or carrying
an exception through Test, Verifier and merge. Extend the existing Test Result;
do not create a second acceptance ledger or ask later owners to reconstruct logs.

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

Keep three facts together: **observation**, **failure attribution**, and
**permitted next stage**. For example, exit 1 with three XCTest failures and a
green Swift Testing summary is Failed overall. Reproducing the same three on
the base supports a baseline attribution; it does not authorize excluding them.

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
