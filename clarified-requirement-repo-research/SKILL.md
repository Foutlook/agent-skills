---
name: clarified-requirement-repo-research
description: Use when a clarified requirement document, PRD, speckit spec, work-order analysis, or feature brief has already been produced and Codex needs to archaeologically inspect user-specified dependent backend source repositories to identify repository boundaries, required code-change repositories, per-repository change scope, implementation owners, entrances, call chains, data sources, integration boundaries, risks, and source-backed evidence before planning or coding. Default to the configured read-only remote repository codebase MCP `repo_codebase` (`mcp_servers.repo_codebase`, streamable-http, `http://idea-mcp.91jzx.cn/stream`) as the source repository entrypoint; read local checkouts only when the remote MCP cannot read the needed repository, file, search result, or semantic evidence, or when the user explicitly asks for local-only analysis. Trigger for requests such as "根据澄清后的需求考古依赖仓库", "分析需要改哪些仓库", "每个仓库变更范围", "基于 spec 找源码证据", "输出 research.md", or "先做后端依赖仓库调研".
---

# Clarified Requirement Repo Research

## Purpose

Turn a clarified requirement document into a source-backed backend dependency repository research report. Use the clarified requirement as input claims, not source truth. Extract verification targets, locate dependent backend repositories or modules, determine repository boundaries, identify which repositories need code changes, define each repository's change scope, then reconstruct entrances, behavior, data flow, ownership, and unknowns from read-only source evidence.

This skill complements `repo-research`: keep its evidence discipline, but start from a clarified requirement package and focus on cross-repository dependency archaeology before implementation planning.

## References

- Read `references/input-target-extraction.md` when extracting analysis targets from a clarified requirement, PRD, speckit spec, work-order analysis, issue note, or pasted evidence.
- Read `references/codegraph-guide.md` when the selected local repository contains `.codegraph/` or CodeGraph MCP/CLI tools are available for that local checkout.
- Read `references/tool-selection-guide.md` before choosing project-local codegraph, local filesystem, remote repository, MCP/codebase adapter, IDE-backed adapter, or text-search fallback paths.
- Read `references/java-spring-research.md` when the selected repository or target slice is Java/Spring, Spring Boot, MyBatis, JPA, RPC provider/client, listener, scheduler, or backend service code.
- Read `references/multi-repo-dependency.md` when a requirement crosses repositories, applications, clients, BFF layers, backend services, shared SDKs, message consumers, or configuration/material repositories.
- Read `references/product-capability-model.md` when reconstructing product-facing capabilities from entrances, call chains, data access, and integration evidence.
- Read `references/runtime-validation-plan.md` when static source analysis cannot prove behavior because runtime configuration, generated artifacts, remote service state, broker state, data state, logs, traces, or deployment environment are needed.
- Read `references/forward-test-checklist.md` after substantial skill changes or when validating the skill on a realistic clarified requirement plus explicit local repository path.
- Read `references/fact-records.md` when recording source facts, repository candidates, entrances, edges, symbols, unknowns, or tool capability probes.
- Read `references/research-output-template.md` before writing or updating the final `research.md`.

## Source Repository Boundary

- Treat the current requirement/specification workspace as planning material, not source truth, unless the user explicitly says the source code lives there.
- Default the research domain to backend source code: backend services, BFF/gateway, domain services, shared backend SDKs, mappers/repositories, scheduled jobs, listeners, message consumers, backend configuration, SQL/migrations, and backend-facing contracts. Include frontend/mobile/client repositories only when the requirement explicitly asks for them or backend evidence proves a contract/UI coordination dependency.
- For personal use, default source access to the configured read-only remote repository codebase MCP: `[mcp_servers.repo_codebase]`, `type = "streamable-http"`, `url = "http://idea-mcp.91jzx.cn/stream"`. Treat its exposed read/list/search/symbol capabilities as the first source repository entrypoint.
- Remote URLs, repository identifiers, `repo.list.md` entries, and routing results are usable as remote MCP lookup hints. Try `repo_codebase` inventory/search/read capabilities first instead of asking for a local checkout path by default.
- Read local checkouts only after the remote MCP cannot read the needed repository, branch/ref, file, search hit, source slice, or semantic evidence, or when the user explicitly asks for local-only analysis.
- CodeGraph is available only for an explicit local checkout path that contains `.codegraph/`; use it after falling back to local analysis, not as the default first source path.
- If the remote MCP cannot read the required source and no local source repository path is available, ask the user to specify the local checkout path. Do not continue by guessing from locally visible directories.
- Do not default to locally visible source repositories just because they are easy to read. First identify the intended source boundary from the clarified requirement, `repo.list.md`, repository routing result, work-order metadata, or user-provided repository path.
- State each analyzed repository or project path before source analysis. State any candidate repository that is excluded and why.

## Required User Checkpoints

Pause and ask the user before continuing when a source boundary or access decision cannot be proven from the request:

- The configured `repo_codebase` remote MCP is unavailable, lacks the needed read/search/list/symbol capability, or cannot access the target repository/ref/file, and no explicit local source repository path is available for fallback archaeology.
- The input provides only a vague product clue with no repository identifier, routing result, repo list entry, source hint, or local fallback path, and remote MCP lookup cannot narrow the owner.
- Multiple repository candidates are plausible and the clarified requirement package does not identify the intended owner.
- The task depends on CodeGraph, but the selected local checkout has no `.codegraph/`, the graph is stale/conflicting, or source fallback is insufficient for the requested conclusion.
- Verification requires runtime, remote service, observability, production data, environment access, or any write-capable action not already authorized by the user.
- The user request shifts from read-only research to source edits, build changes, commits, or runtime mutation.

## Stable Fact Records

Normalize important findings into these intermediate records before synthesis:

- `InputDocument`: input file path, document type, requirement package directory, sibling artifacts read, and unresolved document gaps.
- `AnalysisTarget`: target id, requirement claim, verification question, expected behavior, source hints, priority, non-goals, and current status.
- `RepositoryCandidate`: repository id/path, route terms, source hits, confidence as a hint, and unresolved ownership questions.
- `Entrance`: route, controller, page/activity, listener, job, workflow delegate, message consumer, CLI, SDK method, or public service entrypoint.
- `Capability`: user-visible or system-visible behavior owned by a module, with boundaries and evidence.
- `Edge`: direct call, framework wiring, injected dependency, event publication, subscription, async dispatch, scheduled execution, RPC, HTTP, SQL, or message edge.
- `Symbol`: class, method, function, route, table/model, config key, topic, event, DTO, request/response field, or build artifact.
- `ChangeScope`: repository/module, change decision, required or not, backend layer, target ids, files/classes likely to change, contract/config/data changes, tests, migration/runtime validation, evidence, and confidence.
- `Unknown`: runtime-only dependency, missing repository, unavailable tool, conflicting source evidence, or unverified assumption.

Link `Entrance`, `Capability`, `Edge`, `Symbol`, `ChangeScope`, and `Unknown` records back to `AnalysisTarget` ids whenever the research is target-driven.

## Repository-Dimension Change List

The final research report must make the code-change repositories visible by repository dimension before describing target-level or module-level details:

- Treat `需改仓库清单` as the authoritative repository-dimension summary. It must contain one row per repository or repository/module boundary that may be affected.
- Include all repositories classified as `Must change`, `May change`, `Runtime/config only`, or `Unknown` in the summary table. Repositories proven as `No code change` can be listed in the exclusion/boundary section, but do not mix them into the required-change list unless they are needed to explain a dependency.
- Do not only list changes by `AnalysisTarget`, entrance, package, class, or module. Always group the change decision back under its owning repository.
- `每仓库变更范围` must contain one subsection for every repository in the change summary table, using the repository name/path as the subsection title.
- If a single target affects multiple repositories, duplicate the target id under each affected repository and explain that repository's owned boundary, not a generic cross-target action.
- If repository ownership cannot be proven, keep the row as `Unknown` and state exactly what source evidence is missing; do not hide it inside a general risk paragraph.

## Capability Probe And Tool Selection

- First probe the configured `repo_codebase` remote MCP and record whether it can provide repository inventory, file listing, exact file reads, indexed search, source slices, symbol lookup, AST/PSI, call resolution, or diagnostics for the target repository/ref.
- Use remote MCP read-only capabilities as the default high-resolution path. Prefer semantic/source-slice evidence returned by `repo_codebase` over local text search when both are available.
- If remote MCP access fails, is incomplete for the decisive evidence, or cannot identify the requested repository/ref, downgrade to a user-provided local checkout path and record the remote failure boundary.
- When falling back to an explicit local checkout that has `.codegraph/`, use CodeGraph first as a relationship navigation layer for entrances, call chains, symbol neighborhoods, and module dependencies. Confirm final conclusions with source file reads.
- If the repository is remote-only or identified only by name and remote MCP cannot provide enough evidence, ask for a local checkout path only for the missing evidence or CodeGraph-backed analysis.
- If `.codegraph/` exists in the selected local checkout or CodeGraph MCP/CLI tools are available for that checkout, read `references/codegraph-guide.md`, probe the actually available CodeGraph commands or MCP tools, then use the strongest available graph navigation path before broad text search.
- Probe available repository adapters before choosing the analysis path. Record which capabilities exist: inventory, file list/read, indexed search, symbol resolution, AST/PSI extraction, call resolution, framework inference, source slicing, diagnostics, and optional runtime evidence.
- Prefer the strongest verified capability per language: semantic AST/symbol/call resolution first, indexed search and framework conventions second, raw text search as candidate discovery or fallback.
- Do not assume one adapter's language support means another adapter exposes equivalent semantic APIs. If a capability is unavailable, record the downgrade and confidence impact.
- Treat tool adapters as implementation details. Product conclusions must be expressed as source facts, not as dependency on one MCP, IDE, language server, linter, or CLI.
- If the input includes repository-routing output, treat candidate repositories, route terms, source hits, candidate directories, and unknowns as source hints only. Do not convert route confidence such as `高` into `Proven`.

## Language-Specific Notes

- Java/Kotlin/Spring/Android: when an IDEA-backed adapter or equivalent semantic codebase adapter is available, use it as the high-resolution path. Confirm key symbols with symbol information, inspect framework wiring and call edges semantically, and use source reads for final evidence slices. Text and regex search are candidate discovery or fallback, not substitutes for successful PSI facts.
- Java/Spring: inspect controllers, service implementations, repositories/mappers, DTOs, scheduled jobs, listeners, AOP/aspects, transaction boundaries, config/profile gates, SQL/query clients, RPC/HTTP SDKs, message clients, and exception handling.
- Android/Kotlin: inspect activities/fragments/pages, navigation, lifecycle observers, receivers, view models, bridges, SDK calls, local persistence, feature flags, and build variants.
- JavaScript/TypeScript/Node.js/frontend/Python/Go/Rust: probe available semantic tooling first, then use manifests, route declarations, imports, symbols, framework conventions, indexed search, and source slices. Mark framework-inferred edges when runtime routing, dependency injection, decorators/macros, or generated handlers affect truth.

## Workflow

1. Establish the requirement package.
   - Identify the clarified requirement file, its sibling artifacts, and the output directory.
   - Read the clarified requirement first, then read sibling context only when directly referenced or needed: `spec.md`, `spec.zh-CN.md`, `plan.md`, `research.md`, `repo.list.md`, contracts, diagrams, issue/work-order notes, or pasted evidence.
   - If the requirement is not actually clarified and key behavior, actors, source boundaries, or success criteria are missing, stop and ask for clarification instead of inventing repository assumptions.

2. Extract verification targets.
   - Read `references/input-target-extraction.md` before target extraction.
   - Normalize the requirement into target records before scanning source code.
   - For each target, record: target id, requirement claim, expected behavior, source hints, suspected repository/module, key entities or API names, priority, non-goals, and open questions.
   - Separate requirement statements from source facts. Requirement language such as "should", "new", or "expected" is not proof that code exists.

3. Locate dependent repositories.
   - Read `references/tool-selection-guide.md` before choosing concrete repository access tools.
   - Prefer explicit repository hints from the clarified requirement package, `repo.list.md`, work-order metadata, module names, endpoint names, package names, app identifiers, or existing research.
   - If repository ownership is unknown, route first using available read-only repository search/list tools, then use the configured `repo_codebase` remote MCP to validate candidate repositories before any local checkout fallback.
   - State the analyzed source project path or repository identifier before analysis. Do not confuse the current specification/workspace repository with a source repository.
   - Determine the repository boundary before deep analysis: primary backend owner, dependent backend repositories, shared SDK/contract repositories, configuration or SQL repositories, and repositories intentionally excluded.
   - For every repository candidate, classify it as `Must change`, `May change`, `No code change`, `Runtime/config only`, or `Unknown`, and keep the classification evidence-backed.
   - Build the code-change repository list by repository dimension before writing implementation details. The list is not optional when any source repository is inspected.

4. Inspect source repositories read-only.
   - Read `references/fact-records.md` before recording repository candidates, tool probes, source facts, or unknowns.
   - Read `references/codegraph-guide.md` when `.codegraph/` exists or CodeGraph tools are available.
   - Read `references/java-spring-research.md` for Java/Spring backend slices.
   - Read `references/multi-repo-dependency.md` when analysis spans more than one repository or runtime application.
   - Use only read-only capabilities. Default to `repo_codebase` remote MCP inventory, list/search/read file APIs, source slices, semantic codebase adapters, indexed search, or IDE-backed symbol lookup when exposed by the remote adapter.
   - Fall back to project-local CodeGraph, local filesystem reads, and shell text search over authorized local mirrors only when the remote MCP cannot read the necessary evidence or the user explicitly requests local-only analysis.
   - Do not use write-capable codebase namespaces or mutate source repositories unless the user explicitly asks for edits.
   - Inventory languages and product surface: VCS roots, modules, source roots, test roots, generated-code roots, Maven/Gradle manifests, `pyproject.toml`, `Cargo.toml`, `package.json`, HTML route roots, `go.mod`, app identifiers, and build variants.
   - Start from manifests and entrances: controllers, routes, activities/pages, listeners, jobs, workflow delegates, message consumers, SDKs, CLIs, public service methods, and frontend routes.
   - When scope is broad, split work by analysis target, module, entrance family, or cross-cutting mechanism. Use subagents for independent slices when available.

5. Reconstruct dependency behavior.
   - Read `references/product-capability-model.md` before synthesizing capability conclusions for the final report.
   - Map each verification target to implementation owners, entrances, capabilities, call chains, data reads/writes, async/event/job paths, external APIs/RPCs, configuration gates, and runtime-dependent points.
   - Expand direct and implicit chains: injected interfaces, route handlers, middleware, decorators/macros, generated handlers, AOP/aspects, interceptors, filters, guards, event emitters, pub/sub, scheduled jobs, async executors, repositories, ORM models, SQL/query clients, HTTP/RPC SDKs, message clients, and config.
   - Track source consistency: do not build an entity set from source A while mapping ownership/status/chapter/flow data from source B unless evidence proves the scopes match.
   - Distinguish guards from real business dependencies. Trace to the final fetch, calculation, persistence, or remote call before concluding a field or module is required.
   - Avoid speculative fallback designs. Prefer the smallest source-backed conclusion: confirmed, partially confirmed, not found, runtime-dependent, or unknown.
   - Derive each repository's code-change scope from proven gaps or contract/data ownership. Do not mark a repository as `Must change` just because it appears in a downstream call chain; prove that its owned contract, behavior, schema, config, or data source must change for the target to pass.
   - When synthesizing multiple targets, aggregate all per-target changes back into per-repository `ChangeScope` records so the handoff shows which repository changes, why, and what coordinates with it.

6. Verify evidence.
   - Attach file path, line range or symbol, repository/module, and confidence to every important claim.
   - Use minimal source slices around the decisive code: final assignment points, query parameters, remote call arguments, branch order, transaction boundaries, retries, async dispatch, and exception handling.
   - If tools fail or repositories are unavailable, record the attempted tool, failure boundary, and what evidence remains unverified.
   - Read `references/runtime-validation-plan.md` when static source evidence cannot prove the target.
   - Do not claim full runtime truth from static code alone. Runtime configuration, generated bytecode/artifacts, remote services, broker state, live subscriptions, traces, and logs require runtime evidence.

7. Write the research report.
   - Read `references/research-output-template.md` before writing or updating the report.
   - Default output: `research.md` in the same package/directory as the clarified requirement input, unless the user requests another path.
   - Preserve existing sibling documents and comments. If updating an existing `research.md`, change only the sections needed for the current research.
   - Keep conclusions evidence-first and make unknowns actionable.
- Always include a code-change repository list and per-repository change scope before handoff to planning or implementation.
- The code-change repository list must be grouped by repository first, not by requirement target first. Each listed repository must have a matching subsection in `每仓库变更范围`.

## Output Shape

Use this structure unless the user asks otherwise:

```markdown
# 依赖仓库考古 Research

## 输入与范围
## 需求目标提取
## 仓库与模块定位
## 需改仓库清单
## 每仓库变更范围
## 入口清单
## 能力地图
## 模块与边界
## 核心业务逻辑
## 调用链与时序
## 数据来源与状态
## AOP/事件/异步/任务
## 外部依赖
## 目标验证结论
## 风险与未知
## 证据索引
## 工具与边界记录
```

For sequence diagrams, label static-only chains as `源码推断时序`. Use `alt`, `opt`, `par`, and explicit async notes when branches or asynchronous behavior matter.

## Evidence Levels

| Level | Meaning |
|---|---|
| Proven | Direct source fact or verified semantic-tool fact with repository, file, line/symbol evidence. |
| Framework inferred | Static framework convention connects components, but runtime selection may depend on config, profile, bean name, build variant, or generated code. |
| Requirement claim | Comes from the clarified requirement package and still needs source validation. |
| Runtime dependent | Requires live config, generated artifact, remote service, broker state, trace, log, or environment evidence. |
| Unknown | Static source evidence is insufficient, unavailable, or conflicting. |

## Handoff Checklist

Before finishing, include:

- Clarified requirement input path and output `research.md` path.
- Analyzed repositories/modules, backend repository boundary, required code-change repositories, and any repositories intentionally excluded.
- Per-repository change scope: owned capability, API/DTO/contract, service/domain logic, data model/SQL, config, async/job/message, tests, migration, runtime validation, and confidence.
- A repository-dimension change summary that lets the reader answer “需要改哪些仓库” without reading the whole report.
- Evidence chain for each major conclusion: failure or behavior point, actual data source, key parameters, and why the conclusion is sufficient.
- Unverified assumptions, unavailable tools, missing repositories, or runtime-only questions.
- Suggested next step: planning, implementation, additional clarification, or runtime validation.
