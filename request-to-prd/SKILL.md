---
name: request-to-prd
description: Turns a rough bug report or feature request into a self-contained, self-grilled first-draft PRD using repo docs, code exploration, recommended answers, and explicit human-only unknowns. Use when the user provides one or more paragraphs of product, bug, or feature text and asks for a PRD, first draft, self-grill, non-interactive design pass, or spec from a rough request.
---

# Request To PRD

## Core Rule

This skill is self-contained. Do not invoke or assume availability of `grill-with-docs`, `/to-prd`, `to-prd`, or setup skills. Recreate the needed behavior from this skill's files.

## Required Reads

Before drafting, read:

- [SELF-GRILL.md](SELF-GRILL.md) for the non-interactive grilling process and question bank.
- [PRD-TEMPLATE.md](PRD-TEMPLATE.md) for the output format, bug/feature variants, and publishing rules.

Read [EXAMPLES.md](EXAMPLES.md) only if the expected output shape is unclear.

## Quick Start

Given a paragraph or more describing a bug report or feature request, perform a non-interactive grilling pass, answer each question with the best evidence-backed or recommended answer, and produce a first-draft PRD. Do not ask the user questions during the first pass unless the source request is missing or unreadable.

## Workflow

1. **Intake the request**
   - Classify it as `bug`, `feature`, or `mixed`.
   - Extract stated problem, desired outcome, actors, examples, constraints, urgency, and explicit non-goals.
   - Preserve ambiguity; do not silently convert uncertainty into fact.

2. **Discover repo context**
   - Read relevant root guidance such as `AGENTS.md`, `CLAUDE.md`, `CONTEXT-MAP.md`, `CONTEXT.md`, and `docs/adr/` when present.
   - If `CONTEXT-MAP.md` exists, identify the relevant bounded context before reading glossary or ADR files.
   - Search code and tests for named concepts, UI text, APIs, commands, errors, workflows, and modules from the request.
   - Use existing domain vocabulary. If the request conflicts with the glossary or code, call out the conflict in the PRD.

3. **Self-grill the request**
   - Follow [SELF-GRILL.md](SELF-GRILL.md).
   - Answer from code/docs where possible.
   - Use recommended assumptions only when they are defensible.
   - Mark human-only unknowns as `Requires human input`.

4. **Draft the PRD**
   - Follow [PRD-TEMPLATE.md](PRD-TEMPLATE.md).
   - Draft for refinement, not final approval.
   - Include enough implementation shape for an engineer to reason about scope.
   - Separate facts, assumptions, contradictions, and human-only unknowns.

5. **Handle documentation and publishing**
   - Do not update `CONTEXT.md` or ADRs in this automated pass. Recommend doc follow-ups instead.
   - If the user explicitly asks to publish the PRD, discover the repo's issue tracker workflow and publish there.
   - Apply `ready-for-agent` only if that label vocabulary is documented.
   - If publishing is not requested or not discoverable, return the PRD draft directly.

## Quality Bar

- Bugs include expected vs. actual behavior, reproduction or detection signals when available, suspected affected area, regression risk, and fix validation.
- Features include actors, core workflows, edge cases, acceptance criteria, and non-goals.
- The recommended answer is concrete when repo evidence or a defensible default exists.
- Human-only unknowns are explicit and are not answered by invention.
- If no relevant repo docs exist, say that and proceed from code and request evidence.

