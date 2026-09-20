---
name: research-evidence-plan
description: >-
  Translate a Research Contract, Decision Model, and Hypothesis Map into a prioritized evidence program. Use when the team must decide which signals, data, sources, interviews, analyses, or experiments are worth obtaining, in what order, and when to stop. Produces work items, research waves, method choices, value-of-information reasoning, and stop rules; does not fabricate findings or execute side-effecting research.
metadata:
  owner: jay1803
  family: research
  maturity: stable
  distribution: research
---


# Research: Evidence Plan

Choose the smallest evidence program capable of changing or strengthening the
decision. Make the connection from hypothesis to signal to evidence to method
explicit.

Read the [Evidence Contract](../research/references/evidence-contract.md),
[Research Depth Contract](../research/references/research-depth-contract.md),
and [Research Routing Map](../research/references/research-routing-map.md).

## Boundary

- Own critical-uncertainty prioritization, evidence requirements, method
  selection, work items, dependencies, research waves, budget assumptions, and
  stop rules.
- Decide whether an uncertainty is best addressed by desk research, market or
  competitor evidence, user research, internal data, causal analysis,
  forecasting, monitoring, or an experiment.
- Distinguish information that is merely interesting from information likely to
  change the choice or next action.
- Do not execute interviews, surveys, experiments, purchases, outreach, or
  operational changes.
- Do not invent data availability, sample size, source access, or method
  capability.

## Workflow

1. Read the accepted Research Contract, Decision Model, Hypothesis Map,
   existing evidence, mode, source boundary, and resource constraints.
2. List the remaining uncertainties and the exact criterion or hypothesis each
   affects.
3. For each uncertainty, state how different possible findings would change the
   decision, ranking, confidence, or next action.
4. Judge current uncertainty, consequence of error, decision sensitivity,
   method discriminating power, cost, delay, access, and risk.
5. Prioritize using qualitative value-of-information reasoning. Do not require a
   numeric score when the inputs cannot support one.
6. Select the least expensive credible method that can produce the needed
   signal. Reject methods that cannot support the claim strength.
7. Identify source classes, populations, time windows, definitions, and
   freshness requirements.
8. Reuse current evidence and avoid duplicating the same evidentiary lineage.
9. Build dependencies and parallel research waves after shared definitions are
   stable.
10. Define completion evidence and positive, negative, conflicting,
    unavailable, and null-result handling for each work item.
11. Define wave-level stop rules and terminal possibilities.
12. Return the plan to the controller; do not dispatch successors.

## Method Selection

| Need | Candidate owner |
| --- | --- |
| Current official, academic, document, or supplied-source facts | `$research-desk` |
| Market/category/value-chain/channel structure | `$research-market-landscape` |
| Competitor, substitute, status quo, or build-vs-buy evidence | `$research-competitive` |
| Participant recruitment, instrument, interview, survey, or observation plan | `$research-user-study` |
| Synthesis of actual participant material | `$research-user-synthesis` |
| Definitions, quality, trends, cohorts, segments, or quantitative relationships | `$research-data-analysis` |
| Causal attribution, confounding, counterfactual, or mechanism strength | `$research-causal-analysis` |
| A test that changes exposure or behavior to distinguish hypotheses | `$research-experiment-design` |
| Future probability, range, scenarios, and signposts | `$research-forecasting` |

Several methods can be complementary. Do not demand triangulation when one
authoritative source settles the specific claim; do demand it when interested,
indirect, or method-limited evidence carries the decision.

## Value-of-Information Questions

For each uncertainty:

- Could a plausible answer reverse the decision or change the next action?
- How costly is a wrong choice?
- How uncertain are we now?
- Can the proposed method actually distinguish the hypotheses?
- How much does the evidence cost in time, money, access, privacy, and delay?
- Can a reversible pilot or monitoring plan create the information while
  making progress?
- Does the decision expire before the evidence arrives?
- Is the unknown a value judgment that requires the decision owner rather than
  research?

Deprioritize an uncertainty that has high scientific interest but low decision
leverage.

## Research Wave Rules

- Wave 0 resolves definitions, access, source boundary, and method feasibility.
- Later waves contain independent work items whose questions and inputs are
  stable.
- Close a wave only when each required work item is accepted, rejected with a
  reason, or blocked.
- Recalculate priorities after every wave; do not execute the original backlog
  blindly.
- Stop when further evidence is unlikely to change the next action, even if
  unanswered questions remain.

## Output

```markdown
## Evidence Plan

Research ID:
Mode:
Decision or Use:
Source Boundary:
Resource / Timing Constraints:

### Critical Uncertainties
| ID | Unknown | Criterion / Hypothesis | How It Could Change the Decision | Current Uncertainty | Consequence of Error | Priority Rationale |
| --- | --- | --- | --- | --- | --- | --- |

### Evidence Work Items
| Work ID | Question | Signal | Evidence / Source | Method | Owner Skill | Dependencies | Completion Evidence | Result Handling |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |

### Research Waves
- Wave 0: <definitions/access/method>
- Wave 1: <parallel high-value evidence>
- Wave 2: <conditional work triggered by Wave 1>

### Existing Evidence Reused
- <Artifact and why it remains current.>

### Deliberately Not Researched
- <Unknown and why its decision value is low.>

### Stop Rules
- Decision Ready when:
- Experiment Ready when:
- Monitor when:
- Inconclusive when:
- Blocked when:

### Recommended Next Route
- <First authorized work item(s), not a self-dispatch.>
```

## Sub-Agent Contract

Default bounded route: `worker/deep`. Return a plan, not findings. Preserve the
source and authorization boundary. Explicitly mark side-effecting evidence
collection as requiring separate execution authority.
