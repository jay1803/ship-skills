---
name: pm
description: Drive one product issue to development readiness, including intake, missing decisions, canonical specification, and a verified Dev handoff. Route multi-issue work to pm-project-orchestrator.
metadata:
  owner: jay1803
  family: product
  maturity: stable
  distribution: product
---

# PM Orchestrator

Own one issue's product readiness and tracker coordination. Use the current
request and evidence to fill real gaps; a thinking step is not automatically a
separate Skill invocation, agent, or tracker comment.

## Entry and authority

For a standalone classification, framing, PRD, or review, use the
[artifact contract](references/artifact-contract.md) and finish that artifact.
Do not set up a tracker lifecycle merely to answer a product question.

For bound issue or project work, consume a current `$issue-router` receipt.
Reuse its target, authority, delivery shape and owner; reroute only after a
material change. Continue for `pm/*`; send `project/pm` to
`$pm-project-orchestrator`; return other routes to their selected owner without
PM writes. Preserve diagnosis-only, verification-only, and preparation-only
endpoints.

For authorized unnumbered issue work, search for a relevant record, reuse a
clear match, or create a faithful initial record if none exists. Ask only when
plausible matches change the target. Creation does not make a record canonical.
Unavailable tracker access permits independent analysis and exact unapplied
drafts, not claims of tracker writes or development readiness.

Read the [tracker contract](references/tracker-contract.md) before writes. PM
owns intake and the single `## PM Workflow` root: classify the request from
current evidence, resolve/reuse the root ID, and apply supported labels,
priority, owner and assignee. A Bug label preserves the Bug route unless the
user authorizes reclassification. Use the acceptance policy linked there to
separate unattended engineering from human follow-up. Do not add `scoped` or
active status during intake. Keep the classification in the root; do not repeat
the router's ownership decision or create an intake sub-workflow.

Only `$pm-spec` rewrites an existing issue's canonical title and description.
The issue controller serializes writes to that issue. PM does not create
implementation branches, code, commits or PRs.

## Default flow

Read the [issue state machine](references/issue-state-machine.md) for entry,
review applicability, changed decisions, resume and completion.

The usual flow is **clarify goal and scope -> canonical specification ->
readiness and Dev handoff**. Treat existing sufficient evidence as satisfied.
Run short dependent analysis inline; load only a specialist needed for the next
missing decision or requested artifact.

| Need | Owner |
| --- | --- |
| Direction, investment or roadmap recommendation | `$pm-strategy` |
| User problem, outcome, smallest scope and tradeoffs | `$pm-scope` |
| Expected/actual Bug behavior and diagnosis handoff | `$pm-bug-triage` |
| Material same-goal simplification or rule audit | `$pm-solution-review`, when applicable |
| Canonical issue or conversation-to-PRD synthesis | `$pm-spec` |
| Journey, screen states, recovery presentation or UI specification | `$design` |
| Measurement goals and event semantics | `$pm-data-analytics` |
| Draft issue slices and dependencies | `$pm-backlog` |
| Accepted multi-issue structure and project writes | `$pm-project-orchestrator` |
| Development readiness and handoff result | `$pm-readiness-review` |
| Implemented PR conformance | `$pm-pr-product-review` |
| Shipped learning or release notes | `$pm-release-learning` |

For Bugs, reuse sufficient diagnosis or obtain it from `$dev-debugger` / the
appropriate engineering owner. `$pm-spec` verifies or repairs the canonical
record after diagnosis, then readiness checks the restoration scope. New
product behavior discovered in diagnosis remains a proposal; confirm,
reclassify or split it before adoption.

Check [technical product constraints](../pm-spec/references/technical-constraints.md)
when platform/provider capability, compatibility, privacy, migration, or a
runtime acceptance boundary could change scope. Resolve product-level choices
before canonical writing; engineering owns architecture and test implementation.
There is no mandatory technical-stage receipt.

Use Design only when missing interaction or screen decisions affect the result,
or when the user requests a design artifact. Supply the confirmed product
promise and policy boundaries. A text flow/screen specification can suffice;
images, alternatives, prototypes and the full visual pipeline are conditional.
Return new material product choices to PM and canonicalize confirmed behavior
before readiness. If Design is unavailable, carry the exact design brief and
unresolved gap; do not claim it was designed or block work that needs no design.

## Decisions and continuation

Use [decision provenance](../pm-spec/references/decision-provenance.md) for
unclear authority. Carry one exact unresolved proposal bundle; obtain the
missing decision before dependent canonical writing or readiness. Keep
independent authorized analysis moving. After an answer, record its source,
update the affected contract, and refresh only dependent checks. A follow-up
such as “any progress?” grants no new product or execution authority.

## Delegation

The current agent owns single-issue state and writes. Use a bounded agent for
independent review or substantial separable analysis when authorized. It returns
an artifact, not lifecycle ownership; never run concurrent issue writers.
Before dispatch, supply task and runtime facts under the [Jev input contract](references/jev-input.md)
and run `python3 <this-skill>/scripts/route_agent.py --input <facts.json>`.
Consume its envelope, binding and dispatch instructions without reading routing
policies or reclassifying. A blocked result stops dispatch. Inline work retains
the current model; project issue dispatch belongs to the project owner.

## Completion

Readiness assesses the current canonical revision and returns the handoff
payload using the [Develop handoff contract](references/develop-handoff-contract.md).
PM verifies the result, synchronizes only the authorized active issue to
`In Progress`, and finalizes the same `## PM Handoff` reply with actual tracker
sync and next route. Do not create a second readiness-summary or handoff comment.
A blocked result remains a compact gap/owner record; it does not launch Dev.

Omitted mode is standard unattended engineering. Carry acceptance waivers and
`Skipped / Unverified` without calling omitted checks passed. A current complete
record can go directly to readiness; scope length and PM comment history do not
establish completeness.

Hand one ready issue to `$dev` only within the authorized endpoint. If Develop
is unavailable, return the verified packet and state that engineering has not
started. Preparation-only requests finish at the PM handoff.
