# Client Bindings

An archetype says what a skill owns. A binding says how one client makes the
skill behave that way: who may invoke it, where it runs, which tools it may
use, when it loads, and how it receives input. Read this after choosing the
archetype, for the clients the skill ships to.

## Contents

- [Where policy lives](#where-policy-lives)
- [Bindings by archetype](#bindings-by-archetype)
- [Explicit-only invocation](#explicit-only-invocation)
- [Isolation](#isolation)
- [Tool scope](#tool-scope)
- [Auto-loading and background knowledge](#auto-loading-and-background-knowledge)
- [Arguments and live context](#arguments-and-live-context)
- [Discovery and context budget](#discovery-and-context-budget)
- [Portability rules](#portability-rules)

Sources: the Claude Code skills reference
(<https://code.claude.com/docs/en/skills>) and the Codex `skill-creator`
system skill with its `references/openai_yaml.md`. Both change; when a field
below decides a design, confirm it against the current client.

## Where Policy Lives

| Concern | Codex | Claude Code |
| --- | --- | --- |
| Discovery text | `name` and `description` frontmatter | `name` and `description` frontmatter |
| Invocation policy | `agents/openai.yaml`: `policy.allow_implicit_invocation` | frontmatter `disable-model-invocation`, `user-invocable` |
| UI metadata | `agents/openai.yaml`: `interface.*` | frontmatter `argument-hint`; no UI file |
| Explicit invocation | `$skill-name` | `/skill-name`; a plugin skill is always `/plugin-name:skill-name` |
| Declared dependencies | `agents/openai.yaml`: `dependencies.tools` (MCP servers) | none at skill level; `allowed-tools` pre-approves tools |
| Free-form catalog fields | frontmatter `metadata` map, preserved by tooling | frontmatter `metadata` map, accepted and not acted on |

Claude Code does not read `agents/openai.yaml`; Codex does not act on
Claude-only frontmatter. Keep the two consistent: `short_description` and
`default_prompt` must describe the same skill as the frontmatter, and the
invocation policy must be one decision expressed in both places.
`agents/openai.yaml` is optional in Codex: a skill that needs only a name,
description, and body ships without it, and Codex tooling adds `interface.*`
values only when the user provides or requests them.

## Bindings by Archetype

| Archetype | Codex | Claude Code |
| --- | --- | --- |
| Atomic capability | Default automatic selection; `interface.default_prompt` shows the entry | Default; `argument-hint` and `$ARGUMENTS` carry the input contract |
| Operational procedure | `policy.allow_implicit_invocation: false` when the decision below says explicit-only | `disable-model-invocation: true` when explicit-only; `allowed-tools` pre-approves the read-only precondition and verification commands, not the mutation itself |
| Artifact generator | No binding beyond `assets/` | `${CLAUDE_SKILL_DIR}` locates bundled assets and scripts |
| Router | Routes are references or explicit `$worker-skill` invocations | Routes may be references, skills, or subagents; `$0`, `$1` select by argument |
| Orchestrator | Workers are skills invoked explicitly; state lives in the artifact or tracker | Workers are usually subagents, which may preload worker skills with `skills:`; `context: fork` with `agent:` runs the skill itself in an isolated subagent |
| Review gate | Independence comes from a fresh session or worker; state the boundary in the text | `context: fork` gives a subagent with no conversation history; its `agent:` type, not the skill's `disallowed-tools`, sets what it may do (see [Isolation](#isolation)); `!` lines inject read-only command output; `model` on the skill, or `model` and `effort` in the agent definition, set depth |
| Domain guide | Selected by description only | `paths:` loads it only for matching files; `user-invocable: false` hides background knowledge from the `/` menu |

## Explicit-Only Invocation

Both clients select skills automatically by default. The two vendors phrase the
exception differently. The Claude Code reference recommends
`disable-model-invocation: true` for workflows such as `/commit`, `/deploy`, or
`/send-slack-message`, so that the model does not choose their timing. The Codex
`skill-creator` says not to infer explicit-only invocation from sensitive
operations, and to keep the skill discoverable with authorization required
immediately before the mutation.

Decide on one criterion and express it in every target client; for the skill
being designed it supersedes either vendor's default. Make a skill
explicit-only when its whole job is a mutation whose timing the user owns, such
as deploying, committing, sending, or publishing, so that automatic selection
would start that mutation unasked. Keep a skill discoverable when it guides a
task that merely contains a gated mutation, and keep the gate. In Claude Code
the model cannot invoke a skill marked `disable-model-invocation: true`, even
from an orchestrator, and it cannot be preloaded into subagents; only the user
starts it.

Explicit-only invocation never replaces the
[authorization check](archetypes.md#authorization-check) before the mutation,
but an explicit invocation can satisfy it. `/deploy-staging main` or
`$deploy-staging main` names the action and its scope, so the skill checks its
preconditions and proceeds without asking again. It stops to ask only in the
cases the check lists, such as a missing scope or a command that differs from
what was named. The client's own permission prompt for the command is a
separate layer that the user's permission settings control. The skill adds no
confirmation of its own to a named request, and it does not pre-approve the
mutating command to suppress the client's prompt (see
[Tool scope](#tool-scope)).

Explicit-only invocation is not a block. It controls who selects the skill, not
whether the model may run the underlying command. Claude Code refuses a model
invocation of a `disable-model-invocation` skill and tells the model not to
reproduce its steps another way. That is an instruction, not enforcement: a
request such as "run the deploy script" can still reach the script directly.
When the command itself must not run without the user, pair the skill with the
client's command controls. These belong in client or repository configuration,
not in the skill (see [Not a skill](archetypes.md#not-a-skill)).

- Claude Code: an `ask` permission rule such as `Bash(./scripts/deploy.sh *)`
  prompts on every run, in or out of the skill, because ask and deny rules
  override `allowed-tools`. A `deny` rule also blocks the skill, so it suits a
  command the user runs by hand. A `PreToolUse` hook covers conditions a rule
  cannot express. A Bash rule matches the command text the model writes, not
  every way of starting the program, so treat it as a guardrail; sandboxing is
  the enforcement boundary.
- Codex: its approval policy and sandbox settings.

## Isolation

`context: fork` in Claude Code starts a new subagent of the type named in
`agent` and gives it the skill content as its whole prompt. The subagent does
not see the conversation history, runs in the background unless
`background: false`, and applies edits outside the session's checkpoints. Use
it for a review gate or a forward test that must not see the implementation
thread. It requires the skill to state a complete task; guideline-only content
returns nothing useful from a fork. When the task depends on the conversation,
delegate to a subagent that forks the conversation instead.

When `agent` is omitted the fork uses the `general-purpose` subagent with its
full tool set. The fork's tools come from that agent type (and, for a
background fork, the narrower background tool set), so choose the agent type
for what the fork may do. Do not make the skill's `disallowed-tools` the fork's
boundary. The skills reference defines that field for the invoking
conversation and does not say that it reaches the fork. It also clears on the
user's next message, while a background fork may still be running.

For a review gate, choose the agent type by what the gate must not do:

- `Explore` lacks Write and Edit but keeps Bash. Only its prompt and the user's
  permission rules keep its shell commands read-only, so a command such as
  `gh pr comment` stays reachable wherever those rules allow it. `Explore` also
  skips `CLAUDE.md` and the git status snapshot, so a gate that must apply
  repository rules either reads them itself or uses a project subagent.
- A gate that must not run mutating commands uses a project subagent under
  `.claude/agents/` with `tools: Read, Grep, Glob` and no Bash. The skill
  injects the command output that the gate needs, such as `gh pr diff`, with
  `!` lines (see [Arguments and live context](#arguments-and-live-context)).
- A subagent's `tools` field takes tool names, not permission rules. An entry
  such as `Bash(gh pr diff *)` does not limit Bash to that command, so a
  command-level allowlist in `tools` is unsupported. To let a subagent run only
  some commands, list `Bash` and add a `PreToolUse` hook to its frontmatter that
  rejects the rest, or deny the mutating commands in permission settings.
  Claude Code skips a project subagent's frontmatter hooks in a folder the user
  has not trusted, including `claude -p` runs there, so prefer the agent
  without Bash when the gate must hold everywhere.

Set `background: false` when the invoking turn needs the verdict, as a gate
before merge usually does.

Codex has no skill-level fork. Obtain independence with a fresh session or a
worker that receives only the frozen target, and write that requirement into
the skill so it holds in every client.

## Tool Scope

In Claude Code, `allowed-tools` grants permission for the turn; it does not
remove tools. Pre-approve only the read-only precondition and verification
commands, including those that `!` lines inject: pre-approving the mutating
command itself would let the skill grant the permission that the design
invariants reserve for the user. `disallowed-tools` removes tools from the
invoking conversation for the turn; do not assume it narrows one tool such as
`Bash` to some commands. Both fields clear on the next user message. Codex
declares MCP dependencies in `agents/openai.yaml` and documents no per-skill
tool restriction.

A review gate that must not edit says so in its text; the text is the portable
boundary. In Claude Code, a gate that runs inline adds `disallowed-tools` as
reinforcement for its turn. A forked gate takes its boundary from its `agent`
type instead (see [Isolation](#isolation)).

## Auto-Loading and Background Knowledge

`paths:` in Claude Code limits automatic loading to work on matching files,
using the same glob format as path-specific memory rules. It suits a domain
guide for one language, directory, or file type. `user-invocable: false` keeps
a knowledge skill out of the `/` menu while the model can still apply it. Codex
has neither; a domain guide there is selected by description, so the
description must name the file types or domains it covers.

## Arguments and Live Context

Claude Code substitutes `$ARGUMENTS`, `$ARGUMENTS[N]` or `$N`, names declared
in `arguments`, `${CLAUDE_SKILL_DIR}`, `${CLAUDE_PROJECT_DIR}`, and plugin
paths in the skill body and in `allowed-tools`. A `` !`command` `` line runs
before the content reaches the model and injects its output. This suits an
atomic skill that needs current repository state, and a forked gate that must
review command output without running commands. The command runs in the
invoking session, under its permission rules and the skill's `allowed-tools`,
and never prompts. In a `context: fork` skill it runs before the subagent
starts, and the subagent receives only the output. The whole invocation aborts,
and a fork never starts, when a command exits non-zero (apart from exit 1 from
a search or comparison command) or its permission check does not return allow.
Pre-approve each injected command in `allowed-tools`. In auto mode an
unapproved command is handed to the model to run instead, but a forked skill
that sets `agent` still aborts. Codex passes arguments as the text after
`$skill-name`.
A router's shared contract should therefore accept its input from either the
argument string or the request text.

## Discovery and Context Budget

Claude Code lists every skill's name and description in context under one
budget. When the listing overflows, descriptions are shortened starting with
the least-used skills, and the listed text of one skill is cut at a fixed
length. After context compaction, each invoked skill is re-attached only up to
a per-skill limit inside a combined limit.

| Limit | Claude Code value |
| --- | --- |
| Listing budget | 1% of the model's context window |
| Listed `description` (with `when_to_use`) | 1,536 characters |
| Re-attached skill after compaction | first 5,000 tokens per skill |
| Combined re-attached skills | 25,000 tokens |
| Recommended `SKILL.md` length | under 500 lines |

Codex also exposes only the name and description before loading. The same
rules follow for both: key use case in the first sentence, invariants in the
first part of `SKILL.md`, conditional detail in references.

## Portability Rules

- Keep `name`, `description`, and the body client-neutral; name a client only
  where the mechanism differs.
- Frontmatter a client does not define is not acted on. The skill must still be
  correct when only `name` and `description` are honored, so a safety or
  authorization boundary is always stated in the text, not only in a field.
- Express one invocation decision in both places: `disable-model-invocation`
  and `policy.allow_implicit_invocation` must agree.
- Show explicit invocation in both syntaxes, or in neutral words such as
  "invoke `skill-name` explicitly", rather than only as `$skill-name`.
- Put catalog or ownership fields under `metadata`; do not reuse a client's
  frontmatter field names as metadata keys.
- Validate with each target client's tooling; see
  [evaluation.md](evaluation.md#structural-check).
