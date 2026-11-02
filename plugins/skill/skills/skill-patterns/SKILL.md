---
name: skill-patterns
description: Select and review the smallest effective architecture for an agent skill in Codex or Claude Code. Use when deciding whether a skill should be atomic, procedural, artifact-generating, routing, orchestrating, review-gating, or domain-guided; when decomposing an oversized skill; when binding an archetype to a client's invocation policy, isolation, tool scope, or auto-loading; or when reviewing discovery boundaries, ownership, and validation. Do not use to discover or install existing skills, or to scaffold skill files, which the environment's skill-creation workflow owns.
metadata:
  owner: jay1803
  family: skill
  maturity: stable
  distribution: skill
---

# Skill Patterns

Design the smallest skill that changes what a capable agent would otherwise get
wrong. Every instruction, reference, script, extra agent and external call costs
context, time or money on every use, so each one stays only when it prevents a
real failure. The archetypes are client-neutral; how Codex or Claude Code
implements one is a separate binding decision.

## Principles

1. **Earn the footprint.** A skill's footprint is what an agent reads before
   acting on a typical request (`SKILL.md` plus the references that path always
   loads), the agents it dispatches, its external or paid calls, and its
   scripts. Keep an element only when it prevents a demonstrated or concretely
   foreseeable failure. Judge the whole loading path, not one file's length.
2. **Default to the running agent.** It is capable and already holds the
   context. Add an external model, classifier, script or extra agent only when
   it beats the agent on determinism, independence, cost or calibration, and
   say what shows that. Bookkeeping such as hashes, receipts or ledgers must
   establish the fact it claims; if it cannot, it is ceremony.
3. **Write outcomes and criteria, not procedures and prohibitions.** Use fixed
   steps only where order is fragile or authorization depends on it, and
   prohibitions only for safety and authorization. Keep each rule in one place.
4. **Keep called skills stateless.** Budgets, ledgers, retries and cross-run
   state belong to the orchestrator that owns the lifecycle; a called skill
   returns the facts of its run through a small interface.
5. **Change by subtraction.** Before adding a rule, look for one to delete,
   generalize or replace. A fix replaces a rule rather than stacking an
   exception. Do not keep version-compatibility layers for ephemeral artifacts.
6. **Prove value by comparison.** Compare a new or substantially changed skill
   with no skill or the previous version on the same realistic tasks, for both
   outcome quality and cost; see [evaluation](references/evaluation.md).
7. **Preserve intent and authority.** A skill may guide an action but never
   grants permission for an external mutation; an authorization check is a
   scope comparison, not a new question (see the
   [authorization check](references/archetypes.md#authorization-check)).
8. **Stay client-neutral.** Name a client only where its mechanism differs,
   and never let a safety or authorization boundary depend on a field only one
   client honors.

## Scope

This skill owns architecture selection, client binding, and design review. The
environment's skill-creation workflow owns scaffolding, supported metadata and
structural validation; apply both when creating or substantially revising a
skill. Guidance that belongs in repository instructions, a hook, CI or a
subagent is [not a skill](references/archetypes.md#not-a-skill). How a change
is tracked, reviewed and merged belongs to the host repository's policy.

## Workflow

1. Name realistic requests that should trigger the skill and nearby ones that
   should not, then state its primary job in one sentence. Split unrelated jobs.
2. Sketch the minimal alternative first: what a capable agent does with no
   skill or a one-paragraph instruction, and which failures that version makes.
   The design exists to prevent those failures and nothing else.
3. Select one primary archetype from [archetypes](references/archetypes.md);
   add a secondary pattern only for the same primary job.
4. Read [client bindings](references/client-bindings.md) only when a target
   client needs explicit-only invocation, isolation, tool scope, file-scoped
   loading or arguments. A skill needing only name, description and body ships
   without `agents/openai.yaml`.
5. Choose the minimum resources: shared purpose, invariants and completion in
   `SKILL.md` with invariants early (compaction may keep only the start);
   conditional detail in `references/` with a stated reading condition;
   `scripts/` only for deterministic repeated work; `assets/` only for files
   copied into output.
6. Draft a discriminating description: capability and key use case in the
   first sentence, positive triggers next, and only the exclusion needed to
   prevent likely misrouting. Descriptions share a truncated listing budget.
7. For external operations, approval gates or model-controlled decisions, read
   the [execution contract](references/execution-contract.md); it starts by
   asking whether they are needed at all.
8. Audit every mandatory rule, prohibition, gate, default or limit. Keep it
   only when it has a source (a user request, a verified repository or
   external source, or a safety, authorization or fragility rationale), it
   prevents a demonstrated or concretely foreseeable failure, and it lives in
   one place. Try to satisfy a requested fix by generalizing or replacing an
   existing rule first. Label any other constraint as a proposal and confirm
   it with the user; do not hide one in an example, template or reference.
9. Validate under [evaluation](references/evaluation.md), and implement through
   the skill-creation workflow when implementation is requested.

## Architecture Decision

Before implementation, provide or internally establish:

```markdown
## Skill Architecture

- Primary job: <one sentence>
- Primary archetype: <atomic | procedure | artifact | router | orchestrator | review-gate | domain-guide>
- Trigger examples / exclusions: <representative and near-miss requests>
- Minimal alternative: <what the simplest version does and the failures it makes>
- Structure: <files and the failure each prevents>
- Footprint: <words read before acting on a typical request; agents; external calls; scripts>
- Client bindings: <per target client, or none>
- Ownership and state: <canonical writes, who holds cross-run state, external destinations and authority, or none>
- Validation: <structural checks, comparative behavior and cost evidence>
- Deferred complexity: <resources or modes not justified yet>
```

Keep the brief proportional; it is a decision aid, not an extra deliverable.
Separate requirements, defaults, recommendations and examples, and keep
canonical write authority and handoff ownership explicit when several skills
touch one workflow.
