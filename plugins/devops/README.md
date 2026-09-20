# DevOps plugin

DevOps groups repository setup, deployment-skill authoring, and production
release orchestration. Each Skill retains its own scope and authorization rules.

## Entrypoints

- [`repo-initialize`](skills/repo-initialize/SKILL.md) initializes or updates
  repository agent guidance and optional policies from the repository template.
- [`deploy-skill-creator`](skills/deploy-skill-creator/SKILL.md) captures an
  evidenced project deployment and verification procedure in a local Skill.
- [`release`](skills/release/SKILL.md) owns repository-policy production
  promotion, tags, optional deployment orchestration, and GitHub Releases.

Develop owns issue delivery and hands production release requests to DevOps.
Project-specific deploy Skills remain in their project repositories. Install
Develop too when invoking the issue-delivery handoff described by a Skill.

Install with `codex plugin add devops@jay1803-ship-skills` or
`claude plugin install devops@jay1803-ship-skills`. In Claude Code, use
`/devops:repo-initialize`, `/devops:deploy-skill-creator`, or `/devops:release`.
This package reorganizes existing Skills without changing their workflows.
