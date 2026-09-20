---
name: pm-scope
description: Clarify the user problem, desired outcome, and smallest coherent product scope with meaningful non-goals and proposed tradeoffs before specification.
metadata:
  owner: jay1803
  family: product
  maturity: stable
  distribution: product
---

# PM: Scope

Turn an unclear request into a confirmed, buildable product boundary. Keep the
problem, outcome and scope together; do not create separate framing and scope
artifacts merely to document the analysis.

For standalone framing or scoping, use the
[artifact contract](../pm/references/artifact-contract.md) and finish the
requested analysis. For issue work, use the
[state machine](../pm/references/issue-state-machine.md) and
[tracker contract](../pm/references/tracker-contract.md).

## Establish the boundary

Read the original request, current behavior and relevant evidence. Identify
who is affected, what they are trying to do, what blocks them and what observable
outcome would improve. Distinguish facts from assumptions and the requested
outcome from a suggested implementation. Ask only for missing information that
changes the target, product promise or meaningful scope.

Define the smallest complete user- or operator-visible outcome, included
behavior, plausible non-goals, and real tradeoffs. Reuse existing product
mechanisms where they achieve the goal. Do not invent future-proofing rules or
exhaustive non-goals. Split only for independently valuable outcomes, owners,
dependencies, release timing or acceptance boundaries; ordinary design/build/QA
phases and file count are not separate outcomes. Send decomposition drafts to
`$pm-project-orchestrator`; this Skill cannot create children.

Read [technical constraints](../pm-spec/references/technical-constraints.md)
when provider capability, compatibility, data safety or another product-level
constraint could change the boundary. Establish it before specification rather
than saving a predictable product question for engineering closeout.

## Decisions

Compare proposed behavior with the original request, verified inherited
behavior and user-confirmed decisions. Use
[decision provenance](../pm-spec/references/decision-provenance.md) when the
source is unclear. Show any new material product rule as a Decision Delta with
its source, impact and recommendation; do not silently convert it to a
requirement. Engineering invariants stay engineer-owned unless they change
observable behavior. Honor already-delegated discretion within its bounds.

An unresolved material delta pauses dependent writing and review, not independent
analysis. When the user resolves it, record the answer and source under the
existing PM root, update the existing scope artifact if one exists, then
continue. No downstream blocked receipt is needed for the same pending question.

## Result and next owner

Return the outcome, evidence basis, smallest scope, meaningful non-goals and any
unresolved decision. A framing-only request can stop at the clarified problem.
For a lifecycle request, apply the state machine's Solution Review criteria:
use `$pm-solution-review` when a material rule or simplification judgment remains;
otherwise proceed to `$pm-spec`. Resolve needed interaction/screen design through
`$design`, retaining PM ownership of product policy.

The controller may consume this result inline. Publish a `## Scope` reply only
when there is a material decision, tradeoff or supporting evidence to preserve;
update its existing comment ID on revision. Do not repeat the canonical issue,
write a placeholder artifact, edit title/description or change metadata.
