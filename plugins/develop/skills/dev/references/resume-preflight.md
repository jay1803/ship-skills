# Resume-First Preflight

Read for a request that may enter or resume Dev, after an implicit Direct
exclusion has been resolved. This is the canonical routing, readiness,
resume-evidence, and receipt contract. Return to the root stage-selection
gates only after a passing preflight.

## Issue Router Gate

Before the preflight, any goal, Git/Linear/PR mutation, repository work,
or downstream Dev delegation, run the Jev-backed canonical `$issue-router` for a
request that names a Linear issue, issue URL, parent, project, or
issue set. Consume its one read-only Issue Route receipt; do not repeat broad
target, delivery-shape, cardinality, or workflow-owner classification.

- `dev/new-*` and `dev/resume` proceed to the existing Resume-First
  Preflight, which remains the owner of readiness validation, resume evidence,
  and the Resume Receipt.
- `post-pr/review`, `fix`, `ci`, or `merge` continues from that exact existing
  lifecycle owner and anchor; do not create a second branch, PR, or controller.
- `project/dev` goes to `$dev-project-orchestrator` with the complete scope.
- `project/pm` goes to `$pm-project-orchestrator` with the complete scope; do
  not begin Dev State while any included issue still needs PM work. This
  includes a target currently modeled as one issue when its Delivery Shape
  Precheck is `multi` or `ambiguous`; preserve it as
  the provisional umbrella rather than selecting one hidden delivery unit.
  Existing branch/PR/head state remains a resume anchor but does not permit
  further Dev mutation until PM Project resolves the shape.
- `investigate/*` and `verify/*` stop before Dev State, goal, Git, tracker, PR,
  or downstream Dev-role work. Their fixed owner returns the terminal brief or
  frozen-target ledger and may only propose a new route.
- `pm/*`, `direct/*`, `status/read-only`, `release/release`, and `blocked/*`
  stop before Dev State, goal, Git, tracker, PR, or downstream Dev-role work.

Explicit `$dev` and a requested mode remain in the receipt but cannot bypass
readiness, protected boundaries, CI, merge policy, authority, or release
ownership. The router does not select Dev phases, runtime/model bindings, or
write authority; Dev verifies freshness before its first mutation and reroutes
only after a material state or decision change.

Dev consumes `terminal_intent: change` only. It must preserve the router's
completion contract and transition history in the Resume Receipt, but it may
not reinterpret an `investigate/*` or `verify/*` result as permission to fix,
open a PR, update a tracker state, or resume delivery. A later repair request
uses a new canonical Issue Route receipt with the fresh authorization and the
diagnosis/verification evidence as its resume anchor.

## Resume-First Preflight

Before creating or reusing a goal, changing git state, writing the tracker,
creating or updating a PR, or delegating any downstream Dev role, run one hard
**read-only preflight**. This gate applies to every request that may enter Dev,
including a resume. It has exactly five terminal routes:

- `direct`: preserve the Direct Artifact or Direct Patch result and return it
  without Dev State, goal, git, tracker, PR, or downstream Dev-role work;
- `pm_required`: the canonical issue lacks a product decision, stable scope,
  critical acceptance criterion, dependency, or PM readiness evidence that
  changes implementation; start **zero** downstream Dev roles;
- `dev_new`: evidence supports a new Dev lifecycle; or
- `dev_resume`: evidence supports continuing the same issue lifecycle; or
- `blocked`: read-only evidence is unavailable, contradictory, stale in a way
  that cannot be resolved without a decision, or crosses a protected boundary;
  start **zero** downstream Dev roles.

The preflight rehydrates, from current evidence rather than inferred history:

1. issue, project, status, labels, canonical description, PM root/replies,
   combined PM Handoff/readiness evidence (or the current legacy separate pair),
   and the current Router Delivery Shape receipt;
2. branch/worktree, PR, base/head, CI, combined Review V2, merge state, and
   existing visible worker/controller IDs; and
3. the effective mode (`fast`, `standard`, or `strict`) and Direct eligibility.

Do not create a goal, claim an issue, invoke `$dev-git-setup`, or make a
tracker/PR mutation until a `dev_new` or `dev_resume` preflight passes.
For a single-issue Dev entry, only `delivery_shape: single` can return those
routes. `multi` or `ambiguous` returns `pm_required`
with `$pm-project-orchestrator` as next owner; it starts zero downstream Dev
roles even when the issue was previously marked ready.

After a pass and immediately before the first delegation, the controller emits
one compact **Resume Receipt** containing: issue; readiness basis; `new` or
`resume`; delivery shape; mode; required, conditional, and skipped gates;
validation floor; terminal intent; phase-plan preset; and
invalidators/escalation triggers. Reuse
the verified PM root/stage replies
and matching current branch/PR/head/CI/review state. Do not recreate comments,
workers, branches, PRs, or completed gates merely because the controller was
restarted.

Revise the Resume Receipt only when the selected route or material phase plan
changes. Record non-material evidence and downstream invalidations in the
existing receipt/state without creating a new receipt revision.

When current upstream evidence changes, record the source and invalidate only
the downstream dependent gates. For example, a changed PR head invalidates
current verification, Review V2, Product Review, CI evidence, and merge
readiness; it does not invalidate the canonical PM record or already-completed
unrelated discovery. A changed canonical requirement invalidates its dependent
technical plan and later implementation evidence. Escalate instead of guessing
when a change alters product scope, protected-boundary treatment, ownership, or
the required validation floor.
