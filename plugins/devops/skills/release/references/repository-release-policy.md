# Repository Release Policy

Contract version: `release-policy/v1`

The repository owns its production-promotion branches and merge authority in:

```text
<repo>/.agents/policies/release.yaml
```

`$release` resolves the live remote default branch and reads this exact
repository-relative path from that branch. It does not grant authority from the
current worktree, a feature branch, or the promotion source branch. `AGENTS.md`,
a README, the project deploy skill, memories, prior runs, and inferred
conventions are not substitutes for this policy and do not override it.

## Schema

```yaml
schema: release-policy/v1
promotion:
  source: develop
  target: main
  pull_request: required
  merge:
    executor: human
    agent_authorization: not-applicable
    auto_merge: forbidden
    method: repository-default
```

Required values:

- `schema`: exactly `release-policy/v1`.
- `promotion.source` and `promotion.target`: distinct, non-empty branch names
  that resolve on the live remote.
- `promotion.pull_request`: exactly `required` in version 1.
- `promotion.merge.executor`: `human` or `agent`.
- `promotion.merge.agent_authorization`:
  - `not-applicable` when `executor: human`;
  - `explicit-release-request` when a user request to carry the release through
    completion authorizes the merge after all gates pass; or
  - `explicit-merge-request` when the user must explicitly request the merge in
    addition to asking for release preparation.
- `promotion.merge.auto_merge`: `forbidden` or `allowed`. `allowed` is valid
  only with `executor: agent`.
- `promotion.merge.method`: `repository-default`, `merge`, `squash`, or
  `rebase`. `repository-default` is valid only with `executor: human`; an Agent
  executor requires an explicit method.

Reject unsupported schema versions, missing required keys, unknown values,
invalid executor/authorization combinations, equal source and target branches,
and branch names that do not resolve on the live remote. An invalid present
policy is `blocked - invalid release policy`; do not silently replace it with a
default or use its partially valid fields for mutations.

## Missing-File Default

When the exact policy path is absent, use the schema example above as an
explicit built-in default: `develop -> main`, PR required, human merge,
auto-merge forbidden, repository-default merge method. Report that the
missing-file default was used. Do not create the file or require an `AGENTS.md`
entry.

The default preserves existing repositories safely without turning the absence
of a policy into a blocker. It does not prevent creating a release PR. A present
but invalid policy remains a blocker because it signals an unresolved repository
decision or typo.

## Effective Authority

The effective action is the intersection of:

1. this repository policy, which defines what the repository permits;
2. the current user's request, which defines what this run is authorized to do;
3. live hosting state, including branch rules, required checks, reviews,
   mergeability, permissions, and supported merge methods.

No source broadens another. A policy that permits Agent merge does not authorize
an unrequested merge. A user request does not override a human executor, branch
protection, a required review, a failing check, or a merge conflict. Never use
administrator bypass, force updates, direct ref writes, another Agent/service,
or a different merge method to evade the effective policy.

Fetch the live remote and re-read the default-branch policy immediately before
creating or reusing the release PR and again immediately before any merge or
auto-merge mutation. If it changed, recompute the effective action and make
sure the PR still has the exact configured source and target.

If the worktree, promotion source, or release PR changes this file, report the
pending policy change but continue using the policy already landed on the live
remote default branch. A policy change takes effect only after it lands there;
an unmerged candidate cannot grant itself merge authority.

## Executor Behavior

For `executor: human`, `$release` prepares the PR and returns `ready for human
merge`. It must not merge, enable auto-merge, enqueue, operate a merge control,
call an equivalent API, or delegate the action. Waiting for the human action is
a valid state, not a failed merge.

For `executor: agent`, `$release` may use the configured merge method only when
the current request satisfies `agent_authorization` and all live gates pass. It
may enable auto-merge only when `auto_merge: allowed`, the same authorization is
present, and delayed merging is within the requested release lifecycle.
Otherwise it waits with the exact missing authorization or live gate.

After either executor acts, re-fetch the PR and remote branches. Advance only
after the PR is confirmed merged into the configured target and record that
exact target commit.

## Deploy Boundary

This policy owns source-control promotion and merge authority. The repository's
project deploy skill owns only environment-specific build, migration, upload,
rollout, runtime verification, and rollback procedures for an exact immutable
revision. It must not decide, override, or grant release-branch merge authority.
