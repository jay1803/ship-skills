---
name: release
description: "Orchestrate a production release under repository policy, including promotion, tag, optional project deployment, and GitHub Release. Excludes ordinary issue delivery."
metadata:
  owner: jay1803
  family: devops
  maturity: stable
  distribution: devops
---

# Release: Orchestrator

Own the global production-release state machine. `$release` decides what is
being released and whether the release may advance. When a repository provides
a project deploy skill, that skill owns how an exact revision is deployed and
verified; otherwise `$release` uses the GitHub-only release route.

Read [the repository release policy contract](references/repository-release-policy.md)
before resolving branches, creating or reusing a release PR, or deciding who may
merge it. `$release` reads `.agents/policies/release.yaml` directly from the
live remote default branch; it does not require or use `AGENTS.md` as a
release-policy source.

The policy's promotion source maps to `test`; its promotion target maps to
`production`. When the policy file is absent, the contract supplies this safe
default:

```text
develop -> test
main    -> production
```

Do not rename branches to environments. Configured branch names are
source-control roles; `test` and `production` are runtime environments.

Read [references/project-deploy-contract.md](references/project-deploy-contract.md)
before invoking or accepting a project deploy skill.

## Boundary

- `$dev` and `$dev-merge-handoff` own issue delivery through a merged PR into
  the repository's integration branch and the corresponding test-environment
  evidence.
- `$release` owns release scope, production-promotion readiness, the
  policy-configured promotion PR and merge decision, version/tag decisions,
  project-deployment orchestration when available, GitHub Release publication,
  and release closeout.
- The project deploy skill owns project-specific build, migration, upload,
  rollout, runtime verification, and rollback procedures.
- `$release` must not copy project-specific deployment commands into this
  global skill or improvise them. It also must not create deployment work solely
  because a repository has no deploy skill.
- Repository policy defines capability, not run authorization. A release
  request authorizes only the requested release lifecycle. A request
  to inspect, plan, draft, or prepare a release does not authorize merging,
  tagging, deploying, publishing, or rollback.

## Repository Release Policy Resolution

1. Resolve the Git root, fetch the live remote, resolve its default branch, and
   read exactly `.agents/policies/release.yaml` from that remote branch before
   release mutations. Never use the current worktree or promotion source's
   copy to grant merge authority.
2. Validate it against `release-policy/v1`. If it is absent, use and disclose
   the contract's built-in human-merge `develop -> main` default. If it is
   present but invalid, stop mutation with `blocked - invalid release policy`.
3. Capture the configured source branch, target branch, PR requirement, merge
   executor, Agent authorization mode, auto-merge rule, and merge method.
4. Re-fetch and re-read the authoritative remote-default-branch file
   immediately before PR creation/reuse and before merge or auto-merge. A
   changed policy invalidates the prior merge decision.
5. Compute effective authority from repository policy, the current user request,
   and live GitHub enforcement. Never treat one as overriding another.

## Project Deploy Skill Resolution

Resolve the release route before starting an environment deploy or verification:

1. Prefer `<repo>/.agents/skills/deploy/SKILL.md`.
2. Otherwise use `<repo>/.codex/skills/deploy/SKILL.md` when that is the
   repository's established local-skill root.
3. Otherwise use an explicitly named project-specific deploy skill supplied by
   repository instructions or the user.
4. If none exists, select the `github-only` route. Do not route to
   `$deploy-skill-creator`, fabricate deployment commands, or treat the absence
   as a readiness gap. Test and production environment evidence are
   `not-applicable`; release-critical Git and GitHub checks still apply.
5. If several candidates conflict, stop and report the candidates instead of
   guessing.

For the project-deploy route, read the resolved project skill completely.
Confirm that it supports the `production` environment, consumes an exact commit
or tag, and can return the required deployment receipt. A generic command
mentioned in a README is not a substitute for the project deploy contract.

The `github-only` route can complete an explicitly authorized GitHub Release
after the configured promotion, merge, tag, and GitHub checks succeed. It does
not claim that a production environment is running the tagged revision, and it
does not produce or require a deployment receipt.

## Release State

Maintain one explicit state:

```text
scoping
-> release-pr-open
-> test-verified (project-deploy) | test-not-applicable (github-only)
-> merge-ready
-> promotion-merged
-> tagged
-> deploying-production -> production-verified (project-deploy)
   | production-not-applicable (github-only)
-> github-release-published
-> complete
```

Valid stop states are `waiting`, `blocked`, and `failed-deployment`. Never skip
required test or production verification on the project-deploy route. On the
GitHub-only route, record both environment stages as `not-applicable` and do
not treat a GitHub Release page as proof that production is running the intended
revision.

## Release Scope And Version

1. Fetch live remote and GitHub state before making release claims.
2. Capture the exact configured remote source and target SHAs and compare them
   with:

   ```bash
   git rev-list --left-right --count origin/<target>...origin/<source>
   git diff --check origin/<target>...origin/<source>
   gh pr list --state open --base <target> --head <source>
   ```

3. Build release scope from the commits, merged PRs, linked issues, migrations,
   generated artifacts, compatibility notes, and rollback constraints present
   in the configured target-to-source range. Do not silently include unrelated
   or unreviewed work.
4. Resolve the version from the repository's documented convention, package
   metadata, or explicit user input. Do not invent a new versioning scheme.
5. Before drafting release notes, read
   [references/release-notes.md](references/release-notes.md). Follow repository
   writing guidelines first; otherwise use the English default template and
   include only sections supported by this release. Keep internal implementation
   detail in validation or risk notes unless users need it to act safely.
6. If repository policy requires version, changelog, or generated-release files
   to change before promotion, make one scoped release-preparation commit on
   the configured source from an isolated clean worktree, push it, update the
   candidate SHA,
   and rerun the test-environment gate. Never modify an unrelated dirty checkout.

If the source contains no releasable change, return `no-op`. If the target
contains changes absent from the source, report divergence and require a safe
reconciliation plan before promotion; never overwrite either branch.

## Production PR

Create or reuse exactly one PR with the configured target as base and source as
head. The PR must identify the candidate SHA, release version, user-facing
changes, validation, release route, and known risks. Include a deploy/rollback
plan only for the project-deploy route.

Re-fetch and re-read the authoritative repository release policy before the PR
mutation. If a reusable PR does not match the current configured source and
target, report the mismatch instead of repurposing it.

## Test Environment Gate

On the project-deploy route, the exact configured source candidate must have
test-environment evidence before the production PR becomes ready:

- If source-candidate deployment is automatic, call the project deploy skill
  with `action: verify`, `environment: test`, and the exact candidate SHA.
- If source-candidate deployment is manual and the user authorized the full release,
  call it with `action: deploy`; otherwise report the required action.
- Require the returned `observed_ref` to match the candidate or an explicitly
  documented immutable equivalent.
- Treat failed health checks, smoke tests, migrations, or version-integrity
  checks as release blockers.

Do not substitute local tests or green CI for the project's runtime test receipt.

On the GitHub-only route, record test-environment evidence as `not-applicable`.
Do not invent a test environment or call a deploy skill; retain the required
source-control, GitHub-check, review, and mergeability gates.

## Merge Decision

Before declaring readiness, verify live:

- the PR still represents the intended configured source candidate;
- required CI and repository release checks pass;
- mergeability is clean and required review is complete;
- project-deploy test-environment verification matches that candidate, or the
  GitHub-only route has explicit `not-applicable` environment evidence;
- release notes and version remain accurate;
- the current repository release policy still matches the PR source and target;
- the current request satisfies any configured Agent authorization; and
- the configured merge method and auto-merge behavior are permitted by live
  GitHub rules.

Apply the executor behavior from `release-policy/v1`:

- `executor: human`: return `ready for human merge` and wait. Do not merge,
  enable auto-merge, enqueue, operate a merge control, call an equivalent API,
  or delegate the action.
- `executor: agent`: merge with the configured method only when the current
  request satisfies `agent_authorization` and every live gate passes. Enable
  auto-merge only when policy says `allowed` and the same current authorization
  covers it. Otherwise wait with the exact missing authorization or gate.

Never bypass branch protection, use an administrator override, force-update a
ref, substitute another merge method, or delegate around the policy. After the
configured executor acts, re-fetch GitHub and remote state. Advance only when
the PR is confirmed merged and record the exact target commit.

## Tag And GitHub Release

1. Re-run the release-critical checks against the confirmed target commit.
2. Ensure the intended tag does not already point elsewhere locally or remotely.
3. Create an annotated tag on the exact confirmed target commit and push only that
   tag. Never move or reuse a published version tag.
4. On the project-deploy route, create or update a draft GitHub Release for that
   tag. Keep it draft until the production deployment receipt passes, unless
   repository evidence explicitly defines GitHub Release publication as the
   deployment trigger.
5. On the GitHub-only route, publish the GitHub Release after the tag and
   release-critical checks pass.
6. If publication triggers deployment on the project-deploy route, publish,
   invoke the project deploy skill in `verify` mode, and keep the release
   incomplete until verification passes.

## Production Deployment

Only on the project-deploy route, invoke the resolved project deploy skill using
`release-deploy/v1` with the exact tag and target commit. Do not translate its
project-specific steps into ad-hoc commands in the release controller. The
GitHub-only route has no production-deployment phase.

Accept success only when the receipt proves:

- the target is production;
- the observed running revision matches the requested immutable revision;
- required migration, rollout, health, and smoke checks passed;
- rollback information is present when the project supports rollback.

On deployment failure, leave the GitHub Release as draft when possible, preserve
the tag as immutable evidence, and return `failed-deployment`. Do not silently
retag, publish success, or initiate rollback without explicit authorization or
an already-authorized project policy.

## Closeout

After the project-deploy route's production verification, or after GitHub
Release publication on the GitHub-only route:

1. Publish the GitHub Release and verify that it targets the exact tag.
2. Record the release PR, target commit, tag, route, verification evidence,
   risks, and rollback target. Record a deployment receipt and environment only
   for the project-deploy route; otherwise record them as `not-applicable`.
3. Reconcile the configured source with post-release target changes using the
   repository's safe synchronization policy; never force-update or discard
   unrelated work.
4. Update only tracker records actually covered by this release. Preserve any
   required outcome-verification or human-acceptance state that remains open.
5. Report release completion after GitHub Release publication is confirmed and,
   on the project-deploy route only, production verification is confirmed.

## Output

```markdown
## Release Result

Decision: <no-op | waiting | blocked | release PR open | ready for human merge | ready for merge authorization | failed-deployment | complete>
Project: <name>
Release version: <version>
Release PR: <URL or not created>
Release policy: <remote default branch, path, and digest | built-in missing-file default>
Promotion: <source -> target>
Merge policy: <executor, Agent authorization, auto-merge, method>
Candidate: <SHA>
Target commit: <SHA or pending>
Tag: <tag or pending>
GitHub Release: <draft URL | published URL | pending>
Release route: <project-deploy | github-only>
Project deploy skill: <path or name | not-applicable>

### Environment Evidence
- Test: <requested ref, observed ref, checks, receipt | not-applicable>
- Production: <requested ref, observed ref, checks, receipt | not-applicable>

### Scope
- <included PRs/issues and user-facing changes>

### Gates And Risks
- <review, CI, migration, compatibility, rollback, unresolved items>

### Next Action
- <human merge, Agent merge authorization, repair, deploy authorization, rollback decision, or none>
```
