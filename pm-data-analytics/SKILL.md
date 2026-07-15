---
name: pm-data-analytics
description: >-
  Define product analytics for a feature or change. Use for success metrics, guardrail metrics, events, properties, failure signals, dashboards, learning questions, and privacy-aware measurement plans.
---

# PM: Data & Analytics

Define what should be measured and learned without over-instrumenting the product.

## Workflow

1. Confirm the product goal and behavior being measured.
2. Define success metrics, guardrail metrics, and failure signals.
3. Map key user or system moments to analytics events.
4. Identify learning questions and when to review the data.
5. Keep event payloads minimal and privacy-aware; do not invent sensitive tracking.

## Measurement Rules

- Prefer metrics tied to the product goal, not vanity counts.
- Include guardrails when a feature could increase errors, latency, churn, support load, privacy risk, or user frustration.
- Mark event names and properties as proposed unless an existing analytics schema is verified.
- Avoid collecting PII or detailed content unless there is a clear product need and privacy rule.
- If analytics are not needed for the current slice, say so and explain why.

## Sub-Agent Contract

This skill is safe to run inline or as a bounded sub-agent. When delegated:

- Use only the request, provided sources, and directly referenced tracker context.
- Produce the analytics plan and any allowed tracker comment or draft.
- Follow this skill's tracker-write rules; do not edit issue descriptions unless this skill explicitly owns that write.
- Return sources read, writes applied or drafts, blockers, and open questions.

## Output

```markdown
## Analytics Plan

### Success Metrics
- <Metric, definition, expected direction, review window.>

### Guardrail / Failure Signals
- <Signal that would show harm, regression, or low quality.>

### Proposed Events
| Event | Trigger | Properties | Purpose |
| --- | --- | --- | --- |
| <event_name> | <moment> | <minimal properties> | <question answered> |

### Learning Questions
- <What we need to learn after launch.>

### Privacy / Data Notes
- <Data minimization, sensitive data, retention, or consent constraint.>
```
