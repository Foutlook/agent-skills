# Windows test DMS 取证

仅当需求与代码差异分析需要数据库结构、链路或实际数据覆盖证据时读取。目标是让主 Agent 在任意本地项目目录中，通过用户级 DMS MCP 使用 Windows 进程环境中的测试凭证查询对应数据库。

## 全局能力与凭证边界

- 固定使用用户级 `aliyun-dms-mcp-server_test`，它应注册在 `~/.codex/config.toml`，不能依赖项目级 `.codex/config.toml`、自定义子 Agent 或当前工作目录。
- 只允许从 Codex 本地进程环境转发 `SDD_ALIYUN_DMS_TEST_ACCESS_KEY_ID` 和 `SDD_ALIYUN_DMS_TEST_ACCESS_KEY_SECRET`。
- 用户级启动器把这两个变量映射为 DMS 子进程所需的 `ALIBABA_CLOUD_ACCESS_KEY_ID` 和 `ALIBABA_CLOUD_ACCESS_KEY_SECRET`。主 Agent 只能判断 Provider 是否可用，不得读取、打印、复制、持久化或要求用户粘贴凭证值。
- 不读取 `.zstt-kit/.env`、项目 `.env`、数据库用户名和密码，也不依赖 `project-databases.json`、固定工作区路径或 Shell 当前目录。
- 不调用生产 DMS Provider，不把生产环境作为无命中、鉴权失败、目标不唯一或数据不足时的对照或回退。
- Windows 环境变量修改后，已有 Codex 进程可能仍保留旧环境。Provider 因变量缺失而不可用时，最小继续动作为确认变量已设置并完全重启 Codex，不暴露变量值。

Windows 环境变量只解决鉴权；本机仍需具备 `py`、`uvx` 和已注册的用户级 `aliyun-dms-mcp-server_test`。任一运行时不可用时返回精确能力缺口，不改读项目配置，也不声称数据库中没有数据。

## 主 Agent 工作流

1. 从最新适用代码、Mapper/Repository、SQL、Schema 或运行配置中证明目标 schema、表、字段、关联键、租户、状态和时间条件；不能从目录名或需求名称猜数据库。
2. 将需要确认的数据事实收敛为一个 `persistence-state` 查询目标，并固定 `environment=test` 与 `provider=aliyun-dms-mcp-server_test`。
3. 使用 `searchDatabase` 按精确 schema 做收敛发现；对候选使用 `getDatabase`，必要时结合 `listInstances`、`getInstance` 核验实例身份和 `EnvType=test`。
4. 仅在需要时使用 `listTables` 和 `getTableDetailInfo` 核验表、字段及索引。
5. 使用 `executeScript` 执行最小只读 SQL，记录 DatabaseId、Schema、表、筛选条件、时间窗口、脱敏结果和限制。
6. 根据直接数据库事实判断 `支持`、`部分支持`、`不支持` 或 `待补证`；不把 Provider 可用、表存在或零命中单独当作数据支持结论。

同一数据库事实或同一关联关系的发现、元数据与查询保持在当前主 Agent 上下文中，复用已经取得的 DatabaseId、Schema、表和条件，不重复发现。

## 目标库解析

对应数据库必须来自当前需求与代码证据：

1. 优先使用数据访问配置、Mapper SQL、Repository、迁移脚本或 Schema 中已经证明的 schema 名；
2. 用 `searchDatabase` 按精确 schema 搜索并限制页大小；
3. 用 `getDatabase` 核对 SchemaName、DatabaseId、实例别名和状态；需要确认环境时再用 `listInstances` 或 `getInstance`，只接受 `EnvType=test`；
4. 有多个测试候选时，先用代码配置、实例别名或已证明的服务关系消歧；仍不唯一且不同选择会改变结论时，只询问一个目标库选择问题，不猜测；
5. 无法从代码或 DMS 唯一定位目标库时标记 `待补证`，不得借用名称相似的数据库。

## 查询限制

- 只执行单条 `SELECT`、只读 CTE、`SHOW`、`DESC`、`DESCRIBE` 或 `EXPLAIN`；禁止 DML、DDL、锁定读、存储过程、临时对象、文件输出和任何可能改变状态的函数。
- 明细查询必须稳定排序并显式 `LIMIT`，默认最多返回 100 行；优先使用 `COUNT`、分组、空值率、去重数、时间边界和关联缺失数等聚合。
- 只选择判断需求所需的字段。不得返回真实姓名、手机号、证件号、Token、内容正文等敏感数据；需要区分样本时使用不可逆脱敏值或聚合结果。
- `executeScript` 是具备写能力的通用工具，但本场景授权仅覆盖上述只读变体。任何无法明确判定为只读的 SQL 都不得执行。

## 调用输入与证据输出

调用前至少锁定：

- 唯一的 `environment=test` 和 `provider=aliyun-dms-mcp-server_test`；
- 需求 ID、要判定的数据事实及其对变更范围的影响；
- 代码已经证明的仓库、分支/提交、schema、表、字段、关联键、租户、状态和时间条件；
- 允许的元数据工具、只读 SQL 边界、返回行数和敏感字段限制；
- 停止条件：事实得到直接覆盖，或所有有界 test DMS 路径均得到明确缺口。

结果必须包含实际 Provider、test 环境、DatabaseId 或可复核的目标库身份、Schema、表、查询目的、SQL 选择条件、时间窗口、脱敏结果、证据状态和限制。不要输出凭证、连接地址及无关原始载荷。
