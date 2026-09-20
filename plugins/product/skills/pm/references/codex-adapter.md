# Codex Agent Routing Adapter

Use this adapter only after the shared routing contract resolves executor policy
to Codex. It is the canonical PM/Dev location for current Codex model names.
Resolve model capability first and reasoning effort second; do not collapse them
into one opaque profile choice.

## Stage 1: Select The Model

Map the provider-neutral capability tier after applying the contract's ambiguity,
judgment, blast-radius, failure-cost, validation-quality, and fast-tier gates:

| Capability tier | Codex model | Selection boundary |
| --- | --- | --- |
| `fast` | `gpt-5.6-luna` | Economical default when the shared fast-tier conditions pass |
| `standard` | `gpt-5.6-terra` | Normal repository or domain reasoning with clear ownership and risk boundaries |
| `deep` | `gpt-5.6-sol` | Cross-boundary, judgment-heavy, conflicting-evidence, or high-cost work |
| `critical` | `gpt-6-astra` | Hardest unresolved reasoning, critical decisions, or justified escalation beyond Sol |

`worker/fast` is the only code-capable Luna route. New controllers require
at least `controller/standard -> gpt-5.6-terra/high`; neither Luna nor Spark
may own an orchestrator or full issue lifecycle.
`operator/fast` remains limited to an exact already-decided operation and must
not infer code changes. A one-line change, one file, `Fast` label, or low estimate
does not pass the fast-tier gate by itself.

### Optional Spark Binding

Keep Terra and Sol as ordinary and complex-work defaults. Astra is not an
automatic replacement for either, and low reasoning does not make it the
cheapest option.

For a bounded `worker/fast` code task, consider `gpt-5.3-codex-spark/medium`
when `performance_preference: latency` and every shared fast-tier gate passes.
The exact files, reference pattern, textual instructions, validation, and stop
conditions must fit the runtime's available context and tools. Spark is a
text-only coding alternative; do not use it for screenshot interpretation,
image-dependent work, open-ended diagnosis, controllers, or independent review.
A `Fast` delivery label alone never selects Spark.

With cost preference or no demonstrated need for low latency, keep Luna for
fast-tier work. Do not infer that Spark is cheaper than Luna or stronger than
Terra. Spark is outside the capability/fallback ladder: record the specialized
binding and its selection reason, and diagnose unavailability before choosing
another binding. An explicit Spark request is not permission for silent model
substitution; report a mismatch if its task requirements cannot be met.

## Stage 2: Select Reasoning Effort

Choose effort from search breadth, debugging, tool iteration, boundary checks,
validation quality, and lifecycle ownership:

| Semantic route | Initial Codex binding | Notes |
| --- | --- | --- |
| `controller/standard` | `gpt-5.6-terra/high` | Ordinary clear engineering or PM issue with full lifecycle control |
| `controller/deep` | `gpt-5.6-sol/high` | Cross-module, judgment-heavy, conflicting-evidence, or high-cost issue |
| `controller/critical` | `gpt-6-astra/high` | Hardest unresolved control, irreversible migration, major release, or critical contract/security decision |
| `explorer/fast` | `gpt-5.6-luna/low` | Known-target narrow lookup or repeatable evidence gathering |
| `explorer/standard` | `gpt-5.6-terra/medium` | Repository scan, dependency trace, or ordinary context reconstruction |
| `worker/fast` | `gpt-5.6-luna/medium` | Explicit, mechanical, local, reversible, deterministically validated mutation |
| `worker/standard` | `gpt-5.6-terra/medium` | Clear scoped implementation or artifact with normal engineering reasoning |
| `worker/fast` with eligible latency preference | `gpt-5.3-codex-spark/medium` | Optional bounded text-only coding alternative; all fast-tier gates still apply |
| `worker/deep` | `gpt-5.6-sol/high` | Cross-boundary implementation, substantive plan/spec, or judgment-dense artifact |
| `reviewer/standard` | `gpt-5.6-terra/high` | Ordinary independent review; preserve the `high` floor |
| `reviewer/deep` / `architect/deep` | `gpt-5.6-sol/high` | Architecture, security, privacy, release, product, or cross-module review |
| `worker/critical`, `reviewer/critical`, or `architect/critical` | `gpt-6-astra/high` | Hardest unresolved reasoning or critical decision; role and authority stay explicit |
| `operator/fast` | `gpt-5.6-luna/low` | Exact approved low-risk operation with no interpretation |

Raise `worker/standard` from `medium` to `high` when several assumptions must be
tested, debugging becomes non-trivial, tool iteration grows, or validation is
weaker than the normal deterministic path. Keep the model tier unchanged only
when ambiguity, blast radius, judgment, and failure cost still fit `standard`;
otherwise escalate the semantic route.

Keep reasoning separate from model capability. These are provisional starting defaults,
not measured optima. Use `high` for controllers and substantive review; reserve
Astra/`xhigh` for an explicit reason that `high` is insufficient. `max` and
`ultra` are not automatic routing defaults. Do not spend `xhigh` effort on Luna,
Spark, or Terra as a substitute for a justified stronger capability route.

Development delivery mode remains independent: `--fast` does not select Luna,
and a standard or strict lifecycle does not automatically select Terra or Sol.

## Spawn Behavior

Inspect the actual tool schema and its usage restrictions before binding the
route. When supported and permitted, set both explicitly:

- `model`: the resolved model from stage 1;
- reasoning: the resolved effort from stage 2, using the tool's actual field
  (`reasoning_effort` for bounded spawn, `thinking` for visible task creation).

### Visible Codex Tasks

For `create_thread`, a model field may exist while its usage rule permits an
override only when the user explicitly named that model. Follow that rule;
the adapter's recommendation and permission to delegate are not an explicit
user model choice. If the tool requires the application default, omit `model`
and record `proposed_model` separately from `requested_model: application-default`.
Set `thinking` when permitted. Do not describe a usage restriction as an absent
field or unavailable model, and do not change client defaults or use another
dispatch surface to bypass it.

Application-default selection is not an availability substitution: no requested
model was rejected. Report `model_selection: application-default` and the
constraint instead of claiming the proposed model was selected. It does not
consume or reset escalation budgets. A required exact binding, forbidden model
deviation, known below-floor default, or unverifiable mandatory spend ceiling
still stops dispatch; do not use default selection to bypass those constraints.
Otherwise preserve the semantic route and report any unexposed binding as
unknown, without claiming the capability floor has been verified.

When the user explicitly names a supported model, pass it in `model` under the
tool's rule, subject to the existing capability and authority boundaries. A
general request to use agent-routing is not a named-model request under a tool
rule that specifically requires one.

Visible task creation may have no profile selector. With profile fallback
allowed, carry the role instructions in the prompt and record that the named
profile was not selected; textual `role: worker` is not proof of runtime profile
loading. With fallback forbidden, stop. Do not replace a user-owned issue task
with a bounded agent to obtain model or profile controls.

For a fresh issue-controller thread, classify its issue before creation and use
`controller/standard`, `controller/deep`, or
`controller/critical`. Apply the same evidence-based classification to new
top-level controllers; persistence alone does not select Astra or `xhigh`.
An existing controller retains its actual runtime binding; do not claim an
in-place model switch or create a duplicate controller to match this table.

The generated role profiles intentionally omit `model` and
`model_reasoning_effort`. Pinned profile values would override spawn/default
resolution and collapse role, capability tier, reasoning, and executor. If a
client can select a named profile and explicit model together, use both. If its
spawn API cannot select a profile, set permitted model/effort overrides and carry
the role instructions plus full routing envelope in the task prompt.

Some spawn surfaces allow model overrides only when the child receives no parent
history or a bounded history fork. When full-history inheritance prevents an
override, provide a focused handoff or record the inherited binding; never claim
the requested binding was accepted when it was not.

## Visible Binding And Receipt

Publish the shared request notice before every spawn or user-owned thread
creation and the active notice after acceptance. Keep capability tier, model,
and reasoning separately visible:

```text
Routing request: focused edit | worker/fast | lifecycle/role: bounded/worker | tier/reasoning: fast/medium | executor policy: required codex | proposed: codex gpt-5.6-luna/medium | profile: worker | profile fallback: allowed
Routing active: focused edit | worker/fast | executor: codex | model: gpt-5.6-luna/medium | profile: worker | runtime role: worker | executor fallback: none | model fallback: none | reasoning fallback: none | profile fallback: none | independence: not-required
```

A successful call confirms only that Codex accepted the explicit values passed
to that call. Preserve those values in the child prompt and require the shared
routing receipt. When runtime metadata exposes the effective turn binding,
verify it; otherwise report the accepted values without claiming independent
runtime verification.

A queued creation result establishes dispatch acceptance, not a running task or
effective model/profile. Keep it pending until a real task ID is available. At
the first ready/active observation, make one supported read of that task's
binding metadata or runtime-sourced receipt and update the existing registry
and resolved notice. Distinguish accepted arguments from observed execution;
if the read exposes no model/profile, retain `unknown` with the observability
limit rather than continuing to promise verification after startup. Do not
infer effective values from the title, recommended route, prompt, or settings
alone. Avoid repeated unchanged reads, duplicate tasks, or an unrequested live
model switch. Report a known mismatch without relabeling the semantic tier.

If the named role is unavailable, retry through `default` only when the routing
envelope says `profile_fallback: allowed`. When it says `forbidden`, report the
unavailable profile and stop without attempting `default`. Keep model and
reasoning unchanged and report an allowed fallback as:

```text
Routing active: focused edit | worker/fast | executor: codex | model: gpt-5.6-luna/medium | profile: default | runtime role: default | executor fallback: none | model fallback: none | reasoning fallback: none | profile fallback: worker unavailable | independence: not-required
```

Profile unavailability never changes provider or model by itself. When default
fallback starts, report the active model, the unavailable requested profile, the
`default` runtime role, and that profile-specific instructions were not loaded.
Keep these explicit fields in the receipt or fallback packet:

```yaml
model_active: gpt-5.6-luna
requested_profile_unavailable: worker
requested_profile_fallback: allowed
accepted_profile: default
runtime_role_default: default
profile_instructions: not-loaded
```

## Escalation And Availability

Apply the shared separate effort/capability budgets and keep permissions, write scope, approval,
executor policy, and lifecycle unchanged:

- Luna -> Terra: mechanical execution expands into normal repository reasoning
  or non-trivial debugging;
- Terra -> Sol: cross-module ownership, product/architecture judgment,
  security-sensitive work, or high failure cost appears;
- Sol -> Astra: the hardest unresolved reasoning remains or a critical decision
  requires the highest tier;
- Spark -> the evidence-selected Terra, Sol, or Astra route: its bounded coding
  assumptions fail. Do not bounce through Luna or force intermediate attempts.

An effort-only Terra/medium -> Terra/high adjustment leaves the capability
allowance available for Sol/high if new evidence requires deep reasoning.
The task-wide counters do not reset on the Sol attempt. A spent capability
allowance blocks a further automatic Astra upgrade even if effort remains.
Use the shared accounting for destination defaults and simultaneous changes.

For model unavailability, the only automatic stronger-model order is:

```text
gpt-5.6-luna -> gpt-5.6-terra -> gpt-5.6-sol -> gpt-6-astra
```

This is the configured stronger-fallback order, not a benchmark result. It
applies only to models explicitly listed in
`availability_fallback.allowed_models`, within the existing cost policy and
supported tools, context, and reasoning. For example, a Luna task with
`allowed_models: [gpt-5.6-terra]` stops if Terra is also unavailable; it cannot
continue to Sol or Astra. Empty or omitted lists allow no model substitution. An
explicit model request, budget limit, or required binding takes precedence.
Spark has no automatic availability substitution in this order; report its
unavailability and obtain a binding decision from the controller. Use the shared
Dispatch Failure Diagnosis with `runtime_unavailable` when the target rejects
Spark as unavailable; use `dispatch_rejected` only for a controller/API rejection.
Record the requested binding and `accepted_model: unknown` when no acceptance
exists, with `model_fallback: none`; do not emit an active routing notice for
that failed attempt. Never silently relax its latency preference or claim a new binding was accepted before it was.
Do not substitute in the opposite direction without explicit authorization.
Record requested model, accepted model, `model_fallback`, requested reasoning,
accepted reasoning, and `reasoning_fallback` separately. If executor policy
resolves away from Codex, stop using this adapter and remap the unchanged
provider-neutral route through the resolved executor's adapter.

## Controller Status And Wake Capabilities

Read when a Codex controller dispatches persistent issue tasks or resumes their
coordination. Follow the actual tool schema; CLI, desktop and hosted surfaces
need not expose the same capabilities.

- When available, use `wait_threads` for compact task status, batching targets
  and carrying each returned cursor as `afterCursor`. `timeoutMs: 0` gives an
  immediate snapshot; a bounded wait can confirm an in-flight dispatch. A
  timeout or unchanged commentary is not task completion. Read detailed task
  history only for the affected blocker, missing callback or unresolved gate.
  For a healthy idle reconciliation, take at most one compact snapshot per
  target unless a new actionable signal or unresolved health check requires
  another read. Do not follow an unchanged snapshot with a 45–55 second wait
  and then repeat on the same cursor merely to keep the turn alive.
- A `wait_threads` call waits within the current turn. It does not establish a
  subscription that wakes a task after the turn ends. Once only external
  progress remains, save cursors and return to the verified callback and
  task-attached heartbeat path supported by that runtime. Reuse its existing
  automation and shared reconciliation state instead of adding another poller.
- Tell persistent workers to send their completion/blocker packet to the
  controller through the supported task messaging tool (for example,
  `send_message_to_thread` where available). Keep this callback as the primary
  wake and the orchestrator's longer heartbeat as backup; do not send progress
  requests to healthy workers merely because a status wait timed out.
- An authorized goal continuation uses the same cursor and recovery deadline
  as callbacks and heartbeat. Reuse a signal already checked for this cycle;
  perform any fresh liveness check required by the active goal contract, then
  end if no controller action remains. Do not create an additional heartbeat,
  rewrite its prompt or chain waits to occupy the goal turn. If the host
  immediately starts another goal turn, report its missing pause/coalescing
  capability once; a Skill cannot stop that scheduler or change goal status
  merely to reduce wakes.
- Use a detached terminal-condition watcher only with evidence that its
  completion notification can wake the same controller after the turn ends.
  A shell PID, exec session ID, or pollable output is not that evidence. If
  this capability is absent or unknown, retain supported callback/heartbeat
  recovery; do not copy Claude background-command assumptions into Codex.
- If no supported callback or automation can resume the controller, disclose
  that automatic continuation is unavailable. Saving controller state enables
  later recovery but does not schedule it. Do not replace a persistent issue
  task with a bounded agent to obtain different wake behavior.

Shared barrier, recovery deadlines, quiet-wake backoff and Review evidence stay
with the calling orchestrator. These capability checks do not claim measured
Codex token savings or change its host scheduler.

## Evidence And Calibration

Model identities, Light/Low effort naming, and Spark's text-only interactive
coding purpose were checked against [official model guidance](https://learn.chatgpt.com/docs/models)
on 2026-09-05. [Luna's model page](https://developers.openai.com/api/docs/models/gpt-5.6-luna)
describes its cost-sensitive workload focus. Resolve actual availability and
supported effort from the target runtime before dispatch; public documentation
does not prove account access or an accepted binding.

The worker model/effort defaults above are provisional calibration candidates.
The controller Terra/high minimum is a user-selected policy floor; calibration
does not authorize production dispatch below it. Compare bounded-worker
Terra/medium vs Terra/high and Terra/high vs Sol/high using equivalent tasks.
The defaults implement the current routing proposal. They are not measured
quality, latency, token-savings, or subscription-usage equivalence claims.
Evaluate comparable tasks with the same acceptance and review criteria before
retiring Terra or Sol, promoting Spark beyond its bounded scope, or making
Astra/low an ordinary-work default. Count failed attempts and repairs as cost.
