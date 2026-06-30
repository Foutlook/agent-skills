# Tool Selection Guide

Use this reference to choose a source-access path for personal repository archaeology. Default to the configured read-only remote repository codebase MCP `repo_codebase` as the source repository entrypoint: `[mcp_servers.repo_codebase]`, `type = "streamable-http"`, `url = "http://idea-mcp.91jzx.cn/stream"`. Use local checkouts only when the remote MCP cannot read the needed repository, branch/ref, file, search result, source slice, or semantic evidence, or when the user explicitly requests local-only analysis. CodeGraph applies only after falling back to a selected local checkout containing `.codegraph/`.

## First Decision

| Situation | Action |
|---|---|
| User gives a local repository path | Still probe `repo_codebase` first when repository identity/ref can be mapped to remote. Use the local path as fallback or when the user explicitly requests local-only analysis; if local fallback is used, verify it exists, check for `.codegraph/`, and use CodeGraph before broad text search when available. |
| User gives a remote repository URL or name | Use it as the primary lookup hint for `repo_codebase`; do not ask for a local checkout unless remote read/search/list/symbol evidence is unavailable or insufficient. |
| Requirement package names repositories in `repo.list.md` or metadata | Treat them as remote MCP lookup candidates first. Confirm each candidate with source evidence before marking ownership proven. |
| Only product keywords are available | Route/search repositories read-only first, then validate likely candidates through `repo_codebase`. Treat route/search confidence as hints only. |
| Remote MCP cannot read the needed evidence and no local repository path is available | Stop and ask the user to specify the local checkout path. Do not guess from local directories. |

## Access Priority

Prefer the strongest available read-only source for the selected repository:

1. Configured remote `repo_codebase` MCP read-only capabilities: repository inventory, file listing, exact file reads, indexed search, source slices, symbol lookup, AST/PSI, call resolution, diagnostics, or equivalent semantic evidence.
2. Other read-only semantic codebase or IDE-backed adapters when they can prove symbol/call/AST/PSI facts for the same target repository/ref.
3. Project-local CodeGraph only after local fallback is required and the selected repository is a local checkout with `.codegraph/`.
4. Local filesystem read over the explicit repository path when remote MCP evidence is unavailable or insufficient.
5. Raw text search fallback with source slices for confirmation.

Do not use write-capable adapters for read-only archaeology. If only a write-capable namespace exists, ask for a read-only path or use a local explicit checkout if available.

## Project-Local Codegraph

When the selected local repository contains `.codegraph/`:

- Treat CodeGraph as a relationship navigation layer, not final product truth.
- Run or request `codegraph_status` / `codegraph status` when available to check health and pending sync before relying on the graph.
- Probe which CodeGraph MCP tools or CLI subcommands are actually available. Prefer MCP `codegraph_explore` or CLI `codegraph explore` when present; otherwise use focused commands such as `query`, `node`, `callers`, `callees`, `impact`, and `files`.
- After following a CodeGraph edge, read the source files around the decisive method, route, query, mapper, RPC client, event publication, subscription, or response assignment.
- If CodeGraph and source disagree, trust source and record the graph as stale, partial, or conflicting.
- If CodeGraph does not cover framework wiring, reflection, configuration routing, Spring AOP, async execution, message brokers, generated code, or runtime feature flags, mark those edges as framework inferred or runtime dependent until source/runtime evidence confirms them.

## Local Repository Path

When the user provides a local path:

- Confirm the path is the intended source repository, not the requirement/specification package.
- Check whether the project has `.codegraph/`; if yes, use CodeGraph before broad text search.
- Inspect top-level manifests before deep search: Maven/Gradle, `package.json`, `go.mod`, `pyproject.toml`, `Cargo.toml`, Android manifests, iOS/project files, route roots, and module folders.
- Use `rg --files` and targeted `rg -n` searches when no semantic adapter is available.
- Keep reads UTF-8 and avoid modifying files unless the user explicitly changes the task from research to implementation.

## Remote Repository Or Repository Service

When the user provides a remote repository URL/name:

- Treat it as the primary lookup hint for the configured `repo_codebase` remote MCP.
- Use configured read-only repository service tools by default: list repositories, list branches, list files, get file blobs, search code, source slices, semantic symbol/call lookup, or equivalent exposed capabilities.
- Do not attempt CodeGraph analysis for a remote-only repository.
- Record the branch/ref used. If branch is unspecified, use the default branch reported by the tool or ask when default cannot be determined.
- If remote access fails because of auth, network, permissions, missing tools, missing repository, missing ref, or incomplete source evidence, record the boundary and fall back to a user-provided local checkout. Ask for a local path only when it is not already available.

## MCP Or Codebase Adapter

Before relying on an adapter, run a capability probe and record it in `fact-records.md` format:

- Inventory: project path, VCS roots, modules, source roots, test roots, generated roots, manifests.
- Search/read: file listing, indexed search, exact file reads, source slices.
- Semantics: symbol lookup, type resolution, references, call resolution, AST/PSI, diagnostics.
- Runtime: logs, traces, configuration, or live evidence if explicitly requested and available.

Use semantic facts when the probe proves they are available. If a semantic probe fails, downgrade to indexed/text search and mark confidence accordingly.

## IDEA-Backed Java/Kotlin Path

When the adapter is IDEA-backed and the repository slice is Java/Kotlin:

- Use module/source-root inventory before shell/text inventory.
- Resolve key classes, methods, routes, DTOs, mappers, listeners, and config symbols semantically when possible.
- Use source reads to capture final evidence slices even when semantic lookup succeeds.
- Treat regex matches as candidate discovery, not final proof, when PSI/symbol facts are available.

## Fallback Text Search Path

Use fallback text search when `codegraph`, semantic adapters, and indexed adapters are unavailable or incomplete:

- Start from requirement identifiers: endpoint paths, DTO fields, table names, topic names, class names, app ids, package names, UI text, config keys, and error messages.
- Search narrowly, then expand through imports, references, route registration, dependency injection, and manifest/module structure.
- Confirm every conclusion with nearby source lines and record confidence as direct source fact or framework inferred.

## Stop And Ask Conditions

Stop and ask the user when:

- The configured `repo_codebase` remote MCP cannot read the required evidence and no explicit local source repository path exists for fallback analysis.
- Multiple repository candidates look plausible and the requirement gives no ownership clue.
- The selected repository is inaccessible and no equivalent read-only source is available.
- The task depends on CodeGraph, remote MCP evidence is insufficient, and only a remote repository URL/name was provided.
- The task depends on CodeGraph but the local checkout has no `.codegraph/`, or the graph is stale, unreadable, or generated from a different branch/commit and no source fallback is sufficient.
- Verification requires runtime-only evidence and the user has not authorized runtime, remote, observability, or environment access.
- The task has shifted from research to code changes.
