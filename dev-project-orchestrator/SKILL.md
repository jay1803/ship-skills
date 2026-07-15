---
name: dev-project-orchestrator
description: >-
  Engineering/project orchestrator for multiple dev-ready Linear issues, milestones, project issue sets, and strict dependency sequences. Use when work spans several issues and needs implementation order, dependency analysis, Direct/Serial/Parallel/Blocked decisions, controller-owned execution waves, merge barriers, safe $dev dispatch, integration planning, or strict sequence mode where issues must be built and merged one at a time before the next starts. Also supports opt-in deep parallelization planning with --deep-plan for verified mapper/graph/verifier analysis; this deep mode is not the default. Accepts simple commands such as $dev-project-orchestrator --sequence AG-1 AG-2 AG-3 --fast and can analyze Linear projects or milestones directly without a separate prompt generator.
---

# Dev: Project Orchestrator

Plan and control engineering execution for project-level issue sets. This skill decides order, batching, branch strategy, integration checkpoints, wave barriers, and strict sequence progression. Each individual coding issue is still executed by `$dev`.

## Command Forms

- `$dev-project-orchestrator <project, milestone, parent issue, or issue list>`: analyze dependencies and produce an engineering execution plan.
- `$dev-project-orchestrator --plan-only <scope>`: analyze order, batches, risks, and branch strategy without starting implementation.
- `$dev-project-orchestrator --deep-plan <scope>`: opt into read-only mapper JSON, schema validation, conflict graph construction, verifier review, and wave planning before implementation.
- `$dev-project-orchestrator --sequence <ISSUE-1> <ISSUE-2> <ISSUE-3> [--fast|--slow]`: execute a strict serial chain. Build and merge the current issue before starting the next.
- `$dev-project-orchestrator --sequence <project or milestone> [--plan-only]`: inspect live Linear scope, derive the safe dependency order, then either show the sequence plan or execute it if the user asked to build.

Default mode is `--fast` with lightweight project planning. Use `--slow` only when the user asks for standard/full/hands-on QA. Use deep planning only when the user explicitly requests `--deep-plan`, verified conflict mapping, or a similarly deep parallelization report.

## Boundary

- Use this skill for multiple issues, a Linear project, a milestone, an epic, dependency-heavy issue family, or strict ordered sequence.
- Use `$dev` directly for one dev-ready issue.
- Use `$pm-project-orchestrator` when the project brief, cutline, milestones, issue setup, or PM assignment plan is missing.
- Use `$pm-readiness-review` for child issues whose product readiness is unclear.
- Use `$dev-spike` or `$dev-api-research` for project-level unknowns that block architecture or sequencing.
- Use `$dev-api-steward` or require `$dev` workers to run it when project work changes internal API behavior, OpenAPI/Swagger, generated clients, docs, changelog, versioning, migrations, or client compatibility.
- Use `$dev-integration-manager` when multiple PRs/branches need merge ordering, combined validation, cross-branch conflict handling, API contract checks, or an integration branch.
- Do not implement production code in this skill. Control the project path and invoke `$dev` for issue-level implementation.

## Operating Rules

- Verify live Linear, GitHub, repo, branch, PR, and CI state before making current-state claims.
- Treat dependencies as a graph. Mark each issue `Ready`, `Blocked`, `WIP`, `Done`, or `Unknown` with evidence.
- Parallelize only when issues are independently buildable, contracts are stable, file ownership does not overlap, and merge order is known.
- Do not parallelize work that changes the same files, migrations, schemas, generated outputs, package/project files, API contracts, product decisions, or release gates.
- Do not parallelize backend/API contract changes with dependent client changes until the API contract is stable and the API Steward checkpoint is planned.
- Do not run deep planning by default. For high-risk or unclear multi-slice work, recommend deep planning and ask before running it unless the user already requested it.
- In deep planning mode, keep all work read-only against production code. Temporary mapper JSON and graph artifacts may be written only under `/tmp` or another clearly disposable planning directory.
- Every implementation worker must use `$dev` and receive exactly one concrete Linear issue ID.
- Keep the invoking thread as the persistent project controller. The controller alone owns the dependency graph, worker registry, wave barriers, retries, successor dispatch, and project completion.
- By default, run each issue-level `$dev` implementation in a fresh Codex thread created with the thread-management tool, including the first executable issue.
- Workers must never dispatch successor issues. They implement one issue, reach a terminal result, and report that result to the controller.
- If fresh thread creation is unavailable, continue the issue in the current thread only after clearly reporting the heavier-context fallback.
- Prefer fast mode for `$dev` workers unless the project plan explicitly requires standard hands-on QA.
- If project execution will produce multiple PRs with shared behavior, plan the `$dev-integration-manager` checkpoint before merge.

## Fresh Thread Handoff

When this skill needs a fresh issue thread:

1. Use the Codex thread-management tool directly.
   - If the create-thread tool is not already available, search for it first with `tool_search` using `create_thread`.
   - Create one new thread per ready issue in the current saved project. Dispatch every member of the same safe wave before waiting.
   - Use a local environment unless the user explicitly asks for a new worktree.
   - For an explicit worktree request, use the worktree environment and preserve requested branch or starting-state details when the tool supports them.
2. Include the controller thread id and worker callback packet in the initial prompt. Resolve the controller id with the thread-management tools; do not guess when multiple threads could match.
3. Use the worker handoff as the new thread's initial prompt without adding summaries, hidden instructions, or extra commentary.
4. Record the returned worker thread id against the issue before creating another worker or yielding.
5. Do not execute a worker payload in the controller thread after its fresh thread was created.
6. After dispatching the complete ready wave, report all worker thread ids and enter the Controller-Owned Wave Execution workflow.
7. If direct worker callbacks are unavailable, continue with controller heartbeat monitoring instead of decentralizing successor dispatch.
8. If the current project id is unavailable and the thread tool cannot infer it, ask one short question for the target project instead of falling back to a projectless thread.

## Controller-Owned Wave Execution

Use this state machine for normal project batches and strict sequence mode. Treat a strict sequence as waves containing exactly one issue.

1. Initialize controller state before dispatch:
   - Controller thread id.
   - If the id is not directly available, give the controller a unique project-specific title, then use the thread listing and reading tools to resolve it unambiguously.
   - Ordered dependency graph and wave membership.
   - Per-issue state: `Pending`, `Dispatched`, `Merged`, `Blocked`, or `Stopped`.
   - Worker thread id, retry count, PR URL, merge commit, validation result, and blocker.
   - A `dispatched` marker for every issue to prevent duplicate thread creation.
2. Dispatch every currently ready issue once. Key the worker registry by Linear issue ID and record the thread id immediately.
3. Wait for worker callbacks. A callback wakes the controller; it does not authorize the worker to dispatch another issue.
4. On every callback or heartbeat:
   - Read the reporting worker thread.
   - Verify live Linear, GitHub, PR, CI, and base-branch merge state.
   - Update the matching registry entry.
   - Re-evaluate the entire active wave, not only the reporting worker.
5. Open a barrier only when every issue in the active wave is verified `Merged`. Thread completion, an open PR, green CI without merge, or a worker's unsupported claim is not sufficient.
6. Before dispatching unlocked successors, re-read controller state and live issue/PR state. Dispatch only issues still `Pending` with all hard predecessors `Merged` and no existing worker, branch, or PR that represents active work.
7. Dispatch the newly ready wave exactly once, then wait again. Never let workers decide that they were the last finisher.
8. If a worker reports `Blocked` or fails to merge, keep dependent issues closed. Resume the same worker with its existing branch, worktree, PR, checks, and evidence for up to five total attempts. Mark the project `Stopped` after attempt five and report the blocked downstream issues.
9. Complete the project only when all required issues are verified `Merged` and any planned integration checkpoint passes.

### Wake Strategy

- Prefer event-driven callbacks: instruct each worker to use the thread messaging tool to send the Worker Callback Packet to the controller after merge or a concrete blocker.
- Use a heartbeat attached to the controller thread as a recovery mechanism while workers are active. On wake, inspect every active worker and live PR state so missed callbacks, interrupted workers, and externally merged PRs can still advance the graph.
- Do not poll continuously. Use a reasonable heartbeat interval and remove or disable the heartbeat when no workers are active, the project completes, or the project stops.
- If neither callbacks nor heartbeat automation is available, report that automatic continuation is unavailable and ask the user to resume the controller. Do not transfer orchestration ownership to a worker.

### Barrier Example

```text
Wave 1: MO-480, DS-24, MO-475, MO-478
Barrier: all four verified merged
Wave 2: MO-474
Barrier: MO-474 verified merged
Wave 3: MO-473, MO-476
Barrier: both verified merged
Wave 4: MO-477, MO-481
```

## Dependency Analysis

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

Do not force unrelated issues into a dependency chain. In normal project mode, use independent batches. In strict sequence mode, serialize unrelated work only when the user explicitly asks for one ordered queue, and label it as serialization rather than dependency.

## Normal Project Workflow

1. Identify the project, milestone, parent issue, or issue set.
2. Read PM artifacts: project brief, milestone plan, issue list, acceptance criteria, dependencies, cutline, risk map, and readiness results.
3. Read engineering context: repo surface, existing modules, known contracts, migrations, build/test topology, active PRs, release branch policy, and CI constraints.
4. Classify every issue:
   - `Ready`: dev-ready and can be assigned to `$dev`.
   - `Blocked`: missing product decision, dependency, API contract, design, access, or upstream work.
   - `WIP`: already being implemented or reviewed.
   - `Done`: merged or otherwise available on the base branch.
   - `Unknown`: cannot verify state with available tools.
5. Build the dependency graph with explicit edge reasons.
   - In default mode, use lightweight issue, repo, branch, and contract evidence.
   - In `--deep-plan` mode, run the Deep Parallelization Plan workflow below and use its conflict graph as the dependency graph.
6. Create execution batches:
   - Batch 0: research, API research, spike, contract clarification.
   - Batch 1: foundation/backend/schema/shared contract.
   - Batch 2: parallel clients/features that depend on stable foundations.
   - Batch 3: integration, polish, edge cases, data migration cleanup.
   - Batch 4: release hardening, combined validation, rollout/rollback checks.
7. Decide parallelization. Name what can run together, what cannot, and why.
8. Define branch strategy: base branch, per-issue branches, integration branch if needed, merge order, and PR ownership.
9. Define risk and validation strategy across conflicts, schema/API contracts, tests, rollbacks, and release gates.
10. For API-changing batches, require the relevant `$dev` worker to run `$dev-api-steward` and return contract/docs/changelog/client-impact results before dependent client batches proceed.
11. If asked to execute, initialize controller state and dispatch `$dev` workers wave-by-wave through Controller-Owned Wave Execution. Run `$dev-integration-manager` before merge when multiple PRs interact or combined validation is required.

## Deep Parallelization Plan

Use this workflow only for `--deep-plan` or an explicit user request for verified conflict mapping. This mode is intentionally heavier than the default project plan.

1. Intake.
   Resolve each issue, PR, branch, parent issue, or feature slice into a concise implementation hypothesis. For a parent issue, inspect child issues and preserve the user's slicing unless the existing split is unusable. If tracker access is unavailable, state what could not be verified and continue from provided text only when the local implementation surface can still be inspected.
2. Map slices.
   Spawn one `slice_mapper` subagent per issue or slice when subagent tools are available. Give each mapper one slice, the repo path, relevant base/target branch details, and `references/deep-plan-output-schema.md`. Require read-only repo inspection and JSON-only output.
3. Normalize mapper outputs.
   Save each mapper output as a separate JSON file in a disposable planning directory. Run:

   ```bash
   node scripts/validate_deep_plan_json.ts /path/to/mapper-outputs/*.json
   ```

   If validation fails, ask the responsible mapper for corrected JSON using the reported errors. Do not manually patch mapper findings unless the error is purely formatting and the source answer is unambiguous.
4. Build the conflict graph.
   Run:

   ```bash
   node scripts/build_deep_conflict_graph.ts /path/to/mapper-outputs/*.json
   ```

   Use the graph to detect `same_file_conflict`, `same_symbol_conflict`, `API_contract_dependency`, `schema_or_migration_dependency`, `test_dependency`, and `product_scope_dependency`.
5. Synthesize execution waves.
   - Wave 0: contracts, schemas, migrations, shared fixtures, generated outputs, prerequisites, or decisions that must stabilize first.
   - Wave 1: safe parallel work with disjoint files, symbols, contracts, and validation paths.
   - Wave 2: dependent work that waits for Wave 0 or Wave 1 outputs.
   - Wave 3: integration, regression verification, conflict resolution, end-to-end QA, and final merge sequencing.
6. Verify the draft.
   Spawn one `plan_verifier` subagent when subagent tools are available. Ask it to disprove the draft plan using mapper JSON and the conflict graph, focusing on hidden coupling, unsafe parallelism, missing tests, wrong wave ordering, shared generated files, lockfile conflicts, schema/API drift, and product-scope overlap.
7. Finalize.
   Incorporate verifier findings. If subagent tools were unavailable, state that mapping or verification was performed locally rather than independently. Separate verified facts from assumptions and name missing information that could change execution order.

### Mapper Prompt

```markdown
You are a slice_mapper for a read-only deep parallelization plan.

Slice: <issue id, PR, branch, or feature slice>
Repo: <absolute repo path>
Base/target: <branches if known>

Inspect the repo read-only. Do not edit files, create branches, run migrations, or implement anything.
Return JSON only, matching dev-project-orchestrator/references/deep-plan-output-schema.md.

Focus on likely touched files, symbols, contracts, migrations, tests, runtime dependencies, product dependencies, validation commands, and whether this slice is safe to run in parallel.
```

### Verifier Prompt

```markdown
You are a plan_verifier for a read-only deep parallelization plan.

Inputs:
- Mapper JSON outputs: <paths or pasted JSON>
- Conflict graph: <path or pasted JSON>
- Draft wave plan: <draft>

Try to disprove the plan. Identify hidden coupling, unsafe parallelism, missing tests, missing prerequisites, wrong wave ordering, merge-order risks, and cases where a shared API/schema/product contract must be stabilized first.
Return findings ordered by severity and include concrete evidence.
```

## Strict Sequence Mode

Use strict sequence mode when the user says `--sequence`, provides ordered blocking issues, says the work is stacked, says "one by one", or asks to merge each issue before starting the next.

Strict sequence mode replaces the previous standalone sequence flow:

- Run exactly one current issue per thread.
- Build the current issue on top of the latest base branch, usually `develop`.
- Keep the invoking thread as controller and start the first issue in a fresh worker thread.
- Require the current issue's PR to merge through `$dev-release-handoff` before starting the next issue.
- Retry blockers on the same current issue up to five times before stopping the sequence.
- Require each worker to report its result to the controller. The controller verifies the merge and dispatches the next worker.
- Never start issue N+1 until issue N is merged.

### Sequence Inputs

- Require an ordered list of issue IDs, or a Linear project/milestone that can be analyzed into a safe order.
- Controller state must carry already merged issues, remaining issues, mode, repo/base branch, retry count, worker thread ids, and cross-issue notes.
- If a user gives only one dev-ready issue and this is not part of a project or sequence, use `$dev` directly instead of `$dev-project-orchestrator`.

### Sequence Workflow

1. Start or reuse one active goal in the controller for the complete sequence.
   - The goal covers every current issue, retry, merge result, successor dispatch, and sequence completion.
   - Workers do not create sequence goals or dispatch successors.
2. Establish the queue.
   - Parse the issue list or derive it from Linear scope.
   - Record already merged issues, remaining ordered list, mode, repo/base branch, worker registry, and cross-issue notes in controller state.
   - Echo current issue, already merged issues, remaining issues, mode, repo/base branch, and the five-retry stop rule.
3. Sync the base branch before building.
   - Run `git fetch origin`.
   - Fast-forward the local base branch when possible so it includes previously merged sequence work.
4. Dispatch the current issue through the Fresh Thread Handoff workflow and record its worker thread id.
   - Mode is fast unless `--slow` selected standard mode.
   - Pass issue ID, repo path, base branch, already merged predecessor list, cross-issue notes, and "must reach merged PR or concrete blocker".
   - `$dev` owns branch/worktree setup, implementation, validation, PR creation, code review, `$dev-fix`, `$dev-ci-repair`, `$pm-pr-product-review`, and `$dev-release-handoff`.
5. Wait for the callback or heartbeat, then gate the result in the controller.
   - Proceed only after live verification that `$dev` produced a PR to the base branch and merged it through `$dev-release-handoff`.
   - If no PR merged, retry the same issue under Retry Policy.
6. Record the merge.
   - Capture issue ID, PR URL, head branch, validation/QA result, release handoff result, and squash commit.
   - Add this issue to the already-merged list.
7. Continue or finish from the controller.
   - If issues remain, sync the base again and dispatch only the next issue in a fresh worker thread.
   - If this was the last issue, disable the heartbeat and report the whole sequence summary.

### Retry Policy

- Treat the first build/merge pass as attempt 1.
- Retry blockers up to five total attempts for the current issue.
- Retry when `$dev` produces no merged PR, PR Product Review fails, validation fails, review comments remain unresolved, conflicts remain unresolved, checks are red, or `$dev-release-handoff` cannot merge.
- Reuse the existing branch, worktree, PR, validation output, review comments, and merge-gate error. Do not restart blindly.
- Keep every retry scoped to the current issue.
- If all five attempts fail, stop the sequence and do not dispatch later issues.

### Sequence Worker Invocation Shape

```markdown
Use $dev to resolve exactly one Linear issue end to end.
Mode: <fast unless --slow was selected, then standard>.

Context:
- Controller thread: <thread id>
- Assigned issue: <Linear issue ID and title>
- Repo: <repo path>
- Base branch: <base branch, usually develop>
- Already merged in this sequence: <list or "none yet">
- Cross-issue notes: <contracts, naming, gotchas, or "none">

Run the full $dev workflow inline: set up the issue branch from the base branch, implement, validate, run the mode-appropriate QA bar, create a PR to the base branch, run code review, fix conflicts and failing checks, address valid review comments, run final PR Product Review, and land the PR through $dev-release-handoff.

After reaching a merged PR or concrete blocker, send the Worker Callback Packet to the controller thread. Do not start, create, or message any successor issue thread.
```

## Worker Handoff Shape

For non-sequence project batches, send this shape to each issue-level worker in a fresh Codex thread by default:

```markdown
Use $dev.
Mode: <fast by default, or standard only if required>.

Project:
Controller thread:
Assigned issue:
Wave / batch:
Base branch:
Dependencies already satisfied:
Assigned scope:
Expected touched areas:
Do not touch:
Validation required:
Integration notes:
API Steward expectations:
Stop and report if:

Resolve exactly this issue through the $dev workflow. After reaching a merged PR or concrete blocker, send the Worker Callback Packet to the controller thread. Do not create or dispatch successor issue threads.
```

## Worker Callback Packet

Require every normal-batch and strict-sequence worker to send this packet to the controller with the thread messaging tool:

```markdown
Dev project worker callback
- Project: <project>
- Issue: <issue id>
- Worker thread: <thread id>
- Attempt: <number>
- Status: <merged | blocked>
- PR: <number and URL, or none>
- Head branch: <branch>
- Validation / QA: <result>
- Release handoff: <result>
- Merge commit: <commit, or none>
- Blocker and attempted fix: <details, or none>
- Integration notes: <notes, or none>

Controller action: verify this result against live Linear, GitHub, CI, and base-branch state; update the full active-wave barrier; dispatch unlocked successors only if the barrier is satisfied.
```

## Output

For normal project mode:

```markdown
## Engineering Execution Plan

Project:
Milestone:
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
Integration branch if needed:
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
Active wave:
Worker registry:
Barrier status:
Wake strategy:
Next unlock condition:
```

For deep planning mode:

```markdown
## Conflict / Dependency Graph
- <edge or dependency summary with issue IDs and reason>

## Wave Plan
### Wave 0 - Contracts / Schema / Prerequisites
- <issue or task> - <why first>

### Wave 1 - Safe Parallel Work
- <issue> - <owner/scope/validation>

### Wave 2 - Dependent Work
- <issue> - <waits for what>

### Wave 3 - Integration / Regression Verification
- <validation and merge sequencing>

## Assignment Recommendations
- <issue> - <parallel/serial/blocked recommendation, expected files, validation>

## Verification Notes
- <verifier finding or "No hidden blockers found">

## Missing Information
- <assumption or unavailable source that could change execution order>
```

For strict sequence mode:

```markdown
## Strict Sequence State

Controller thread:
Current issue:
Worker thread:
Mode:
Repo / base branch:
Already merged:
Remaining:
Retry attempt:

### Dependency Evidence
- <Issue A> before <Issue B> because <evidence>

### Current Issue Result
- PR:
- Validation / QA:
- Release handoff:
- Squash commit:
- Merged: <yes | no>

### Next Action
<controller dispatches next worker | wait for callback or heartbeat | sequence complete | stopped>

### Stop Reason
<only if stopped>
```
