---
name: review-pr
description: >-
  Review a GitHub PR for production-code structure and maintainability, with inline comments when requested. Excludes correctness and test review.
metadata:
  owner: jay1803
  family: review
  maturity: stable
  distribution: review
---

# Review: Pull Request

Review the production-code structure of one GitHub pull request and, when requested, publish one
verified GitHub `COMMENT` review. The pull request and its frozen head are the
canonical target; local repository context may support analysis but never
replaces the GitHub diff or posting evidence.

This is a focused PR review, not comprehensive `$review`. Do not invoke
`$review-spec`, `$review-correctness`, `$review-code-quality`, conditional test
review, or `$review-judge`.

Read the sibling
[Code Quality Findings Contract](../review-code-quality/references/code-quality-findings-contract.md)
before reviewing. Apply its evidence, materiality, bounded-alternative, and
proportionality bars to structural findings. Read
[GitHub Review Posting](references/github-review-posting.md) before any GitHub
write.

## Target And Authorization

- Accept one GitHub pull request URL or number with an unambiguous repository.
  A current-branch PR is acceptable only when `gh pr view` resolves exactly one
  open pull request. Do not accept an arbitrary local diff or infer a range.
- Require authenticated read access before inspection and GitHub pull-request
  write access before posting. Never print credentials or authentication data.
- Post one `COMMENT` review only when the user explicitly asks for GitHub
  comments or has already authorized posting on this exact PR. Selecting or
  invoking the skill alone does not grant posting permission. Otherwise return
  the proposed comments as `draft only` without asking for permission to finish
  the analysis. A read-only or "do not comment" instruction always preserves
  draft-only behavior. `APPROVE` and `REQUEST_CHANGES` require explicit
  authorization for that event and PR.
- Do not modify files, create branches, push commits, resolve threads, merge the
  PR, or change repository settings.

## Review Scope

Inspect the PR patch and only the surrounding production code needed to judge:

- module and ownership boundaries;
- dependency direction and public or internal interfaces;
- state, lifecycle, and control-flow design;
- unnecessary abstraction, wrappers, modes, or indirection;
- duplicated policy and scattered special cases;
- cohesion, coupling, extension paths, and materially simpler structures.

Exclude tests, test fixtures, snapshots, test-support code, coverage artifacts,
generated files, vendored sources, and lockfiles from review. Do not run tests,
builds, linters, type checks, formatters, benchmarks, or CI commands. Do not
inspect CI logs or emit missing-test, test-quality, coverage, or failing-check
findings; CI and Dev validation own those surfaces.

Do not broaden into behavioral correctness, security, specification compliance,
product acceptance, or visual design. If a candidate concern cannot be stated
as a concrete code-structure or software-design cost, withhold it and name the
excluded owning review only when that handoff helps the caller.

## Workflow

1. Resolve and freeze the pull request.
   - Capture canonical repository identity, PR URL and number, base/head branch,
     immutable base/head SHAs, state, and draft status with `gh pr view`.
   - Retrieve the GitHub patch and changed-file metadata. Record which files are
     in production-code scope and which were excluded by the boundary above.
   - Stop if the PR is closed, the repository is ambiguous, the patch is
     unavailable, or the exact head cannot be frozen.

2. Inspect the scoped code.
   - Review every in-scope changed hunk and the minimum callers, owners, or
     interfaces needed to evaluate its structure.
   - Respect established repository conventions and proven compatibility or
     lifecycle constraints. Withhold style preferences, speculative
     future-proofing, and broad rewrites.
   - Prefer a small number of high-confidence findings. Each finding must name
     the maintenance scenario, material cost, evidence, and smallest
     behavior-preserving direction.

3. Bind findings to the GitHub diff.
   - Prefer an inline comment on the smallest changed line or range that makes
     the concern understandable. Record exact `path`, `line`, `side`, and the
     frozen `commit_id`.
   - Use the review body for a cross-file architectural finding or a finding
     that cannot be attached truthfully to a current diff line. Do not force an
     unrelated line anchor merely to make a comment inline.
   - Write comments as review feedback, not implementation patches: explain the
     structural cost and bounded direction without rewriting the whole change.

4. Recheck and publish once, only when posting is authorized.
   - For draft-only work, return the proposed findings without a write.
   - Immediately before writing, query `headRefOid` again. If it differs from
     the frozen head, return `stale` without posting.
   - Batch all inline comments and the summary into one GitHub review with event
     `COMMENT`, bound to the frozen head SHA. A clean review posts one concise
     summary stating that no actionable code-structure findings were observed.
   - Avoid per-comment posting loops. After any ambiguous transport failure,
     re-read reviews and comments before retrying so the PR does not receive
     duplicates.

5. Verify GitHub state after a write.
   - Re-read the created review and its inline comments. Verify repository, PR,
     review ID, author, commit SHA, event/state, paths, lines, bodies, and URLs.
   - Return `blocked - review not verified` when the write or its target binding
     cannot be confirmed. Never report a draft or local result as posted.

## Finding Shape

```markdown
### [blocking | non-blocking] Concise structural concern

Why it matters: <specific maintenance, ownership, coupling, or extension cost>

Evidence: <changed path/symbol and relevant caller, owner, interface, or convention>

Direction: <smallest behavior-preserving structural correction>
```

For an inline comment, omit headings that add noise but preserve the same three
facts. Do not post naming, formatting, or taste-only nits.

## Output

```markdown
## PR Code Review

Repository: <owner/repo>
PR: <URL and number>
Base Revision: <full SHA>
Head Revision: <full SHA>
Decision: <findings | no findings | stale | blocked | draft only>
Review Event: <COMMENT | not posted>
GitHub Review: <verified URL | not posted>

### Findings
- <classification, path:line or summary placement, and concise concern>

### Scope
- Production-code files reviewed: <paths/count>
- Excluded files: <test/generated/vendor/lockfile paths/count>
- Tests and CI: not run or assessed

### Posting Evidence
- <review ID and verified inline-comment URLs, or blocker>
```

This result is only a code-structure and software-design review. It is not
approval of correctness, security, requirements, tests, product behavior,
visual design, CI, merge readiness, or release readiness.
