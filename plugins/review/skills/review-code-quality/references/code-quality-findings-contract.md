# Code Quality Findings Contract

Contract version: `1`

`$review-code-quality` is an isolated specialist for demonstrable maintenance
cost, unnecessary abstraction, and codebase-health risks in one frozen pull
request or immutable diff. It is not a reviewer orchestrator, a correctness or
security review, Product Review, Design Review, or a license for aesthetic
rewrites.

## Finding Bar

Emit a finding only when all of the following are true:

1. The frozen change introduces or preserves a concrete structure that causes
   material recurring maintenance cost: a likely repeated edit burden, obscured
   ownership or control flow, needless policy duplication, or a proven obstacle
   to safely extending or debugging the changed behavior.
2. Evidence ties that cost to the diff and to relevant callers, ownership
   boundaries, tests, local conventions, or the governing contract. Cite paths,
   symbols, and the maintenance scenario precisely enough for another reviewer
   to check.
3. A smaller, direct alternative is concrete, bounded to the affected behavior,
   and compatible with the governing specification and established public or
   integration contracts.
4. The alternative has proportional benefit. It must reduce the identified
   maintenance cost without expanding into an unrelated rewrite, speculative
   future-proofing, or a preference-only cleanup.
5. The concern is not better classified as correctness, security, privacy,
   authorization, or specification compliance. Route those concerns to their
   owning lens instead.

Classify a finding as `blocking maintenance risk` only when leaving the
structure in place creates a material and near-term codebase-health cost for
the changed path. Use `optional improvement` for a concrete, bounded
simplification with a real but non-blocking benefit.

## Withhold Instead Of Finding

Do not emit a finding for naming, formatting, subjective style, or a local
pattern difference alone. Do not require a simpler structure when inspected
behavior, compatibility, lifecycle, or integration evidence justifies the
complexity. Do not use the specialist to pressure a broad refactor merely
because a smaller local alternative exists.

Withhold an individual candidate when its necessary evidence is unavailable;
retain unrelated confirmed findings. This alone does not make the review
incomplete. Use `context insufficient` only if the missing evidence prevents
inspection of a required part of the assigned surface; name that coverage gap
and retain any proven findings. A completed `no findings` result means no
candidate met this lens's bar, not that unrelated review lenses passed.

## Required Finding Shape

```markdown
### [blocking maintenance risk | optional improvement] Concise title

Maintenance scenario: <recurring edit, debugging, ownership, or extension action>

Material cost: <specific burden caused by the frozen structure>

Evidence: <changed path/symbol plus caller, convention, contract, test, or command>

Bounded alternative: <smallest direct, spec-compatible change that reduces the cost>

Scope check: <why the alternative is proportional and does not become a broad rewrite>
```

If a finding cannot be written in this form with concrete evidence and a
proportional alternative, withhold it.
