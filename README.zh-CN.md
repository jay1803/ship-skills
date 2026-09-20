# Ship Skills

jay1803 的产品、工程、设计与研究 agent 技能源码 monorepo。相关技能以带版本号的
插件形式一起发布，同时支持 Codex 与 Claude Code，这样一台机器只需安装自己需要的
那条生命周期。

> English version: [`README.md`](README.md)

## 仓库结构

```text
ship-skills/
├── plugins/
│   ├── product/    # 从 issue 受理到可开发的范围与验收标准
│   ├── develop/    # 从可开发 issue 到实现与合并交接
│   ├── review/     # 独立的规格、正确性与可维护性评审
│   ├── devops/     # 仓库初始化与生产发布
│   ├── design/     # 从设计方向到设计评审
│   ├── project/    # 项目提案、kickoff、进展更新与收尾
│   └── research/   # 从开放问题到可决策的证据
├── catalog/        # 自动生成的机器可读清单
├── scripts/        # 安装、目录生成、打包、校验脚本
└── wiki/           # 工作流与目录文档
```

| 插件 | 技能数 | 范围 |
| --- | --- | --- |
| `product` | 14 | 把 issue 和项目梳理成可开发的成果 |
| `develop` | 16 | 交付可开发的 issue 与依赖链 |
| `review` | 6 | 评审 PR 代码并编排相互隔离的评审视角 |
| `devops` | 3 | 初始化仓库、准备并执行发布 |
| `design` | 6 | 设计流程、界面、原型、设计系统与视觉产出 |
| `project` | 8 | 准备并维护项目生命周期文档 |
| `research` | 16 | 把开放问题转化为可决策的证据 |

`plugins/` 下的每个目录是一个发布边界，各自拥有 Codex 插件清单、Claude Code 插件
清单和 npm 包清单。新增技能不需要新建仓库或 npm 包：把它放进与其生命周期一致的插
件即可。

自动生成的清单是 [`catalog/skills.json`](catalog/skills.json)。人类可读的工作流
文档从 [`wiki/CATALOG.md`](wiki/CATALOG.md) 和
[`wiki/PM_DEV_WORKFLOW.md`](wiki/PM_DEV_WORKFLOW.md) 开始。

## 在 Codex 中安装

首选安装方式是本仓库自带的本地 Codex marketplace：

```bash
codex plugin marketplace add ~/github/ship-skills
codex plugin add product@jay1803-ship-skills
codex plugin add develop@jay1803-ship-skills
```

插件安装相互独立，一台机器可以只安装自己需要的那一系列。`review`、`devops`、
`design`、`project`、`research` 同理。

## 在 Claude Code 中安装

```bash
claude plugin marketplace add ~/github/ship-skills
claude plugin install product@jay1803-ship-skills
```

安装后以 `/product:pm`、`/develop:dev` 这样的形式调用。

在开发环境下，或者想让 Codex 和 Claude Code 直接看到每个插件技能，可以使用幂等的
本地链接脚本：

```bash
cd ~/github/ship-skills
./scripts/install-local.sh
./scripts/install-local.sh --check
```

默认会把已激活的技能链接进 `~/.agents/skills` 和 `~/.claude/skills` 两处，绝不会
替换无关的文件或链接。使用 `--target-dir PATH` 可以校验或安装到暂存目录。

## npm 包

本仓库是一个私有 npm workspace，每个插件对应一个可发布的包：

| 包 | 来源 | 用途 |
| --- | --- | --- |
| `@jay1803/ship-skills-product` | `plugins/product` | 产品就绪与范围 |
| `@jay1803/ship-skills-develop` | `plugins/develop` | 工程交付 |
| `@jay1803/ship-skills-review` | `plugins/review` | 独立代码评审 |
| `@jay1803/ship-skills-devops` | `plugins/devops` | 仓库初始化与发布 |
| `@jay1803/ship-skills-design` | `plugins/design` | 视觉设计工作流 |
| `@jay1803/ship-skills-project` | `plugins/project` | 项目生命周期文档 |
| `@jay1803/ship-skills-research` | `plugins/research` | 证据与决策支持 |

npm 用于语义化版本、tarball 内容和注册表分发。Codex 安装通过插件 marketplace 完
成，这样 runtime 才能正确注册清单和技能。发布前：

```bash
npm run check
npm run pack:check
npm publish --workspace @jay1803/ship-skills-product
```

本仓库目前暂未自动化发布流程。

## 新增或迁移技能

每个激活技能必须位于：

```text
plugins/<plugin>/skills/<skill-name>/SKILL.md
```

技能目录名必须和 frontmatter 里的 `name` 一致。激活技能还需要携带以下元数据字段：

```yaml
metadata:
  owner: jay1803
  family: <plugin>
  maturity: stable
  distribution: <plugin>
```

`family` 和 `distribution` 都等于插件目录名，`npm run check` 会强制校验。

改动之后：

```bash
npm run catalog
npm run check
npm run pack:check
git diff --check
```
