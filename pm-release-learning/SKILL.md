---
name: pm-release-learning
description: >-
  Summarize product learning after a feature ships and draft user-friendly release notes from shipped issues, merged PRs, or the latest main commit. Use after merge or release to capture what was built, assumptions tested, metrics to watch, feedback, open risks, follow-up issues, changelog copy, App Store release notes, or plain-language release summaries.
---

# PM: Release Learning

Close the product loop after shipping and communicate what changed.

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
- "Validation" -> "You will now see a clearer message when..."
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

## Sub-Agent Contract

This skill is safe to run inline or as a bounded sub-agent. When delegated:

- Use only the request, provided sources, and directly referenced release, PR, issue, or tracker context.
- Produce the release notes, release learning artifact, and any allowed follow-up drafts.
- Follow this skill's tracker-write rules; do not edit issue descriptions unless this skill explicitly owns that write.
- Return sources read, writes applied or drafts, blockers, and open questions.

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
