# PRD Template And Output Rules

## Output Contract

Return a first-draft PRD unless the user explicitly asked to publish it. The PRD should be detailed enough to drive follow-up questioning and implementation planning, but not presented as approved final product direction.

Avoid fragile file paths and code snippets unless a compact type, state machine, reducer, schema, or API shape records a decision more precisely than prose.

## Standard PRD

```md
# <PRD title>

## Intake Summary
Type: <bug | feature | mixed>
Source request: <brief neutral summary>
Evidence reviewed: <docs/code/tests/issues searched or "No relevant repo docs found">

## Problem Statement
<Problem from the user's perspective, using repo vocabulary and noting conflicts.>

## Proposed Solution
<Recommended product behavior and technical shape at PRD level.>

## Goals
- <Outcome the work should achieve>

## Out Of Scope
- <Explicit or recommended exclusions>

## User Stories
1. As a <actor>, I want <capability>, so that <benefit>.

## Functional Requirements
- <Observable behavior, acceptance criteria, and edge cases.>

## Implementation Decisions
- <Modules or contracts likely affected, schema/API/UI behavior, compatibility, rollout, and observability.>

## Testing Decisions
- <Behavior-focused test strategy, modules to test, and similar existing test patterns when found.>

## Assumptions
- <Assumption> - Basis: <code/docs/default reasoning>. Confidence: <high | medium | low>.

## Contradictions Or Vocabulary Conflicts
- <Conflict> - Recommended interpretation: <interpretation>.

## Open Questions Requiring Human Input
- <Question> - Why human input is required: <specific reason>.

## Self-Grill Resolution Log
| Question | Recommended answer | Basis | Confidence |
| --- | --- | --- | --- |
| <Key question> | <Answer or "Requires human input"> | <Evidence or reason> | <high/medium/low/human> |

## Proposed Documentation Follow-Ups
- <Glossary terms or ADR candidates to confirm before writing durable docs.>
```

Omit `Contradictions Or Vocabulary Conflicts` only when there are no conflicts. Omit `Proposed Documentation Follow-Ups` only when there are no glossary or ADR candidates.

## Bug Variant Requirements

For bugs, ensure the PRD includes:

- Expected behavior.
- Actual behavior.
- Reproduction steps, detection signals, or a clear note that reproduction is unavailable.
- Affected users, roles, environments, or data states when knowable.
- Suspected owning area at module or boundary level.
- Regression risk and nearby behaviors that must keep working.
- Fix validation and regression test expectations.
- Operational concerns such as data repair, rollback, monitoring, or customer communication when relevant.

Use this functional-requirement shape when useful:

```md
## Functional Requirements
- Given <state>, when <action/event>, then <expected observable behavior>.
- The system must not <regression or unsafe behavior>.
- Existing <workflow/API/data> must continue to <compatibility expectation>.
```

## Feature Variant Requirements

For features, ensure the PRD includes:

- Primary and secondary actors.
- Core happy path.
- Empty, loading, failure, unauthorized, duplicate, stale, and partial-completion states when relevant.
- Permissions, plan gates, auditability, notifications, webhooks, or downstream effects.
- Data lifecycle: create, read, update, delete, import, export, sync, retention.
- Rollout or migration needs for existing users.
- Acceptance criteria for the smallest coherent launch.

Use this user-story shape:

```md
1. As a <primary actor>, I want <core workflow>, so that <user-visible benefit>.
2. As a <secondary actor/system>, I want <supporting behavior>, so that <operational or user benefit>.
```

## Implementation Decisions

Keep implementation detail at the PRD level. Prefer boundaries and contracts over file paths.

Good:

- The existing invitation lifecycle should own resend and expiry behavior.
- The API should return a stable validation error when the requested transition is invalid.
- A migration should backfill missing status values before enforcing the new invariant.

Avoid:

- Edit `src/foo/bar/baz.ts` to add three `if` statements.
- Copy the existing modal and tweak CSS.
- Introduce a new service without explaining the boundary it owns.

## Testing Decisions

Tests should focus on observable behavior and contracts.

Include:

- The highest-value regression tests.
- Existing prior-art tests or fixture patterns when found.
- Negative cases for invalid input, permissions, retries, and stale state.
- Migration or compatibility tests when data or API contracts change.

Avoid:

- Snapshot-heavy tests that only lock incidental markup.
- Tests that assert private helper behavior without user-visible value.
- Broad end-to-end coverage when a narrower contract test proves the behavior.

## Publishing Rules

Only publish when the user explicitly asks to publish, create an issue, or add the PRD to the tracker.

Before publishing:

- Discover the issue tracker from repo docs, config, or existing issue templates.
- Preserve the PRD body exactly enough that future agents can work from it.
- Apply labels only when the repo documents the label vocabulary.
- Apply `ready-for-agent` only when documented.
- If publishing is requested but the tracker is not discoverable, return the PRD and state what is missing.

Do not run setup skills or assume a tracker convention.

