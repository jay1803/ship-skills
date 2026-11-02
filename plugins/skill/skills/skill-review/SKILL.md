---
name: skill-review
description: Independently assess a frozen agent Skill, Skill change or Skill family for useful decisions, footprint and necessity, discovery, authorization, execution and completion behavior. Use for Skill design and behavioral acceptance or a whole-Skill over-design audit, not ordinary code-only PR review, session-cost audits, fixes or publication.
metadata:
  owner: jay1803
  family: skill
  maturity: experimental
  distribution: skill
---

# Skill Review

Judge whether a Skill causes the right decisions at a cost it earns, and what
evidence supports that. Keep the reviewed source, repository and external
systems read-only; a review request does not authorize fixes, issue changes,
posting, publication, installation, paid provider calls or replay of private
sessions. Use a fresh context without the author's reasoning or prior verdicts;
if that is unavailable, label the assessment non-independent rather than
claiming a gate passed.

## Modes and target

- **Change review** judges one change: a PR or base/head pair with an
  unambiguous repository, or a design draft at its content digest.
- **System audit** judges a whole Skill or Skill family at a recorded revision.
  Use it when asked, when a Skill has accumulated many revisions, or when a
  change review finds accumulation signs; recommend it rather than silently
  widening a change review.

Bind supporting references, scripts and representative consumers along with
`SKILL.md`. Governing authority is the original request, explicit host policy
and designated requirements; separate them from defaults, examples and reviewer
preferences, and never elevate an author's preferred output or a historical
incident into a requirement. Missing authority blocks only the affected
judgment.

## Method

Apply each step to the changed path and its direct consequences in a change
review, and to the whole target in a system audit. The
[rubric](references/review-rubric.md) holds the questions for each surface.

1. **Job:** state the primary job and the realistic positive and nearby
   negative requests.
2. **Footprint:** measure what a typical request reads before the agent acts,
   the agents it dispatches, its external or paid calls and its scripts; for a
   change, the delta.
3. **Minimal alternative:** derive the simplest design that meets the same
   requirements, and compare an official or comparable implementation when one
   exists.
4. **Justify the difference:** every element beyond that alternative
   (instruction, reference, agent, external call, script, evidence mechanism or
   state) must name the failure it prevents, with evidence or a concrete
   scenario, under the rubric's necessity and cost questions; otherwise it is a
   finding whose correction is usually deletion.
5. **Behavior:** discovery, authority, execution and completion under the
   rubric, using comparative evaluation for material claims.

For independent forward evaluation, give the evaluator the frozen Skill and
minimum raw inputs without expected outcomes, suspected defects or the
authoring conversation, and judge its output against criteria held separately.
Observation-only review does not authorize an external operation; read the
[execution contract](../skill-patterns/references/execution-contract.md) before
any authorized execution and keep a writing evaluator separate from this
reviewer. Keep structural checks, manual audits, supplied-answer tests,
independent simulations, real execution and provider calls distinct, and never
invent telemetry. A missing test is an evidence gap for its claim, not proof of
a defect.

## Judgment

```markdown
## Skill Review

- Target / mode / authority: <identity, change review or system audit, governing sources>
- Footprint: <typical-path words, agents, external calls, scripts; delta for a change>
- Minimal alternative: <one paragraph, and any reference implementation compared>
- Findings: <location, behavior, impact, smallest correction; ordered by impact>
- Evidence gaps: <unverified claim and missing condition>
- Decision: <findings | needs-evidence | no-findings | stale>
```

Each finding needs a source location, observed or demonstrable behavior,
practical impact (including recurring cost) and the smallest supported
correction. Hypotheses stay hypotheses. If findings and gaps coexist, keep
both. `no-findings` is scoped to the evidence inspected; it is not approval to
merge or a claim that omitted execution occurred.

Before delivering, verify the target is still the reviewed revision or digest;
a changed relevant target makes the result `stale`. Return findings to the
author or `skill-dev` without repairing, posting or changing tracker state.
