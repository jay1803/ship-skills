---
name: pm-backlog
description: Draft independently valuable issue slices and dependencies from stable product scope. Hand authorized tracker creation to pm-project-orchestrator.
metadata:
  owner: jay1803
  family: product
  maturity: stable
  distribution: product
---

# PM: Backlog

Convert stable scope into a clean issue tree.

For a standalone analysis or draft, follow the
[Product Artifact Contract](../pm/references/artifact-contract.md) and complete
the requested artifact without tracker setup. The tracker steps below apply
only to an issue-bound lifecycle or authorized publication.

## Boundary

- Own issue-tree quality: independently understandable slices, duplicate detection, follow-ups, dependency edges, proposed milestone assignments, and tracker-ready ticket shape.
- Do not decide product strategy, project commitment, or the
  v1/deferred/rejected cutline. Route strategy evidence to `$pm-strategy` and
  require the user to confirm commitment or cutline decisions.
- Always return a draft. Do not edit project descriptions, milestones,
  membership, project dependencies, or other project-level fields.
- Do not create or update child, follow-up, parent, sibling, dependency, or
  related issue records, even when the user requests the write directly. Return
  the exact tracker-ready draft and name `$pm-project-orchestrator` as the owner
  of any live multi-issue mutation.
- Do not rewrite existing child issue descriptions; route canonical per-issue specification changes to `$pm-spec`.

## Workflow

1. Read existing tracker context when available so you do not duplicate issues or break dependency order.
2. Read the source plan, spec, PRD, playbook, conversation, workflow capture, or existing issue before drafting slices.
3. Confirm the parent outcome and split only when each child remains independently understandable and testable.
4. Keep child tickets as vertical product slices, not lifecycle phases. A materially necessary deferred human acceptance deliverable is the exception defined by Acceptance Classification; keep it outside the engineering completion barrier.
5. Propose dependencies, follow-ups, labels, owners, and milestone assignments when the destination tracker is clear.
6. For every proposed issue, decide whether a person must exercise or approve the delivered result beyond automated checks, developer-run manual QA, PR Product Review, or external technical review. When required, include `human-acceptance-required` plus executable human acceptance instructions.
7. Return every proposed child/follow-up issue and relationship as a draft. Do
   not apply tracker mutations from this Skill. When the user asks for live
   creation or updates, preserve the request in the handoff to
   `$pm-project-orchestrator` instead of emulating that controller.

Apply [Acceptance Classification](../pm-spec/references/acceptance-policy.md)
to every draft and preserve that distinction in the live-write handoff. In
standard delivery, suggested real-environment tests do not gate implementation.
Reuse or draft a separate human-owned acceptance ticket only when materially
necessary or requested; it can depend on implementation, never block it or its
successors. Do not create a ticket merely to enumerate routine skipped tests.

## Ticket Rules

- Each ticket should include problem, scope, out of scope, acceptance criteria, and notes.
- Tickets requiring a person to accept the result must include the exact `human-acceptance-required` label and a Human Acceptance section covering environment/build, tester or role, prerequisites, numbered steps, expected results, evidence, and acceptance-result fields to be completed in the PM thread.
- Do not use the human acceptance label for ordinary automated validation, developer-run manual QA, PR Product Review, or external technical review alone.
- Split by release timing, risk, dependency, owner, or acceptance criteria differences.
- Keep research/spike tickets separate only when they unblock later build slices.
- Add follow-up tickets for deliberately deferred work.
- Do not create duplicate tickets for the same user outcome.
- Use clear verbs: Add, Support, Show, Prevent, Notify, Track, Migrate, Document.
- Prefer thin vertical slices that produce a demoable or verifiable result. If a small prefactor makes later slices simpler, put that ticket first and explain the dependency.

## Skill Backlog Mode

For reusable Skill or playbook work, read
[skill-backlog.md](references/skill-backlog.md). Ordinary product slicing does
not need that reference.

## Output

```markdown
## Backlog Draft

Write Status: draft only
Product Writes: none
Required Next Owner: <$pm-project-orchestrator for live writes, or none>

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
   Required Acceptance Criteria:
   - Given <context>, when <action>, then <observable result>.
   Nonblocking Recommendations:
   - <P2/P3 recommendation and deferred status; omit when empty.>
   Validation:
   - <Command, review step, or evidence expected.>
   Human Acceptance:
   - <Not required, or label + environment/build + tester/role + prerequisites + numbered steps + expected results + evidence + accepted-by/date fields recorded in the PM thread when completed.>
   Dependencies:
   - <Dependency or "None.">
   Notes:
   - <Decision, edge case, label, owner, skill resource, deprecation, or follow-up.>

### Follow-Ups
- <Deferred ticket or "None.">
```
