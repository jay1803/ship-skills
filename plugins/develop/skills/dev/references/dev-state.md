# Dev State And Reporting

Read when creating or updating Dev State and when reporting completion or a blocker.

## Output

Keep a concise dev-stage state:

```markdown
## Dev State

Issue: <id/title>
Goal: <address feature/fix bug and merge PR | explicit narrower boundary>
Readiness Basis: <verified PM handoff | existing canonical issue audit>
Preflight: <direct | pm_required | dev_new | dev_resume | blocked>
Delivery Shape: <single | multi | ambiguous and decisive evidence>
Resume Receipt: <issue, readiness, resume state, delivery shape, mode, gates, validation floor, invalidators>
Evidence Invalidations: <none | changed source, dependent gates, and reason>
Branch: <branch/worktree>
Branch Strategy: <policy source, scope, upstream, issue PR base, temporary branch, promotion target>
Mode: <fast | standard | strict>
Skipped / Unverified: <entries or none>
Phase: <git-setup | repo-context | debug | spike | api-research | architecture | refactor-architecture | api-steward | planning | implementation | test | verification | PR | pr-traceability | technical-review | fix | CI | pr-product-review | merge-handoff | test-handoff>
Owner: <$dev orchestrator | sub-agent artifact: <skill> | serial worker: <skill> | conditional: <skill>>
Implementer(s): <$dev-implementer: implement-ios | implement-macos | implement-swiftui | implement-web | implement-backend | implement-supabase | multiple | not selected yet>
PR/Merge: <not opened | open | review/CI pending | blocked | merged to the resolved base>
Review Readiness: <not applicable | blocked with missing evidence | ready with PR/base/head/dependency/merge-ready artifact evidence>
Review Run: <not started | run ID, generation, attempt count, generation status, frozen head, and prior combined artifact>
Review Repair Limit / Authority: <default 5 | verified user override with source, quote and scope>
Review Repair Budget: <effective limit minus attempt count | not applicable>
Issue/PR Review History: <prior runs, cumulative repair heads/root causes, base-drift reasons>
Review Convergence: <not reached | passed with evidence | blocked/replan>
Production Loop: <not required | required | iteration N | passed | blocked | awaiting-outcome-verification>
Outcome Verification Readiness: <not required | ready | blocked - may begin development | blocked - blocks development>
Loop Verifier: <not applicable | verifier and independence>
Latest Loop Observation: <not applicable | symptom, hypothesis, change, and threshold result>
Status: <ready | running | blocked | retrying | awaiting-test-deploy | awaiting-human-acceptance | awaiting-outcome-verification | complete>

### Current Artifact
- <The artifact just produced or required next.>

### Next Action
<Next Dev skill or escalation route.>

### Blockers
- <Only concrete blockers, or "None.">
```

Final Dev reports must include the mode, project classification, bug diagnosis decision when used, spike/API research decision when used, refactor architecture decision when used, API Steward result when used, validation commands, QA result, outcome-loop contract/evidence/status when required, PR URL, PR traceability/status sync result, combined Review v2 result (including the default thermo-nuclear code-quality rubric), review/CI repair result, PR Product Review result, resolved-base merge/test handoff outcome, release-candidate commit, and human-acceptance status/steps/evidence when required.

Progress reports distinguish observed worker messages or artifacts from
inference. A clean worktree or absent failure message alone does not establish
worker health, phase, or test progress. Prefer meaningful stage changes and
new evidence; do not repeatedly query Git solely to narrate unchanged state.
