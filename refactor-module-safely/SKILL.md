---
name: refactor-module-safely
description: Use this skill whenever the user asks Codex to refactor, reorganize, modularize, simplify, decouple, clean up, or improve a specific code module, feature module, service, controller, domain flow, or architecture area while preserving business behavior. This skill is especially important for requests like "重构这个功能模块", "优化代码结构但不改业务逻辑", "按 Clean Code/DDD/设计模式重构", "拆分这个 service", "整理架构", or any refactor where user review is required before changing behavior.
---

# Refactor Module Safely

## Purpose

Guide behavior-preserving refactors from the module architecture downward. The goal is to reduce real maintenance cost without changing business logic unless the user explicitly approves a reviewed behavior change.

Use Clean Code, design principles, design patterns, and DDD as tools, not decoration. Every change must pay for itself with a concrete reason: lower coupling, clearer responsibility, reduced duplication, safer tests, easier extension for known needs, or removal of misleading structure.

## Operating Rules

- Start with the user-identified module and its actual execution paths. Do not refactor adjacent areas just because they look imperfect.
- Preserve existing business behavior by default. Treat observable behavior, persistence effects, external calls, events, logs relied on by operations, authorization checks, validation rules, and error semantics as behavior.
- If a behavior change appears necessary, stop before implementation and present a change proposal for review.
- If the user says "直接改" or asks not to wait, continue only for behavior-preserving structural work. Still stop for any possible behavior change, data result change, authorization/validation change, persistence change, external-call change, or compatibility risk.
- Avoid speculative architecture. Use foreseeable requirements the user provided or that are clearly visible in code. Do not build generic frameworks, abstract factories, plug-in systems, or broad DDD layers without evidence they solve current complexity.
- Do not refactor for taste alone. If a change cannot be justified against the current module's pain or risk, leave it out.
- Preserve unrelated comments. Update or add comments only where changed non-trivial logic needs the business rule, boundary, trigger condition, or data source explained.
- Respect project-specific coding rules, including method-call layout, encoding, testing, and data-fetching performance constraints.

## Required Workflow

### 1. Understand The Module Boundary

Before proposing changes, identify:

- The user-requested feature/module boundary.
- Public entry points: controllers, handlers, jobs, listeners, commands, scheduled tasks, API endpoints, or UI routes.
- Internal collaborators: services, repositories, domain objects, mappers, clients, caches, events, and configuration.
- Data sources and side effects: database tables, RPC/external APIs, messages, files, transactions, locks, and metrics.
- Runtime facts and propagation channels: Redis/cache state, delayed timers, dedupe keys, distributed locks, in-memory state, MQ messages, WebSocket pushes, after-commit callbacks, and scheduled jobs.
- Existing tests and missing test coverage for the behavior being preserved.

Prefer code evidence over naming assumptions. A guard clause, null check, or field presence is not automatically a true business dependency; trace the final fetch/calculation point and the concrete parameters used there.

### 2. Build A Behavior Baseline

Create a short baseline before designing the refactor:

- Current responsibilities and where they are mixed.
- Current behavior contract, including important edge cases.
- Current data flow from entry point to final persistence/fetch/calculation.
- Current fact ownership: distinguish real-time runtime state, persisted records, derived response DTOs, and outbound notifications. Do not collapse them into one vague "data source" when they have different consistency or lifecycle rules.
- Current risks: duplication, N+1 calls, hidden side effects, transaction ambiguity, unclear naming, misplaced domain rules, brittle conditionals, or difficult tests.
- Verification options: existing tests, focused new tests, golden-master tests, request/response examples, logs, or manual checks.

For code changes, prefer adding focused characterization tests before refactoring when existing coverage is weak and the behavior is observable.

### 3. Decide The Review Path

Choose one of these paths before editing:

- **Fast path**: Use only for tiny, local, behavior-preserving cleanup where all conditions are true: one narrow area, no public contract change, no data/query/remote-call change, no authorization or validation change, no transaction or error semantic change, and verification is straightforward. State the scope, reason, behavior-preservation basis, and verification before editing; user pre-approval is not required unless project instructions require it.
- **Plan review path**: Use for substantial module refactors, multi-file moves, responsibility splits, new abstractions, DDD boundary changes, test strategy changes, or anything the user explicitly asked to review first. Present the refactor plan and wait for approval.
- **Behavior-change path**: Use when any result, side effect, validation, compatibility, persistence, external call, or error behavior may change. Present the business logic change proposal and wait for explicit approval.

When unsure, choose the plan review path. If the uncertainty is about behavior, choose the behavior-change path.

### 4. Produce A Refactor Plan For User Review

Do not implement substantial refactors before presenting a plan and receiving approval. The plan should be specific enough for the user to reject risky parts.

Use this structure:

```markdown
## 重构计划

### 目标
- [What the refactor will improve]

### 当前证据链
- 入口: [entry points]
- 真实调用链: [main downstream calls]
- 最终数据源/计算点: [fetch/calculation/persistence points]
- 实际影响结果的参数: [parameters]
- 守卫条件 vs 真实业务依赖: [distinction]

### 拟修改范围
- [files/classes/functions]

### 不修改范围
- [explicitly excluded areas]

### 重构步骤
1. [small, reviewable step]
2. [small, reviewable step]

### 每一步的理由
- [change]: [why this is needed, not just style]

### 业务逻辑影响
- 默认结论: 不改变业务逻辑
- 依据: [why behavior is expected to remain equivalent]

### 验证方式
- [tests/commands/manual checks]

### 无法确定点
- [questions the user must confirm before implementation]
```

If the task is tiny, keep the plan concise, but still include scope, reason, behavior impact, verification, and uncertain points.

Example of the expected level of specificity:

```markdown
## 重构计划

### 目标
- 将订单结算 Service 中的参数校验、价格汇总、优惠分摊拆成可命名的内部步骤，降低单方法复杂度。

### 当前证据链
- 入口: OrderSettlementController#settle
- 真实调用链: controller -> OrderSettlementService#settle -> priceMapper.batchQuery -> couponClient.batchGet
- 最终数据源/计算点: priceMapper.batchQuery 返回商品价格；settle 方法内完成优惠分摊计算
- 实际影响结果的参数: orderItemList、couponIdList、memberLevel
- 守卫条件 vs 真实业务依赖: request.storeId 只用于入口非空校验，当前结算计算未使用它参与价格或优惠计算

### 拟修改范围
- OrderSettlementService 内部私有方法拆分
- 补充当前结算结果的 characterization test

### 不修改范围
- Controller 接口、DTO 字段、Mapper SQL、couponClient 协议

### 重构步骤
1. 用现有输入输出补一组结算结果保护测试
2. 提取 validateSettlementRequest、loadPriceContext、calculateDiscountAllocation
3. 将批量查询结果显式映射为 priceBySkuId，避免后续拆分时引入循环查询

### 每一步的理由
- 保护测试: 先锁定当前业务行为，避免把计算差异误当成重构
- 私有方法拆分: 每个方法对应一个业务阶段，降低主流程阅读成本
- priceBySkuId: 保持批量读取边界清晰，防止 N+1 回退

### 业务逻辑影响
- 默认结论: 不改变业务逻辑
- 依据: 不改入口参数、SQL、远程调用、优惠公式和错误类型，只调整内部组织方式

### 验证方式
- 运行 OrderSettlementServiceTest
- 如有集成测试，运行订单结算相关测试集

### 无法确定点
- storeId 非空校验是否是历史遗留限制，还是上游依赖的接口契约？如需要删除，必须单独走业务逻辑变更提案。
```

### 5. Behavior Change Gate

If any required change may alter business logic, do not hide it inside "refactor". Present it separately and wait for user approval.

Use this structure:

```markdown
## 业务逻辑变更提案

### 为什么单纯重构不够
- [evidence]

### 变更前方案
- 行为: [current behavior]
- 优点: [current benefits]
- 问题: [current risks or limitations]

### 变更后方案
- 行为: [new behavior]
- 优点: [benefits]
- 代价: [costs]

### 对比
- 数据结果: [same/different]
- 兼容性: [impact]
- 性能: [impact]
- 上下游影响: [impact]
- 测试影响: [needed changes]

### 风险
- [risk and mitigation]

### 需要你确认
- 是否允许该业务逻辑变更？
```

Only implement the behavior-changing part after explicit approval. If the user rejects it, continue with the behavior-preserving subset.

### 6. Execute In Small Closed Loops

After approval:

- Make small, cohesive edits that map to the reviewed plan.
- Prefer improving names, extracting cohesive functions/classes, moving rules to clearer owners, reducing duplication, and clarifying boundaries over adding abstractions.
- Use design patterns only when the code already has pattern-shaped pressure:
  - Strategy: multiple interchangeable algorithms or policy variants.
  - Template Method: stable skeleton with variable steps.
  - Factory: object creation rules are complex or repeated.
  - Adapter: external API shape leaks into domain/application code.
  - Specification: domain predicates are combined, reused, and tested.
- Use DDD selectively:
  - Keep application services focused on orchestration.
  - Put real domain rules near domain concepts when the project has or benefits from that structure.
  - Do not introduce aggregates, repositories, domain events, or value objects merely because DDD vocabulary exists.
- Avoid N+1 database/RPC/API calls. For list or batch flows, collect parameters first, fetch in bulk, then map in memory.
- Keep comments outside the changed logic untouched.

### 7. Verify And Report

Run the planned verification. If a test fails, investigate before changing implementation further.

Final response should include:

- What changed.
- Why each meaningful change was justified.
- Whether business behavior was preserved or what approved behavior change was made.
- Verification commands and results.
- Remaining risks or unverified points.

## Output Quality Bar

Use these checks to keep outputs reviewable instead of ceremonial:

- A refactor plan is acceptable only if a reviewer can identify the entry point, changed files, unchanged files, data source or calculation point, verification command, and at least one concrete reason for each proposed step.
- A behavior-preservation claim is acceptable only if it names what did not change: public contract, query or remote-call parameters, calculation formula, persistence effect, validation/authorization rule, error type, or event/log side effect as relevant to the module.
- For modules with Redis/cache runtime state, timers, MQ, WebSocket, or after-commit callbacks, a behavior-preservation claim must also state which consistency boundary is unchanged: lock scope, timer lifecycle, dedupe key semantics, transaction boundary, retry/scan behavior, or notification timing.
- An uncertainty item is acceptable only if it blocks a decision or could change scope, behavior, compatibility, data correctness, or verification strategy. Do not list vague questions that can be answered by reading code.
- A design-pattern or DDD recommendation is acceptable only if it points to repeated variants, misplaced domain rules, dependency leakage, or testability pain visible in the target module.
- A final report is acceptable only if it connects each meaningful code change back to the reviewed plan and states whether the verification passed, failed, or could not be run.

If an output cannot meet this bar, gather more code evidence or reduce the proposed scope before proceeding.

## Refactor Heuristics

Use these heuristics to decide whether a change belongs in the refactor:

- **Include** changes that reduce a concrete problem visible in the target module: long method with mixed abstraction levels, repeated business rules, unclear dependency direction, hidden remote calls, hard-to-test branches, confusing names, duplicated DTO mapping, or misplaced validation.
- **Exclude** changes that only satisfy personal style: blanket renaming, moving files without boundary improvement, replacing straightforward code with patterns, generic base classes, new framework layers, or formatting churn.
- **Prefer minimal closed-loop fixes** when removing incorrect restrictions or historical guards. Do not add fallback fields, alternate branches, or cross-entity mappings unless proven by code, schema, query, or API usage.
- **Prefer readability that preserves locality**. Small functions are useful when they name a concept or isolate a responsibility; excessive fragmentation can make business flow harder to follow.
- **Prefer explicit dependencies**. Make data sources and side effects easier to see rather than hiding them behind vague helpers.

## Plan Review Checklist

Before implementing, confirm the plan answers:

- What exact module is being refactored?
- What current behavior must remain unchanged?
- What code evidence proves the real call chain and data source?
- Which changes are structural only?
- Which changes could affect behavior and therefore need approval?
- Why is each change necessary?
- What foreseeable requirement is being supported, and where is the evidence?
- What will not be touched?
- How will equivalence be verified?
- What is still uncertain and needs user confirmation?

## Validation Prompts

This skill includes `test-prompts.json` with representative prompts for dry-run or forward-testing validation. Use those prompts when evaluating whether the skill still enforces planning, behavior preservation, limited design, and explicit behavior-change review.
