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

Successful stdout contains the canonical `issue_route` and `routing_evidence`.
Use `issue_route.selected.next_owner`, terminal intent, authority and completion
contract directly. Return blocked routes without starting another workflow.
Reuse a still-current receipt; on material input change refresh the affected
facts and invoke the command again, rather than reclassifying in the main model.

The only network operation is a paid TypeSafe decision request containing the
supplied evidence and policy. No tracker or repository mutation occurs. Credentials
are read from `TYPESAFE_API_KEY`, `JEV_API_KEY`, or `JEV_ENV_FILE` (default
`~/.config/jev/.env.local`); the file is parsed, never sourced or printed.
The command pins `jev-1.13.0`, validates typed choices and reports input/policy
hashes, probabilities, usage and elapsed time. It does not retry POSTs.
Exit 0 means routed; exit 2 means a blocking input, policy, binding or service
boundary. Report the reason and repair that boundary; do not silently return to
main-model routing or ask Jev to grant missing authority.
