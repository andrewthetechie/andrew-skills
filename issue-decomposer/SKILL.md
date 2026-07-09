---
name: issue-decomposer
description: Decomposes PRDs, conversation context, and feature descriptions into small, tracer-bullet issue drafts that a context-starved coding model can implement alone. Use when the user asks to break down a PRD, convert requirements into issues, decompose a feature, or grill requirements before planning implementation work.
---

# Issue Decomposer

Turn a PRD, planning conversation, or feature description into a reviewed graph of self-contained implementation drafts. This skill drafts only: it does not create tracker issues, implement code, open pull requests, or edit project files.

Start by stating:

```text
DECOMPOSER LOOP STATE: Read Source
```

If the source is missing or empty, ask for it.

Before drafting any issue, read and apply [ISSUE_CONTRACT.md](ISSUE_CONTRACT.md). It is the single source of truth for tracer-bullet shape, issue format, codebase artifacts, wide refactors, and the final quality gate.

## Process

State the current loop state before each phase:

```text
DECOMPOSER LOOP STATE: [Read Source | Grill | Record Decisions | Ground Context | Shape Graph | Tighten Drafts | Quiz Graph | Finalize Drafts | Complete]
```

### 1. Read Source

Read the full available source, including a referenced PRD, issue, or discussion. Identify users, outcomes, constraints, non-goals, success criteria, decisions already made, and questions that would change the work.

Done when known facts, safe assumptions, and material gaps are distinct.

### 2. Grill

Resolve material ambiguity one question at a time. Quote or point to the relevant source, say why the answer changes the work, and offer a reasonable default when one exists. Probe vague promises such as "simple", "support", "integration", "works", and "end-to-end", along with ownership, migrations, permissions, errors, rollout, observability, and tests.

Ask before an answer would otherwise make the implementer choose a product or design contract: an API or data shape, default, validation or duplicate rule, environment/configuration value, migration, security behavior, error contract, file boundary, or test seam. Stop when every remaining uncertainty can be recorded as a non-misleading assumption.

### 3. Record Decisions

Create a compact decision ledger: resolved decisions, adopted defaults, rejected alternatives, explicit assumptions, and unresolved blockers. Confirm it before decomposition when it changes scope or graph shape.

Done when no draft will silently turn an unresolved product decision into an implementation detail.

### 4. Ground Context

When repository context exists, explore enough to ground the work in current reality: the relevant domain glossary and ADRs, nearby behavior and tests, file layout, real integration seams, and applicable dependency types/docs. Use the project's vocabulary in titles and drafts.

Identify any **prefactor** that makes the change easy before the change is made. A prefactor is a separate draft only when it removes a concrete obstacle to the target slices; record that obstacle and place it first.

Done when every proposed draft can cite verified facts rather than inferred contracts, or is explicitly blocked on the fact it needs.

### 5. Shape Graph

Build the work graph from **tracer-bullet** drafts. A tracer bullet is a narrow but complete, demoable or independently verifiable path through every affected layer; it is not a horizontal "backend first" or "UI first" task. Each ordinary draft must fit a fresh implementation context and leave the repository valid when it lands.

Give every draft its exact **Blocked by** edges. An edge exists only when its blocker genuinely gates the work; independent slices begin on the **frontier** and may run in parallel. Use the wide-refactor exception in `ISSUE_CONTRACT.md` when one mechanical change cannot stay green as ordinary tracer bullets.

Done when the graph has complete delivery slices, only genuine blockers, explicit parallelism, and a valid-state strategy for every node.

### 6. Tighten Drafts

Produce each draft in the required format and run the contract's context-free simulation. The implementer has only this issue: paste every required repository or dependency artifact, rather than naming a path, symbol, convention, or integration literal and expecting rediscovery.

Done when every final-gate check in `ISSUE_CONTRACT.md` passes, or the draft is explicitly blocked pending a verification step.

### 7. Quiz Graph

Present the proposed graph as a numbered list. For each draft, show its title, blockers, and end-to-end outcome. Also identify the initial frontier and every intentional exception to ordinary tracer-bullet delivery.

Ask whether the granularity is right, whether each blocking edge genuinely gates its draft, and whether any drafts should split or merge. Iterate until the user approves the graph.

### 8. Finalize Drafts

Produce polished issue drafts in dependency order, blockers first. Keep them as text; do not publish them to a tracker.

### 9. Complete

Summarize the issue count, approved dependency graph, initial frontier and parallel opportunities, delivery strategy for any wide refactor, and unresolved blockers.

## Hard Constraints

- The decision ledger precedes graph shaping, and graph approval precedes final drafts.
- Final drafts use the full issue contract; a reference is not a substitute for the artifact an implementer must use.
- Verified repository and dependency contracts are facts. Unknown contracts are visible verification blockers, never invented literals.
- Drafts default to an independently valid repository state. The only exception is the explicit, staged wide-refactor strategy in the issue contract.

