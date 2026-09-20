---
name: research
description: >-
  Decision-research orchestrator for open, strategic, diagnostic, forecasting, discovery, design, and evaluation questions. Use when the user asks what to choose, why an outcome happened, what is likely, where an opportunity exists, how a system should be designed, whether an intervention worked, or requests deep research that must become an evidence-backed recommendation. Owns the canonical Research State, routes narrow research workers, prioritizes uncertainties by decision value, accepts evidence, controls synthesis and review, and stops only at an explicit decision, experiment, monitoring, scan, blocked, inconclusive, or stopped terminal state.
metadata:
  owner: jay1803
  family: research
  maturity: stable
  distribution: research
---


# Research: Orchestrator

First restate and define the question, then give the answer or useful options
supported by existing information. Enter targeted evidence research only when
a remaining ambiguity or information gap matters to the requested answer.
Stop when further research has less value than acting, testing, or monitoring.

Read the [Research State Contract](references/research-state-contract.md),
[Research Depth Contract](references/research-depth-contract.md), and
[Evidence Contract](references/evidence-contract.md) before controlling a
multi-worker research run. Read the
[Question Type Contract](references/question-type-contract.md) when classifying
or decomposing the request, the
[Research Routing Map](references/research-routing-map.md) before dispatch, and
the [Decision Brief Contract](references/decision-brief-contract.md) before
accepting synthesis or declaring completion.

## Boundary

- Own one canonical Research State: question, mode, decision/use, alternatives,
  hypotheses, evidence plan, worker registry, accepted evidence, belief state,
  artifacts, review target, and terminal status.
- Own question classification, stage selection, research-wave dependencies,
  evidence acceptance, state invalidation, synthesis acceptance, review repair,
  and final completion.
- Use worker skills for bounded outputs. Do not reproduce their detailed
  procedures in this orchestrator or let workers dispatch successors.
- Recommend a commitment; do not make the user's product, budget, hiring,
  investment, publication, production, or other consequential commitment unless
  the user has explicitly delegated that decision and the relevant action owner
  authorizes execution.
- Research work is read-only by default. Public browsing and analysis of
  supplied or connected data are allowed when requested. Interviews, surveys,
  experiments, purchases, outreach, tracker changes, repository changes, and
  production mutations need separate authorization and the appropriate owner.
- Respect an attached-source or named-source boundary exactly. Unsupported
  points remain unsupported.
- Do not equate research volume with quality. Search, source, page, and token
  counts are activity measures, not completion evidence.
- Do not force every request through every worker. Audit existing evidence and
  select only stages whose missing result can change the decision or assurance.
- Keep the controller in the invoking thread or persistent controller session.
  Workers return artifacts; only this controller updates the canonical state.

## Entry Classification

Classify the request along four independent axes.

### Question Type

Choose one primary type:

- `choice`: select among alternatives.
- `diagnosis`: explain an observed outcome.
- `forecast`: estimate an unresolved future outcome.
- `discovery`: find and prioritize opportunities, risks, or leverage points.
- `design`: select a system, policy, product, process, or architecture.
- `evaluation`: determine whether an intervention worked, for whom, and why.

Record dependent question types without letting them replace the primary
completion condition. Split the request when two questions have materially
different owners, horizons, evidence bases, or actions.

### Research Mode

- `scan`: map the territory, priors, gaps, and next research priorities.
- `standard`: default decision-oriented research for a reversible,
  medium-stakes choice.
- `deep`: high-stakes, hard-to-reverse, contested, regulated, foundational, or
  explicitly deep work with independent review.

### Execution Intent

- `plan-only`: frame, model, and plan the research; do not run side-effecting
  collection.
- `execute`: perform authorized passive evidence work and any separately
  authorized collection.
- `review-only`: freeze and review an existing brief.
- `update`: revise an existing Research State with new evidence or constraints.

### Source Boundary

Record whether research may use:

- only supplied sources;
- supplied plus public sources;
- specified connected internal sources;
- supplied data and approved analysis tools;
- participant evidence;
- experiments or operational tests.

Absence of access is a blocker or plan input, not permission to invent results.

## Resume-First Audit

Before framing a new state or dispatching work:

1. Bind the raw request and every supplied file, source, URL, dataset, prior
   brief, decision, constraint, and as-of date.
2. Search the available context for an existing Research State or equivalent
   current artifacts.
3. Mark each stage `current`, `stale`, `conflicting`, `partial`,
   `not applicable`, or `missing`.
4. Reuse current artifacts and accepted evidence. Do not recreate a stage only
   because its named artifact is absent when equivalent evidence already exists.
5. Select the earliest missing or invalidated result whose absence prevents a
   decision or changes the next evidence priority.
6. Create or revise the controller receipt before the first worker dispatch.

Use this receipt:

```markdown
## Research Controller Receipt

Research ID:
State Version:
Primary Question Type:
Dependent Types:
Mode:
Execution Intent:
Decision or Use:
Decision Owner:
Source Boundary:
Current Artifacts:
Earliest Material Gap:
Required Workers:
Conditional Workers:
Review Requirement:
Stop Rule:
```

## Workflow

### Phase 1: Frame and Answer from Existing Information

1. **Restate the question.** Preserve the user's intended answer: a decision
   rule, for example, is different from applying that rule to decide today.
   Reuse supplied context and prior artifacts before asking for more.
2. **Identify necessary definitions.** Surface only ambiguity that changes the
   answer. Reuse an accepted definition; otherwise name the unresolved meaning
   and offer candidate interpretations when useful. A term such as “quality
   trial” may need definition before analysis; the agent need not decide that
   definition for the user. Use `$research-question-framing` or
   `$research-decision-model` for bounded framing/modeling work when needed,
   rather than automatically dispatching both.
3. **Give the current answer or options.** Present what existing information
   supports, with decisive reasons, conditions, and uncertainty. If a full
   answer is unavailable, give the useful partial answer and the exact gap.
   Do not substitute a method explanation for the requested answer. Follow the
   [Decision Brief Contract](references/decision-brief-contract.md), including
   its framework-only and missing-answer rules.
4. **Decide whether more work is necessary.** Distinguish these gaps:

   | Gap | Next action |
   | --- | --- |
   | Meaning, scope, or a business preference only the user can settle | Ask the focused question; offer labeled options without inventing agreement |
   | Missing, stale, conflicting, or insufficient evidence that could change the answer | Enter Phase 2 for that uncertainty within the authorized source boundary |
   | No material gap for the requested output | Complete with the supported answer or options and applicable assurance |

Show this first-pass result before evidence work. A missing user decision does
not by itself justify market, data, or user research. When evidence could help
resolve ambiguity, name that relationship; independent evidence work may
continue without pretending dependent definitions are settled. Questions for
the user and proposed evidence work are both valid next actions.

These phases are conditional work boundaries, not mandatory separate turns or
an approval gate for already authorized passive research. Preserve explicit
research depth, freshness, and review requirements: plausible options alone do
not satisfy a request for evidence-backed comparison. `review-only` retains its
direct review route.

### Phase 2: Resolve Decision-Relevant Evidence Gaps

Enter with the first-pass answer, the specific uncertainty, why resolving it
could change the answer, and the evidence needed. Select data analysis, desk,
market, competitive, user, causal, forecast, or experiment-design work from
that gap; the topic alone does not require all those disciplines.

1. **Map uncertainty.** Run `$research-hypothesis-map` when serious competing
   explanations or what-must-be-true claims have not been represented. Require
   supporting, disconfirming, and decisive signals.
2. **Plan evidence.** Run `$research-evidence-plan` to translate hypotheses and
   criteria into evidence, methods, research priorities, waves, and stop rules.
   Prioritize by expected decision value rather than curiosity or ease.
3. **Dispatch evidence waves.** Select only relevant workers from the routing
   map. Run independent streams in parallel after shared definitions are stable.
   Give every worker a bounded assignment and source boundary.
4. **Accept or reject artifacts.** Check each returned artifact against the
   Evidence Contract. Add accepted rows to the ledger, record contradictions,
   update hypotheses, and invalidate only dependent downstream artifacts.
5. **Open the next barrier.** After each wave, ask whether the current answer is
   robust enough to act, whether one further uncertainty could reverse it, and
   whether a better method exists. Stop low-value research.
6. **Return to the question.** Run `$research-synthesis` when the accepted evidence is
   sufficient to update beliefs and draft the Decision Brief. The synthesizer
   may recommend; it cannot accept its own draft or declare the controller
   complete.
### Completion from Either Phase

1. **Review when required.** Freeze the draft and run `$research-review` for
   deep mode, explicit review, or another review trigger. Review is independent
   judgment, not in-place editing.
2. **Repair deliberately.** When review is conditional or failed, route each
    finding to the artifact owner: framing, model, hypothesis, evidence plan,
    specialist evidence, analysis, forecast, or synthesis. A changed draft
    invalidates the previous review.
3. **Complete honestly.** Choose exactly one terminal state and record the
    next action and revisit triggers.

Phase 1 may finish inline with a concise, source-grounded brief; unused evidence
workers and waves are not prerequisites. Keep the applicable state and
assurance, without manufacturing intermediate artifacts. Neither a missing
definition nor a missing business decision becomes `Monitor` merely because
the agent has listed next steps; use the terminal state matching that gap.

## Stage Selection

| Missing or invalid evidence | Next owner |
| --- | --- |
| Decision/use or question boundaries | `$research-question-framing` |
| Alternatives, criteria, causal/value drivers, or tradeoffs | `$research-decision-model` |
| Competing hypotheses and falsification signals | `$research-hypothesis-map` |
| Research priority, method, waves, or stop rule | `$research-evidence-plan` |
| External, academic, official, or supplied-source facts | `$research-desk` |
| Market/category structure and economics | `$research-market-landscape` |
| Competitor, substitute, or status-quo evidence | `$research-competitive` |
| A participant study or instrument | `$research-user-study` |
| Actual participant material to synthesize | `$research-user-synthesis` |
| Quantitative internal or supplied data | `$research-data-analysis` |
| Causal attribution or counterfactual strength | `$research-causal-analysis` |
| A discriminating pilot or test | `$research-experiment-design` |
| Future probability, range, scenario, or signposts | `$research-forecasting` |
| Belief update and draft recommendation | `$research-synthesis` |
| Independent quality and readiness judgment | `$research-review` |

### Existing Evidence Shortcut

Skip a stage when current material provides the same decision-relevant result.
Examples:

- A user-supplied decision memo may satisfy framing and part of the model.
- A verified analytics report may satisfy one data work item.
- A current API specification may satisfy a desk-research question.
- Existing interviews may require synthesis, not a new study.
- A previous Decision Brief may need only an update and fresh review.

Record what satisfied the stage and why it remains current. Do not create filler
artifacts.

## Research Planning and Value of Information

For every open uncertainty, judge:

```text
research priority
≈ probability that resolving it changes the decision
× consequence of choosing poorly
× current uncertainty
× ability of the method to discriminate
÷ cost, delay, and risk of getting the evidence
```

This is a reasoning aid, not a requirement to manufacture numeric precision.

Prefer evidence that distinguishes live alternatives. Deprioritize a fact when
knowing it more precisely would not change the action. Consider acting,
piloting, staging, or monitoring when research is slower or less informative
than a reversible action.

Every work item must state:

- the decision criterion or hypothesis it informs;
- the signal that would support or weaken it;
- the evidence and method;
- the source boundary;
- the expected artifact;
- the completion evidence;
- the consequence of a positive, negative, conflicting, or unavailable result.

## Evidence Wave Rules

Parallelize only after shared definitions are accepted. A worker owns one
question or evidence package, not the entire research outcome.

Safe examples:

- External market evidence and internal cohort analysis.
- Competitor analysis and user-study planning.
- Separate hypotheses with independent source sets.
- Base-rate research and driver research for a forecast.

Serialize:

- Framing before evidence whose scope depends on it.
- Metric definitions before quantitative analysis.
- Hypothesis definition before causal testing.
- Evidence collection before synthesis.
- Draft freeze before review.
- Review repair before a new completion claim.

Only the controller updates the Research State, accepts evidence, opens a wave,
or dispatches successors.

## Worker Contract

Before delegation, read the routing map and send:

```markdown
## Research Worker Assignment

Research ID:
State Version:
Owner Skill:
Assigned Question:
Decision Use:
Accepted Inputs:
Criterion or Hypothesis:
Source Boundary:
Method Constraints:
Expected Artifact:
Completion Evidence:
Dependencies:
Known Contradictions:
Out of Scope:
```

A worker returns:

- sources or data inspected;
- method and scope;
- artifact;
- evidence-ledger rows;
- limitations and contradictions;
- how the result changes or fails to change the decision;
- recommended next route;
- blockers and unavailable evidence.

Reject artifacts that answer a different question, cross the source boundary,
invent evidence, omit material contrary findings, or overstate the method.

## Contradiction Handling

Do not resolve disagreement by majority vote.

1. Compare definitions, time, population, geography, incentives, and methods.
2. Trace apparently independent sources to their original lineage.
3. Determine whether the disagreement affects a threshold, ranking, causal
   claim, or forecast.
4. Commission a discriminating analysis only when the contradiction can change
   the decision.
5. Preserve unresolved disagreement and lower confidence when it cannot be
   resolved.

## Synthesis Gate

Start synthesis only when:

- the Research Contract and current Decision Model are accepted;
- required research-wave barriers are closed;
- every load-bearing judgment can cite accepted evidence or a labeled
  assumption;
- serious alternatives and counterevidence are present;
- critical unavailable evidence is represented;
- the remaining uncertainty is bounded enough to recommend action, experiment,
  monitoring, or an inconclusive stop.

Synthesis is not a last-minute summary of source briefs. It updates the belief
state and applies the decision model.

## Review Gate

Review is mandatory for deep mode and the triggers in the Research Depth
Contract. Freeze:

- Research State version;
- Decision Brief revision or hash;
- Evidence Ledger revision;
- source boundary and as-of date.

The reviewer returns `pass`, `conditional`, `fail`, or `unknown`. The controller
owns the repair loop and must rerun review after a material change.

## Terminal States

### Decision Ready

Use when the accepted evidence and decision model support a robust or clearly
conditional action. Record recommendation, confidence, owner, next action, and
revisit triggers.

### Experiment Ready

Use when research isolated a decision-critical uncertainty that passive evidence
cannot resolve, and `$research-experiment-design` produced an acceptable
protocol with decision thresholds. Do not claim the hypothesis is proven.

### Monitor

Use when acting now or waiting is appropriate until named signposts change.
Record metric/event thresholds and review cadence.

### Scan Complete

Use only for scan mode when the territory, priors, gaps, and next research
priorities are mapped. Do not label it decision-ready.

### Inconclusive

Use when available evidence cannot distinguish alternatives within the
authorized method, source, time, or budget boundary. Name what would be needed.

### Blocked

Use when a required source, access, definition, participant population,
decision, or method is unavailable. Name the blocker and resume trigger.

### Stopped

Use when continuing would have insufficient decision value, duplicate accepted
work, violate the source boundary, or exceed authorization.

## Output

At completion, provide:

```markdown
## Research Completion

Research ID:
State Version:
Question:
Mode:
As Of:
Terminal Status:
Current Answer:
Confidence:
Decisive Evidence:
Residual Uncertainty:
Next Action:
Next Owner:
Revisit Triggers:
Decision Brief:
Evidence Ledger:
Review:
Sources / Artifacts:
Limitations:
```

Use the template in [assets/decision-brief-template.md](assets/decision-brief-template.md)
when a durable file is needed. A concise answer can link to the full state and
brief; it must not hide uncertainty or skipped assurance.

## Sub-Agent Contract

The invoking thread remains `controller/critical`. Delegate workers according
to the routing map. Each worker receives only the minimum current state and raw
evidence required for its bounded job. Preserve the decision owner, source
boundary, scope, and as-of date across every handoff.

Do not ask a worker to “research everything” or “give the final answer.” Do not
treat a worker’s fluent prose as accepted evidence. Verify artifact boundaries
and update state from observable results.
