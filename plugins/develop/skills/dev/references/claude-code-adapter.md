# Claude Code Agent Routing Adapter

Use this adapter only after the shared routing contract resolves executor policy
to Claude Code. It maps the same provider-neutral lifecycle, role, capability
tier, and reasoning depth used by the Codex adapter. Do not create a Codex-only
semantic route or infer executor from role.

## Stage 1: Select The Model Alias

Map the provider-neutral capability tier after applying the shared ambiguity,
judgment, blast-radius, failure-cost, validation-quality, and fast-tier gates:

| Capability tier | Claude model alias | Selection boundary |
| --- | --- | --- |
| `fast` | `haiku` | Only when every shared fast-tier gate condition passes |
| `standard` | `sonnet` | Normal repository or domain reasoning with clear ownership and risk boundaries |
| `deep` | `opus` | Cross-boundary, judgment-heavy, conflicting-evidence, or high-cost work |
| `critical` | `opus` | Hardest unresolved reasoning or genuinely critical work |

Use stable aliases so Claude Code can resolve the current allowed version. Do
not copy full Claude model IDs into the shared contract or role profiles.

## Stage 2: Select Effort

Choose effort independently from model alias:

| Semantic route | Initial Claude Code binding | Notes |
| --- | --- | --- |
| `controller/standard` | `sonnet/high` | Ordinary clear issue with full lifecycle control |
| `controller/deep` | `opus/high` | Cross-module, judgment-heavy, conflicting-evidence, or high-cost issue |
| `controller/critical` | `opus/high` | Hardest unresolved reasoning or genuinely critical control; xhigh requires explicit justification |
| `explorer/fast` | `haiku/medium` | Known-target lookup or repeatable narrow evidence gathering |
| `explorer/standard` | `sonnet/medium` | Repository scan, dependency trace, or ordinary context reconstruction |
| `worker/fast` | `haiku/medium` | Explicit, mechanical, local, reversible, deterministically validated mutation |
| `worker/standard` | `sonnet/medium` | Clear scoped implementation or artifact with normal reasoning |
| `worker/deep` | `opus/high` | Cross-boundary implementation, substantive plan/spec, or judgment-dense artifact |
| `reviewer/standard` | `sonnet/high` | Ordinary independent review; preserve the `high` floor |
| `reviewer/deep` / `architect/deep` | `opus/high` | Architecture, security, privacy, release, product, or cross-module review |
| `operator/fast` | `haiku/medium` | Exact approved low-risk operation with no interpretation |

Raise `worker/standard` to `high` for non-trivial debugging, broader tool
iteration, several tested assumptions, or weaker validation while capability
still fits `standard`. Do not make `haiku/xhigh` or `sonnet/xhigh` a default
combination; a genuine `xhigh` need normally selects a critical route on Opus.

`operator/fast` never performs code reasoning. The shared fast-tier gate, not
line count or delivery mode, controls whether `worker/fast` is legal. New
controllers require at least `controller/standard -> sonnet/high`; the shared
controller floor excludes Haiku from lifecycle ownership.

The existing Haiku/medium defaults for exact exploration and operations remain
an executor-specific higher-effort default; record that binding rather than
claiming the shared low setting was applied. For these two routes, keep
`requested_reasoning: low` as the semantic request, propose and pass `medium`
to Claude, and record `accepted_reasoning: medium` only after acceptance with
`reasoning_fallback: adapter default low -> medium`. The request notice shows
both the semantic low request and proposed Claude medium binding. No new field
or silent normalization is needed. Codex's Spark alternative does not map to a
Claude alias. A latency preference never changes required executor or
review independence. GPT-6 performance assumptions do not establish Claude
performance.

## Invocation Behavior

Set model alias and effort explicitly on the invocation or controller session
when the runtime exposes both. For a fresh issue-controller session, classify
the issue before creation. Classify top-level controllers from their scope too;
persistence alone does not select `critical` or `xhigh`. An already-running
controller retains its observed binding.

When an installed runtime provides named role profiles, prefer profiles that do
not pin model or effort. If the runtime cannot select a profile, carry the role
instructions and routing envelope in the task prompt. Treat a requested alias
as accepted only when the invocation or runtime evidence confirms it; otherwise
record the effective model as `unknown` or the observed substitution.

Runtime configuration such as `CLAUDE_CODE_SUBAGENT_MODEL` or an organization
allowlist can override alias resolution. Do not infer the effective model from a
profile name. Profiles inherit all available parent permissions. Narrow access
only for explicit user restrictions or enforced runtime limits, as defined in
the shared contract; a role does not select plan mode or a tool allowlist.

## Controller Session Evidence

For issue lifecycle ownership, use a runtime-native persistent session or
configured worker entry that returns a session identity and exposes that issue
as a separate user-owned session, with supported read/status and continuation
operations. Record the creation receipt, session identity, and management
surface before assigning it a controller entry in the worker registry. Pending
creation is not an active controller; resolve its outcome before retrying or
falling back, so an accepted but unobserved session cannot duplicate ownership.

### Discover The Actual Session Surface

Check the installed runtime's help and callable tools before declaring session
creation unavailable. In runtimes exposing native background sessions,
`claude --bg` is a controller-session entry; it is not `Agent` with a background
flag. A configured Axis entry remains valid under its own management contract.
Do not bypass a required executor/host or configured worker entry with a local
CLI launch. For a native local entry, use the assigned repository directory and
pass the classified model, effort, role instructions, and exact issue handoff.

The native command surface is:

| Operation | Supported entry and evidence |
| --- | --- |
| Create | `claude --bg --name <unique-name> --model <alias> --effort <level> -- <handoff>` returns a short background ID |
| Identify/status | `claude agents --json --all --cwd <directory>` exposes background ID, full `sessionId`, working directory, process/status and lifecycle state |
| Read | `claude logs <background-id>` shows recent terminal output; `claude attach <background-id>` opens the user-visible conversation |
| Continue live | Use native `ListAgents` / `SendMessage` where available, or the supported attached conversation / agent-view reply surface |
| Stop | `claude stop <background-id>` stops execution while preserving the conversation; re-read status before transferring ownership |
| Resume stopped | `claude --bg --resume <session-id> -- <follow-up>` continues the saved session; verify the returned identity |

Record the short background ID and full session ID separately in the existing
registry, together with the observed directory, accepted binding and creation
receipt. A display name is a discovery label, not durable identity. Reconcile
listing and runtime evidence before assigning the issue, and verify the actual
branch/worktree before allowing writes; separate sessions alone do not prove
filesystem isolation. Preserve the invoking workflow's branch and one-writer
rules, including when the runtime automatically creates a worktree.

Use `--` before a positional handoff, especially after variadic flags such as
`--tools`, so the prompt is not consumed as another option value. A created but
empty/idle session is not proof that the handoff was delivered.

For resume, reuse saved options. Repeating configuration flags or resuming an
already-running session can create a copy instead of continuing the same owner.
Compare the returned ID with the registry; an unexpected copy is not an accepted
replacement. Reconcile and quiesce duplicate execution before continuing the
same issue. A missing transcript or a fresh restart is not restored lifecycle
state: reconstruct the issue, branch, PR and pending gates before resuming work.

### Messaging And Completion

Before creating the first worker, verify the callback transport of the
controller session itself and record the result as `callback_transport` in the
worker registry. Whether cross-session messaging exists depends on how the
session was started (interactive REPL, `-p`, `--bg`, worktree, desktop app),
so check the running session, not the runtime version:

1. Confirm `SendMessage` is registered as a callable tool in the current
   session through the tool listing or a deferred-tool search. `ListAgents`
   alone is not proof: it can list peers and mention `SendMessage` in a session
   where `SendMessage` is not registered. Record `callback_transport:
   native-messaging` only after that confirmation.
2. Do not use the desktop app's session-management `send_message` as a
   callback or dispatch channel. That tool describes itself as a hand-off for
   a person reading the other session, not for orchestrating background work,
   and it neither runs in nor delivers to unattended sessions. Its presence is
   `callback_transport: ineligible` evidence, not native messaging.
3. Require the same check on the worker side. The worker handoff must tell the
   worker to confirm `SendMessage` at start and, when it is missing, to deliver
   the Worker Callback Packet through the [external callback record](claude-communication.md#external-callback-record)
   instead of finishing silently. A worker that completes without either
   delivery is `callback: undelivered`, which the controller heartbeat must
   detect from session status and the external record.

Discover the intended peer through `ListAgents`; resolve ambiguous names using
the runtime's returned address. Use `SendMessage` only for the assigned workers
and controller within the authorized scope. Default to native persistent-session
messaging as the wake signal, with the external callback record as the durable
carrier in every mode; read [communication selection, the external record, heartbeat limits and the file-mailbox fallback](claude-communication.md)
before choosing a transport or recovering a failed callback. Direct inbox writes
are permitted only through that guarded fallback; do not write sockets or
runtime membership registries. Verify callback receipt separately from send acceptance: an accepted send does not prove the recipient processed
it, and a print-mode controller may exit before a reply arrives.

Keep the owning controller reachable, or use the invoking orchestrator's
supported heartbeat/status recovery. On Claude Code the controller must stay a
live interactive session: a print-mode controller exits before callbacks or
heartbeats fire, and the heartbeat tools carry the idle-only, session-only and
expiry limits recorded in [Claude heartbeat](claude-communication.md#claude-heartbeat). When messaging is unavailable, held or
refused, record that boundary rather than changing permission settings or
pretending the session itself could not be created. Cross-session messages do
not grant user approval or bypass either session's permissions. Worker idle,
completed, stopped, and callback-received states are not issue merge/acceptance
evidence; verify the live lifecycle gates before opening a wave barrier.

### Agent Teams And Bounded Helpers

Classify the observed lifecycle, not the tool name alone. Ordinary `Agent`
subagents are bounded helpers. With experimental Agent Teams enabled, named
agents can instead become teammates with independent context, messaging and a
user-visible team panel. That enables team-scoped collaboration but does not
by itself satisfy the separate persistent issue-session contract above.

Agent Teams currently require an interactive lead; `-p` / Agent SDK execution
does not spawn teammates. In-process teammates are not restored by `/resume`,
cannot create nested teams, and cannot run their own background subagents.
Keep those limits explicit when selecting bounded collaboration under an issue
controller. Do not enable the experimental flag globally as an incidental
routing action, promote a teammate to issue owner from its ID alone, or remove
serial fallback solely because team messaging exists.

If no qualifying persistent creation entry exists or creation definitively
fails, report the observed limitation and apply the invoking orchestrator's
serial inline fallback. Pending or accepted-but-unobserved creation must first
be reconciled to avoid duplicate ownership. For Dev project execution, fallback
holds one active issue through review, repair, CI and required acceptance waits.
Bounded helpers remain available under that owner. Model/profile substitution
does not change this lifecycle boundary.

Runtime details evolve; verify capability against the installed version and
current official [agent-view documentation](https://code.claude.com/docs/en/agent-view),
[cross-session messaging](https://code.claude.com/docs/en/cross-session-messaging),
and [Agent Teams](https://code.claude.com/docs/en/agent-teams). Version or feature
flags alone are not a successful session or callback receipt.

## Visible Binding And Receipt

Apply the shared request and active notices:

```text
Routing request: focused edit | worker/fast | lifecycle/role: bounded/worker | tier/reasoning: fast/medium | executor policy: required claude-code | proposed: claude-code haiku/medium | profile: worker | profile fallback: allowed
Routing active: focused edit | worker/fast | executor: claude-code | model: haiku/medium | profile: worker | runtime role: worker | executor fallback: none | model fallback: none | reasoning fallback: none | profile fallback: none | independence: not-required
```

If a named profile is unavailable, use the runtime default only when the routing
envelope says `profile_fallback: allowed`. When it says `forbidden`, report the
unavailable profile and stop without attempting `default`. For an allowed
fallback, keep alias and effort unchanged, report the unavailable profile and
default runtime role, and state that profile-specific instructions were not
loaded. Profile unavailability never changes provider or model by itself.
Record `model_active`, `requested_profile_unavailable`,
`requested_profile_fallback: allowed`, `accepted_profile: default`,
`runtime_role_default: default`, and `profile_instructions: not-loaded` in the
fallback packet.

If Claude Code is preferred but unavailable and executor fallback is allowed,
publish the executor failure before retrying. Remap the unchanged semantic route
through the Codex adapter; do not carry a Claude alias into a Codex receipt or
describe executor substitution as profile fallback.

## Independent Review

When `independent_from` is set, compare the resolved executor with the referenced
implementation execution before dispatch. Claude Code can implement or review;
the role does not determine provider. A new Claude session, profile, or alias
does not satisfy executor independence when the referenced implementation also
used Claude Code.

## Escalation And Availability

Apply the shared separate effort/capability budgets without expanding permissions, write scope,
approval, executor policy, or lifecycle:

- Haiku -> Sonnet for normal repository reasoning or non-trivial debugging;
- Sonnet -> Opus for cross-module ownership, judgment-heavy, security-sensitive,
  or high-cost work.

For model unavailability, the only automatic stronger-model order is:

```text
haiku -> sonnet -> opus
```

Filter that order through `availability_fallback.allowed_models`; only listed
aliases may be substituted. Empty or omitted lists forbid model substitution.
Preserve task-wide adjustment counters and all existing cost limits.
Do not substitute in the opposite direction without explicit authorization.
Record requested and accepted alias, effort, model fallback, reasoning fallback,
profile fallback, and executor fallback separately.
