---
name: dev-self-review
description: >-
  Review local implementation changes before opening a pull request. Use after tests pass and before PR creation to catch obvious mistakes, scope creep, weak tests, naming issues, dead code, unsafe assumptions, and missing validation.
---

# Dev: Self Review

Review the diff like a strict senior engineer before opening a PR.

## Workflow

1. Inspect `git status`, the diff, changed tests, and validation results.
2. Compare the diff against the product spec, dev plan, and technical approach.
3. Prioritize correctness, maintainability, architecture fit, error handling, performance, security/privacy, tests, and scope control.
4. Fix only trivial local issues when clearly safe; otherwise route findings back to the selected implementer.
5. Do not approve a PR when required tests are missing, validation failed, or scope drift is present.

## Output

```markdown
## Self Review

Decision: <approve for PR | needs changes | blocked>

### Findings
- [<severity>] <issue, file/evidence, and required action>

### Scope Check
- <In scope / scope drift / uncertain>

### Test Check
- <Adequate / weak / missing / blocked>

### Recommended Next Step
<`$dev-pr-writer` if approved; otherwise the selected implementer, `$dev-test`, or stop.>
```
