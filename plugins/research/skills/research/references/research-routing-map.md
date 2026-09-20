# Research Routing Map

`$research` owns routing. Worker skills may recommend a next route but never
dispatch successors or declare the controller complete.

## Capability Tiers

These are planning defaults rather than provider-specific requirements.

| Work | Default tier | Escalate when |
| --- | --- | --- |
| Controller state, synthesis acceptance, final completion | `controller/critical` | Never delegate controller authority |
| Framing, decision model, hypothesis map, evidence plan | `worker/deep` | Stakes, ambiguity, or cross-domain complexity is high |
| Desk, market, competitive, user-study, data, causal, experiment, forecast | `worker/standard` | Method complexity or consequence requires `worker/deep` |
| Synthesis | `worker/deep` | Deep mode or major contradictions |
| Independent review | `worker/deep` with fresh context | Always independent from the synthesis author when feasible |

The controller should use the strongest available reasoning suitable for the
decision, while keeping narrow factual retrieval or extraction proportionate.

## Stage Selection

Apply the controller's [two-phase workflow](../SKILL.md#workflow) before
selecting evidence workers. The first-pass answer may complete the request;
otherwise route the named gap, not every discipline related to the topic.
Clarification and business preferences are not automatically evidence tasks.

| Evidence state | Next owner |
| --- | --- |
| Decision/use, scope, owner, horizon, or source boundary unclear | `$research-question-framing` |
| Alternatives, objectives, constraints, criteria, or causal/value drivers unclear | `$research-decision-model` |
| Competing explanations or what-must-be-true claims are not explicit | `$research-hypothesis-map` |
| Signals, methods, priorities, stop rules, or research waves are unclear | `$research-evidence-plan` |
| Current external facts, standards, papers, documents, or supplied-source facts are needed | `$research-desk` |
| Category structure, demand, segments, value chain, channels, economics, or maturity is unclear | `$research-market-landscape` |
| Direct, indirect, substitute, status-quo, or build alternatives need evidence | `$research-competitive` |
| Participant evidence is needed but no valid study/instrument exists | `$research-user-study` |
| Actual interviews, surveys, observations, or usability records need synthesis | `$research-user-synthesis` |
| Supplied or connected quantitative data must be defined, validated, segmented, or analyzed | `$research-data-analysis` |
| A cause or attributable effect is material and observational evidence may mislead | `$research-causal-analysis` |
| A critical uncertainty is best resolved through a pilot, test, or intervention | `$research-experiment-design` |
| The primary or dependent question concerns an unresolved future | `$research-forecasting` |
| Accepted evidence is sufficient to update beliefs and draft the recommendation | `$research-synthesis` |
| Deep mode, high stakes, major conflict, weak identification, or explicit review | `$research-review` |

## Common Routes by Question Type

These are conditional dependency examples when the named work is needed, not
mandatory pipelines. Reuse first-phase framing and existing evidence; omit
workers whose output cannot change the answer or required assurance.

### Choice

```text
Question Framing
→ Decision Model
→ Hypothesis Map
→ Evidence Plan
→ selected evidence workers
→ Synthesis
→ conditional Review
```

### Diagnosis

```text
Question Framing
→ Hypothesis Map
→ Data Analysis
→ Causal Analysis
→ optional Desk/User evidence
→ Synthesis
→ conditional Review
```

Use Decision Model when a downstream intervention choice is part of the same
authorized research outcome.

### Forecast

```text
Question Framing
→ optional Decision Model
→ Evidence Plan
→ Desk/Data/Market inputs
→ Forecasting
→ Synthesis
→ conditional Review
```

### Discovery

```text
Question Framing
→ Decision Model for opportunity criteria
→ Evidence Plan
→ Market Landscape + Competitive + User evidence
→ Hypothesis Map for shortlisted opportunities
→ Synthesis
```

### Design

```text
Question Framing
→ Decision Model
→ Hypothesis Map
→ Desk/Competitive/Causal evidence as relevant
→ Experiment Design for unresolved feasibility or behavior
→ Synthesis
→ handoff to Product/Dev/Design
```

### Evaluation

```text
Question Framing
→ Decision Model or theory of change
→ Evidence Plan
→ Data Analysis + Causal Analysis
→ User Evidence Synthesis where experience or implementation matters
→ Synthesis
→ Review
```

## Concurrency

After the Research Contract, Decision Model, and relevant hypotheses are stable,
independent evidence streams can run in parallel.

Good parallel candidates:

- Market structure and competitor evidence using distinct source sets.
- Internal cohort analysis and external desk research.
- User-study planning while desk research resolves terminology.
- Base-rate research and driver research for a forecast.
- Separate evidence packages for independent hypotheses.

Serialize when:

- A later question depends on an earlier definition, taxonomy, alternative set,
  metric, or causal frame.
- Two workers would mutate or reinterpret the same canonical artifact.
- One worker’s result determines whether another method is needed.
- Source access, participant sampling, or experiment design depends on a
  decision not yet accepted.
- Synthesis would begin before required evidence-wave barriers close.
- Review would begin before a target revision is frozen.

Shared topic is not itself a reason to serialize. Shared unresolved definitions
are.

## Worker Handoff Packet

```markdown
## Research Worker Assignment

Research ID:
State version:
Owner skill:
Assigned question:
Decision use:
Accepted inputs:
Hypothesis or criterion:
Source boundary:
Method constraints:
Required artifact:
Completion evidence:
Dependencies:
Known contradictions:
Out of scope:
```

A worker that receives an incomplete packet returns `upstream_blocked` with the
missing field. It does not redefine the research question.

## Controller Acceptance Receipt

```markdown
## Research Artifact Receipt

Work item:
Artifact:
Accepted / Rejected / Blocked:
Evidence rows accepted:
Decision-model or hypothesis updates:
Contradictions:
Downstream invalidations:
Next route:
```

Acceptance means the artifact may influence synthesis. It does not imply that
all of its claims are true or that the research is complete.
