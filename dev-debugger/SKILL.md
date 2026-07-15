---
name: dev-debugger
description: >-
  Diagnose bug tickets in the Dev workflow before architecture, planning, or implementation. Use when a Linear issue, PM bug triage brief, product spec, user report, test failure, crash, hang, regression, wrong UI, wrong data, performance issue, flaky behavior, or field-only defect needs reproduction, evidence gathering, root-cause analysis, ranked hypotheses, affected files/contracts, validation strategy, and a fix direction. Produces a Bug Diagnosis Brief and routing decision for $dev-architect, $dev-planner, $dev-implementer, $dev-spike, or $dev-api-research.
---

# Dev: Debugger

Diagnose bugs before fixing them. The output is a root-cause brief that lets the Dev workflow plan and implement a narrow fix without guessing.

Run after `$dev-repo-context` and before `$dev-architect` for bug tickets, regressions, crashes, hangs, wrong behavior, and field-only defects. Do not implement the fix in this role unless the user explicitly asks.

## Reference Selection

Read the shared workflow first, then load one or more references from `references/`:

- iOS app, iOS simulator/device-only bug, Xcode iOS target, UIKit, App Intents, crash, hang, memory, performance, or iOS runtime behavior: [debug-ios.md](references/debug-ios.md)
- macOS app, AppKit, macOS SwiftUI scene/window/menu, sandbox/TCC, signing, entitlement, packaging, crash, hang, performance, or macOS runtime behavior: [debug-macos.md](references/debug-macos.md)
- SwiftUI state, layout, navigation, sheet, animation, accessibility, preview, performance, identity, or view lifecycle bug: [debug-swiftui.md](references/debug-swiftui.md)
- Frontend web, React, Next.js, Vite, browser behavior, hydration, routing, responsive layout, client state, accessibility, or web test failure: [debug-web.md](references/debug-web.md)
- Backend/API/service bug that is not primarily Supabase: [debug-backend.md](references/debug-backend.md)
- Supabase schema, migration, RLS, Auth, Edge Functions, Storage, Realtime, generated types, or Supabase integration defect: [debug-supabase.md](references/debug-supabase.md)

Multiple references are allowed when the bug crosses surfaces. Pair `debug-swiftui.md` with `debug-ios.md` or `debug-macos.md` when app-level runtime evidence matters.

## Scope Gate

- Use for defects: crash, hang, regression, incorrect output, broken UI, wrong data, performance issue, flaky behavior, failed acceptance check, field report, or reproducible test failure.
- Do not use for new features, product ambiguity, strategic priority, PR review comments, or failing CI infrastructure. Route those to PM, `$dev-fix`, or `$dev-ci-repair`.
- Do not re-ask for evidence already present in the PM bug triage brief, issue, comments, screenshots, logs, stack traces, or attachments.
- If the report is not actually a bug, stop with the reason and route back to `$pm-readiness-review` or the correct Dev role.
- If a PM bug triage brief is present, treat its expected behavior, actual behavior, severity, user impact, affected platform, environment, workaround, and open questions as the product source of truth unless newer tracker comments supersede it.

## Workflow

1. Resolve the bug ticket and any PM bug triage brief. Capture expected behavior, actual behavior, affected platform, environment, severity, user impact, reproducibility, regression window, workaround, open questions, and available evidence.
2. Load the relevant `debug-*.md` reference(s).
3. Gather evidence from issue text, comments, attachments, logs, crash reports, screenshots, failing tests, CI output, reproduction steps, and repo context.
4. Reproduce when practical and safe. In fast mode, prefer automated or non-interactive reproduction first; use hands-on simulator/device/browser QA only when the user requested standard mode or the bug cannot be responsibly diagnosed without it.
5. Search from evidence anchors: stack frames, error strings, UI text, route names, API names, test names, model fields, migration names, log keys, and feature names.
6. Read candidate code paths from user action or request entrypoint to failure point. Distinguish proven root cause from plausible hypothesis.
7. Produce a ranked diagnosis with verification steps and a fix direction. If evidence is too thin, produce an evidence-capture plan instead of fake certainty.
8. Route next:
   - Root cause clear and fix shape straightforward: `$dev-architect` or `$dev-planner`.
   - Multiple technical approaches or unknown feasibility: `$dev-spike`.
   - External API behavior is the main unknown: `$dev-api-research`.
   - Evidence missing: stop with the exact evidence needed.

## Output

```markdown
## Bug Diagnosis Brief

Bug:
<Issue ID/title or symptom summary.>

Mode:
<fast | standard | not specified>

Surface:
<iOS | macOS | SwiftUI | web | backend | Supabase | mixed | unknown>

Debug References Used:
- <debug-ios | debug-macos | debug-swiftui | debug-web | debug-backend | debug-supabase>

Evidence:
- <Issue text, logs, stack trace, screenshot, failing test, command output, source file, or "missing">

Reproduction:
- <Steps tried, result, reproducibility, environment, or blocker>

Root Cause:
<Confirmed cause with file/line when known, or "not confirmed">

Confidence:
<high | medium | low>

Affected Files / Contracts:
- <File, API, model, migration, permission, UI state, route, or contract>

Hypotheses:
1. <Hypothesis> - likelihood: <high | medium | low>
   - Why: <evidence>
   - Verify: <specific command, tool, log, test, or repro>
   - Fix direction: <narrow change>

Validation Plan:
- <How the eventual fix must prove the bug is gone>

Risks / Guardrails:
- <Scope, data, migration, compatibility, privacy, performance, or rollback concern>

Open Questions:
- <Only questions that block confidence or implementation>

Decision:
<diagnosed | needs evidence | needs spike | needs API research | not a bug | blocked>

Recommended Next Step:
<$dev-architect | $dev-planner | $dev-implementer | $dev-spike | $dev-api-research | $pm-readiness-review | stop>
```

Keep the brief evidence-led. A useful diagnosis names what is known, what is only likely, and how to prove the fix.
