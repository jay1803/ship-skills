# Test Authoring Gate

Shared by `$dev-implementer` and `$dev-test`; read before adding or changing a
durable test.

Select verification before authoring durable tests. Start with existing tests,
fixtures and required checks; zero new tests is a complete result when they
already prove the selected behavior. A runnable harness, changed file, test-count
target or coverage percentage alone does not justify another committed test.
Explicit user/repository testing requirements and the selected validation floor
still apply; missing required evidence remains blocked or unverified.

Before adding or changing a test, identify the observable behavior, invariant,
or independent contract it protects, a credible regression that would make it
fail, and the gap in existing coverage. Check which existing test owns that
contract at the strongest practical boundary; reuse it unchanged when sufficient,
extend it for a missing case, and add another layer only for a distinct failure
it can detect. An existing test that reproduces a bug is already its regression
test; a bug ticket does not require a duplicate.

Choose representative inputs from different rules, transitions, thresholds or
failure mechanisms. More values in the same equivalence class need distinct
regression value. Keep useful faults diagnosable; grouping assertions or moving
them into a loop does not itself reduce scenarios or maintenance work.

Reject assertions that merely restate source structure, private call shape, or
uncontracted constants, copy the implementation as their oracle, or verify
behavior supplied by the mock itself. A test that breaks under a
behavior-preserving refactor is suspect unless that structure is an explicit
compatibility contract. Prefer the owned input/output boundary over a new
production export, flag, or wrapper used only by tests; if a small seam is
necessary to expose that boundary, justify its distinct value under the
[TDD guidance](../../dev-implementer/references/tdd.md#decide-before-writing-a-test).
Keep independent API, migration, security, package, and architecture contract
checks when they guard real drift, including a source inspection that is the
cheapest reliable proof. Name the actual contract and failure it detects; an
architecture label alone does not turn UI source spelling into a contract.
Without a meaningful UI or external observation point, use available build,
existing-test or temporary repro evidence and report its limits instead of
adding a source-string, empty or self-fulfilling mock test as a substitute.

Temporary probes and one-off repro scripts need not become permanent tests;
retain them only when they protect an enduring regression or required contract.
Apply this judgment to the test diff before handoff, and summarize additions,
extensions or sufficient unchanged coverage in the existing implementation and
Test Result. Zero new tests is not a skipped check. Do not create a per-test form
or extra evidence artifact, or remove pre-existing coverage as incidental cleanup.
