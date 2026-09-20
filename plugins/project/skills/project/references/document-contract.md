# Project document contract

All Project stages use this contract for evidence, document ownership and
continuity. Read it before producing or modifying a project record.

## Authority and evidence

Use the user's named document, scope and destination. Prefer explicit decisions
and accepted records over summaries; assess the source's authority, effective
date and relevant revision before using a newer statement. A newer informal
message does not automatically replace an approved date, budget or commitment.
Show unresolved conflicts instead of choosing by timestamp alone.

Separate sourced facts, attributed decisions, estimates, proposed actions and
unknowns. Link supporting records and state the observation date for current
status or metrics. Do not invent links, approvers, owners, targets, confidence
percentages or commitments. A suggested owner is not an assigned owner.

Keep the work within the requested sources/time window. Begin with supplied
material and known project links; expand through `proj-sources` only to fill a
material gap or fulfill an explicit discovery request. Report unavailable
sources and unchecked periods. No evidence of change is not evidence of no
change. Preserve unresolved blockers across updates.

## Canonical records

- **Proposal:** rationale and requested decision. Once approved, preserve the
  approved revision or snapshot and the approval record. Revisions requiring a
  new decision remain proposals until accepted.
- **Entry Page:** current overview, approved baseline reference, milestone and
  dependency state, resources, decisions, dated update history and continuation.
  Create or reuse it during kickoff. Small projects can keep kickoff material
  here; larger projects can link a separate kickoff document.
- **Execution systems:** own detailed product/engineering work. Link and read
  them as evidence; document work does not transfer their write authority.
- **Closeout:** delivery/acceptance evidence, results against the baseline,
  outstanding measurement and handover actions, and lessons.

Maintain the approved baseline, current plan and change history separately.
Record a change's old/new values, rationale, source and approval state. An
unapproved suggestion can be listed as pending; do not promote it into the
committed plan. An accepted replan does not erase variance from the baseline.

## Writes and recovery

Follow the user's existing authorization: create or update the named artifact
when requested; draft/review-only requests do not authorize canonical writes.
Ask only for a genuinely missing destination, decision or write authority. Do
not impose an extra approval round on already-authorized document edits.
Writing a document does not authorize sending Slack/email, booking meetings,
creating channels, changing permissions or mutating product/engineering trackers.

Use available configured tools without assuming a provider or API exists.
If the destination cannot be accessed, return a clearly labeled draft or diff
and the access gap; never claim it was published. Preserve the requested
platform and location. Do not silently create a replacement canonical page.

Before writing, read the current destination and compare planned edits with its
latest content. Change affected sections, preserve unrelated edits and history,
and reuse known artifact IDs/URLs. After writing, re-read to verify the content
and destination. On a partial failure or unknown outcome, inspect what landed
before another write; complete only missing authorized changes.

Avoid duplicate pages, repeated update entries and no-op reconciliation logs.
A repeat invocation with the same evidence should leave the document unchanged.
For incremental reads, retain per-source coverage/cutoffs and unresolved gaps;
a successful source's cutoff must not skip an unavailable source on recovery.
Distinguish checked-through, observed-at and effective event dates. The latest
calendar date in a log is not automatically a safe coverage watermark.

## Continuation

Keep a short continuation block in the current working document (proposal
before kickoff, Entry Page afterward): current stage/artifact, last verified
state and source coverage, unresolved decisions/conditions, next action and
its owner or ownership gap. Reference supporting records rather than copying
sensitive source transcripts. Stage changes need evidence; writing this block
does not itself approve or complete a stage.

Mirror the user's/document's language and useful existing layout. Templates
supply content prompts, not mandatory empty sections. Return the requested
artifact even when missing facts require it to remain a draft.
