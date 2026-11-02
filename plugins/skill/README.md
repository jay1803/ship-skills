# Skill plugin

Design, develop and independently assess reusable agent Skills. The four
entrypoints own different artifacts; a request can use one directly without
loading a full lifecycle or another routing service.

- [skill-patterns](skills/skill-patterns/SKILL.md): architecture, discovery,
  client bindings and the execution/authorization design contract.
- [skill-dev](skills/skill-dev/SKILL.md): implement the authorized design using
  the environment's `skill-creator`, then obtain proportional behavior evidence.
- [skill-review](skills/skill-review/SKILL.md): independently judge a frozen Skill
  change, or audit a whole Skill family for over-design, against its minimal
  alternative; return supported findings and concrete gaps without repairs.
- [skill-session-review](skills/skill-session-review/SKILL.md): audit Codex or Claude
  sessions from task input through verified outcome and identify evidence-backed
  opportunities to reduce avoidable cost.

Use `skill-patterns` for new or substantial design, `skill-dev` for authoring,
and `skill-review` in a fresh context for separate acceptance. Use
`skill-session-review` for session-cost audits; it remains separate from Skill
authoring and acceptance. Ordinary wording changes remain light. Code Review
supplements executable scripts. Repository
issues, commits, PRs, human merge policy and release procedure stay with the host.

The plugin uses no mandatory remote evaluator. Live provider tests remain scoped
to their action, destination, payload and existing authority. Static validation,
independent simulation and actual execution are reported separately.

Install through the marketplace with `codex plugin add skill@jay1803-ship-skills` or
`claude plugin install skill@jay1803-ship-skills`. Invoke `$skill-patterns`, `$skill-dev`,
`$skill-review` or `$skill-session-review` in Codex; `/skill:skill-patterns`,
`/skill:skill-dev`, `/skill:skill-review` or `/skill:skill-session-review` in Claude Code.

`skill-patterns` moved from standalone into this plugin without a duplicate
active copy. Rerun the repository's standalone linker to remove its old managed
link, and install the plugin through the native client. A source move does not
update installed consumers. Preserve unrelated same-name files or installations. Do not pass
`--skill skill-patterns` to the standalone linker after this migration.

## Discovery evaluation

Six opt-in cases cover explicit, implicit and contextual selection among the
design, authoring and Skill-review entrypoints, plus a session-audit request and
an adjacent code-review request. Run the
selected suite through the repository's `npm run eval:trace` runner and retain
the raw JSONL outside tracked source. It checks a schema-constrained discovery
decision, not native Skill-load telemetry or full lifecycle execution:

```bash
npm run eval:trace -- \
  --case mx154-skill-discovery/explicit-review \
  --case mx154-skill-discovery/implicit-design \
  --case mx154-skill-discovery/implicit-authoring \
  --case mx154-skill-discovery/contextual-behavior-review \
  --case mx154-skill-discovery/negative-code-pr \
  --case mx154-skill-discovery/explicit-session-review \
  --run-dir .eval-runs/skill-discovery
```
