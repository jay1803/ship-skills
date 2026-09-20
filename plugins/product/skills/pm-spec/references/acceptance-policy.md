# Acceptance Classification

Use when drafting, canonicalizing, or checking ticket acceptance. Separate
**Required outcomes** from **Nonblocking recommendations**. Required outcomes
prove the confirmed primary promise and carry their source. P2/P3 defects,
polish, and improvements are nonblocking by default; do not put them in a
mandatory checklist, readiness gate, or required validation section. Record
useful recommendations separately with their priority and deferred status.
Omit an empty recommendations section.

An exception making a P2/P3 item mandatory needs an explicit instruction from
the requirement owner covering that item (or a clearly bounded class), or an
independently binding repository/CI/security obligation with its source. A
heading, repeated checklist entry, generic approval, or agent preference is not
such authority. Preserve explicit strict review selection as a delivery gate;
it does not rewrite the ticket's product acceptance.

These P-levels describe findings, not the tracker's scheduling priority. A
P2-priority feature ticket still has a required primary outcome. Do not assign
invented P-levels to every product requirement or demote the user's request
because the issue has a normal priority.

When consuming an older ticket, retain original wording and show any applicable
later instruction, superseded gate, and current gate effect. Do not silently
rewrite historical evidence. An explicit instruction to record P2/P3 without
fixing them applies to acceptance items too when the issuer controls that
requirement; carry it through Dev and Review. A skip stays skipped, a failed
observation stays failed, and independent CI, safety, permissions, and branch
protection still require their own evidence and authority.

## Unattended Engineering Acceptance

For standard delivery (also when mode is omitted), write required product
outcomes so engineering can validate them with simulator/local runtime, seed
accounts and suitable mock E2E. Strict retains the same validation boundary;
severity alone does not require a person or real environment.

Physical-device, real-account, live-environment/provider tests and named-human
sign-off are nonblocking recommendations for engineering, even when an older
ticket calls them mandatory. Preserve the original requirement and record the
effective mode waiver; do not delete product behavior or call skipped evidence
passed. Missing real credentials, devices or human availability does not block
readiness, PR, merge, engineering Done or successors. Applying this mode rule
is not a new product decision requiring another confirmation.

When real-environment acceptance is materially necessary, it may be a separate
human-owned follow-up ticket. Record the concrete reason simulated evidence is
insufficient for that later acceptance, build/revision, tester or role, safe
access/data prerequisites, steps, expected results and evidence/accepted-by/date
fields. Reuse an existing ticket. Otherwise hand the draft to
`$pm-project-orchestrator` for creation within existing tracker authorization;
without that authority or tool support, return the draft and continue engineering.
Keep routine skipped tests in recommendations rather than manufacturing tickets.

Only the separate acceptance ticket carries `human-acceptance-required` for
this deferred work. It may be blocked by the implementation/build, never the
reverse, and stays outside engineering completion barriers. Do not dispatch it
as a coding worker or require it to become dev-ready. Human acceptance remains
unverified until a person supplies its evidence; a merged PR cannot close it.

Readiness review checks for unattended blockers: devices, personal credentials,
interactive sign-in, named testers, live deployment and required human approval
of tests. Route canonical wording/label corrections to their PM owners and carry
the waiver in the handoff; the paperwork itself must not stall an otherwise ready
implementation. Preserve real product ambiguity, failed automated checks,
implementation dependencies, enforced CI and merge/release authority. An explicit
standalone live-validation request retains its own completion contract.
