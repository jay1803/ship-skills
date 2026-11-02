# Review Depth

Read before dispatching any reviewer. Depth follows the selected mode and the
changed semantics; neither a green test nor a small diff proves low impact.

| Route | When | Reviewers |
| --- | --- | --- |
| `focused` | Prior findings and a repair diff are supplied | One reviewer |
| `lightweight` | `fast` or `standard` with no protected boundary | One reviewer |
| `full` | `strict`, an explicit full request or binding full/three-lens policy, or a changed protected boundary | Two finders and the Judge |

Protected boundaries include authorization, security/privacy, destructive data,
schema/migration, concurrency/ownership and shared/public contracts.
Classification follows the changed semantics, not the filename: fixing an
ordinary comment in an auth file is not an auth change, while changing one
comparison in an auth check is. Normative product/agent instructions,
build/config, generated outputs and executable comments are not mechanical just
because they contain no runtime code. Strict also inspects related failure,
recovery and concurrency paths.

A route is not a pass. A skipped or omitted review is never `approved` or
`clean`. Preserve validation, Product/Design, CI, posting and merge authority.

## Shared packet

Give each reviewer only:

- the frozen repository/PR/base/head and the full current diff, with relevant
  enclosing code and directly affected callers;
- governing requirement and acceptance sources with their precedence, any
  required claims with unchanged wording, and explicit no-fix boundaries;
- current validation facts, the selected mode and the severity policy;
- which required sources the runtime can read, and any unavailable capability
  with its effect on the assigned surface.

Never forward implementer reasoning, sibling outputs, credentials or posting
permission. Supply a long authority as a complete readable snapshot with its
source and revision; the reviewer cites the provisions it relies on. If a
source turns out to be missing, supplement the same reviewer on the unchanged
target, or rerun only that reviewer with a complete packet.

## Lightweight

One reviewer answers in one pass: does the change satisfy the governing
requirement, introduce a concrete behavioral defect, or create a material local
maintainability problem? Use the correctness
[search angles](../../review-correctness/references/correctness-findings-contract.md#search-angles)
and the [repository-instruction check](../../review-code-quality/references/code-quality-findings-contract.md#repository-instructions).
Before returning, check each candidate against the code and label it with a
Judge [disposition](../../review-judge/references/judge-contract.md#candidate-dispositions).
Load related source only where needed; no exhaustive rubric audit.

If the reviewer finds a changed protected boundary or broader impact, it returns
that evidence and Review reruns as full on the complete current target. The
lightweight output is kept, not converted into finder outputs. Ask the reviewer
for a bounded clarification of a gate-relevant ambiguity; an unresolved one is
`blocked`, not silently regraded.

## Focused

Give one reviewer the prior result's open findings with their native IDs, the
repair diff, the governing acceptance sources and the current target. It checks
that each finding is fixed, then inspects the delta and the sibling or caller
paths it implicates, including stateful lifecycle paths
(reset/cancel/disconnect/delete, late callbacks, stale identities) when the
changed invariant touches them. Green tests alone cannot close a finding. New
findings follow the same verification and dispositions; a protected boundary in
the delta escalates to full.

## Full

Dispatch the correctness and maintainability finders together, each with the
shared packet. Collect both before judgment, even if one reports a defect or a
missing authority; no partial set may be judged. Give the Judge both unchanged
outputs, the target, required claims and read access to the frozen head.
