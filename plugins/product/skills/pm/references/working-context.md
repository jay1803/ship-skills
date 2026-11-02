# Reusable PM Context

The issue owner keeps one working context through intake, spec and readiness.
This is a compact index of current facts and results, not another tracker
artifact or a summary that replaces the canonical contract. Pass it to the next
selected Skill; keep still-loaded source text available instead of fetching or
summarizing it again.

## What to carry

- Exact issue/target, current issue-route receipt, authorized endpoint and write
  scope, mode, PM root ID/URL and existing material record IDs.
- Canonical title/description and its source revision or content hash, stored
  once; decision sources with exact approved text or unresolved proposal bundle.
- Only start-relevant dependencies and applicable review/design/diagnosis
  results, each linked to its inputs and source revision. Missing evidence stays
  missing; a summary or router prediction is not an approval.
- Current `REVIEW:PRODUCT` label state on the bound product outcome when the
  Solution Review gate applies. Carry `approved` only with review evidence;
  otherwise record a label-based waiver. Engineering children inherit the
  parent's product disposition without copying its label.
- Current `pm_action`, its gap/owner, completed results and verified write
  readbacks. Readiness includes assessed canonical binding, relevant decisions,
  dependencies, applicability/waivers and the existing handoff ID.

Links alone are insufficient when the next owner must assess the underlying
text. Pass the needed excerpts and exact source anchors once; fetch a missing
source on demand. An independent reviewer receives the original contract and
provenance needed for its own judgment, not just the producer's conclusion.
Do not copy the whole PM history or every Skill reference into worker prompts.

## Loading by action

Read this contract once per continuous issue run. Preserve it across compaction
with the working-context pointers; expand missing text as needed.

| Action | Load now | Expand only when needed |
| --- | --- | --- |
| `clarify` | Exact gap, decision/diagnosis source and selected owner Skill | Scope, Bug Triage, Solution Review, Design or technical constraints relevant to that gap |
| `write-spec` | `$pm-spec`, current canonical and confirmed delta | Decision provenance for uncertain authority; acceptance policy for acceptance changes; applicable review/design evidence |
| `assess-readiness` | `$pm-readiness-review`, full current product contract and its evidence | Relevant disputed history, applicable gates and conditional runtime handoff fields |
| `reuse-handoff` | Existing handoff and its canonical/decision/dependency bindings | Only changed or unverified sources, plus tracker contract if writing |
| `blocked` | Exact inaccessible/conflicting source or unresolved authority | Only the evidence needed to repair that boundary |

Load the tracker contract before the first write, then reuse it. Use existing
tracker tools for lookup, exact metadata/root writes and readback; these operations
need no intake agent, new analysis stage, separate route call or stage comment.
Only apply supported metadata from evidence, never guessed priorities or owners.
All writes retain existing writer ownership and serialization.

## Freshness

On uninterrupted continuation, use verified readbacks to update the context.
Before a mutation, check affected source revisions and exact target; after a
wait, error, handoff to a new owner or concurrent activity, refresh uncertain
bindings. An unchanged timestamp is not proof about separately edited comments
or dependencies. If no cheap revision check exists, read the affected source.
Do not reread unrelated documents merely because the Skill changed.

Compare relevant content when an `updatedAt` changes: a scheduling label or
unrelated comment does not invalidate product decisions or readiness. A changed
canonical promise, decision, required review input, dependency or authority
invalidates its dependent results. Preserve unrelated current evidence. If the
meaning or source binding cannot be established, treat that result as unverified.
A relevant change after routing returns to `$issue-router`; do not repair its
semantic route in the main model. Routine successful transitions below are the
exception, not permission to reinterpret changed requirements.
Adding or removing `REVIEW:PRODUCT` changes the review-gate input; refresh that
binding before a new handoff or Dev dispatch.

## Progress without another routing call

Keep the original route receipt immutable. Advance `pm_action` in the working
context with the producing owner, input bindings and actual result. These are
local PM progress records, not new workflow receipts or authority:

| Verified result | Next action within the same authorized PM endpoint |
| --- | --- |
| Exact pending proposal answered, no change to the routed scope/target or authority, all prerequisite evidence available | `write-spec` for a confirmed canonical delta; `assess-readiness` if canonical already matches |
| Diagnosis, applicable review/design or dependency evidence completed, confirms the routed candidate without new decisions, all prerequisites now satisfied | `write-spec` for a confirmed canonical delta; otherwise `assess-readiness` |
| Spec write or verification succeeded, all prerequisites satisfied | `assess-readiness` for the resulting canonical state |
| Readiness returned `ready` for current inputs | Finalize/reuse the same handoff and perform only authorized tracker sync |
| Current handoff inputs unchanged | `reuse-handoff`; no new spec write, review or comment required |
| Any new gap, changed outcome/shape, contradictory evidence, uncertain transition or expanded endpoint | Refresh affected facts and obtain a new issue route; do not guess a new action |

A new substantive readiness assessment is still required after a product change.
Jev's `pm_gate` only locates existing evidence, and `reuse-handoff` is a request to
verify a prior result, never a newly granted readiness verdict. Standalone direct
Spec/Readiness requests use their requested artifact endpoint; they need no new
routing call merely to enter an already selected Skill. Legacy receipts without
`pm_action` remain valid ownership evidence: reuse an established current phase
when available, otherwise obtain the action once from `$issue-router`.

Preparation-only work stops at its handoff. A transition into Dev follows the
existing route/authorization contract; these local PM transitions cannot launch
Dev, reopen Done, approve new product policy or expand mutation scope.

## Measuring the change

When comparing runs, count total main-agent, delegated-agent and Jev tokens/cost,
source fetches, routing calls, elapsed time and rework. Separate provider prompt
caching from fewer reads and smaller prompts. Do not claim savings from moving
text into another agent or the router; this contract specifies reuse, not a
measured savings percentage.
