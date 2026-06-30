# Forward Test Checklist

Use this checklist after substantial skill changes or when validating the skill on a real clarified requirement package. The goal is to test whether the skill can guide a fresh agent from a requirement document and explicit local repository path to a useful `research.md` without hidden context.

## Test Input

Prepare a realistic request with only the information a future user would provide:

```text
使用 $clarified-requirement-repo-research，根据 <clarified-requirement-file> 考古依赖仓库。
源码仓库本地路径：<local-checkout-path>
请输出 research.md。
```

If the task should use CodeGraph, choose a local checkout that already contains `.codegraph/`. Do not give the tester conclusions, suspected files, expected call chains, or known bugs unless those are present in the requirement document itself.

## Acceptance Criteria

The run is acceptable only if the output:

- States the clarified requirement input path and the analyzed local repository path before source conclusions.
- Does not assume a global repository collection path.
- Checks whether `.codegraph/` exists before using CodeGraph.
- Uses CodeGraph as navigation evidence and confirms decisive conclusions from source files.
- Extracts `AnalysisTarget` records before broad source scanning.
- Maps each important conclusion back to target ids.
- Distinguishes requirement claims, source-proven facts, framework-inferred edges, runtime-dependent behavior, and unknowns.
- Records tool capability boundaries, including CodeGraph freshness or staleness when available.
- Names missing repositories, inaccessible files, stale graph evidence, or runtime-only dependencies as unknowns instead of inventing conclusions.
- Produces a `research.md` shape compatible with `references/research-output-template.md`.

## Failure Signals

Treat these as skill gaps to fix:

- The agent guesses a repository path when the user did not provide one.
- The agent treats a remote URL or repository name as CodeGraph-capable.
- The agent relies on CodeGraph output without source confirmation.
- The agent scans source before extracting requirement targets.
- The agent drops targets that source does not confirm.
- The agent turns route/search confidence into `Proven`.
- The agent adds speculative fallback design instead of reporting the smallest source-backed conclusion.
- The final report lacks evidence paths, symbols, line ranges, or confidence levels.

## Review Notes

After each forward test, record:

- Prompt used:
- Requirement input:
- Local source path:
- CodeGraph available: yes / no / stale / unavailable
- Output path:
- What worked:
- What failed:
- Skill file or reference to update:
- Whether another forward test is needed:
