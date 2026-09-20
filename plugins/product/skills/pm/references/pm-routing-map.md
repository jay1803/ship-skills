# Product PM Agent Routing Map

Use this map after the shared routing contract and before the active runtime
adapter. It defines PM task classes in semantic terms; model names remain in the
runtime adapter.

The map applies when PM work is delegated. A narrow PM Skill executed inline
does not replace or downgrade the current controller route.

## Controllers

The invoking `$pm` thread, persistent `$pm-project-orchestrator`, and fresh
issue workers use `lifecycle: controller` and `role: worker`. Classify the whole
owned scope through the shared contract: clear ordinary scope is `standard`,
cross-boundary judgment is `deep`, and the hardest or critical decisions are
`critical`. Every new controller has a minimum `standard` capability tier;
fast models are reserved for bounded work, even when the whole issue is simple.
Controllers retain the `high` reasoning floor; `xhigh` needs an explicit
complexity reason and is never implied by persistence.

The `worker` role describes responsibility for producing and advancing the PM
package; it does not select a bounded worker profile. Controllers retain state
transitions, tracker-write coordination, retries, communication, and completion
at every tier. An inline PM skill does not switch the active controller's model.

All roles inherit available permissions under the shared contract. Coordinate
controller task ownership as follows; these are not permission or approval gates:

- `$pm`: the assigned issue and the PM artifacts its active Skills own;
- `$pm-project-orchestrator`: the bound project, its project fields, milestones,
  membership, dependency graph, and explicitly in-scope issue set;
- fresh issue worker: its assigned issue only, never a project, parent issue,
  milestone, or sibling issue.

## Bounded PM Defaults

| Task or Skill | Default route | Use for |
| --- | --- | --- |
| Known issue, comment, document, or source lookup | `explorer/fast` | Exact target retrieval with little interpretation |
| Issue inventory, source inspection, or competing-match analysis | `explorer/standard` | Read-only evidence gathering across several sources |
| `$pm-bug-triage` | `worker/standard` | Severity, impact, reproduction route, and diagnosis handoff |
| `$pm-release-learning` | `worker/standard` | Bounded release synthesis and follow-up drafts |
| `$pm-scope` | `worker/deep` | Problem, outcome, scope, constraints and tradeoffs |
| `$pm-solution-review` | `reviewer/deep` | Independent same-goal product-solution simplification gate |
| `$pm-spec` | `worker/deep` | Canonical title and product requirement |
| `$pm-data-analytics` | `worker/deep` | Metrics, event semantics, and validation plan |
| `$pm-backlog` | `worker/deep` | Issue decomposition, cutline drafts, and dependency structure |
| `$pm-strategy` | `worker/deep` | Roadmap, portfolio, sequencing, and product-principle decisions |
| `$pm-readiness-review` | `reviewer/deep` | Independent pre-Dev product-readiness gate |
| `$pm-pr-product-review` | `reviewer/deep` | Independent implementation, acceptance, and release gate |
| Exact, already-decided tracker mutation or approved-text posting | `operator/fast` | One low-risk operation with exact target and payload |

`operator/fast` is never the default route for a whole PM Skill. Do not use it
when the task must classify, infer scope, compose substantive content, choose a
status, edit a canonical title or description, or decide the next PM phase.

`reviewer/standard` may be used for an ordinary independent check of a low-risk
artifact. The canonical readiness and product-review gates remain
`reviewer/deep`. Apply the shared judgment-review capability floor to the
specific producing decisions; deterministic checks do not establish that
architecture or acceptance criteria are complete.

`architect/deep` is not a default PM route. Use it only when evidence reveals a
genuine cross-system technical contract or ownership conflict. Return the
result to `$pm-scope` / `$pm-spec`, `$dev`, or the appropriate controller; the
architect does not take over PM lifecycle or tracker ownership.

## Requirements, Permissions, And Writes

Select requirements from the actual payload. PM delegation commonly needs
`tracker-read`, `tracker-write`, `browser`, or `network`; repository-backed
product investigation may also need `repo-read`.

Use `permissions: inherit` and `write_scope: task` by default for every role,
including exploration and review. Carry only explicit user restrictions or
enforced runtime limits as narrower permissions. The task determines the
requested artifact and targets; coordinate writers for the same issue, canonical
description, PM thread, or other source-of-truth artifact without asking the
user to authorize each handoff again.

## PM Escalation

Use the shared escalation result shape and separate task-wide allowances:
one effort adjustment and one capability escalation by default. Preserve used
counters across redispatches; neither allowance resets the other.

- `explorer/fast` -> `explorer/standard` when the known target expands into
  multi-source evidence gathering.
- `explorer/standard` -> `worker/deep`, `reviewer/deep`, or `architect/deep`
  when the task crosses from gathering evidence into product judgment,
  independent gating, or technical contract resolution.
- `worker/standard` -> `worker/deep` when evidence is conflicting, requirements
  are materially ambiguous, or the decision involves privacy, security, data
  loss, irreversible scope, or major product judgment.
- `operator/fast` -> `worker/standard` or `worker/deep` when the operation
  requires interpretation, content composition, or a state decision.

Escalation may change role, capability tier, or reasoning depth. It must not
silently expand permissions, `write_scope`, phase ownership, or the controller's
authorized tracker surface.

## PM Delegation Envelope

Every delegated PM prompt must include the full shared routing envelope plus:

```yaml
pm_skill: <exact PM Skill or supporting task>
target_artifact: <one bounded artifact or operation>
sources: <issue IDs, comments, documents, PRs, URLs, or paths>
pm_thread: <root comment ID or URL, or none>
allowed_writes: <exact fields, comments, or none>
forbidden_writes: <explicit adjacent targets>
validation: <evidence or re-fetch required before return>
stop_conditions: <complete, blocked, or escalation boundary>
```

Record the requested route and the actual runtime, model, and reasoning binding
in an existing worker registry or handoff. Publish the shared request and
resolved routing notices for every dispatch. For a one-off bounded delegation
without a registry, require the shared routing receipt in the returned result.
