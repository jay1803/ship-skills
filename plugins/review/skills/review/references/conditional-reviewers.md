# Conditional Reviewer Signals

Architecture, test, security, and integration reviewers are non-discoverable,
one-shot prompts. Use this reference only after the three core source artifacts
return. A concrete signal in the frozen diff or a verified core artifact is
required; risk labels, issue metadata, intuition, or broad desire for more
confidence are not signals.

Apply the [mode policy](severity-policy.md#review-depth-and-test-expectations)
before signaling: optional omitted coverage is not a required gap.

Evaluate signals once. Dispatch all signaled prompts against the same frozen
target in isolated contexts. Do not evaluate conditional outputs for more
signals and do not create a recursive second wave.

A core finding does not short-circuit this generation. Finish the signal
evaluation and every signaled one-shot reviewer before judgment. Neither an
individual core result nor a conditional result may route implementation or CI
repair; only the final accepted combined artifact may do that.

## Architecture

Signal when evidence shows a changed ownership boundary, persistent data
model, public interface, dependency direction, or cross-module lifecycle whose
structural validity is not covered by a concrete core finding.

Prompt focus: inspect only the signaled boundary on the frozen diff. Determine
whether ownership, dependencies, lifecycle, and compatibility preserve the
repository's established architecture. Return evidence-backed blocking or
advisory findings and a bounded remediation direction. Do not perform general
code quality or specification review.

## Test

Signal when mode-required behavior lacks relevant executable coverage, existing
tests contradict the new behavior, or a core finding's reproduction/repair
depends on a concrete test boundary.

Prompt focus: inspect only the signaled behavior and test surface. Identify a
specific untested regression path, false-positive/false-negative test, or
missing deterministic proof. Distinguish required regression coverage from
optional breadth. Do not judge general code style or product scope.

## Security

In standard, signal a concrete exposure or unresolved reachable threat at a
changed trust boundary, not the mere presence of auth/input/security code.
Strict may additionally signal changed authentication, authorization, secrets,
untrusted input, cryptography, privacy, destructive access or privilege boundaries.
In both modes name the actual boundary and inspection question.

Prompt focus: trace the exact signaled trust boundary and demonstrate the
attacker/input/precondition, affected asset, behavior, and bounded mitigation.
Withhold speculative hardening. Preserve privacy and authorization findings as
engineering judgments distinct from specification compliance.

## Integration

Signal when the change crosses services, providers, schemas, migrations,
deployment contracts, compatibility promises, or version-skew boundaries.

Prompt focus: inspect the exact producer/consumer or rollout boundary. Identify
a reproducible mismatch, ordering hazard, compatibility break, or missing
integration evidence with a bounded remediation. Do not broaden into release
management or provider invocation.

## Result Contract

Each prompt returns native Markdown with its decision, evidence, findings, and
withheld items. Wrap it in the Review v2 source artifact envelope without
changing its bytes. If a signaled prompt cannot run, cannot inspect the target,
or cannot produce a verified artifact, record the signal and missing source so
the judge selects `coverage-blocked`.
