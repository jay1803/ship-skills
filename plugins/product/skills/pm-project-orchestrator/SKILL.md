---
name: pm-project-orchestrator
description: Structure a Linear project or coordinate PM readiness across related issues, including decomposition of an umbrella issue.
metadata:
  owner: jay1803
  family: product
  maturity: stable
  distribution: product
---

# PM: Project Orchestrator

Turn a product project into a controlled PM execution surface. Infer the next project goal from live state, then complete project structure or drive issue-level `$pm` workers through safe serial and parallel waves to verified PM readiness.

## Issue Router Gate

Before creating project controller state, a goal, inventory, worker wave, or
tracker write, run the Jev-backed canonical `$issue-router` for the supplied parent,
project or issue set. Continue only when its receipt is
`project/pm`, preserving every target ID and the complete scope. Return every
other route to its selected owner without starting this controller. The router
is read-only and does not replace project inventory, cutline, dependency,
worker-wave, PM readiness, or runtime-routing decisions; validate receipt
freshness before the first write and reroute only on a material state change.

`project/pm` may also bind one existing issue whose Delivery Shape Precheck is
`multi` or `ambiguous`. Treat it as a provisional
umbrella, not as a dev-ready single issue: validate the independent outcome
boundaries, decide the accepted end-to-end decomposition, apply parent/child and
dependency writes here, and inventory the resulting children before dispatching
issue-level PM work.

When the umbrella already has a controller, branch, or PR, preserve it as
evidence. Map the existing implementation intact to one accepted child when its
scope matches, or return a fresh single-issue route when no split is accepted.
Do not discard, rewrite, or duplicate existing Git/PR state as part of Product
decomposition.

`project/pm` can also bind a proposed parent for an accepted engineering-task
materialization request. Its product outcome may remain `single`; follow
Engineering Task Materialization below rather than inventing independent
product outcomes or returning it solely because its product shape is single.

## Boundary

- Own the project-level product decisions: outcome, audience, milestone outcomes, decomposition intent, dependency intent, risks, cutline, and PM assignment.
- Own live project-level tracker writes, including the project description, milestone definitions and assignments, project issue membership, and project-level dependency relationships.
- Own accepted decomposition of a provisional umbrella issue: child creation,
  parent/child membership, cutline, and split dependencies. The Router only
  supplied shape evidence; it did not authorize or design the split.
- Own one active project-level goal at a time. Infer it from live state unless the user supplies a narrower or later target.
- Keep the invoking thread as the persistent project controller. The controller alone owns the project inventory, dependency graph, worker registry, wave barriers, project-level tracker writes, successor dispatch, and final PM-to-Dev handoff.
- Before dispatch, follow the [Jev input contract](../pm/references/jev-input.md) and run `python3 <product-pm-skill>/scripts/route_agent.py --input <facts.json>`. Consume the returned envelope and binding without reclassifying or reading routing policies. Supply `lifecycle: controller` for fresh user-owned issue workers and the complete task scope as evidence. Existing controllers retain their actual bindings. A blocked result stops dispatch.
- Do not write every child issue's final PRD/spec. Route child issues to `$pm`, `$pm-scope`, `$pm-solution-review`, `$pm-spec`, `$design`, `$pm-data-analytics`, or `$pm-readiness-review` when they need per-issue artifacts.
- Use `$pm-backlog` to draft a normalized issue tree, duplicate/follow-up set, dependency graph, and proposed milestone assignments from an authorized decomposition. Keep project cutline, final assignment decisions, and live project writes here.
- When `$pm-backlog` runs inside this workflow, require a draft-only artifact. Accept or reject it, then apply the approved project-level tracker writes here before advancing.
- Use `$pm-strategy` when product direction, roadmap fit, segment focus, sequencing, or product-principle tradeoffs need shaping.
- Use `$pm-strategy` when the open question is whether the project should exist, continue, or be stopped; the user owns the final commitment decision.
- Use `$pm-readiness-review` only after a child issue has enough PM artifacts to judge dev readiness.
- If the request is one ordinary `delivery_shape: single` issue without an
  accepted engineering-task materialization request, route to `$pm`
  instead of this skill. A one-record provisional umbrella is project scope even
  before children exist.
- Do not create branches, worktrees, code, commits, or PRs. Hand dev-ready issue sets to `$dev-project-orchestrator` only after PM execution is complete or at an explicitly reported partial handoff.
- Treat `plan`, `audit`, `draft`, or `analyze` as plan-only requests. Treat `start`, `continue`, `run`, `prepare`, or `finish` as authorization to execute the PM waves and apply in-scope tracker writes.
- A bare project URL, parent, milestone, or issue list authorizes identifying and
  inspecting that target, not project mutations. Use surrounding user intent
  and existing authorization to decide whether execution is requested.
- Tool permissions remain separate from workflow routing. Create user-owned
  threads or tool-managed goals only when the user request satisfies the active
  tool contract. If PM execution is authorized without permission to create new
  tasks, run serially in the current thread; retain issue ownership and evidence.

## Workflow

1. Identify the project source: Linear project, epic, parent issue, provisional
   umbrella issue, roadmap item, milestone, document, user-provided brief, or
   explicit issue list.
2. Inventory all issues and relations in the bound scope before project writes.
   Read linked comments, documents, designs, and technical evidence only when
   they affect the requested structure, decisions, dependencies, or readiness.
   A narrow status/audit request does not require complete project preparation.
   For a provisional umbrella, verify the Router's shape evidence against its
   canonical outcome and acceptance boundaries. If it is actually one coherent
   outcome without an accepted engineering-task plan to materialize, return it to the exact single-issue PM owner with a fresh Router
   receipt rather than manufacturing children.
3. Select or reuse the active project goal using Project Goal Selection. Record the selected goal, evidence, completion criteria, and whether it came from the user or live state.
4. Audit every issue independently. Record its existing PM artifacts, confirmed decisions, missing decisions, tracker state, current owner, hard predecessors, and earliest verified missing PM skill. Do not infer a completed prerequisite or readiness from a recently created status, title, label, or thin description.
5. Reconcile existing commitments, shipped behavior, duplicates, stale scope, and assumptions. Preserve useful project and issue content instead of treating every issue as net-new.
6. Write or refresh the project brief: what is being built, why now, for whom, user/business outcome, success signal, non-goals, and decision context.
7. For a verified provisional umbrella, define independently valuable
   end-to-end child outcomes before per-issue PM dispatch. Do not split by
   design/implementation/QA phase, technical layer, file count, estimate, or
   expected PR count. A materially necessary separate human acceptance follow-up
   follows Acceptance Classification and is not another coding slice. Use `$pm-scope` when an outcome boundary is unresolved and
   `$pm-backlog` for the draft tree; accept and apply the split here.
8. Set the cutline:
   - **v1**: must ship to deliver the core outcome.
   - **Deferred**: valuable but not needed for the first coherent version.
   - **Rejected**: not aligned, duplicate, too risky, or not worth carrying.
9. Build the dependency and conflict graph. Include product-decision dependencies, parent/child and split dependencies, shared project writes, shared source-of-truth artifacts, external decisions, and dev dependencies that constrain product scope.
10. Audit acceptance using [Acceptance Classification](../pm-spec/references/acceptance-policy.md#unattended-engineering-acceptance). Keep standard engineering unattended: real-environment tests are recommendations or materially necessary separate human acceptance tickets, not implementation gates. Reuse or create the follow-up within existing tracker authority, with a human owner/role, executable steps and `human-acceptance-required`. It may depend on the delivered build, never block implementation or its successors; keep it deferred outside the coding inventory and PM Ready barrier. Missing follow-up logistics or write access leaves a draft, not an engineering block.
11. Build the risk map across product, technical, UX, data, privacy, analytics, migration, rollout, external dependency, and operational risk.
12. Classify every issue as `Direct`, `Parallel`, `Serial`, or `Blocked`; select its next PM skill and explain the evidence for that route.
13. Synthesize ordered PM waves. A wave contains all currently safe independent issue workers; sequence scheduling is a wave containing one issue.
14. Apply controller-owned project setup before dispatch: project description, cutline, milestones, issue membership, and project-level dependency relationships. Otherwise produce exact tracker-ready drafts.
15. In execution mode, dispatch and control work required by the active goal. In plan-only mode, stop after the verified goal selection, wave plan, and tracker drafts.
16. Verify the active goal's completion criteria before marking it complete. If execution authorization continues and a later standard goal is now unlocked, advance the in-memory objective and continue within the authorized endpoint.
17. When the active goal is `PM Ready`, complete with a verified project PM state and hand all dev-ready issues, dependencies, deferred work, and blockers to `$dev-project-orchestrator`.

## Engineering Task Materialization

Use this path when the caller supplies a current accepted engineering task plan
inside approved product scope and requests its tickets. The planner owns the
technical design and task boundaries; this controller validates scope coverage
and owns materialization. These children need coherent engineering outcomes,
verification and safe PR boundaries, not independently marketable features.
The product-decomposition prohibition on layer/phase tickets still applies to
inventing product outcomes; it does not reject justified engineering tasks.

Require stable task keys, implementation/design kind, parent-acceptance mapping,
shared contracts, concrete ticket bodies, owned artifacts, prerequisites and
design readiness. Return missing engineering design to the planning owner;
do not redo it inside PM or fabricate a Product decision. A supplied complete
plan needs no additional installed planning Skill or ceremonial PM rewrite.

Within existing write authority, create/reuse each assigned task record. The
controller may delegate a bounded write of one accepted ticket body, with exact
team/project/parent, task key, allowed fields and existing ID when present.
Keep one writer per key, reconcile uncertain create results before retrying,
verify every write, and retain confirmed IDs on partial failure. The controller
alone applies parent/child links, dependency edges and readiness/status changes.
Tracker-only helpers are not persistent PM/Dev issue controllers.

Preserve canonical parent scope and combined acceptance. Check each coding
child's own engineering result and mapped product constraints using current
readiness evidence; parent approval or plan acceptance alone does not mark
children ready. Keep unresolved implementation and design-only records outside
the ready coding inventory. The parent is a container for execution, not an
additional coding worker or a completed product outcome. Reuse matching
branches/PRs under the accepted child mapping. Refresh routing for the complete
included coding inventory before the Dev project handoff, preserving actual
implementation dependencies and deferred records.

Plan-only requests return these drafts and mappings without writes. Missing
authority leaves materialization pending. Ordinary single-task work still uses
the existing single-issue route.

## Project Goal Selection

Do not require the user to formulate a goal. Read live project state first and select the earliest unmet project gate. Treat a user-provided goal as an endpoint override, while preserving any unmet prerequisite.

Use one active controller goal at a time:

| Goal | Select when | Verified completion |
| --- | --- | --- |
| `Project Structured` | The project description, milestones, issue tree, cutline, membership, or dependencies are incomplete | The canonical project description is complete; valuable milestones have observable outcomes and exit criteria; every in-scope capability maps to a created issue; issue membership, parent/child structure, cutline, and dependencies are applied and verified |
| `PM Ready` | Project structure is complete but one or more in-scope issues have not completed their required PM chain | Every in-scope issue is verified `Ready`, `Done`, `Deferred`, or `Rejected`; accepted split children are inventoried; required v1 issues are not blocked; and the Dev project handoff is complete |
| `Project Plan Verified` | The user explicitly requests plan, audit, analysis, or draft-only work | Current state, selected execution goal, dependencies, issue routes, waves, tracker-ready drafts, and blockers are documented without claiming live execution |

Use these shapes for the in-memory objective or an explicitly requested
tool-managed goal:

- `Project Structured`: `Structure <PROJECT> so its canonical description, milestones, issue tree, cutline, membership, and dependencies are complete and verified.`
- `PM Ready`: `Bring every in-scope <PROJECT> issue through its required PM chain to a verified terminal state and produce the Dev project handoff.`
- `Project Plan Verified`: `Produce a verified current-state, goal, dependency, and PM wave plan for <PROJECT> without applying execution writes.`

Goal lifecycle rules:

- Keep the selected objective in controller state after inventory; use a goal
  tool only when the user explicitly requests a tool-managed goal and its
  lifecycle rules permit it; do not ask the user to restate information that the tracker answers.
- If the user explicitly asks only for project setup, stop after `Project Structured`. If the user asks to continue, run, prepare, or finish the project,  complete `Project Structured`, re-read live state, then continue with `PM Ready`.
- If the project is already structured, select `PM Ready` directly. If all issues already appear ready, keep `PM Ready` long enough to verify the evidence and produce the handoff, then complete it.
- Never mark `Project Structured` complete from drafts when live writes were authorized, or `PM Ready` complete while a required v1 issue is blocked or unverified.
- Workers do not own the project goal or mark it complete. They may record issue-local objectives; tool-managed goals require the
  user authorization specified by the active goal tool; only the controller verifies and closes the project goal.
- Follow the goal tool's status rules. A partial result, completed wave, open question, or exhausted token budget is not goal completion.

## Per-Issue Audit

For every discovered issue, record:

| Field | Required evidence |
| --- | --- |
| Issue | ID, title, project/milestone, parent/children |
| Delivery shape | Router classification, independent outcomes, shared acceptance, and decisive signals |
| Current state | Tracker status, labels/type, assignee, active owner or worker |
| Sources read | Description, PM comments, linked docs/designs, dependencies, relevant shipped behavior |
| PM state | Existing artifacts and the earliest missing PM artifact |
| Product state | v1, deferred, rejected, duplicate, or outside the project cutline |
| Dependencies | Hard predecessors, shared decisions, project writes, external blockers |
| Human acceptance | Required/not required, label state, canonical steps state, acceptance owner or role |
| Execution | Direct, parallel wave, serial predecessor, or blocked |
| Terminal target | Ready, Done, Blocked, Split, Deferred, or Rejected |

Use these controller states:

- `Unknown`: inventory or evidence is incomplete.
- `Pending`: PM work is known but not dispatched.
- `Dispatched`: one issue worker owns the active PM route.
- `Ready`: readiness review passed and the issue-level Dev handoff is complete.
- `Done`: the issue is already shipped, closed, or otherwise requires no PM work.
- `Blocked`: a user, product, technical, or external decision prevents progress.
- `Split`: the original issue was replaced by an accepted child-issue plan; inventory the new children before completing the project.
- `Deferred` or `Rejected`: the controller applied or drafted the cutline decision with its reason.
- `Stopped`: execution cannot safely continue and the controller reported why.

## Assignment Rules

Use `$pm` for a raw issue's intake and single-issue ownership. Select the next
missing decision rather than dispatching every Skill for every child:

- `$pm-scope`: unclear user problem, outcome, buildable boundary or tradeoff.
- `$pm-strategy`: unsettled direction, investment or roadmap commitment.
- `$pm-bug-triage`: missing expected/actual Bug evidence or diagnosis route.
- `$pm-solution-review`: an applicable material simplification/rule review under
  the [state machine](../pm/references/issue-state-machine.md), not every non-Bug.
- `$pm-spec`: canonical synthesis or a confirmed change missing from active text.
- `$design`: needed interaction/screen specification or requested visual artifact.
- `$pm-data-analytics`: material measurement goals or event decisions.
- `$pm-backlog`: draft issue tree, dependencies or follow-ups for this controller.
- `$pm-readiness-review`: sufficient canonical evidence needing the final gate
  and combined handoff.

Read [technical constraints](../pm-spec/references/technical-constraints.md)
when capability, shared interface or runtime fidelity can change scope. Resolve
product choices before spec; do not require a technical-stage artifact.

## Changed decisions and integration dependencies

When active scope or a shared decision changes, inspect the affected portion of
the existing inventory, including cross-parent prerequisites and reused local
implementations. Map prior issue/branch/PR evidence to its actual outcome;
missing delivery links do not prove implementation never happened.

Route confirmed canonical changes through each affected issue's Spec owner,
keeping same-issue writes serial. A parent comment is not sufficient propagation
when active child or cross-parent descriptions still say the opposite. Verify
changed canonical fields and acceptance classification before dependent handoff.
If the user authorized only one issue, return sibling-change drafts without
mutating them; otherwise complete the authorized affected updates.

For a shared interface, distinguish independent preparation from final semantic
alignment, review or merge. Record producer -> consumer integration order in the
existing dependency graph and supported tracker relationships, with the boundary
explained when a relation is coarser than the permitted parallel work. Re-read
relations after writes. Shared filenames alone do not prove a hard dependency;
changed shared semantics can require one. Refresh only affected readiness and
integration evidence, retaining valid reviews and independent work.

## PM Execution Planning

Classify work as follows:

- `Direct`: the controller can verify an already terminal issue or apply a project-only write without an issue worker.
- `Parallel`: separate child issues can run together because their product decisions, source artifacts, and mutable tracker items are independent.
- `Serial`: an issue depends on another issue's product decision, split, canonical spec, technical boundary, or external result.
- `Blocked`: no safe PM route can proceed until a named decision or source becomes available.

Parallelize issue workers only when all of these are true:

- Each worker owns exactly one concrete issue ID.
- Workers write to different child issues.
- The project brief, cutline, and relevant shared decisions are stable enough for both workers.
- Neither worker can invalidate the other's scope, acceptance criteria, split, or readiness result.
- Any hard predecessor is already terminal in the required state.

Do not parallelize:

- Two PM skills acting on the same issue.
- A parent decomposition or split with child specs that depend on its outcome.
- Issues that share an unresolved product, UX, API, privacy, migration, analytics, or rollout decision.
- Any worker with controller-owned project description, milestone, membership, cutline, or project-dependency writes.
- `$pm-spec` with another writer on the same issue.

Shared membership in one project is not itself a reason to serialize. Reserve project-level writes for the controller, then run independent child-issue PM chains in parallel.

## Worker Execution

For authorized worker dispatch or resume, read
[worker-execution.md](references/worker-execution.md). Plan-only work does not
load the worker handoff, callback, and wave-control protocol. Without permission
for new tasks, keep one active issue inline and preserve its PM gates and resume
state before advancing dependent work.

## Tracker Write Authority

- This skill may update the project description, project status fields, milestone definitions, project-level dependency notes, and issue membership when tools allow.
- This skill may create child issues, follow-up issues, research issues, and rejected/closed issue recommendations when the project cutline requires them.
- For a provisional umbrella, create children only after the controller accepts
  independently valuable end-to-end outcomes. Preserve the umbrella as parent
  or project context and verify every created child and relation before PM waves
  continue.
- For an accepted engineering-task plan, apply Engineering Task Materialization;
  preserve the parent's product acceptance and verify task-local readiness.
- For a separate human acceptance issue, apply `human-acceptance-required` and executable steps at creation. For old implementation acceptance metadata, route labels to `$pm` and canonical wording to `$pm-spec`, carrying the mode waiver immediately; do not block engineering readiness on deferred human testing.
- Do not rewrite an existing child issue's canonical product spec. Route that to `$pm-spec`.
- Issue workers may update only their assigned child issue within the authority of the PM skill they are running. They must return proposed project-level changes to the controller.
- When live tracker tools are unavailable, produce exact project-description, milestone, issue, and dependency drafts instead of claiming updates were applied.

## Output

Lead with the selected objective, execution authority, and verified result.
Link applied project/issue changes or return drafts; name remaining decisions,
blocked branches, and the next owner. Use
[project-output.md](references/project-output.md) for a formal project brief or
wave plan. Do not imply execution, new tasks, or Dev dispatch from a plan.
