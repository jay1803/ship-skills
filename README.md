# Ship Skills

Source monorepo for jay1803's PM-to-Dev delivery and design agent skills.
Related skills ship together as versioned Codex plugins so a machine can
install exactly the lifecycle it needs.

> 中文版见 [`README.zh-CN.md`](README.zh-CN.md)。

## Repository model

```text
ship-skills/
├── plugins/
│   ├── delivery/   # PM intake through readiness review, Dev repo context
│   │                 through implementation, review, and release handoff
│   └── design/     # design direction through design review
├── catalog/        # generated machine-readable inventory
├── scripts/        # install, catalog, packaging, validation
└── wiki/           # workflow and catalog documentation
```

The two directories under `plugins/` are the release boundaries. Each has a
Codex plugin manifest and an npm package manifest. Adding a new skill does not
require a new repository or npm package: put it in the plugin whose lifecycle
it shares.

The generated inventory is [`catalog/skills.json`](catalog/skills.json). Human
workflow documentation starts at [`wiki/CATALOG.md`](wiki/CATALOG.md) and
[`wiki/PM_DEV_WORKFLOW.md`](wiki/PM_DEV_WORKFLOW.md).

## Install in Codex

The preferred install path is this repository's local Codex marketplace:

```bash
codex plugin marketplace add ~/github/ship-skills
codex plugin add delivery@jay1803-ship-skills
codex plugin add design@jay1803-ship-skills
```

Plugin installs are independent, so a machine can install only the series it
needs.

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

The repository is a private npm workspace with two publishable packages:

| Package | Source | Purpose |
| --- | --- | --- |
| `@jay1803/ship-skills-delivery` | `plugins/delivery` | PM, Dev, release handoff |
| `@jay1803/ship-skills-design` | `plugins/design` | visual design workflow |

npm is used for semantic versions, tarball contents, and registry distribution.
Codex installation is performed through the plugin marketplace so the runtime
can register manifests and skills correctly. Before publishing:

```bash
npm run check
npm run pack:check
npm publish --workspace @jay1803/ship-skills-delivery
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
  family: delivery
  maturity: stable
  distribution: delivery
```

After a change:

```bash
npm run catalog
npm run check
npm run pack:check
git diff --check
```
