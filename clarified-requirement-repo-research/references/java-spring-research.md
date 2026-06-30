# Java Spring Research

Use this reference when the selected repository or module is Java/Spring, Spring Boot, MyBatis, JPA, Dubbo, Feign, scheduled jobs, listeners, or similar backend code.

## Preferred Trace Order

Start from the requirement target and trace to the final effect:

1. Entrance: controller route, RPC provider, message listener, scheduled job, workflow delegate, CLI, or public service method.
2. Request/DTO binding: request class, path/query/body fields, Jackson annotations, aliases, validation annotations, and default values.
3. Service implementation: concrete implementation, injected dependencies, feature flags, guard clauses, and branch order.
4. Data or integration boundary: mapper/repository/JPA query, SQL/XML, RPC/HTTP client, message publication, cache, config service, or file/object storage.
5. Final effect: database read/write, response field assignment, event payload, remote payload, state transition, or calculation result.
6. Cross-cutting behavior: transaction, AOP/aspect, interceptor/filter, exception mapping, retry, async executor, scheduler, and idempotency.

## Controller To Service

- Record route path, HTTP method, class-level mapping, method-level mapping, request DTO, response wrapper, authentication/user context, and validation.
- Resolve the injected service implementation. Do not assume interface method behavior without finding the concrete implementation.
- If multiple implementations exist, check qualifiers, bean names, profiles, conditional annotations, configuration, or runtime-dependent selection.

## Service To Data Source

- Trace method parameters into the final mapper/repository/RPC call.
- Separate guard conditions from true business dependencies. A null check proves only that code guards a field; it does not prove the field determines the result.
- Confirm final query parameters, SQL filters, table names, joins, ownership scopes, and response assignment points.
- Avoid adding fallback relationships unless code/schema/query/API evidence proves the mapping is real.

## MyBatis/JPA/SQL

- For MyBatis, inspect mapper interface and XML/annotation SQL together.
- For JPA, inspect repository method names, annotations, specifications, entity mappings, and transaction boundaries.
- For hand-written SQL, record the exact WHERE/JOIN/GROUP conditions and parameter source.
- Check for N+1 risks when list rendering, batch aggregation, or loop enrichment is involved.

## RPC/HTTP/MQ

- Record client type, endpoint/topic/method, request payload, response usage, timeout/retry behavior, and fallback/error handling.
- For message flows, trace publisher, topic/tag/key, consumer, idempotency, and async transaction boundaries.
- Treat remote service state and broker subscriptions as runtime-dependent unless source plus runtime evidence confirms them.

## Cross-Cutting Checks

- `@Transactional`: propagation, rollback rules, async boundary crossing.
- AOP/aspects/interceptors/filters: authorization, logging, tenant/user context, idempotency, request mutation.
- Async/scheduler: executor, delay, retry, ordering, error handling.
- Config/profile/conditional beans: runtime profile, feature flags, remote config, build variants.

## Java/Spring Evidence Checklist

For every important conclusion, include:

- entrance file/symbol and route/topic/job
- concrete service implementation
- final data source or remote call
- key parameters at final fetch/calculation/write
- branch/guard that affects behavior
- transaction/async/error boundary
- exact source evidence
