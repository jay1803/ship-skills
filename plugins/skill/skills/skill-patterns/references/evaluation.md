# Skill Evaluation

Show three things: the package is valid, the skill causes the intended
decisions, and it beats the simpler alternative at an acceptable cost.
Structural validation proves only the first.

## Footprint

Measure what a typical request costs before the agent acts:

- Words in `SKILL.md` plus the references the typical path always reads, for
  example with `wc -w`; list conditional references separately.
- Agents or subagents dispatched, external or paid calls, and script lines.

Report the footprint for a new skill and the before/after change for a revision.
An element that adds footprint must name the failure it prevents; a revision
that only adds should explain why nothing could be removed or replaced.

## Comparative evaluation

For a new skill or a substantial change, run the same realistic tasks with the
candidate and with a baseline: no skill, or the previous version. Use
independent evaluators that receive the request, the skill under test and the
minimum raw inputs, without the intended answer, suspected defects or the
authoring conversation (a subagent or `context: fork` in Claude Code; a fresh
session or worker in Codex). Claude Code's `claude plugin eval` runs a
with-and-without arm for plugin skills.

Judge the outputs against criteria held separately from the evaluators, and
record cost alongside quality: tokens, tool calls, wall time, agents and
external calls where the client exposes them, otherwise labeled proxies. A
skill that does not improve outcomes, or matches them at higher cost, should be
simplified or dropped. Keep the evaluation small: a few tasks that exercise the
decisions the skill exists for, including one where it should not change the
outcome.

## Discovery check

Use representative prompts rather than keyword assertions: positive requests
that should load the skill, boundary requests the description must still
discriminate, nearby requests that belong elsewhere, and explicit invocation
(`$skill-name` in Codex; `/skill-name` or `/plugin-name:skill-name` in Claude
Code). Descriptions share a truncated listing budget, so check that the first
sentence alone routes correctly (see
[client-bindings.md](client-bindings.md#discovery-and-context-budget)). If the
skill triggers too broadly, narrow the capability or add one meaningful
exclusion rather than a list of negatives.

## Behavioral check

Exercise the decisions that justify the skill: the normal path reaches the
outcome; a conditional path reads only its route; missing information triggers
a question only when it changes scope, authorization, architecture or result;
side effects stay within authority and confirm the actual target; failure,
partial completion and blocked work are distinguished; a handoff gives the next
owner enough state. Prefer observable invariants over exact wording, heading
counts or regex snapshots.

## Structural check

Supplementary: folder name and frontmatter `name` agree; the description states
capability and triggers; no scaffold placeholders remain; every reference is
linked from `SKILL.md` with a reading condition; scripts are executable and
tested; invocation policy, isolation, tool scope and UI metadata agree across
target clients; no README, changelog or empty resource directory was added
without a packaging need. Run the environment's validator, such as the
`quick_validate.py` shipped with `skill-creator`, the repository's checks and a
whitespace/diff check. In Claude Code, `/skill-doctor` reports skills that are
never invoked and what the listing costs, which helps prune.

## Proportional evidence

Match evidence to the changed decision. Wording-only edits need a diff review
and structural checks. Reuse existing scenarios for changed behavior, add a case
only for a missing decision or regression, and retire cases whose mechanism no
longer exists. A shared contract needs representative caller and boundary
checks, not copied audit narratives. Keep the summary in the response or PR;
follow repository tooling for run output and provenance, and never refresh
historical hashes or results to manufacture a pass.

## Review result

```markdown
## Skill Evaluation

- Footprint: <typical-path words, agents, external calls, scripts; before/after>
- Comparison: <baseline, tasks, outcome quality and cost per arm>
- Discovery: <positive, boundary, and negative behavior>
- Behavioral invariants: <what was exercised and observed>
- Scope / authorization: <preserved or finding>
- Structural validation: <pass | fail | blocked, with evidence>
- Findings: <ordered by impact, or None>
- Recommended change: <smallest supported correction, or None>
```

Do not declare a skill effective because its YAML parses or its expected
headings exist.
