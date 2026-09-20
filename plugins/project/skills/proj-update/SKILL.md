---
name: proj-update
description: Gather project progress and reconcile an Entry Page or plan, then draft a stakeholder update. Also supports log-only reconciliation; accepts existing document platforms and local Markdown.
metadata:
  owner: jay1803
  family: project
  maturity: stable
  distribution: project
---

# Project Update

Maintain an accurate current overview and useful dated progress record. Read the
[document contract](../project/references/document-contract.md) before edits.

## Resolve the task

Read the named Entry Page/plan and previous update. Preserve its platform,
structure, language and existing project vocabulary. Determine whether the user
wants fresh evidence collection, reconciliation against the document's own log,
a stakeholder update draft, or an authorized combination. A log-only request
does not require external searches. A draft-only request does not change the page.

Use known source links and per-source coverage to choose the incremental window.
For a first update, use the kickoff date or an explicitly stated window when
available; otherwise state the bounded window used or ask when it changes the
meaning of the update. Distinguish missing coverage from confirmed no changes.
Read relevant docs, channel threads and meeting notes through available tools.
A calendar event proves a meeting was scheduled, not what was decided.

## Reconcile evidence into state

Compare with the previous blockers, active work, next work, decisions, owners,
risks and outcome measures. Follow relevant source links and deduplicate events.
Use authority and effective dates to resolve changes, not merely the latest
message. Do not treat a file modification timestamp alone as a changed decision.

Update actual state changes, not activity counts. Preserve unresolved blockers
until evidence supports resolution; distinguish work proposed, started, merged,
deployed, accepted and measured. Label suggested mitigations and owners as
recommendations. Surface consequential risks and the decision/action needed.

For each material change, compare old/current values and retain the source:

- Accepted scope/date/resource changes update the current plan and history;
  the approved baseline remains intact.
- Proposed changes stay pending; unresolved conflicting sources stay visible.
- Metric readings include definition/window/date; a target is achieved only
  when comparable evidence supports it.
- Newly verified resource links can be added within the authorized document
  scope; do not create channels or send stakeholder messages.

Apply only genuine differences. Avoid duplicate updates or a new reconciliation
entry when nothing changed. If the page already reflects the log, say so.
Retain incomplete source coverage for the next invocation. Do not advance an
unavailable source's cutoff because another source was checked successfully.

## Output and write verification

A useful update explains overall status, what changed since the previous
covered period, progress against milestones, risks/blockers, decisions needed,
and next actions/owners. Include source links and material coverage gaps. Match
an established format; omit empty sections rather than manufacturing progress.

For an authorized page update, reconcile the overview and add the dated update
without overwriting history. Re-read to confirm both edits landed. If only part
succeeds, report the exact partial result and inspect it before completing the
remaining write. Use [proj-review](../proj-review/SKILL.md) when preparing a
reviewed stakeholder deliverable. Return the updated destination or draft,
coverage/gaps, significant changes and pending decisions. Writing the update
does not mean it was sent to stakeholders or the project is complete.
