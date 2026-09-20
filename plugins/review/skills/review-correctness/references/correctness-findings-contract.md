# Correctness Findings Contract

Contract version: `1`

`$review-correctness` is an isolated specialist for demonstrable correctness
defects in one frozen pull request or immutable diff. It is not a reviewer
orchestrator, a Finding Judge, Product Review, or Design Review.

## Finding Bar

Emit a finding only when all of the following are true:

1. A concrete triggering scenario is available, including relevant preconditions
   and the action or input that reaches the changed behavior.
2. The expected and actual affected behavior differ in a way attributable to
   the frozen change or its violated interface contract.
3. Evidence ties the scenario to the diff and to a relevant caller, consumer,
   state transition, or contract boundary. Cite paths, symbols, tests, or
   reproducible commands precisely enough for another reviewer to check.
4. Confidence is `high`; uncertainty about an unavailable caller, runtime
   dependency, data shape, or contract is a reason to withhold the finding.
5. The remediation direction is bounded to the faulty behavior. It must not
   prescribe an unrelated redesign or broad refactor.

Accepted categories are concrete defects, regressions, state or edge-case
failures, and contract violations. A compatibility break is a contract
violation only when an affected consumer or documented interface proves it.

## Exclusions

Do not emit findings for architecture preference, aesthetics, naming, unusual
but functioning code, hypothetical hardening, or a missing test by itself.
Do not infer a defect from a diff without tracing the changed behavior. Do not
turn incomplete context into a speculative finding.

Withhold an individual candidate when its necessary evidence is unavailable;
retain unrelated confirmed findings. This alone does not make the review
incomplete. Use `context insufficient` only if the missing evidence prevents
inspection of a required part of the assigned surface; name that coverage gap
and retain any proven findings. A completed `no findings` result means no
candidate met this lens's bar, not that unrelated review lenses passed.

## Required Finding Shape

```markdown
### [severity] Concise defect title

Confidence: high

Triggering scenario: <preconditions and action/input>

Affected behavior: <expected behavior versus observed behavior>

Evidence: <changed path/symbol plus caller, consumer, test, contract, or command>

Bounded remediation: <smallest direction that restores the affected behavior>
```

Severity describes the demonstrated impact, not code style. If a finding cannot
be written in this form with concrete evidence, do not emit it.
