---
name: deploy-skill-creator
description: "Create or update a repository-local deploy skill when a project needs its evidenced deployment and verification procedure captured."
metadata:
  owner: jay1803
  family: devops
  maturity: stable
  distribution: devops
---

# Deploy Skill Creator

Generate one self-contained project deploy skill that implements the
`release-deploy/v1` contract for the repository's actual test and production
environments.

Read the canonical
[project deploy contract](../release/references/project-deploy-contract.md) and
[references/discovery-checklist.md](references/discovery-checklist.md), then
use [assets/deploy/SKILL.md.template](assets/deploy/SKILL.md.template) as the
starting artifact. The template is not an instruction source at runtime; copy
and adapt it into the target repository.

## Output Location

Use this precedence unless the user or repository policy specifies a location:

1. Update an existing repository-local deploy skill in place.
2. Use an existing `.agents/skills` root.
3. Otherwise use an existing `.codex/skills` root.
4. For a new project with neither, create `.agents/skills/deploy/SKILL.md`.

Do not create both local skill roots. The generated skill name is `deploy`
unless repository policy requires a project-qualified name.

## Workflow

1. Resolve the repository root and read repository instructions before writing.
2. Search for existing deploy skills, CI/CD workflows, build scripts, release
   scripts, provider configuration, infrastructure manifests, runtime health
   routes, migration procedures, rollback docs, and version endpoints.
3. Establish live deployment facts for the `test` and `production`
   environments. Consume the exact immutable revision supplied by `$release` or
   `$dev-merge-handoff`; do not infer environment or merge authority from a
   branch name.
4. Determine whether each environment deploys automatically or requires an
   explicit operation, and how an exact commit/tag maps to a built artifact.
5. Identify exact authorization, account/project/host/region selection,
   migration ordering, rollout, readiness, smoke, revision-integrity, retry,
   stop, and rollback behavior.
6. Update an existing deploy skill rather than replacing project knowledge. For
   a new skill, render the template and remove every placeholder and irrelevant
   optional section.
7. Keep secrets out of the skill. Name required credential variables or login
   prerequisites without copying their values.
8. Validate the generated skill structurally with the environment's
   `quick_validate.py`, then review it behaviorally against one realistic test
   verification request and one production deployment request without mutating
   a live environment.
9. If the generated skill is tracked by the project repository, hand it to the
   normal `$dev` workflow for review and merge into `develop`; creating the
   artifact does not authorize committing directly to a protected branch.

## Missing Information

Do not fill operational gaps with plausible commands. A generated skill may be
complete and honest while declaring a deployment path `blocked` pending a named
fact, provided it includes:

- the exact missing decision or evidence;
- how it should be discovered;
- which mutations are forbidden until it is resolved;
- the read-only verification still available.

Stop before writing when several target projects, providers, accounts, or skill
roots are materially plausible and repository evidence cannot select one.

## Generated Skill Requirements

The artifact must:

- implement `deploy` and `verify` as distinct actions;
- support `test` and `production`, or explicitly block an unsupported target;
- accept a full immutable `requested_ref` and optional release tag;
- never infer target environment from the current checkout or host;
- verify the observed runtime revision and required health/smoke checks;
- declare automatic versus manual deployment for each environment;
- define migration, retry, stop, and rollback boundaries;
- return the `release-deploy/v1` receipt;
- exclude release-policy resolution, release scope, versioning, tag creation,
  promotion merge, and GitHub Release ownership, which remain global `$release`
  responsibilities;
- contain no template tokens, TODO markers, example secrets, or invented facts.

## Output

```markdown
## Project Deploy Skill

Project:
Repository:
Skill path:
Contract: release-deploy/v1

### Capabilities
- Test: <automatic/manual, deploy/verify support>
- Production: <automatic/manual, deploy/verify support>
- Revision integrity:
- Rollback:

### Evidence Sources
- <repo files, workflows, provider/runtime checks>

### Validation
- Structural:
- Behavioral dry run:
- Develop integration: <PR/commit or required next action>

### Unresolved Operational Facts
- <fact and safe stop boundary, or none>
```
