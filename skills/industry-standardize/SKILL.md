---
name: industry-standardize
description: Use when asked to industry-standardize a plan, architecture, or implementation, or to replace homegrown machinery with established components.
---

# Industry-standardize

Assume prior art exists for the problem class. Treat each complicated custom mechanism as a **suspect**. Compare each suspect with established options. Require every replacement to satisfy the actual contract.

## Method

1. **Book the suspects.** Trace custom mechanisms through their callers or dependent plan steps.
   Include data structures, algorithms, protocols, persistence, state machines, schedulers, retries, and coordination.
   Weight scrutiny by complexity. For each suspect, separate required behavior from the chosen design and name the problem class.
   Record invariants, compatibility, failure behavior, and relevant workload, performance, concurrency, durability, security, and operating constraints.
   Cite evidence for each constraint or mark it unknown.
   **Done when you name every material suspect and path and separate each contract from its design.**

2. **Inventory prior art.** Search existing project mechanisms and dependencies first.
   Then inspect standard library and platform features, framework facilities, and established algorithms, protocols, libraries, or services.
   Include the current design as a candidate.
   Read authoritative documentation or project evidence to establish each plausible option's contract and, where relevant, maintenance status.
   Mark unverified claims explicitly.
   **Done when each plausible option has a source and contract, or a named verification gap.**

3. **Compare fit and reach a verdict.** Compare candidates against relevant constraints.
   Cover reachable work, memory, I/O, failure and recovery, concurrency, security, interoperability, operating cost, compatibility, and migration.
   Accept simple bounded work when larger systems lack a material advantage.
   Passing tests establish behavior only under tested conditions.
   Classify each claim as a **demonstrated issue**, **credible concern**, or **open question**.
   An issue needs reachable harm, a measurement, or a violated requirement.
   A concern has a concrete mechanism but lacks a material runtime fact.
   An open question could change the verdict.
   **Replace** when evidence shows an established option preserves behavior and improves material complexity or cost.
   **Retain** when no alternative has a demonstrated material advantage.
   Use **Verify** for concerns and open questions that could change the choice.
   Name the least costly way to resolve them.
   **Done when every suspect has a supported verdict based on current requirements.**

4. **Carry out the verdict.** For assessments, report each verdict, evidence, source, location, behavior difference, and verification need.
   Rank replacement proposals by impact and confidence.
   For requested changes, revise the plan or code and remove superseded machinery.
   Update affected callers and tests.
   Use focused tests or other evidence to establish preserved behavior.
   For plans, specify migration and validation steps.
   **Done when requested changes are complete and all uncertainty that could change a verdict is visible.**

