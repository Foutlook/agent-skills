# Codegraph Guide

Use this reference only when the selected source repository is an explicit local checkout that contains a CodeGraph index. CodeGraph is a local-first code-intelligence tool: it stores symbols, edges, and files in a local `.codegraph/` SQLite database and exposes the graph through MCP tools and CLI commands. Treat CodeGraph as the preferred relationship navigation layer for local repositories, then confirm decisive conclusions from source slices.

## Official Documentation

- Introduction: `https://colbymchenry.github.io/codegraph/getting-started/introduction/`
- Quickstart: `https://colbymchenry.github.io/codegraph/getting-started/quickstart/`
- Your First Graph: `https://colbymchenry.github.io/codegraph/getting-started/your-first-graph/`
- Knowledge Graph: `https://colbymchenry.github.io/codegraph/core-concepts/knowledge-graph/`
- Resolution & Frameworks: `https://colbymchenry.github.io/codegraph/core-concepts/resolution/`
- MCP Server: `https://colbymchenry.github.io/codegraph/reference/mcp-server/`
- CLI: `https://colbymchenry.github.io/codegraph/reference/cli/`
- Languages: `https://colbymchenry.github.io/codegraph/reference/languages/`

## Discovery

Look for a project-local `.codegraph/` directory at the selected local repository root. If it exists and the CodeGraph MCP integration is active, prefer the MCP tool path. If MCP tools are not available but the CLI is installed, use CLI commands from the repository root.

Probe the current CodeGraph surface before choosing commands. Different installations expose different MCP tools and CLI subcommands; do not assume `explore` exists. Record the available commands/tools, then choose the strongest supported read-only navigation path.

If the user provided only a remote repository URL/name, treat it as a routing hint. CodeGraph is out of scope until the user provides a local checkout path.

Do not initialize, re-index, sync, or install CodeGraph unless the user asks or the task explicitly permits environment/tooling changes. For read-only archaeology, first inspect existing index status.

## Freshness Check

Before using CodeGraph facts, record:

- source repository path
- `.codegraph/` presence
- CodeGraph access path: MCP or CLI
- `codegraph_status` or `codegraph status` result when available
- node/edge/file counts when reported
- pending sync or staleness banners
- branch/ref/commit if available from repository metadata
- covered languages and likely excluded files
- known blind spots such as reflection, generated routes, Spring AOP, async executors, message brokers, feature flags, runtime configuration, `.gitignore` exclusions, dependency/build directories, and files over 1 MB

If a CodeGraph response contains a pending-sync or stale-file warning, read the named files directly before concluding.

## How To Use Codegraph

Use CodeGraph to answer navigation questions:

- Which files or symbols are near a requirement term?
- Which entrance calls this service/function?
- Which callers reach this method?
- Which callees are downstream of this entrance?
- Which module owns a symbol or package?
- Which cross-module or cross-repository dependencies appear in the graph?
- Which symbols should be read from source first?

Preferred MCP path:

- `codegraph_status`: check health, statistics, and pending sync when exposed.
- `codegraph_explore`: when exposed, ask a natural-language question or provide symbol/file names for architecture, flow, where-is-X, and how-does-X-work questions.
- Optional tools when available: `codegraph_node`, `codegraph_search`, `codegraph_callers`, `codegraph_callees`, `codegraph_impact`, `codegraph_files`.

CLI equivalents:

```bash
codegraph status
codegraph query UserService --kind class --limit 10
codegraph callers handleRequest --json
codegraph callees handleRequest --json
codegraph impact AuthMiddleware --depth 3
codegraph files --json
```

If the installed CLI exposes `explore`, use it for broad natural-language navigation after `status`. If it does not, approximate the workflow with `query` for candidate symbols/files, then `callers`, `callees`, and `impact` for graph expansion. Use `files` or local `rg --files` for inventory gaps, and always confirm conclusions by reading source.

Do not stop at CodeGraph output. For every important conclusion, read source files around the decisive route, method, query, mapper, RPC client, event publication, subscription, configuration key, or response assignment.

## Source Confirmation

After following a CodeGraph edge, confirm source facts:

```markdown
### Graph Edge Confirmation
- Target ids:
- Graph node/edge:
- Source file:
- Source symbol:
- Source lines:
- Confirmed parameters/payload:
- Confirmed branch/guard:
- Confirmed side effects:
- Confidence:
```

Use source lines as final evidence in `research.md`; cite graph as navigation or supporting evidence only.

## Conflict Handling

When CodeGraph and source disagree:

| Conflict | Interpretation | Action |
|---|---|---|
| CodeGraph shows edge but source no longer has it | Index may be stale, generated from another branch, or edge is indirect/generated | Check status/pending sync, re-check branch/commit, search source, mark graph `Stale` or `Conflicting` if not confirmed |
| Source has edge but CodeGraph misses it | Coverage may be partial or file excluded | Trust source, record CodeGraph blind spot |
| CodeGraph node path no longer exists | Index may be stale or repository moved files | Re-locate symbol by source search, record stale path |
| CodeGraph edge has heuristic provenance | Edge crosses dynamic dispatch or framework synthesis | Confirm wiring site and source behavior; mark confidence accordingly |
| CodeGraph cannot express framework wiring | Static graph is incomplete for runtime/framework behavior | Mark edge `Framework inferred` or `Runtime dependent` until source/runtime evidence confirms |

Never hide conflict by writing fallback conclusions. Name the mismatch and the smallest next step.

## Graph Vocabulary

Expect CodeGraph to model:

- nodes such as files, modules, classes, interfaces, functions, methods, fields, variables, imports, exports, routes, and components
- edges such as contains, calls, imports, exports, extends, implements, references, type_of, returns, instantiates, overrides, and decorates
- heuristic provenance for synthesized dynamic-dispatch edges

## Output Notes

In `research.md`, include a concise `Codegraph` subsection under tool boundaries:

- `.codegraph/` path and MCP/CLI access path
- status result and pending sync/staleness warnings
- branch/commit if available
- freshness
- coverage and blind spots
- available CodeGraph commands/tools and how CodeGraph was used, such as `explore` when available, `query`, `callers`, `callees`, `impact`, or `files`
- which conclusions were source-confirmed
