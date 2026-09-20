---
name: dev-project-orchestrator
description: "Plan or execute multiple dev-ready issues as dependency waves or an ordered merge sequence. Single-issue delivery belongs to dev."
metadata:
  owner: jay1803
  family: develop
  maturity: stable
  distribution: develop
---

# Dev: Project Orchestrator

Plan and control engineering execution for project-level issue sets. This skill
decides order, batching, branch strategy, integration checkpoints, wave
barriers, and sequence progression. A single Develop task may own the complete
multi-issue dependency graph and its execution. Each issue worker still executes
exactly one coding issue through `$dev`; that worker boundary must never be
promoted into a top-level single-issue limit.

Read the canonical [branch strategy](../dev/references/branch-strategy.md) before resolving bases or merge direction.

## Issue Router Gate

Before creating project controller state, a goal, dependency graph, worker
thread, branch, or wave, run the Jev-backed canonical `$issue-router` for the
supplied parent, project, or issue set. Continue only when its
receipt is `project/dev`, preserving the complete target scope. Return every
other route to its selected owner without starting this controller. The router
does not replace readiness, graph/wave/barrier ownership, integration planning,
release ownership, or agent runtime routing; validate freshness before the first
mutation and reroute only on a material state or decision change.

`project/dev` requires a materialized parent/project/issue-set whose complete
included issue inventory is current and ready. A target still modeled as one
provisional umbrella with `delivery_shape: multi` or `ambiguous` remains
`project/pm`; do not infer children, create placeholder
workers, or choose a convenient implementation slice inside Develop.

## Command Forms

- `$dev-project-orchestrator <project, milestone, parent issue, or issue list>`: analyze dependencies and produce an engineering execution plan.
- `$dev-project-orchestrator --plan-only <scope>`: analyze order, batches, risks, and branch strategy without starting implementation.
- `$dev-project-orchestrator --deep-plan <scope>`: opt into read-only mapper JSON, schema validation, conflict graph construction, verifier review, and wave planning before implementation.
- `$dev-project-orchestrator --sequence <ISSUE-1> <ISSUE-2> <ISSUE-3> [--fast|--standard|--strict]`: execute a serial chain. Build and merge the current issue before starting the next.
- `$dev-project-orchestrator --sequence <project or milestone> [--plan-only]`: inspect live Linear scope, derive the safe dependency order, then either show the sequence plan or execute it if the user asked to build.

Default delivery mode is `--standard`; omitted mode and explicit `--standard` are identical. Use `--fast` only for unattended primary-path delivery. Preserve `--strict` through worker dispatch; it blocks P0/P1/P2 while standard blocks P0/P1. Apply the mode's unattended validation waiver to each issue's QA/acceptance requirements; unattended alone does not select fast. Read [`../dev/references/development-mode-contract.md`](../dev/references/development-mode-contract.md). Sequence scheduling is independent of delivery mode; `--sequence --strict` retains serial scheduling with the stricter review threshold.

## Boundary

- Use this skill for multiple issues, a Linear project, a milestone, an epic, dependency-heavy issue family, or strict ordered sequence.
- Use `$dev` directly for one dev-ready issue.
- Use `$pm-project-orchestrator` for one provisional umbrella issue until its
  accepted end-to-end children, parent/child relations, dependencies, and
  per-child readiness are materialized. Product owns product-outcome
  decomposition; `$dev-planner` owns engineering task boundaries within approved
  outcomes. This controller owns scheduling after the ready-inventory handoff.
- When the project brief, cutline, issue setup, or material product decisions are
  missing, preserve the project scope and route the exact gaps to
  `$pm-project-orchestrator`. Use `$pm` only for each exact issue that needs
  single-issue Product shaping; do not invent project-level product state inside
  Develop.
- Use `$pm-readiness-review` for child issues whose product readiness is unclear.
- Use `$dev-spike` or `$dev-api-research` for project-level unknowns that block architecture or sequencing.
- Use `$dev-api-steward` or require `$dev` workers to run it when project work changes internal API behavior, OpenAPI/Swagger, generated clients, docs, changelog, versioning, migrations, or client compatibility.
- Use `$dev-integration-manager` when multiple PRs/branches need merge ordering, combined validation, cross-branch conflict handling, API contract checks, or an integration branch.
- Do not implement production code in this skill. Control the project path and invoke `$dev` for issue-level implementation.

## Operating Rules

- Verify live Linear, GitHub, repo, branch, PR, and CI state before making current-state claims.
- Treat dependencies as a graph. Mark each issue `Ready`, `Blocked`, `WIP`, `Awaiting Human Acceptance`, `Done`, or `Unknown` with evidence.
- Parallelize only when issues are independently buildable, contracts are stable, file ownership does not overlap, and merge order is known.
- Do not parallelize work that changes the same files, migrations, schemas, generated outputs, package/project files, API contracts, product decisions, or release gates.
- Do not parallelize backend/API contract changes with dependent client changes until the API contract is stable and the API Steward checkpoint is planned.
- Do not run deep planning by default. For high-risk or unclear multi-slice work, recommend deep planning and ask before running it unless the user already requested it.
- In deep planning mode, keep all work read-only against production code. Temporary mapper JSON and graph artifacts may be written only under `/tmp` or another clearly disposable planning directory.
- Every implementation worker must use `$dev` and receive exactly one concrete Linear issue ID.
- Keep the invoking thread as the persistent project controller. The controller alone owns the dependency graph, worker registry, wave barriers, retries, successor dispatch, and project completion.
- Before dispatch, follow the [Jev input contract](../agent-routing/references/jev-input.md) and run `python3 <agent-routing-skill>/scripts/route_agent.py --input <facts.json>`. Consume the returned envelope and binding without reclassifying or reading routing policies. Supply `lifecycle: controller` for fresh user-owned issue workers and the complete task scope as evidence. Existing controllers retain their actual bindings. A blocked result stops dispatch.
- By default, run each issue-level `$dev` implementation in a fresh user-owned controller thread or session on the resolved executor, including the first executable issue. It must be visible in that executor's supported task/session surface and recorded in the worker registry; an internal bounded sub-agent is not an equivalent substitute.
- Treat an explicit request to execute, build, finish, or ship a multi-issue scope through this skill as an explicit request to create the required user-owned issue threads. Do not ask for separate thread-creation consent or claim that thread creation was not requested. A plan-only or analysis-only request does not authorize worker-thread creation.
- Workers must never dispatch successor issues. They implement one issue, reach a terminal result, and report that result to the controller.
- Consider persistent worker creation unavailable only after the resolved executor's controller/session entry cannot be found or an actual creation attempt fails. Then use the Serial Inline Fallback in the worker-execution reference, keeping one active issue in the current user-owned controller thread after clearly reporting the heavier-context fallback. Never use a bounded sub-agent or serial sub-agent as the persistent owner of an issue workflow, and never describe that fallback as parallel execution.
- Pass one resolved delivery mode to every `$dev` worker. Standard is the default; never let workers infer a different implicit mode.
- Derive `Validation required` from the mode contract: standard focuses on primary
  flows and the ticket's regression, without automatic reverse-red/mutation or
  unrelated edge-case matrices. Strict selects deeper checks by risk. Carry the
  source of explicit additional requirements; do not upgrade the worker through
  a copied checklist. Callback summaries need results and material limitations,
  not per-assertion proof.
- In fast mode, the controller aggregates skipped/unverified entries from every worker in project state and final reporting. Do not create a dedicated risk ticket merely to record fast-mode omissions.
- If project execution will produce multiple PRs with shared behavior, plan the `$dev-integration-manager` checkpoint before merge.

## Dependency Analysis

When the accepted product scope needs technical decomposition or ticket
preparation, use `$dev-planner` for the shared plan and read the
[engineering ticket protocol](../dev-planner/references/engineering-ticket-protocol.md).
Keep planning distinct from issue implementation: the controller may assign one
bounded planning subagent per independent task, in capacity-limited batches,
with fixed ownership and the shared design. Reconcile their drafts before
authorized persistence. Tracker writes remain with the existing authorized
owner; new scope/relations require fresh readiness and routing before execution.
Design-only tasks return decision artifacts and never enter the coding-worker
merge queue. Stable planning inputs do not waive implementation predecessors.

Use live Linear data first when available. For every candidate issue, gather:

- Issue ID, title, state, team, labels, assignee, project, milestone, and URL.
- Description, acceptance criteria, important comments, attachments, and linked docs.
- Explicit relations: blocked by, blocks, parent, sub-issue, related, duplicate.
- Existing branch or PR links.
- Repo or code-area hints from labels, description, comments, linked PRs, or project metadata.

Use hard dependency edges for:

- Explicit Linear `blocked by` / `blocks` links.
- Issue text that says one item depends on, follows, requires, or must land after another.
- Required implementation order: schema before API, API before client, shared model before consumers, provider contract before provider implementation, data plumbing before UI, feature implementation before polish or validation.
- API Steward checkpoints before dependent client work when backend/API behavior, docs, generated clients, or migration guidance must be updated.

Use soft ordering signals only when no hard links exist:

- Research, API study, or contract lock before implementation.
- Shared infrastructure before narrower feature work.
- Backend/domain support before user-visible integration.
- Tests, docs, cleanup, and release polish after the behavior they validate.

If hard links contradict the user-provided order, pause and ask before executing. If the graph contains a cycle, show the cycle and ask for the edge to break unless issue text clearly resolves it.

Do not force unrelated issues into a dependency chain. In normal project mode, use independent batches. In sequence mode, serialize unrelated work only when the user explicitly asks for one ordered queue, and label it as serialization rather than dependency.

## Normal Project Workflow

1. Identify the project, milestone, parent issue, or issue set.
2. Read PM artifacts: project brief, milestone plan, issue list, acceptance criteria, dependencies, cutline, risk map, and readiness results.
3. Read engineering context: repo surface, existing modules, known contracts, migrations, build/test topology, active PRs, release branch policy, and CI constraints.
4. Classify every issue:
   - `Ready`: dev-ready and can be assigned to `$dev`.
   - `Blocked`: missing product decision, dependency, API contract, design, access, or upstream work.
   - `WIP`: already being implemented or reviewed.
   - `Awaiting Human Acceptance`: a separate human acceptance deliverable awaits evidence; keep it outside the engineering worker queue and merge barriers. Old labels on implementation issues follow the mode waiver.
   - `Done`: merged or otherwise available on the base branch with mode-required gates satisfied; in fast mode, any skipped human acceptance must already be recorded in controller state and issue closeout.
   - `Unknown`: cannot verify state with available tools.
5. Build the dependency graph with explicit edge reasons.
   - In default mode, use lightweight issue, repo, branch, and contract evidence.
   - In `--deep-plan` mode, run the Deep Parallelization Plan workflow in the deep-planning reference and use its conflict graph as the dependency graph.
6. Create execution batches:
   - Batch 0: research, API research, spike, contract clarification.
   - Batch 1: foundation/backend/schema/shared contract.
   - Batch 2: parallel clients/features that depend on stable foundations.
   - Batch 3: integration, polish, edge cases, data migration cleanup.
   - Batch 4: release hardening, combined validation, rollout/rollback checks.
7. Decide parallelization. Name what can run together, what cannot, and why.
8. Resolve the canonical branch strategy: repository policy first; otherwise
   use one temporary branch per repository for this batch/project/parent. Record
   upstream, issue PR base, promotion target, scope, and ownership. On execution,
   create/publish or verify/reuse it before dispatch; pass it to every worker.
9. Define risk and validation strategy across conflicts, schema/API contracts, tests, rollbacks, and release gates.
10. For API-changing batches, require the relevant `$dev` worker to run `$dev-api-steward` and return contract/docs/changelog/client-impact results before dependent client batches proceed.
11. If asked to execute, initialize controller state and dispatch `$dev` workers wave-by-wave through Controller-Owned Wave Execution in the worker-execution reference. Run `$dev-integration-manager` before merge when multiple PRs interact or combined validation is required.

## Output

For normal project mode:

```markdown
## Engineering Execution Plan

Project:
Milestone:
Mode: <fast | standard | strict>
Skipped / Unverified: <entries or none>
Ready issues:
Blocked / WIP / unknown issues:

## Dependency Graph
- <Issue A> -> <Issue B>: <B depends on A>

## Execution Batches
- Batch 0: <research/spike>
- Batch 1: <foundation>
- Batch 2: <parallel client/feature work>
- Batch 3: <integration/polish>
- Batch 4: <release hardening>

## Parallelization Decision
Can run in parallel:
Cannot run in parallel:
Reason:

## Branch Strategy
Base branch:
Per-issue branches:
Temporary integration branch (or repository-policy exception):
Policy source / scope:
Final promotion target / aggregate PR:
Merge order:

## Risk
File conflicts:
Schema conflicts:
API contract risks:
Testing risks:
Rollback risks:

## Dispatch Plan
- <Batch/issue>: use `$dev` with <mode> and <key constraints>
- Integration checkpoint: <use `$dev-integration-manager` or "Not needed">

## Controller State
Controller thread:
Execution mode: <persistent-workers | serial-inline>
Active issue and pending gate (serial-inline):
Active wave:
Worker registry:
Barrier status:
Wake strategy:
Next unlock condition:
```


## Conditional References And Completion

| Request or pending state | Read |
| --- | --- |
| --deep-plan or explicitly requested verified conflict mapping | [Deep planning](references/deep-planning.md) and its [mapper schema](references/deep-plan-output-schema.md) |
| --sequence, an ordered queue, or merge-before-next scheduling | [Sequence mode](references/sequence-mode.md) |
| Execution is requested, or an existing worker/inline issue needs continuation | [Worker execution](references/worker-execution.md), before dispatch, helper work, or accepting a callback |

Default project planning uses the dependency analysis and normal workflow above;
it does not load deep mapper instructions or create implementation workers.
A plan-only request finishes at the engineering plan. Execution keeps the
invoking controller responsible for the complete graph and live merge barriers.
Workers never dispatch successors. Persistent-worker unavailability uses the
single-active-issue Serial Inline Fallback, preserving its pending gates and
helper state; a bounded sub-agent cannot substitute for an issue controller.

Execution completes only when every required issue meets its mode-required
merge/test/acceptance barrier and any planned integration checkpoint passes.
For a temporary batch branch, also require the verified aggregate PR merge and
final handoff from the branch strategy contract; child merges alone do not
complete the project.
Preserve skipped/unverified evidence in every mode, and do not treat an open PR,
green CI, or worker completion as an eligible merge barrier.
