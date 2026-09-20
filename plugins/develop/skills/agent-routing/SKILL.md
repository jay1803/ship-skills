---
name: agent-routing
description: "Select executor and runtime bindings when dispatching or escalating a delegated controller, worker, or bounded agent."
metadata:
  owner: jay1803
  family: develop
  maturity: stable
  distribution: develop
---

# Agent Routing

Resolve semantic role, capability, reasoning and runtime binding through Jev
when it is configured. The executing model consumes the returned packet without
loading or repeating the classification policy, PM map or adapter
model-selection tables.

Jev is optional. Set `TYPESAFE_API_KEY` (or `JEV_API_KEY`) in the environment or
in `JEV_ENV_FILE` (default `~/.config/jev/.env.local`). A `credential_unavailable`
exit means no route was obtained: select the binding from the adapter references
yourself and report it as locally selected.

Default every role to all available parent permissions. Only explicit user
restrictions narrow access; runtime-enforced limits still apply. Delegation and
phase transitions never require renewed user approval for the authorized task.
Responsibility and write coordination do not create permission gates.

1. Collect the task, explicit user restrictions (if any) and current runtime inventory
   using the [input contract](references/jev-input.md).
2. Run `python3 <this-skill>/scripts/route_agent.py --input <facts.json>`.
3. Accept `routing_envelope` and `runtime_binding`, then follow the returned
   dispatch instructions. Preserve explicit executor/model/profile constraints.
4. Report a `blocked` reason without dispatch or silent main-model fallback.
   Refresh changed evidence and rerun only when the named boundary is resolved.

A route is a proposal until the runtime accepts it. Publish requested and actual
bindings separately; unknown effective values remain unknown. The helper does
not create agents, switch controllers, grant writes or change lifecycle gates.
Use the same helper for evidence-backed escalation with the prior route and
its existing counters.

The program consumes the canonical [routing contract](references/routing-contract.md),
[PM map](references/pm-routing-map.md), [Codex adapter](references/codex-adapter.md)
and [Claude adapter](references/claude-code-adapter.md). Read those only when
maintaining routing policy or investigating a routing defect; for persistent
session creation/recovery, read only the selected adapter execution section.

## Runtime Assets

Provider-neutral role definitions live in `assets/roles/`. Generated runtime
profiles live in `assets/codex-agents/` and `assets/claude-agents/`. Both omit
model and reasoning settings so role remains independent from depth and
executor selection. After changing a role, regenerate and check both formats:

```bash
./scripts/render-agent-profiles.py --write
./scripts/render-agent-profiles.py --check
```

Copy the profiles into a Codex installation with:

```bash
./scripts/link-codex-agents.sh --apply
```

Use `--check` to verify the copied files, or `--target-dir PATH` to install them into a
different Codex home or staging directory.

Link the same semantic profiles into a Claude Code installation with:

```bash
./scripts/link-claude-agents.sh --apply
```

Claude Code profiles target `~/.claude/agents/` by default. Use `--check` or
`--target-dir PATH` the same way as for Codex. Restart an existing Claude Code
session after creating its `agents/` directory for the first time; later edits
inside an already-watched directory can be picked up without restarting.
