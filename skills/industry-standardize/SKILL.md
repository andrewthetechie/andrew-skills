---
name: industry-standardize
description: Review proposals and code changes for custom mechanisms replaceable by established standards, algorithms, data structures, or existing platform facilities. Use for industry-standardize reviews or requests to find reinvented machinery.
---

# Industry-standardize

Find concrete substitutions that remove custom machinery or satisfy a required external contract.
A useful finding names the existing mechanism, its replacement, and the resulting edit.
The replacement can be a formal standard, an established computer science technique, or an existing implementation.
Call each one what it is. An algorithm needs neither an RFC nor a new dependency to qualify.

Default to review. Apply changes when the user requests them.

## 1. Locate the custom mechanisms

Read the supplied proposal or diff completely. For code changes, inspect the affected callers, tests, dependencies, and contracts as needed.
For proposals, distinguish explicit design choices from details the document leaves unspecified.

Record each mechanism's location, required behavior, and constraints that could rule out a replacement.
Include relevant scale, ordering, failure behavior, compatibility, and deployment restrictions. Mark missing facts as unknown.
Express the problem independently of its implementation, such as dependency ordering, duplicate suppression, or interval lookup.

Keep this inventory as working notes. Review the mechanisms within the requested scope, including algorithms hidden inside otherwise ordinary application code.
Treat domain policy and simple glue as possible reasons to retain code.
An omitted feature becomes relevant only when it prevents a specific replacement or violates an explicit requirement.

Finish when every in-scope custom mechanism has a location, a problem statement, and the constraints needed to compare alternatives.

## 2. Find a specific replacement

Start with facilities the project already has, then the language runtime and platform.
Search by the problem statement when no suitable option is apparent.
Consider established algorithms and data structures as well as protocols, formats, packages, and services.
Prefer the smallest option that meets the constraints. A familiar technology name alone establishes no fit.

Read primary sources for plausible candidates: specifications, official documentation, implementation source, or original algorithm publications.
Verify the relevant version, behavior, and limitations. For new dependencies, verify maintenance status and license constraints.
Cite the exact section or API that supports the replacement, using sources inspected during this review.
Use available search and retrieval tools. If source access fails, mark the affected claim unverified.

Finish each comparison when one replacement has a supported contract, or the plausible alternatives fail named constraints.
If verification remains blocked, record the source gap that prevents comparison.
Research further alternatives only when they could change the recommendation.

## 3. Prove the substitution

Promote a candidate to a finding only when all of these are concrete:

- **Location and mechanism.** Cite a file and symbol, diff hunk, or proposal section. Describe the custom work it performs.
- **Replacement.** Name the specific algorithm, API, library facility, or standard provision, with supporting evidence.
- **Edit.** State what code or proposed machinery disappears, what takes its place, and what domain logic remains.
- **Fit.** Map the replacement to the required behavior. Address relevant semantic differences and migration costs.
- **Payoff.** Show a specific correctness, complexity, maintenance, or interoperability benefit that justifies the change.
- **Validation.** Name a focused check that distinguishes a correct substitution from a behavior regression.

For an algorithm, connect its operations and preconditions to this workload. Distinguish asymptotic improvements from measured performance.
For a standard, identify the consumer or requirement that needs its semantics.
For a library or service, count the configuration, adapters, dependencies, and operations it adds against the machinery it removes.
Preserve required behavior and identify intentional corrections to defective behavior.

Retain custom code when benefits are only stylistic, existing facilities already handle the problem, or replacements add unjustified machinery.
If a missing fact could reverse the decision, state the conditional replacement and the smallest check needed.
Keep such candidates separate from supported findings. Omit speculative candidates that lack a concrete replacement or payoff.

Finish when every inventoried mechanism has a supported substitution, a reason to retain it, or a decision-changing verification gap.

## 4. Report actionable findings

Lead with the strongest findings. Rank them by concrete benefit and evidence. Combine findings that require the same edit.
Title each finding with the mechanism, specific replacement, and location.
Cover the remaining evidence from step 3 in compact prose, with citations beside the claims they support.

Use a short code or before/after sketch when it makes the edit clearer.
For a proposal, make the replacement precise enough to rewrite the affected section.
For conformance changes, name the exact fields, operations, or semantics to change.

Report only findings that pass step 3, plus unresolved checks that could change a concrete recommendation.
There is no finding quota. When none qualify, say so and briefly explain the relevant constraints.
Keep the full inventory internal unless the user requests coverage details.

When the user requests edits, implement the supported substitutions and remove superseded machinery.
Update affected callers and perform focused validation. For proposals, specify migration and acceptance checks instead.

Finish when each finding can become a bounded edit without another architecture investigation.

## Calibration

- Repeated dependency scans can become a topological sort when the graph and required ordering permit it.
  Identify the replacement routine, cycle behavior, and scan logic removed.
- A cross-process duplicate check can become a database uniqueness constraint plus a conflict-safe operation.
  Specify the unique key, conflict behavior, and existing-data migration.
- A fixed dispatch table may already express the domain policy directly.
  Retain it when a framework adds machinery without removing a real burden.

When changing this skill, use [the review cases](references/review-cases.md) to check specific replacements and justified no-finding outcomes.

