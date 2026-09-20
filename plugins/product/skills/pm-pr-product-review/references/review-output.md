# Product Review Output Examples

Use the relevant example for a requested formal review or PR comment. Omit
empty sections and preserve evidence and unresolved requirements.

## Output Shapes

Use this shape for normal product review:

```markdown
## Product Review

Decision: <approve | request changes | questions | blocked>

### Findings
- [<severity>] <Product issue, evidence, and requested change.>

### Product Drift
- <Scope drift, changed promise, or "None.">

### Follow-Ups
- <Follow-up issue/comment or "None.">
```

Use this shape for a Merge-Ready Gate pass:

```markdown
PR Product Review: Passed

Compared PR #<number> against Linear <issue ids>. The implementation matches the stated requirements and I found no missing or materially different scope.

Evidence checked
- Linear requirements: <issue ids and related issues>
- PR scope: <head branch> -> <base branch>, commit <sha>
- Platform coverage: iOS <covered / out of scope / N/A>, macOS <covered / out of scope / N/A>
- Validation/QA evidence: <brief summary or "not required by issue">
```

Use this shape for changed product behavior:

```markdown
PR Product Review: Failed - Different

Compared PR #<number> against Linear <issue ids>. The implementation does not match the stated requirements.

Differences
1. <Requirement or workflow>
   Expected: <expected behavior>
   PR delivers: <actual delivered behavior>
   Evidence: <file, diff area, comment, or observed artifact>

Requirements covered
- <covered item, if useful>
```

Use this shape for incomplete scope:

```markdown
PR Product Review: Failed - Incomplete

Compared PR #<number> against Linear <issue ids>. The implementation is aligned with the issue direction but does not fully address the required scope.

Remaining scope
1. <Requirement>
   Expected: <expected behavior>
   Current PR: <what is present or missing>
   Evidence: <file, diff area, comment, or observed artifact>

Requirements covered
- <covered item, if useful>
```

Use this shape for blocked review:

```markdown
PR Product Review: Blocked

I could not complete PR product review for PR #<number> against Linear <issue ids>.

Blocked evidence
- <Linear, GitHub, review state, diff, artifact, or access problem>

What is needed
- <specific next action to unblock the comparison>
```

