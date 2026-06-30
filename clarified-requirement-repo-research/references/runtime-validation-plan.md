# Runtime Validation Plan

Use this reference when static source analysis cannot prove a requirement because behavior depends on runtime configuration, generated artifacts, remote services, broker state, data state, logs, traces, feature flags, or deployment environment.

## Runtime-Dependent Triggers

Mark a target as runtime-dependent when evidence depends on:

- active Spring profile, build variant, environment variable, or remote config
- generated code, bytecode enhancement, codegen routes, or reflection
- message broker subscriptions, delayed queues, retry queues, or consumer deployment
- remote service behavior, third-party SDK behavior, or data-service state
- database content, cache content, search index state, or object storage
- live logs, traces, metrics, dashboards, or user/session context

## Runtime Validation Item

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

## Validation Methods

Choose the least invasive method that can answer the question:

- inspect deployment/config metadata
- read logs or traces for a known request id
- call a safe read-only API
- inspect message topic subscriptions or consumer deployment
- run an existing test or local reproduction
- check database/cache/search state with approved read-only access
- ask user for environment-specific evidence when access is unavailable

## Safety Rules

- Do not run mutating runtime operations unless the user explicitly asks.
- Do not access remote, production, database, observability, or cloud resources without authorization.
- Do not print secrets or `.env` values.
- If runtime access is unavailable, record the exact missing evidence and the next human-verifiable step.

## Research Output

In `research.md`, runtime-dependent findings should include:

- what source evidence proves
- what source evidence cannot prove
- exact runtime evidence needed
- suggested validation method
- impact on planning or implementation
