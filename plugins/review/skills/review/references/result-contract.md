# Review Result Contract

Every route returns this result. It describes one run on one frozen target;
it carries no cross-run state.

```markdown
## Technical Review

Repository: <repository>
PR: <url or none>
Target Type: <pull-request | immutable-diff>
Base Revision: <full SHA>
Head Revision: <full SHA>
Mode: <fast | standard | strict>
Depth: <lightweight | focused | full>
Started At: <timestamp>
Decision: <approved | comments | stale | blocked>
Common Action: <repair-required | advisory | coverage-blocked | none>
Independence: <satisfied | not satisfied: reason>
GitHub Posting: <verified URL | not posted | not applicable>

### Findings
- <ID, source, native severity or classification, disposition, scenario and
  evidence; for focused review, each prior finding's status: fixed or open>

### Coverage
- Assessed: <requirements, correctness, maintainability, or the focused delta>
- Gaps: <unreadable code, specification not assessed, required claim without
  evidence, unavailable observation (unverified); or "None">

### Limitations
- <stated limits, or "None">

### Next Step
<caller, `$dev-implementer`, `$dev-ci-repair`, or blocked reason>
```

`Decision` follows the common action: `coverage-blocked` is `blocked`,
`repair-required` and `advisory` are `comments`, and `none` is `approved`.
A drifted base or head is `stale` whatever the findings. `approved` requires
complete coverage and no actionable, advisory or evidence-gap item. Standalone
missing or ambiguous specification authority is recorded as `Specification not
assessed` and is at least `advisory`.

An observation the agent cannot obtain in its environment (a physical device,
real account or provider, external environment, or human-only check) is
recorded as `unverified` with its reason; it does not make otherwise complete
coverage incomplete. An available check that was not run, an actual failure,
unreadable code and missing authority remain gaps.

Full review attaches both finder outputs unchanged. Never fabricate finder
outputs or an approval for work that did not run.
