# Jev Issue Routing Policy

Consumed by the routing program, not by the executing model.

# Issue Router

Select exactly one workflow owner before PM, Dev, or a project controller starts.
The router is thin, deterministic, inline, and read-only: it binds the request's
terminal intent, classifies whether change-capable issue scope is one coherent
delivery or a provisional umbrella, produces one canonical receipt, then stops.
It is not a Skill-DAG planner, agent dispatcher, or replacement for downstream
gates.

## Boundary

- Do not create agents, threads, goals, branches, worktrees, commits, PRs,
  tracker comments, tracker state changes, files, or any other external write.
- Do not perform repository-wide search, architecture, implementation planning,
  PM readiness, child-issue design, Dev phase planning, Review, Release
  execution, or runtime/model routing.
- Select workflow ownership and terminal intent only. `$agent-routing` runs
  later, inside the selected workflow, and keeps its executor/model/profile
  receipt separate. The router does not select a Dev phase plan.
- Preserve one writer: this receipt grants no authority that the next owner did
  not already have.

## Read Budget

Use the smallest current evidence that distinguishes a fixed route.

- A no-target Direct Artifact/Patch request needs no tracker read.
- For one explicit issue, parent, project, or issue set, read the
  bound target once and only its router-relevant state. For a change-capable
  issue, that read includes the canonical outcome, acceptance boundary, named
  delivery targets, unresolved external product decisions, and asynchronous
  human/credential gates needed by the Delivery Shape Precheck.
- Read the canonical PM root/readiness/handoff and one linked branch/PR head,
  check, review, or merge state only when needed to distinguish PM, resume, or
  post-PR ownership.
- Do not search for a different issue, scan installed skills, or ask other
  agents to fill an evidence gap. If the minimum state cannot select one route,
  return `blocked`.

## Delivery Shape Precheck

For change delivery, apply
[Acceptance Classification](../../pm-spec/references/acceptance-policy.md#unattended-engineering-acceptance)
to the bound evidence: standard is unattended, and waived real-device/account/
environment or human testing does not itself create a blocked or multi route.
A recorded deferred human acceptance follow-up stays outside the included coding
inventory; its missing dev readiness does not block `project/dev`. Preserve
actual product/implementation dependencies and standalone verification intent.

Before applying the Fixed Decision Table, classify the delivery shape for every
bound issue that could enter PM or Dev change delivery. Status-only, terminal
investigation/verification, policy-permitted release, and no-target Direct
requests retain their higher-priority routes; the shape still prevents a
change-capable umbrella issue from reaching single-issue Dev.

Use exactly one classification:

- `single`: one coherent product or operator outcome has one shared acceptance
  boundary. Its implementation surfaces cannot be independently accepted,
  deferred, or rolled back without leaving that outcome incomplete.
- `multi`: current canonical evidence identifies at least two independently
  valuable delivery outcomes that can be accepted, deferred, or rolled back
  separately. For a target currently modeled as one issue, preserve that issue
  as the provisional umbrella and select `project/pm`; PM owns the actual
  decomposition and tracker writes.
- `ambiguous`: current evidence suggests more than one delivery outcome, or an
  unresolved provider/auth/model/product decision changes the implementation
  boundary, but the one permitted read cannot prove a safe split. For a
  change-capable single issue, select `project/pm` so Product can resolve the
  boundary before Dev. If even the target or evidence source is unavailable or
  contradictory, use `blocked/*` instead.

When signals overlap, apply this precedence: if at least two independent
outcomes are already proven, classify `multi` even when one outcome also has an
unresolved provider/auth/model/product decision. Use `ambiguous` only when the
outcome boundary itself is not yet proven. This keeps Readiness deterministic:
a proven need for decomposition routes as `multi`; boundary uncertainty remains
PM work without pretending a split was accepted.

Strong evidence for `multi` requires independent outcome boundaries, not a
counting heuristic. Useful signals include independently usable results,
separate acceptance owners or authorities, independently deferrable or
reversible delivery units, multiple repositories or hosts that each produce a
usable result, and asynchronous device/credential/real-environment work whose
failure does not invalidate completed implementation. A combination of these
signals may establish `multi`; a single weak signal does not.

Asynchronous proof is not automatically a separate outcome. A device, host,
credential, deployment, or human-verification activity that only proves the
same shared acceptance remains part of `single`, even when it happens later.
It contributes to `multi` only when it is itself an independently acceptable,
deferrable operational delivery with a distinct owner or authority and its
failure does not invalidate another completed outcome.

Do not classify `multi` solely because work crosses backend/frontend/test
layers, uses several files or technologies, has a large estimate, is expected
to use several commits or PRs, or includes ordinary synchronous QA for the same
end-to-end result. Never split one outcome into design, implementation, and QA
phase tickets.

This precheck identifies workflow shape only. It does not name child issues,
design their scopes, mutate the tracker, build a dependency graph, or select an
agent, model, capability, reasoning level, executor, or Dev phase.

An explicit request to materialize an accepted engineering task plan binds its
owning issue as the proposed `parent` target, even before child IDs exist. The
same product outcome remains `single` when appropriate; technical task count
does not redefine product shape. Use the existing project row below: incomplete
child inventory/readiness routes to `project/pm` for engineering materialization.
Once coding children are materialized and currently ready, an explicit Dev
request for that inventory may select `project/dev`. Exclude its container
parent and deferred design-only work from coding workers while retaining parent
acceptance and dependencies. An ordinary one-issue request without this
materialization intent keeps its existing route. Routing supplies no write grant.

## Fixed Decision Table

Apply the first matching row. `family`, `variant`, and `next_owner` must be one
of these values; never invent an arbitrary Skill chain.

| Priority | Current evidence | Family / variant | Next owner |
| --- | --- | --- | --- |
| 1 | Read-only status, explanation, or non-fresh audit request; or a Done/merged issue without explicit follow-up scope | `status` / `read-only` | current agent / Linear reader |
| 2 | Explicit production promotion, version/tag, or authorized production/main deployment mutation that is within repository policy | `release` / `release` | `$release` |
| 3 | The requested target or action authority cannot be identified/bound, evidence sources are contradictory, or resolving status would require an unapproved live side effect | `blocked` / `clarify`, `decision`, `authority`, or `state-conflict` | user or the named existing owner |
| 4 | One bounded target explicitly asks to diagnose, reproduce, compare feasibility, or research an external API, and does not also authorize change delivery | `investigate` / `bug-diagnosis`, `technical-spike`, or `api-research` | `$dev-debugger`, `$dev-spike`, or `$dev-api-research` |
| 5 | One bounded target explicitly asks for fresh proof of a repo/artifact, exact PR head, deployment, or live outcome, and does not also authorize repair or delivery | `verify` / `repo`, `pr`, `deploy`, or `live-outcome` | `$dev-verifier` or the exact existing verification-contract owner |
| 6 | A change-capable target currently modeled as one issue has `delivery_shape: multi` or `ambiguous` | `project` / `pm` | `$pm-project-orchestrator` with the provisional umbrella scope |
| 7 | Project, parent, issue set, or dependency sequence with complete, non-conflicting scope evidence: select `project/pm` for explicit `$pm`, any included missing or blocked PM gate, or no explicit Dev intent; select `project/dev` only for explicit `$dev` when every included issue is currently ready | `project` / `pm` or `dev` | matching project orchestrator |
| 8 | An existing PR has a provable next gate | `post-pr` / `review`, `fix`, `ci`, or `merge` | current PR lifecycle owner |
| 9 | Existing controller, branch, worktree, PR, CI, or review state is resumable without a more-specific post-PR gate | `dev` / `resume` | existing Dev controller or phase |
| 10 | Direct eligibility is satisfied and no full issue/PR/tracker lifecycle was requested | `direct` / `artifact` or `patch` | task-specific Skill / current agent |
| 11 | One issue lacks current development readiness, has a product gap, or is an undiagnosed Bug | `pm` / `feature`, `bug`, or `existing-gap` | `$pm` and its earliest missing owner |
| 12 | One ready issue with `delivery_shape: single` has no resumable Dev state | `dev` / `new-fast`, `new-standard`, or `new-strict` | `$dev` |

For a post-PR route, confirmed review or merge-conflict repair selects `fix`, a
failing or missing required check selects `ci`, a current PR awaiting combined
review selects `review`, and all current merge gates selects `merge`. Otherwise
select `dev/resume` with the exact durable anchor.

The `post-pr/fix` owner is `$dev-implementer` using its PR-repair reference,
the existing PR, and accepted Review state when applicable. Preserve the `fix`
receipt variant; it selects a repair path, not a new issue or worker. This
mapping does not grant code, push, reply, or thread-resolution authority.

Priority 6 intentionally precedes post-PR and resume. An active controller,
branch, or PR does not grandfather a target whose current canonical evidence is
newly `multi` or `ambiguous`. Preserve every existing artifact and immutable PR
head as resume evidence, stop further Dev mutation, and route the provisional
umbrella to `project/pm`. PM Project decides whether that work maps intact to an
accepted child or whether the target is actually `single`; neither Router nor
Dev discards, rewrites, or duplicates the existing branch/PR.

An explicit `$pm`, `$dev`, or mode is a strong intent signal only after the
rows above establish a safe workflow. `$dev` with missing readiness remains
`pm/existing-gap`; `--fast` only chooses or carries a Dev mode and never skips
safety, CI, merge, authority, or release policy. An explicit new follow-up for a
Done issue enters PM without reopening the completed issue.

For project scope, `project/pm` is the deterministic safe default: it retains
the complete scope while the PM project controller resolves missing or mixed
readiness. The router may select `project/dev` only when the request explicitly
asks for Dev and the one bound scope read proves that every included issue is
currently ready. A provisional umbrella remains `project/pm` until PM has
materialized and verified its child issue set. Conflicting or unavailable scope
evidence remains `blocked`.

## Terminal Intent And Fixed Variants

Terminal intent is a completion boundary, not a delivery mode or a runtime
route. Effective delivery modes are `fast`, `standard`, and `strict`. Preserve strict
and `new-strict` through routing. Standard blocks P0/P1; strict blocks P0/P1/P2.
Preserve named verification requirements; mode alone does not add QA or change
scheduling. Previously normalized receipts remain historical evidence; an
explicit new strict request updates the pending mode rather than old artifacts.

| Family / variant | Terminal intent | Completion output | Default mutation budget | Stop condition |
| --- | --- | --- | --- | --- |
| `status/read-only` | `answer` | current report | `none` | report is returned |
| `direct/artifact` / `direct/patch` | `artifact` | bounded local artifact or patch | existing Direct budget | Direct result is validated |
| `investigate/bug-diagnosis` | `diagnosis` | diagnosis brief with evidence, confidence, options, and recommended route | `none`, `scratch-only` for exact explicitly authorized repro/instrumentation, or `retained-diagnostic-artifact` only for an exact user-authorized path plus targeted validation and cleanup/retention disposition | `conclusive`, `inconclusive`, `blocked`, or `not-applicable` brief is returned |
| `investigate/technical-spike` | `diagnosis` | spike report and decision | `none`, or explicit scratch-only experiment | feasibility decision or blocker is returned |
| `investigate/api-research` | `diagnosis` | primary-source research brief | `none` | feasible, risky, blocked, or not-applicable research decision is returned |
| `verify/repo` / `pr` / `deploy` / `live-outcome` | `verification` | frozen-target claim ledger and overall result | `none`, or `explicit-verification-actions` inside the exact authorized envelope | `pass`, `fail`, `blocked`, `unverified`, or `not-applicable` is returned |
| `dev/*` / `post-pr/*` | `change` | selected Dev or PR lifecycle gate | `scoped-lifecycle` | selected lifecycle contract reaches its terminal gate |
| `release/release` | `release` | repository release contract result | repository-policy-defined | release contract terminal result |

`investigate/*` and `verify/*` are fixed ownership variants. They do not create
a new controller Skill, implementation branch, PR, tracker closeout, or
downstream architecture/planner/implementer dispatch. A request that explicitly
includes repair, PR, merge, or issue closeout has terminal intent `change` and
selects the existing Dev or post-PR route; investigation may then be a selected
conditional Dev phase rather than a stopping route.

`verify/*` freezes its exact target before collecting evidence: repository or
artifact revision for `repo`, immutable PR head for `pr`, named environment and
observed revision for `deploy`, and the existing Production Loop or Human
Acceptance contract for `live-outcome`. A status question remains
`status/read-only`; it is not verification until fresh evidence is requested.
Skipped, stale, inaccessible, or mismatched-environment evidence is never a
pass. Ambiguous or side-effecting live verification actions select
`blocked/authority` before execution.

## Canonical Route Receipt

Return this receipt exactly once. Keep values factual and minimal; `evidence`
names the live sources used, not a narrative reconstruction.

```yaml
issue_route:
  version: 3
  request: <normalized intent and explicit mode>
  target:
    kind: <none | issue | parent | project | issue-set>
    ids: [<IDs>]
  delivery_shape:
    classification: <not-applicable | single | multi | ambiguous>
    independent_outcomes: [<outcome or none>]
    shared_acceptance: <one shared acceptance boundary or none>
    signals:
      repositories_or_hosts: [<targets or none>]
      external_product_decisions: [<decisions or none>]
      asynchronous_human_gates: [<gates or none>]
      expected_delivery_units: <one | multiple | unknown>
    evidence: [<minimal canonical issue evidence>]
    next_owner: <continue-route-table | $pm-project-orchestrator | blocked>
  live_state:
    issue_state: <state>
    pm_gate: <ready | missing | blocked | not-applicable>
    dev_state: <none | active | resumable | terminal>
    pr_state: <none | open | checks | review | merge-ready | merged>
  selected:
    family: <fixed family>
    variant: <fixed variant>
    next_owner: <one owner>
    resume_anchor: <none or exact artifact/controller/PR>
    mode: <not-applicable | fast | standard | strict>
    terminal_intent: <answer | artifact | diagnosis | verification | change | release>
  completion_contract:
    required_output: [<artifact or evidence ledger>]
    mutation_budget: <none | scratch-only | retained-diagnostic-artifact | scoped-lifecycle | explicit-verification-actions>
    stop_after: <named terminal gate or result>
    allowed_transition:
      - <new receipt only after fresh delivery authorization or existing canonical full-delivery mandate>
  resume:
    duplicate_policy: <resume same fresh owner/receipt | not-applicable>
    transition_history: <from/to/trigger/authorization/resume_anchor, or none>
  evidence: [<minimal live sources>]
  forbidden_next_actions: [<gates/actions that cannot run yet>]
  reroute_trigger: <material state or decision change only>
```

## Consumer Rules

The selected controller validates receipt freshness immediately before its first
mutation and reuses the receipt's target/delivery-shape/cardinality/owner
decision rather than repeating the classification. Reroute only when a material
input changes: canonical requirement or readiness, delivery shape, target
cardinality, active controller, branch/PR/head, CI/review/merge state, or
release authority. A changed PR head invalidates downstream Dev gates; it does
not erase a current PM record.

Downstream ownership remains unchanged:

- `$pm` fills single-issue product gaps and owns PM roots/readiness.
- `$pm-project-orchestrator` validates provisional umbrella shape, owns the
  accepted decomposition and project-level tracker writes, then inventories the
  resulting child set.
- `$dev` applies its Resume-First preflight and selects Dev phases after workflow
  ownership is known; it rejects `multi` or `ambiguous` single-issue receipts
  before mutation.
- Project orchestrators retain complete multi-issue scope. Product owns split
  decisions and PM waves; Develop owns engineering waves and barriers only
  after the issue set is materialized and ready.
- Review, Release, and agent-routing consume their own contracts only when
  their workflow is selected.

An investigate or verify owner stops at its completion contract. On
`inconclusive`, `fail`, `blocked`, or `unverified`, it returns the smallest
failure boundary, evidence, and a proposed next route; it does not repair,
retry a side effect, start Dev, change tracker completion, or dispatch that
proposal. Moving from `diagnosis` or `verification` to `change` requires fresh
user delivery authorization or an already explicit full-delivery canonical
issue, followed by a new router receipt. A material state change can invalidate
evidence and require re-routing, but never supplies delivery authority. The new
receipt records the authorization and reuses still-fresh evidence as its resume
anchor.
Repeated unchanged requests resume the same fresh receipt/owner rather than
creating a second investigation, verification, PM root, branch, or PR.
