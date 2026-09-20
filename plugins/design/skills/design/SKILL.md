---
name: design
description: Design user flows, interaction states and screen specifications from clear product intent, or route visual direction, alternatives, prototypes, design systems and craft review. Use for UX/UI design and textual engineering handoffs as well as visual artifacts. Product policy and scope stay with PM; production implementation stays with Dev.
metadata:
  owner: jay1803
  family: design
  maturity: stable
  distribution: design
---

# Design Orchestrator

Turn clear product intent into interaction/screen specifications, visual
artifacts or reusable design decisions. Choose the smallest path that produces
the requested result; a text specification does not need the visual pipeline.

## Boundary

- Require an understandable product goal and known material policy boundaries,
  not a pre-existing UX or UI artifact. Inspect supplied briefs, current UI,
  screenshots, code and design-system sources before asking for missing facts.
- Own journeys, screen sequence, interaction states and recovery presentation,
  hierarchy, controls, copy placement, accessibility and platform differences
  within that product promise. Honor bounded delegated design discretion.
- PM owns product goals, scope, acceptance and material policy: permissions,
  retention/deletion, automatic account actions, fallback promises, eligibility
  and other user rights. Return unresolved changes to `$pm` / `$pm-scope`; do
  not turn a design choice into authorization for new product behavior.
- Canonical issue title/description changes belong to `$pm-spec`. Return
  confirmed behavior and source links for synthesis. A standalone design request
  does not require an issue, tracker writes or a full PM lifecycle.
- Production architecture, application code, tests, PRs and releases go to
  `$dev` or the relevant platform implementation owner. Disposable prototype
  evidence does not prove production integrations.
- Slide decks go to the presentation skill; deep motion work to the relevant
  motion specialist when available.

## Select the artifact

| Requested or missing result | Path |
| --- | --- |
| Flow, screens, states, controls, copy or textual engineering specification | Read [interaction specification](references/interaction-spec.md), produce it inline |
| Typography, palette, density, imagery or visual language | `$design-direction` |
| Wireframes, alternatives, layout/component comparisons | `$design-explore` |
| Clickable mockup or usability-test artifact | `$design-prototype` |
| Tokens, component inventory or canonical system refinement | `$design-system` |
| Existing artifact critique or finished visual polish gate | `$design-review` |

Complete a text-only request with the text artifact and any material unresolved
choices. Do not force images, options, prototypes, a design-system phase or a
separate craft gate. For visual work, typical dependencies are direction ->
exploration -> optional prototype -> review; reuse existing decisions and read
only the next needed Skill. If a visual artifact cannot be generated or verified,
return the usable result and exact limitation without claiming completion.

## Decisions and state

Confirm medium, platform, audience, fidelity and intended handoff from context.
Ask only for missing choices that materially change the result; choose routine
reversible details within the authorized design discretion. A user request for
a particular design artifact authorizes producing it without another blanket
approval pause. External publication/attachments retain their own authority.

For multi-phase work, carry the source brief, approved policy and direction,
active artifact, current phase, existing system sources, decisions, evidence,
open blockers and next owner. Do not create this state record for every small
copy or layout request. A changed policy goes back to PM before dependent work;
independent design may continue within known boundaries.

## Delegation and writes

Keep phase selection and Design State in the current agent. Delegate bounded
source inspection or independent review when authorized and useful. Serialize
writers touching the same artifact; `$design-system` alone writes canonical
system tokens/components. Workers return actual sources, artifacts, decisions,
verification and gaps, without taking product lifecycle ownership.

When a Product controller authorizes an exact issue reply, return or publish
only the design artifact under its supplied PM root ID, verify the parent, and
reuse an existing design reply on revision. If the root or reply capability is
missing, return the artifact to that controller; do not create a new PM thread
or edit canonical issue fields. Standalone artifact work remains draft-only
unless publication was requested.

## Handoff

Return the artifact and only the decisions and limits the next owner needs:
flow/screens, relevant state transitions and recovery, controls/copy, platform
and accessibility differences, source policies, optional system/token links and
verification performed. Mark simulated integrations and unknowns explicitly.

Send new or changed product behavior to `$pm-spec` through the PM controller
before readiness. Hand implementation-ready design to Dev within the user's
requested endpoint, without replacing product acceptance or prescribing
production architecture.
