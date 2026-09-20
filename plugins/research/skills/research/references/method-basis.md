# Method Basis

This family is an operational synthesis for agent research rather than a copy
of any one external methodology. The following sources support several of its
central design choices.

## Analytic Standards

Office of the Director of National Intelligence, Intelligence Community
Directive 203, Analytic Standards:

- https://www.dni.gov/files/documents/ICD/ICD-203.pdf
- https://www.dni.gov/index.php/ic-legal-reference-book/123-about

Relevant principles include describing source and method quality, expressing
uncertainty, distinguishing underlying information from assumptions and
judgments, analyzing alternatives, maintaining customer relevance, using clear
logical argumentation, and explaining changes or significant differences in
analytic judgment.

Applied here:

- Evidence Contract statement types.
- Alternative and counterevidence requirements.
- Calibrated confidence.
- Versioned belief changes.
- Decision-owner relevance.

## Value of Information

U.S. Geological Survey materials:

- https://www.usgs.gov/publications/introduction-prediction-and-value-information
- https://www.usgs.gov/publications/a-simplified-method-value-information-using-constructed-scales
- https://www.usgs.gov/publications/value-information-analysis-a-decision-support-tool-biosecurity

Relevant principle: reducing uncertainty is valuable to the extent that it
improves the decision or expected outcome. A scientifically interesting unknown
may have little decision value; a narrow uncertainty can dominate the value of
additional research.

Applied here:

- Evidence Plan prioritization.
- Research wave barriers.
- Stop rules.
- `Experiment Ready` and `Monitor` terminal states.
- Rejection of exhaustive research as a default.

## Evaluation and Causal Methods

HM Treasury, The Magenta Book and Annex A, updated May 15, 2026:

- https://www.gov.uk/government/publications/the-magenta-book
- https://www.gov.uk/government/publications/the-magenta-book/magenta-book-central-government-guidance-on-evaluation-html
- https://www.gov.uk/government/publications/the-magenta-book/magenta-book-annex-a-analytical-methods-for-use-within-an-evaluation-html
- https://www.gov.uk/government/publications/the-magenta-book/quality-in-policy-impact-evaluation-qpie-html

Relevant principles include scoping an evaluation around its intended use,
selecting methods that fit the question, data, resources, timing, and context,
and requiring a credible counterfactual or appropriate theory-based reasoning
before making attributable impact claims.

Applied here:

- Question-type-specific completion.
- Data, Causal Analysis, Experiment Design, and Evaluation routes.
- Counterfactual and confounding checks.
- Method-strength limits on claims.
- Quality assurance for evidence synthesis.

## Repository Architecture Basis

The family follows the repository’s own Skill architecture:

- one primary job per worker;
- orchestration only where controller state, phase ownership, barriers, and
  completion would otherwise drift;
- conditional depth in references;
- deterministic validation in scripts;
- behavior contracts that inspect observable routing and completion rather than
  exact prose.

The repository source remains authoritative for packaging and lifecycle
conventions. This file records methodological support, not a new repository
policy.
