# Review Severity And Release Threshold

This is the canonical defect-threshold policy. Review owns this source;
Develop ships a byte-identical package-local mirror. Explicit user policy may
change a threshold or defer acceptance within the issuer's authority, but
cannot relabel evidence, authorize writes, or bypass independently required CI,
safety, permissions, or repository policy.

## Severity

Use demonstrated impact, reachable conditions, scope, recoverability, and
confidence. Effort to fix and number of changed lines do not determine severity.

| Level | Meaning | Representative impact |
| --- | --- | --- |
| P0 | Critical emergency requiring immediate action | Widespread outage, catastrophic data loss, or an actively exploited critical boundary |
| P1 | Serious defect that must be fixed before delivery | Core path unavailable, permanent loss/corruption of important data, exploitable authorization bypass, or process failure under realistic conditions |
| P2 | Confirmed bounded defect that can normally be scheduled | Limited noncritical behavior failure, recoverable degradation, or a usable workaround |
| P3 | Low-impact defect or optional improvement | Minor usability/copy issue or local maintainability improvement |

Examples guide judgment; a rare trigger is not automatically low severity when
impact is irreversible. Cite the scenario and consequence. An unproven concern
is withheld with missing evidence, not assigned a convenient lower priority.
Native specification classifications and optional-improvement labels remain
intact alongside any source-authored P-level. Do not convert Linear's numeric
priority enum or an unlabeled `blocking`/`medium` word mechanically into a P-level.

## Mode Gate

- Standard (also the default for a standalone review): confirmed P0/P1 block.
  P2/P3 remain visible advisories. A complete current generation with no P0/P1
  advances the technical gate without another advisory-only fix/review cycle.
- Strict: confirmed P0/P1/P2 block; P3 may remain. It uses the same selected
  lifecycle surfaces, with deeper risk-selected failure, recovery, concurrency
  and security inspection; it does not automatically add reviewers, models,
  manual testing, exhaustive cases or per-assertion mutations.
- Fast retains its separately defined omissions and unskippable conditions.
  If Review is explicitly selected in fast mode, use the standard defect gate
  unless the caller explicitly supplies a stricter threshold.

Small nonblocking fixes may join an already-required repair batch when scoped,
low-risk, independently verifiable, and not forbidden by the user. An explicit
"record P2/P3 only; do not fix" instruction excludes those items even from a
batch that already contains P1 repairs, including acceptance-related findings. They do not create a new repair round
or expand acceptance. After a nonblocking generation, record remaining items
and advance; do not edit the reviewed head just to polish it. An explicitly
requested advisory fix is new authorized scope and needs current validation.
Any change invalidates affected exact-head evidence; never reuse old approval
as if no edit occurred.

P2/P3 acceptance recommendations are nonblocking by default. A checklist heading
alone cannot make them mandatory. Preserve the confirmed primary outcome;
Linear issue priority is not finding severity. An explicit stricter policy or
item/bounded-class requirement authority can make a P2/P3 item blocking; record
that source. Do not invent acceptance to bypass the selected defect threshold.

A later explicit user instruction may defer a requirement the user controls,
including a confirmed P2/P3 acceptance violation. Keep the original requirement,
finding and failed evidence; record the exact instruction and current gate
effect using the assembly contract. A threshold override alone does not defer
required proof. Independent CI, safety, permissions, required review coverage,
and branch protection remain separate gates. Missing or ambiguous authority
returns to its owner rather than silently waiving a requirement.

## Review Depth And Test Expectations

Standard focuses on required behavior, primary flows and concrete regressions.
Missing unrelated edge-case tests or reverse-red evidence is not itself a finding,
coverage gap or reason for a repair round. A bug ticket needs relevant regression
coverage; existing relevant failures and explicitly required checks remain visible.
Do not invent broader acceptance from a desire for more tests. Strict inspects
related failure, recovery and concurrency boundaries and may select targeted
mutation evidence when useful; breadth alone is not a quality measure.

For standard security inspection, use the actual deployment and exposure: do not
apply a multi-tenant/public-service threat model to a local personal tool without
evidence. A security concern needs a concrete reachable input/actor, affected asset
and consequence tied to this change. Preserve directly introduced credential
exposure, cross-account access and irreversible data damage. Do not demand generic
hardening, extra permission layers or hypothetical attack matrices. Strict can
inspect additional changed trust-boundary failure paths; speculative findings
remain excluded. A personal-project label never excuses a demonstrated defect.

Apply this scope to core lenses, conditional signals and Judge. Pass the selected
mode and explicit requirement sources in the review packet. Default omissions
are not missing required coverage; observed defects retain their severity and
explicit user/repository requirements retain their authority.

## Severity Clarification

Judge preserves native labels and does not regrade. When a confirmed candidate
lacks a P-level needed for the gate, or supplied findings materially disagree
about whether the same demonstrated consequence crosses it, return a named
clarification request to Review. Review asks only the originating source for
its impact/preconditions and source-authored level on the same target, retaining
the original and the additive reply. Do not start another full wave or ask
siblings to vote. Unresolved gate-relevant ambiguity blocks the decision;
ordinary source-native optional advice and withheld hypotheses do not.

Keep requirement-completeness findings separate from engineering priority.
A later level change must explain new evidence or different conditions; do not
silently overwrite earlier labels or count repeated mentions as new defects.
