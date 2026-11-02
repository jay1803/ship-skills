# Dev State And Reporting

Keep one compact current-state record, updating it from accepted evidence rather
than copying every phase's history into each handoff. Preserve existing field
names when a caller uses them; no fixed set of empty/not-applicable rows is needed.

```markdown
## Dev State
Issue: <verified ID/scope>
Goal: <authorized lifecycle or explicit narrower boundary>
Resume Receipt: <current route/readiness/phase plan and source reference>
Mode: <fast | standard | strict>
Skipped / Unverified: <applicable omissions and authority, or none>
Branch: <worktree, resolved base and current revisions when present>
PR/Merge: <PR identity, gate or merge state when present>
Phase: <current selected phase>
Owner: <actual owner/helper identity>
Status: <running | blocked | retrying | complete, or concrete handoff wait>
Current Artifact: <immutable source/reference, identity and result>
Next Action: <next selected owner/action and wake condition when pending>
Blockers: <concrete dependent blockers, or none>
```

Add conditional details only when they change execution or prove a claim:
branch strategy; naming/worker recovery; evidence invalidations; material decision
comments; shared discovery parent and included/deferred tickets; PR traceability;
selected Review readiness/history/coverage/rounds/limit authority; required outcome
loop; cleanup and test handoff. Persist detailed Review history once under the
[Review lifecycle ledger](review-lifecycle.md#ledger). Pass its resolvable
reference plus current target and remaining rounds, not recursively expanded
results. Unavailable required references block the
affected acceptance; summaries cannot replace them. Keep actual observations,
requested bindings and unknown runtime values distinct.

A final report states what changed, selected validation commands/results, current
mode/omissions, commit and PR, gate outcomes and the authorized delivery boundary.
Include Review depth and actual coverage, merge/cleanup/test evidence,
release candidate or acceptance/production-loop evidence when applicable. Preserve
pending, authored, committed, pushed, merged, deployed and verified distinctions;
report the next action for remaining gates. Do not print unselected phase paperwork.

When discoveries exist, report their shared parent and included/deferred summary
under [discovered-work ownership](execution-ownership.md#autonomous-decisions-and-discovered-work).
For merged work include [cleanup evidence](../../dev-merge-handoff/SKILL.md#cleanup-evidence),
keeping a retention/cleanup blocker distinct from completed delivery.

Progress describes observed worker messages/artifacts and meaningful state changes.
A clean tree or absent failure alone proves neither worker health nor test progress.
Avoid repeated Git queries merely to narrate unchanged state.
