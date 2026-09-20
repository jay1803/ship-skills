---
name: pm-readiness-review
description: Assess whether one issue has sufficient confirmed product scope and acceptance evidence to begin development; return one combined readiness and Dev handoff result.
metadata:
  owner: jay1803
  family: product
  maturity: stable
  distribution: product
---

# PM: Readiness Review

Assess the current product contract for engineering. Verify the evidence and
real gaps rather than whether every PM stage left a comment. Keep independent
judgment separate from repairing scope or writing specifications.

For standalone assessment, use the
[artifact contract](../pm/references/artifact-contract.md). For issue work, use
the [state machine](../pm/references/issue-state-machine.md) and
[tracker contract](../pm/references/tracker-contract.md).

## Evidence and judgment

Read the canonical issue, current route, relevant decisions, dependencies and
applicable review/design evidence. Reuse fresh controller context; expand into
history when authority or a conflicting requirement needs resolution. If intake
is already evidenced but the PM root is missing, initialize the one root under
the tracker contract. Missing classification routes to `$pm`.

Check:

- The user/operator, observable outcome, confirmed core behavior, meaningful
  scope and critical acceptance are understandable from the canonical issue.
- Material rules have valid provenance, including exact later overrides.
  No unresolved agent proposal or contradictory active product requirement is
  embedded as decided. Use
  [decision provenance](../pm-spec/references/decision-provenance.md) when unclear.
- The route has `delivery_shape: single`. Return `split` for proven `multi` or
  `blocked` for `ambiguous`, both to `$pm-project-orchestrator`. Do not invent
  children or infer multiple outcomes from file count, layers, time or QA.
- Start-relevant dependencies and product constraints are sufficient. A named
  technical-stage comment is unnecessary when the underlying evidence exists.
  Engineer-owned architecture and verifier mechanics are not PM prerequisites.
- Any Solution Review required by the state machine covers the current inputs.
  Reuse its result; do not repeat the full simplification audit. If inapplicable,
  carry the reason. An authorized skip stays disclosed, not approved.
- Needed interaction/screen decisions are available from existing evidence or
  Design. Text specifications suffice when no visual artifact is required.
  Design proposals do not authorize new retention, permission, fallback or
  other product policy.
- For Bugs, expected behavior and sufficient diagnosis support the canonical
  restoration contract. A Spec verification can suffice without rewriting
  accurate text. New behavior still needs product confirmation.

Apply [Acceptance Classification](../pm-spec/references/acceptance-policy.md).
P2/P3 recommendations and waived human/device/live testing do not become
engineering gates. Preserve strict severity, failed automated checks and real
implementation dependencies. An older acceptance label or deferred human
logistics may need owner updates; carry the verified waiver immediately.

Use the [Develop handoff contract](../pm/references/develop-handoff-contract.md)
for mode and conditional runtime evidence. Report development readiness
separately from outcome-verification readiness; missing evidence logistics
block development only when they change the implementation boundary or safety,
not merely because later real-world evidence remains unverified.

## Result and writes

Return `ready`, `blocked`, `split`, `reject` or `defer`, with the actual gap and
next owner. If an upstream owner already has an unresolved decision, return it
without another blocked tracker comment. If this assessment discovers a new gap,
record it once and route repair to its owner. Do not edit title, description or
scope, or interpret a review request as authority to launch Dev.

Return the gate and handoff in one payload. When publication is authorized,
create/update the single `## PM Handoff` reply under the verified root. Consume
legacy separate Readiness/Handoff evidence without manufacturing another pair.
The PM controller completes authorized tracker sync and next dispatch in that
same record. Readiness is valid only for its bound canonical state; no completed
sync or engineering launch may be claimed before it occurs.

```markdown
## PM Handoff

Issue / Repository: <exact target>
PM Thread: <verified root URL>
Canonical Revision: <revision or updatedAt and relevant source binding>
Decision: <ready | blocked | split | reject | defer>
Delivery Shape: <single | multi | ambiguous, decisive evidence>
Development Readiness: <ready | blocked>
Outcome Verification Readiness: <not required | ready | unverified - engineering may proceed | blocked - blocks development>
Solution Review: <applicable result/link | not applicable and reason | skipped by user and source>
Critical Acceptance / Constraints: <only essentials or canonical links>
Dependencies / Existing Implementation: <start conditions and relevant issue/PR evidence>
Design / Runtime Evidence: <only material evidence, limits and missing owners>
Mode: <standard | fast | strict>
Skipped / Unverified: <actual omissions, failures remain failures>
Required Before Build: <actual gaps or none>
Tracker Sync: <verified fields or unapplied/pending>
Next Route: <exact owner and authorized endpoint>
```

Omit empty optional fields. Detailed tests, source audits and design content
remain at their links. A blocked result is an assessment, not a Dev-ready handoff.
