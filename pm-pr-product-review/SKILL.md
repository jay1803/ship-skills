---
name: pm-pr-product-review
description: >-
  Review an implemented PR against the original product intent and Linear requirements. Use for post-implementation product review, merge-ready PR requirements-conformance gates after review comments are resolved, scope, acceptance criteria, edge cases, user behavior, copy, analytics, product drift, and iOS/macOS feature coverage.
---

# PM: PR Product Review

Review product conformance, not code quality. Do not implement fixes in this role.

## Modes

- Use **Product Review** when the user asks for product feedback on a PR, implementation, or shipped behavior against intent, scope, UX states, UI design, copy, analytics, or product drift.
- Use **Merge-Ready Gate** when development is finished, a GitHub PR exists, review comments are resolved, and the workflow needs a pass, different, incomplete, or blocked product-scope decision before merge.

## Inputs

- Require a GitHub PR URL or number, or infer the PR from the current branch only when that is unambiguous.
- Require at least one Linear issue ID, or infer issue IDs from the PR title, branch, commits, PR body, or linked references.
- Default the target base branch to `develop`; if the PR targets another branch, call that out in the result.
- In Merge-Ready Gate mode, treat unresolved review comments as blocking unless they are clearly out of scope. If the review state cannot be checked, mark the result blocked or ask whether the user wants a pre-final product review.

## Workflow

1. Verify the target PR.
   - Use GitHub tools or `gh pr view` to capture the PR number, URL, head branch, base branch, author, merge state, review state, linked issues, latest commit, and changed files.
   - Compare the PR head against its base branch, usually `develop`, not against local unstaged work.
2. Read the source of truth.
   - Read the original issue, product spec, acceptance criteria, linked comments, PR description, and PR diff when available.
   - For Linear-backed work, read the primary issue title, description, comments, attachments, linked documents, labels, status, parent, children, and linked issues.
   - Include child issues when the PR claims to complete a parent, umbrella, or project slice.
   - Include parent or dependency issues when they define constraints, non-goals, platform scope, rollout behavior, or acceptance criteria for the PR.
   - If Linear access is unavailable, use the PR body and linked text as fallback evidence and mark Merge-Ready Gate mode blocked unless the full requirements are already present in available material.
3. Build the requirements matrix.
   - Convert source material into required behavior, acceptance criteria, explicit non-goals, constraints, affected platforms, validation expectations, and deferred scope.
   - Preserve exact issue wording for ambiguous requirements, but keep quotes short.
   - Mark inferred expectations as inferred; do not fail the PR on an inferred expectation unless it follows directly from explicit acceptance criteria.
4. Read the implementation.
   - Inspect the PR diff, commits, touched tests, migrations, config changes, screenshots, validation notes, QA comments, and review-fix commits.
   - Read the relevant changed code paths deeply enough to understand delivered behavior, not just file names.
   - Missing tests alone are not a product failure unless the issue requires them or the risk makes a requirement unverifiable.
5. Compare requirement by requirement.
   - Mark each requirement as `Covered`, `Partial`, `Missing`, `Different`, `Out of scope`, or `Blocked`.
   - `Covered`: implementation satisfies the requirement and no contradictory behavior is visible in the PR.
   - `Partial`: some required behavior is present, but an edge, platform, state, or acceptance criterion is not addressed.
   - `Missing`: the PR does not implement the requirement.
   - `Different`: the PR implements behavior that conflicts with or materially changes the requirement.
   - `Out of scope`: the PR omits something explicitly excluded or deferred.
   - `Blocked`: the requirement cannot be verified because Linear, GitHub, build artifacts, generated files, or code context are unavailable.
6. Look for product drift: changed promise, missing state, unplanned scope, confusing copy, missing measurement, or deferred behavior implemented accidentally.
7. Separate product findings from engineering implementation details.
8. Provide comments suitable for the PR or issue tracker when tools are available and the workflow asks for posting. In Merge-Ready Gate mode, always leave a PR comment when a GitHub write tool is available; if commenting fails, provide the exact comment text in chat.

## Review Focus

- Does the shipped behavior solve the stated problem?
- Does it stay inside scope and respect non-goals?
- Are material UX states, UI design expectations, and edge cases covered?
- Are copy, labels, defaults, and destructive behavior aligned with the product promise?
- Are analytics, privacy, and rollout expectations respected when they were part of scope?
- Are any follow-ups needed because the implementation made a product tradeoff?

## Cross-Platform Coverage

For user-facing features in products that ship on both iOS and macOS, treat iOS coverage and macOS coverage as separate requirements unless the issue explicitly scopes the feature to one platform.

- Verify each platform from the implementation, not just intent: shared code only counts for a platform when it actually compiles and behaves there.
- If the feature is delivered on only one platform and the issue does not limit scope, mark the missing platform `Partial` and use `Failed - Incomplete` in Merge-Ready Gate mode.
- Respect explicit single-platform scope, such as iOS-only, macOS window/menu behavior, widgets, or share extensions; mark the other platform `Out of scope` and say why.
- For backend, shared-logic-only, CI, docs, refactors, or other non-feature work with no user-facing platform surface, mark platform coverage `N/A`.
- When the issue is silent and the second platform may apply, do not silently pass. Flag the unaddressed platform and recommend confirming scope.

## Decision Rules

- `approve` / `Passed`: every explicit requirement is `Covered` or properly `Out of scope`, no material `Partial`, `Missing`, `Different`, or `Blocked` items remain, and cross-platform expectations are addressed when relevant.
- `request changes` / `Failed - Different`: delivered behavior materially differs from the Linear description, product spec, or acceptance criteria, even if the result may be useful.
- `request changes` / `Failed - Incomplete`: delivered behavior follows the intended direction but leaves explicit requirements unaddressed or partially addressed.
- `questions`: product intent, scope, or platform coverage is ambiguous but enough evidence exists to ask focused product questions.
- `blocked`: required Linear or PR evidence could not be read, review state could not be verified, or the implementation cannot be compared with enough confidence.

## Sub-Agent Contract

This skill is safe to run inline or as a bounded sub-agent. When delegated:

- Use only the request, provided sources, and directly referenced PR, issue, or tracker context.
- Produce the product review or merge-ready gate result and any allowed PR comment or draft.
- Follow this skill's tracker-write rules; do not edit issue descriptions unless this skill explicitly owns that write.
- Return sources read, writes applied or drafts, blockers, and open questions.

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

## Output Discipline

- Lead the chat response with the same result posted to the PR.
- Use concrete issue IDs, PR numbers, branch names, files, and commits.
- Do not claim a product-scope pass from code review alone; pass requires a requirement-by-requirement match.
- Do not rewrite Linear requirements to match the PR. Treat Linear as the source of truth unless a later Linear comment or linked decision explicitly changes it.
- Keep the final answer short after posting the PR comment: result, PR comment status, and any blocking access issue.
