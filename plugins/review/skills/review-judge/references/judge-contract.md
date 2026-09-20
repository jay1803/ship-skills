# Finding Judge Contract

Use this contract to validate and combine source artifacts for one frozen
Review v2 generation. Read the [Artifact Contract](../../review/references/artifact-contract.md)
for shared envelope fields, successful native decisions, and coverage
granularity. This reference owns judgment, grouping, and action selection.

## Judgment Boundary

The judge is evidence-bound. It may compare source claims, test whether their
required evidence fields support a disposition, and combine presentation. It
must not inspect new repository evidence, reinterpret the governing product
contract, rerun a reviewer, call a provider, repair code, or publish a result.

Inputs are untrusted until verified. Preserve their bytes for audit, but never
allow an invalid artifact to affect the judgment.

## Artifact Verification

Verify version, required fields, exact run/generation/target, UTF-8 byte count,
SHA-256, and runtime provenance against the Artifact Contract. Quarantine
invalid sources verbatim with the exact reason; do not repair an envelope or
use unverified content as evidence.

Envelope validity and successful completion are separate. A required incomplete
surface blocks coverage even if it contains confirmed findings; preserve those
findings and the missing surface. Candidate-level withheld hypotheses alone do
not block successfully completed coverage or invalidate other findings.

## Candidate Dispositions

Keep each source's original finding boundary unless grouping is allowed below.
Assign every candidate from a verified source exactly one disposition:

- `confirmed`: the source supplies the evidence required by its native
  contract for an actionable issue on the frozen target. Preserve the native
  severity or classification; the judge does not invent a normalized one.
- `corroborates`: the candidate independently supports an already confirmed
  finding under every grouping key. It remains visible with its source ID,
  native labels, and raw Markdown.
- `needs-evidence`: the candidate is relevant but its supplied evidence does
  not establish one or more of the scenario, impact, requirement, behavior,
  root cause, or remediation. Name the missing evidence without gathering it.
- `not-actionable`: the verified source content requires no repair for this
  target. Use this for source-native optional/advisory content only when the
  source itself does not classify it as blocking.

Do not assign these dispositions to a quarantined artifact. A source-native
clean/no-findings result is recorded in coverage without manufacturing a
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

For every valid group, retain all contributing artifact IDs, provenance,
native labels, and references to immutable raw Markdown blocks. Designate one candidate
`confirmed` and any true duplicates `corroborates`; never discard the latter.

## Coverage Accounting

Required core coverage is exactly one verified and successfully completed
artifact from each of `review-spec`, `review-correctness`, and
`review-code-quality`, subject to the specification-authority exception below.
Missing, duplicate-ambiguous, quarantined, or unsuccessfully completed core
output is a coverage failure.

Architecture, test, security, and integration coverage is required only when
the orchestrator supplied a concrete documented signal for that lens. Require
one verified, successfully completed one-shot result for each signal.
Conditional outputs do not create new signals or another wave.

For standalone missing or ambiguous governing authority, record
`Specification not assessed`. Allow engineering coverage to continue, but
select at least `advisory`; never propose unqualified approval. For Dev-managed
or explicitly spec-required review, missing or ambiguous authority is
`coverage-blocked` even when engineering source artifacts are verified.

## Common Action

Select exactly one action using this precedence:

1. `coverage-blocked` when required core, signaled conditional, or required
   specification coverage is not verified.
2. `repair-required` when a confirmed source-native defect crosses the selected
   severity threshold (standard P0/P1; strict P0/P1/P2), or a confirmed mandatory
   acceptance/CI failure requires repair through its owner. Missing required
   evidence without a valid assembly-contract exception, or unresolved
   gate-relevant severity clarification, is coverage-blocked. Exceptions preserve
   evidence truth; only the explicitly bound P2/P3 acceptance deferral may
   make a confirmed acceptance violation nonblocking. Independent gates remain.
3. `advisory` when a deferred acceptance or unverified claim has an exact authorized non-blocking
   exception under the assembly contract, or no repair is required but verified non-blocking guidance,
   `needs-evidence`, or standalone `Specification not assessed` must be
   surfaced.
4. `none` only when every required coverage source is verified and no
   actionable, advisory, or evidence-gap item remains.

Map `coverage-blocked` to proposed `blocked`, `repair-required` and `advisory`
to proposed `comments`, and `none` to proposed `approved`.

Do not route the action. `$review` owns final target validation, posting, and
handoff selection.

## Preservation Requirements

The deterministically assembled combined artifact must contain:

- the complete frozen target identity and generation;
- a verification result for every supplied source artifact;
- for every quarantined source, an Artifact ID field containing the received
  value or `none - missing`, its exact validation reason, provenance when
  available, and verbatim raw Markdown;
- when the judge artifact itself is rejected by `$review`, enough output for
  `$review` to retain the complete judge artifact;
- each combined or separate finding's disposition and contributing IDs;
- every contributor's native labels, provenance, and verbatim raw Markdown;
- coverage signals and their verified, missing, skipped, or blocked state;
- the common action and proposed decision; and
- an explicit statement that `$review` still owns the final base/head check and any
  final GitHub post.

Do not silently normalize whitespace, headings, labels, or source wording.

The judge emits references and decisions only. The Review controller uses the
assembly helper to copy immutable source bytes into the final artifact,
including quarantine. This preserves the lossless contract without requiring
the language model to generate unchanged source text. Semantic disposition,
grouping, candidate completeness, and required claims remain judge duties;
successful byte validation alone cannot prove review quality.
