# Develop Handoff Contract

This Product-owned contract defines what PM promises when one issue is handed
to an engineering workflow. It does not copy or control the Develop plugin's
internal lifecycle. If `$dev` is unavailable, return the complete handoff packet
instead of pretending engineering started.

## Delivery Mode

Resolve `fast`, `standard`, or `strict`. Omitted mode resolves to `standard`.
Carry strict unchanged: standard blocks P0/P1, strict blocks P0/P1/P2.
Apply [Acceptance Classification](../../pm-spec/references/acceptance-policy.md#unattended-engineering-acceptance)
before carrying QA, acceptance surfaces and runtime thresholds as named
requirements. Preserve mode waivers and separate human follow-ups on resume. The mode alone does not
add hands-on QA or a broader validation bundle. Do not invent other aliases.

| Mode | Product meaning | Required disclosure |
| --- | --- | --- |
| `fast` | The user explicitly prefers unattended primary-path delivery with optional review, hands-on QA, human acceptance waiting, and broad validation allowed to be skipped by Develop. | Preserve every known omission under `Skipped / Unverified`; never describe skipped work as passed. |
| `standard` | Default unattended engineering with normal automated validation, review and CI. | Carry simulator/seed/mock evidence, waived real-environment tests and any separate human acceptance follow-up; they do not block engineering. |

| `strict` | Same selected stages as standard, with P0/P1/P2 defects blocking and P3 advisory. | Preserve mandatory acceptance separately from defect severity. |

Every PM handoff carries:

```markdown
Mode: <fast | standard | strict>
Skipped / Unverified: <entries or none>
```

Product decides whether the approved outcome is clear enough to build. Develop
owns its current validation, review, merge, deployment, and completion rules.

## Resume Evidence

A PM handoff is resume-safe only when it identifies the canonical issue
description revision, PM root and combined PM Handoff/readiness evidence. A
legacy separate review/handoff pair remains usable when current; do not require
both old and new formats or a new comment solely for migration. On a
resume, Dev rehydrates those records together with live branch/PR/head/CI/Review
state before any mutation. PM reuses the existing root and stage replies; a
changed canonical requirement names the dependent Dev gates that require fresh
evidence rather than resetting unrelated completed work.

## Production Loop Contract

Apply the unattended acceptance rule first: later real-environment evidence may
be materially necessary without being an engineering completion gate. Keep it
unverified with a separate human follow-up when warranted.

Use a production loop when an implementation can pass ordinary repository tests
yet fail only under representative scale or data, a real runtime/provider,
migration or rollout conditions, external interoperability, or a measurable
performance/resource threshold.

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
Iteration / Escalation: <limit and condition requiring a decision>
```

Keep two decisions separate:

- **Development readiness**: engineering has enough product and technical
  context to begin safely.
- **Outcome-verification readiness**: the required environment, verifier,
  threshold, permissions, and budget are executable.

Missing implementation-owned verifier details may block outcome completion
without blocking development. They block development only when the unknown
changes product scope, architecture, safety, or the acceptance boundary.

Product supplies the outcome, product-known constraints, environment fidelity,
and pass threshold. It must not invent production access, implementation-owned
commands, or a verifier. Develop or Release owns execution and durable evidence.
