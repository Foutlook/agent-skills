# Input Target Extraction

Use this reference to convert a clarified requirement package into source-verification targets before reading source code.

## Read Order

1. Read the primary clarified requirement document.
2. Read sibling artifacts only when referenced or needed: `spec.md`, `spec.zh-CN.md`, `plan.md`, prior `research.md`, `repo.list.md`, contracts, diagrams, issue/work-order notes, screenshots converted to text, or pasted evidence.
3. Identify whether source repository paths or repository identifiers are explicit. If not, ask the user to provide them before source archaeology.

## Extraction Rules

- Treat requirement text as claims to verify, not source facts.
- Extract behavior targets, data targets, integration targets, ownership targets, compatibility targets, and validation targets separately when they differ.
- Preserve negative scope and non-goals. They prevent source search from drifting.
- Keep target ids stable, such as `T-001`, `T-002`, and reuse them in fact records and the final report.
- Do not infer cross-entity mappings unless code, schema, query, API usage, or the requirement explicitly proves the relationship.

## InputDocument Template

```markdown
### InputDocument
- Path:
- Type:
- Requirement package directory:
- Sibling artifacts read:
- Source repository paths or identifiers:
- Missing source boundary:
- Document gaps:
```

## AnalysisTarget Template

```markdown
### AnalysisTarget T-001
- Claim:
- Verification question:
- Expected behavior:
- Source hints:
- Suspected repository/module:
- Key symbols/entities/API names:
- Priority:
- Non-goals:
- Input evidence:
- Status: Requirement claim
- Open questions:
```

## Target Categories

Use these categories only when they help structure the work:

- `Behavior`: user-visible or system-visible behavior that must be confirmed.
- `Entrance`: API, page, Activity, listener, job, consumer, command, SDK, or workflow entry.
- `Data`: persistence, query, calculation, ownership, mapping, cache, or status source.
- `Integration`: RPC, HTTP, message topic, SDK, third-party system, or platform callback.
- `Boundary`: repository/module ownership, source split, cross-app handoff, build variant, or deployment dependency.
- `Validation`: tests, logs, observability, manual verification, or runtime-only evidence.

## Extraction Checklist

- Identify all actors, systems, pages, APIs, jobs, events, and state changes named by the requirement.
- Convert each ambiguous requirement into a verification question.
- Capture exact words or identifiers that can seed source search.
- Mark missing repository path as a blocker for source archaeology.
- Separate "new behavior expected" from "existing behavior found".
