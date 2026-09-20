# Ship Skills

Source monorepo for jay1803's product, engineering, design and research agent
skills. Related skills ship together as versioned plugins for Codex and Claude
Code, so a machine can install exactly the lifecycle it needs.

> 中文版见 [`README.zh-CN.md`](README.zh-CN.md)。

## Repository model

```text
ship-skills/
├── plugins/
│   ├── product/    # issue intake through dev-ready scope and acceptance
│   ├── develop/    # dev-ready issues through implementation and merge handoff
│   ├── review/     # independent specification, correctness and quality review
│   ├── devops/     # repository setup and production release
│   ├── design/     # design direction through design review
│   ├── project/    # project proposal, kickoff, updates and closeout
│   └── research/   # open questions through decision-ready evidence
├── catalog/        # generated machine-readable inventory
├── scripts/        # install, catalog, packaging, validation
└── wiki/           # workflow and catalog documentation
```

| Plugin | Skills | Scope |
| --- | --- | --- |
| `product` | 14 | Shape issues and projects into dev-ready outcomes. |
| `develop` | 16 | Build and ship dev-ready issues and dependency chains. |
| `review` | 6 | Review PR code and orchestrate isolated review lenses. |
| `devops` | 3 | Set up repositories and prepare and execute releases. |
| `design` | 6 | Design flows, screens, prototypes, systems, and visual artifacts. |
| `project` | 8 | Prepare and maintain project lifecycle documents. |
| `research` | 16 | Turn open questions into decision-ready evidence. |

The directories under `plugins/` are the release boundaries. Each has a Codex
plugin manifest, a Claude Code plugin manifest, and an npm package manifest.
Adding a new skill does not require a new repository or npm package: put it in
the plugin whose lifecycle it shares.

The generated inventory is [`catalog/skills.json`](catalog/skills.json). Human
workflow documentation starts at [`wiki/CATALOG.md`](wiki/CATALOG.md) and
[`wiki/PM_DEV_WORKFLOW.md`](wiki/PM_DEV_WORKFLOW.md).

## Install in Codex

The preferred install path is this repository's local Codex marketplace:

```bash
codex plugin marketplace add ~/github/ship-skills
codex plugin add product@jay1803-ship-skills
codex plugin add develop@jay1803-ship-skills
```

Plugin installs are independent, so a machine can install only the series it
needs. The same names work for `review`, `devops`, `design`, `project` and
`research`.

## Install in Claude Code

```bash
claude plugin marketplace add ~/github/ship-skills
claude plugin install product@jay1803-ship-skills
```

Installed skills are invoked as `/product:pm`, `/develop:dev`, and so on.

For development, or to expose every plugin skill directly to Codex and Claude
Code, use the idempotent local linker:

```bash
cd ~/github/ship-skills
./scripts/install-local.sh
./scripts/install-local.sh --check
```

By default it links active skills into both `~/.agents/skills` and
`~/.claude/skills`. It never replaces unrelated files or links. Use
`--target-dir PATH` to validate or install into a staging directory.

## npm packages

The repository is a private npm workspace with one publishable package per
plugin:

| Package | Source | Purpose |
| --- | --- | --- |
| `@jay1803/ship-skills-product` | `plugins/product` | product readiness and scope |
| `@jay1803/ship-skills-develop` | `plugins/develop` | engineering delivery |
| `@jay1803/ship-skills-review` | `plugins/review` | independent code review |
| `@jay1803/ship-skills-devops` | `plugins/devops` | repository setup and release |
| `@jay1803/ship-skills-design` | `plugins/design` | visual design workflow |
| `@jay1803/ship-skills-project` | `plugins/project` | project lifecycle documents |
| `@jay1803/ship-skills-research` | `plugins/research` | evidence and decision support |

npm is used for semantic versions, tarball contents, and registry distribution.
Codex installation is performed through the plugin marketplace so the runtime
can register manifests and skills correctly. Before publishing:

```bash
npm run check
npm run pack:check
npm publish --workspace @jay1803/ship-skills-product
```

Publishing is intentionally not automated by this repository yet.

## Add or move a skill

Every active skill must live at:

```text
plugins/<plugin>/skills/<skill-name>/SKILL.md
```

The skill directory and frontmatter `name` must match. Active skills also carry
these metadata fields:

```yaml
metadata:
  owner: jay1803
  family: <plugin>
  maturity: stable
  distribution: <plugin>
```

`family` and `distribution` both equal the plugin directory name, which
`npm run check` enforces.

After a change:

```bash
npm run catalog
npm run check
npm run pack:check
git diff --check
```
