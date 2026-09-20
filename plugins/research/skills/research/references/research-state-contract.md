# Research State Contract

The Research State is the controller-owned record of what question is being
answered, what evidence has been accepted, what remains uncertain, and why the
next research action is justified. It is the continuity surface for new,
resumed, updated, and reviewed research.

## Authority

- `$research` owns the canonical state, its version, worker registry, research
  waves, accepted artifacts, invalidation decisions, and terminal status.
- Worker skills own only their returned artifacts. They may propose state
  changes but cannot accept their own work into the state or declare the whole
  question complete.
- `$research-synthesis` owns a draft Decision Brief. `$research-review` owns an
  independent judgment on a frozen draft. `$research` accepts, rejects, or
  routes repairs and owns the final handoff.
- A user correction, newly supplied source, changed decision constraint, or
  fresh material event can revise the state. The controller records the
  invalidated downstream artifacts instead of silently rewriting history.

## Minimum State

```yaml
research_id: <stable identifier>
state_version: <monotonic revision>
status: <state below>
mode: scan | standard | deep
execution_intent: plan-only | execute | review-only | update
created_at:
updated_at:

question:
  raw_request:
  primary_type: choice | diagnosis | forecast | discovery | design | evaluation
  dependent_types: []
  decision_or_use:
  decision_owner:
  objective:
  horizon:
  scope:
  exclusions:
  constraints:
  stakes:
  reversibility:
  decision_date:
  source_boundary:
  output_required:

decision_model:
  alternatives:
  baseline_or_status_quo:
  hard_constraints:
  objectives:
  criteria:
  thresholds:
  tradeoffs:
  current_preference_order:
  sensitivity:

hypotheses:
  - id:
    claim:
    mechanism:
    scope:
    supports:
    disconfirms:
    decisive_signal:
    status: open | supported | weakened | rejected | unresolved

evidence_plan:
  critical_uncertainties:
  work_items:
  waves:
  stop_rules:
  budget_or_limits:

evidence_ledger:
  accepted_items:
  contradictions:
  unavailable_evidence:
  source_quality_notes:

belief_state:
  current_judgments:
  confidence:
  material_changes:
  unresolved_decision_relevant_uncertainty:

artifacts:
  research_contract:
  decision_model:
  hypothesis_map:
  evidence_plan:
  specialist_briefs:
  draft_decision_brief:
  review:
  accepted_decision_brief:

terminal:
  status:
  reason:
  next_owner:
  next_action:
  revisit_triggers:
```

Fields may be omitted when they do not apply. Do not fill an inapplicable field
with invented content merely to satisfy the shape.

For Phase 1, retain the restated question, material definitions, source-backed
answer or options, and remaining gap in the corresponding fields above. Record
the reason to stop or enter Phase 2 in the terminal or evidence-plan fields.
The state may be concise and inline; a separate file or worker artifact is not
required solely to answer from existing information.

## Controller States

| State | Meaning | Exit condition |
| --- | --- | --- |
| `Intake` | The raw request is bound; the research use is not yet clear | Current Research Contract accepted |
| `Framed` | Decision/use, question type, scope, and constraints are clear | Decision Model accepted or explicitly unnecessary |
| `Modeled` | Alternatives, criteria, causal drivers, or forecast target are explicit | Competing Hypothesis Map accepted or not applicable |
| `Planned` | Critical uncertainties, methods, waves, and stop rules are explicit | Authorized evidence work begins |
| `Collecting` | One or more evidence workers are active or their artifacts are being accepted | Required current wave reaches its barrier |
| `Synthesizing` | Evidence is stable enough to update beliefs and draft a recommendation | Draft Decision Brief accepted for review or completion |
| `Reviewing` | An independent review is judging a frozen draft | Review accepted and repairs resolved |
| `Decision Ready` | A decision owner can act on the accepted brief | Terminal |
| `Experiment Ready` | Research isolated a critical uncertainty and produced a credible test | Terminal handoff to experiment owner |
| `Monitor` | A choice is conditional on future signposts rather than more immediate research | Terminal with monitoring plan |
| `Scan Complete` | Territory, priors, gaps, and next research priorities are mapped | Terminal |
| `Inconclusive` | Available evidence cannot distinguish alternatives within authorized limits | Terminal |
| `Blocked` | Required access, source, authority, or method is unavailable | Resume after named blocker changes |
| `Stopped` | Continuing has insufficient decision value or would violate scope | Terminal unless the user changes the contract |

`Decision Ready` is a research completion state, not an automatic commitment.
The decision owner remains responsible for the commitment unless a separate
delegation explicitly grants it.

These states do not force a collection pipeline. When existing information
suffices, move from framing/modeling to synthesis and applicable completion or
review. If a missing definition or business decision blocks the requested
judgment, return that gap and next action as `Blocked`; do not label it
`Monitor` without an actual signpost-based reason to wait.

## Entry and Resume Audit

Before new research work:

1. Bind the raw question and every supplied source, file, URL, dataset, prior
   brief, decision, or constraint.
2. Search the current conversation, supplied workspace, and explicitly
   connected sources for an existing Research State or equivalent artifacts.
3. Mark each artifact `current`, `stale`, `conflicting`, `partial`, or
   `unavailable`.
4. Reuse current artifacts. Run the earliest decision-relevant missing stage;
   do not recreate every named stage for procedural appearance.
5. Record the selected mode, execution intent, source boundary, and material
   assumptions before dispatching workers.

A resumed state keeps its `research_id` and increments `state_version` only for
a material change: question, scope, mode, decision model, accepted evidence,
belief state, review target, or terminal status. Progress notes alone do not
need a new semantic version.

## Invalidation Rules

Invalidate only downstream artifacts that depend on changed evidence.

- Changed objective, decision owner, horizon, or hard constraint invalidates the
  Decision Model and every dependent artifact.
- A new alternative invalidates comparative hypotheses, relevant evidence-plan
  work, ranking, synthesis, and review; unrelated source briefs remain usable.
- A corrected source claim invalidates the evidence rows and judgments that
  cite it.
- A changed dataset or analysis definition invalidates the affected analysis,
  dependent causal claims, synthesis, and review.
- A new event after a forecast's as-of time invalidates the current forecast
  judgment, not the historical evidence trail.
- A changed draft after review invalidates the review. Review must bind the
  exact target revision.

Never erase the former state when it explains why a judgment changed. Record
the superseded artifact and the evidence that caused the change.

## Work Items and Waves

Each research work item records:

```yaml
work_id:
owner_skill:
question_or_hypothesis:
accepted_inputs:
source_boundary:
method:
expected_artifact:
decision_use:
dependencies:
can_run_with:
cannot_run_with:
completion_evidence:
status: pending | dispatched | returned | accepted | rejected | blocked
```

A wave contains independent work items whose outputs do not define one
another's question, source scope, method, or canonical state. The controller
opens a wave only after its dependencies are accepted and closes it only after
every required item is accepted, rejected with a named reason, or blocked.

Workers never dispatch successor workers. They recommend the next route to the
controller.

## Completion Evidence

The controller may declare a terminal state only when it can show:

- The primary question and intended decision/use remain the same as the accepted
  Research Contract.
- The Decision Model or equivalent causal/forecast frame is explicit.
- The evidence used for material claims is present in the accepted ledger.
- Facts, inferences, assumptions, judgments, and forecasts are distinguishable.
- Material alternatives and counterevidence were considered.
- Confidence reflects source and method limits.
- Remaining uncertainty is named and its decision relevance is assessed.
- The next action is concrete.
- Revisit triggers or monitoring signals are present when the answer can change.
- The required review gate, if any, passed or its conditions are explicitly
  carried into the terminal result.
