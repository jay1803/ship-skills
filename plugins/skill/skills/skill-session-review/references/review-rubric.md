# Review rubric and attribution

Use this reference while evaluating evidence and writing recommendations.

## Diagnose from input to verified outcome

Follow the path the task took while locating the largest supported avoidable
costs. The first visible expensive stage need not be the root cause. Omit
unsupported findings, not evidence limitations.

| Stage | Questions |
| --- | --- |
| Input | Did the entry task contract state the goal, scope, acceptance, constraints, evidence pointers, and output needed for efficient correct work? Did extra or conflicting context send work down a costly path? |
| Routing | Did the segment require the model, reasoning effort, agent count, and Skill selection used? Could a cheaper first pass escalate on an observable trigger without increasing total cost or weakening quality? |
| Workflow | Did required phases and handoffs add information or necessary independent checks? Did an instruction force unnecessary planning, research, or review? |
| Context | Were source, Skill, tool-result, and handoff contents useful and current? Did duplicate loads, oversized results, or compaction cause avoidable rediscovery? |
| Execution | Were applicable historical instructions loaded and followed? Separate clear-rule violations from correct execution of an expensive contract. |
| Verification | Were checks sufficient, repeated for a reason, or omitted despite the task's quality floor? |
| Outcome | What was actually verified, partial, blocked, or unknown, and at what total observed cost and latency? |

### Input quality and prompt-induced work

Treat input as the task contract the agent could see at entry: user request,
ticket, higher-priority instructions, selected Skill, injected project context,
prior turns or handoff, and expected output. Record each source and its owner;
their authority and editability differ. Check goal ambiguity, missing acceptance
or constraints, uncertain inclusion/exclusion, contradictory context, and a
prompt-mandated phase disproportionate to the task. If the agent correctly
followed a costly requirement, attribute the design defect to that requirement's
owner. If a current issue or repository source was intentionally the source of
truth, retrieval may be necessary rather than an input defect. Do not blame a
brief user request merely because the agent had to inspect normal task evidence.

Classify input segments as observed decision-relevant, plausibly protective,
unobserved use, repeated, or suspected conflict. Unreferenced text is not
proven removable: a constraint may prevent a wrong branch. A proposed minimum
sufficient task contract should retain the goal, acceptance, boundaries,
authority, relevant state, and current evidence pointers. Test removal or
reorganization before claiming savings. For an input remedy, identify the
missing or excessive source, the owner who can change it, and the smallest
contract that would have avoided the observed branch or rediscovery.

### Already-decomposed tasks

When the user supplies pre-decomposed tickets, review execution against those
boundaries; do not add another routine decomposition gate. Duration alone,
including a run over two hours, does not justify smaller tickets. Recommend
reassessment only with evidence of a failed boundary, such as independently
reviewable outcomes or hidden coupling that caused rework. Route that feedback
to `dev-planner` (or the actual engineering planning owner),
without invoking it or creating children. Account for integration and handoff
costs; missing product decisions need clarification, not a split. Missing prior
assessment evidence limits confidence and is not itself proof of a bad split.
An old `no_split` is not a reason to dismiss later evidence: new producer or
durable-state ownership, failed design assumptions and independently verifiable
outcomes warrant affected-boundary reassessment even within an already-assigned
leaf. Inspect the actual diff/contract changes, safe intermediate states and
integration cost; large mechanical changes can still remain one PR. Distinguish
more helpers or stronger reasoning from separate issue/PR delivery, and name the
controller/planner handoff needed to change that boundary without executing it.

### Time, tokens and context

Treat elapsed time and token usage as separate measurements. Tool or human
waiting may dominate duration without dominating tokens; repeated status polls
can add avoidable usage during that wait. Silence alone does not identify waiting
or active reasoning. Use observed call/result timing and usage coverage; do not
invent a precise phase allocation from task totals. Follow the source reference's
usage deduplication rules and distinguish cached input from other usage.

Inspect context growth where evidence points to cost: repeated unchanged source
loads, oversized tool outputs, full-history handoffs, and rediscovery after
compaction. Separate necessary recovery from avoidable loss of useful state.
The shorter path should identify information to retain, retrieve narrowly, or
reuse, while preserving required independent verification and freshness checks.
For a costly full-history handoff, test a concise contract carrying goal,
constraints, decisions, evidence pointers, open questions, verification state,
and next responsibility. Keep source links and any context needed to audit it.

### Model and Skill economy

Divide a session into meaningful execution segments only where the trace
supports boundaries. For each costly segment, record the observed model and
reasoning effort if available, task difficulty, uncertainty, result, and
escalation or retry cost. Consider cheaper-default, cheaper-first-with-escalation,
or current-capability-required as hypotheses, not model-name prescriptions.
Architecture ambiguity, conflicting evidence, and novel debugging may warrant
stronger capability; mechanically checkable work may permit a cheaper route.
State the escalation trigger, quality gate, model-switching feasibility, and
what context an escalation must rebuild. Do not infer segment-level model cost
from a session-wide usage total. Use a dated rate card only with compatible,
model-attributed usage; keep input, cache, output, and reasoning treatment
consistent with that card. A routing proposal should name the segment, observed
model and effort (or unknown), policy, reason, escalation trigger, quality
gate, and comparison needed to validate it.

For a relevant Skill, trace available, selected, loaded, applied, and outcome
before assessing its footprint. Inspect actual core/reference loads, repeated
loads, context-size proxies, induced tool calls, extra agents or verification,
and observed benefit. Static file bytes are not billable tokens, and one
session cannot establish rework avoided by a Skill. Move detail behind a
conditional reference only when usage shows it can be omitted without losing
source fidelity, authority rules, or an important decision.

## Root cause before edits

Classify both the affected stage above and its causal source/owner: task
contract or breakdown, model/agent routing, orchestration or handoff, context
construction, Skill instructions, agent execution, verification design,
environment/tool limit, changed user intent, or unresolved/mixed cause. A Skill
instruction can be part of the input and still be owned by that Skill; do not
count it twice. State the causal link and confidence (high/direct evidence,
medium/credible inference, low/hypothesis); confidence and impact are separate.
A clear rule ignored once need not gain more emphatic wording. Match the remedy
to the failure: improve discovery/loading or handoff context when absent, resolve
conflicts at their owner, and use a targeted execution regression or feasible
mechanical check for a clear-rule violation. Do not prescribe enforcement that
the runtime cannot support.
A missing fallback may merit a small conditional instruction; a transient service
failure alone does not establish a Skill defect. Map namespace aliases and installed
copies to one canonical Skill before proposing changes; do not edit the cache.

Use impact to prioritize: unauthorized consequential actions, materially incorrect
outcomes, or false completion first; repeated rework and avoidable cost next;
minor clarity issues last. Avoid a synthetic overall score unless the user requests
one and its rubric can be explained. A successful task can contain serious issues;
a failed task can show correct Skill use under an external blocker.

For every efficiency finding identify the redundant segment, knowledge available
at that point, necessary work that must remain, and a concrete alternative.
Changed source, new failures, or new evidence may justify rereads and reruns.
Safety checks, independent verification, and context recovery are not waste merely
because they consume tokens. Recommend batching only when operations are independent.
If usage is unavailable or incomparable, state that and use labeled proxies;
never assign measured savings to an untested proposal.

## Recommendation quality

A useful recommendation names the responsible owner and concrete alternative,
explains what becomes cheaper and why the same user intent, acceptance,
verification, correctness, and authority should hold, and describes an
observable regression check. For a Skill defect, include the target section
and concise proposed text or deletion.
Compare avoidable calls/reads or compatible measured usage while also checking
acceptance, required verification and authority. Predicted savings remain unproven
until comparable runs support them. Prefer the smallest reusable correction. Preserve
user intent, required authority, and valid exception paths. Do not turn a one-off
preference into a universal rule. Mark unresolved causes as hypotheses and explain
what additional evidence would discriminate them.

For material cost changes, propose a quality-preserving experiment: baseline,
candidate, comparable task/input and tool availability, single changed policy,
acceptance and verification gates, measured usage, tool/retry counts, latency,
and failure or escalation rate. Include the cost of failed attempts and
recovery. Use several comparable tasks or runs when variance matters; a single
replay can be contaminated by prior knowledge. For subjective outcomes use an
independent blind comparison where feasible. Report quality and cost
separately, including spend per verified completion across comparable runs;
do not divide the cost of one failed run by a fabricated success. Promote a
routing or prompt change only after the quality floor is observed, and leave
untested alternatives as hypotheses. Prioritize by supported
avoidable cost and risk rather than a fixed routing/workflow/prompt order.

Example (illustrative, not a standing rule): repeated whole-suite checks after a
local documentation edit may support replacing an unconditional rerun instruction
with change-based check selection. Verify both the documentation-only case and a
shared dependency change that still requires broad checks. If the original checks
were mandated by repository policy, address the policy owner rather than advising
the agent to ignore it.
