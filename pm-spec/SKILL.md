---
name: pm-spec
description: >-
  Write execution-ready product specs, PRDs, user stories, requirements, acceptance criteria, decision records, and tracker-ready issue content. Use after the problem and scope are clear enough to hand to engineering, or when the current conversation should be synthesized into a PRD without another interview; this is the PM skill that owns updating the canonical issue description.
---

# PM: Spec

Produce the main PM handoff artifact for development.

## Workflow

1. Read the original issue description, title, labels, status, priority, assignee, comments, attachments, linked context, and any available docs.
2. Read prior PM comments before writing, especially `$pm-intake`, `$pm-problem-framing`, `$pm-scope`, `$pm-ux-state`, `$pm-ui-design`, `$pm-data-analytics`, `$pm-technical-boundary`, and `$pm-backlog` artifacts.
3. Verify the problem, user, goal, scope, non-goals, constraints, and edge-case decisions from the issue plus comments.
4. If a material decision is missing, ask before writing a spec that would hide ambiguity.
5. Write requirements as observable product behavior, not implementation tasks.
6. Include acceptance criteria that a developer and QA reviewer can verify.
7. Update the canonical issue description when tracker tools allow. This is the only PM skill in the default chain that should rewrite the existing issue description.
8. For the default dev-ready workflow, route next to `$pm-technical-boundary` after the spec is written so product-level constraints are explicit before readiness review.
9. If writing back to Linear with tools, assign the issue to the current/requesting user when identity is known and add the `scoped` label. Create or verify the label if tools allow and it is missing.

## Conversation-to-PRD Mode

Use this path when the user asks to turn the current conversation, notes, prototype, or already-discussed product idea into a PRD.

- Synthesize from the current conversation, directly referenced docs, repo context, and tracker context if present. Do not run a broad interview just to fill every template section.
- Explore the repo only enough to use the project's domain language, understand the current product shape, and respect relevant ADRs or local conventions.
- Ask only when a missing decision would change the target user, scope, product promise, release boundary, or validation seam. Otherwise write the assumption explicitly.
- Identify the highest practical testing seam for the change. Prefer existing seams over new ones, and prefer fewer seams that verify external behavior. If the seam choice itself changes scope or architecture, confirm it before publishing.
- If the user asks to publish and tracker tools allow, create or update the tracker-ready product record using this skill's write authority. Use normal PM metadata rules instead of bypassing intake/readiness semantics.

## Spec Rules

- Preserve exact user wording when it defines product intent.
- Use the project's domain glossary and existing product vocabulary when repo context is available.
- Include material edge cases and recommended resolutions; do not dump a generic checklist.
- Keep implementation details out unless they are product-level constraints.
- Include implementation decisions only when they are already decided, constrain product behavior, or define a contract engineers must preserve.
- Do not include file paths or code snippets in the spec. Exception: a prototype may contribute a small decision-rich snippet when prose would be less precise; trim it to the state shape, reducer, schema, or contract being decided.
- Cover user stories deeply enough to represent the important actors, flows, and outcomes, without padding the spec.
- Mark uncertainty explicitly as assumptions or open questions.
- If there are no open questions, write "None."

## Description Write Authority

- Own the final dev-ready issue description.
- Do not write the description from only the current prompt. Read the issue description and all relevant PM comments first.
- Synthesize prior comments into a clean product record; remove duplication and preserve decisions.
- If prior PM comments conflict, call out the conflict and ask for a decision instead of silently choosing.
- If tracker tools are unavailable, provide the exact replacement issue description and state that it still needs to be applied.
- Comments from earlier PM steps are working notes. The issue description written by `$pm-spec` is the canonical product handoff.

## Sub-Agent Contract

This skill is safe to run inline or as a bounded sub-agent. When delegated:

- Use only the request, provided sources, prior PM comments, and directly referenced tracker context.
- Produce the canonical product requirement and, when tools allow, the issue-description update this skill owns.
- Follow this skill's tracker-write rules; do not run concurrently with other PM writers on the same issue.
- Return sources read, writes applied or drafts, blockers, and open questions.

## Output

```markdown
## Product Requirement

### Problem
<The user or business problem in one or two paragraphs.>

### Target User
<Who this is for and when they need it.>

### Goal
<The outcome we are trying to create.>

### User Story
As a <user>, I want <capability>, so that <outcome>.

### In Scope
- <Included behavior or deliverable.>

### Out of Scope
- <Excluded behavior or deferred idea.>

### User Experience / Behavior
- <Specific behavior visible to the user or operator.>

### Requirements
- <Observable product requirement.>

### Acceptance Criteria
- Given <context>, when <action>, then <observable result>.

### Testing / Validation
- <Highest practical seam, prior art in the codebase, and what external behavior must be verified.>

### Edge Cases / Suggested Resolutions
- <Material edge case, recommended handling, and whether it is in scope, deferred, or intentionally ignored.>

### Decisions / Product Constraints
- <Decision made, product-level implementation constraint, or externally visible contract, and why.>

### Open Questions
- <Only unresolved questions that still matter, or "None.">

### Risks / Dependencies
- <Risk, dependency, or external constraint.>

### Recommended Next Step
<Usually `$pm-technical-boundary` for the default dev-ready workflow; otherwise name the blocking PM step or readiness review.>
```
