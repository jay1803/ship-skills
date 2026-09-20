# Production Loop Contract

Use this contract when an implementation can look correct in ordinary tests yet still fail only under real scale, representative data, external interoperability, rollout or migration conditions, or another measurable runtime constraint. It makes those constraints part of the Dev loop without turning every issue into a production experiment.

## Applicability

Apply the [unattended validation rule](development-mode-contract.md#unattended-validation-and-deferred-acceptance)
before treating a loop as an engineering gate. A material need for later real
evidence belongs in a separate human acceptance follow-up; it does not require
real credentials, devices or deployment during standard engineering delivery.
Keep its fidelity and threshold intact and unverified, while running the
applicable simulator/seed/fixture validation.

Mark `Production Loop: required` when at least one material acceptance risk depends on:

- production-scale or representative data;
- a real runtime, provider, platform, migration, or rollout environment;
- measurable performance, memory, reliability, or resource limits;
- compatibility judged by software or a service outside the implementation worktree; or
- an open-ended objective that must improve against an external metric.

Use `Production Loop: not required` when normal repository validation, review, and any separately defined human acceptance can directly prove the outcome. A subjective product decision belongs in Human Acceptance, not in this contract.

## Contract

Record the smallest sufficient contract:

```markdown
Production Loop: <required | not required>
Outcome: <observable result>
Hard Constraints:
- <constraint that must remain true>
Environment / Data: <fixture, representative, production-scale, or live surface>
External Verifier: <command, harness, service, library, metric, or none>
Verifier Independence: <agent-authored | repository-controlled | external/immutable>
Pass Threshold: <measurable success condition>
Verification Timing: <pre-merge | post-deploy | both>
Resource Budget: <time, compute, cost, requests, or not constrained>
Iteration / Escalation: <limit and the condition that requires a decision>
```

PM supplies the product-known outcome, constraints, required environment fidelity, and pass threshold. Engineering may complete implementation-owned details such as the exact harness command or safe execution environment. Mark unknowns explicitly with an owner; do not invent a verifier or production access.

## Readiness

Keep two decisions separate:

- **Development readiness**: engineering has enough product and technical context to begin safely.
- **Outcome-verification readiness**: the required environment, verifier, threshold, permissions, and budget are executable.

Missing implementation-owned verifier details do not automatically block development. They block an outcome-complete claim, and they block development only when the unknown changes product scope, architecture, safety, or the acceptance boundary.

## Evidence Record

For every verifier run, record both dimensions instead of collapsing all checks into a generic `passed` result:

```markdown
Environment Fidelity: <fixture | representative | production-scale | live>
Verifier Independence: <agent-authored | repository-controlled | external/immutable>
Command / Surface: <exact command, harness, service, or metric>
Observation: <measured result or failure symptom>
Threshold Result: <pass | fail | blocked>
Evidence: <logs, report, artifact, URL, trace, or other durable evidence>
```

An agent-authored test can be useful without being independent. A production-scale run can expose realistic failures without proving correctness if the verifier is weak. Claim the contract passed only when the recorded fidelity and independence satisfy its stated requirements.

## Controller Ownership

`$dev` controls the loop. `$dev-test` captures observations and verifier evidence;
`$dev-implementer` applies one scoped change at a time. Neither worker changes
the goal, threshold, verifier, or resource boundary independently. Complete
implementation-owned contract details during planning; return to PM only when
an unknown changes product scope, safety, the user promise, or acceptance.
Apply existing same-check and review/CI repair limits unless the loop contract
sets a lower resource or iteration boundary.

## Loop Rules

1. Run the implementation against the contract's environment and verifier.
2. Preserve the observed symptom before changing code or tests.
3. Record the current hypothesis, scoped change, and next verifier run.
4. Do not weaken, replace, or edit an external verifier merely to obtain a pass. If the verifier is wrong, stop with evidence and obtain the appropriate owner decision.
5. Keep production data, credentials, deploys, and external mutations within the workflow's existing authorization and safety boundaries.
6. Stop at the contract's iteration or resource limit and report the last observation, attempted hypotheses, remaining uncertainty, and next decision.

## Completion

- A required pre-merge verifier must pass before merge handoff can merge into the resolved issue PR base.
- Apply mode waivers before pre-merge or post-deploy gates. A waived real-environment verifier stays unverified without holding engineering Done or successors open. A remaining enforced test-environment verifier keeps its actual pending/fail/pass state; never bypass enforcement.
- A failed test-environment verifier returns control to `$dev` for a new bounded repair cycle or an explicit escalation decision. A production-only verifier belongs to `$release` and the project deploy skill.
- Deferred human acceptance has its own ticket and evidence boundary, not an engineering gate. Record the omission under `Skipped / Unverified` without claiming acceptance.
