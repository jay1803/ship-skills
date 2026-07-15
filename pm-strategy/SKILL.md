---
name: pm-strategy
description: >-
  Own product vision, roadmap shape, portfolio priorities, product principles, sequencing, strategic approach, strategic tradeoffs, portfolio balance, and strategic memory. Use when product work needs whole-product direction or a strategy brief before project orchestration; use proj-bet instead when the primary question is go/no-go commitment.
---

# PM: Product Strategy

Own the product portfolio and roadmap layer. Define how the product should pursue a direction: the thesis, roadmap shape, priority order, strategic approach, and tradeoffs before project decomposition or single-issue readiness work begins.

## Boundary

- Own whole-product direction, roadmap priorities, product principles, strategic approach, sequencing, portfolio balance, and strategic memory.
- Validate a strategic candidate before expanding it: separate the user problem from the proposed solution, and judge whether the problem is sufficiently real, painful, frequent, and central to pursue now.
- Route go/no-go commitment decisions, opportunity-cost calls, and kill/continue judgments to `$proj-bet`.
- Route shaped roadmap projects to `$pm-project-orchestrator` for decomposition, milestones, issue setup, dependency maps, and assignment plans.
- Route single-issue clarity to `$pm` and `$pm-readiness-review`. Do not turn this skill into a PRD writer.
- Challenge weak product direction, confused sequencing, unclear target segments, off-thesis roadmap drift, or tradeoffs that would erode user trust.
- Record why strategic direction and roadmap choices were made so future PM and Dev agents do not repeat old debates.

## Workflow

1. Read product thesis, current roadmap, active projects, user/customer evidence, business goals, product principles, known constraints, and prior strategic decisions when available.
2. State the product thesis and current roadmap context in plain product terms.
3. Identify the strategic objective and underlying user problem: what product direction, user segment, business goal, or product principle needs to be advanced, and whether the proposed solution is the right level of ambition now.
4. Shape the strategic approach: target segment, product surface, sequencing, roadmap theme, product principle tradeoffs, and dependency order.
5. Compare viable approaches, including different sequencing, narrower/wider project shapes, research-first paths, maintenance-first paths, or portfolio rebalance. Surface only the 2–5 missing user scenarios that would materially change priority, MVP shape, product fit, trust, retention, learning, or completion.
6. Judge portfolio balance across new features, quality, growth, infrastructure, design debt, user trust, and maintenance.
7. Define the roadmap recommendation: focus areas, priority order, project proposals, dependencies, risks, success signal, and strategic memory.
8. If the unresolved question is whether to commit at all, produce the strategy context and route the go/no-go call to `$proj-bet`.
9. Route shaped projects to `$pm-project-orchestrator` for decomposition.

## Responsibilities

- **Product vision guard**: keep work aligned with the product's core thesis, taste, and product principles.
- **Roadmap planning**: turn product direction into quarterly, monthly, or milestone priorities.
- **Strategic approach**: define the product angle, target segment, wedge, sequencing, and tradeoffs.
- **Priority shaping**: decide which roadmap themes or projects should come first and why.
- **Strategic validation**: pressure-test whether a candidate solves a worthwhile user problem before committing roadmap capacity.
- **Portfolio balance**: balance new features, quality, growth, infrastructure, design debt, and user trust.
- **Strategic memory**: record direction, alternatives, tradeoffs, and revisit conditions.

## Strategy Rules

- Answer "how should the product pursue this direction?" not "should we commit to this bet?"
- Use `$proj-bet` when the primary artifact is a go/no-go one-pager with opportunity cost, confidence, key beliefs, and kill signals.
- Prefer roadmap moves that compound the product thesis, clarify the target user, and reduce future strategic ambiguity.
- Name tradeoffs explicitly: what becomes slower, less polished, less flexible, or less trustworthy if this strategy is chosen.
- Be selective with scenario discovery. Exclude nice-to-have, speculative, enterprise-only-without-evidence, or technically interesting but weak user-value scenarios; name the strongest exclusions and why they wait.
- Prefer the smallest user-visible path to value. Consider scope, opportunity cost, learning value, and reversibility before recommending a roadmap commitment.
- Create project proposals only at the product-project level; child issue decomposition belongs to `$pm-project-orchestrator`.

## Sub-Agent Contract

This skill is safe to run inline or as a bounded sub-agent. When delegated:

- Use only the request, provided sources, and directly referenced roadmap, project, issue, or tracker context.
- Produce the strategy brief and any allowed tracker comment or draft.
- Follow this skill's tracker-write rules; do not edit issue descriptions unless this skill explicitly owns that write.
- Return sources read, writes applied or drafts, blockers, and open questions.

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
