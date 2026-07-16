---
name: finishing-with-business-staging
description: Use when implementation is complete and a development branch needs to be finished without forgetting newly created business code. Verifies relevant tests, invokes git-add-new-business-code to stage only qualifying untracked business files, blocks integration while commit-worthy changes remain, then guides merge, push and Pull Request, keep, or confirmed discard. Trigger for requests such as “收尾分支”“检查新增业务代码并完成开发”“完成实现并处理分支”.
---

# Finishing With Business Staging

## 目标

在开发实现完成后，先验证代码，再检查是否遗漏新增业务代码，最后安全处理开发分支。

这里的 `staging` 指 Git 暂存区，不是预发布环境。

必须使用 `git-add-new-business-code` 检查并暂存符合范围的新增业务文件。分支收尾步骤由本技能独立定义。

## 核心约束

- 先获得新的测试证据，再声称实现完成。
- 只通过 `git-add-new-business-code` 暂存未跟踪的新增业务代码；不要使用 `git add .` 或 `git add -A`。
- 不要自动暂存已有文件的修改、删除或重命名。
- 存在应提交但尚未提交的改动时，不要合并、推送或清理工作区。
- 除非用户在当前请求中明确授权，否则不要自动提交或推送。
- 删除分支、丢弃提交或清理工作树前，必须展示影响并取得明确确认。
- 不要删除由宿主工具创建且当前流程不拥有的工作树。

## 工作流程

### 1. 确认仓库和变更范围

运行以下只读命令：

```bash
git status --short
git branch --show-current
git rev-parse --show-toplevel
git rev-parse --git-dir
git rev-parse --git-common-dir
```

如果当前目录不是 Git 仓库，停止并报告正确的仓库路径要求。

区分以下状态：

- 已提交的分支改动
- 已暂存但未提交的改动
- 未暂存的已跟踪文件改动
- 未跟踪文件
- 分离头指针，也就是 detached HEAD

### 2. 运行相关验证

选择项目已有且与本次改动直接相关的测试或构建命令。优先使用项目文档、持续集成配置和现有脚本中已经存在的命令。

完整读取退出码、通过数、失败数和跳过数。验证失败时立即停止，不进入分支处理。

如果无法确定验证命令，明确报告缺少的依据；不要把“没有运行测试”描述为“测试通过”。

### 3. 暂存遗漏的新增业务代码

调用 `git-add-new-business-code`，严格执行它的分类和精确暂存规则：

1. 使用 `git ls-files --others --exclude-standard` 获取未跟踪文件。
2. 只暂存明确属于新增业务代码、测试代码或前端业务代码的文件。
3. 跳过文档、配置、生成文件、资源文件和其他非业务新增。
4. 将无法确定的文件列为待确认项，不要自动暂存。
5. 不提交，不推送。

### 4. 执行集成门禁

重新运行：

```bash
git status --short
```

按以下规则决定是否可以继续：

| 状态 | 处理方式 |
|---|---|
| 存在已暂存改动 | 停止分支集成，列出文件并提示先提交 |
| 存在未暂存的已跟踪文件改动 | 停止分支集成，列出文件并提示处理 |
| 存在待确认的未跟踪文件 | 可以保留分支，但在处理前禁止清理或丢弃工作树 |
| 工作区干净 | 继续选择分支收尾方式 |

例如，新建的 `OrderService.java` 被暂存后，不能直接推送旧提交或合并分支；必须先让用户确认提交范围并完成提交。

### 5. 确认基础分支

优先读取远端默认分支：

```bash
git symbolic-ref refs/remotes/origin/HEAD
```

如果无法确定，再检查 `main`、`master` 和当前分支的合并基础。存在多个合理候选时，向用户确认，不要猜测。

### 6. 提供收尾选项

普通开发分支提供以下四项：

1. 合并到本地基础分支
2. 推送当前分支并创建拉取请求（Pull Request）
3. 保留当前分支，稍后处理
4. 丢弃当前分支和相关工作树

分离头指针只提供以下三项：

1. 创建新分支、推送并创建拉取请求
2. 保持现状，稍后处理
3. 丢弃当前工作

不要在用户选择前执行合并、推送、创建拉取请求或删除操作。

### 7. 执行用户选择

#### 合并到本地

1. 再次确认工作区干净。
2. 切换到基础分支并安全拉取远端更新。
3. 合并开发分支。
4. 在合并结果上重新运行相关验证。
5. 只有合并和验证都成功后，才清理本流程拥有的工作树和分支。

#### 推送并创建拉取请求

1. 推送当前分支并设置远端跟踪关系。
2. 默认创建草稿拉取请求，除非用户明确要求可直接评审。
3. 拉取请求说明必须包含改动、原因、影响和验证结果。
4. 保留当前工作树和分支，便于继续处理评审反馈。

#### 保持现状

报告当前分支、工作树路径和剩余改动，不执行清理。

#### 丢弃

先列出将被永久删除的分支、提交、未提交改动和工作树路径，要求用户输入明确确认。没有确认时不得执行。

## 输出要求

最终报告必须包含：

- 验证命令及结果
- 新增业务文件的暂存结果
- 被跳过或待确认的文件
- 当前分支和基础分支
- 用户选择及实际执行结果
- 是否保留或清理工作树
