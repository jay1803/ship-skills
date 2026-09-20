# Research Depth Contract

Research depth controls assurance, breadth, and review. It is not a requested
word count and does not authorize unnecessary work.

Depth applies to both phases of the [Research workflow](../SKILL.md#workflow).
Existing evidence can satisfy the requested assurance without new collection.
First-phase completion records why further evidence is unnecessary; an Evidence
Plan is needed when evidence work remains, not as a mandatory empty artifact.
This shortcut does not waive freshness, counterevidence, or required review.

## Mode Selection

### Scan

Use when the user asks to explore, map, get oriented, identify possibilities,
or determine what should be researched.

Required:

- Research Contract with explicit source boundary.
- Preliminary Decision Model or opportunity criteria when needed.
- Initial landscape, hypotheses, or evidence gaps.
- Highest-value next research questions.
- Honest `Scan Complete` terminal state.

A scan may state a provisional prior. It cannot claim `Decision Ready` unless
the controller explicitly upgrades the mode and satisfies the corresponding
gates.

### Standard

Default when:

- A real decision or recommendation is requested.
- Stakes and reversibility are moderate.
- The decision can be revisited.
- Available time or budget does not justify deep assurance.

Required:

- Current Research Contract.
- Decision Model or equivalent diagnosis/forecast frame.
- Competing hypotheses or alternatives.
- Evidence Plan with qualitative value-of-information reasoning when further
  evidence is needed, otherwise the reason existing evidence suffices.
- Sufficient accepted evidence to distinguish the serious alternatives.
- Synthesis with confidence, residual uncertainty, next action, and revisit
  triggers.
- Review when a review trigger applies.

### Deep

Use when the user explicitly requests deep research or when the decision is
high-stakes, difficult to reverse, highly contested, regulated, security- or
privacy-sensitive, expensive, strategically foundational, or likely to cause
large downstream lock-in.

Additional requirements:

- Broader alternative and counterevidence search.
- Greater source independence and lineage checking.
- Explicit method validity and causal/forecast limitations.
- Sensitivity to assumptions, thresholds, and plausible scenarios.
- Named evidence that could overturn the recommendation.
- Independent `$research-review` on a frozen draft.
- Conditional or blocked completion when the assurance floor cannot be met.

Deep mode does not require exhaustive knowledge. It requires an explicit
argument that the remaining unknowns do not justify more research before the
next action.

## Review Triggers

Run `$research-review` when any of these is true:

- Mode is `deep`.
- The user asks for independent review or verification.
- Recommendation affects a high-cost, hard-to-reverse commitment.
- Material sources conflict.
- A causal claim is central but identification is limited.
- A forecast carries narrow uncertainty despite volatile inputs.
- The recommendation depends heavily on one interested or low-independence
  source.
- The evidence plan was materially changed during synthesis.
- The controller cannot distinguish weak evidence from a robust conclusion.

Review is optional for a standard reversible decision when evidence is direct,
the decision rule is stable, and the controller can explain why review adds
little value.

## Research Budget and Stop Rule

At each wave barrier, the controller asks:

1. Could resolving the remaining uncertainty plausibly change the decision or
   next action?
2. Is the expected improvement worth the cost, delay, and risk of collecting
   the evidence?
3. Is the method capable of resolving it?
4. Can the decision be staged, piloted, reversed, or monitored instead?
5. Has the authorized source, time, money, or access boundary been reached?

Continue only when the next work item has material expected decision value.
Stop as `Decision Ready`, `Experiment Ready`, `Monitor`, `Inconclusive`,
`Blocked`, `Scan Complete`, or `Stopped`.

## Plan-Only and Review-Only

`plan-only` authorizes framing, modeling, hypothesis mapping, and evidence
planning. It does not authorize external interviews, surveys, experiments,
purchases, account changes, tracker writes, or other side effects. Passive
reading of supplied material and public sources is allowed when the user asked
for a researched plan; disclose any external research performed.

`review-only` freezes the supplied target and routes directly to
`$research-review`. The reviewer may inspect cited sources and necessary raw
material, but does not repair the target or restart the full research lifecycle.

## Mode Change

A mode change is a material state revision. Record:

- Previous mode.
- New mode.
- Trigger.
- Added or removed assurance gates.
- Evidence already reusable.
- Newly required work.
- Any previous terminal claim that is no longer valid.
