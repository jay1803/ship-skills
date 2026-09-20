---
name: repo-initialize
description: "Initialize or update a repository's AGENTS.md and optional .agents policies from the agent repository template while preserving project-specific rules."
metadata:
  owner: jay1803
  family: devops
  maturity: stable
  distribution: devops
---

# Repository Initialization and Updates

Produce or update repository-local agent guidance from one pinned template
revision. `AGENTS.md` is the entrypoint, `.agents/` owns project rules and
procedures, and shared Skills own reusable workflows. Return a scoped,
reviewable repository diff.

Use for requests such as "initialize this repository for our agents", "add the
optional repository policy layout", or "update our agent template while keeping
local rules". Ordinary feature implementation, executing a deployment, and
installing global Skills are separate jobs; do not turn them into repository
initialization.

## Source and Scope

The canonical template and updater live in
[jay1803/agent-repo-template](https://github.com/jay1803/agent-repo-template).
Read [template operations](references/template-operations.md) when fetching,
previewing, applying, or upgrading it. Keep the template and updater there;
do not bundle a second copy in this Skill.

Resolve the target repository and physical checkout path before writing. Read
its `AGENTS.md`, applicable nested instructions, `.agents/` rules, established
local Skills, relevant manifests, and CI/release documentation. Inspect Git
status, branch, remotes, and existing worktrees. Preserve unrelated edits and
submodule state; use the repository's required issue/worktree/PR process when
applicable. Do not import the Skills source repository's tracker or branch
policy into an unrelated project.

Initialization authorizes the requested guidance changes. It does not itself
authorize creating a GitHub repository, changing visibility/protection, merging,
publishing, deploying, installing plugins, or modifying global configuration.
When the user requests a GitHub template-derived repository, resolve its owner,
name, and visibility, create it within that scope, and verify the returned repo.
Otherwise operate on the existing local repository.

## Select the Smallest Applicable Content

- Root `AGENTS.md` is the sole rule index; link adopted policies and SOPs
  directly with their reading triggers. Do not add a secondary `.agents/README.md`.
  Missing optional rules do not require filling out every module or asking
  routine engineering questions.
- Existing project decisions and maintained documents determine the adaptation.
  Use the standard paths in [policy mapping](references/policy-mapping.md) for
  adopted modules. Preserve rule meaning while migrating in-scope documents and
  updating their consumers; preserve a different path only for a documented
  repository exception. Existing inline rules can remain in `AGENTS.md`.
- Select coding, validation, or local-Skill maintenance modules when requested
  or when repository evidence makes their inclusion useful. Adapt them to
  actual conventions and runnable commands; omit unsupported claims.
- Read [policy mapping](references/policy-mapping.md) before adding or changing
  branch, merge, release, or deployment guidance. Do not turn an inactive example
  into a new permission or mandatory project rule without an owner decision.
- Keep `.template/modules/` examples inactive. A deploy Skill requires real
  operational evidence; route that bounded authoring task to
  `$deploy-skill-creator` when requested or needed for the selected scope.

No file is required solely because the template offers it. Missing ordinary
engineering guidance falls back to repository evidence and applicable Skill
defaults. Missing authority does not grant an external action. If a declared
rule is broken, invalid, or conflicts with another rule, resolve that boundary
before the dependent operation; continue independent authorized work.

## Initialize or Update

Preview against the inspected checkout before applying. Read the proposed source
content as well as the path/status receipt. Proceed with reversible, in-scope
changes already authorized by the user; a preview is not an extra approval gate.
Ask only for an unresolved project decision or additional authority that matters.

For a new adoption, add only the selected guidance. Preserve existing project
instructions around the managed block and avoid duplicate discovery sections.
For existing layout migration, follow [the migration procedure](references/template-operations.md#layout-migration)
to move documents, repair relative links, and retire the old index and its ledger
entry. A request to preserve rules does not by itself freeze their old paths.
For an update, use `.agents/template-state.json` and the prior source revision
to distinguish upstream changes from local customizations. The updater applies
only the safe subset and reports preserved files; it does not perform a semantic
merge. Reconcile reported files deliberately from the old source, current file,
and new source when the user's scope authorizes it. Preserve local restrictions,
removed modules, and unrelated text. A generic update request does not authorize
relaxing merge/release permissions or deleting local Skills.

Do not delete or forge the ledger to force replacement, or treat its hashes as
permission. A changed policy requires semantic review even if the local file was
untouched. Report pending policy changes separately from currently effective
remote policy. A retired template file remains local until removal is explicitly
within scope and its consumers have been checked.

## Validation and Completion

Check the final diff against the selected modules and project decisions. Verify
required links resolve, optional discovery paths are accurately described,
commands come from real repository evidence, and no active scaffolding tokens,
credentials, or machine-specific facts were introduced. Run the pinned template's
focused tests/checker when adopting a new source revision and use the target
repository's applicable validation. A repeat preview should show no unintended
writes; deliberate local customizations may remain reported as preserved.

For a newly generated deploy Skill, use its own structural and behavioral checks.
Do not run deployments to test initialization. Do not claim the full Develop
lifecycle supports a project's branch model without checking the installed
workflow; report the concrete compatibility boundary when it does not.

Follow the target's authorized delivery policy for commits, PRs, and review.
Return the repository, template revision, enabled/omitted modules, changed and
preserved files, validation results, compatibility or decision gaps, and actual
commit/PR state. Distinguish authored guidance from integrated source, installed
Skills, and effective release authority. No plugin publication or local/global
installation follows automatically from authoring this artifact.
