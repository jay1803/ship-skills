---
name: design
description: >-
  Orchestrate design-stage work after product intent is clear. Use when Codex needs to route an approved product brief, PM UX/UI artifact, existing interface, or design request through visual direction, wireframes or variations, a disposable interactive prototype, design-system extraction or refinement, or a design quality review. Keep product behavior in pm-* and production implementation in dev-*.
---

# Design Orchestrator

Turn clear product intent into visual artifacts, reusable system decisions, and review evidence. Own phase selection and Design State; delegate each artifact to the narrow design skill that owns it.

## Boundary

- Require a clear user goal, workflow, and screen-level product requirement before visual execution.
- Route unclear product behavior, scope, states, acceptance criteria, or tracker work to `$pm`, `$pm-ux-state`, or `$pm-ui-design`.
- Own visual direction, exploration artifacts, prototypes, design-system artifacts, and craft review.
- Route production architecture, application code, tests, pull requests, and release work to `$dev` or the relevant platform implementation skill.
- Route slide-deck files to the presentation skill. Route deep motion work to `animation-vocabulary`, `apple-design`, `improve-animations`, or `review-animations` as appropriate.

## Default Paths

- Greenfield visual work: `$design-direction` -> `$design-explore` -> optional `$design-prototype` -> `$design-review`.
- Existing product with a design system: optional `$design-system` extraction/audit -> `$design-explore` -> optional `$design-prototype` -> `$design-review`.
- Design-system work: `$design-system` -> `$design-review`.
- Existing artifact review: `$design-review` directly.

Do not run every worker by default. Load only the next skill required by the requested outcome.

## Operating Workflow

1. Read the supplied brief, PM artifacts, screenshots, brand guidance, design-system sources, and relevant code before asking questions.
2. Confirm the target medium, fidelity, audience, approved behavior, and requested deliverable from available context.
3. Ask only for missing decisions that materially change the artifact. Choose a reasonable default for minor reversible choices and state it.
4. Classify the next artifact and route it to one narrow skill.
5. Maintain Design State across phases. Carry approved decisions forward; do not make later workers rediscover them.
6. Run `$design-review` before stakeholder delivery when the request includes a finished artifact or polish gate.
7. Return artifact links, decisions, evidence, and the next handoff without recapping routine steps.

## Routing

- Need a visual language, typography, palette, density, shape, imagery, or motion direction: use `$design-direction`.
- Need wireframes, visual options, alternate layouts, or substantive variations: use `$design-explore`.
- Need a clickable mockup with real state and feedback: use `$design-prototype`.
- Need tokens, foundations, component inventory, system documentation, or consistency cleanup: use `$design-system`.
- Need accessibility, hierarchy, interaction-state, conformance, generic-aesthetic, or final polish review: use `$design-review`.
- Need a product journey, involved screens, state model, UI requirements, or acceptance criteria: route to PM.
- Need production code: route to Dev.

## Delegation Model

Keep orchestration and Design State in the main agent.

- Delegate bounded source inspection, screenshot inventory, or independent review passes when fresh judgment helps.
- Run artifact writers serially when they touch the same files or canonical design-system source.
- Let `$design-system` be the only design-family skill that writes canonical token or component-system definitions.
- Require delegated workers to return sources read, artifacts created or changed, decisions, verification evidence, blockers, and open questions.

## Design State

Maintain this compact record for multi-phase work:

```markdown
## Design State
- Source brief:
- Product behavior status: clear / needs PM
- Platform and medium:
- Current phase:
- Approved direction:
- Existing system sources:
- Active artifact:
- Review mode: report / fix / final gate
- Decisions carried forward:
- Open blockers:
- Next route:
```

## Handoff

For Dev handoff, provide the approved artifact, selected direction, system/token sources, component and state decisions, responsive or platform differences, accessibility requirements, asset gaps, and unresolved design decisions. Do not replace the PM acceptance criteria or prescribe implementation architecture.
