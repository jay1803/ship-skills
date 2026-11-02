# Sequence Scheduling

Read when `--sequence`, a request to merge issues one by one, or an explicit
merge-before-next queue is requested. Ordered dependency edges or a native PR
stack alone do not select it; apply the
[stack contract](../../dev/references/stacked-prs.md) for a selected stack.
Delivery mode is independent. Execution follows
[worker execution](worker-execution.md); this file records only what sequence
scheduling changes. Plan-only creates no goal, branch or worker.

- **Queue.** Use the user's ordered issue list, or derive a safe order from the
  live scope's hard edges. Serialize unrelated issues only when the user asks
  for one ordered queue, and label that order as serialization, not dependency.
- **One issue at a time.** Dispatch the next issue only after the current one
  is verified merged into its resolved issue PR base under the mode's barrier;
  a held merge, a stack-ready layer or an open PR keeps the queue waiting.
  Fetch and fast-forward the base before each dispatch so the next worker
  builds on the merged predecessors.
- **Handoff additions.** Add the already-merged list and cross-issue notes
  (contracts, naming, gotchas) to the standard worker handoff.
- **Stop.** When the current issue exhausts its retry ceiling, stop the
  sequence; later issues are not dispatched.
- **Production promotion.** If an issue PR is a repository-defined production
  promotion, stop before dispatch and route it to `$release`.
- **Finish.** After the last issue, run the branch strategy's integration
  checkpoint before reporting sequence completion.

```markdown
## Sequence State

Controller thread:
Current issue / worker thread:
Mode: <fast | standard | strict>
Skipped / Unverified: <entries or none>
Repo / base branch:
Already merged:
Remaining:
Retry attempt:
Dependency evidence: <Issue A before Issue B because <evidence or "requested serialization">>
Current issue result: <PR, validation, merge/test handoff, merge commit; merged | held | no>
Next action: <dispatch next worker | wait for callback, heartbeat or held merge | complete | stopped and why>
```
