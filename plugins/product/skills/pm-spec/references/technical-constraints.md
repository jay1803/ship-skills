# Technical Product Constraints

Read during scope/spec work when platform or provider capability,
compatibility, migration, privacy, performance or runtime fidelity could change
the product promise or acceptance boundary. This is conditional investigation,
not a mandatory PM stage or a separate receipt.

Verify current constraints from available repository, provider or platform
sources. Distinguish supported capability from assumptions. Identify only
product-level decisions engineering needs before choosing implementation:
platform/version support, observable authorization/fallback behavior, data
retention and migration promises, compatibility, rollout or performance bounds.
Do not choose architecture, code paths, test commands or invent production access.

Use [decision provenance](decision-provenance.md) for new observable rules.
Confirm material product choices before `$pm-spec` writes them. Engineer-owned
invariants and verifier mechanics can remain in supporting evidence or the Dev
plan without a new approval. If the constraint yields no material gap, continue
without an empty technical appendix or not-required tracker comment.

For a shared contract, identify its existing owner, affected producers/consumers,
and available issue/branch/PR evidence. Tell the project controller when a
changed interface or requirement invalidates an integration order; preserve
independent preparation and distinguish it from final alignment/acceptance.
Do not create dependencies or edit sibling issues from one issue worker.

When ordinary tests may pass without proving the promised runtime outcome,
use the [Production Loop Contract](../../pm/references/develop-handoff-contract.md#production-loop-contract).
State the product-known outcome, fidelity and pass boundary, and who supplies
missing evidence. Inspect feasible local runtime/seed/provider-seam options
before calling a path untestable. Replacing an external provider may be useful;
replacing the behavior under test with a success flag does not prove the path.
PM sets what must be demonstrated; engineering owns implementing the test seam.

Separate “enough product information to build” from “later outcome evidence is
executable.” Apply [unattended acceptance](acceptance-policy.md#unattended-engineering-acceptance)
before turning environment logistics into a gate. Preserve failed automated
checks, actual dependencies and policy authority. If an uncertainty genuinely
changes scope or safety, return the exact gap to the owner. A useful standalone
spike is a draft for the project controller, not a child this reference creates.

Keep essential confirmed constraints in the canonical product promise. Put
source detail, technical evidence and verifier mechanics in linked supporting
artifacts without copying them into every downstream receipt.
