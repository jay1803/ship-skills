---
name: review-judge
description: >-
  Validate and combine isolated review artifacts for one frozen target after the reviewers finish.
metadata:
  owner: jay1803
  family: review
  maturity: stable
  distribution: review
---

# Review: Finding Judge

Validate and combine Review v2 source artifacts. Judge only supplied evidence;
do not inspect the repository to create findings or replace a specialist's
semantic judgment.

Read the [Judge Contract](references/judge-contract.md), the shared
[severity policy](../review/references/severity-policy.md), and
[assembly contract](../review/references/assembly-contract.md) before judging.

## Inputs

Require one frozen target envelope, its coverage signals and requirements, and
the complete set of source artifacts collected for the generation. Stop when
the target envelope itself is incomplete or inconsistent.

## Workflow

1. Verify each artifact's envelope, exact target binding, raw Markdown byte
   length and SHA-256, and source provenance. Quarantine failures verbatim.
2. Preserve every verified artifact's raw Markdown, native labels, and
   provenance exactly. Assign each candidate one allowed disposition.
3. Group only findings that satisfy every deduplication key in the Judge
   Contract. Never collapse specification and engineering judgments.
4. Account for required core and signaled conditional coverage using the shared artifact contract's
   successful native-decision allowlist.
   Envelope-valid but unsuccessful results remain history and make required
   coverage `coverage-blocked`; then select exactly one common action.
5. Return a compact proposed decision to `$review` for deterministic assembly. Do not modify files,
   invoke reviewers or providers, route repairs, or post to GitHub.

## Output

Return the decision JSON defined in the assembly contract: exact target,
source/candidate dispositions and group IDs, mandatory-claim outcomes,
clarification requests, and proposed common action. Reference source IDs and
byte ranges; do not reproduce raw Markdown. The controller assembles it with
all immutable source bytes and validates completeness before acceptance.

This is a proposed judgment, not a current-head verdict. Only `$review` may
accept it after the final target check. If input validation fails, identify the
source and reason; Review retains its original bytes in quarantine.
