# Behavior-Preserving Refactor Design

Read when structural change is the primary outcome and safe implementation
depends on boundaries, migration order, invariants, compatibility, or rollback.
Small incidental cleanup uses the ordinary technical approach.

Treat existing behavior as the contract unless an approved requirement changes
it. Use current modules, callers, tests, ownership, build targets, generated
artifacts, and dependencies from source evidence or the current brief.
If behavior invariants are unknown, stop migration design and recommend
`$dev-spike`, `$dev-debugger`, or product clarification; do not infer them from a
preferred target structure.

Include in the same Technical Plan, when applicable:

1. Current versus target responsibilities, approved structural goal, and
   concrete non-goals. Reject aesthetic cleanup outside that goal.
2. Invariants to preserve: API/model semantics, persistence, UI, permission,
   concurrency, performance, analytics, or other observed contracts. Name how
   each is proved; source anchors matter more than a separate design document.
3. Affected callers, modules, build/generated surfaces, and compatibility risks.
   Route API behavior/docs/generated-client impact to `$dev-api-steward`.
4. Incremental migration order with build/test checkpoints at meaningful cut
   points; avoid a large-bang move when smaller reversible steps work.
5. Characterization/golden tests before movement where existing behavior is
   under-tested, focused contract tests, compile checks, and required regression
   or runtime proof. Tests should assert the preserved behavior.
6. Rollback strategy and safe PR boundaries. Recommend a split when modules can
   move independently, safety tests must land first, or one change is not
   reviewable. The project controller owns actual multi-issue scheduling.

Conclude `proceed`, `spike first`, `split`, or `blocked`, with the evidence and
next owner. Do not produce another planner artifact after this plan solely to
repeat migration steps, invariants, or validation.
