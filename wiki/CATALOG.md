# Skill Catalog

A map of every skill in this repository: what each one does and when to reach
for it. Skills are grouped by plugin, which is also the install and release
boundary. Within a group, the **orchestrator** (if any) is the entry point —
start there and let it route to the narrower skills.

Invoke a skill with `$name` in Codex or `/plugin:name` in Claude Code, or just
describe the task and let the agent match it against the skill's description.

> 中文版见 [`CATALOG.zh-CN.md`](CATALOG.zh-CN.md)。

## Quick index

| Plugin | Skills | Entry point |
| --- | --- | --- |
| [Product](#product) | 14 | `issue-router`, then `pm` |
| [Develop](#develop) | 16 | `dev` |
| [Review](#review) | 6 | `review` |
| [DevOps](#devops) | 3 | `repo-initialize` or `release` |
| [Design](#design) | 6 | `design` |
| [Project](#project) | 8 | `project` |
| [Research](#research) | 16 | `research` |

---

## Product

Turn a request into confirmed, dev-ready product scope. **Start with
`issue-router`** when the right workflow is not yet settled; it selects one
read-only route before any PM, Dev, investigation, verification or release work
begins. **Start with `pm`** once the work is known to be product work on a
single issue.

- `issue-router` — Select one read-only workflow route for a bound issue or project before PM, Dev, investigation, verification, or release.
- `pm` — Drive one product issue to development readiness: intake, missing decisions, canonical specification, and a verified Dev handoff.
- `pm-strategy` — Shape product direction, roadmap priorities, and evidence-backed investment recommendations before project commitment.
- `pm-scope` — Clarify the user problem, desired outcome, and smallest coherent scope with meaningful non-goals and proposed tradeoffs.
- `pm-spec` — Synthesize confirmed scope or a diagnosed bug into a concise PRD or canonical issue title and description.
- `pm-solution-review` — Review a confirmed solution for unnecessary complexity and unsupported rules while preserving its goal.
- `pm-readiness-review` — Assess whether one issue has enough confirmed scope and acceptance evidence to begin development, and return the Dev handoff.
- `pm-backlog` — Draft independently valuable issue slices and dependencies from stable product scope.
- `pm-bug-triage` — Clarify expected versus actual behavior, impact, severity, and actionable evidence before engineering diagnoses a bug.
- `pm-data-analytics` — Design feature success metrics, event semantics, and privacy-aware measurement plans.
- `pm-project-orchestrator` — Structure a project or coordinate PM readiness across related issues, including decomposition of an umbrella issue.
- `pm-project-status` — Read current project and roadmap status, milestone health, and shipment evidence.
- `pm-pr-product-review` — Compare an implemented PR with confirmed requirements and acceptance criteria, without implementing fixes.
- `pm-release-learning` — Draft evidence-backed release notes, or summarize post-release learning from shipped changes and feedback.

## Develop

Engineering delivery from a coding-ready issue to a merged PR. **Start with
`dev`** for a single issue; use `dev-project-orchestrator` for dependency waves
or an ordered merge sequence, and `dev-integration-manager` for an explicit
cross-PR checkpoint.

- `dev` — Deliver one coding-ready issue through its PR, review, CI, merge, and test handoff.
- `dev-project-orchestrator` — Plan or execute multiple dev-ready issues as dependency waves or an ordered merge sequence.
- `dev-integration-manager` — Coordinate integration of an explicit PR or branch set when merge order, contracts, conflicts, or combined validation need a shared checkpoint.
- `agent-routing` — Select executor and runtime bindings when dispatching or escalating a delegated controller, worker, or bounded agent.
- `dev-git-setup` — Prepare or reconcile an issue branch and isolated worktree, preserving existing checkouts and verifying integration bases.
- `dev-planner` — Design approved engineering work, decide task boundaries, and prepare implementation-ready ticket plans.
- `dev-spike` — Investigate unresolved technical feasibility or competing implementation paths before architecture.
- `dev-api-research` — Research third-party API or SDK capabilities and integration contracts when external behavior needs clarification.
- `dev-api-steward` — Maintain owned backend/API contracts and client-facing documentation when implementation may change API behavior or compatibility.
- `dev-implementer` — Implement approved changes and repair PR review findings or conflicts, preserving scoped ownership and validation evidence.
- `dev-debugger` — Diagnose an observed defect, regression, crash, or unexplained test failure and return an evidence-backed root-cause brief before repair.
- `dev-test` — Run post-implementation validation under the selected Dev mode and classify failures before PR preparation.
- `dev-ci-repair` — Repair red PR checks or repeated CI/environment failures escalated by `dev-test`.
- `dev-verifier` — Audit completion claims against fresh tests, runtime evidence, acceptance criteria, and an exact revision.
- `dev-pr-writer` — Prepare, push, and open or reuse a GitHub PR from implemented work with validation evidence.
- `dev-merge-handoff` — Gate and complete one issue PR merge into the resolved integration base, cleanup, and test-revision handoff.

## Review

Independent review of a frozen target. **Start with `review`**, which runs the
lenses in isolation so they cannot contaminate each other, then combines them.

- `review` — Coordinate independent specification, correctness, and maintainability review of a GitHub PR or explicit base/head diff.
- `review-spec` — Compare a frozen implementation with its governing requirements for specification compliance.
- `review-correctness` — Find evidence-backed behavioral defects and regressions in a PR or explicit base/head diff.
- `review-code-quality` — Review for material maintainability costs and bounded simplifications, returning findings to the caller.
- `review-judge` — Validate and combine isolated review artifacts for one frozen target after the reviewers finish.
- `review-pr` — Review a GitHub PR for production-code structure and maintainability, with inline comments when requested.

## DevOps

Repository setup and production release. These own authorization-sensitive
operations and stay separate from issue delivery.

- `repo-initialize` — Initialize or update a repository's `AGENTS.md` and optional `.agents` policies from the template, preserving project-specific rules.
- `release` — Orchestrate a production release under repository policy: promotion, tag, optional deployment, and GitHub Release.
- `deploy-skill-creator` — Capture a project's evidenced deployment and verification procedure in a repository-local deploy skill.

## Design

Visual execution between approved product intent and production engineering.
**Start with `design`** when the required artifact or phase is unclear.

- `design` — Design user flows, interaction states and screen specifications from clear product intent, or route to the narrower design skills.
- `design-direction` — Define a concrete visual direction for an approved product brief or interface.
- `design-explore` — Explore comparable visual solutions for an approved screen, component, or flow.
- `design-prototype` — Build and verify a disposable interactive prototype from an approved flow and screen specification.
- `design-system` — Extract, create, refine, and document reusable design-system foundations and components.
- `design-review` — Review design artifacts, prototypes, system definitions, or implemented UI for visual quality and conformance.

Product scope and acceptance stay with Product; production implementation stays
with Develop.

## Project

Project documents from stakeholder proposal through closeout. **Start with
`project`** to prepare or resume a document workflow. This is project
communication and lifecycle state, not issue decomposition.

- `project` — Prepare and maintain project documents from proposal through kickoff, progress updates, and closeout.
- `proj-sources` — Find and inventory relevant sources for a named project across connected workspace tools, with explicit coverage and access gaps.
- `proj-context` — Build or refresh a project onboarding context pack from existing documents and relevant sources.
- `proj-proposal` — Write or refine a stakeholder project proposal, including a short go/no-go brief.
- `proj-kickoff` — Turn an approved proposal into kickoff material and a reusable Project Entry Page.
- `proj-update` — Gather project progress, reconcile the Entry Page or plan, then draft a stakeholder update.
- `proj-review` — Review a proposal, kickoff, update, or closeout document for decision quality, evidence, and consistency.
- `proj-closeout` — Prepare a completion review, handover, and retrospective against approved goals and actual delivery evidence.

## Research

Open questions into decision-ready evidence. **Start with `research`**, which
frames the question and routes to the right method; the sub-skills are stages of
one evidence program rather than independent report generators.

- `research` — Decision-research orchestrator for open, strategic, diagnostic, forecasting, discovery, design, and evaluation questions.
- `research-question-framing` — Convert a vague or overloaded request into a current Research Contract.
- `research-decision-model` — Build an explicit model of how the question will be judged.
- `research-hypothesis-map` — Create a competing, falsifiable map of explanations or what-must-be-true claims.
- `research-evidence-plan` — Translate the Contract, Decision Model, and Hypothesis Map into a prioritized evidence program.
- `research-desk` — Collect and organize current external, documentary, academic, official, or supplied-source evidence for one bounded question.
- `research-market-landscape` — Map the decision-relevant structure of a market, category, ecosystem, channel, or technology landscape.
- `research-competitive` — Investigate and compare the alternatives competing for the same user, buyer, budget, workflow, or outcome.
- `research-user-study` — Design a decision-relevant user, customer, stakeholder, operator, or expert study.
- `research-user-synthesis` — Synthesize actual qualitative and survey evidence into decision-relevant findings.
- `research-data-analysis` — Analyze supplied or connected quantitative data for a decision-relevant question.
- `research-experiment-design` — Design a credible, proportionate experiment, pilot, or quasi-experimental measurement plan.
- `research-causal-analysis` — Assess whether evidence supports a causal explanation or attributable effect.
- `research-forecasting` — Produce a calibrated forecast for a resolvable future target, with drivers, scenarios, and update signals.
- `research-synthesis` — Synthesize an accepted Research State and Evidence Ledger into a traceable, calibrated draft Decision Brief.
- `research-review` — Independently review a frozen Research State, Evidence Ledger, and Decision Brief before the decision is taken.
