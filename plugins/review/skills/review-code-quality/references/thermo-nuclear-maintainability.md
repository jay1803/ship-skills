# Thermo-Nuclear Maintainability Lens

This is the default rubric for `$review-code-quality`, in orchestrated and
standalone review alike. Omitted or legacy `Review Lens: default` input uses
this rubric; new Review envelopes record `Review Lens: thermo-nuclear`.
The rubric does not change the specialist's native output or evidence bar.

## Boundary

- Return maintainability findings to the caller under the code-quality finding
  contract. Do not post, orchestrate other reviews, or change their execution order.
- Preserve approved behavior and product scope. Recommend a structural change
  only when it has concrete diff or surrounding-code evidence and a plausible
  behavior-preserving path.
- Treat file size as evidence, not a verdict. Crossing roughly 1000 lines is a
  strong decomposition signal only when the PR causes the growth and a clearer
  ownership split is available.
- Do not demand speculative rewrites, novelty, abstraction for its own sake, or
  a large refactor whose risk is disproportionate to the demonstrated problem.

## Reviewer Prompt

Perform an unusually strict maintainability audit of the PR diff and the
surrounding code. Search for a concrete "code-judo" move: a behavior-preserving
reframing that deletes concepts, branches, modes, wrappers, or layers instead of
merely rearranging them. Be ambitious when the evidence supports a materially
simpler design, but keep every finding actionable and tied to the current change.

For each meaningful change, test these questions:

- Did the PR create structural regression, incidental complexity, or a missed
  opportunity for an obvious and materially simpler implementation?
- Did it scatter feature flags, nullable modes, special-case conditionals, or
  edge handling through an already busy flow?
- Is there a missing state model, policy, dispatcher, pure function, component,
  or module that would remove branching rather than hide it?
- Does an abstraction earn its indirection, or is it a thin wrapper, identity
  helper, generic mechanism, cast, `any`, `unknown`, or optional boundary that
  obscures a simpler invariant?
- Is the logic in the canonical owning layer and reusing canonical helpers, or
  is feature detail leaking across an API/package boundary?
- Did the change make a cohesive file too large or coupled to scan? If so, is
  there a concrete ownership-based decomposition rather than an arbitrary split?
- Is orchestration unnecessarily sequential, or can related updates leave
  partial state when a clearer parallel or atomic structure is available?

Prefer remedies that delete a layer, simplify the state model, collapse
duplicate branches, move ownership to the canonical layer, make a type boundary
explicit, extract one focused unit, or make related updates atomic. Do not settle
for naming or formatting nits when the real issue is structural.

## Finding Bar

Return a maintainability finding only when all of these are true:

1. The regression or missed simplification is concrete in the diff and relevant
   surrounding code.
2. It materially increases reader state, coupling, branching, indirection, or
   future change risk.
3. A specific behavior-preserving direction is available.
4. The expected improvement justifies the refactor risk and scope.

Treat a finding as blocking when the PR clearly worsens architecture, scatters
special cases, crosses ownership boundaries, adds unearned abstraction, or
causes unjustified file sprawl and the cleaner path is concrete. Prefer a small
number of high-confidence findings over a long list of cosmetic comments.

Return `no findings` when no candidate meets the code-quality contract. Use
its native classifications and distinguish optional improvements from blocking
maintenance risk; this lens does not create a separate approval or output schema.

## Provenance

This compact lens adapts the structural-review intent of Cursor's
[Thermo-Nuclear Code Quality Review](https://github.com/cursor/plugins/blob/main/cursor-team-kit/skills/thermo-nuclear-code-quality-review/SKILL.md)
to the Dev workflow's existing correctness gates, read-only reviewer role, and
GitHub verification contract.
