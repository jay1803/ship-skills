---
name: pm-bug-triage
description: >-
  Triage newly created or unclear bug reports before engineering diagnosis. Use after PM intake classifies a request as a bug, when a Linear issue is labeled Bug, or when a bug report needs expected behavior, actual behavior, severity, user impact, affected platforms, repro evidence, priority, owner, and next route clarified before dev-debugger or dev work.
---

# PM: Bug Triage

Clarify the product facts of a bug before diagnosis or implementation.

## Workflow

1. Read the issue, title, description, labels, comments, screenshots, logs, attachments, linked PRs, affected release, and any known customer/support context.
2. Confirm whether this is truly a bug.
   - `Bug`: existing promised behavior is broken, regressed, crashing, incorrect, unavailable, too slow, or data-damaging.
   - `Unclear`: expected behavior, actual behavior, platform, or repro evidence is missing.
   - `Not a bug`: the request is a missing feature, UX confusion, support/config issue, data cleanup, expected limitation, or product decision.
3. Capture expected behavior and actual behavior in user/product terms. Do not diagnose root cause here.
4. Assess severity from impact evidence: data loss, crash, broken core workflow, release blocker, affected customers, workaround, frequency, and regression risk.
5. Identify affected platforms, environments, versions, user segments, permissions, and known repro/evidence.
6. Decide the next route:
   - Clear app bug -> `$dev-debugger` for root-cause diagnosis.
   - Backend, web, infra, or data bug -> the relevant engineering/debug workflow, with the triage brief as context.
   - Missing product decision -> `$pm-problem-framing` or `$pm-scope`.
   - Not a bug -> reclassify route and explain why.
7. Post the bug triage brief as an issue comment when tracker tools are available.
8. Update tracker metadata when supported and clear: labels, priority/severity, owner, assignee, status, affected platform, and bug type. Do not edit the issue description.

## Triage Rules

- Treat a `Bug` label as a strong signal, but still verify the report contains expected behavior, actual behavior, affected surface, and enough evidence for diagnosis.
- Ask only for missing facts that change severity, route, or engineering readiness. Do not re-ask for details already present in the issue.
- Do not block on perfect repro steps when crash logs, screenshots, support reports, metrics, or credible customer evidence already make the bug actionable.
- Do not downgrade severity only because a workaround exists; record the workaround and judge remaining impact.
- Do not turn product ambiguity into an engineering bug. If expected behavior is not established, route the decision back through PM.
- Do not create root-cause hypotheses. That belongs to `dev-debugger` or the relevant engineering diagnosis workflow.

## Severity Guide

- `Critical`: data loss, privacy/security exposure, crash loop, total core-workflow outage, payment/account blocker, or release-blocking regression.
- `High`: frequent crash or broken important workflow with limited workaround, major platform-specific failure, severe performance regression, or meaningful customer impact.
- `Medium`: incorrect or degraded behavior with a workaround, contained platform/version impact, visible UX failure, or moderate support burden.
- `Low`: minor polish defect, rare edge case, unclear impact, typo/copy issue, or cosmetic inconsistency.

## Tracker Writes

- Always leave a triage comment when tools allow.
- Auto-update labels, priority/severity, owner, assignee, status, affected platform, and bug type only when evidence supports the change and the tracker fields are available.
- Assign to the current/requesting user when identity is known and no better owner is clear.
- If tracker tools are unavailable, provide the exact comment and metadata update list.
- Do not edit the existing issue description; `$pm-spec` is the only PM skill that owns canonical description rewrites.

## Sub-Agent Contract

This skill is safe to run inline or as a bounded sub-agent. When delegated:

- Use only the request, provided sources, and directly referenced tracker context.
- Produce the bug triage brief and any allowed tracker comment, metadata updates, or drafts.
- Follow this skill's tracker-write rules; do not edit issue descriptions unless this skill explicitly owns that write.
- Return sources read, writes applied or drafts, blockers, and open questions.

## Output

```markdown
## Bug Triage Brief

Decision: <bug | unclear | not a bug>
Severity: <critical | high | medium | low> - <why>
User Impact: <who is affected, frequency, business/customer impact>
Affected Platforms: <iOS | macOS | web | backend | all | unknown>
Environment / Version: <known OS, app version, release, account segment, or "unknown">

### Expected Behavior
- <What should happen, in product/user terms.>

### Actual Behavior
- <What happens instead.>

### Evidence
- <Screenshot, log, support report, comment, metric, attachment, or issue detail.>

### Repro / Trigger
- <Known steps, frequency, or "Not yet known.">

### Workaround
- <Known workaround or "None known.">

### Next Route
- <`$dev-debugger`, engineering workflow, `$pm-problem-framing`, `$pm-scope`, support/ops, or close/reclassify> - <why>

### Questions
- <Only blocking questions needed to route or diagnose safely.>

### Tracker Updates
- Labels: <applied / recommended / unchanged and why>
- Priority / Severity: <applied / recommended / unchanged and why>
- Owner / Assignee: <applied / recommended / unchanged and why>
- Status: <applied / recommended / unchanged and why>
```
