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
DECOMPOSER LOOP STATE: [Read Source | Grill | Summarize Decisions | Inspect Context | Decompose | Tighten Drafts | Review Proposed Issues | Finalize Drafts | Complete]
```

1. **Read Source**: Identify goals, users, constraints, requirements, non-goals, and success criteria.
2. **Grill**: Ask one clarifying question at a time. Reference the source, explain why the answer matters, and suggest a default when reasonable.
3. **Summarize Decisions**: Restate resolved decisions, accepted defaults, rejected alternatives, and remaining assumptions. Get confirmation before decomposing when decisions affect scope.
4. **Inspect Context**: If a repo or code context is available, inspect local docs, file structure, tests, and nearby analogs enough to name realistic integration points.
5. **Decompose**: Break the work into small, issue-only-context drafts with dependencies, risks, expected files, tests, and validator stopping points.
6. **Tighten Drafts**: Rewrite every draft until it contains enough local context and explicit contracts for a smaller model to implement it without reading the PRD or making product/design decisions. Run the context-free reread: read each issue as an implementer who has ONLY this issue text (no PRD, no conversation, no ability to browse beyond what the issue quotes). List every symbol, type, signature, integration contract, or literal value the issue NAMES but does not SHOW. Each such item must be pasted in (or the issue marked blocked pending verification) before the draft is done. You hold the hidden context, so you cannot feel this gap unless you deliberately simulate the starved reader.
7. **Review Proposed Issues**: Present the proposed issue graph and ask the user to approve it or request splits/merges before finalizing.
8. **Finalize Drafts**: Produce polished issue drafts in text form only.
9. **Complete**: Summarize issue count, dependency graph, parallel work opportunities, and unresolved items.

## Grilling Rules
Do not skip grilling. Probe vague words like "simple", "basic", "support", "integration", "works", and "end-to-end". Challenge missing acceptance criteria, undefined users, data ownership, migration needs, validation behavior, error handling, rollout, permissions, observability, and test strategy.

Ask only one question per turn during grilling. Stop asking when remaining uncertainty can be handled as explicit assumptions without making the issue drafts unsafe or misleading.

Ask before decomposing when the answer would otherwise force an implementer to choose an API shape, data model, file layout, environment variable, default value, validation rule, duplicate-handling rule, error contract, secret-handling behavior, migration behavior, or test seam.

## Codebase Grounding
When a repo is available, do not decompose from requirements alone. Identify expected files using exact paths where possible. For new files, name the intended directory and filename when obvious; otherwise name the directory, naming pattern, and nearest existing analog.

Every implementation issue should include at least one expected file, directory, or path pattern. Do not use placeholders like `src/...` or "find the right file". If paths cannot be inferred, ask a clarifying question or mark the issue as blocked by context discovery.

### Paste artifacts, do not point at them
A path or a symbol name is a pointer, not specificity. If an issue references an existing symbol, type, function, event/message contract, config key, enum, error shape, or call site, you MUST open the defining source and paste the real signature, type definition, return shape, or exact excerpt into the issue. A smaller model cannot guess a signature correctly from its name; when you only name it, the implementer invents a shape and gets it wrong. Quote the nearest analog you tell the implementer to copy, do not just cite it.

### Ground in dependencies, not just the repo
Grounding extends to third-party and dependency APIs the work integrates with (package types, SDK option names, stream/event field names, callback shapes), not only first-party files. The riskiest contract is usually the external integration seam. Open the installed package's types/docs and paste the verified shape.

### Never state an unverified value as fact
Do not write a concrete literal you have not verified against source as if it were known: event-type strings, option/parameter keys, enum values, route paths, env var names, and field names are the common offenders. A confidently wrong value is worse than an open question, because the implementer will faithfully build the wrong thing and fail silently. For any contract you cannot verify against real source, mark the issue blocked pending a verification spike (or add a tiny "verify the real contract first" step inside the issue) instead of inventing a value.

## Required Issue Contract
Before decomposing, read and apply [ISSUE_CONTRACT.md](ISSUE_CONTRACT.md). It defines the mandatory issue format, small-model handoff standard, and tightening quality gate. Do not skip it, and do not finalize drafts until every issue passes that gate.

## Issue Draft Format
Each issue draft must follow the full format in [ISSUE_CONTRACT.md](ISSUE_CONTRACT.md). The required sections are: User Story, Description, Context Pack, Implementation Contract, Acceptance Criteria, Test Expectations, Dependencies, Labels, Estimate, Risk, and Validator Stopping Point.

## Sizing Rules
Prefer many small issues over fewer broad ones. The issue should be scoped so it can be worked with only the issue as its context: include necessary local facts, file paths, APIs, snippets, examples, defaults, and test commands instead of relying on the implementer to rediscover intent from the PRD or conversation.

Split an issue when it has multiple independently testable behaviors, spans distinct layers, combines scaffolding with user-facing behavior, combines schema/data changes with consumers, has more than one validation concern, likely touches more than 3 production files, requires broad discovery, or needs phrases like "end-to-end", "full workflow", "wire through", "integration", or "across the system".

Every issue must end at a valid repository state. Do not create knowingly broken stepping-stone issues where tests, builds, migrations, or runtime assumptions are fixed only by later work.

## Review Checklist
Before finalizing drafts, show a proposed issue graph with planned order, dependencies, expected files, critical contracts, sizing rationale, acceptance criteria, test expectations, validator stopping point, and any issue near the size limit.

Wait for approval or requested changes before producing final drafts.

## Red Flags - Stop and Tighten
These mean an issue is "named but not shown" and will produce wrong implementations:

- References a function, type, hook, or class by name without pasting its real signature/return shape.
- States an integration literal (event name, option/param key, enum value, route, env var, field name) you did not verify against source.
- Says "matching the existing pattern", "see X", or "copy the convention in Y" instead of quoting the actual excerpt to copy.
- Touches a dependency/SDK seam but quotes only repo files, never the package's real API.
- Uses "assume", "should be", "likely", or "to be confirmed" for a contract the implementer needs to compile or integrate.
- The Implementation Contract restates the PRD in prose instead of pasting concrete artifacts.
- Adds a `continue`, `break`, early return, or branch but does not paste the enclosing control-flow skeleton (the loop, try/catch, or function) it must land in, so the implementer cannot know where the edit goes.
- Consumes a symbol delivered by a sibling or not-yet-merged issue without giving its exact import path and where it comes from.

When you hit one, paste the real artifact or mark the issue blocked pending verification. Do not finalize.

## Guardrails
- Do not create issues in an issue tracker.
- Do not implement code or edit project files as part of decomposition.
- Do not mention or depend on project-specific external tools.
- Do not skip the decision summary before decomposition.
- Do not finalize drafts before the proposed issue graph is reviewed.
- If the PRD contradicts itself, target context is unavailable, or a critical requirement cannot be defaulted safely, stop with one clarifying question.
