---
name: research-forecasting
description: >-
  Produce a calibrated forecast for a resolvable future target using base rates, drivers, constraints, scenarios, probabilities or ranges, and update signals. Use when an open question depends on what is likely by a defined horizon, including market, technology, adoption, policy, product, operational, or strategic futures. Produces a Forecast Brief with an as-of date and signposts; does not present a scenario as inevitable or use false precision.
metadata:
  owner: jay1803
  family: research
  maturity: stable
  distribution: research
---


# Research: Forecasting

Estimate an unresolved future outcome in a form that can be checked and updated.
Anchor on a resolvable target, reference classes, causal drivers, constraints,
and explicit uncertainty.

Read the [Evidence Contract](../research/references/evidence-contract.md) and
[Question Type Contract](../research/references/question-type-contract.md).

## Boundary

- Own target definition, resolution criteria, as-of date, horizon, base rates,
  reference classes, drivers, constraints, dependencies, scenarios,
  probabilities or ranges, uncertainty, signposts, and update cadence.
- Use accepted current evidence and clearly label judgment.
- Distinguish forecast from scenario, aspiration, plan, and decision threshold.
- Do not declare a future inevitable or treat a vivid narrative as probability.
- Do not produce a precise number when the evidence supports only a range or
  direction.
- Do not hide model uncertainty, regime change, correlated drivers, or unknown
  unknown exposure.

## Preconditions

Require a target that can eventually resolve:

```text
variable or event
population / geography / system
unit and threshold
horizon or resolution date
as-of date
resolution source or rule
```

When the user's wording is not resolvable, return to
`$research-question-framing`.

## Workflow

1. Define the forecast target and how it will be scored or judged later.
2. Establish the outside view: relevant historical base rate, reference class,
   adoption curve, comparable transition, or prior distribution.
3. Establish the inside view: current state, mechanisms, drivers, constraints,
   dependencies, and planned interventions.
4. Check whether the reference class is genuinely comparable and whether a
   regime change makes it weak.
5. Decompose the target into drivers or conditional events without multiplying
   speculative precision.
6. Build a central case and meaningful upside/downside or alternative scenarios.
7. Assign probabilities, intervals, or qualitative confidence appropriate to
   the evidence. Ensure scenario probabilities are coherent when they are meant
   to be exhaustive.
8. Identify correlations, tail risks, bottlenecks, irreversible events, and
   feedback loops.
9. Compare with market consensus, expert views, or current plans when available;
   preserve disagreement and incentives.
10. Perform sensitivity: which driver, threshold, or assumption moves the
    forecast most?
11. Define leading indicators and signposts that update the forecast before the
    horizon.
12. Record the forecast, rationale, source/evidence ledger, and update cadence.

## Forecast Rules

- Begin with the outside view before explaining why this case is different.
- Separate uncertainty in the world from uncertainty in the model.
- Use conditional forecasts when the outcome depends on a decision or
  intervention: `P(Y | action A)` versus `P(Y | status quo)`.
- A forecast can be useful without a single-point estimate.
- Use wide intervals when structural uncertainty dominates.
- Do not average expert numbers without understanding their information,
  independence, incentives, and definitions.
- Preserve known disagreement rather than converting it into artificial
  consensus.
- State what would make the forecast wrong.
- Record the forecast before the outcome when calibration or learning matters.
- Update from material evidence; do not rewrite the original forecast as though
  it was always current.

## Scenario Rules

A scenario is a coherent conditional world, not a prediction by itself. Each
scenario should state:

- triggering conditions;
- driver configuration;
- mechanism;
- observable signposts;
- outcome implications;
- assigned probability or qualitative plausibility if justified.

Avoid scenario sets that omit the base case or differ only in adjectives.

## Output

```markdown
## Forecast Brief

Research ID:
Decision Use:
Target:
Resolution Rule / Source:
Population / Geography / System:
Unit / Threshold:
As-Of Date:
Horizon:

### Base Rate / Reference Class
- <Evidence, comparability, limits.>

### Current State
- <Accepted starting facts.>

### Drivers and Constraints
| Driver / Constraint | Mechanism | Evidence | Direction | Uncertainty |
| --- | --- | --- | --- | --- |

### Forecast
Central Estimate / Range:
Probability:
Confidence:
Conditions:

### Scenarios
| Scenario | Conditions | Probability / Plausibility | Outcome | Signposts |
| --- | --- | --- | --- | --- |

### Sensitivity and Tail Risk
- <What moves the forecast and what could break the model.>

### Disagreement
- <Alternative forecast, source, and reason.>

### Update Plan
Leading Indicators:
Revisit Thresholds:
Review Cadence:
Next As-Of Date:

### Decision Effect
- <How the forecast changes or conditions the current decision.>

### Evidence Ledger Rows
- <Structured rows.>
```

## Sub-Agent Contract

Default route: `worker/deep` for long-horizon, strategic, financial, policy, or
regime-sensitive forecasts; otherwise `worker/standard`. Return a resolvable,
dated forecast with uncertainty and signposts. Do not collapse scenarios into
certainty.
