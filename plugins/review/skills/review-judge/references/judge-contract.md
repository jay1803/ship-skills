# Finding Judge Contract

Use this contract to verify and combine the two finder outputs of one full
review: correctness (including any specification findings) and
maintainability. It owns verification, grouping, coverage and action selection.

## Judgment Boundary

The judge verifies source claims against the frozen code. For each candidate,
read only the cited locations plus the callers, guards or callees needed to
confirm or refute it; complete evidence fields do not replace that check. It
must not search for new findings, reinterpret the governing product contract,
rerun a reviewer, call a provider, repair code, or publish a result.

Check that each output names the frozen target and a native completion decision,
and that every candidate it reports, including withheld items, is accounted
for. An output bound to another target, or one without a completion decision,
does not count as coverage; name it so Review can rerun that finder.

## Candidate Dispositions

Keep each source's original finding boundary unless grouping is allowed below.
Assign every candidate exactly one disposition:

- `confirmed`: the cited code bears out the claim (for a defect, the
  triggering input or state and the wrong result), and the source meets its
  native contract for an actionable issue. Preserve the native severity or
  classification; the judge does not invent a normalized one.
- `corroborates`: the candidate independently supports an already confirmed
  finding under every grouping key. It stays visible with its source and labels.
- `needs-evidence`: the cited code supports the claim's mechanism, but one or
  more of the trigger, impact, requirement, behavior, root cause, or
  remediation remains unproven. Name the missing evidence.
- `not-actionable`: the candidate requires no repair for this target: the
  frozen code contradicts it (quote the contradicting line in the reason), the
  code does not support it at all, or it is source-native optional/advisory
  content that the source itself does not classify as blocking.

A source-native clean result is recorded in coverage without manufacturing a
candidate finding.

## Deduplication

Group candidates only when they have:

- the same frozen target;
- the same governing requirement;
- the same triggering scenario;
- substantially the same observed behavior;
- substantially the same root cause; and
- substantially the same remediation direction.

If any key differs or is absent, retain separate findings. Similar file paths,
symptoms, severity words, or remediation verbs are not sufficient.

Specification compliance and engineering judgments are separate even when all
other keys appear related. Do not collapse a missing/extra/unverifiable product
requirement into a correctness, code-quality, architecture, test, security, or
integration judgment. Cross-reference them as related while preserving both.
In a group, designate one candidate `confirmed` and any true duplicates
`corroborates`; never discard the latter.

## Coverage Accounting

Full coverage requires a completed correctness output (`findings` or `no
findings`) and a completed maintainability output (`findings` or `no
findings`). `blocked`, `context insufficient`, `stale` or a missing output is
incomplete coverage, even when it contains confirmed findings; preserve those
findings and name the missing surface. A withheld candidate alone does not make
coverage incomplete.

When requirement sources were supplied, specification is assessed only if the
correctness output reports `compliant` or `findings` under the specification
contract. For standalone review with missing or ambiguous authority, record
`Specification not assessed` and select at least `advisory`. For Dev-managed or
explicitly spec-required review it is `coverage-blocked`.

Account for every required claim as `pass`, `fail`, `blocked` or `unverified`
with its evidence. An observation the agent cannot obtain in its environment is
`unverified` and advisory; other missing required evidence blocks.

## Common Action

Select exactly one action using this precedence:

1. `coverage-blocked` when required finder, specification or claim coverage is
   incomplete, or a gate-relevant severity clarification is unresolved.
2. `repair-required` when a confirmed defect crosses the selected threshold
   (standard P0/P1; strict P0/P1/P2), or a confirmed mandatory acceptance or CI
   failure requires repair through its owner. A requirement the caller marks
   deferred, with the authority it cites, stays a finding but does not force
   repair; independent CI, safety and permission gates remain.
3. `advisory` when no repair is required but a non-blocking finding,
   `needs-evidence` item, deferred requirement, unverified observation, or
   `Specification not assessed` must be surfaced.
4. `none` only when coverage is complete and no actionable, advisory or
   evidence-gap item remains.

Return the dispositions with reasons, groups, claim outcomes, clarification
requests and the proposed common action. Reference finding IDs; do not rewrite
source text. `$review` owns the final base/head check and any posting.
