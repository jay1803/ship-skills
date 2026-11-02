# Executable Issue Routing

Use Python 3.11+ and the installed Skill's absolute
`scripts/route_issue.py --input FILE` path, or pipe JSON to stdin. The script
reads [issue policy](issue-policy.md) and the canonical acceptance policy;
the caller does not read or repeat those classifications.

```json
{
  "request": "Research this SDK's resumable upload contract; stop at findings",
  "target": {"kind": "issue", "ids": ["ENG-123"]},
  "evidence": [{"source": "Linear ENG-123", "content": "The bound issue asks for external API feasibility research only.", "revision": "observed updatedAt"}],
  "issue_state": "In Progress",
  "authority": {"delivery": false, "release": false, "direct": false, "mutation_budget": "none"}
}
```

`target.kind`: `none`, `issue`, `parent`, `project`, `issue-set`, `artifact`,
`pr`, or `environment`. Bound targets need nonempty IDs and current evidence.
Copy the actual request/accepted continuation, canonical description, readiness
record and relevant current PR/CI/Review facts; do not preclassify route, shape
or mode. One bound target read is normally enough. Do not search other issues
or entire repositories to fill gaps. Include the complete included coding
inventory for a project; explicit deferred human acceptance remains outside it.
For an issue, copy its current label names to `labels` when review applicability
matters; only the exact `REVIEW:PRODUCT` label on that issue can settle its
Product Solution Review gate. Include the parent link, accepted engineering plan
and acceptance mapping when claiming an engineering-task child. A child link or
technical title alone does not establish that role or readiness.
For an explicit request to materialize a supplied, accepted engineering task
plan, bind the owning issue ID as the proposed `parent` target and include that
request, plan basis and actual child/readiness inventory. This is target binding,
not a caller-selected delivery shape. Keep an ordinary single-issue request as
`issue`; do not fabricate a parent intent to force a project route.

`authority` is the caller's already-established authorization, never a Jev
prediction: `delivery`, `release`, and `direct` are booleans. A release flag
must incorporate repository policy; a user's delivery request cannot waive
human-only merge/release rules. Read-only investigation and verification need
no delivery flag. Optional `mutation_budget` preserves an explicitly authorized
`scratch-only`, `retained-diagnostic-artifact`, `explicit-verification-actions`
or Direct `workspace-write` scope. Supply its exact path/target and stop condition
in `authority.scope`; a route never grants these writes.

Provide `resume_anchor` (exact existing controller/branch/PR/head) and optionally
`resume_owner` for resume/post-PR work. Fresh verification requires `frozen_target`
with its immutable revision or live acceptance contract; use `verification_owner`
only for an already-bound verification-contract owner. Carry `transition_history`
when a new authorized endpoint supersedes an earlier one. Optional
`delivery_evidence` carries verbatim outcome/acceptance facts, not a caller's
shape decision.

For an existing PM handoff, optionally supply `pm_handoff` from the actual
record, not a prediction:

```json
{
  "canonical_source": "issue:ENG-123",
  "canonical_revision": "contract-r7",
  "handoff_source": "comment:handoff-42",
  "handoff_revision": "handoff-r2",
  "assessed_canonical_revision": "contract-r7",
  "decision": "ready"
}
```

Both `(source, revision)` pairs must appear in `evidence`; include the current
canonical and relevant decision/dependency facts once. Without a matching ready
record the program downgrades a proposed reuse to `assess-readiness`. This checks
bindings only: the PM owner still verifies semantic freshness and authorization.
Do not fetch an entire comment history solely to fill this optional field.

Successful stdout contains the canonical `issue_route` and `routing_evidence`.
`live_state.issue_role` distinguishes a product outcome from an accepted
engineering task when the bound evidence supports it. It does not grant a task
write, technical approval or product decision.
Use `issue_route.selected.next_owner`, terminal intent, authority and completion
contract directly. For `pm/*`, the additive `pm_action` field contains `action`
(`clarify`, `write-spec`, `assess-readiness`, `reuse-handoff`, `blocked`), a bounded
`next_owner`, `gap`, `required_input` and zero-based `evidence_refs` into the
receipt's top-level evidence list. It leaves the lifecycle owner as `$pm`;
`blocked` stops dependent PM work even when workflow routing itself succeeded.
Do not repeat classification or treat this field as product/readiness approval.
Return blocked routes without starting another workflow.
Reuse a still-current receipt. Inside PM, the verified local transitions in
[working context](../../pm/references/working-context.md) need no new paid call;
keep their progress separate from the immutable route. Otherwise on material
input change refresh the affected
facts and invoke the command again, rather than reclassifying in the main model.

The network operations are the [Jev-first decision cascade](decision-cascade.md)
over the supplied evidence and policy; low-confidence questions can additionally
use Luna Decisions through OpenRouter. No tracker or repository mutation occurs. Jev credentials
are read from `TYPESAFE_API_KEY`, `JEV_API_KEY`, or `JEV_ENV_FILE` (default
`~/.config/jev/.env.local`); the file is parsed, never sourced or printed.
The command pins `jev-1.13.0`, validates typed choices and reports input/policy
hashes, probabilities, usage and elapsed time, with original provider receipts and
final decision sources kept separately. It does not retry POSTs.
Exit 0 means routed; exit 2 means a blocking input, policy, binding or service
boundary. Report the reason and repair that boundary; do not silently return to
main-model routing or ask Jev to grant missing authority.
The separate `needs-main-model` state (also exit 2) carries only unresolved
low-confidence disagreements. Complete its bound resolution and resume the same
input with `--decision-resolution`; accepted choices are not reopened.
