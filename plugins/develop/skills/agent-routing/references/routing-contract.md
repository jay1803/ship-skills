# Agent Routing Contract

The caller decides the task semantics; `scripts/route_agent.py` applies the
floors, picks executor and model from [`models.json`](../scripts/models.json)
and resolves the profile. Lifecycle ownership, permissions and delivery mode are
separate decisions.

## Decide

- `role`: `explorer` gathers evidence; `worker` produces or implements a scoped
  artifact; `reviewer` independently judges an existing artifact; `architect`
  resolves cross-module design or contract ambiguity; `operator` applies one
  exact, already-decided, low-risk non-code operation.
- `tier`: `fast` only for explicit, mechanical, reversible work with a
  deterministic check and no new function behavior; `standard` for ordinary
  reasoning in clear boundaries; `deep` for cross-boundary work, conflicting
  evidence or high failure cost; `critical` for the hardest or irreversible
  decisions.
- `effort`: `medium` for retrieval, mechanical or text/style edits; `high` for
  local function logic, lifecycle control and substantive review; `xhigh` for
  coupled cross-file changes in a settled design; `max` for architecture,
  contract or state-flow decisions and hard diagnosis. File count sets neither.
- `decision_state`: `unresolved` while substantial design judgment, conflicting
  evidence or difficult diagnosis remains, else `settled`. A missing product
  decision goes to its owner, not to a stronger model.
- `risk`: `excluded` for auth, security, privacy, payments, deletion,
  schema/migration, public contracts, concurrency, signing, production
  configuration or release; `unknown` if you cannot tell; else `ordinary`.
- `judgment_review`: `yes` when the primary job is independent judgment of an
  existing artifact; pass the producing decisions' tier as
  `producing_capability_tier`. Self-checks and first-time design are `no`.

## Input

```json
{
  "request": "<task and expected artifact>",
  "lifecycle": "bounded | controller",
  "decisions": {"role": "worker", "tier": "standard", "effort": "high",
                "decision_state": "settled", "risk": "ordinary",
                "judgment_review": "no", "reason": "<task evidence>"},
  "requirements": ["repo-read", "code-write"],
  "runtime": {"codex": {"models": ["gpt-6.1-sol"], "reasoning_levels": ["medium", "high"],
                        "requirements": ["repo-read", "code-write"],
                        "model_selection": "explicit | application-default | inherited",
                        "profile_selection": true, "profiles": {"worker": "available"}}}
}
```

A `controller` owns a persistent lifecycle; a `bounded` agent returns one
artifact. Fill `runtime` from the current tool schema and observed acceptance;
unattempted profiles are `not_attempted` and `observed_model` records a known
default. Optional fields carry existing facts only: `evidence`, `validation`,
`stop_conditions`; `permissions` and `write_scope` (default `inherit`/`task`);
`profile_fallback` (default `allowed`; `forbidden` keeps the named profile);
`executor_policy` (default `auto`, `any`, fallback `allowed`; `independent_from:
{id, executor}`); `required_role`, `required_model`, `required_profile`,
`exact_binding_required`; `availability_fallback.allowed_models`;
`previous_route` and `role_change_authorized`. Never include credentials.

## Helper Rules

| Condition | Result |
| --- | --- |
| `risk: excluded` / `unknown` | tier at least `deep` / `standard` |
| `controller` lifecycle | at least `standard` and `high` |
| Judgment review | at least the producing tier; a missing tier blocks |
| `unresolved` or `critical` | at least `deep` and `max` |
| `reviewer`, `architect` or `deep` | at least `high` effort |
| `fast` with `xhigh` or `max` | `standard` tier |
| `previous_route` | same lifecycle, permissions and write scope; no lower tier or effort; a role change needs `role_change_authorized` |

A `required` executor is the only candidate; otherwise the named executor goes
first and others follow only with fallback `allowed`. `independent_from`
excludes its executor. Unresolved work takes the table's `unresolved` model,
other work its tier model; explicit and observed models must sit within
`ceilings`. An unavailable model moves only forward along `fallback_order` to a
model in `allowed_models`. A runtime without explicit selection cannot honor a
required model. A named profile falls back to the default only when allowed.

## Dispatch And Escalation

Carry the task, sources, restrictions and, without a profile selector, the role
instructions. Record requested and accepted executor, model, effort, profile and
each fallback separately. If a required controller route cannot be dispatched,
control stays with the current owner.

An agent that outgrows its route returns `status: escalation_required` with the
reason, evidence and recommended decisions. Its owner verifies the evidence and
reruns with `previous_route`; `adjustment` reports a capability escalation or an
effort adjustment. Missing credentials, infrastructure or an ambiguous external
write need diagnosis, not a stronger model.
