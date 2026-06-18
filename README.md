# Agent Skills Collection

个人积累的 Agent Skills 集合，用于提升 AI Agent 在特定场景下的执行质量。

## Skills 列表

### prd-clarifier

**用途**: 需求澄清

把 PRD、PDF、网页说明、截图、流程图、时序图、表格等混合需求材料，梳理成一份更明确、更严谨、可被 AI 继续消费的 Markdown 规范文档。

**适用场景**:
- 产品给出的是 PRD、飞书文档、网页、PDF、截图混合材料
- 产品给出的是一句话需求或产品想法，需要先引导再澄清
- 需求存在散乱、冲突、缺失或歧义，需要先澄清并结构化

**安装方式**:
```powershell
# Claude Code
Copy-Item -Recurse .\prd-clarifier $env:USERPROFILE\.claude\skills\

# Codex
Copy-Item -Recurse .\prd-clarifier $env:USERPROFILE\.codex\skills\
```

**详细文档**: [prd-clarifier/README.md](prd-clarifier/README.md)

---

### writing-backend-technical-solutions

**用途**: 后端技术方案编写

把"已澄清需求文档 + 当前代码事实"整理成一份可直接进入开发评审的后端详细技术方案。

**适用场景**:
- 用户要求"后端技术方案""后端详细设计""技术方案评审稿"
- 输入包含已澄清需求文档，且需要结合当前代码逻辑输出可评审的完整方案
- 需要流程图、时序图、核心改动、数据存储变更、发布回滚、风险分析

**安装方式**:
```powershell
# Claude Code
Copy-Item -Recurse .\writing-backend-technical-solutions $env:USERPROFILE\.claude\skills\

# Codex
Copy-Item -Recurse .\writing-backend-technical-solutions $env:USERPROFILE\.codex\skills\
```

---

### refactor-module-safely

**用途**: 安全重构指定功能模块

从整体架构和真实执行链路出发，在不改变业务逻辑的前提下重构用户指定模块；若必须变更逻辑，先产出变更前后方案、对比与风险，等待人工审阅后再继续。

**适用场景**:
- 用户要求“重构这个功能模块”“优化代码结构但不改业务逻辑”
- 需要按 Clean Code、设计原则、设计模式、DDD 整理模块职责与结构
- 需要先给出可审阅的重构计划、不确定点和行为变更边界

**安装方式**:
```powershell
# Claude Code
Copy-Item -Recurse .\refactor-module-safely $env:USERPROFILE\.claude\skills\

# Codex
Copy-Item -Recurse .\refactor-module-safely $env:USERPROFILE\.codex\skills\
```

---

### repo-wiki

**用途**: 基于代码库自动生成结构化 Wiki 文档

从代码库中提取关键信息，生成一份覆盖项目架构、模块关系与实现细节的结构化 Wiki 文档。自动检测 BPMN 流程、DDD 分层、策略模式、状态机等场景并生成 Mermaid 图表。

**适用场景**:
- 用户要求"生成 repo wiki""项目文档""代码库概览""architecture doc"
- 用户说"帮我梳理一下这个项目""这个代码库是怎么组织的"
- 需要快速了解一个新项目的架构、模块关系和关键设计决策

**核心特性**:
- 三种输出模式：完整 Wiki / 轻量概览 / 局部 Wiki，按用户意图自动选择
- 证据链原则：每个结论附文件路径或类名作为证据
- 智能画图：自动检测 BPMN/Workflow/Strategy/State/DDD 等模式并生成 Mermaid 图
- 大型项目策略：>500 文件时分批扫描、并行分析、聚焦核心模块

**安装方式**:
```powershell
# Claude Code
Copy-Item -Recurse .\repo-wiki $env:USERPROFILE\.claude\skills\

# Codex
Copy-Item -Recurse .\repo-wiki $env:USERPROFILE\.codex\skills\
```

---

### tob-weekly-review

**用途**: TOB 研发周报与跨仓库复盘

把 git log、PR/MR、需求文档、测试反馈、发布记录和历史周报整理成可复盘的 TOB 研发周报，并形成风险 action 闭环。

**适用场景**:
- 用户要求生成 TOB 周报、研发周报、跨仓库复盘或迭代总结
- 需要从多个仓库梳理业务进展、后端工作、跨模块依赖和发布风险
- 需要回看上周 action，并沉淀下周动作、测试关注点和证据索引

**安装方式**:
```powershell
# Claude Code
Copy-Item -Recurse .\tob-weekly-review $env:USERPROFILE\.claude\skills\

# Codex
Copy-Item -Recurse .\tob-weekly-review $env:USERPROFILE\.codex\skills\
```

---

## 目录结构

```
skills/
├── prd-clarifier/
│   ├── SKILL.md              # Skill 主定义
│   ├── README.md             # 使用说明
│   ├── commands/             # 平台命令适配
│   │   ├── claude/
│   │   └── codex/
│   ├── examples/             # 使用示例
│   ├── evals/                # 评测材料
│   └── references/           # 参考模板
│
├── writing-backend-technical-solutions/
│   ├── SKILL.md              # Skill 主定义
│   ├── test-prompts.json     # 测试用例
│   └── references/           # 参考模板与示例
│
├── refactor-module-safely/
│   ├── SKILL.md              # Skill 主定义
│   ├── test-prompts.json     # 测试用例
│   └── agents/               # 平台适配配置
│
├── repo-wiki/
│   └── SKILL.md              # Skill 主定义
│
├── tob-weekly-review/
│   ├── SKILL.md              # Skill 主定义
│   ├── agents/               # 平台适配配置
│   ├── references/           # 周报模板
│   └── scripts/              # 周报骨架生成脚本
│
└── README.md                 # 本文件
```

## Skill 使用流程

推荐的 Skill 联用流程：

```
原始需求材料 → prd-clarifier → 澄清文档 → writing-backend-technical-solutions → 后端技术方案 → 实现编码

新项目接手 → repo-wiki → 项目架构文档 → 快速理解全貌

TOB 多仓库迭代 → tob-weekly-review → 周报 / 风险 action / 下周计划
```

1. 先用 `prd-clarifier` 把散乱需求整理成结构化文档
2. 再用 `writing-backend-technical-solutions` 结合代码库生成可评审方案
3. 方案评审通过后进入实现编码
4. 接手新项目时用 `repo-wiki` 快速生成项目架构文档
5. 每周用 `tob-weekly-review` 固定沉淀 TOB 研发进展与风险闭环

## 安装全部 Skills

```powershell
# 一键安装到 Claude Code
Copy-Item -Recurse .\prd-clarifier $env:USERPROFILE\.claude\skills\
Copy-Item -Recurse .\writing-backend-technical-solutions $env:USERPROFILE\.claude\skills\
Copy-Item -Recurse .\refactor-module-safely $env:USERPROFILE\.claude\skills\
Copy-Item -Recurse .\repo-wiki $env:USERPROFILE\.claude\skills\
Copy-Item -Recurse .\tob-weekly-review $env:USERPROFILE\.claude\skills\

# 一键安装到 Codex
Copy-Item -Recurse .\prd-clarifier $env:USERPROFILE\.codex\skills\
Copy-Item -Recurse .\writing-backend-technical-solutions $env:USERPROFILE\.codex\skills\
Copy-Item -Recurse .\refactor-module-safely $env:USERPROFILE\.codex\skills\
Copy-Item -Recurse .\repo-wiki $env:USERPROFILE\.codex\skills\
Copy-Item -Recurse .\tob-weekly-review $env:USERPROFILE\.codex\skills\
```

## 版本管理

本仓库用于版本管理和持续迭代 Skills。建议：

- 每次 Skill 更新后提交版本记录
- 重要变更记录在 CHANGELOG
- 评测结果可作为质量参考

## License

MIT
