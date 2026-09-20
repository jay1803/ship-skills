---
name: pm-release-learning
description: Draft evidence-backed release notes or summarize post-release product learning from shipped changes and feedback.
metadata:
  owner: jay1803
  family: product
  maturity: stable
  distribution: product
---

# PM: Release Learning

Close the product loop after shipping and communicate what changed.

For a standalone analysis or draft, follow the
[Product Artifact Contract](../pm/references/artifact-contract.md) and complete
the requested artifact without tracker setup. The tracker steps below apply
only to an issue-bound lifecycle or authorized publication.

## Modes

- Use **Release Learning** when the user asks what shipped, what was learned, which assumptions were tested, what metrics to watch, or which follow-up issues should exist after a release.
- Use **Release Notes** when the user asks for release notes, changelog copy, app update text, App Store release notes, or a plain-language summary of what was just released.

## Release Learning Workflow

1. Read the shipped issue, merged PR, release notes, product spec, review comments, and available feedback or metrics.
2. Summarize what actually shipped, not what was originally hoped for.
3. Name the assumption or learning question the release tests.
4. Identify metrics, guardrails, and feedback channels to watch.
5. Recommend follow-up issues only when they are concrete and tied to learning, risk, or deliberately deferred scope.

## Release Notes Workflow

1. Prefer the user's supplied shipped issue, PR, release branch, product spec, or implementation notes when available.
2. When asked to draft notes from the latest primary-branch commit, run this from the target repository:

   ```bash
   python3 <skill_dir>/scripts/latest_main_commit.py
   ```

   Use `--fetch` only when refreshing the remote branch is appropriate. Use `--ref <branch>` when the repository uses another primary branch.
3. Read the commit subject, body, changed files, stats, and diff. If the behavior is ambiguous, inspect nearby tests or docs touched by the commit before drafting.
4. Infer user-visible changes from implementation details. If the diff is purely internal, say so and write a short internal-only note instead of inventing user-facing features.
5. Draft concise release notes in normal-user language.
6. Verify every note is supported by the source material. Remove details that are only guesses.

## Release Notes Style

- Use simple words and short sentences.
- Lead with the user benefit, not the implementation.
- Avoid commit hashes, file names, function names, APIs, database tables, and framework terms unless the user asks for technical notes.
- Do not mention "the latest commit" in the final notes.
- Do not overstate the release. Small fixes should get small notes.
- Prefer bullets when there are multiple changes.
- Keep App Store style notes to 1-4 bullets or a short paragraph.

Translate implementation language into user language:

- "Refactored", "migration", "schema", "RPC", "cache", "state management" -> describe the visible result.
- Describe validation changes only when the diff proves a user-visible result;
  an internal validation change does not imply new messaging.
- "Crash", "exception", "race condition" -> "Fixed an issue where..."
- "Performance" -> "Made ... faster" only if the source material supports a real speed or responsiveness improvement.
- "UI polish" -> name the screen or action users recognize.

## Output Shapes

For release notes, use this shape unless the user asks for a specific format:

```markdown
## Release Notes

- Added ...
- Improved ...
- Fixed ...
```

Only include categories that are true. If there is one small change, use one plain sentence instead of forcing categories.

For product learning, use this shape:

```markdown
## Release Learning

### Shipped
- <User-visible or operator-visible behavior delivered.>

### Assumption Tested
- <Assumption this release is meant to validate.>

### Metrics To Watch
- <Metric, guardrail, or feedback source.>

### Early Feedback / Evidence
- <Known feedback, support signal, metric, or "Not available yet.">

### Product Gaps
- <Known gap, tradeoff, or deferred scope.>

### Follow-Up Issues
- <Issue title, why it matters, priority, or "None.">
```
