---
name: research-market-landscape
description: >-
  Map the decision-relevant structure of a market, category, ecosystem, channel, or technology landscape. Use when demand, segments, jobs, value chain, distribution, business models, economics, regulation, maturity, trends, or structural constraints must be understood before choosing an opportunity or strategy. Produces a Market Landscape Brief grounded in sources; does not substitute market size or trend popularity for strategic fit.
metadata:
  owner: jay1803
  family: research
  maturity: stable
  distribution: research
---


# Research: Market Landscape

Explain how a market or ecosystem works well enough to identify the structural
forces that matter to the accepted decision. Focus on mechanisms, segments,
economics, distribution, and change rather than producing market-size theater.

Read the [Evidence Contract](../research/references/evidence-contract.md).

## Boundary

- Own category definition, demand structure, actor/segment map, jobs and buying
  context, value chain, distribution, business models, economics, maturity,
  regulation, technology constraints, structural trends, and uncertainty.
- Use the accepted Decision Model to decide which dimensions matter.
- Distinguish addressable opportunity for this decision owner from a broad
  headline market.
- Do not rank the final strategic alternatives or commit the roadmap.
- Do not treat a large TAM, fast growth rate, popular narrative, or competitor
  funding as proof of fit.
- Do not fabricate proprietary market data or precision unavailable from the
  sources.

## Workflow

1. Define the market/category boundary, geography, customer/actor, time horizon,
   and decision use.
2. Clarify the unit of analysis: users, buyers, transactions, workloads,
   channels, spend, revenue, installed base, or another measure.
3. Map demand: jobs, triggers, frequency, urgency, current workarounds, and
   willingness or ability to change.
4. Segment by variables that change needs, economics, access, behavior, or
   adoption; avoid decorative demographic splits.
5. Map the ecosystem and value chain: suppliers, platforms, distributors,
   complements, gatekeepers, standards, and power.
6. Explain business models and economics: who pays, why, pricing basis,
   acquisition/distribution cost, switching cost, margins or constraints when
   evidence exists.
7. Assess distribution and channel structure: where discovery, evaluation,
   purchase, adoption, and retention happen.
8. Assess category maturity, concentration, regulation, technical constraints,
   and structural barriers.
9. Identify trends and drivers, separating durable mechanisms from recent
   attention.
10. Show uncertainties, source limits, countertrends, and what would alter the
    opportunity judgment.
11. Return evidence-ledger rows and decision implications.

## Analysis Rules

- Define the market from the decision problem, not from the largest available
  report category.
- Separate user, buyer, payer, operator, and beneficiary where they differ.
- Distinguish total activity from reachable demand and reachable demand from
  attractive demand.
- Avoid adding incompatible market estimates. Explain definitions and ranges.
- Treat analyst market-size estimates as model outputs with assumptions, not
  observed facts.
- Identify non-consumption and status quo when they compete for behavior.
- Use historical change to test whether a claimed trend is new, cyclical, or
  durable.
- Include regulatory, platform, and distribution dependence when these can
  dominate product quality.
- Identify where the decision owner can build an advantage rather than only
  where current demand is largest.
- State whether the landscape is evidence of an opportunity, a prior for
  further research, or merely context.

## Optional Quantification

Quantify only when the unit and sources support it:

```text
reachable opportunity
= relevant population or workload
× incidence/frequency
× reachable share
× plausible adoption or conversion
× economic value
```

This is a modeling scaffold. Every term needs a definition, source, range, and
sensitivity. Do not present a single point estimate when uncertainty dominates.

## Output

```markdown
## Market Landscape Brief

Research ID:
Assigned Decision:
Market / Category Definition:
Geography:
Time Horizon:
Unit of Analysis:
As-Of Date:

### Demand and Jobs
- <Actor, situation, job, trigger, frequency, urgency, substitute.>

### Segments
| Segment | Distinguishing Need / Behavior | Access / Economics | Evidence | Relevance |
| --- | --- | --- | --- | --- |

### Ecosystem and Value Chain
- <Actors, flows, gatekeepers, complements, bargaining power.>

### Distribution and Channels
- <Discovery, evaluation, acquisition, adoption, retention surfaces.>

### Business Models and Economics
- <Who pays, pricing basis, cost, switching, margin or constraint.>

### Maturity, Regulation, and Structural Constraints
- <Stage, concentration, standards, policy, platform or technical dependency.>

### Trends and Countertrends
| Driver | Mechanism | Evidence | Durability | Counterevidence |
| --- | --- | --- | --- | --- |

### Opportunity Implications
- <What the landscape makes more or less plausible for the Decision Model.>

### Unknowns and Source Limits
- <Decision-relevant gap.>

### Evidence Ledger Rows
- <Structured rows.>

### Recommended Next Route
- <Usually competitive, user, data, hypothesis, or synthesis work.>
```

## Sub-Agent Contract

Default route: `worker/standard`; use `worker/deep` for multi-sided,
regulated, capital-intensive, or rapidly changing markets. Return the landscape,
evidence rows, definitions, and decision implications. Do not issue the final
strategic commitment.
