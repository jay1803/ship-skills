---
name: pm-solution-review
description: Review a confirmed product solution for unnecessary complexity and unsupported rules while preserving its goal. Excludes strategy, design, and code review.
metadata:
  owner: jay1803
  family: product
  maturity: stable
  distribution: product
---

# PM: Solution Review

Find the simplest product solution that fully achieves the already-confirmed
goal. Treat product direction, target outcome, and the decision to invest as
fixed inputs, not questions to reopen. Use this Skill when explicitly requested
or when the shared state machine identifies a material rule/simplification
question. A non-Bug label alone does not require this review. Reuse existing
review evidence after verifying unchanged inputs.

For issue lifecycle work, apply the shared [Issue PM State Machine](../pm/references/issue-state-machine.md),
including its downstream entry guard and single stage-comment identity.

For a standalone analysis or draft, follow the
[Product Artifact Contract](../pm/references/artifact-contract.md) and complete
the requested artifact without tracker setup. The tracker steps below apply
only to an issue-bound lifecycle or authorized publication.

Review prerequisites below use the shared state-machine freshness and explicit
user-override rules. A disclosed skip is not an approval and never resolves an
unconfirmed product decision.

## Preconditions

- Bind an issue review to its verified PM root and current candidate. A
  standalone review uses the supplied artifact without tracker setup.
- Require a confirmed problem, target user or operator, desired outcome, product
  direction, and candidate scope. If direction or investment value is unsettled,
  stop and route to `$pm-strategy`; require an explicit user commitment decision
  before reviewing a solution.
- Read the original request, confirmed decisions, inherited behavior, problem
  framing, scope artifact, and the existing product mechanisms the proposal
  could reuse.
- Review a stable candidate before canonical writing when this gate applies.
  Existing equivalent scope evidence is sufficient. Missing or invalidated
  applicable review runs before readiness unless the state machine permits an
  explicit omission. Restoring established Bug behavior does not need this
  review; newly proposed behavior remains a separate product decision.
- If Scope or another upstream stage owns an unresolved Decision Delta, return
  `upstream_blocked` to the PM controller with that owner and required user
  decision. Do not perform the review and do not post a Product Solution Review
  comment.

## Review Boundary

Review only how the product should achieve the confirmed goal:

- whether every proposed capability directly contributes to that goal;
- whether product concepts, rules, modes, settings, roles, surfaces, or
  exceptions can be removed;
- whether the proposal can extend an existing canonical product mechanism
  instead of creating a parallel path;
- whether one simpler product rule or ownership choice can eliminate several
  special cases: a product-judo move;
- whether future-proofing, configurability, optionality, or generalization adds
  obligations not required by the confirmed goal;
- whether adjacent outcomes have entered the proposal without being necessary;
- whether critical acceptance proves the goal without turning the first version
  into a broader platform capability.

Explicitly exclude:

- product direction, roadmap priority, opportunity cost, and go/no-go value;
- UI, interaction, visual treatment, journey states, and design quality;
- security, privacy, abuse, trust, compliance, and safety review;
- project sequencing, staffing, rollout, reversibility, learning plans, and
  delivery management;
- technical architecture, APIs, data models, implementation, testing strategy,
  and code quality.

Route an excluded concern to its owning review instead of using it to pass or
fail this gate.

## Rule and Constraint Audit

Audit every material product rule or constraint in the candidate issue,
including defaults, limits, thresholds, timeouts, retention, automatic actions,
fallbacks, visibility, permissions, irreversible effects, compatibility choices,
and scope cuts. For each, record one provenance class and its exact source:

- `User confirmed`: the user explicitly approved this rule.
- `Inherited behavior`: a verified current contract establishes it.
- `Engineering invariant`: a cited non-observable correctness or safety need.
- `Agent proposal`: the rule was authored or materially expanded by an agent
  without the preceding sources.

Test whether each rule is necessary for the confirmed goal. Recommend removal
of rules that do not materially support it; do not edit the reviewed scope. Do not retain an agent-authored product rule merely
because it sounds prudent or appears in an otherwise complete issue. If an
`Agent proposal` changes observable behavior, keep it out of approval, publish
it as a Decision Delta, and stop for the user's confirmation. A review may
recommend deleting it without confirmation when deletion preserves the confirmed
goal.

## Finding Bar

A simplification finding is valid only when all of these are true:

1. It preserves the confirmed direction, target user, and product outcome.
2. It identifies concrete product complexity in the current proposal.
3. It offers a specific smaller solution, not a preference or vague request to
   rethink the feature.
4. It demonstrates how the smaller solution still achieves the complete goal.
5. It materially removes scope, concepts, rules, product surfaces, or ongoing
   product obligations.

Do not block because a reviewer prefers another design. Do not expand the
solution in the name of completeness. Prefer deleting complexity over moving it
between requirements.

## Decision Rules

- `approve`: no concrete, materially simpler same-goal solution remains, and
  every retained material rule is necessary and traceable to a valid source.
- `simplify`: at least one high-confidence finding can materially reduce product
  complexity while preserving the goal.
- `blocked`: the confirmed goal, direction, candidate scope, provenance, or
  required issue evidence is unavailable or contradictory, including an
  unconfirmed material Agent proposal that cannot simply be removed.

When the decision is `simplify`, classify the recommended change as an `Agent
proposal` in the Decision Delta. Route to user confirmation, then `$pm-scope`
to refresh the candidate solution and rerun this review. Do not advance to
`$pm-spec` until the latest review is `approve`.

## Tracker Writes

- Do not edit the issue title or description; `$pm-spec` remains the canonical
  writer.
- Do not change labels, status, priority, assignee, project, milestone, or issue
  relationships.
- Reply with the review under the existing PM workflow root using the heading
  `## Product Solution Review`. Create it only on the first legal run; later
  runs update that comment by ID. Never add a same-stage `Supersedes` reply or
  another top-level PM comment.
- If tracker tools or threaded replies are unavailable, return the exact reply
  draft without claiming it was posted.

## Output

```markdown
## Product Solution Review

Decision: <approve | simplify | blocked>
Confidence: <high | medium | low>

### Confirmed Goal
- <Direction, target user/operator, and outcome held fixed by this review.>

### Current Product Solution
- <Concise description of the candidate solution being reviewed.>

### Rule and Constraint Audit
| Rule / Constraint | Necessary for Goal? | Provenance and Source | Result |
| --- | --- | --- | --- |
| <material rule, or `None`> | <yes / no> | <User confirmed / Inherited behavior / Engineering invariant / Agent proposal, with source> | <retain / remove / Decision Delta> |

### Simplification Findings
1. <Concrete product complexity, or `None`.>
   - Simpler solution: <specific smaller solution>
   - Same-goal proof: <why the confirmed outcome remains complete>
   - Scope removed: <capabilities, concepts, rules, modes, settings, or surfaces>

### Product-Judo Opportunity
- <One underlying product rule that can eliminate several special cases, or `None`.>

### Decision Delta
- <Agent proposal requiring confirmation, or `None`.>

### Recommended Next Step
<Use `$pm-spec` when the canonical issue needs synthesis or a rewrite; for a verified complete existing record, use `$pm-readiness-review` when approved. Otherwise user confirmation -> `$pm-scope` -> rerun `$pm-solution-review`, or an exact blocker owner.>
```
