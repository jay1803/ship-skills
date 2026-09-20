---
name: research-user-study
description: >-
  Design a decision-relevant user, customer, stakeholder, operator, or expert study. Use when interviews, surveys, contextual inquiry, observation, usability sessions, diary work, or concept tests are needed but the sampling frame, recruitment, instrument, consent, evidence standard, or analysis plan is not yet credible. Produces a User Study Plan and instrument; does not fabricate participants, conduct outreach, or report findings that were not collected.
metadata:
  owner: jay1803
  family: research
  maturity: stable
  distribution: research
---


# Research: User Study

Design the smallest participant study capable of reducing a decision-critical
uncertainty. Treat recruitment, instrument, consent, observation, and analysis
as parts of one evidence method.

Read the [Evidence Contract](../research/references/evidence-contract.md) and
[Research Depth Contract](../research/references/research-depth-contract.md).

## Boundary

- Own the research objective, participant population, sampling logic,
  recruitment criteria, method, session protocol, interview or survey
  instrument, consent/privacy requirements, capture plan, analysis plan, and
  completion evidence.
- Design studies for users, customers, non-users, churned users, buyers,
  operators, stakeholders, domain experts, or other actors when their evidence
  is decision-relevant.
- Do not invent participant quotes, sample composition, response rates,
  findings, or saturation.
- Do not contact people, schedule sessions, send surveys, record participants,
  or offer incentives without explicit authorization and the appropriate tool.
- Do not ask participants to decide the product or strategy. Study behavior,
  context, needs, tradeoffs, and reactions; the decision owner retains judgment.
- Do not use a survey when the constructs and answer options are not understood,
  or use a few interviews to estimate population prevalence.

## Study Selection

Choose the method that can observe the needed signal.

| Research need | Candidate method |
| --- | --- |
| Understand context, workflow, language, motivations, or unknown needs | Semi-structured interview or contextual inquiry |
| Observe actual behavior or breakdowns | Direct observation, diary, log-assisted interview |
| Test comprehension, usability, or workflow | Moderated or unmoderated task study |
| Compare reactions to bounded concepts | Concept test with explicit tradeoffs |
| Estimate prevalence after constructs are defined | Survey with sampling and measurement plan |
| Understand choice tradeoffs | Forced choice, ranking, conjoint-like design when justified |
| Learn from specialist knowledge | Expert interview, with expertise and conflict-of-interest record |
| Study longitudinal behavior | Diary or repeated-measure study |

Mixed methods are justified when one method defines the construct and another
estimates or tests it. More methods are not automatically better.

## Workflow

1. Read the Research Contract, Decision Model, Hypothesis Map, Evidence Plan,
   existing user evidence, source boundary, and privacy constraints.
2. State the exact decision-critical uncertainty and how participant evidence
   could change the decision.
3. Define the target population and the dimensions that matter for sampling:
   behavior, lifecycle stage, segment, role, geography, device, experience,
   success/failure state, or another relevant variable.
4. Set inclusion, exclusion, diversity, and negative-case criteria. Avoid a
   convenience sample that structurally cannot answer the question.
5. Select method, session format, sample rationale, recruitment channel,
   incentive assumptions, timing, and stopping logic.
6. Design neutral tasks and questions. Start from recent concrete behavior before
   opinion, speculation, or proposed solution.
7. Include disconfirming prompts, alternative explanations, tradeoffs, and
   counterexamples.
8. Specify consent, recording, data minimization, retention, anonymization, and
   access. Do not collect sensitive data without a clear need and authorization.
9. Define capture and analysis: notes, transcript, task outcome, coding frame,
   segment comparison, survey analysis, and evidence-ledger output.
10. Pilot the instrument when feasible. Record what would make the study
    inconclusive or require revision.
11. Return the plan and exact authorization/access blockers.

## Interview Rules

- Ask about actual recent situations before hypothetical future behavior.
- Avoid leading, compound, loaded, and solution-confirming questions.
- Ask for the sequence, context, trigger, workaround, cost, alternatives, and
  consequence.
- Separate user, buyer, payer, approver, and operator when roles differ.
- Do not treat stated willingness to pay or adopt as observed behavior.
- Ask what would make the participant choose differently.
- Use the same core questions across participants while allowing relevant
  follow-up.
- Protect participant dignity and avoid unnecessary personal information.

## Survey Rules

- Define the construct before writing response options.
- Use mutually interpretable scales and include appropriate “not applicable” or
  “do not know” options.
- Avoid double-barreled questions and false precision.
- Plan sampling, non-response handling, segmentation, and uncertainty.
- Do not infer representativeness from a large convenience sample.
- Predefine primary questions and comparisons where the result will drive a
  consequential decision.

## Study Plan Output

```markdown
## User Study Plan

Research ID:
Decision Use:
Critical Uncertainty:
Hypotheses / Criteria:
Method:
Why This Method Can Discriminate:

### Participants
Target Population:
Sampling Dimensions:
Inclusion:
Exclusion:
Negative / Counterexample Cases:
Sample Rationale:
Recruitment:
Incentive Assumption:

### Protocol
Format:
Duration:
Environment:
Materials / Concepts:
Tasks:
Core Questions:
Disconfirming Questions:
Pilot:

### Evidence and Analysis
Capture:
Primary Signals:
Coding / Analysis:
Segment Comparisons:
Null / Conflicting Result Handling:
Completion Evidence:

### Ethics, Consent, and Privacy
Consent:
Recording:
Sensitive Data:
Anonymization:
Retention:
Access:

### Execution Requirements
Authorization Needed:
Tools / Accounts:
Owner:
Timing:
Risks / Blockers:

### Instrument
<Exact guide, survey, task script, or observation sheet.>

### Recommended Next Route
After real collection: `$research-user-synthesis`.
```

## Sub-Agent Contract

Default route: `worker/standard`; use `worker/deep` for sensitive, expert,
longitudinal, statistically consequential, or multi-population studies. Return a
plan and instrument only. Mark every operational action that still needs
authorization.
