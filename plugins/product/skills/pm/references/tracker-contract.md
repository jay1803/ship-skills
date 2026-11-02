# Linear Issue Contract

Read before authorized Product tracker writes. One controller coordinates each
issue, one Skill owns its canonical record, and one PM thread holds decisions
and material evidence. A Skill does not grant mutation authority.

## Acceptance

Apply [Acceptance Classification](../../pm-spec/references/acceptance-policy.md),
including its unattended-engineering rule, before carrying older acceptance
requirements forward. Required outcomes prove the confirmed product promise;
nonblocking recommendations and skipped/failed observations remain distinct.

Use `human-acceptance-required` for separate human acceptance work needing
special access or judgment; do not use it for ordinary automated QA or technical
review. Resolve and reuse the exact label. Only create a missing label when
supported and authorized. Human acceptance requires an environment/build,
tester or role, safe prerequisites, actions, expected result and evidence;
record accepted-by/date only after actual acceptance.

For standard/strict unattended engineering, deferred physical-device,
real-account, live-environment and named-human tests do not block engineering.
`$pm` owns label alignment and `$pm-spec` the effective canonical wording. Carry
the mode waiver immediately while those updates are pending. A materially
needed human follow-up is drafted for `$pm-project-orchestrator`, remains
outside engineering barriers and cannot be closed from a merge. Do not invent
extra tickets for routine omitted QA. A standalone live-validation request keeps
its own requested completion contract.

Mechanical root/metadata maintenance uses the established route and
[working context](working-context.md). Apply the exact supported payload with
tracker tools and verify readback; it is not a separate intake analysis, agent
or routing call. Preserve unchanged fields and reuse known record IDs.

## One thread, material records only

`$pm` creates or reuses exactly one `## PM Workflow` root with the classification
and relevant source links. Direct-entry readiness may perform this bounded
initialization when equivalent intake evidence already exists. Keep the exact
root comment ID; the issue ID or a child URL is not a substitute.

Later writes use a native reply under that root (with the `linear` Skill: the
CLI's `--parent <root-comment-id>` or the equivalent parent field of another client). Re-read a
reply and verify `parent.id` equals the root. When native replies are unavailable,
append to the verified root only if editing is supported. Otherwise return an
exact unapplied draft; do not post another top-level PM comment.

Search before creating a material record. Reuse its existing comment ID on
revision; do not add same-stage siblings or `Supersedes` replies. Existing
duplicates are history to reconcile, not a reason to create more. After a
transport error, inspect the target before retrying a write.

A phase does not require a comment of its own. Keep ordinary reasoning inline
and write only material decisions, supporting evidence, blockers or the final
handoff. Omit empty sections and unchanged/not-applicable receipts. Preserve:

- `## Product Decision`: exact material proposal, user answer and source;
- supporting artifacts, such as Scope, Bug Triage, Solution Review or Design,
  when their new information or independent provenance needs a durable record;
- `## PM Handoff`: the combined readiness result, canonical revision, essential
  evidence, exceptions, actual tracker sync and next route.

Do not duplicate the spec into comments or repeat review findings in a second
readiness summary. A spec mutation can be recorded in the combined handoff;
use a separate compact write receipt only when it is needed before a wait or
for an independently requested spec artifact. Source history remains available
when current canonical text changes.

Use the root URL as the primary PM process link. A child URL is evidence, not a
replacement for `PM Thread`. Use the
[state machine](issue-state-machine.md) for legacy readiness/handoff pairs and
resume/freshness checks.

For issue-bound Product Solution Review approval, resolve the exact
`REVIEW:PRODUCT` label and add it only to the reviewed outcome within the
authorized write scope. If the label does not exist, create it only when label
management is supported and authorized; otherwise return the pending label
action. An already present exact label may waive the advisory review without a
review comment. Record that as a waiver unless a current approval is evidenced.

## Writer ownership

| Owner | Allowed work within the user's authorization |
| --- | --- |
| `$pm` | Resolve/create a faithful initial issue; intake, root, metadata, authorized status sync and final handoff coordination |
| `$pm-spec` | Rewrite an existing issue's canonical title and description, align acceptance wording/label and add `scoped` only after verified canonical completion |
| `$pm-scope` | Clarify problem/scope, propose decisions and return decomposition drafts; material supporting reply only |
| `$pm-bug-triage` | Bug evidence, severity and supported bug metadata; no canonical rewrite, `scoped` or active status |
| `$pm-solution-review` | Independent simplification and provenance findings; add `REVIEW:PRODUCT` on issue-bound approval when authorized; no scope repair or canonical rewrite |
| `$pm-readiness-review` | Read-only gate judgment and its authorized combined handoff reply; no scope repair or inferred Dev launch |
| `$pm-data-analytics` | Measurement plan and its authorized supporting reply |
| `$pm-backlog` | Draft issue trees, dependencies and follow-ups; no live multi-issue writes |
| `$pm-project-orchestrator` | Accept decomposition; authorized project fields, membership, children and dependencies; route existing issue rewrites through their Spec owners |
| `$design` | Interaction/screen artifacts and evidence; return new material product policy to PM, never rewrite the canonical issue |

Strategy, release learning and PR Product Review keep their own bounded artifact
contracts. Shared routing and model capability do not expand any write scope.
No concurrent writers for one issue or canonical artifact. A worker assigned one
issue returns sibling/project changes to its controller.

Before a mutation, verify the exact target and payload. After it, verify the
changed fields and thread parent. If access is unavailable, return drafts and
state what remains unapplied. An initial issue record, an attempted write or a
readiness label alone is not a canonical specification or completed handoff.
