---
name: project
description: Prepare and maintain project documents from stakeholder proposal through kickoff, progress updates and closeout. Resume an existing document workflow; excludes product issue decomposition and engineering delivery.
metadata:
  owner: jay1803
  family: project
  maturity: stable
  distribution: project
---

# Project

Own the project's document lifecycle. Route by the requested outcome and current
records, not by a presumed requirement to complete every earlier stage.

## Entry and routing

Read the named draft or Entry Page first. Reuse the existing proposal, approval,
resources and progress record. Ask only when the target or a decision that changes
the requested work cannot be resolved from available evidence.

| Request | Owner |
| --- | --- |
| Prepare, refine or make the case for a proposal; a short go/no-go brief | [proj-proposal](../proj-proposal/SKILL.md) |
| Turn an approved proposal into a kickoff and Entry Page | [proj-kickoff](../proj-kickoff/SKILL.md) |
| Gather progress, reconcile a page, or prepare a stakeholder update | [proj-update](../proj-update/SKILL.md) |
| Summarize delivery, handover, results and lessons | [proj-closeout](../proj-closeout/SKILL.md) |
| Review an existing project document without changing it | [proj-review](../proj-review/SKILL.md) |
| Find missing project materials or build an onboarding context pack | [proj-sources](../proj-sources/SKILL.md) / [proj-context](../proj-context/SKILL.md) |

Research supplies evidence for an unresolved question. Use available research
results directly; if more research is necessary, identify the bounded question
and use the Research plugin when installed. Missing Research does not block a
useful draft with honest gaps. Do not replay a full investigation before writing.

Linear roadmap/issue status belongs to Product's `pm-project-status`; product
scope/decomposition belongs to `pm` / `pm-project-orchestrator`. Engineering
issue, PR, CI, merge and delivery state belongs to Develop's existing lifecycle
owners. Recommend these owners when needed; do not create or update their
tracker objects as a side effect of project documentation. Missing optional
plugins do not block document work and do not justify claiming a handoff ran.

## Execution and continuity

Read the [document contract](references/document-contract.md) before producing
or changing project records. Load only the selected stage's instructions.

Within the authorized stage, gather relevant context, produce the requested
artifact, review it with `proj-review` when preparing a reviewed deliverable,
and fix supported findings. These are steps in the same task; no repeated
permission question or separate agent is required. A review-only request ends
at findings. Stop revising when the requested quality is met or remaining gaps
need external facts/decisions; return the artifact and those gaps.

Advance stages only with evidence and task authority:

- A review-ready proposal is not leadership approval. Record the actual
  approver, approved revision/scope and conditions when provided.
- Approval allows an authorized kickoff task to use that scope. It does not
  demonstrate resource commitments or that a kickoff meeting occurred.
- Updates reflect evidenced changes; passage of time does not start work or
  resolve blockers.
- Closeout distinguishes delivered work, accepted handover and measured impact.
  Unresolved outcomes retain an owner/checkpoint or an explicit ownership gap.

A request to do one stage ends there. A request to continue the project can
advance as far as current evidence and authorization support, then records the
next action and dependency. Resume from that record on the next invocation.
Skills do not provide a scheduler, listener or approval-waiting service. Report
periodic automation only when a separately authorized runtime actually exists.

## Completion

Return the artifact or verified destination, its review/publication state,
material gaps and next action. Preserve draft, review-ready, approved, kickoff
prepared, active, paused/cancelled and closed as distinct evidence-backed states;
use the project's existing vocabulary where equivalent. Do not mark the project
complete merely because this invocation completed.
