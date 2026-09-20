---
name: pm-pr-product-review
description: Compare an implemented PR with confirmed product requirements and acceptance criteria; assess conformance without implementing fixes.
metadata:
  owner: jay1803
  family: product
  maturity: stable
  distribution: product
---

# PM: PR Product Review

Review product conformance, not code quality. Do not implement fixes in this role.

For a standalone analysis or draft, follow the
[Product Artifact Contract](../pm/references/artifact-contract.md) and complete
the requested artifact without tracker setup. The tracker steps below apply
only to an issue-bound lifecycle or authorized publication.

## Modes

- Use **Product Review** when the user asks for product feedback on a PR, implementation, or shipped behavior against intent, scope, UX states, UI design, copy, analytics, or product drift.
- Use **Merge-Ready Gate** when development is finished, a GitHub PR exists, review comments are resolved, and the workflow needs a pass, different, incomplete, or blocked product-scope decision before merge.

## Inputs

- Require a GitHub PR URL or number, or infer the PR from the current branch only when that is unambiguous.
- Require at least one Linear issue ID, or infer issue IDs from the PR title, branch, commits, PR body, or linked references.
- Read the actual PR base branch and frozen head; do not assume a repository branch convention.
- In Merge-Ready Gate mode, treat unresolved review comments as blocking unless they are clearly out of scope. If the review state cannot be checked, mark the result blocked or ask whether the user wants a pre-final product review.

## Workflow

1. Verify the target PR.
   - Use GitHub tools or `gh pr view` to capture the PR number, URL, head branch, base branch, author, merge state, review state, linked issues, latest commit, and changed files.
   - Compare the PR head against its base branch, using the actual PR base, excluding local unstaged work.
2. Read the source of truth.
   - Read the original issue, product spec, acceptance criteria, linked comments, PR description, and PR diff when available.
   - For Linear-backed work, read the primary issue title, description, comments, attachments, linked documents, labels, status, parent, children, and linked issues.
   - Include child issues when the PR claims to complete a parent, umbrella, or project slice.
   - Include parent or dependency issues when they define constraints, non-goals, platform scope, rollout behavior, or acceptance criteria for the PR.
   - If Linear access is unavailable, use the PR body and linked text as fallback evidence and mark Merge-Ready Gate mode blocked unless the full requirements are already present in available material.
3. Build the requirements matrix.
   - Apply [Acceptance Classification](../pm-spec/references/acceptance-policy.md#unattended-engineering-acceptance)
     and the current Dev mode waiver. Keep deferred real-environment/human tests
     visibly unverified outside the required engineering matrix; missing such
     evidence is not `Failed - Incomplete` or `Blocked`. Continue to check all
     required product behavior against current implementation evidence.
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
8. Provide comments suitable for the PR or issue tracker when tools are available and the workflow asks for posting. In either mode, post only when the user or enclosing authorized workflow requests a PR comment. Otherwise return the review in chat. If an authorized comment fails, return its unapplied draft.

## Review Focus

- Does the shipped behavior solve the stated problem?
- Does it stay inside scope and respect non-goals?
- Are material UX states, UI design expectations, and edge cases covered?
- Are copy, labels, defaults, and destructive behavior aligned with the product promise?
- Are analytics, privacy, and rollout expectations respected when they were part of scope?
- Are any follow-ups needed because the implementation made a product tradeoff?

## Cross-Platform Coverage

Derive platform coverage from the issue, confirmed decisions, and verified
repository product contracts. A product shipping on iOS and macOS does not by
itself promise both platforms for every feature.

- For confirmed platforms, inspect implementation and available validation;
  shared code is not proof of build or runtime behavior on an unverified target.
- Fail incomplete coverage only when a confirmed requirement is missing.
- If platform scope cannot be established, report `questions` or a specifically
  blocked requirement. Do not invent scope or silently claim coverage.
- Mark irrelevant platforms `Out of scope` or `N/A` with their evidence.

## Decision Rules

- `approve` / `Passed`: every explicit requirement is `Covered` or properly `Out of scope`, no material `Partial`, `Missing`, `Different`, or `Blocked` items remain, and cross-platform expectations are addressed when relevant.
- `request changes` / `Failed - Different`: delivered behavior materially differs from the Linear description, product spec, or acceptance criteria, even if the result may be useful.
- `request changes` / `Failed - Incomplete`: delivered behavior follows the intended direction but leaves explicit requirements unaddressed or partially addressed.
- `questions`: product intent, scope, or platform coverage is ambiguous but enough evidence exists to ask focused product questions.
- `blocked`: required Linear or PR evidence could not be read, review state could not be verified, or the implementation cannot be compared with enough confidence.

## Output

Lead with the verdict, then requirement findings with source and implementation
evidence. Record the PR head/base, confirmed platform scope, unverified claims,
and comment status. Use [review-output.md](references/review-output.md) when a
formal gate or PR comment needs a structured result.

## Output Discipline

- Lead with the verdict; when a comment was authorized, match its result.
- Use concrete issue IDs, PR numbers, branch names, files, and commits.
- Do not claim a product-scope pass from code review alone; pass requires a requirement-by-requirement match.
- Do not rewrite Linear requirements to match the PR. Treat Linear as the source of truth unless a later Linear comment or linked decision explicitly changes it.
- Keep the final answer short after posting the PR comment: result, PR comment status, and any blocking access issue.
