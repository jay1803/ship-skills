# 技能目录

本仓库所有技能的索引：每个技能做什么、什么时候用。技能按领域分组；组内若有
**编排器（orchestrator）**，即为入口——先从它开始，由它路由到更细分的技能。

在 Codex 中用 `$name` 调用，在 Claude Code 中用 `/name` 调用；也可以直接描述任务，
让 agent 根据技能描述自动匹配。

> English version: [`CATALOG.md`](CATALOG.md)

## 快速索引

| 分组 | 技能 |
| --- | --- |
| [PM 工作流](#pm-工作流) | `pm` + 15 个子技能 |
| [Dev 工作流](#dev-工作流) | `dev` + 20 个子技能 |
| [设计](#设计) | `design` + 5 个子技能 |

---

## PM 工作流

产品管理流水线：一个编排器加多个单一职责的子技能。**任何 PM 需求先从 `pm` 开始**。
单个 issue 会自动路由到对应环节；项目 issue 集合则由 `pm-project-orchestrator`
盘点，并通过安全的串行/并行 PM worker waves 推进到开发就绪。

完整流水线阶段顺序和路由逻辑见 [`PM_DEV_WORKFLOW.zh-CN.md`](PM_DEV_WORKFLOW.zh-CN.md)。

## Dev 工作流

工程执行流水线，与 PM 对应。**单个 dev-ready issue 从 `dev` 开始**；多 issue 用
`dev-project-orchestrator`，跨 PR 集成用 `dev-integration-manager`。

完整流水线阶段顺序和路由逻辑见 [`PM_DEV_WORKFLOW.zh-CN.md`](PM_DEV_WORKFLOW.zh-CN.md)。

## 设计

在已批准的产品意图和生产工程之间执行视觉设计。当不确定需要哪个设计产物或阶段时，
**先从 `design` 开始**。

- `design` — 把明确的产品意图路由到方向、探索、原型、系统或评审。
- `design-direction` — 定义具体的视觉语言：字体、色彩、密度、层级、形状、图像与动效。
- `design-explore` — 产出可比较的线框图、视觉方案、组件选项或流程分镜。
- `design-prototype` — 构建并验证带真实状态与反馈的一次性交互原型。
- `design-system` — 提取、创建、精炼并沉淀基础规范、tokens、组件与一致性问题。
- `design-review` — 评审无障碍性、层级、交互状态、系统一致性、响应式和打磨度；默认只汇报问题，只有在被要求时才动手修复。

产品行为和界面需求仍归 `pm-ux-state` 和 `pm-ui-design` 所有；生产实现仍归 `dev`
和各平台技能所有。
