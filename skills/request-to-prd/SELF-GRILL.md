# Self-Grill Procedure

## Purpose

Run the questioning part of a grill session without interrupting the user. The agent asks the questions internally, researches the repo when possible, chooses recommended answers when defensible, and records the questions that genuinely require a human.

## Evidence Rules

- **Fact**: Directly supported by the user's request, repo docs, code, tests, issue tracker, or visible product text.
- **Assumption**: Not directly proven, but a normal product or engineering default fits the request and repo shape.
- **Requires human input**: Depends on product strategy, user intent, policy, legal/compliance judgment, customer promises, risk acceptance, production-only data, unavailable external facts, branding, pricing, or subjective UX preference.
- **Contradiction**: The request, docs, code, or tests disagree. Surface the conflict and recommend the least risky interpretation.

Do not turn an unknown into an assumption just to make the PRD look complete.

## Case File

Before drafting, build a private case file:

- Request type: `bug`, `feature`, or `mixed`.
- Stated user problem and desired outcome.
- Actors, permissions, plans, roles, or personas involved.
- Named domain concepts and their glossary definitions.
- Current behavior found in code, tests, docs, logs, screenshots, or issue text.
- Similar existing workflows, APIs, commands, screens, or test patterns.
- Constraints: compatibility, migration, performance, security, privacy, rollout, dependencies.
- Explicit non-goals and likely exclusions.
- Open contradictions and unavailable evidence.

Use this case file to answer the question bank. The case file does not need to appear in the final answer unless useful.

## Question Bank

Ask the relevant questions below. Add project-specific questions when the request or code suggests them. Record only the important resolutions in the final self-grill log.

### Domain Language

- What exact domain concept is the user naming?
- Does the glossary define the term differently?
- Are there overloaded terms such as account, user, organization, project, workspace, session, job, task, run, event, or state?
- What canonical term should the PRD use?
- What terms should be avoided because they conflict with existing docs or code?
- Is the request describing one bounded context or multiple contexts?

### Current Behavior

- What does the system do today?
- Where is that behavior visible: UI, API, CLI, job, integration, data model, or background process?
- Which modules appear to own the behavior?
- Are there tests that lock in current behavior?
- Is this current behavior intentional, accidental, legacy, or undocumented?
- Does code contradict the user's description?

### Desired Behavior

- What should be different when the work is complete?
- What must stay the same?
- What is the smallest change that solves the user-visible problem?
- What would a user observe as proof that the issue is fixed or the feature exists?
- Is the request asking for a product behavior change, implementation cleanup, data repair, or operational process?

### Bug-Specific Questions

- What is the expected behavior?
- What is the actual behavior?
- How can the issue be reproduced or detected?
- Is this a regression? If yes, what likely changed?
- What data or state makes the bug appear?
- What users, roles, environments, browsers, platforms, or integrations are affected?
- What is the failure mode: incorrect result, missing result, duplicate work, crash, timeout, stale state, permissions leak, or confusing UX?
- What is the safest fix shape?
- What validation proves the bug is fixed and does not regress nearby behavior?

### Feature-Specific Questions

- Who is the primary actor?
- What workflow are they trying to complete?
- What trigger starts the workflow?
- What state changes when the workflow succeeds?
- What states are visible before, during, after, and on failure?
- What permissions or plan gates apply?
- What data needs to be created, read, updated, deleted, imported, exported, or synced?
- What notifications, audit records, webhooks, or downstream effects are expected?
- What defaults should apply?
- What should happen for empty states, partial completion, retries, cancellation, duplicate submissions, and stale data?

### Boundaries And Edge Cases

- What inputs are valid, invalid, missing, duplicated, too large, too old, or unauthorized?
- What happens when the operation is repeated?
- What happens when two users or jobs act on the same resource?
- What happens during network failure, timeout, third-party failure, process restart, or partial write?
- What migration or backfill is needed for existing data?
- Does the change affect backwards compatibility for APIs, exports, saved URLs, webhooks, or SDKs?
- What rate limits, quotas, retention rules, or privacy boundaries matter?
- What should be logged or measured?

### Implementation Shape

- Which existing deep module or boundary should own the behavior?
- Is a new abstraction justified, or should the work extend an existing module?
- What contracts may change: API, schema, event, command, component props, config, job payload, permission check?
- What invariants should the implementation preserve?
- Can the decision be described without fragile file paths?
- Does the request imply a durable architectural decision? If yes, recommend an ADR follow-up instead of writing one.

### Tests

- What user-visible behavior needs test coverage?
- Which existing tests are the closest prior art?
- Should tests be unit, integration, end-to-end, contract, migration, or regression tests?
- What should not be tested because it is implementation detail?
- What fixtures or factories are needed?
- What negative cases prove the boundaries?

## Recommended Answer Policy

Use this priority order:

1. Answer with repo evidence when available.
2. Answer with explicit user request details when repo evidence is absent.
3. Use a low-risk product or engineering default and label it as an assumption.
4. Mark `Requires human input` when the answer changes product intent, business risk, compliance posture, customer commitment, or subjective UX direction.

Recommended answers should be direct. Avoid phrasing like "maybe" or "possibly" unless the PRD is explicitly recording uncertainty.

## Self-Grill Log

The final PRD should include a compact table of the important questions. Include questions that shaped scope, surfaced contradictions, justified assumptions, or require human input. Do not dump the entire question bank.

