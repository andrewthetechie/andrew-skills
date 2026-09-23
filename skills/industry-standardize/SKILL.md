---
name: industry-standardize
description: Use when asked to industry-standardize a plan, architecture, or implementation, or to find homegrown machinery that should become standard components.
---

# Industry-standardize

Assume the problem is already solved elsewhere. Every complicated bespoke mechanism in scope is a **suspect** that must earn its keep against a named standard.

## Method

1. **Book the suspects.** Within the requested scope, trace custom data structures, algorithms, protocols, persistence, state machines, schedulers, retry logic, and coordination through their callers or dependent plan steps. Write the suspect list out explicitly. For each, record the problem it solves and its observable **contract**: invariants, failure behavior, scale, performance, and operational constraints. Weight scrutiny by complexity carried.
2. **Name the standard.** Search the language's standard library first, then existing project dependencies and platform features, then mature ecosystem libraries or services. Read authoritative documentation to confirm the candidate exists, is maintained, and holds the semantics you are about to claim for it. Name the specific primitive, library, protocol, or system.
3. **Reach a verdict.** Compare the candidate against the recorded contract: edge cases, concurrency, durability, security, interoperability, migration cost. **Replace** when the candidate preserves the contract and deletes more complexity than it introduces. **Acquit** when a requirement you can point to demands the bespoke design. Evidence is documented semantics; popularity and familiarity are not evidence.
4. **Carry out the verdict.** When the user asked for a change, revise the plan or implementation to use the chosen standard, remove the superseded machinery, and update affected callers and tests. For a plan, specify migration and verification steps. For code, verify behavior with focused tests or other appropriate checks. When the user asked for an assessment, deliver actionable replacement proposals instead.

## Completion bar

Every suspect on the list carries a verdict, with the concrete standard named or the requirement that acquits it. State every behavior difference a replacement introduces. Rank replacements by complexity removed and confidence. Cite the plan section or code location, and mark which claims are verified against documentation and which are assumptions.

