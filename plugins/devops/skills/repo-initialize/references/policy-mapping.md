# Repository Policy Mapping

Read when selecting module paths, migrating existing agent documentation, or
changing branch/merge, release, or deployment guidance.

## Ownership

| Concern | Canonical destination or owner |
| --- | --- |
| Development base, PR target, branch names, integration merge conditions | `.agents/policies/development.md` |
| Production promotion branches and merge executor | `.agents/policies/release.yaml`, interpreted by global `$release` |
| Version files, changelog, publication ordering | `.agents/runbooks/release.md` |
| Exact environment, artifact, rollout, verification, rollback | `.agents/skills/deploy/SKILL.md` via `$deploy-skill-creator` |
| Code and architecture constraints | `.agents/policies/coding.md` |
| Validation requirements | `.agents/policies/validation.md` |
| Skill addition, modification, renaming, and removal | `.agents/policies/skills.md` |
| Rule index and essential repository instructions | Root `AGENTS.md` |

Markdown policies are contextual instructions for the Agent. Do not describe
arbitrary YAML policy files as machine-enforced contracts. Reuse established
project rules without duplicating their contents. These are standard names for
adopted modules, not a requirement to create every file. Root `AGENTS.md` links
them directly with reading triggers; do not add `.agents/README.md` as another
index. Existing inline instructions may stay in root AGENTS.

When adopting this layout, migrate in-scope existing agent documents to their
standard paths while preserving semantics and updating consumers. For example,
`.agents/release.md` becomes `.agents/runbooks/release.md`. A documented repository
exception or explicit request to preserve a path takes precedence; merely finding
an old path does not make it an exception. Keep external/runtime-required paths
when moving them would break a consumer, and document the exception in root
AGENTS. Follow [layout migration](template-operations.md#layout-migration) for
conflicts, relative links, legacy index contents, and update bookkeeping.

## Resolve Decisions from Evidence

Before selecting the split-branch development/release modules, establish the
actual integration branch, production promotion path, required PR/review/checks,
merge executor, merge method, and whether platform auto-merge is allowed. Prefer
current project policy and explicit owner decisions. Recent PR history alone
cannot grant merge authority. Ask for a missing authority decision only when the
requested setup needs it; otherwise leave that optional module absent.

Agent execution of a merge and enabling platform auto-merge are separate
capabilities. Allowed capability also needs authorization from the current
request and passing live hosting gates. Never copy a permissive example over a
human-owned merge decision under the guise of template maintenance.

## Release and Deployment Contracts

Read the canonical
[release-policy/v1 contract](../../release/references/repository-release-policy.md)
when generating or adapting `release.yaml`. It defines valid executor/method/
authorization combinations, branch existence, the explicit missing-file default,
and the remote default branch as the source of effective policy. A worktree or
unmerged PR cannot authorize itself. A malformed present policy is not absence.

The template's `release` module contains the contract's human-merge default.
Adopting it is optional; it does not create `develop` or `main`. Agent merge may
be configured only from an explicit applicable project decision using the
contract's valid fields, never from a generic initialization/update request.

Read the canonical
[release-deploy/v1 contract](../../release/references/project-deploy-contract.md)
when a deploy Skill is needed. Its `deploy` and `verify` actions are separate,
accept immutable revisions, and return runtime evidence. Keep credentials out
of authored files. Do not use a generic template to invent provider commands,
accounts, hosts, rollout triggers, or rollback authorization. Reuse a working
project deploy Skill instead of duplicating it.

## Current Compatibility Boundary

The audited Develop 0.6.x `dev-merge-handoff` routes `main` PRs to `$release`;
`release-policy/v1` requires distinct promotion source/target branches. General
agent guidance can be initialized in a main-only repository, but this does not
make its full automated Dev merge/release lifecycle supported. Preserve its
branch model, omit incompatible split-branch modules, and report the boundary.
Inspect the installed Skills on later runs because support may evolve. Do not
rewrite global Skills or create branches as an unrequested workaround.
