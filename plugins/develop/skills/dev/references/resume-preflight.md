# Resume-First Preflight

Read for a request that may enter or resume Dev, after an implicit Direct
exclusion has been resolved. This is the canonical request-owner, readiness,
resume-evidence, and receipt contract. Return to the root stage-selection gates
only after a passing preflight.

## Request Owner

Classify the current request's completion boundary from its own words and live
evidence. Available permission does not request delivery, and a current request
to diagnose, research, or verify and stop outranks earlier broader permission.

| Current request | Owner |
| --- | --- |
| Deliver or resume one issue | the preflight below, then this issue worker |
| Deliver a parent, project, or issue set | `$dev-project-orchestrator` with the complete scope |
| Next gate of an existing PR: Review, comment/conflict repair, red CI, or merge | `$review`, `$dev-implementer`, `$dev-ci-repair`, or `$dev-merge-handoff` from that exact PR; never a second branch, PR, or controller |
| Diagnose a defect, test feasibility, or research an external API, then stop | `$dev-debugger`, `$dev-spike`, or `$dev-api-research`, ending at its brief |
| Freshly verify a repository revision, PR head, deployment, or live outcome | `$dev-verifier` verify-only, ending at its ledger |
| Production promotion | `$release` |
| Status or explanation | answer directly |

Investigation, verification, release, and status owners start no Dev State,
goal, Git, tracker, PR, or downstream Dev-role work. A brief or ledger may
propose a next step but never authorizes it: moving to a change needs a new
explicit user request or authorization, with that brief or ledger as the resume
anchor. An explicit `$dev` or requested mode bypasses only the Direct
exclusion, never readiness, protected boundaries, CI, merge policy, authority,
or release ownership.

## Resume-First Preflight

Before creating or reusing a goal, changing git state, writing the tracker,
creating or updating a PR, or delegating any downstream Dev role, run one hard
**read-only preflight** for every request that may enter Dev, including a
resume. It rehydrates, from current evidence rather than inferred history:

1. issue, project, status, labels, canonical description, comments, and any
   existing readiness or handoff record;
2. branch/worktree, PR, base/head, CI, the technical Review ledger and current
   result with actual coverage, merge state, and
   existing visible worker/controller IDs; and
3. the effective mode (`fast`, `standard`, or `strict`) and Direct eligibility.

It has exactly five terminal routes:

- `direct`: a [Direct path](entry-readiness.md#direct-exclusion-gate) applies;
  return its result under that path;
- `decision_required`: the [entry audit](#entry-audit) finds a missing decision
  that changes what gets built;
- `dev_new` or `dev_resume`: the audit passes and evidence supports a new
  lifecycle or continuing the same issue lifecycle; or
- `blocked`: read-only evidence is unavailable, contradictory, stale in a way
  that cannot be resolved without a decision, or crosses a protected boundary.

`decision_required` and `blocked` start **zero** downstream Dev roles. Do not
create a goal, claim an issue, invoke `$dev-git-setup`, or make a tracker/PR
mutation beyond the decision record below until a `dev_new` or `dev_resume`
preflight passes.

## Entry Audit

Every issue, existing or newly drafted, passes this read-only audit before
branch/worktree creation or repository research. A current PM handoff is
supporting evidence, never a requirement.

- Confirm one coherent buildable outcome (`delivery_shape: single`), not a
  project or hidden issue sequence. Multiple files, layers, technologies,
  commits, expected PRs, estimate, or ordinary synchronous QA alone do not
  prove `multi` and must not cause a mechanical split.
- Identify the objective, current/expected behavior, in-scope work, meaningful
  non-goals, and critical acceptance criteria from the issue and linked evidence.
- Verify that material product rules are requester-authored, inherited from
  cited current behavior, or otherwise explicitly confirmed. Dev never fills a
  product gap with its own default, and a generic "continue" is not a decision.
- Confirm dependencies, repository ownership, and execution order are clear
  enough to start.
- Distinguish implementation inputs from human/device/credential/deployment or
  production-only proof that can remain pending until outcome completion.

On a pass, record the readiness basis (the canonical issue and any decision
comments) in Dev State and build the implementation brief from those sources.
Do not rewrite a sufficient issue or add ceremonial comments or labels. Issue
status, assignee/delegate, labels, description length, or an existing branch
are supporting context, never sufficient proof by themselves. When only
outcome-verification logistics are pending and they do not affect the
implementation choice, record `Outcome Verification Readiness: blocked - may
begin development`, preserve the exact requirement through merge/test handoff,
and do not claim overall outcome completion.

On `decision_required`, ask the requester for the exact missing product
decision, scope boundary, critical acceptance criterion, human-safety
instruction, or dependency, with the options the evidence supports, and record
the question and its answer on the ticket; continue from the recorded answer.
A `multi` or `ambiguous` shape is `decision_required` for the whole scope:
propose the outcome split from the issue's own stated outcomes and ask the
requester to confirm it, because Dev never invents outcome boundaries. Develop
creates the confirmed children with its tracker authority (otherwise exact
drafts), and execution continues through `$dev-project-orchestrator`.

## Resume Receipt

After a pass and immediately before the first delegation, record the
**Resume Receipt** in [Dev State](dev-state.md): readiness basis; `new` or
`resume`; delivery shape; required, conditional, and skipped gates; validation
floor; terminal intent; phase-plan preset; and invalidators/escalation triggers.

Revise the Resume Receipt only when the selected route or material phase plan
changes. Record non-material evidence and downstream invalidations in the
existing receipt/state without creating a new receipt revision.

When current upstream evidence changes, record the source and invalidate only
the downstream dependent gates. For example, a changed PR head invalidates
current verification, technical Review, CI evidence, and merge readiness; it
does not invalidate the canonical issue record or already-completed unrelated
discovery. A changed canonical requirement invalidates its dependent
technical plan and later implementation evidence. Escalate instead of guessing
when a change alters product scope, protected-boundary treatment, ownership, or
the required validation floor.
