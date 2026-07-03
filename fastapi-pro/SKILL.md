---
name: fastapi-pro
description: Designs, implements, reviews, and diagnoses production FastAPI services with Pydantic and SQLAlchemy. Use when work involves FastAPI routes, dependencies, validation, authentication, async I/O, database sessions, WebSockets or SSE, OpenAPI contracts, tests, or API performance.
---

# FastAPI Pro

Default to async-first, end-to-end non-blocking I/O for FastAPI work. Treat synchronous I/O as an explicit compatibility boundary and isolate it from the event loop rather than letting it shape the service.

Within that default, treat the repository's pinned versions, architecture, and conventions as the source of truth. Do not add dependencies or upgrade packages unless the task requires it.

## Workflow

### 1. Ground the task

- Classify the work as build/change, design/review, or diagnosis/performance.
- Inspect project configuration and adjacent app construction, routes, schemas, dependencies, persistence code, exception handlers, and tests before proposing a pattern.
- Trace the request path across the HTTP, validation, authorization, domain, persistence, and external-service boundaries that the task touches.

Complete this step when the target behavior, compatibility constraints, framework versions, and affected boundaries are known.

### 2. Make the contract explicit

For endpoint work, define or recover:

- method and path;
- path, query, header, and body inputs with validation constraints;
- success response schema, headers, and status code;
- error conditions and the project's error envelope;
- authentication, object-level authorization, and sensitive-data rules;
- pagination, idempotency, concurrency, or versioning semantics when relevant.

Preserve public behavior unless a breaking change is requested. For REST endpoint design or review, read and apply [REST_API_CHECKLIST.md](REST_API_CHECKLIST.md).

Complete this step when every externally observable outcome has an intentional contract.

### 3. Take the matching branch

#### Build or change

- Use Pydantic models at the transport boundary; keep persistence models internal. Separate input and output models when mutability, permissions, or representation differ.
- Use FastAPI dependencies for request-scoped resources and cross-cutting policy. Prefer typed `Annotated` aliases when the repository already uses them.
- Build an end-to-end async I/O chain by default: use `async def`, async database drivers, and async HTTP clients. When a blocking library is unavoidable, isolate it with the repository's thread-pool or worker pattern; never execute blocking I/O on the event loop.
- Manage shared application resources with lifespan context and request resources with cleanup-aware dependencies.
- Keep one SQLAlchemy session per request or unit of work. Bound transactions explicitly, roll back failures, prevent accidental lazy I/O, and never share an `AsyncSession` across concurrent tasks.
- Keep HTTP translation at the router boundary. Introduce service or repository layers only when domain complexity or the existing architecture warrants them.
- Map domain failures to stable HTTP errors at the boundary. Do not leak internals, credentials, or data the caller cannot access.

Complete this branch when the implementation matches the contract and resource, transaction, authorization, and async boundaries are explicit.

#### Design or review

- Apply every relevant item in the REST checklist and trace implementation behavior rather than judging route declarations alone.
- Prioritize correctness, contract compatibility, authorization, data exposure, transaction safety, async hazards, and missing tests.
- Report findings first, ordered by severity. Include file and line, observed evidence, impact, and a concrete correction; avoid speculative rewrites.
- If there are no material findings, say so and identify residual risks or unverified behavior.

Complete this branch when every affected contract and relevant checklist item has been accounted for.

#### Diagnose or tune

- Reproduce the failure or establish a baseline before changing code.
- Form and test specific hypotheses. Inspect blocking I/O, N+1 queries, implicit lazy loads, oversized serialization, connection-pool pressure, leaked resources, transaction scope, and downstream latency as relevant.
- Make the smallest evidence-backed correction, then repeat the original measurement or reproduction.

Complete this branch when evidence identifies the cause and the same probe demonstrates the result.

### 4. Verify

- Add or update focused tests for the changed contract and regression. Cover success plus relevant validation, not-found/conflict, authentication, authorization, rollback, and concurrency cases.
- Assert status, response body and headers, side effects, and forbidden side effects—not merely that the endpoint returns.
- Run the repository's configured formatter, linter, type checker, and smallest sufficient test set; widen testing when shared boundaries changed.
- Confirm generated OpenAPI reflects the intended public contract when routes or schemas changed.

Complete the task only when changed behavior is exercised, applicable checks pass, and any check that could not run is reported with the reason.

