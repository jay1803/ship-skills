---
name: research-data-analysis
description: >-
  Analyze supplied or connected quantitative data for a decision-relevant research question. Use when metric definitions, coverage, data quality, trends, cohorts, segments, funnels, retention, economics, relationships, anomalies, or uncertainty must be computed and interpreted. Produces a reproducible Data Analysis Brief with methods and limitations; does not invent unavailable data, mistake positive amounts or labels for semantics, or make causal claims beyond the design.
metadata:
  owner: jay1803
  family: research
  maturity: stable
  distribution: research
---


# Research: Data Analysis

Use quantitative evidence to answer a bounded research question. Establish the
data contract before calculation, validate whether the dataset can support the
claim, and separate descriptive relationships from causal interpretation.

Read the [Evidence Contract](../research/references/evidence-contract.md).

## Boundary

- Own metric definitions, source coverage, data-quality assessment,
  transformations, descriptive and inferential analysis, segmentation,
  uncertainty, sensitivity, reproducible calculations, and quantitative
  evidence-ledger rows.
- Use supplied files or connected data sources only within their authorized
  scope.
- Do not infer field semantics from names or signs when source documentation or
  context is needed.
- Do not invent rows, impute consequential values silently, or hide exclusions.
- Do not claim causality from correlation, before/after movement, or model fit
  alone. Route material causal questions to `$research-causal-analysis`.
- Do not optimize for visual complexity or an attractive dashboard. Choose the
  simplest analysis that changes the decision.

## Data Contract

Before calculating, establish:

```yaml
decision_question:
unit_of_analysis:
population:
time_window:
as_of:
data_sources:
coverage:
refresh_or_sync_status:
metric_definitions:
dimensions:
inclusion_exclusion:
known_missingness:
privacy_or_sensitivity:
```

If coverage is partial, syncing, stale, or mismatched, qualify the result in the
same sentence as the first reported total or trend.

## Workflow

1. Read the Research Contract, Decision Model, hypothesis, evidence assignment,
   and data source documentation.
2. Inventory tables/files/accounts, fields, row counts, date coverage,
   identities/keys, granularity, refresh state, and permissions.
3. Validate definitions, signs, units, currencies, time zones, duplicates,
   joins, missingness, outliers, censoring, survivorship, and selection.
4. Reconcile inconsistent sources or state why they cannot be reconciled.
5. Define the analysis population and baseline before looking for a favorable
   segment.
6. Perform the smallest decision-relevant analysis:
   - totals/rates/distributions;
   - trend and seasonality;
   - cohort or retention;
   - funnel and transition;
   - segment comparison;
   - unit economics;
   - variance/anomaly;
   - relationship or predictive model;
   - scenario or sensitivity.
7. Quantify uncertainty when the sampling or model warrants it.
8. Run robustness checks against reasonable definitions, windows, exclusions,
   and outlier handling.
9. Distinguish observed result, derived fact, inference, and causal hypothesis.
10. Save or describe reproducible transformations and calculations.
11. Return the brief, evidence rows, and causal or data blockers.

## Analysis Rules

- Use denominators and population definitions consistently.
- Compare like periods, cohorts, and maturity windows.
- Do not mix acquisition volume with user quality; define activation,
  retention, value, and cost separately.
- Avoid aggregation that hides segment reversals or survivorship.
- A statistically detectable effect may be decision-irrelevant; report effect
  size and threshold relevance.
- A practically important effect may remain uncertain; do not convert
  uncertainty into zero effect.
- Multiple comparisons and post-hoc slicing increase false discoveries.
- Predictions need held-out or temporal validation when used for action.
- A chart does not repair a weak metric definition.
- Protect sensitive data; aggregate or redact when individual detail is not
  needed.

## Visualization

Create a chart only when it improves judgment. Every chart should show:

- metric and unit;
- population and time;
- denominator where relevant;
- comparison or baseline;
- uncertainty or data gaps when material;
- source/as-of note.

Do not use dual axes or decorative precision that obscures interpretation.

## Output

```markdown
## Data Analysis Brief

Research ID:
Question / Hypothesis:
Decision Use:
Data Sources:
Coverage / Sync Status:
As-Of:
Unit of Analysis:
Population:
Metric Definitions:

### Data Quality
- <Completeness, duplicates, joins, missingness, bias, stale or partial coverage.>

### Method
- <Transformations, comparisons, models, exclusions, uncertainty.>

### Results
| Result | Value / Range | Population / Window | Decision Threshold | Interpretation | Confidence |
| --- | --- | --- | --- | --- | --- |

### Segments / Cohorts
- <Decision-relevant heterogeneity.>

### Robustness and Sensitivity
- <Definition, period, exclusion, model, or outlier check.>

### Causal Limits
- <What the design can and cannot establish.>

### Reproducibility
- <Query, notebook, script, formula, or transformation description.>

### Decision Effect
- <How the analysis updates the criterion or hypothesis.>

### Evidence Ledger Rows
- <Structured quantitative evidence.>

### Recommended Next Route
- <Synthesis, causal analysis, experiment, more data, or stop.>
```

## Sub-Agent Contract

Default route: `worker/standard`; use `worker/deep` for high-stakes,
multi-source, statistical, financial, sensitive, or causal-adjacent analysis.
Return the data contract, quality findings, reproducible method, results,
uncertainty, and decision effect. Do not exceed connected-data coverage.
