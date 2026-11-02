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

Plan and control engineering execution for a multi-issue scope: order,
admission, branch strategy, integration checkpoints, barriers and sequence
progression. One Develop task may own the complete dependency graph and its
execution; the per-issue worker boundary never limits this controller to one
issue.

Read the [controller/worker boundary](../dev/references/execution-ownership.md#controller-issue-worker-and-bounded-agents) before execution. Two persistent layers own management; bounded implementation and Review stay inside issue workers.

Execution is unattended by default. Apply the
[autonomous decision and discovered-work rule](../dev/references/execution-ownership.md#autonomous-decisions-and-discovered-work)
to controller decisions, ticket comments, the shared follow-up parent and
blocking remediation. Deferred discoveries stay outside the execution inventory.

Once execution is accepted, apply the [thread names](references/worker-execution.md#controller-and-worker-thread-names)
to this controller and its worker handoffs.

Read the canonical [branch strategy](../dev/references/branch-strategy.md) before resolving bases or merge direction.
For native stacked PR execution, also read its
[stack contract](../dev/references/stacked-prs.md). Resolve development admission
separately from landing; an unmerged stack-ready layer never completes an issue.

## Readiness Gate

Classify every issue from live evidence under the
[entry audit](../dev/references/resume-preflight.md#entry-audit) and mark one
that is not dev-ready `Blocked`, naming the exact decision to ask the requester.

Before the first mutation or worker dispatch (controller state, goal, branch,
tracker write or worker thread), require a materialized parent/project/issue-set
whose complete included issue inventory is current and ready, and recheck it
only on a material state or decision change. A target still modeled as one
provisional umbrella with `delivery_shape: multi` or `ambiguous` first needs the
requester-confirmed outcome split under that audit; do not infer children,
create placeholder workers, or choose a convenient implementation slice.

## Command Forms

- `$dev-project-orchestrator <project, milestone, parent issue, or issue list>`: analyze dependencies and produce an engineering execution plan.
- `$dev-project-orchestrator --plan-only <scope>`: analyze order, risks, and branch strategy without starting implementation.
- `$dev-project-orchestrator --deep-plan <scope>`: opt into read-only mapper JSON, schema validation, conflict graph construction, verifier review, and wave planning before implementation.
- `$dev-project-orchestrator --stack <scope>`: resolve native stacks for permitted
  same-repository dependency chains, preserving independent work and batch trunks.
  Record stack-ready development edges and integration ownership; plan-only
  remains read-only. Explicit merge-before-next requirements retain their gates.
- `$dev-project-orchestrator --sequence <ISSUE-1> <ISSUE-2> <ISSUE-3> [--fast|--standard|--strict]`: execute a serial chain. Build and merge the current issue before starting the next.
- `$dev-project-orchestrator --sequence <project or milestone> [--plan-only]`: inspect live Linear scope, derive the safe dependency order, then either show the sequence plan or execute it if the user asked to build.

Resolve one delivery mode for the scope: `--standard` unless the user
explicitly selects `--fast` or `--strict`; unattended execution alone does not
select fast. Pass it unchanged to every worker; workers never infer another.
Read the [development-mode contract](../dev/references/development-mode-contract.md)
when composing worker handoffs: it governs each handoff's `Validation required`,
defect threshold and unattended acceptance waiver. Add only an issue's
source-bound requirements, not a copied checklist. Sequence scheduling is
independent of delivery mode.

## Boundary

- Use this skill for multiple issues, a Linear project, a milestone, an epic, dependency-heavy issue family, or strict ordered sequence.
- The requester confirms product-outcome boundaries; `$dev-planner` owns
  engineering task boundaries within approved outcomes. This controller owns
  scheduling once the inventory is ready.
- When the project brief, cutline, issue setup, or material product decisions are
  missing, preserve the project scope and ask the requester for the exact gaps;
  do not invent project-level product state inside Develop.
- Use `$dev-spike` or `$dev-api-research` for project-level unknowns that block architecture or sequencing.
- Require the owning `$dev` worker to run `$dev-api-steward` when project work changes internal API behavior, OpenAPI/Swagger, generated clients, docs, changelog, versioning, migrations, or client compatibility, and to return its contract results before a dependent client issue starts.
- Issue workers own eligible merges by default; preserve only a source-bound user/repository assignment to another executor under the [merge-executor rule](references/worker-execution.md#merge-executor-assignment).

## Operating Rules

- Verify live Linear, GitHub, repo, branch, PR, and CI state before making current-state claims.
- Treat dependencies as a graph. Mark each issue `Ready`, `Blocked`, `WIP`, `Awaiting Human Acceptance`, `Done`, or `Unknown` with evidence.
- Run issues in parallel only when each is independently buildable, its contracts are stable and the merge order is known. Never parallelize issues that change the same files, migrations, schemas, generated outputs, package/project files, API contracts, product decisions or release gates; a client that depends on a changing API waits until that contract is stable and its API Steward checkpoint is planned.
- Before admitting a wave, budget the actual executor's issue/helper capacity under [capacity scheduling](references/worker-execution.md#capacity-scheduling); leave room for the next required bounded phase.
- Do not run deep planning by default. Select it when requested or when concrete
  high-risk or unclear multi-slice work needs it within the authorized scope,
  and record the decision. It stays read-only against production code; mapper
  JSON and graph artifacts go only to a disposable planning directory.
- Keep the invoking thread as the persistent project controller. The controller alone owns the dependency graph, worker registry, wave barriers, retries, successor dispatch, and project completion.
- Run each issue's `$dev` delivery in a fresh, user-visible persistent worker on the resolved executor, routed, created and recorded under [worker execution](references/worker-execution.md); when creation is unavailable, apply its Worker Creation Failure And Recovery.
- Treat a human request to execute, build, finish, or ship a multi-issue scope as including the required user-visible issue threads. Reuse that request and any explicit thread authorization for this scope without a separate Skill-level confirmation. Plan-only or analysis-only requests do not create workers. Honor a stronger active tool restriction or actual denial; identify its exact source and affected action instead of attributing another approval rule to the user or bypassing it.
- Record observable phase checkpoints and intervene through the owning worker
  when their proof is overdue, work does not converge or delivery boundaries
  change; use [Progress Intervention](references/worker-execution.md#progress-intervention).
  Time/token pressure never waives gates.
- On controller wakes apply the [recovery contract](references/controller-recovery.md).
- Consume Review follow-up, handoff and exhaustion decisions under the
  [Review lifecycle's controller disposition](../dev/references/review-lifecycle.md#controller-disposition-after-exhaustion).
  Worker retries never reset its counts.

## Integration Checkpoints

A temporary batch always ends with an integration checkpoint; other strategies
need one when PRs interact, share a contract or need combined validation. Assign
it to a designated worker running `$dev-integration-manager` with the explicit
PR set, never a nested project controller, and verify its returned evidence.
The controller performs none of these merges unless a source-bound merge-executor
assignment names it.

| Branch strategy | Checkpoint runs | Merges |
| --- | --- | --- |
| Temporary batch branch | after every required child merge into the batch branch | issue workers merge their child PRs; the integration worker validates the batch and lands the aggregate promotion PR under repository authority |
| Native stack | before the authorized group lands | issue workers own their layers up to stack-ready; the integration worker lands the group on the trunk |
| Issue PRs to the resolved base under repository policy | before the first interacting PR merges | issue workers merge their own PRs in the checkpoint's order |

## Dependency Analysis

When the accepted product scope needs technical decomposition or ticket
preparation, use `$dev-planner` for the shared plan and the
[ticket preparation](references/ticket-preparation.md) rules for assignments,
draft acceptance and persistence. Design-only tasks return decision artifacts
and never enter the coding-worker merge queue. Stable planning inputs do not
waive implementation predecessors.

Use live Linear data first when available. For every candidate issue, gather:

- Issue ID, title, state, team, labels, assignee, project, milestone, and URL.
- Description, acceptance criteria, important comments, attachments, and linked docs.
- Explicit relations: blocked by, blocks, parent, sub-issue, related, duplicate.
- Existing branch or PR links.
- Repo or code-area hints from labels, description, comments, linked PRs, or project metadata.

A hard dependency edge needs one of:

- An explicit `blocked by` / `blocks` link, or issue text stating that one item depends on or must land after another.
- An evidenced producer/consumer need: the consumer uses a schema, API contract, shared model, generated output, migration, design decision or API Steward result that the producer creates or changes, shown by issue text, contracts or code.

Record each edge with its evidence. Layer or work type alone (backend before
client, research before implementation, polish after features) is a soft
preference: it may order admission when capacity is scarce, but never holds a
ready issue or adds an edge.

If hard links contradict the user-provided order, pause and ask before executing. If the graph contains a cycle, show the cycle and ask for the edge to break unless issue text clearly resolves it. Do not force unrelated issues into a dependency chain.

## Normal Project Workflow

1. Identify the project, milestone, parent issue, or issue set.
2. Read product artifacts: project brief, milestone plan, issue list, acceptance criteria, dependencies, cutline, risk map, and readiness results.
3. Read engineering context: repo surface, existing modules, known contracts, migrations, build/test topology, active PRs, release branch policy, and CI constraints.
4. Classify every issue:
   - `Ready`: dev-ready and can be assigned to `$dev`.
   - `Blocked`: not dev-ready, or missing a product decision, dependency, API contract, design, access, or upstream work.
   - `WIP`: already being implemented or reviewed.
   - `Awaiting Human Acceptance`: a separate human acceptance deliverable awaits evidence; keep it outside the engineering worker queue and merge barriers. Old labels on implementation issues follow the mode waiver.
   - `Done`: merged or otherwise available on the base branch with mode-required gates satisfied; in fast mode, any skipped human acceptance must already be recorded in controller state and issue closeout.
   - `Unknown`: cannot verify state with available tools.
5. Build the dependency graph from hard edges with their evidence.
   - In default mode, use lightweight issue, repo, branch, and contract evidence.
   - In `--deep-plan` mode, run the Deep Parallelization Plan workflow in the deep-planning reference and use its conflict graph as the dependency graph.
6. Decide the execution order: what is ready now, what each hard edge unlocks, and what can run in parallel under the operating rules, with the reason for each exclusion.
7. Resolve the canonical branch strategy: repository policy first; otherwise
   use one temporary branch per repository for this batch/project/parent. Record
   upstream, issue PR base, promotion target, scope, and ownership. Select and
   record native stack layers/pins and development gates when applicable;
   preserve separate stacks for independent projects or repositories. On execution,
   create/publish or verify/reuse it before dispatch; pass it to every worker.
8. Define risk and validation strategy across conflicts, schema/API contracts, tests, rollbacks, release gates, and the integration checkpoint.
9. If asked to execute, initialize controller state and admit ready `$dev` workers as actual dependencies and verified capacity permit through Controller-Owned Wave Execution in the worker-execution reference.

## Output

For normal project mode:

```markdown
## Engineering Execution Plan

Project:
Milestone:
Mode: <fast | standard | strict>
Skipped / Unverified: <entries or none>
Ready issues:
Blocked / WIP / unknown issues: <issue, gap and owner>

## Dependency Graph
- <Issue A> -> <Issue B>: <hard edge and its evidence>

## Execution Order
Ready now:
Unlocked by a merge: <issue <- predecessor>
Soft ordering preferences: <or none>

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
Native stacks when selected: <trunk, layers/owners/pins, development versus merge gates>

## Risk
File conflicts:
Schema conflicts:
API contract risks:
Testing risks:
Rollback risks:

## Dispatch Plan
- <issue>: use `$dev` with <mode> and <key constraints>
- Integration checkpoint: <timing and owner, or "Not needed">

## Controller State
Controller thread:
Execution mode: <persistent-workers | dispatch-blocked | not started (plan-only)>
Creation/recovery blocker and preserved pending gates:
Active wave:
Worker registry:
Decision comments:
Discovery parent / included blockers / deferred discoveries:
Barrier status:
Wake strategy:
Next unlock condition:
```


## Conditional References And Completion

| Request or pending state | Read |
| --- | --- |
| --deep-plan or explicitly requested verified conflict mapping | [Deep planning](references/deep-planning.md) and its [mapper schema](references/deep-plan-output-schema.md) |
| --sequence, an ordered queue, or merge-before-next scheduling | [Sequence mode](references/sequence-mode.md) |
| Technical decomposition, ticket drafting or persistence | [Ticket preparation](references/ticket-preparation.md) |
| Execution is requested, or an existing worker needs continuation | [Worker execution](references/worker-execution.md), before dispatch, helper work, or accepting a callback |
| Callback, heartbeat, uncertain worker health or a pending external gate needs reconciliation | [Controller recovery](references/controller-recovery.md), including its quiet-return check and host failure boundary |
| Creating, resuming or replacing a persistent worker, choosing its callback or wake transport, a failed dispatch, or an escalation | [Executor sessions](references/executor-sessions.md) for the resolved executor |

A plan-only request finishes at the engineering plan and loads no execution
reference.

Execution completes only when every required issue meets its mode-required
merge/test/acceptance barrier and any planned integration checkpoint passes.
Accept each worker’s cleanup or explicit retention handoff under
[Cleanup Acceptance](references/worker-execution.md#cleanup-acceptance); a
merge barrier passing does not establish worker closeout.
For a temporary batch branch, also require the verified aggregate PR merge and
final handoff from the branch strategy contract; child merges alone do not
complete the project.
Keep every worker's skipped/unverified entries in project state and the final
report in every mode, without a dedicated risk ticket for fast-mode omissions.
An open PR, green CI, stack-ready development admission or worker completion
is never an eligible merge barrier.
