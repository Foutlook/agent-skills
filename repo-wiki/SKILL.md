---
name: repo-wiki
description: |
  Use when the user asks for a repo wiki, project documentation, codebase overview, architecture doc,
  module documentation, project structure explanation, or asks how a repository is organized.
  Also use for Chinese prompts such as "生成项目文档"、"生成 repo wiki"、"项目架构"、
  "模块文档"、"代码库概览"、"帮我梳理一下这个项目"、"这个代码库是怎么组织的"。
---

# Repo Wiki Generator

从代码库中提取关键信息，生成一份结构化的 Wiki 文档，让任何开发者（包括未来的自己）能快速理解项目的全貌。

## 核心理念

好的 Wiki 不是把代码抄一遍，而是回答三个问题：
1. **这个项目是什么？** — 使命、技术栈、构建方式
2. **它是怎么组织的？** — 模块划分、数据流、关键决策
3. **我该怎么上手？** — 开发流程、约定、常见陷阱

## 先判断输出模式

不要把所有请求都升级为写入完整 Wiki。先根据用户措辞选择模式：

| 用户意图 | 输出模式 | 写文件 |
|---|---|---|
| "生成 repo wiki"、"生成项目文档"、"写到 docs" | 完整 Wiki | 是，默认 `docs/REPO-WIKI.md` |
| "梳理一下"、"介绍项目结构"、"代码库概览" | 轻量概览 | 否，先在对话中输出；用户确认后再落文档 |
| "只看某模块"、"模块文档"、指定目录/包名 | 局部 Wiki | 只写用户指定范围的文档，或先输出草稿 |

写入文件前必须确认目标路径和覆盖策略：
- 如果 `docs/REPO-WIKI.md` 已存在，先说明将更新它，并避免静默覆盖重要内容。
- 如果用户没有明确要求写文件，优先输出对话版概览。
- 如果信息不足，不要编造；用"待补充"标注，并说明缺少哪类证据。

## 输出格式

生成 `docs/REPO-WIKI.md`，包含以下章节（按需裁剪，不是每个项目都需要全部）：

```markdown
# [项目名] Wiki

## 1. 项目概述
## 2. 技术栈
## 3. 构建与运行
## 4. 项目结构
## 5. 模块详解
## 6. 架构设计
## 7. 数据模型
## 8. API 接口
## 9. 配置说明
## 10. 开发约定
## 11. 常见问题
## 12. 证据索引
```

## 执行流程

### Phase 1: 项目探测

快速识别项目类型和规模，决定后续分析策略。

1. **识别语言和框架**
   - 检查根目录的构建文件：`pom.xml`（Java/Maven）、`package.json`（Node）、`build.gradle`（Gradle）、`Cargo.toml`（Rust）、`go.mod`（Go）、`requirements.txt`/`pyproject.toml`（Python）
   - 读取构建文件中的依赖和插件，提取框架信息

2. **识别项目规模**
   - 统计源文件数量和目录深度
   - 判断是单模块还是多模块项目

3. **读取现有文档**
   - 检查 `README.md`、`CLAUDE.md`、`docs/` 目录
   - 提取已有信息，避免重复劳动

**建议命令：**
```bash
rg --files -g '!**/target/**' -g '!**/node_modules/**' -g '!**/dist/**' -g '!**/build/**' -g '!**/generated/**' -g '!**/.git/**'
rg --files -g 'pom.xml' -g 'package.json' -g 'build.gradle' -g 'go.mod' -g 'Cargo.toml' -g 'pyproject.toml'
```

### Phase 2: 结构扫描

优先使用 `rg --files` 和 `rg` 系统性地探索代码库；如果当前环境没有 ripgrep，Claude Code 可退回使用 Glob/Grep 工具。扫描时排除生成物、依赖目录和构建产物，避免把机器生成代码当成业务结构。

**默认排除：**
`target/`、`build/`、`dist/`、`node_modules/`、`.git/`、`.idea/`、`.vscode/`、`generated/`、`gen/`、`coverage/`、`logs/`

**目录结构映射：**
```
rg --files -g '*.java' -g '*.py' -g '*.ts'（根据语言选择）
rg --files -g 'pom.xml' -g 'build.gradle'（多模块项目）
rg --files -g '*.yml' -g '*.yaml' -g '*.properties' -g '*.json'（配置文件）
```

**关键模式搜索：**
```
rg "@SpringBootApplication|@Module|def main|func main"（入口点）
rg "@RestController|@Controller|@RequestMapping|@app\.route"（API 端点）
rg "@Entity|@Table|@Document|class .*Model"（数据模型）
rg "@Service|@Component|@Repository"（服务层）
rg "@Configuration|@Bean"（配置类）
rg "interface .*Service|interface .*Repository"（接口定义）
```

### Phase 3: 深度分析

对识别出的关键文件进行详细阅读。

**分析顺序（按依赖关系从外到内）：**

1. **入口层** — 启动类、主配置、路由定义
2. **接口层** — Controller、Facade、API 定义
3. **服务层** — 业务逻辑、编排器、策略模式
4. **领域层** — 实体、值对象、领域事件
5. **基础设施层** — 数据库访问、外部集成、消息队列

**对于每个模块，提取：**
- 职责描述（一句话）
- 核心类列表及其角色
- 对外暴露的接口
- 依赖的其他模块
- 关键设计模式

### Phase 4: 文档生成

将分析结果组织成结构化 Wiki。

**写作原则：**
- 用简短的表格代替大段文字，每个重要表格加"证据"列（文件路径或类名）
- 包含实际的文件路径和类名，不要泛泛而谈
- 标注关键设计决策和"为什么这样做"
- 记录已知的陷阱和注意事项
- 精简为王：能用一行表格说清的不要写成段落，目标信息密度 > 文字量

**画图原则：**
扫描阶段检测以下模式，命中则必须画图（Mermaid 优先，ASCII 备选）：

| 检测信号 | 图表类型 | Mermaid 语法 | 示例 |
|----------|----------|-------------|------|
| `.bpmn` 文件存在 | BPMN 流程图 | `graph TD` + 菱形判断节点 | 前测流程、课时流程 |
| `Workflow` 接口 + 多个实现 | 工作流状态图 | `graph TD` 展示状态流转 | Z 值状态机 |
| `Strategy` 接口 + 多个实现 | 策略分支表 | 表格（非图）| Z 值策略 |
| `State` 枚举含状态转换逻辑 | 状态机图 | `stateDiagram-v2` | 学习状态机 |
| 3+ 模块间有调用关系 | 模块依赖图 | `graph LR` 箭头 | 模块依赖简图 |
| DDD 分层（Controller/Service/Domain/Infra） | 分层架构图 | `graph TD` 分层框 | tob-learning 架构 |
| 外部系统集成 3+ 个 | 系统上下文图 | `graph LR` 中心节点 | 外部系统集成 |
| 复杂请求处理链路（5+ 步骤） | 数据流图 | `graph TD` 线性链路 | 答题处理流程 |

**检测命令：**
```bash
# BPMN 文件
find . -name "*.bpmn" -not -path "*/target/*"

# Workflow/Strategy 模式
rg "interface.*Workflow|interface.*Strategy" --type java

# State 枚举
rg "enum.*State" --type java

# DDD 分层
rg "@RestController|@Service|@Repository|@Component" --type java -l | head -20
```

**不画图的场景（避免过度图表化）：**
- 简单 MVC（Controller → Service → Mapper）：用一行表格
- 单一职责的小模块：合并到"其他模块"表格
- 纯数据 CRUD：不需要流程图

**证据链原则：**
- 技术栈表：每行附证据列（`pom.xml`、`bootstrap.properties`、`@注解`）
- 模块表：附 Java 文件数（用 `find ... | wc -l` 统计）
- 核心类表：附文件路径
- 实体表：附对应的 SQL 脚本路径
- 架构结论：附启动类、配置文件、关键接口路径

**各章节指导：**

#### 1. 项目概述
- 一句话描述项目使命（从构建文件 description 或 README 提取）
- 核心业务链路图（ASCII，展示请求从入口到数据层的完整路径）
- 目标用户/使用场景

#### 2. 技术栈
带证据列的表格，版本从构建文件 `<properties>` 提取：

| 类别 | 技术 | 版本 | 用途 | 证据 |
|------|------|------|------|------|
| 语言 | Java | 8 | 主开发语言 | `pom.xml` java.version |
| 框架 | Spring Boot | 2.5.15 | Web 框架 | `pom.xml` spring-boot.version |
| ... | ... | ... | ... | ... |

#### 3. 构建与运行
列出实际可用的命令（从构建文件提取，不要猜测）。
如果有文档生成插件（如 smart-doc、Javadoc），说明如何跳过以加速本地验证。

#### 4. 项目结构
带文件数的模块表 + 树形目录 + 模块依赖简图：

| 模块 | 文件数 | 职责 | 证据 |
|------|--------|------|------|
| module-a | 123 | 主入口 | `JzxApplication.java` |
| ... | ... | ... | ... |

模块依赖可用 Mermaid 图或 ASCII 箭头图展示。

#### 5. 模块详解
**核心模块（有复杂业务逻辑的）** 独立章节，包含：
- **职责**：一句话
- **架构模式**：DDD / 策略模式 / 工作流等
- **架构图**：按"画图原则"检测信号，命中则画 Mermaid 图（分层架构、BPMN 流程、状态机、数据流等）
- **核心类**：表格（类名 | 角色 | 文件路径）
- **设计模式详情**：如策略分支表、Agent 角色表（含降级策略）
- **核心实体**：实体→表名映射表

**简单模块** 合并到"其他模块"表格，一行一个模块。

#### 6. 架构设计
- **分层架构图**：用 Mermaid 或 ASCII 框图（接口层→应用服务层→领域层→基础设施层→数据层）
- **RPC 暴露模式**：展示接口定义→实现→调用的三方关系
- **外部系统集成**：表格（外部系统 | 集成方式 | 用途）
- **关键设计决策**：为什么选择这个架构

#### 7. 数据模型
- 核心实体→表名映射表（不需要列出所有字段）
- 实体间关系（ASCII 图，1:N 等）
- 特殊字段说明（如 JSON 格式、时间字段类型差异）
- SQL 脚本位置（证据）

#### 8. API 接口
按模块分组的端点表（路径 | 方法 | 描述）。
核心模块列出具体端点，简单模块只列路径前缀。

#### 9. 配置说明
- 配置文件列表（文件 | 用途）
- 关键运行配置表（配置项 | 值）
- 配置域概览（Nacos、Dubbo、DB、Redis、MQ 等）

#### 10. 开发约定
从 CLAUDE.md、AGENTS.md、.editorconfig 等提取，表格格式（约定 | 内容 | 证据来源）。

#### 11. 常见问题
从代码注释、README、CLAUDE.md 中提取已知陷阱，附代码示例。

#### 12. 证据索引
新增章节：将全文引用的关键文件汇总为一张速查表（主题 | 文件路径），方便快速定位。

### Phase 5: 验证与完善

生成后进行自检：

1. **完整性检查** — 每个模块是否都有记录？关键流程是否都有描述？
2. **准确性检查** — 文件路径是否正确？版本号是否匹配？
3. **可读性检查** — 新人能否看懂？是否有未解释的术语？
4. **一致性检查** — 各章节信息是否矛盾？

## 处理不同项目类型

### Java/Spring Boot 多模块项目
- 重点分析 Maven/Gradle 模块依赖
- 关注 Dubbo/RPC 接口定义
- 提取 MyBatis Mapper 和 SQL
- 识别 Spring Bean 注入关系

### Node.js/TypeScript 项目
- 分析 package.json 的 scripts 和 dependencies
- 识别 Express/Koa/Nest 等框架
- 关注中间件链和路由组织

### Python 项目
- 分析 requirements.txt/pyproject.toml
- 识别 Django/Flask/FastAPI 框架
- 关注装饰器模式的路由定义

### Go 项目
- 分析 go.mod 依赖
- 识别 Gin/Echo 等框架
- 关注接口定义和实现分离

## 大型项目策略

当代码库规模较大（>500 个源文件）时：

1. **分批扫描** — 按模块分批处理，避免上下文溢出
2. **并行分析** — 使用 Agent 工具并行分析独立模块
3. **渐进生成** — 先生成框架，再填充细节
4. **聚焦核心** — 优先分析业务核心模块，基础设施模块可以简化

大型仓库不要一口气深读所有文件。优先级如下：
1. 根构建文件和模块构建文件
2. 启动类、路由/Controller、公开 API/Facade
3. 核心 Service、Domain、Mapper/Repository
4. 配置文件和 README/docs 中提到的关键流程
5. 测试用例中覆盖的主流程

如果源文件超过 2000 个，先生成目录级概览和核心模块清单，再询问用户是否继续深挖所有模块。

## 输出示例

生成的 Wiki 应该像这样简洁、有证据、有图：

```markdown
### 5.3 jzx-tob-learning（学习核心 · DDD）

**职责：** 基于 Z 值驱动自适应学习，协调 AI Agent 判定、策略决策和状态机流转。

**分层架构（检测信号：DDD 分层 → 画图）：**
```
Controller 层
├── LearningController      /tob/learning（start/answer/voice/choice）
├── SituationController     /tob/situation（推荐/ZPD）
└── LearningPropController  /tob/prop（道具）

应用服务层
├── LearningOrchestratorServiceImpl  核心编排器
└── ZpdCalculateServiceImpl          ZPD 掌握度计算

领域层
├── ZValueStrategy（接口 + 4 实现）   Z 值策略
├── Workflow（接口 + 6 实现）         状态驱动工作流
└── AgentCoordinator                  Agent 调用协调（超时降级）

基础设施层
├── 12 个 Repository、10 个 Mapper
└── 5 个 DubboService Facade、2 个 MQ Consumer
```

**Z 值策略（检测信号：Strategy 接口+多实现 → 策略分支表）：**

| Z 值 | 答对 | 答错 |
|------|------|------|
| null | Z→1，思路验证 | Z→0，错误归因 |
| 0 | 保持，思路验证 | 保持，推荐讲解 |
| 1 | Z→2，下一题 | 保持，错误归因 |
| 2 | Z→3，通关 | 保持，错误归因 |

**5 个 AI Agent（证据：`AgentCoordinator.java`）：**

| Agent | 角色 | 降级策略 |
|-------|------|----------|
| B | 语义判官 | 失败返回 Ambiguous |
| F | 归因判官 | 失败返回 Invalid |
```

```markdown
### 5.4 jzx-activiti（自适应学习引擎）

**前测流程（检测信号：`.bpmn` 文件存在 → 画 BPMN 流程图）：**

​```mermaid
graph TD
    A([开始]) --> B[开始前测]
    B --> C[选择登陆岛屿]
    C --> D[选择登岛PT]
    D --> E[取题] --> F[生成答题记录]
    F --> G{用户操作}
    G -->|SUBMIT| H[掌握度更新]
    G -->|CONTINUE| I[学情刷新]
    H --> J{题量>阈值?}
    J -->|否| K[岛内切换PT]
    J -->|是| L[结束前测]
    K --> M{可用PT?}
    M -->|是| E
    M -->|否| N[切换岛屿]
    N --> O{可用岛屿?}
    O -->|是| D
    O -->|否| L
    I --> P{切换PT?}
    P -->|是| K
    P -->|否| G
​```
```

## 注意事项

- **不要编造信息** — 只写从代码中实际读到的内容。如果某个章节信息不足，标注"待补充"
- **保持最新** — 提醒用户代码变更后需要重新生成
- **尊重现有文档** — 如果 README 或 CLAUDE.md 已有相关内容，引用而非重复
- **路径要准确** — 所有文件路径必须是实际存在的
- **版本号要准确** — 从构建文件中读取，不要使用默认值
- **区分概览和文档写入** — 用户只想了解项目时，不要擅自创建或覆盖文件
- **保留证据链** — 关键架构、模块职责、API 结论应能追溯到代码路径、构建文件或现有文档
- **遵守仓库约定** — 如果项目有 AGENTS.md、CLAUDE.md、README 或编码规范，生成 Wiki 时优先遵守其中的语言、编码、路径和提交流程要求
