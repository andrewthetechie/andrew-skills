---
name: issue-improver
description: Ratchet bug reports and feature requests toward implementation readiness by reproducing behavior, verifying claims, and editing in repository evidence, concrete contracts, acceptance criteria, and validation. Use when an issue is vague, stale, unverified, missing code references, or needs improvement instead of a readiness verdict.
---

# Issue Improver

Ratchet one existing issue toward implementation readiness. Preserve the reporter's intent, replace uncertainty with evidence, and make the largest safe improvement the available context supports. A useful partial improvement is a successful run.

Start by stating:

```text
ISSUE IMPROVER STATE: Resolve Input
```

If the issue is missing or empty, ask for the issue text, path, URL, or tracker identifier.

Before changing the issue, read [`../issue-reviewer/REVIEW_CHECKLIST.md`](../issue-reviewer/REVIEW_CHECKLIST.md). It is the single source of truth for the ideal handoff state. Treat its unmet checks as improvement opportunities; reserve `PASS` for an issue that actually satisfies the full checklist.

## Mutation Contract

Scope mutations to the supplied issue's title and body. Keep repository files and all other tracker state read-only unless the user separately expands the task. When the source issue cannot be edited, return copy-paste-ready Markdown.

Preserve original logs, screenshots, reproduction details, and reporter observations. Distinguish them from diagnoses, proposed solutions, and newly verified facts.

## Process

State the current phase before each major action:

```text
ISSUE IMPROVER STATE: [Resolve Input | Baseline | Investigate | Rewrite | Apply | Complete]
```

### 1. Resolve Input

Resolve a pasted issue, local file, URL, or tracker identifier into its complete title, body, and relevant discussion. Locate the target repository and any linked source document when available. Capture the original title and body before editing, and determine whether the result can be written back or must be returned as Markdown.

Complete when the issue text, destination, repository availability, and source-document availability are explicit.

### 2. Baseline

Read the issue on its own. Separate:

- observed behavior or requested outcome;
- expected behavior and impact;
- reproduction steps, environment, and verification status;
- stated facts, hypotheses, and proposed solutions;
- scope, non-goals, acceptance criteria, and validation; and
- named code or dependency contracts that are not shown.

Choose improvements in this order: correct contradicted claims; establish verification status; add repository evidence; make contracts and scope concrete; add acceptance and test detail; then polish structure and title.

Complete when the original intent is stated in one sentence and every material gap has a priority.

### 3. Investigate

Build a compact evidence ledger for every material claim that may enter the revised issue: `Verified`, `Contradicted`, `Unsupported`, `Ambiguous`, or `Outdated/Risky`, with its source.

For a bug report:

- Derive the smallest safe reproduction from the report, nearby tests, and current behavior.
- Run the narrowest existing command or disposable probe that can verify it. Record the exact command, relevant environment, observed output, and status: `Reproduced`, `Not reproduced`, or `Unverified` with the reason.
- Trace the observed path to the smallest relevant code seam and its tests.

For a feature request or chore:

- Trace the current behavior and the nearest analogous end-to-end path.
- Identify the concrete integration seam, constraints, existing conventions, and decisions still owned by the requester.
- Confirm whether the requested outcome fits one bounded issue; record a decomposition need when it contains independent outcomes.

For every branch, open the real definitions, call sites, tests, configuration, and installed dependency types that support a claim. Cite repository evidence as `path:line` and paste the smallest exact signature, type, literal, or excerpt an implementer must rely on. Use primary documentation when a required external contract is absent locally.

Use local, read-only, and disposable verification. When meaningful verification requires production access, destructive state, secrets, or interaction with external users, record the safe setup needed and leave the claim `Unverified`.

Complete when every newly added technical fact has evidence and every material verification attempt has a result or a concrete reason it could not run.

### 4. Rewrite

Follow the repository's issue template when one exists and add any evidence-bearing sections it lacks from this set. Without a template, add only the sections that carry useful information:

- Summary or outcome
- Actual and expected behavior
- Reproduction and verification status
- Technical context and code references
- Implementation contract: expected files, exact interfaces, behavior, errors, and security constraints
- Scope and non-goals
- Acceptance criteria
- Test expectations and validator stopping point
- Open questions

Write verified facts as facts, label hypotheses, and expose unsupported contracts as open questions or verification work. Correct contradicted claims rather than preserving confident misinformation. Keep acceptance criteria observable and tie them to the evidence-backed behavior. Improve the title when a more specific title preserves the original intent.

Complete when the revised issue closes at least one material gap, introduces zero unsupported facts, and remains faithful to the original request.

### 5. Apply

Write the revised title and body back to the supplied tracker issue or local issue file when write access exists; otherwise return the complete revised Markdown. Re-read the persisted issue after an update and confirm the intended text is present.

Compare the result with the original and the issue-review checklist. Report:

- what changed;
- bug verification status or current-behavior evidence;
- code and source references added;
- remaining gaps and why they remain; and
- whether the issue is incrementally improved or fully handoff-ready.

Complete when the revised issue is persisted or returned in full and every claimed improvement is visible in the final text.

### 6. Complete

State:

```text
ISSUE IMPROVER STATE: Complete
```

Link the updated issue when possible. Keep unresolved questions in the issue itself so the next person does not need this conversation.

## Hard Rules

- Treat evidence quality as more important than section count.
- Preserve uncertainty explicitly; `Not reproduced` means the attempted conditions did not reproduce the report, not that the report is false.
- Prefer exact artifacts over pointers: show the signature, type, literal, control-flow excerpt, or dependency shape that the issue names.
- Limit the run to issue improvement. Investigation supports the issue edit; implementation belongs in a separate task.

