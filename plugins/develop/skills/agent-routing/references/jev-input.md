# Executable Agent Routing

This is the caller's input contract, not a classification policy. Python 3.11+
is required. Invoke the package-local `scripts/route_agent.py --input FILE`
(or pipe JSON to stdin). Product's PM copy is generated from Develop and runs
without a Develop installation. Use an absolute script path after resolving
the installed Skill directory; do not assume the repository cwd is that directory.

Supply observed task/runtime facts. Do not preselect tier, effort or model unless
the user or an existing binding explicitly fixes it. The command loads the
canonical policies itself, queries Jev once, enforces floors and emits a packet.
The executing model accepts that packet without reading or redoing the policies.

```json
{
  "request": "Find the handler for this known route and report its path",
  "lifecycle": "bounded",
  "evidence": [{"source": "caller", "content": "One known symbol lookup; no writes."}],
  "permissions": "inherit",
  "write_scope": "task",
  "requirements": ["repo-read"],
  "profile_fallback": "allowed",
  "executor_policy": {"mode": "required", "executor": "codex", "fallback": "forbidden", "independent_from": "none"},
  "runtime": {
    "codex": {
      "models": ["gpt-5.6-luna", "gpt-5.6-terra", "gpt-5.6-sol", "gpt-6-astra"],
      "reasoning_levels": ["low", "medium", "high", "xhigh"],
      "requirements": ["repo-read"],
      "model_selection": "explicit",
      "profile_selection": true,
      "profiles": {"explorer": "available", "worker": "not_attempted"}
    }
  },
  "validation": "Return the actual path and symbol",
  "stop_conditions": "Return after lookup"
}
```

The example's inventory is illustrative, not evidence of availability. Populate
it from the current tool schema, configured executor and actual acceptance or
failure evidence. `model_selection` describes what the tool permits:
`explicit`, `application-default`, or `inherited`. Optional `observed_model`
records runtime evidence; absent effective values remain unknown. Missing
profile entries are `not_attempted`; a failure for one role says nothing about
another. A profile failure never removes a model from the inventory.

Optional fields:

- `permissions`: defaults to `inherit` (all available parent permissions). Use
  `read-only`, `workspace-write`, or `external-write` only to carry an explicit
  user restriction or an enforced runtime limit, never merely a role default.
- `write_scope`: defaults to `task`; concrete targets can be discovered during
  execution. Carry an explicit user scope unchanged. A missing per-phase
  allowlist or separate approval is not a routing blocker.

- `required_role`, `required_model`, `required_profile`, `exact_binding_required`:
  carry explicit constraints; do not turn preferences into requirements.
- `performance_preference`: `cost` or `latency`; otherwise Jev applies policy.
- `producing_capability_tier`: the semantic tier of the producing decisions for
  judgment review, not the producer's incidental runtime model. Omission on a
  judgment review blocks rather than guessing a weaker floor.
- `executor_policy.independent_from`: `{ "id": "execution-id", "executor":
  "codex" }` when cross-executor independence is required.
- `availability_fallback.allowed_models`: exact permitted replacements; omitted
  means no substitution. Never populate this from a model's recommendation.
- `previous_route`, `adjustment_budget`, `role_change_authorized`: carry the
  previous envelope/counters and existing role-change authority on escalation.
  Do not reset counters by creating another task. Ordinary resume with no new
  decision reuses its existing packet instead of making another request.
- `allowed_writes`, `forbidden_writes`: carry explicit user restrictions when
  present; omission adds no restriction. Task ownership is coordination, not a
  separate permission grant.

Only pass the minimum task-relevant evidence. Do not include credentials or raw
session exports. The API key stays local: `TYPESAFE_API_KEY`, then `JEV_API_KEY`,
then those variables in `JEV_ENV_FILE` (default `~/.config/jev/.env.local`). The
dotenv reader parses assignments; it never executes the file. Requests go only
to `https://api.typesafe.ai/v1/systemone` using pinned `jev-1.13.0`.

Exit 0 / `status: routed` means a proposed executable packet, not a spawned or
accepted agent. Exit 2 / `status: blocked` reports the failed boundary. Missing
credentials, unavailable binding, invalid response or transport failure never
silently falls back to main-model classification. Obtain missing facts or repair
the named boundary and explicitly rerun; the command does not retry POSTs.
No confidence threshold is invented: Jev makes typed decisions, while code
enforces policy constraints. Confidence is retained for evaluation, not treated
as correctness or permission. Low-confidence ambiguity can select blocked.

The packet includes `routing_envelope`, `runtime_binding`, role instructions,
the task and concise dispatch instructions. Preserve it through dispatch and
record the actual runtime receipt separately. A fresh packet is required when
request, evidence, authority, policy or runtime inventory materially changes;
the input/policy digests identify the evaluated snapshot. Do not use a digest
as proof that a live PR or permission has not changed.

For persistent-session creation, callback transport or dispatch recovery, load
only the relevant execution section of the selected adapter. Those mechanics
remain runtime-specific; do not read its model-selection tables or reclassify.

API contract: [TypeSafe API](https://docs.typesafe.ai/api),
[models](https://docs.typesafe.ai/models), and
[confidence](https://docs.typesafe.ai/confidence).
