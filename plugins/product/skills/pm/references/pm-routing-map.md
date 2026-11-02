# PM Agent Routing Map

Read when deciding the routing fields for delegated PM work. These are starting
decisions for the [routing contract](routing-contract.md#decide) checklist; the
actual task facts can raise them. Model names stay in the helper's table.

## Controllers

The invoking `$pm` thread, persistent `$pm-project-orchestrator` and fresh PM
issue workers use `lifecycle: controller` and `role: worker`; the helper keeps
them at least `standard` and `high`. Clear ordinary scope stays `standard`,
cross-boundary judgment is `deep`, and the hardest or critical decisions are
`critical`. Persistence alone selects neither `critical` nor `xhigh`, and an
inline PM Skill keeps the current controller's model.

Task ownership coordinates writers; it is not a permission gate. `$pm` owns the
assigned issue and the PM artifacts its active Skills own;
`$pm-project-orchestrator` owns the bound project, its fields, milestones,
membership, dependency graph and in-scope issue set; a fresh issue worker owns
its assigned child issue only.

## Bounded PM Defaults

| Task or Skill | Default route | Use for |
| --- | --- | --- |
| Known issue, comment, document, or source lookup | `explorer/fast` | Exact target retrieval with little interpretation |
| Issue/project inventory, source inspection, or competing-match analysis | `explorer/standard` | Read-only evidence gathering across several sources |
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

`operator/fast` never covers a whole PM Skill or any task that must classify,
infer scope, compose content, choose a status, edit a canonical title or
description, or decide the next PM phase. `reviewer/standard` suits an ordinary
check of a low-risk artifact; the readiness and product-review gates stay
`reviewer/deep` with `judgment_review: yes`. Use `architect/deep` only for a
genuine cross-system technical contract or ownership conflict, and return its
result to `$pm-scope`, `$pm-spec`, `$dev` or the owning controller.

Select requirements from the actual payload: commonly `tracker-read`,
`tracker-write`, `browser` or `network`, plus `repo-read` for repository-backed
investigation.
