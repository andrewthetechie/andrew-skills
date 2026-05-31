---
name: issue-decomposer
description: Decomposes PRDs, conversation context, and feature descriptions into small, implementation-ready issue drafts that can be worked from the issue alone by small or local coding LLMs. Use when the user asks to break down a PRD, convert requirements into issues, decompose a feature, or grill requirements before planning implementation work.
---

# Issue Decomposer

## Quick Start
Use this skill to turn a PRD or planning conversation into workable issue drafts. The output is decomposition only: do not create issues in an issue tracker, implement code, open pull requests, or edit project files unless the user explicitly asks for a separate follow-up task.

Start by stating:

```text
DECOMPOSER LOOP STATE: Read Source
```

If the PRD, conversation summary, or feature description is missing or empty, stop and ask for it.

## Workflow
State the current loop state before each major action:

```text
DECOMPOSER LOOP STATE: [Read Source | Grill | Summarize Decisions | Inspect Context | Decompose | Review Proposed Issues | Finalize Drafts | Complete]
```

1. **Read Source**: Identify goals, users, constraints, requirements, non-goals, and success criteria.
2. **Grill**: Ask one clarifying question at a time. Reference the source, explain why the answer matters, and suggest a default when reasonable.
3. **Summarize Decisions**: Restate resolved decisions and remaining assumptions. Get confirmation before decomposing when decisions affect scope.
4. **Inspect Context**: If a repo or code context is available, inspect local docs, file structure, tests, and nearby analogs enough to name realistic integration points.
5. **Decompose**: Break the work into small, issue-only-context drafts with dependencies, risks, expected files, tests, and validator stopping points.
6. **Review Proposed Issues**: Present the proposed issue graph and ask the user to approve it or request splits/merges before finalizing.
7. **Finalize Drafts**: Produce polished issue drafts in text form only.
8. **Complete**: Summarize issue count, dependency graph, parallel work opportunities, and unresolved items.

## Grilling Rules
Do not skip grilling. Probe vague words like "simple", "basic", "support", "integration", "works", and "end-to-end". Challenge missing acceptance criteria, undefined users, data ownership, migration needs, validation behavior, error handling, rollout, permissions, observability, and test strategy.

Ask only one question per turn during grilling. Stop asking when remaining uncertainty can be handled as explicit assumptions without making the issue drafts unsafe or misleading.

## Codebase Grounding
When a repo is available, do not decompose from requirements alone. Identify expected files using exact paths where possible. For new files, name the intended directory and filename when obvious; otherwise name the directory, naming pattern, and nearest existing analog.

Every implementation issue should include at least one expected file, directory, or path pattern. Do not use placeholders like `src/...` or "find the right file". If paths cannot be inferred, ask a clarifying question or mark the issue as blocked by context discovery.

## Issue Draft Format
Each issue draft must include:

```md
# [Concise, action-oriented title]

## User Story
As a [persona], I want [capability] so that [benefit].

## Description
[Concrete scope, required context, expected approach, integration points, and expected files or path patterns.]

## Acceptance Criteria
- [ ] [Specific, testable outcome with example input/output when useful]

## Test Expectations
- [Test type, target behavior, example inputs, and expected outputs]

## Dependencies
- Blocked by: [issue title or "None"]
- Blocks: [issue title or "None"]

## Labels
`feature|enhancement|bug|chore|docs|test`, `[area]`, `priority:[high|medium|low]`

## Estimate
[Small|Medium|Large]

## Risk
[1-5] - [blast radius, complexity, security, data, or migration reason]

## Validator Stopping Point
[Build/test/lint/check command or observable coherent state expected after this issue]
```

## Sizing Rules
Prefer many small issues over fewer broad ones. The issue should be scoped so it can be worked with only the issue as its context: include necessary local facts, file paths, APIs, snippets, examples, defaults, and test commands instead of relying on the implementer to rediscover intent from the PRD or conversation.

Split an issue when it has multiple independently testable behaviors, spans distinct layers, combines scaffolding with user-facing behavior, combines schema/data changes with consumers, has more than one validation concern, likely touches more than 3 production files, requires broad discovery, or needs phrases like "end-to-end", "full workflow", "wire through", "integration", or "across the system".

Every issue must end at a valid repository state. Do not create knowingly broken stepping-stone issues where tests, builds, migrations, or runtime assumptions are fixed only by later work.

## Review Checklist
Before finalizing drafts, show a proposed issue graph with planned order, dependencies, expected files, sizing rationale, acceptance criteria, test expectations, validator stopping point, and any issue near the size limit.

Wait for approval or requested changes before producing final drafts.

## Guardrails
- Do not create issues in an issue tracker.
- Do not implement code or edit project files as part of decomposition.
- Do not mention or depend on project-specific external tools.
- Do not skip the decision summary before decomposition.
- Do not finalize drafts before the proposed issue graph is reviewed.
- If the PRD contradicts itself, target context is unavailable, or a critical requirement cannot be defaulted safely, stop with one clarifying question.

