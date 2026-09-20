---
name: pm-data-analytics
description: Design feature success metrics, event semantics, and privacy-aware measurement plans. Excludes analyzing datasets or implementing dashboards.
metadata:
  owner: jay1803
  family: product
  maturity: stable
  distribution: product
---

# PM: Data & Analytics

Define what should be measured and learned without over-instrumenting the product.

For a standalone analysis or draft, follow the
[Product Artifact Contract](../pm/references/artifact-contract.md) and complete
the requested artifact without tracker setup. The tracker steps below apply
only to an issue-bound lifecycle or authorized publication.

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

## Tracker Write Authority

When the analytics plan belongs on a Linear issue, reply under the single `## PM Workflow` root. If no root exists, use `$pm` intake/root initialization; do not create a separate top-level PM comment. Do not edit the issue description or tracker metadata.

When live tracker tools cannot reply or edit the root, produce exact reply text instead of creating a separate top-level comment or claiming the artifact was posted.

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
