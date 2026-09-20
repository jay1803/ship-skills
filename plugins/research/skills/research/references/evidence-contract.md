# Evidence Contract

This contract governs every evidence-producing and evidence-consuming skill in
the Research family.

## Statement Types

Every material statement in the evidence ledger or Decision Brief must be
recognizable as one of:

| Type | Meaning |
| --- | --- |
| `source_claim` | What a named source asserts |
| `observation` | What was directly measured, seen, or recorded in the accepted material |
| `derived_fact` | A reproducible calculation or transformation from accepted data |
| `inference` | A conclusion supported by evidence but not directly observed |
| `assumption` | A working premise not yet established |
| `judgment` | A decision-relevant evaluation or recommendation |
| `forecast` | A claim about an unresolved future outcome |

Do not translate an organization’s claim into an independent fact merely
because it is written in an official document. Do not hide an assumption inside
a confident sentence.

## Evidence Ledger Row

```yaml
evidence_id:
claim_or_question:
statement_type:
finding:
source:
  title:
  author_or_owner:
  publisher:
  date:
  url_or_path:
  accessed_at:
source_class: primary | official | academic | independent_secondary | company | community | model_output
method:
population_or_scope:
time_scope:
quality:
  directness: high | medium | low
  credibility: high | medium | low
  independence: high | medium | low
  freshness: current | aging | stale | unknown
limitations:
supports:
contradicts:
confidence:
accepted_by_controller: false
```

Use only fields that add decision value. A citation alone is not a quality
assessment.

## Source Precedence

Prefer the closest credible source to the claim:

1. Direct measurements, first-party records, supplied datasets, original
   artifacts, laws/regulations, official specifications, or primary research.
2. Reputable independent analysis with transparent method and citations.
3. Company materials for the company’s own features, policies, pricing, and
   stated strategy; treat performance and comparative claims as interested.
4. Journalism, analyst reports, reviews, communities, and social content for
   discovery, triangulation, lived experience, and leads.
5. Search snippets, aggregators, and model-generated summaries only as
   navigation aids unless the underlying source is inspected.

Authority is claim-dependent. A user interview can be primary evidence of that
participant’s experience, not of market prevalence. Official documentation can
be primary evidence of a published API contract, not necessarily real-world
reliability.

## Quality Dimensions

Judge evidence across:

- **Relevance**: does it bear on the accepted decision model or hypothesis?
- **Directness**: how many inferential steps separate it from the claim?
- **Credibility**: are provenance, method, definitions, and incentives clear?
- **Independence**: do several citations trace back to the same dataset, press
  release, expert, or commercial interest?
- **Freshness**: is it current enough for the claim’s rate of change?
- **Coverage**: what population, segment, geography, period, and conditions does
  it represent?
- **Method validity**: can the design support the strength of claim made?
- **Consistency**: does it cohere with or conflict with other accepted evidence?

Source count is never a substitute for these dimensions.

## Freshness

Record an as-of or access date for volatile claims. Verify current facts such
as prices, product behavior, laws, office holders, market conditions, API
contracts, and schedules against current sources. Preserve older evidence when
it establishes a trend or historical state.

When sources conflict:

1. Check definitions, population, geography, period, and method.
2. Check whether one source is derivative or stale.
3. Prefer the source closest to the underlying observation for the specific
   claim.
4. Keep the disagreement visible when it cannot be reconciled.
5. Lower confidence or change the decision rule instead of choosing the more
   convenient number.

## Independence and Triangulation

Several sources are independent only when their underlying observations or
methods are materially distinct. Two articles quoting the same company study
are one evidentiary lineage.

Triangulation can combine:

- External primary/official sources.
- Independent secondary analysis.
- Internal behavioral data.
- User or expert evidence.
- A controlled or quasi-controlled test.
- A counterexample or negative case.

Require diversity only when it improves the decision. One definitive primary
source can be stronger than many summaries.

## Supplied-Source Boundary

When the user asks to use only attached, supplied, or named sources:

- Treat the boundary as hard.
- Do not fill missing facts from memory or external search.
- State which requested points are unsupported by the supplied material.
- Separate source-derived content from any explicitly authorized inference.
- Acknowledge contradictions and omissions instead of silently reconciling them.

When external research is authorized, distinguish supplied-source evidence from
newly gathered evidence.

## Citation and Quotation

- Cite at claim level when practical.
- Capture URLs or local paths and enough metadata to identify the source.
- Paraphrase rather than copying long passages.
- Quotes must be short, exact, and used only when wording itself matters.
- Never cite a source for a stronger claim than it supports.
- Never fabricate a citation, participant, dataset, statistic, or access result.

## Confidence

Confidence is a judgment about the claim under the stated scope. It is not the
same as source prestige or probability.

Use calibrated language or a simple scale:

- `high`: strong, direct, current evidence; serious alternatives are weak.
- `medium`: useful evidence with material limitations or plausible alternatives.
- `low`: sparse, indirect, stale, conflicting, or method-limited evidence.
- `unknown`: the available material does not support a bounded judgment.

For forecasts, use probabilities or ranges only when they are meaningful and
explain their basis. Avoid fake precision.

## Acceptance Gate

A worker artifact is acceptable only when:

- It answers the assigned question and respects the source boundary.
- Material findings have provenance.
- Statement types and uncertainty are honest.
- Scope, method, and limitations are explicit.
- Contradictory or disconfirming evidence is not omitted.
- The artifact states how it changes or fails to change the decision.
- It does not claim whole-research completion.
