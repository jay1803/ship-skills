# Claude Code Adapter

Use after the helper selects `claude-code`. Model IDs and the effort mapping
live in [`models.json`](../scripts/models.json); this table maps the binding
onto the actual surface.

| Surface | Model | Effort | Profile |
| --- | --- | --- | --- |
| `Agent` subagent | `model`: the full ID where the schema accepts it, otherwise the matching alias (`sonnet`, `opus`) | Runtime effort setting where exposed | Named agent profile from `~/.claude/agents/` |
| Background session (`claude --bg`) | `--model <full ID>` | `--effort <level>` | Role instructions in the handoff |

Request full model IDs where the surface accepts them: the `sonnet` and `opus`
aliases resolve to different versions on different providers, so a model passed
as an alias stays `unknown` until runtime evidence shows the version. List the
full IDs an alias surface can reach in the runtime inventory.
`CLAUDE_CODE_SUBAGENT_MODEL` or an organization allowlist can also override the
requested model, so treat a model as accepted only when the invocation or
runtime evidence confirms it, and record a substitution or `unknown` otherwise.
Claude Code has no `xhigh` or `max` effort; the helper maps both to `high` and
discloses it in `reasoning_fallback`.

Ordinary `Agent` subagents are bounded helpers. Agent Teams teammates add team
messaging but are not independent persistent sessions. Persistent issue
sessions, callbacks and wakes belong to the calling orchestrator.
