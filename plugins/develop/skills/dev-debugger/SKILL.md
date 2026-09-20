---
name: dev-debugger
description: "Diagnose an observed defect, regression, crash, or unexplained test failure and return an evidence-backed root-cause brief before repair."
metadata:
  owner: jay1803
  family: develop
  maturity: stable
  distribution: develop
---

# Dev: Debugger

Diagnose bugs through `Reproduce → Explain → Fix → Prove` before any code
change. The output is an evidence-led root-cause brief that lets the Dev
workflow plan and implement a narrow fix without guessing.

Use current repository evidence for bug tickets, regressions, crashes, hangs, wrong behavior, and field-only defects; investigate before planning only when a technical decision still needs the diagnosis. Do not implement the fix in this role unless the user explicitly asks.

## Reference Selection

Start from the changed surface or diagnostic evidence, not the repository label. Reuse current context that matches the target files, version, environment, and acceptance boundary. Read or load a specialist only when its workflow or an unresolved platform question is needed for the selected task; inspect additional project areas when a concrete dependency or evidence gap reaches them. Repository instructions and required validation still apply. If none of the listed platforms applies, use the shared workflow and repository guidance rather than forcing a match.

Read the shared workflow, then the matching reference(s) from `references/` when applicable:

- iOS app, iOS simulator/device-only bug, Xcode iOS target, UIKit, App Intents, crash, hang, memory, performance, or iOS runtime behavior: [debug-ios.md](references/debug-ios.md)
- macOS app, AppKit, macOS SwiftUI scene/window/menu, sandbox/TCC, signing, entitlement, packaging, crash, hang, performance, or macOS runtime behavior: [debug-macos.md](references/debug-macos.md)
- SwiftUI state, layout, navigation, sheet, animation, accessibility, preview, performance, identity, or view lifecycle bug: [debug-swiftui.md](references/debug-swiftui.md)
- Frontend web, React, Next.js, Vite, browser behavior, hydration, routing, responsive layout, client state, accessibility, or web test failure: [debug-web.md](references/debug-web.md)
- Backend/API/service bug that is not primarily Supabase: [debug-backend.md](references/debug-backend.md)
- Supabase schema, migration, RLS, Auth, Edge Functions, Storage, Realtime, generated types, or Supabase integration defect: [debug-supabase.md](references/debug-supabase.md)

Multiple references are allowed when the bug crosses surfaces. Pair `debug-swiftui.md` with `debug-ios.md` or `debug-macos.md` when app-level runtime evidence matters.

## Scope Gate

- Use for defects: crash, hang, regression, incorrect output, broken UI, wrong data, performance issue, flaky behavior, failed acceptance check, field report, or reproducible test failure.
- When an observed defect also exposes feasibility or third-party API uncertainty, diagnose the defect here first, then route the remaining unknown to `$dev-spike` or `$dev-api-research`.
- For a failure first discovered during post-implementation validation, enter only from an evidence-bearing `$dev-test` handoff after that phase confirms root-cause investigation is still needed. Do not take ownership of every first red local command.
- Do not use for new features, product ambiguity, strategic priority, PR review comments, or failing CI infrastructure. Route those to PM, `$dev-implementer`, or `$dev-ci-repair`.
- Do not re-ask for evidence already present in the PM bug triage brief, issue, comments, screenshots, logs, stack traces, or attachments.
- Do not invent root-cause confidence when the available evidence cannot distinguish the leading causes. Design the smallest useful observability change, collect the missing evidence, and resume diagnosis instead.
- If the report is not actually a bug, stop with the reason and route back to `$pm-readiness-review` or the correct Dev role.
- If a PM bug triage brief is present, treat its expected behavior, actual behavior, severity, user impact, affected platform, environment, workaround, and open questions as the product source of truth unless newer tracker comments supersede it.
- When invoked inside a PM-only kickoff or diagnosis pass that does not authorize implementation, return a successful diagnosis to `$pm-spec` in Bug Synthesis Mode. Do not skip the canonical issue record by routing directly to Dev planning.

## Reproduce → Explain → Fix → Prove

Before code is modified, establish either a reproducible symptom or an explicit
evidence gap that prevents reproduction. A report, a guessed root cause, or a
plausible patch is never enough to enter Fix.

### Reproduce

1. Resolve the bug ticket and any PM bug triage brief. Capture expected and
   actual behavior, affected platform, environment, severity, user impact,
   reported frequency, regression window, workaround, open questions, and
   available evidence.
2. Load the relevant `debug-*.md` reference(s), then preserve issue text,
   comments, attachments, logs, crash reports, screenshots, failing tests, CI
   output, reproduction steps, and repo context before clearing state or
   changing behavior.
3. Attempt the smallest faithful reproduction according to
   [`../dev/references/development-mode-contract.md`](../dev/references/development-mode-contract.md).
   Record exact steps, environment/version/configuration, attempt count,
   observed result, and any mismatch with the report. Fast mode may use an
   existing focused test or non-interactive primary-path evidence; it must
   still name missing optional evidence under `Skipped / Unverified`.
4. Classify the evidence boundary:
   - **deterministic:** one repeatable scenario demonstrates the symptom;
   - **intermittent:** record attempts, occurrence rate or trigger pattern,
     and the observation that would distinguish timing, state, or retry causes;
   - **environment-dependent:** record a compact environment matrix (for
     example version, configuration, account/data state, device/region, or
     provider response) and the smallest comparison needed to isolate the
     differing condition.

### Explain

5. Apply the Evidence Sufficiency Gate. Search from evidence anchors and read
   candidate paths from the user action or request entrypoint to the first
   observed divergence, not only the final error.
6. State competing plausible hypotheses. For each, record supporting and
   conflicting evidence, the discriminating observation, and a verification
   step. A single hypothesis is acceptable only when the evidence rules out
   credible alternatives; say why.
7. Verify the highest-information hypothesis one causal claim at a time.
   Confirm a root cause only when the evidence explains the symptom and the
   discriminator excludes the competing causes. Symptom disappearance alone is
   not root-cause proof.

### Fix

8. Only after Explain confirms the causal boundary, propose the smallest fix
   that removes that cause. Name the changed behavior or contract, affected
   files, non-goals, rollback or containment boundary when relevant, and why a
   broader patch is unnecessary. This role plans the fix; `$dev-implementer`
   owns code mutation unless the user explicitly authorizes otherwise.

### Prove

9. Define proof before routing to implementation: rerun the original
   reproduction or its faithful automated equivalent, exercise the root-cause
   boundary, and add a regression check that would fail with the original
   cause. For intermittent failures, specify the bounded retry/sample or
   deterministic test hook that makes the proof meaningful. For
   environment-dependent failures, prove the fix in the affected environment
   and preserve the comparison boundary; do not claim a local-only pass proves
   the field environment.
10. After implementation, compare the proof results with the pre-fix evidence.
    Route a failed or non-discriminating proof back to Explain, not to another
    speculative patch.

### Stop and Escalate

Stop before a fix and return an evidence-backed blocker when the symptom cannot
be reproduced and the available evidence cannot discriminate the leading
hypotheses. State the attempted reproduction, missing evidence, affected
environment or boundary, risk of guessing, and the smallest next collection
step. Do not convert an evidence gap into a low-confidence root cause.

- If minimal privacy-safe instrumentation can resolve the gap and mutation is
  authorized, route `$dev-implementer` to add it, then resume `$dev-debugger`
  with the captured evidence.
- If instrumentation is not authorized, unavailable, or cannot safely collect
  the needed signal, stop with the exact owner, capture plan, and escalation:
  `$pm-readiness-review` for missing expected behavior or product decision,
  `$dev-spike` for unresolved feasibility, `$dev-api-research` for external
  contract behavior, or the responsible environment/operator for access,
  device, data, or deployment evidence.
- Escalate immediately rather than attempting a patch when the missing
  evidence could conceal a critical correctness, security, privacy,
  authorization, data-loss, or destructive-migration risk.

## Workflow

1. Complete Reproduce. If it yields neither a reproducible symptom nor a
   bounded evidence gap, stop and request the missing report details.
2. Complete Explain and the Evidence Sufficiency Gate before proposing a fix.
3. Complete the conditional Fix plan and regression-proof plan only after the
   root cause is confirmed.
4. Route next:
   - Evidence gap with authorized safe instrumentation: `$dev-implementer` ->
     `$dev-debugger`.
   - Evidence gap without an authorized or safe capture path: stop/escalate as
     defined above.
   - PM-only kickoff or diagnosis pass with enough evidence to synthesize the
     bug: `$pm-spec` in Bug Synthesis Mode.
   - Confirmed root cause and minimal fix/proof plan: return to the controller;
     select `$dev-planner` only for a remaining technical choice or sequencing
     need, otherwise `$dev-implementer` may use the current diagnosis/brief.
   - Multiple technical approaches or unknown feasibility: `$dev-spike`.
   - External API behavior is the remaining unknown: `$dev-api-research`.

## Investigate-Only Terminal

When the canonical Issue Route receipt selects
`investigate/bug-diagnosis` with `terminal_intent: diagnosis`, this skill
performs the same reproduce/explain evidence work but stops after its diagnosis
brief. It does not create a goal, implementation branch or PR, tracker closeout,
or architect/planner/implementer dispatch.

The default mutation budget is read-only. A scratch characterization test or
minimal instrumentation needs exact scope and targeted validation. A durable
characterization test, instrumentation, or repro artifact additionally requires
the receipt to name `retained-diagnostic-artifact`, an exact user-authorized
path, targeted validation, and a cleanup or retention disposition; otherwise
return the plan, not the write. End with `conclusive`, `inconclusive`, `blocked`, or
`not-applicable`, the causal evidence/confidence, affected boundary, candidate
fix/proof plan, and one recommended next route. A repair proposal is not repair
authorization: transition to `change` requires a fresh router receipt carrying
explicit delivery authorization and this brief as its resume anchor.

## Evidence Sufficiency Gate

Evidence is sufficient when it can support a discriminating test between the leading causes. Depending on the surface, useful evidence should make it possible to correlate the failing action or request, observe the relevant boundary outcomes and state transitions, identify environment/version/configuration, and locate the first divergence from expected behavior.

When the gate fails:

1. State the unanswered diagnostic questions before proposing logs.
2. Design the minimum instrumentation that answers those questions at the relevant boundaries. Prefer structured events with timestamps, duration, operation or phase, safe correlation identifiers, environment/version/feature flags, state-transition summaries, external-call outcomes, retry counts, and categorized errors.
3. Keep instrumentation privacy- and production-safe. Use allowlisted fields; never log secrets, tokens, raw sensitive payloads, or unnecessary PII. Define sampling, performance, retention, and removal or rollback constraints when production logging is involved.
4. Keep mutation ownership explicit. `$dev-debugger` owns the instrumentation plan and later analysis; `$dev-implementer` owns code changes unless the user explicitly authorizes diagnostic mutation in the debugger role.
5. Reproduce the original scenario with the instrumentation, confirm that one failing run can be correlated across the relevant boundaries, and return to this gate. Do not rank causes from logs that still cannot answer the stated questions.

Mode changes the required evidence breadth. Fast mode may leave non-primary edge
cases or optional reproduction evidence unverified, but it must stop when the
missing evidence prevents a safe primary-path fix or hides a critical
correctness/security/privacy/data-loss risk. Standard mode keeps the
automated-first diagnosis bar. Strict uses the same diagnosis scope and preserves its stricter repair threshold; add
hands-on or representative-runtime evidence when the reported causal boundary
or explicit requirements need it, not because of the mode label. No mode permits
a speculative patch when the causal boundary is unknown.

## Output

```markdown
## Bug Diagnosis Brief

Bug:
<Issue ID/title or symptom summary.>

Mode:
<fast | standard | strict; omitted resolves to standard>

Surface:
<iOS | macOS | SwiftUI | web | backend | Supabase | mixed | unknown>

Debug References Used:
- <selected references | not applicable, with the actual surface>

Evidence:
- <Issue text, logs, stack trace, screenshot, failing test, command output, source file, or "missing">

Symptom Classification:
<deterministic | intermittent | environment-dependent | unknown>

Evidence Sufficiency:
<sufficient | insufficient - why>

Observability Gaps:
- <Unanswered diagnostic question, missing boundary, or "none">

Instrumentation Plan / Result:
- <Minimal structured log, trace, metric, command, owner, capture result, or "not needed">

Reproduction:
- <Steps tried, result, reproducibility, environment, or blocker>

Reproduction Attempts / Environment Matrix:
- <Attempt count and result, or the compared environment conditions and result>

Root Cause:
<Confirmed cause with file/line when known, or "not confirmed">

First Divergence:
<Earliest observed departure from expected behavior, or "not yet observed">

Confidence:
<high | medium | low>

Affected Files / Contracts:
- <File, API, model, migration, permission, UI state, route, or contract>

Candidate Causes:
1. <Cause> - priority: <high | medium | low>
   - Likelihood: <high | medium | low>
   - Supporting evidence: <evidence>
   - Conflicting or missing evidence: <evidence or "none known">
   - Verify: <specific discriminating command, tool, log, test, or repro>
   - Conditional solution: <narrow change to use only if confirmed>

Discriminating Observation:
<Observation that selected the root cause over the competing hypotheses, or "not yet available">

Minimal Fix:
<Smallest causal change, affected boundary, non-goals, and rollback/containment when relevant; or "not proposed until root cause is confirmed">

Proof Plan / Result:
- <Original reproduction or faithful equivalent, root-cause-boundary check, regression check, affected-environment proof, and result when implemented>

Risks / Guardrails:
- <Scope, data, migration, compatibility, privacy, performance, or rollback concern>

Open Questions:
- <Only questions that block confidence or implementation>

Decision:
<reproduced | explained | fix planned | proved | needs instrumentation | needs evidence | needs spike | needs API research | not a bug | blocked>

Recommended Next Step:
<$pm-spec | $dev-planner | $dev-implementer -> $dev-debugger | $dev-implementer | $dev-spike | $dev-api-research | $pm-readiness-review | stop>
```

Keep the brief evidence-led. A useful diagnosis names what is known, what is only likely, and how to prove the fix.
