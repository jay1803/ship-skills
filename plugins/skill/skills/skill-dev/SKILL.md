---
name: skill-dev
description: Create or revise an agent Skill from an authorized design, implement its resources, and obtain evidence for the decisions it changes. Use for Skill authoring and validation, not design-only advice, independent review, or installing existing Skills.
metadata:
  owner: jay1803
  family: skill
  maturity: experimental
  distribution: skill
---

# Skill Development

Deliver the smallest coherent Skill change that achieves its intended behavior,
with evidence. Preserve user scope, existing work and the host repository's
issue, branch, review and delivery policy. Authoring a Skill does not grant
publication, consumer installation, external data transfer or production
writes.

## Establish the change

Read the existing Skill, its references, callers and packaging before editing,
and search for an existing owner before adding a Skill. For a new or substantial
design, use [skill-patterns](../skill-patterns/SKILL.md) to settle the primary
job, requests, exclusions, minimal alternative, footprint, bindings and
completion conditions; a narrow correction can reuse that design.

Use the environment's `skill-creator` workflow for metadata, scaffolding and
structural validation, reading its current instructions rather than copying
templates. If it is unavailable, report that and use an equivalent documented
path when the task and host policy permit.

## Implement by subtraction

Measure the footprint before and after the change. Satisfy the request by
deleting, generalizing or replacing existing text first; add only what prevents
a failure the current Skill makes. Keep one canonical instruction per decision,
conditional guidance in linked references and only deterministic repeated work
in scripts. Do not add a router, evaluator service, extra agent or external
classifier for ordinary authoring. For an external operation or model decision,
apply the
[execution contract](../skill-patterns/references/execution-contract.md),
starting with whether it is needed.

## Verify

Select evidence with [evaluation](../skill-patterns/references/evaluation.md).
Wording-only changes need a diff audit and structural checks. A new Skill or a
substantial change needs a comparative run (no skill or the previous version
against the candidate) on realistic tasks, reporting outcome quality and cost.
Changed routing, authority, discovery or completion needs representative
positive, boundary and negative behavior. Reuse existing cases, add only
missing or intentionally changed expectations, and retire cases whose mechanism
was removed. Keep run output in the host's ignored or temporary location; never
replace observations, weaken expectations or refresh old hashes to pass. If a
needed execution cannot run, report the unverified claim and its missing
condition.

## Handoff and completion

For a separate judgment, hand the frozen candidate, governing sources, raw cases
and validation output to [skill-review](../skill-review/SKILL.md) in a fresh
context; the author cannot label its own verification independent.

Return the changed paths, intended behavioral difference, footprint before and
after, checks actually run, results and unverified boundaries. Follow host
policy for the commit and PR, and keep authored, committed, pushed, reviewed,
merged, published, installed and runtime-verified states distinct.
