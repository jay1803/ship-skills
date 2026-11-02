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

Choose the executor, model, reasoning effort and profile for one delegated
agent. You make the semantic decisions; the packaged helper applies the
deterministic floors and model table offline and returns a proposal. It never
dispatches, calls a service, or changes authority or lifecycle gates.

Every delegated role inherits all permissions available to its parent for the
authorized task. Only an explicit user restriction or an enforced runtime limit
narrows access; delegation and phase changes never need renewed approval.

1. Decide `role`, `tier`, `effort`, `decision_state`, `risk` and
   `judgment_review` from the task facts you hold, using the checklist in the
   [routing contract](references/routing-contract.md#decide). Carry explicit
   user constraints unchanged; never turn a preference into a requirement.
2. Write those decisions, the task and the current runtime inventory to
   `facts.json` and run
   `python3 <this-skill>/scripts/route_agent.py --input facts.json`.
   Exit 0 returns `routing_envelope`, `runtime_binding`, role instructions and
   the task. Exit 2 returns `blocked` with a reason code: repair the named fact
   or report it, and do not pick a binding around the floor by hand.
3. Dispatch through the selected [Codex](references/codex-adapter.md) or
   [Claude Code](references/claude-code-adapter.md) adapter.

The binding is a proposal until the runtime accepts it. Publish the requested
binding before dispatch and the accepted one afterwards; keep values the
runtime does not expose `unknown`. An existing agent keeps its actual binding on
ordinary resume. To escalate, rerun with the new evidence and the prior
envelope as `previous_route`; the owning controller counts the reported
adjustment against its own budget.

Installing the generated role profiles and the optional DeepSeek Codex profile
is described in the [Develop README](../../README.md#agent-routing-profiles).
