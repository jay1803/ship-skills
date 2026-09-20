# Deterministic Review Assembly

Use with Review v2; transport `assembly_version: 1` does not reinterpret old
Markdown artifacts. Existing immutable evidence stays unchanged. For a new
run, the controller supplies source-native outputs as UTF-8 files and a JSON
manifest. Build source envelope target fields from that one captured target
object rather than retyping them. Source IDs, native names/decisions, provenance
and candidate spans still come from the actual reviewer receipt/output; this
construction does not permit changing a conflicting native declaration.

Before dispatching Judge, the controller runs the same helper read-only:

```sh
python3 <review-skill>/scripts/assemble_review.py --preflight manifest.json
```

It prints JSON and writes no artifact: exit 0 means declared source transport
and coverage are ready for semantic review; exit 1 means blocked, with the
invalid source/reason, missing coverage or manifest error. It needs no invented
Judge decision. Preflight and final assembly share input validation. Repair
only the affected transport/index from preserved originals, or obtain an
additive correction from the originating reviewer when its native receipt is
wrong. Keep valid lenses and the original failed inputs. Rerun preflight after
material input changes; final assembly checks the inputs again.

A preflight pass is not approval: it cannot detect an omitted native candidate,
a lying completion label, a mismatched identity inside arbitrary prose, or a
misquoted/untrusted authorization. Compare the full native output and actual
authority sources before judgment, including withheld items and literal quotes.
Unresolved semantic questions stay with Review/Judge and originating sources.
No dummy dispositions, accepted head, repair attempt or posting follows from
this transport check alone.

After semantic review, the judge returns compact JSON. The controller runs:

```sh
python3 <review-skill>/scripts/assemble_review.py manifest.json judgment.json combined.json
```

The output must be a new scratch artifact outside the reviewed repository. The
helper reads inputs and writes only that output; it neither fetches nor posts.
Invalid judgment/manifest binding rejects assembly. Quarantined sources are
retained losslessly and force coverage-blocked; failed assembly inputs remain
in their original files for audit. Never publish a partial artifact.

## Manifest

The JSON transport uses these keys (SHA fields are full lowercase digests):

```json
{
  "assembly_version": 1,
  "target": {
    "contract_version": 2,
    "run_id": "logical-review-id",
    "generation": 1,
    "invocation": "dev-managed",
    "target_type": "pull-request",
    "repository": "canonical repository identity",
    "pr": "exact PR URL",
    "base": "full 40-character commit SHA",
    "head": "full 40-character commit SHA",
    "mode": "standard",
    "lens": "thermo-nuclear",
    "started_at": "ISO timestamp"
  },
  "conditional_signals": {"test": "concrete changed test boundary"},
  "required_claims": {"acceptance-1": "required real-database reopen proof"},
  "sources": []
}
```

Each source object contains `contract_version: 2`, `id`, `name`, `kind`
(`core` or `conditional`), the exact complete `target`, source-authored
`native_decision`, nonempty `provenance`, `raw_path` relative to the manifest
(or absolute), `raw_length` in bytes, `raw_sha256`, and `candidates`.
Optional source `clarifications` hold additive originating-source replies:
`candidate_id`, exact `target`, `provenance`, `raw_path`, `raw_length`,
`raw_sha256`, and source-authored `priority`. Keep the original candidate label
and raw file unchanged. The helper verifies and embeds each reply separately;
its level resolves that candidate's gate while the original label stays visible.
One accepted reply per candidate is supplied for this assembly; preserve earlier
replies as immutable history if clarification itself is revised. Review/Judge
must verify originating-source identity and any changed-level explanation;
a nonempty provenance string alone does not authenticate identity.

The three core sources are required; each conditional signal requires its named
source. Unsignaled sources and duplicate identities are rejected.

Index every source-native candidate, including withheld and optional items:
`id`, `start` (inclusive UTF-8 byte offset), `end` (exclusive), `category`
(`defect`, `optional`, or `requirement`), and `priority` (`P0`–`P3` or null).
A `requirement` preserves source-native compliance classification. A P2/P3
candidate follows the mode threshold by default even in this category. Supply
`mandatory_authority` only with the verified source of an explicit requirement
exception or independent obligation; a heading alone is insufficient. Optional
`claim_id` binds a requirement candidate to one unchanged `required_claims` entry.
Use the source's candidate boundaries/labels; mechanical indexing must not
invent levels or findings. The complete original Markdown remains in the file;
the judge checks that the candidate index is complete and faithful. A byte/hash
check alone cannot detect an omitted candidate or prove a priority justified.

`required_claims` inventories any mandatory acceptance/CI/evidence claims
supplied to this review. Freeze their original wording, including identity and
evidence fidelity. Do not omit or weaken a required claim to obtain a passing gate.
This does not replace Dev verification or authorize a reviewer to run CI.

An explicit caller override may supply `blocking_levels` and `policy_authority`;
verify the real user authorization before constructing that override. Otherwise
standard/fast-selected review uses P0/P1 and strict uses P0/P1/P2.
For standalone missing specification authority only, set
`specification_not_assessed: true`, a nonempty `specification_reason`, and retain
a verified spec source with native decision `Specification not assessed`.
This produces at least advisory. Dev-managed missing authority is blocked.

## Judge Decision

```json
{
  "assembly_version": 1,
  "target": {},
  "dispositions": [
    {"source_id": "source-1", "candidate_id": "finding-1",
     "disposition": "confirmed", "group_id": "group-1",
     "reason": "evidence-based disposition without copying the source"}
  ],
  "required_claims": {
    "acceptance-1": {"status": "blocked", "evidence": "required fidelity absent"}
  },
  "clarifications": [],
  "common_action": "coverage-blocked"
}
```

Copy the exact target object. Each verified candidate gets exactly one of
`confirmed`, `corroborates`, `needs-evidence`, or `not-actionable`. Quarantined
candidates cannot enter judgment. Each group has exactly one confirmed source;
spec and engineering candidates cannot share a group. The judge applies the
full semantic deduplication keys, preserves native levels, and accounts for
all required claims using the evidence/gate fields below. Legacy v1 `status`
(`pass`, `fail`, `blocked`) remains readable with its original blocking meaning;
new decisions use `evidence_status`. Conflicting fields reject assembly. Clarifications
contain unresolved gate-relevant source questions; a confirmed unlabeled defect
cannot silently pass. A confirmed binding requirement violation requires
repair unless covered by an authorized acceptance deferral below; missing
mandatory evidence blocks. P2/P3 classification alone never creates a mandatory
requirement.

The helper verifies bytes, declared identity bindings, coverage, candidate mapping, mode gate,
and consistency with the proposed action, then embeds original source Markdown
(or quarantined bytes as reversible base64) in the combined JSON. The judge
never needs to generate the raw source text. `$review` still checks semantic
completeness and the current PR base/head, then returns a concise user-facing
summary with the combined artifact reference and any authorized posting result.

## Claim Evidence And Authorized Exceptions

New claim outcomes contain `evidence_status` (`pass`, `fail`, `blocked`, or
`unverified`), `evidence`, and `gate_effect` (`blocking` or `non-blocking`).
Passing evidence is non-blocking; failed evidence requires repair; blocked or
unverified evidence blocks by default. `unverified` records an acknowledged
missing observation without asserting the requirement is false.

Only an explicit instruction from an authority able to defer that exact proof
may make an `unverified` claim non-blocking. The controller verifies this from
the actual instruction and applicable repository policy, then supplies a
`claim_exceptions` manifest map keyed by the unchanged claim ID. Each value is:

```json
{
  "target": {"...": "exact complete frozen target"},
  "requirement": "unchanged full required_claims value",
  "instruction_ref": "durable locator of actual authorizing instruction",
  "instruction_quote": "exact relevant instruction",
  "authorized_by": "identity and authority over this evidence requirement",
  "scope": "exact deferred proof and permitted gate effect"
}
```

The judge copies that exact object into the outcome's `exception_authority`,
retains `evidence_status: unverified`, sets `gate_effect: non-blocking`, and
names `remaining_evidence`. Assembly binds the record to the claim and target;
it cannot authenticate a quote or establish the issuer's authority. Review and
Judge must verify both from supplied source evidence before acceptance. Missing,
ambiguous, or insufficient authority leaves the claim blocking.

An exception produces at least `advisory`, never an unqualified approval. The
ordinary proof exception cannot override failed checks or confirmed violations.
Neither exception can override required review coverage, safety, permissions,
branch protection, or independently required CI. A P2/P3
label or a defect-threshold override is not exception authority. Preserve all
source bytes and original requirements; do not manufacture pass, downgrade a
confirmed violation, or rewrite historical judgments. The combined artifact
exposes normalized `claim_outcomes` and the original `claim_exceptions` as well
as the untouched judge decision. Downstream owners must report the remaining
proof and validate their own gates; Review does not grant merge authority.

### Acceptance Deferral

For an explicit later instruction deferring P2/P3 acceptance, retain the original
claim and supply `claim_kinds: {"claim-id": "acceptance"}`. Unspecified kinds
are independent obligations and cannot use this extension. In the same exact
bound authority object add `effect: "defer-acceptance"` and `priority: "P2"`
(or `P3`). The instruction must actually authorize the gate effect for that
requirement or clearly bounded class; do not infer it from a threshold alone.
New ticket P2/P3 recommendations belong outside `required_claims` in the first
place; this extension preserves an existing requirement and its supersession.

A deferred outcome retains `fail`, `blocked`, or `unverified`, supplies the exact
`exception_authority`, `gate_effect: "non-blocking"`, and `remaining_evidence`
describing the unresolved behavior/proof. Bind each corresponding requirement
candidate with `claim_id`; its source-authored priority must match the exception.
P0/P1, different claims, or independent obligations cannot use that binding.
Review/Judge verify the semantic binding and actual authority, including that
an independently binding CI/security requirement was not mislabeled acceptance.
The helper enforces declared bindings, not the truth of that declaration.

Carry the instruction's repair permission separately: a nonblocking deferral
is not permission to fix an item explicitly marked record-only. Do not suppress
its native finding or failed observation, or claim full acceptance/completion.
