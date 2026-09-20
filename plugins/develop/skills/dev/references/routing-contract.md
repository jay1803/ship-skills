# Agent Routing Contract

Classify every delegated task before creating an agent or user-owned worker
thread. Keep lifecycle ownership, semantic responsibility, model capability,
reasoning depth, runtime requirements, permissions, write scope, and executor
policy as separate decisions.

## Routing Envelope

For an older handoff that omits performance preference, use `cost` and record
the selection evidence at dispatch. Do not infer `latency` from a delivery-mode
label or reclassify a running agent merely to populate the new receipt fields.

```yaml
semantic_route: controller/standard | controller/deep | controller/critical | <bounded-role>/<capability-tier>
lifecycle: controller | bounded
role: explorer | worker | reviewer | architect | operator
capability_tier: fast | standard | deep | critical
reasoning_depth: low | medium | high | xhigh
performance_preference: cost | latency # default: cost; never relax capability gates
selection_reason: <scope, uncertainty, validation, and any latency evidence>
availability_fallback:
  allowed_models: [] # exact executor model IDs/aliases; empty or omitted forbids substitution
adjustment_budget:
  max_effort_adjustments: 1
  max_capability_escalations: 1
  effort_adjustments_used: 0
  capability_escalations_used: 0
requirements:
  - repo-read | code-write | browser | tracker-read | tracker-write | network
permissions: inherit | read-only | workspace-write | external-write # default: inherit
write_scope: task | none | <explicit user scope> # default: task
profile_fallback: allowed | forbidden
executor_policy:
  mode: auto | prefer | required
  executor: any | codex | claude-code
  fallback: allowed | forbidden
  independent_from: none | <execution id whose executor must differ>
```

`semantic_route` is a compact receipt label, not a replacement for the explicit
fields. A controller route combines lifecycle and capability tier, such as
`controller/standard`; a bounded route combines role and capability tier, such as
`worker/fast`. The role still records what a controller is responsible for.

### Lifecycle

- `controller`: owns a persistent PM/Dev lifecycle, state transitions, retries,
  user communication, and final completion. The invoking top-level PM/Dev
  orchestrator and every fresh user-owned issue worker are controllers, but they
  do not necessarily need the same capability tier.
- `bounded`: produces one scoped artifact or performs one explicitly authorized
  operation, then returns control. It does not advance the parent workflow.

A bounded agent is not a replacement for a user-visible controller thread.
Lifecycle ownership imposes the controller capability and reasoning floors
below; it does not grant permission or write scope, or select an executor.

### Roles

- `explorer`: locate code, trace dependencies, inspect documents, and gather
  evidence. The assignment defines the output, not a reduced permission profile.
- `worker`: produce an already-scoped artifact or implement and validate an
  approved change. Keep mutations serial when agents share a branch, worktree,
  tracker item, canonical document, or generated output.
- `reviewer`: independently challenge an artifact, diff, plan, or decision. Do
  not edit the reviewed artifact unless the parent explicitly starts a later fix
  phase.
- `architect`: resolve ambiguity across modules or contracts, identify
  tradeoffs and failure modes, and return a concrete direction.
- `operator`: apply one already-decided, exact, low-risk operation. Do not infer
  scope, compose substantive content, touch code, or choose the next state.

Role names describe responsibility, not model strength. The same role can use
different capability tiers and reasoning depths. `worker` and `reviewer` can run
on Codex or Claude Code; never infer an executor from the role name.

## Two-Stage Capability And Reasoning Selection

Select capability tier first, then reasoning depth. Do not infer either value
from issue size, changed-line count, story points, title, a `Fast` label, or the
Dev delivery mode.

### Stage 1: Select Capability Tier

Choose the lowest tier that satisfies ambiguity, judgment, blast radius,
failure cost, and validation quality:

| Tier | Selection boundary |
| --- | --- |
| `fast` | All fast-tier gate conditions below pass; the task is explicit, mechanical, local, reversible, and deterministically verifiable |
| `standard` | Normal repository or domain reasoning is required, but ownership, product intent, and risk boundaries are clear |
| `deep` | Cross-boundary work, conflicting evidence, substantial product/architecture judgment, or high failure cost requires stronger capability |
| `critical` | The hardest unresolved reasoning, an irreversible migration, major release, or critical security/contract decision requires the highest default capability |

Use these provider-neutral controller routes:

| Route | Use for |
| --- | --- |
| `controller/standard` | An ordinary issue or project controller with clear scope and normal repository reasoning |
| `controller/deep` | An issue or project controller with cross-module, judgment-heavy, conflicting-evidence, or high-cost work |
| `controller/critical` | Genuinely critical control or the hardest unresolved project/issue decisions |

Every new orchestrator or full-lifecycle issue controller has a minimum of
`controller/standard` with `high` reasoning, even for a fully specified simple
issue. Do not dispatch `controller/fast`; reclassify a legacy request before
creating a new controller. Fast models remain available for bounded tasks.
This is a conservative user-selected quality floor, not a measured claim that
fast models cannot manage projects.

Classify top-level and fresh issue controllers from their complete scope. A
clear project with settled dependencies can use `controller/standard`; resolving
cross-module conflicts selects `controller/deep`; critical decisions select
`controller/critical`. Persistence, issue count, and barrier ownership alone do
not select critical capability or `xhigh` reasoning. Preserve all controller
responsibilities at every tier.

These selections govern new dispatches. They do not switch the model of an
already-running controller. Record its observed binding or `unknown`; report a
material mismatch without creating a replacement controller or duplicating work.

Use these bounded routes as initial candidates:

| Route | Use for |
| --- | --- |
| `explorer/fast` | Known-target lookup or repeatable narrow evidence collection |
| `explorer/standard` | Repository scan, dependency trace, or ordinary context reconstruction |
| `worker/fast` | Fast-tier-gated code, test, documentation, or configuration mutation |
| `worker/standard` | Clear scoped implementation or artifact requiring normal engineering reasoning |
| `worker/deep` | Cross-boundary implementation, substantive planning/specification, or judgment-dense work |
| `reviewer/standard` | Ordinary independent review |
| `reviewer/deep` / `architect/deep` | Architecture, security, privacy, release, product, or cross-module analysis |
| `operator/fast` | One exact, already-decided, low-risk operation; never code reasoning |

### Review Capability Floor

For a review that challenges judgment, architecture, security, privacy, or
unresolved assumptions, select at least the capability tier required by those
specific decisions in the producing task. Carry their producing semantic tier
and review scope as evidence. Do not lower the tier just because the diff is
small or acceptance criteria exist; mixed verification and judgment reviews
use the judgment floor. When that evidence is missing, reconstruct it or stop
before dispatch rather than guessing a lower tier.

The producing model's observed binding is not the floor: availability fallback
or overprovisioning does not make an ordinary artifact critical. Conversely,
an underclassified producing route does not justify an underpowered review.
Purely deterministic verification may use a lower tier appropriate to its own
scope; judging whether the tests or criteria are complete is judgment review.
Substantive reviewer effort remains at least high, and executor independence
remains a separate requirement.

### Fast-Tier Gate

Select `worker/fast` only when every condition is proven at dispatch time:

1. Acceptance criteria are complete and no product decision remains open.
2. The mutation target and reference pattern are known; no open-ended root-cause
   investigation is required.
3. The change is local, low-impact, readily reversible, and does not alter
   cross-module ownership.
4. A deterministic validation path exists, such as a focused test, build, lint,
   snapshot, or explicit structured output check.
5. The task does not involve authentication, authorization, security, privacy,
   payment, data deletion, database schema, migration, public API/protocol
   contract, concurrency, signing, production configuration, or release
   decisions.
6. The task does not require reconciling conflicting evidence, choosing a state,
   inferring an external write target, or handling a human-only gate.
7. Exact write scope, allowed and forbidden writes, and stop conditions are
   already present in the dispatch envelope.

One line, one file, a small estimate, or a `Fast` label is never substitute
evidence. If any condition is unknown, choose at least `standard`.

At initial classification, a known authentication, authorization, security,
privacy, payment, deletion, schema/migration, public API/protocol, concurrency,
signing, production-configuration, or release boundary selects at least `deep`,
and selects `critical` when the decision is irreversible or materially critical.
Do not route a known excluded high-risk domain through `standard` merely because
the diff is small. A human-only gate or unresolved external write target stops
dispatch instead of selecting a stronger model as a substitute for authority.

### Stage 2: Select Reasoning Depth

Choose reasoning independently from capability tier based on search breadth,
debugging depth, tool iteration, boundary checking, validation weakness, and
lifecycle control:

| Reasoning depth | Selection boundary |
| --- | --- |
| `low` | Exact retrieval, extraction, transformation, or an already-decided operation with little interpretation and strong validation |
| `medium` | Focused search or implementation with a known path, few tool iterations, strong deterministic validation, and no lifecycle control |
| `high` | Complete issue lifecycle, independent review, multi-step repository reasoning, non-trivial debugging, several tool iterations, or material boundary checks |
| `xhigh` | Exceptional complexity with an explicit reason that `high` is insufficient; never selected solely by lifecycle or model name |

Initial provider-neutral defaults and retained quality floors are:

- `controller/standard` and `controller/deep`: `high`;
- `controller/critical`: `high`; select `xhigh` only with the evidence above;
- `explorer/fast` and `operator/fast`: `low` for the exact tasks above;
- `explorer/standard`, `worker/fast`, and `worker/standard`: `medium` unless
  the reasoning boundary above requires `high`;
- `worker/deep`, `reviewer/standard`, `reviewer/deep`, and `architect/deep`:
  `high`.

Do not make a low-capability model with `xhigh`, or a standard-capability model
with `xhigh`, a default combination. A genuine `xhigh` need normally implies a
`critical` capability tier. An adapter may retain a higher effort default for
its executor; record requested and accepted effort separately. Model names and
lower reasoning settings do not establish lower total cost.

### Cost And Latency Preference

Use `performance_preference: cost` when omitted. Select `latency` for an
explicit speed preference or an interactive coding loop where the user is
waiting; record that reason. This preference selects only among bindings that
meet the capability, validation, modality, tool, and authority requirements.
The active adapter owns any specialized fast-coding alternative. It is not a
new capability tier or an automatic step in the escalation ladder.

Compare total usage and time to an accepted result, including handoff context,
retries, review, and repairs. Do not retire an available middle-tier default
merely because a newer flagship exists. Policy fixtures prove routing
compliance, not model quality or savings; changing defaults on performance
grounds needs representative task evidence, including missed defects and human
correction effort. Keep unmeasured comparisons explicitly unverified.

Keep delegated context focused on the task, relevant decisions, source pointers,
validation, and stop conditions. Reuse prior findings on escalation instead of
restarting discovery. Routing does not itself require an extra agent: preserve
the owning workflow's inline/delegation and independent-review rules.

### Availability Boundary

Before dispatch, the controller records exact permitted replacement model IDs
or aliases in `availability_fallback.allowed_models`. Empty or omitted means
no automatic model substitution, including older handoffs with only a generic
fallback-allowed statement. The active adapter filters this allowlist through
its stronger-only order and tool/context support; the list never authorizes a
weaker model, a different executor, or an override of an explicit binding.

This is a model-selection boundary, not a monetary guarantee. Existing explicit
spend limits still apply; enforce numeric ceilings only with reliable runtime
usage/pricing data, and stop when a required ceiling cannot be checked. Do not
infer API-dollar costs from subscription usage or a model price multiplier.
An unavailable model with no eligible permitted replacement returns a blocker.

Availability substitution preserves semantic tier and does not consume a
capability escalation. It cannot reset adjustment counters or authorize a later
upgrade. Capability escalation is a separate controller decision based on new
task evidence, still subject to the existing cost and authority limits.

### Requirements And Permissions

Requirements describe tool or environment needs, not intelligence. Keep
`browser`, `code-write`, and similar capabilities separate from capability tier
and reasoning depth.

Default to `permissions: inherit`: every role receives all permissions available
to its parent runtime for the user's task. Default `write_scope: task` describes
the assigned work, not a filesystem or tool allowlist. Narrow permissions only
when the user explicitly requires it, including their applicable repository
instructions; preserve enforced runtime limits. Do not infer restrictions from
role, model tier, task size, missing allowlists, or a workflow phase.

Carry explicit restrictions unchanged through delegation and escalation. Full
access does not change the requested outcome or permit unrelated work. Determine
concrete mutation targets from task evidence before acting; ordinary discovery
does not require a new permission grant. Controller ownership and serial writers
coordinate execution, not user approval. Continue the authorized lifecycle
through implementation, validation, PR, CI, eligible merge and cleanup without
asking again because a worker or phase changed. A genuine user restriction or
runtime denial must name its source; routing must not invent an approval gate.

`profile_fallback` authorizes only substitution from the requested named role
profile to the runtime default role. It does not authorize executor, model,
reasoning, permission, write-scope, or lifecycle changes. Keep it separate from
`executor_policy.fallback`.

## Executor Policy

- `auto`: choose any capable executor from current policy and availability.
- `prefer`: try the named executor first; use another only when `fallback` is
  `allowed`, without weakening capability tier, reasoning depth, permissions, or
  write scope.
- `required`: use the named executor or stop with a concrete blocker. Explicit
  user requests such as "use Claude" or "use Codex" are `required` unless the
  user also permits fallback.
- `independent_from`: require a different executor from the referenced
  implementation or decision execution. A new profile or session on the same
  executor does not satisfy it.

Resolve executor policy after the semantic route. Then map the same capability
tier, role, and reasoning depth through that executor's adapter. Do not put
provider model names in the shared role profiles.

Development delivery mode (`fast`, `standard`, or `strict`) is separate from
routing. Delivery mode controls lifecycle gates; capability tier and reasoning
depth control one agent's execution resources. None may silently rewrite the
others.

## Dispatch Contract

Every delegated prompt must include:

- the complete routing envelope;
- the executor policy and requested executor, profile, model, and reasoning;
- the requested profile-fallback policy;
- the exact task and expected artifact;
- source paths, issue IDs, PRs, or URLs;
- allowed and forbidden writes;
- validation expectations;
- stop conditions;
- the routing receipt shape below;
- the escalation result shape below.

Use a named role profile when available. If the runtime cannot select profiles,
include the role instructions in the prompt and still apply the runtime
adapter's model and reasoning values where the tool permits overrides. Tool
usage restrictions take precedence over a Skill recommendation. Preserve the
proposed model separately when the actual request must use an application
default; this is not a model-unavailability fallback. The active adapter owns
surface-specific field mapping and queued-to-running binding verification.

Record semantic route, lifecycle, role, requested and accepted executor,
profile, model, reasoning, profile-fallback policy, independence, fallback, and
escalation in the worker registry or handoff whenever the workflow already
maintains one.

## User-Visible Routing Notice

Do not rely on a client task card to expose the sub-agent model. Make every
dispatch observable in the parent conversation:

1. Before dispatch, publish one concise request with task, semantic route,
   lifecycle/role, requested capability tier and reasoning depth, executor
   policy, runtime model, and profile. Label it as requested, not active.
2. After the runtime accepts the agent or thread, publish one resolved notice
   with accepted executor, profile/runtime role, model, reasoning, each fallback
   field, and independence result.
3. If a requested profile, model, reasoning, or executor fails, publish that
   failure before retrying. Preserve the semantic route and identify exactly
   what changed. Never describe a failed dispatch as active.

Use this compact shape:

```text
Routing request: <task> | <semantic route> | lifecycle/role: <lifecycle>/<role> | tier/reasoning: <capability>/<reasoning> | executor policy: <mode> <requested> | proposed: <executor> <model>/<reasoning> | profile: <requested> | profile fallback: <allowed or forbidden>
Routing active: <task> | <semantic route> | executor: <accepted> | model: <accepted>/<reasoning> | profile: <accepted> | runtime role: <accepted> | executor fallback: <none or reason> | model fallback: <none or reason> | reasoning fallback: <none or reason> | profile fallback: <none or reason> | independence: <result>
```

The notice is observability only. It does not replace the routing envelope,
worker registry, callback, or runtime evidence.

## Routing Receipt

Every delegated agent or user-owned worker thread must return this receipt with
its artifact or callback:

```yaml
routing_receipt:
  requested_route: <semantic route>
  lifecycle: <controller or bounded>
  role: <explorer, worker, reviewer, architect, or operator>
  requested_capability_tier: <fast, standard, deep, or critical>
  requested_reasoning: <low, medium, high, or xhigh>
  performance_preference: <cost or latency>
  selection_reason: <task evidence and any latency preference>
  availability_fallback: <unchanged allowed_models list>
  adjustment_budget: <limits and current task-wide counters>
  executor_policy:
    mode: <auto, prefer, or required>
    executor: <any, codex, or claude-code>
    fallback: <allowed or forbidden>
    independent_from: <none or execution id>
  requested_executor: <codex, claude-code, or any>
  accepted_executor: <codex, claude-code, or unknown>
  executor_fallback: <none or exact substitution reason>
  proposed_model: <adapter recommendation; not proof of a dispatch parameter>
  requested_model: <explicit model or alias, application-default, or inherited>
  model_selection: <explicit, application-default, or inherited; include constraint if any>
  accepted_model: <accepted explicit model, inherited model, or unknown>
  model_fallback: <none or exact stronger-model substitution reason>
  accepted_reasoning: <accepted explicit level, inherited level, or unknown>
  reasoning_fallback: <none or exact substitution reason>
  requested_profile: <name or none>
  requested_profile_fallback: <allowed or forbidden>
  accepted_profile: <name, default, none, or unknown>
  runtime_role: <accepted role/profile or default>
  profile_fallback: <none or exact substitution reason>
  profile_instructions: <loaded, not-loaded, or unknown>
  independence: <not-required, satisfied, degraded, or unknown>
  escalation: <none or exact prior route and reason>
```

The controller compares the receipt with the accepted dispatch call and records
any mismatch. The child echoes only binding data supplied or exposed by the
runtime; it must not invent effective values. Keep executor, profile, runtime
role, model, reasoning, and escalation outcomes separate. Use `unknown` for any
effective value the runtime does not expose.

## Dispatch Failure Diagnosis

When a controller assignment fails before the child completes, diagnose the
failed layer before retrying or changing the route. This is especially important
when the controller and target executor run on different hosts.

1. Identify controller host, target host or executor, task or operation ID,
   routing envelope, requested binding, and observed terminal or pending state.
2. Read controller-side dispatch acceptance and target-side status separately:
   - `dispatch_rejected`: the controller or API did not accept the request;
   - `transport_unreachable`: the request could not reach the target;
   - `runtime_unavailable`: the target could not accept the requested binding;
   - `provisioning_failed`: required setup failed before work began;
   - `child_failed`: the child began work and returned a failure; or
   - `observability_gap`: evidence cannot identify a layer.
3. Report the smallest repair for the failed layer and whether it applies to the
   controller host, target host, or both.

Diagnosis inherits the task permissions. The controller may repair and retry
within that task after resolving ambiguous outcomes, without renewed user
approval. Preserve explicit user restrictions and the selected binding policy.

```text
Dispatch diagnosis: <task or operation ID> | layer: <reason code> | controller: <host> | target: <host or executor>
Evidence: <accepted dispatch result and target-side status/error>
Scope: <controller, target, or both> | retry: <safe, unsafe, or needs approval>
Recommended action: <smallest repair or next approval>
```

## Escalation Contract

An agent should finish its task when it can. `worker/fast`
must stop and return `escalation_required` when evidence reveals an unknown
dependency, wider scope, conflicting evidence, missing deterministic validation,
or any fast-tier exclusion. Other routes escalate when new evidence crosses
capability, reasoning, permissions, write scope, or role boundaries.

```yaml
status: escalation_required
reason_code: <stable short code>
reason: <what exceeded the current route>
evidence:
  - <file, symbol, command result, or external fact>
current_route: <semantic route>
recommended_route: <semantic route>
recommended_capability_tier: fast | standard | deep | critical
recommended_reasoning_depth: low | medium | high | xhigh
performance_preference: <unchanged cost or latency>
adjustment_kind: effort | capability | both
adjustment_budget: <limits and current task-wide counters>
availability_fallback: <unchanged allowed_models list>
profile_fallback: <unchanged allowed or forbidden>
required_capabilities:
  - <capability>
permissions: <unchanged permission>
write_scope: <unchanged exact scope>
recommended_executor_policy:
  mode: auto | prefer | required
  executor: any | codex | claude-code
  fallback: allowed | forbidden
```

The controller verifies new evidence before accepting an adjustment. For each
bounded task, default to one effort adjustment and one capability escalation;
carry both limits and used counters in the envelope, receipt, and handoff.
An older initial handoff defaults to 1/1 with zero used only when no previous
attempt exists. On resume, recover counters from prior evidence; unknown history
does not authorize fresh allowances. A stricter supplied limit wins.

- An effort-only change consumes the effort allowance, not the capability
  allowance. In-place changes count too and require actual runtime support and
  an accepted update receipt; never claim an unsupported live switch.
- A capability increase consumes the capability allowance. Selecting that
  tier's initial effort is part of the upgrade, not a second effort adjustment.
  Raising effort beyond that destination default consumes both allowances.
- Counters belong to the same task across models, sessions, retries, and
  availability substitutions; they never reset on a stronger model. A spent
  effort allowance does not prevent the one evidence-justified capability
  upgrade, or vice versa. Neither allowance requires using the other first.
- Select the required tier directly: fast -> standard for ordinary reasoning,
  standard -> deep for cross-module judgment, deep -> critical for the hardest
  unresolved or critical decisions. Skip intermediate tiers when evidence
  already establishes the destination.
- Do not repeat unchanged failed attempts. Once the required allowance is spent,
  return a concrete blocker to the controller. Raising the budget requires a
  new explicit controller decision within existing authority and cost limits;
  a child cannot reset it by renaming the task.

Missing credentials, unavailable infrastructure, and ambiguous external-write
outcomes need diagnosis or authority resolution, not capability escalation.
Carry the artifact, attempted checks, failure evidence, and remaining question
into an accepted stronger attempt.

An accepted escalation may change semantic route, capability tier, and model
or reasoning binding. A role change requires an explicit controller decision
within existing authority. Never silently expand permissions, write scope,
approval, profile fallback, executor fallback, or lifecycle ownership.

## Fallbacks

- Never silently downgrade capability tier, model strength, or reasoning depth.
- Never treat profile unavailability as model or executor unavailability.
- A runtime-default profile substitution is legal only when
  `profile_fallback: allowed`; otherwise stop after reporting the unavailable
  requested profile.
- `required` executor selection and `fallback: forbidden` fail closed.
- A `prefer` or `auto` executor may fall back only when policy allows it; record
  executor substitution separately from model and profile fallback.
- A stronger available model may replace an unavailable requested model only
  when listed in `availability_fallback.allowed_models` and permitted by the
  adapter, explicit binding, and cost policy. Preserve permissions, write scope,
  approval, lifecycle, and semantic tier; record the substitution. A weaker
  model requires explicit authorization outside automatic fallback.
- Do not claim independent review when `independent_from` is unresolved or
  points to the same executor. Report `degraded` and stop when independence is
  required by the parent workflow.
- If the required controller route is unavailable, keep control in the current
  user-owned thread and report the mismatch instead of creating a weaker
  controller.
- Routing never makes unsafe parallelism safe. Preserve dependency barriers and
  serialize overlapping mutations.
