# Product Capability Model

Use this reference when turning source facts into product-facing capability conclusions. A capability is not just a class, endpoint, or method. It is a source-backed behavior boundary that answers one or more requirement verification targets.

## Capability Card

Record important capabilities with this shape before writing the final report:

```markdown
### Capability C-001
- Target ids:
- Capability name:
- Caller or actor:
- Trigger:
- Entrance:
- Owning repository/module:
- Core rule:
- Data reads:
- Data writes/effects:
- External dependencies:
- Guards versus true dependencies:
- Async/event/job behavior:
- Error, retry, transaction, or downgrade behavior:
- Product boundary:
- Runtime boundary:
- Evidence:
- Confidence:
```

## Required Distinctions

- Separate entrances from capabilities. One endpoint, listener, page, or job may expose multiple capabilities, and one capability may be reachable from multiple entrances.
- Separate guard conditions from business dependencies. A null check, permission check, feature flag, or early return is not a core dependency unless the final fetch, calculation, persistence, or remote call proves it affects the result.
- Separate source-backed behavior from requirement intent. Requirement language describes what should happen; source evidence proves what currently happens.
- Separate product boundary from implementation boundary. Product boundary describes the user or system scenario; implementation boundary describes repository, module, service, table, topic, SDK, or runtime owner.

## Capability Evidence Checklist

Before marking a capability `Confirmed`, verify:

- Entrance or trigger is visible in source, framework wiring, CodeGraph navigation plus source slice, or semantic adapter output.
- Owning module has decisive source evidence, not only route/search confidence.
- Core rule is supported by the branch/order/calculation point that actually affects output.
- Data reads/writes cite final mapper/repository/query/client/file/cache access points.
- External dependencies cite the actual client invocation, topic publish/subscribe, RPC method, SDK call, or generated client boundary.
- Runtime-only behavior is named as `Runtime dependent` instead of silently treated as proven.
- Each capability links back to one or more `AnalysisTarget` ids.

## Compact Report Format

Use a compact table for low-risk capabilities:

```markdown
| Capability | Actor/Trigger | Entrance | Owner | Core rule | Data/effects | Targets | Evidence | Level |
|---|---|---|---|---|---|---|---|---|
```

Use full capability cards for high-risk, cross-repository, source-mismatch, runtime-dependent, or implementation-planning-critical capabilities.

## Common Failure Modes

- Treating a controller method as the whole capability and missing downstream service rules.
- Treating a CodeGraph edge as final proof without reading the decisive source slice.
- Reporting repository ownership from a route/search result without source confirmation.
- Hiding inconsistent data sources with fallback wording instead of naming the mismatch.
- Claiming a field is required because it appears in validation, while the final query or calculation does not use it.
- Dropping targets that have no matching implementation instead of reporting `Not found`, `Runtime dependent`, or `Unknown`.
