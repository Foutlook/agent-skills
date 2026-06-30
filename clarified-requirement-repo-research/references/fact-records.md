# Fact Records

Use this reference to keep source research evidence structured and traceable.

## Evidence Rules

- Every important claim needs repository, file path, line range or symbol, confidence, and linked `AnalysisTarget` ids.
- `codegraph` edges are navigation evidence until confirmed by source slices. Record graph freshness and coverage before relying on it.
- `repo-route` or repository search output is a hint until source files confirm ownership.
- Static source evidence cannot prove runtime-only conditions such as profile selection, generated artifacts, remote service state, broker subscription state, or production configuration.
- If a field appears only in a guard or null check, do not treat it as a business dependency until the final fetch, calculation, persistence, or remote call proves it matters.

## Tool Capability Probe

Record probes before relying on a tool family:

```markdown
### Tool Capability Probe
| Tool/Adapter | Repository | Inventory | Search | Read | Symbol | AST/PSI | Call Resolution | Diagnostics | Notes |
|---|---|---:|---:|---:|---:|---:|---:|---:|---|
|  |  |  |  |  |  |  |  |  |
```

Use `yes`, `no`, `partial`, or `failed`. If a probe fails, record the failure boundary and downgrade path.

## Codegraph Snapshot

Record this when a project-local `codegraph` is used:

```markdown
### Codegraph Snapshot CG-001
- Repository/path:
- `.codegraph/` path:
- Access path: MCP / CLI
- Status command/tool:
- Node/edge/file counts:
- Pending sync or stale-file warning:
- Generated branch/commit:
- Generation time:
- Covered modules/languages:
- Includes tests/generated code:
- Known blind spots:
- Freshness: Fresh / Unknown / Stale / Conflicting
- Used commands/tools:
- Source confirmation required:
```

## RepositoryCandidate

```markdown
### RepositoryCandidate R-001
- Repository/path:
- Source of hint:
- Route/search terms:
- Source hits:
- Confidence as hint:
- Confirmed by source:
- Excluded because:
- Unknowns:
```

## Entrance

```markdown
### Entrance E-001
- Target ids:
- Repository/module:
- Type:
- Route/topic/page/job/symbol:
- File/symbol evidence:
- Parameters or payload:
- Downstream owner:
- Confidence:
```

## Capability

```markdown
### Capability C-001
- Target ids:
- Repository/module:
- Behavior:
- Boundary:
- Inputs:
- Outputs/effects:
- Data sources:
- External dependencies:
- Evidence:
- Confidence:
```

## Edge

```markdown
### Edge G-001
- Target ids:
- From:
- To:
- Edge type:
- Parameters/payload:
- Sync/async:
- Transaction/retry/error behavior:
- Evidence:
- Confidence:
```

## Symbol

```markdown
### Symbol S-001
- Target ids:
- Repository/module:
- Kind:
- Name:
- File/path:
- Meaning:
- Used by:
- Evidence:
```

## Unknown

```markdown
### Unknown U-001
- Target ids:
- Topic:
- Why unknown:
- Evidence checked:
- Needed evidence:
- Impact:
- Suggested next step:
```

## RepoDependency

Record this when a target crosses repositories or runtime applications:

```markdown
### RepoDependency D-001
- Target ids:
- Upstream repository:
- Downstream repository:
- Direction:
- Interface/event/topic/SDK:
- Payload or key parameters:
- Sync/async:
- Ownership boundary:
- Evidence:
- Runtime dependency:
- Risk:
```

## RuntimeValidation

Record this when static source cannot prove behavior:

```markdown
### RuntimeValidation RV-001
- Target ids:
- Runtime question:
- Why static source is insufficient:
- Environment needed:
- Data/setup needed:
- Command/API/log/trace to check:
- Expected observation:
- Evidence owner:
- Risk if not validated:
- Status:
```

## Source Consistency Check

Before synthesizing conclusions:

- Confirm the entity set and mapping data come from the same source or prove their scopes match.
- Confirm query/fetch parameters at the final data access point.
- Confirm remote call parameters at the actual client invocation.
- Confirm final response assignment point for every response field under discussion.
- Reject additive fallback logic in conclusions unless evidence proves the original dependency is necessary and missing.
