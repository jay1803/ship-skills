---
name: pm-backlog
description: >-
  Break product work into clean backlog structure. Use for Linear parent issues, child tickets, subtasks, dependencies, milestones, follow-ups, duplicate checks, tracker-ready issue trees, and turning skill ideas, playbooks, or workflow captures into skill-building backlog slices.
---

# PM: Backlog

Convert stable scope into a clean issue tree.

## Workflow

1. Read existing tracker context when available so you do not duplicate issues or break dependency order.
2. Read the source plan, spec, PRD, playbook, conversation, workflow capture, or existing issue before drafting slices.
3. Confirm the parent outcome and split only when each child remains independently understandable and testable.
4. Keep child tickets as vertical product slices, not lifecycle phases.
5. Add dependencies, follow-ups, labels, owners, and milestones when the destination tracker is clear.
6. Create or update Linear issues only when the user asked for tracker changes and the destination is clear. Assign created issues to the current/requesting user when identity is known.

## Ticket Rules

- Each ticket should include problem, scope, out of scope, acceptance criteria, and notes.
- Split by release timing, risk, dependency, owner, or acceptance criteria differences.
- Keep research/spike tickets separate only when they unblock later build slices.
- Add follow-up tickets for deliberately deferred work.
- Do not create duplicate tickets for the same user outcome.
- Use clear verbs: Add, Support, Show, Prevent, Notify, Track, Migrate, Document.
- Prefer thin vertical slices that produce a demoable or verifiable result. If a small prefactor makes later slices simpler, put that ticket first and explain the dependency.

## Skill Backlog Mode

Use this mode when the source is a skill idea, a reusable workflow, a playbook-to-skill conversion, a Record & Replay capture, or a request to turn repeated work into skill-building tickets.

1. Extract the workflow before splitting it: trigger phrases, source inputs, expected outputs, tools used, file/resource types, user corrections, edge cases, and validation evidence.
2. Decide whether the work belongs in a new skill, an existing skill, or no skill. Prefer updating an existing skill when the behavior shares the same trigger surface or workflow model.
3. Avoid over-splitting. If several candidate skills would duplicate the same model or reference material, create one skill with references/assets instead of several thin wrappers.
4. Plan reusable resources explicitly: `SKILL.md` changes, `references/`, `scripts/`, `assets/`, examples/evals, install or alias updates, and validation commands.
5. Split skill work into independently reviewable tickets, usually in this order:
   - Capture source workflow and decide the target skill boundary.
   - Scaffold or update the skill entrypoint and agent metadata.
   - Add references, assets, or scripts that carry reusable knowledge.
   - Add or update examples/evals when the workflow is complex enough to regress.
   - Validate the skill, test representative scripts, and document tracker-ready evidence.
   - Migrate callers or aliases, then remove obsolete wrappers only after the canonical route is discoverable.
6. Each skill-building ticket must state the target skill, source material, resource changes, acceptance criteria, validation command, dependency, and rollback/deprecation note when relevant.

## Sub-Agent Contract

This skill is safe to run inline or as a bounded sub-agent. When delegated:

- Use only the request, provided sources, and directly referenced tracker context.
- Produce the backlog artifact and any allowed tracker updates or drafts.
- Follow this skill's tracker-write rules; do not edit issue descriptions unless this skill explicitly owns that write.
- Return sources read, writes applied or drafts, blockers, and open questions.

## Output

```markdown
## Backlog Structure

### Parent
Title: <Outcome-oriented title>
Problem: <Why this exists.>

### Child Issues
1. Title: <Verb-led user-visible outcome>
   Problem: <Why this ticket exists.>
   Source: <plan/spec/playbook/workflow capture/issue or "Current conversation">
   Scope:
   - <Included behavior.>
   Out of Scope:
   - <Excluded behavior.>
   Acceptance Criteria:
   - Given <context>, when <action>, then <observable result>.
   Validation:
   - <Command, review step, or evidence expected.>
   Dependencies:
   - <Dependency or "None.">
   Notes:
   - <Decision, edge case, label, owner, skill resource, deprecation, or follow-up.>

### Follow-Ups
- <Deferred ticket or "None.">
```
