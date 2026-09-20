# Sequence Scheduling

Read when --sequence, an ordered queue, or merge-before-next scheduling is requested. Plan-only does not authorize goal creation, worker dispatch, or issue execution. For execution, also read [worker-execution.md](worker-execution.md).

## Sequence Mode

Use sequence mode when the user says `--sequence`, provides ordered blocking issues, says the work is stacked, says "one by one", or asks to merge each issue before starting the next. This scheduling mode is independent of delivery evidence depth.

Sequence mode replaces the previous standalone sequence flow:

- Run exactly one current issue per thread.
- Build the current issue on top of the latest resolved issue PR base.
- Keep the invoking thread as controller and start the first issue in a fresh worker thread.
- Require the current issue's PR to merge into the resolved issue PR base through `$dev-merge-handoff` before starting the next issue.
- If the requested PR is a repository-defined production promotion, stop
  before dispatch and route the production-promotion request to `$release`;
  issue sequencing must not bypass the repository release policy.
- Retry blockers on the same current issue up to five times before stopping the sequence.
- Require each worker to report its result to the controller. The controller verifies the merge and dispatches the next worker.
- Never start issue N+1 until issue N is merged.

### Sequence Inputs

- Require an ordered list of issue IDs, or a Linear project/milestone that can be analyzed into a safe order.
- Controller state must carry already merged issues, remaining issues, mode, repo/base branch, retry count, worker thread ids, and cross-issue notes.
- If a user gives only one dev-ready issue and this is not part of a project or sequence, use `$dev` directly instead of `$dev-project-orchestrator`.

### Sequence Workflow

1. Record or reuse one project objective in controller state for the complete sequence, following the goal-tool boundary in [Controller-Owned Wave Execution](worker-execution.md#controller-owned-wave-execution).
   - The objective covers every current issue, retry, merge result, successor dispatch, and sequence completion; it does not require goal auto-continuation.
   - Workers do not own the sequence objective or dispatch successors.
2. Establish the queue.
   - Parse the issue list or derive it from Linear scope.
   - Record already merged issues, remaining ordered list, mode, repo/base branch, worker registry, and cross-issue notes in controller state.
   - Echo current issue, already merged issues, remaining issues, mode, repo/base branch, and the five-retry stop rule.
3. Sync the base branch before building.
   - Run `git fetch origin`.
   - Fast-forward the local base branch when possible so it includes previously merged sequence work.
4. Dispatch the current issue through the Fresh Thread Handoff workflow and record its worker thread id.
   - Mode is the resolved fast, standard, or strict delivery mode; omitted means standard.
   - Pass issue ID, repo path, resolved issue PR base, already merged predecessor list, cross-issue notes, and "must reach merged PR against the resolved issue base with the mode-required test handoff, or a concrete blocker".
   - `$dev` owns branch/worktree setup, implementation, validation, PR creation, mode-appropriate review gates, `$dev-implementer`, `$dev-ci-repair`, and `$dev-merge-handoff`.
5. Wait for the callback or heartbeat, then gate the result in the controller.
   - Proceed only after live verification that `$dev` produced a PR to the resolved issue PR base and the PR is merged.
   - Apply the mode contract before accepting `merged awaiting test deploy` or
     `merged awaiting human acceptance`. For waived real-environment/human tests,
     verify the skip and any follow-up are recorded, then treat the merged
     implementation as barrier-complete and dispatch its successor. Keep separate
     human acceptance tickets outside the coding queue. Wait only for a remaining
     required gate, such as technically enforced CI/deployment or merge authority.
   - If no PR merged, retry the same issue under Retry Policy.
6. Record the merge.
   - Capture issue ID, PR URL, head branch, validation/QA result, merge/test handoff result, integration commit, and release-candidate evidence.
   - Add this issue to the already-merged list.
7. Continue or finish from the controller.
   - If issues remain, sync the base again and dispatch only the next issue in a fresh worker thread.
   - If this was the last issue, run the batch integration/promotion closeout from the branch strategy contract before reporting sequence completion; preserve any required review or final handoff wait.

### Retry Policy

- Treat the first build/merge pass as attempt 1.
- Retry blockers up to five total attempts for the current issue.
- Retry when `$dev` produces no merged PR against the resolved issue base and a mode-required or unskippable gate fails. Product Review and ordinary review comments trigger retries only in standard mode; fast mode retries them only when they reveal an unskippable critical/primary-path issue. Do not count standard test deployment, outcome verification, or human acceptance waiting as an implementation retry.
- Reuse the existing branch, worktree, PR, validation output, review comments, and merge-gate error. Do not restart blindly.
- Keep every retry scoped to the current issue.
- If all five attempts fail, stop the sequence and do not dispatch later issues.

### Sequence Worker Invocation Shape

```markdown
Use $dev to resolve exactly one Linear issue end to end.
Mode: <fast | standard | strict; standard when omitted>.
Skipped / Unverified: <entries or none>.

Context:
- Controller thread: <thread id>
- Routing binding: <requested semantic route/capability/reasoning/executor/profile/model/profile-fallback policy plus accepted executor/model/reasoning/profile and separate fallbacks>
- Routing receipt required: use the shared agent-routing receipt in the callback
- Assigned issue: <Linear issue ID and title>
- Validation required: <mode-selected checks; source for explicit additions; no automatic standard reverse-red or unrelated edge-case matrix; when the phase plan or repository policy requires technical Review, the combined Review V2 result accepted on the exact PR head to be merged; otherwise carry the mode/preset or explicit exception and its required omission disclosure>
- Branch strategy: <policy source, scope, upstream, issue PR base, temporary branch, promotion target>
- Repo: <repo path>
- Base branch: <resolved issue PR base>
- Already merged in this sequence: <list or "none yet">
- Cross-issue notes: <contracts, naming, gotchas, or "none">

Run the mode-appropriate $dev workflow inline: set up the issue branch from the resolved issue PR base, implement, validate, create a PR targeting the resolved issue PR base, satisfy enforced gates, and land it through $dev-merge-handoff. In fast mode, return all skipped/unverified entries to the controller. Do not perform production promotion from this issue worker; route production release to `$release`.

After reaching a merged PR against the resolved issue base with its mode-required test handoff, or a concrete blocker, send the Worker Callback Packet to the controller thread. Do not start, create, or message any successor issue thread.
```

For sequence mode:

```markdown
## Sequence State

Controller thread:
Current issue:
Worker thread:
Mode: <fast | standard | strict>
Skipped / Unverified: <entries or none>
Repo / base branch:
Already merged:
Remaining:
Retry attempt:

### Dependency Evidence
- <Issue A> before <Issue B> because <evidence>

### Current Issue Result
- PR:
- Validation / QA:
- Merge/test handoff:
- Squash commit:
- Merged: <yes | awaiting release merge | awaiting human acceptance | no>

### Next Action
<controller dispatches next worker | wait for release merge | wait for callback or heartbeat | sequence complete | stopped>

### Stop Reason
<only if stopped>
```
