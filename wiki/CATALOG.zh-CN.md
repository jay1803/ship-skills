# 技能目录

本仓库所有技能的索引：每个技能做什么、什么时候用。技能按插件分组，插件同时也是安
装和发布的边界。组内若有 **编排器（orchestrator）**，即为入口——先从它开始，由它
路由到更细分的技能。

在 Codex 中用 `$name` 调用，在 Claude Code 中用 `/plugin:name` 调用；也可以直接描
述任务，让 agent 根据技能描述自动匹配。

> English version: [`CATALOG.md`](CATALOG.md)

## 快速索引

| 插件 | 技能数 | 入口 |
| --- | --- | --- |
| [产品](#产品) | 14 | `issue-router`，之后 `pm` |
| [开发](#开发) | 16 | `dev` |
| [评审](#评审) | 6 | `review` |
| [DevOps](#devops) | 3 | `repo-initialize` 或 `release` |
| [设计](#设计) | 6 | `design` |
| [项目](#项目) | 8 | `project` |
| [研究](#研究) | 16 | `research` |

---

## 产品

把一个需求收敛成确认过、可开发的产品范围。当还不确定该走哪条工作流时，
**先从 `issue-router` 开始**：它在任何 PM、Dev、排查、验证或发布动作之前，选出唯
一一条只读路由。已经确定是单个 issue 的产品工作时，**从 `pm` 开始**。

- `issue-router` — 在 PM、Dev、排查、验证或发布之前，为绑定的 issue 或项目选出唯一一条只读工作流路由。
- `pm` — 把一个产品 issue 推进到开发就绪：受理、补齐缺失决策、形成规范描述、完成经过验证的 Dev 交接。
- `pm-strategy` — 在项目立项之前，梳理产品方向、路线图优先级和有证据支撑的投入建议。
- `pm-scope` — 厘清用户问题、期望结果和最小可行范围，明确非目标与取舍。
- `pm-spec` — 把确认的范围或已诊断的缺陷，收敛成简洁的 PRD 或规范的 issue 标题与描述。
- `pm-solution-review` — 在不改变目标的前提下，审视已确认方案中不必要的复杂度和缺乏依据的规则。
- `pm-readiness-review` — 判断一个 issue 是否具备足够的范围和验收证据可以开工，并给出 Dev 交接结论。
- `pm-backlog` — 从稳定的产品范围中拆出可独立交付的 issue 切片及其依赖。
- `pm-bug-triage` — 在工程诊断之前，厘清预期与实际行为、影响面、严重度和可执行的证据。
- `pm-data-analytics` — 设计功能成功指标、事件语义和符合隐私要求的度量方案。
- `pm-project-orchestrator` — 组织一个项目或协调多个相关 issue 的 PM 就绪度，包含伞形 issue 的拆解。
- `pm-project-status` — 读取当前项目与路线图状态、里程碑健康度和交付证据。
- `pm-pr-product-review` — 对照确认过的需求和验收标准检查已实现的 PR，只评估符合度，不动手修复。
- `pm-release-learning` — 撰写有证据支撑的 release notes，或从已上线变更与反馈中总结产品收获。

## 开发

从可开发的 issue 交付到合并的 PR。单个 issue **从 `dev` 开始**；依赖波次或指定合
并顺序用 `dev-project-orchestrator`；跨 PR 的统一检查点用 `dev-integration-manager`。

- `dev` — 把一个可编码的 issue 交付完成，覆盖 PR、评审、CI、合并和测试交接。
- `dev-project-orchestrator` — 以依赖波次或指定合并顺序，规划或执行多个可开发 issue。
- `dev-integration-manager` — 当合并顺序、跨分支契约、冲突或联合验证需要统一检查点时，协调一组明确的 PR 或分支。
- `agent-routing` — 在派发或升级受托 controller、worker 或有界 agent 时，选择执行器与运行时绑定。
- `dev-git-setup` — 准备或校正 issue 分支与独立 worktree，保留既有 checkout 并核对集成基线。
- `dev-planner` — 设计已批准的工程工作，划定任务边界，产出可直接实现的工单方案。
- `dev-spike` — 在架构决策之前，调查尚未解决的技术可行性或相互竞争的实现路径。
- `dev-api-research` — 当外部行为需要澄清时，调研第三方 API/SDK 的能力与集成契约。
- `dev-api-steward` — 当实现可能改变 API 行为或兼容性时，维护自有后端/API 契约和面向调用方的文档。
- `dev-implementer` — 实现已批准的变更、修复 PR 评审意见或冲突，保持职责边界与验证证据。
- `dev-debugger` — 诊断观察到的缺陷、回归、崩溃或无法解释的测试失败，在修复前给出有证据的根因结论。
- `dev-test` — 按选定的 Dev 模式执行实现后验证，并在准备 PR 前对失败分类。
- `dev-ci-repair` — 修复 `dev-test` 上报的红色 PR 检查或反复出现的 CI/环境故障。
- `dev-verifier` — 用新鲜的测试、运行时证据、验收标准和确切的 revision 核查完成声明。
- `dev-pr-writer` — 从已实现的工作准备、推送并创建或复用 GitHub PR，附带验证证据。
- `dev-merge-handoff` — 把一个 issue PR 合并进确定的集成基线，完成清理与测试 revision 交接。

## 评审

对冻结目标的独立评审。**从 `review` 开始**：它让各个视角相互隔离地执行，避免彼此
污染，最后再合并结论。

- `review` — 编排对 GitHub PR 或指定 base/head diff 的规格、正确性与可维护性独立评审。
- `review-spec` — 把冻结的实现与其应遵循的需求对照，检查规格符合度。
- `review-correctness` — 在 PR 或指定 base/head diff 中找出有证据支撑的行为缺陷与回归。
- `review-code-quality` — 审视实质性的可维护性代价与有边界的简化空间，把结论返回给调用方。
- `review-judge` — 在各评审完成后，校验并合并针对同一冻结目标的隔离评审产物。
- `review-pr` — 从生产代码结构与可维护性角度评审 GitHub PR，按需给出行内评论。

## DevOps

仓库初始化与生产发布。这些技能掌管对授权敏感的操作，与 issue 交付保持分离。

- `repo-initialize` — 依据模板初始化或更新仓库的 `AGENTS.md` 和可选的 `.agents` 策略，同时保留项目自有规则。
- `release` — 按仓库策略编排生产发布：晋级、打 tag、可选部署和 GitHub Release。
- `deploy-skill-creator` — 把某个项目经过验证的部署与校验流程，沉淀为仓库本地的部署技能。

## 设计

在已批准的产品意图和生产工程之间执行视觉设计。当不确定需要哪个产物或阶段时，
**先从 `design` 开始**。

- `design` — 从明确的产品意图出发设计用户流程、交互状态与界面规格，或路由到更细分的设计技能。
- `design-direction` — 为已批准的产品简报或界面确定具体的视觉方向。
- `design-explore` — 为已批准的界面、组件或流程探索可相互比较的视觉方案。
- `design-prototype` — 依据已批准的流程与界面规格，构建并验证一次性交互原型。
- `design-system` — 提取、创建、精炼并沉淀可复用的设计系统基础规范与组件。
- `design-review` — 评审设计产物、原型、设计系统定义或已实现界面的视觉质量与一致性。

产品范围和验收标准归产品插件，生产实现归开发插件。

## 项目

从利益相关方提案到项目收尾的项目文档。**从 `project` 开始**准备或续接一条文档工
作流。这里关注的是项目沟通与生命周期状态，而不是 issue 拆解。

- `project` — 维护从提案、kickoff、进展更新到收尾的项目文档。
- `proj-sources` — 在已连接的工作区工具中查找并盘点项目相关来源，明确覆盖范围与访问缺口。
- `proj-context` — 从既有文档和相关来源构建或刷新项目上手上下文包。
- `proj-proposal` — 撰写或打磨面向利益相关方的项目提案，包含简短的 go/no-go 判断。
- `proj-kickoff` — 把已批准的提案转化为 kickoff 材料和可复用的项目入口页。
- `proj-update` — 收集项目进展，校正入口页或计划，并起草面向利益相关方的更新。
- `proj-review` — 从决策质量、证据和一致性角度评审提案、kickoff、更新或收尾文档。
- `proj-closeout` — 对照批准的目标和实际交付证据，准备完成评审、交接与复盘。

## 研究

把开放问题转化为可决策的证据。**从 `research` 开始**：它负责界定问题并路由到合适
的方法；子技能是同一套证据程序的不同阶段，而不是各自独立的报告生成器。

- `research` — 面向开放、战略、诊断、预测、探索、设计与评估类问题的决策研究编排器。
- `research-question-framing` — 把含糊或过载的研究请求收敛成一份当前有效的研究契约。
- `research-decision-model` — 明确建模这个问题最终将依据什么来判断。
- `research-hypothesis-map` — 构建一组相互竞争、可证伪的解释或「必须为真」的命题。
- `research-evidence-plan` — 把研究契约、决策模型和假设图转化为有优先级的证据计划。
- `research-desk` — 为一个有界问题收集并组织当前的外部、文献、学术、官方或指定来源证据。
- `research-market-landscape` — 描绘市场、品类、生态、渠道或技术版图中与决策相关的结构。
- `research-competitive` — 调查并比较争夺同一用户、买家、预算、工作流或结果的替代方案。
- `research-user-study` — 设计与决策相关的用户、客户、干系人、操作者或专家研究。
- `research-user-synthesis` — 把真实的定性与问卷证据综合成与决策相关的发现。
- `research-data-analysis` — 针对与决策相关的问题，分析提供的或已连接的定量数据。
- `research-experiment-design` — 设计可信且投入相称的实验、试点或准实验测量方案。
- `research-causal-analysis` — 判断现有证据是否支持某个因果解释或可归因的效应。
- `research-forecasting` — 为可裁定的未来目标给出校准过的预测，含驱动因素、情景和更新信号。
- `research-synthesis` — 把已接受的研究状态与证据台账综合成可追溯、已校准的决策简报草稿。
- `research-review` — 在决策前独立评审冻结的研究状态、证据台账与决策简报。
