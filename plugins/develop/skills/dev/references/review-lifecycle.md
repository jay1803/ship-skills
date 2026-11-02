# Review Lifecycle

Develop owns the loop around stateless `$review` runs: the ledger, re-review
selection, triage, the round budget, acceptance deferral and the controller
disposition after exhaustion. Each Review run returns one result under the
[boundary contract](dev-review-v2-contract.md).

## Ledger

Persist the Review history once in Dev State and pass its reference with the
current target and remaining rounds, not expanded copies. It retains:

- the delivery history ID: the original issue/PR, kept through resumes, splits,
  base changes and new workers;
- every accepted result in order, with its depth, exact target, decision and
  findings (native IDs, severities, scope, relevance and owner);
- cumulative rounds, the plan attempt (1 or 2), rounds since that plan's
  boundary, the limit and its authority, and any replan boundary;
- each disclosed omission and deferral with its evidence and authority.

Missing, reset or contradictory history blocks Review-dependent dispatch,
repair and acceptance. Import earlier v2 artifacts, receipts and their counted
rounds with their original labels; never relabel or recount them.

## Requesting Review

Standard and strict review every PR outside the
[tracked-artifact preset](development-mode-contract.md#tracked-artifact-preset);
for its first review, call `$review` with the mode, governing sources and
required claims. Develop may omit it only when repository policy does not
require Review and the change is proven mechanical: behavior-equivalent, no
protected boundary, required validation passing, no open findings, and no
stronger minimum (an explicit review request needs at least lightweight; an
explicit full or three-lens policy needs full). Record
`technical review: skipped` with that evidence; a skip is never an approval and
cannot start repair.

After a repair, CI fix, conflict resolution, rebase, retarget or base update:

- If the head tree is identical to the reviewed head, reuse the prior result.
  Reuse costs no round and never closes a finding.
- Otherwise request a focused re-review with the open findings and the delta
  when prior independent coverage exists. Request a complete-diff review when
  the history holds only a skip or a replacement plan has started.
- An unexpected change during a review returns `stale` and costs no round;
  reconcile the intended target before asking again.

## Triage

Before repairing a current `repair-required` result, classify each finding's
remediation scope (`in-scope`, `out-of-scope`, `mixed`, `unknown`) and its
relevance (`change-caused`, `required-path`, `independent`, `unknown`). Repair
all confirmed in-scope relevant mode blockers as one batch. A change-caused or
required-path blocker stays blocking even when its fix exceeds scope; hand that
scope decision to the controller. A proven independent baseline defect becomes
a follow-up with its native severity. Unknowns need evidence. Never change a
native severity, and never let a ticket clear a blocker or a mandatory
acceptance or CI gate.

## Budget

Each accepted full, lightweight or focused result counts one round; skip,
reuse, stale results and transport recovery count none, and an escalation
before acceptance counts once. The default is **3 rounds per accepted plan**,
including the initial review, with no automatic P0 extension. Reserve a round
before automatic repair. A verified user's exact numeric override changes only
the original plan's ceiling; "continue" and status questions are not
overrides. Translate old repair-attempt overrides to initial plus attempts.

## Controller Disposition After Exhaustion

The project controller, or the standalone issue worker acting as its controller,
owns this decision. Review and bounded workers report evidence; they cannot
keep the loop running or grant themselves budget.

1. Create or reuse deduplicated tickets for every unresolved finding under the
   shared discovered-work inventory and existing tracker authority, preserving
   native severity, failing outcomes, all three rounds, attempted repairs,
   causes and dependencies. Without tracker writes, leave exact drafts and a
   named persistence action.
2. Apply the acceptance deferral below to remaining acceptance-related P2/P3.
   Defer other findings that do not block delivery under the mode, effective
   acceptance and repository gates, and continue ready project work. Ticketing
   never waives known unsafe behavior, nondeferred required acceptance, CI or
   human merge policy; keep affected work blocked.
3. For a demonstrated project blocker, diagnose why three rounds failed (wrong
   approach, recurring root cause, expanded scope, or an execution/evidence
   failure) and comment the evidence and decision on the ticket. Route an
   unexplained defect to `$dev-debugger`; do not guess from the round count.
4. The controller may hand the failed plan, diagnosis and revised requirements
   to `$dev-planner`. Only an accepted replacement design that addresses the
   diagnosed failure starts **plan attempt 2**, with at most 3 rounds and a
   complete-diff first review. A rename, new worker or unchanged plan is not a
   redesign. Keep the cumulative ledger.
5. If the second plan also exhausts its rounds, pause affected development and
   dependent dispatch. No third plan, fourth round, retry or ticket split resumes
   it automatically. Investigate read-only and comment findings, unknowns and the
   required decision on the ticket.

## Acceptance Deferral

After the active plan's three accepted rounds, the controller may defer
remaining acceptance-related P2/P3 findings, including criteria the original
ticket explicitly required, without an extra item waiver; criteria that
repository policy or the user's current request requires stay binding under
the [precedence](development-mode-contract.md#unattended-validation-and-deferred-acceptance).
Keep the requirement, native finding, severity and failing evidence, and bind
the deferral to the three results, the current target and the follow-up ticket
or draft. Pass it to Review as a caller-marked deferral
and carry it through merge closeout. P0/P1, unknown severity, missing required
coverage, an engineering P2 under strict, and independent CI, safety,
permission, protection and merge gates stay binding. A later requirement-owner
instruction forbidding the deferral wins. It grants no tracker writes, repairs
or merges.

Unavailable agent observations follow the
[unattended validation rule](development-mode-contract.md#unattended-validation-and-deferred-acceptance).
