---
name: pm-bug-triage
description: Clarify expected versus actual behavior, impact, severity, and actionable evidence before engineering diagnoses a bug.
metadata:
  owner: jay1803
  family: product
  maturity: stable
  distribution: product
---

# PM: Bug Triage

Clarify the product facts of a bug before diagnosis or implementation.

For a standalone analysis or draft, follow the
[Product Artifact Contract](../pm/references/artifact-contract.md) and complete
the requested artifact without tracker setup. The tracker steps below apply
only to an issue-bound lifecycle or authorized publication.

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
   - Clear app bug -> `$dev-debugger` for root-cause diagnosis, then `$pm-spec` in Bug Synthesis Mode.
   - Backend, web, infra, or data bug -> the relevant engineering/debug workflow, with the triage brief as context, then `$pm-spec` in Bug Synthesis Mode.
   - Missing product decision -> `$pm-scope`.
   - Not a bug -> reclassify route and explain why.
7. Reply with the bug triage brief under the single `## PM Workflow` root when tracker tools are available. If no root exists, use `$pm` intake/root initialization; do not create a separate top-level PM comment.
8. Update tracker metadata when supported and clear: labels, priority/severity, owner, assignee, status, affected platform, and bug type. Do not edit the issue title or description, and do not add `scoped`.
9. Treat triage as an intermediate artifact. A confirmed bug is not PM-complete until diagnosis returns to `$pm-spec` for the canonical issue record and `$pm-readiness-review` passes.

## Triage Rules

- Treat a `Bug` label as a strong signal, but still verify the report contains expected behavior, actual behavior, affected surface, and enough evidence for diagnosis.
- Ask only for missing facts that change severity, route, or engineering readiness. Do not re-ask for details already present in the issue.
- Do not block on perfect repro steps when crash logs, screenshots, support reports, metrics, or credible customer evidence already make the bug actionable.
- Do not downgrade severity only because a workaround exists; record the workaround and judge remaining impact.
- Do not turn product ambiguity into an engineering bug. If expected behavior is not established, route the decision back through PM.
- Do not create root-cause hypotheses. That belongs to `dev-debugger` or the relevant engineering diagnosis workflow.
- Keep `$pm-spec` as the required continuation after diagnosis; diagnosis comments are evidence, not a substitute for the canonical issue description.
- Do not repeat intake classification or later diagnosis content. The triage reply owns only expected versus actual behavior, affected users and surfaces, severity evidence, workaround when it changes impact, missing diagnosis evidence, and the next route.

## Severity Guide

- `Critical`: data loss, privacy/security exposure, crash loop, total core-workflow outage, payment/account blocker, or release-blocking regression.
- `High`: frequent crash or broken important workflow with limited workaround, major platform-specific failure, severe performance regression, or meaningful customer impact.
- `Medium`: incorrect or degraded behavior with a workaround, contained platform/version impact, visible UX failure, or moderate support burden.
- `Low`: minor polish defect, rare edge case, unclear impact, typo/copy issue, or cosmetic inconsistency.

## Tracker Writes

- Always leave the triage artifact as a threaded reply to the existing PM workflow root when tools allow. Never create another top-level PM workflow comment.
- Auto-update labels, priority/severity, owner, assignee, status, affected platform, and bug type only when evidence supports the change and the tracker fields are available.
- Preserve `human-acceptance-required` unless the acceptance requirement was explicitly removed and `$pm-spec` will update the canonical record.
- Do not move the issue to `In Progress` during triage; defer active status sync until the canonical issue record exists and readiness passes.
- Assign to the current/requesting user when identity is known and no better owner is clear.
- If tracker tools are unavailable, provide the exact comment and metadata update list.
- If threaded replies and root editing are both unavailable, provide the exact reply draft and report the limitation instead of posting a separate top-level comment.
- Do not edit the existing issue title or description; `$pm-spec` is the only PM skill that owns canonical rewrites.
- Do not add `scoped`; `$pm-spec` adds it only after successfully writing or verifying both canonical fields.

## Output

```markdown
## Bug Triage Brief

Decision: <bug | unclear | not a bug>
Severity: <critical | high | medium | low> - <why>
User Impact: <who is affected, frequency, business/customer impact>
Affected Platforms: <iOS | macOS | web | backend | all | unknown>
Environment / Version: <include only when material to impact or repro>

### Expected Behavior
- <What should happen, in product/user terms.>

### Actual Behavior
- <What happens instead.>

### Repro / Trigger
- <Only the shortest actionable trigger or evidence link.>

### Workaround
- <Include only when it changes severity or routing.>

### Next Route
- <`$dev-debugger` or engineering diagnosis -> `$pm-spec`, `$pm-scope`, support/ops, or close/reclassify> - <why>

### Missing Before Diagnosis
- <Only blocking evidence, or `None`.>

### Tracker Updates
- <Only fields changed, attempted, or blocked. Omit unchanged fields.>
```
