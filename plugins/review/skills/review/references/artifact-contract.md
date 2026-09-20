# Review Artifact Contract

Use when constructing or validating Review v2 source and target envelopes.
This file owns the shared data fields and successful coverage decisions.

The target envelope is:

```text
Contract Version: 2
Review Run ID: stable identifier for the logical review/repair lifecycle
Generation: positive integer; starts at 1
Invocation: dev-managed | standalone
Target Type: pull-request | immutable-diff
Repository: canonical repository identity/path
PR: canonical URL/number or none
Base Revision: immutable full commit SHA
Head Revision: immutable full commit SHA
Review Mode: fast | standard | strict | explicit standalone
Review Lens: thermo-nuclear
Started At: timestamp
```

New envelopes preserve `strict` and normalize omitted/legacy `default` lens
to `thermo-nuclear` before dispatch. Record the resolved severity policy;
standard blocks P0/P1 and strict blocks P0/P1/P2. In the JSON transport,
standalone resolves to `mode: standard` unless explicitly selected otherwise;
`invocation: standalone` carries its independent invocation identity. Historical envelopes and
raw source bytes stay unchanged; retain their original labels for provenance.
Do not claim an older default-lens artifact proves the newly required rubric.
For a continuing Dev gate, obtain a fresh generation when that evidence is absent.

## Dispatch Evidence Ownership

Before each isolated lens starts, attach a small packet to its frozen target:

- applicable instructions with exact source, precedence, later overrides,
  superseded requirements, selected mode/base, and explicit no-fix boundaries;
- required claim IDs with unchanged wording, evidence fidelity, current gate
  effect, exception authority, and the source/controller responsible for proof;
- required sources/surfaces and which are readable in the selected runtime;
- controller-provided snapshots with source locator, observation time and exact
  revision binding (including authority and CI when relevant);
- live checks owned by the controller, including final PR base/head checks;
- unavailable capabilities and their specific effect on the assigned surface.

Freeze this inventory before core dispatch; extend evidence ownership when the
one-shot conditional signals are selected. Do not first assign required proof
to a specialist at judgment time.

The packet contains source evidence, never implementation rationale, prior
findings, sibling outputs, credentials, or permission to post. Check capability
before assigning live GitHub/tracker/test work to a runtime that cannot do it.
A readable code lens need not rerun controller-owned CI or local loopback tests
merely to finish inspection. Missing required runtime proof remains a claim gap;
missing essential authority or unreadable code remains incomplete coverage.

If a source is missing after dispatch, supplement the same isolated lens with
that source on the unchanged target when its context and independence remain
valid. Retain the original output and additive completion with provenance;
index the completed source without overwriting the earlier bytes. If the lens
cannot be resumed, retry only that failed lens with a complete packet. Target
changes require fresh target-bound review under the lifecycle contract.

## Source Artifact Contract

Each reviewer returns one immutable source artifact. `$review` preserves it as
received and passes it to `$review-judge`; it must not paraphrase findings into
a lossy intermediate form.

```text
Artifact Contract Version: 2
Review Run ID: copied from target envelope
Generation: copied from target envelope
Source Artifact ID: stable unique identifier
Source Kind: core | conditional
Source Name: review-spec | review-correctness | review-code-quality |
             architecture | test | security | integration
Native Decision: source-native status or label
Provenance: skill/runtime receipt
Target Type: copied from target envelope
Repository: copied from target envelope
PR: copied from target envelope
Base Revision: copied from target envelope
Head Revision: copied from target envelope
Raw Markdown SHA-256: lowercase SHA-256 of the exact UTF-8 Raw Markdown bytes
Raw Markdown Length: exact UTF-8 byte count
Raw Markdown: exact source output, preserved verbatim
```

Native labels, heading structure, finding identifiers, severity or
classification labels, formatting, and runtime provenance are data. They must
remain verbatim in `Raw Markdown`; the orchestrator and judge may reference
them but must not normalize or rewrite them. Transport escaping is allowed
only when it can be deterministically reversed before hashing and judgment.

Before judgment, `$review-judge` verifies the artifact contract version,
required fields, run ID, generation, complete target identity, byte length,
SHA-256, and source provenance. A source is `verified` only when all checks
pass. A malformed artifact, mismatched target, hash mismatch, missing raw
Markdown, missing provenance, or result that cannot be bound to the frozen
target is quarantined. Quarantined content is retained verbatim for audit but
cannot support, corroborate, dismiss, or become an actionable finding.

Envelope verification and successful coverage are separate checks. A verified
artifact satisfies coverage only with one of these source-native completion
decisions:

- `review-spec`: `compliant` or `findings`;
- `review-correctness`: `findings` or `no findings`;
- `review-code-quality`: `findings` or `no findings`;
- a signaled conditional reviewer: a completed `findings` or `no findings`.

The standalone missing/ambiguous specification-authority case is the sole core
exception: record `Specification not assessed` and return at least advisory, never unqualified approval. An envelope-valid `blocked`, `context insufficient`, `pending`, `stale`,
`skipped` or `unverified` result remains evidence history
but is unsuccessful coverage. When that source is required, the judge selects
`coverage-blocked`; neither envelope validity nor retained history converts it
to successful coverage.


## Transport And Assembly

Use [assembly-contract.md](assembly-contract.md) when serializing source
envelopes. Preserve raw UTF-8 bytes in files; do not ask a model to regenerate
them. The manifest binds candidates to source-native IDs or exact byte ranges;
mechanical indexing cannot change native severity or invent a finding.

## Coverage Granularity

A withheld candidate is not an incomplete review surface. Preserve confirmed
findings when another candidate lacks proof. Use `findings` or `no findings`
when the assigned surface was inspected and only individual hypotheses were
withheld. Record each withheld item's missing evidence without making it a
finding or a required coverage gap.

Use `context insufficient` only when missing evidence prevents inspection of a
required part of the assigned surface. Retain any confirmed findings alongside
the named coverage gap; the judge preserves them, but required incomplete
coverage still takes precedence over repair or approval.
