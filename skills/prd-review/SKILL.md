---
name: prd-review
description: Reviews a PRD or technical proposal against the actual repository, fact-checking claims and evaluating proposed architecture against existing code, domain context, and ADRs. Use when the user asks to review, audit, validate, fact-check, or sanity-check a PRD/spec/proposal before implementation.
---

# PRD Review

Review a PRD as an evidence-based design critique. The goal is to catch false assumptions, outdated descriptions, missing constraints, and architecture proposals that do not fit the repo.

## Quick Start

Start by stating:

```text
PRD REVIEW STATE: Read PRD
```

If the PRD path or text is missing, ask for it. Do not implement code, create issues, edit docs, or rewrite the PRD unless the user explicitly asks for a separate follow-up task.

## Workflow

State the current loop state before each major action:

```text
PRD REVIEW STATE: [Read PRD | Extract Claims | Inspect Repo Context | Verify Claims | Evaluate Architecture | Report]
```

1. **Read PRD**: Identify goals, requirements, non-goals, proposed architecture, success criteria, rollout/migration notes, and explicit assumptions.
2. **Extract Claims**: Convert the PRD into checkable claims. Include claims about current behavior, file/module names, APIs, data models, dependencies, tests, constraints, conventions, performance, security, and migration state.
3. **Inspect Repo Context**: Read repo guidance and architecture sources before judging the PRD. Prefer `AGENTS.md`, `CLAUDE.md`, `README*`, `CONTEXT.md`, `CONTEXT-MAP.md`, `docs/adr/`, `docs/agents/`, package/build manifests, tests, and nearby implementation analogs. If `CONTEXT-MAP.md` exists, inspect only the relevant context docs and ADRs.
4. **Verify Claims**: Check each material PRD claim against code and docs. Use exact file paths and line references when possible. Classify claims as `Verified`, `Contradicted`, `Unsupported`, `Ambiguous`, or `Outdated/Risky`.
5. **Evaluate Architecture**: Judge the proposed design against existing domain language, ADRs, module seams, adapters, data ownership, test surfaces, operational constraints, and local patterns. Distinguish evidence from inference.
6. **Report**: Present a full claim-by-claim matrix, then findings ordered by severity. Findings are the primary output; summaries are secondary.

## Claim Review Rules

Treat PRD claims as suspect until verified. Do not rely on naming alone; inspect call sites, tests, schemas, configuration, and runtime wiring when they affect the claim.

Use this classification consistently:

- `Verified`: The code/docs clearly support the claim.
- `Contradicted`: The code/docs show the claim is false or materially incomplete.
- `Unsupported`: No evidence was found after checking the likely sources.
- `Ambiguous`: Evidence points in multiple directions, or the PRD uses overloaded terminology.
- `Outdated/Risky`: The claim may be partly true but depends on stale patterns, deprecated paths, TODOs, fragile assumptions, or untested behavior.

Every material claim must appear in the claim matrix, including verified claims. Keep each row concise: one claim, one classification, strongest evidence, and review implication.

## Architecture Review Rules

Challenge the PRD against the repository's actual language and decisions:

- If the PRD uses a term that conflicts with `CONTEXT.md`, call out the mismatch and cite both meanings.
- If the proposed architecture contradicts an ADR, cite the ADR and explain whether the PRD must change or the ADR should be deliberately revisited.
- If the PRD introduces a new seam, interface, adapter, service, table, queue, or job, check whether nearby analogs already exist and whether the proposed shape follows or fights them.
- If the design crosses ownership boundaries, identify the owning module/context and the data flow that would be affected.
- If tests or validation are underspecified, name the existing test layer or command pattern that should cover the proposal.

Prefer concrete repo-fit critique over abstract architecture advice. Mark speculation explicitly.

## Report Format

Use this structure:

```md
## Claim Matrix
| # | PRD Claim | Classification | Evidence | Review Implication |
|---|-----------|----------------|----------|--------------------|
| 1 | [specific claim] | [Verified/Contradicted/Unsupported/Ambiguous/Outdated/Risky] | [path:line or "Not found in likely sources"] | [what this means for the PRD] |

## Findings
- [Severity] [Classification] [PRD section/claim] - [problem]
  Evidence: [repo path:line or doc path:line]
  Impact: [why the PRD would mislead implementation]
  Recommendation: [specific PRD correction or design adjustment]

## Architecture Fit
[Short assessment of how well the proposal matches current domain language, ADRs, seams, data ownership, and test surfaces.]

## Verified Anchors
- [Important verified claims that reduce uncertainty or constrain the architecture.]

## Open Questions
- [Questions that cannot be answered from the repo and materially affect the PRD.]
```

Severity order: `Critical`, `High`, `Medium`, `Low`. A `Critical` finding means the PRD would likely send implementation in the wrong direction. A `High` finding means a major requirement, data model, or architecture assumption is wrong or unsupported.

The `Claim Matrix` is mandatory. If the PRD is large, group claims by PRD section and keep wording compact, but do not omit material claims just because they are verified.

## Guardrails

- Do not mutate project files during PRD review.
- Do not ask questions until repository evidence has been checked, unless the PRD itself is unavailable.
- Do not invent codebase facts; say `Unsupported` or `Ambiguous`.
- Do not rubber-stamp architecture because it is plausible; require repo evidence.
- Do not decompose into issues unless the user asks for issue planning after the review.

