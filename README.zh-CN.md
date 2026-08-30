# Ship Skills

jay1803 的 PM 到 Dev 交付与设计 agent 技能源码 monorepo。相关技能以带版本号的
Codex 插件形式一起发布，这样一台机器只需安装自己需要的那条生命周期。

> English version: [`README.md`](README.md)

## 仓库结构

```text
ship-skills/
├── plugins/
│   ├── delivery/   # PM 从 intake 到 readiness review，Dev 从 repo context
│   │                 到实现、评审与上线交接
│   └── design/     # 从设计方向到设计评审
├── catalog/        # 自动生成的机器可读清单
├── scripts/        # 安装、目录生成、打包、校验脚本
└── wiki/           # 工作流与目录文档
```

`plugins/` 下的两个目录是发布边界，各自拥有一个 Codex 插件清单和一个 npm 包清单。
新增技能不需要新建仓库或 npm 包：把它放进与其生命周期一致的插件即可。

自动生成的清单是 [`catalog/skills.json`](catalog/skills.json)。人类可读的工作流
文档从 [`wiki/CATALOG.md`](wiki/CATALOG.md) 和
[`wiki/PM_DEV_WORKFLOW.md`](wiki/PM_DEV_WORKFLOW.md) 开始。

## 在 Codex 中安装

首选安装方式是本仓库自带的本地 Codex marketplace：

```bash
codex plugin marketplace add ~/github/ship-skills
codex plugin add delivery@jay1803-ship-skills
codex plugin add design@jay1803-ship-skills
```

插件安装相互独立，一台机器可以只安装自己需要的那一系列。

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

本仓库是一个私有 npm workspace，包含两个可发布的包：

| 包 | 来源 | 用途 |
| --- | --- | --- |
| `@jay1803/ship-skills-delivery` | `plugins/delivery` | PM、Dev、上线交接 |
| `@jay1803/ship-skills-design` | `plugins/design` | 视觉设计工作流 |

npm 用于语义化版本、tarball 内容和注册表分发。Codex 安装通过插件 marketplace 完
成，这样 runtime 才能正确注册清单和技能。发布前：

```bash
npm run check
npm run pack:check
npm publish --workspace @jay1803/ship-skills-delivery
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
  family: delivery
  maturity: stable
  distribution: delivery
```

改动之后：

```bash
npm run catalog
npm run check
npm run pack:check
git diff --check
```
