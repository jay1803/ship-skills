---
name: research-competitive
description: >-
  Investigate and compare the alternatives competing for the same user, buyer, budget, workflow, or strategic outcome. Use when direct competitors, indirect solutions, substitutes, status quo, internal build, partner, or no-action options need current evidence on product, pricing, distribution, capabilities, adoption, or strategic behavior. Produces a decision-aligned Competitive Evidence Brief; does not infer hidden strategy as fact or reduce the analysis to a feature matrix.
metadata:
  owner: jay1803
  family: research
  maturity: stable
  distribution: research
---


# Research: Competitive Research

Understand what alternatives compete for the same outcome and why users or
decision makers choose them. Compare them against the accepted Decision Model,
not against an arbitrary feature checklist.

Read the [Evidence Contract](../research/references/evidence-contract.md).

## Boundary

- Own alternative-set discovery and current evidence about direct competitors,
  indirect solutions, substitutes, status quo, build, buy, partner, and delay.
- Compare products, workflows, pricing, positioning, distribution, switching,
  capabilities, constraints, and observable strategic moves when relevant.
- Distinguish observations, company claims, user reports, and analyst inference.
- Do not present inferred market share, traction, quality, or strategy as fact.
- Do not write the final recommendation or imitate a competitor without
  checking strategic fit.
- Do not collect sensitive, private, deceptive, or unauthorized information.

## Workflow

1. Read the Research Contract, Decision Model, assigned hypotheses, market
   definition, scope, and as-of date.
2. Define the competitive job or resource: what user outcome, buyer budget,
   workflow, attention, channel, platform position, or capability is contested?
3. Build the alternative set:
   - direct products or organizations;
   - indirect solutions and adjacent categories;
   - manual or internal workflows;
   - status quo, no action, delay, or do-it-yourself;
   - partners, platforms, or complements that can become substitutes.
4. Select only alternatives capable of changing the decision. Explain
   exclusions.
5. Gather current evidence from primary product materials, pricing, demos,
   documentation, filings, release notes, observed workflows, user evidence, and
   credible independent sources.
6. Compare alternatives on the accepted criteria and what-must-be-true claims.
7. Analyze mechanisms of advantage: distribution, data, network, workflow lock,
   cost structure, brand/trust, ecosystem, speed, regulation, or capability.
8. Identify strategic groups and patterns instead of producing a flat list.
9. Look for counterexamples: weak incumbents, failed entrants, non-consumption,
   and alternatives users reject.
10. State evidence gaps, source incentives, freshness, and where inference begins.
11. Return evidence-ledger rows and decision implications.

## Comparison Rules

- Features matter only when they alter an accepted outcome, switching decision,
  cost, risk, or distribution.
- Company website claims establish positioning and published capability, not
  independent performance.
- Pricing must record date, plan, unit, conditions, and hidden comparison limits.
- User reviews can reveal recurring experience but usually cannot establish
  prevalence without a sampling frame.
- Funding, headcount, traffic, app rank, and social attention are imperfect
  proxies. State the inference and limits.
- Distinguish current advantage from a capability the decision owner could
  build.
- Avoid copying a competitor's surface solution when the underlying job,
  segment, business model, or distribution differs.
- Include the status quo. It is often the strongest competitor.
- Preserve unknowns; do not fill private strategy with a plausible story.

## Output

```markdown
## Competitive Evidence Brief

Research ID:
Assigned Decision:
Competitive Job / Resource:
Scope:
As-Of Date:

### Alternative Set
| Alternative | Type | Target / Job | Why It Competes | Included / Excluded |
| --- | --- | --- | --- | --- |

### Decision-Aligned Comparison
| Criterion / Hypothesis | Alternative Evidence | Source Type | Current Judgment | Confidence |
| --- | --- | --- | --- | --- |

### Observable Positioning and Behavior
- <What is directly observed or officially claimed.>

### Inferred Advantages and Constraints
- <Inference, supporting evidence, alternative explanation.>

### Strategic Groups and Patterns
- <Meaningful clusters or common models.>

### Counterexamples and Failures
- <Evidence that challenges the obvious narrative.>

### Gaps and Freshness Risks
- <What cannot be established.>

### Decision Implications
- <How this changes or fails to change the Decision Model.>

### Evidence Ledger Rows
- <Structured rows.>

### Recommended Next Route
- <Controller recommendation only.>
```

## Sub-Agent Contract

Default route: `worker/standard`; use `worker/deep` when competitive evidence
is opaque, high-stakes, regulated, or rapidly changing. Preserve claim types
and source incentives. Return the brief and evidence rows without final
commitment.
