---
name: pm-strategy
description: Shape product direction, roadmap priorities, and evidence-backed investment recommendations before project commitment.
metadata:
  owner: jay1803
  family: product
  maturity: stable
  distribution: product
---

# PM: Product Strategy

Own the product portfolio and roadmap layer. Define how the product should pursue a direction: the thesis, roadmap shape, priority order, strategic approach, and tradeoffs before project decomposition or single-issue readiness work begins.

For a standalone analysis or draft, follow the
[Product Artifact Contract](../pm/references/artifact-contract.md) and complete
the requested artifact without tracker setup. The tracker steps below apply
only to an issue-bound lifecycle or authorized publication.

## Boundary

- Own whole-product direction, roadmap priorities, product principles, strategic approach, sequencing, portfolio balance, and strategic memory.
- Validate a strategic candidate before expanding it: separate the user problem from the proposed solution, and judge whether the problem is sufficiently real, painful, frequent, and central to pursue now.
- For go/no-go commitment, opportunity-cost, and kill/continue questions,
  produce the evidence, recommendation, key beliefs, and kill signals, then ask
  the user for the decision.
- Return shaped roadmap projects as structured proposals to
  `$pm-project-orchestrator`. Do not decompose them, set up milestones, or apply
  project-level tracker writes inside this strategy skill.
- Route single-issue clarity to `$pm` and `$pm-readiness-review`. Do not turn this skill into a PRD writer.
- Challenge weak product direction, confused sequencing, unclear target segments, off-thesis roadmap drift, or tradeoffs that would erode user trust.
- Record why strategic direction and roadmap choices were made so future PM and Dev agents do not repeat old debates.

## Workflow

1. Read product thesis, current roadmap, active projects, user/customer evidence, business goals, product principles, known constraints, and prior strategic decisions when available.
2. State the product thesis and current roadmap context in plain product terms.
3. Identify the strategic objective and underlying user problem: what product direction, user segment, business goal, or product principle needs to be advanced, and whether the proposed solution is the right level of ambition now.
4. Shape the strategic approach: target segment, product surface, sequencing, roadmap theme, product principle tradeoffs, and dependency order.
5. Compare viable approaches, including different sequencing, narrower/wider project shapes, research-first paths, maintenance-first paths, or portfolio rebalance. Surface only missing user scenarios that would materially change priority, MVP shape, product fit, trust, retention, learning, or completion.
6. Judge portfolio balance across new features, quality, growth, infrastructure, design debt, user trust, and maintenance.
7. Define the roadmap recommendation: focus areas, priority order, project proposals, dependencies, risks, success signal, and strategic memory.
8. If the unresolved question is whether to commit at all, produce the strategy
   context and go/no-go recommendation, then stop for the user's decision.
9. Route shaped projects to `$pm-project-orchestrator`; route only an exact,
   already-selected single issue to `$pm`.

## Responsibilities

- **Product vision guard**: keep work aligned with the product's core thesis, taste, and product principles.
- **Roadmap planning**: turn product direction into quarterly, monthly, or milestone priorities.
- **Strategic approach**: define the product angle, target segment, wedge, sequencing, and tradeoffs.
- **Priority shaping**: decide which roadmap themes or projects should come first and why.
- **Strategic validation**: pressure-test whether a candidate solves a worthwhile user problem before committing roadmap capacity.
- **Portfolio balance**: balance new features, quality, growth, infrastructure, design debt, and user trust.
- **Strategic memory**: record direction, alternatives, tradeoffs, and revisit conditions.

## Strategy Rules

- Answer both "how should the product pursue this direction?" and, when asked,
  "should we commit?" The Agent recommends; the user decides commitment.
- Prefer roadmap moves that compound the product thesis, clarify the target user, and reduce future strategic ambiguity.
- Name tradeoffs explicitly: what becomes slower, less polished, less flexible, or less trustworthy if this strategy is chosen.
- Be selective with scenario discovery. Exclude nice-to-have, speculative, enterprise-only-without-evidence, or technically interesting but weak user-value scenarios; name the strongest exclusions and why they wait.
- Prefer the smallest user-visible path to value. Consider scope, opportunity cost, learning value, and reversibility before recommending a roadmap commitment.
- Create project proposals only at the product level. Return them as structured
  handoff artifacts for `$pm-project-orchestrator`; do not perform child-issue
  decomposition or project setup in this skill.

## Output

```markdown
## Product Strategy Brief

Product thesis:
Current roadmap context:
Strategic objective:
Target user/segment:
Requirement validity:
Product principles:
Recommended approach:
Valuable missing scenarios:
Deliberately excluded:
Roadmap shape:
Priority order:
Sequencing rationale:
Portfolio balance:
Tradeoffs:
Dependencies:
Risks / constraints:
Success signal:
Projects to shape:
Research / evidence needed:
Strategic memory:
Next route:
```
