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
└── README.md                 # 本文件
```

## Skill 使用流程

推荐的 Skill 联用流程：

```
原始需求材料 → prd-clarifier → 澄清文档 → writing-backend-technical-solutions → 后端技术方案 → 实现编码
```

1. 先用 `prd-clarifier` 把散乱需求整理成结构化文档
2. 再用 `writing-backend-technical-solutions` 结合代码库生成可评审方案
3. 方案评审通过后进入实现编码

## 安装全部 Skills

```powershell
# 一键安装到 Claude Code
Copy-Item -Recurse .\prd-clarifier $env:USERPROFILE\.claude\skills\
Copy-Item -Recurse .\writing-backend-technical-solutions $env:USERPROFILE\.claude\skills\

# 一键安装到 Codex
Copy-Item -Recurse .\prd-clarifier $env:USERPROFILE\.codex\skills\
Copy-Item -Recurse .\writing-backend-technical-solutions $env:USERPROFILE\.codex\skills\
```

## 版本管理

本仓库用于版本管理和持续迭代 Skills。建议：

- 每次 Skill 更新后提交版本记录
- 重要变更记录在 CHANGELOG
- 评测结果可作为质量参考

## License

MIT