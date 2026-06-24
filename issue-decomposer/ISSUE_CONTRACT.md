# Issue Contract

Use this reference whenever the skill drafts or reviews issues. The goal is a self-contained handoff that a smaller coding model can implement without the PRD, conversation, or hidden project knowledge.

## Small-Model Handoff Standard
Each issue must answer these questions directly:

- What exact goal should be implemented, and what is explicitly out of scope?
- Which source decisions, accepted defaults, and assumptions does the issue rely on?
- Which exact files, new paths, or path patterns should be touched?
- Which nearby existing files, tests, or naming conventions should be copied?
- Which public names are required: functions, types, DTOs, routes, commands, config keys, environment variables, events, labels, or metrics?
- What data shape is required: fields, required/optional status, defaults, parsing, validation, duplicate rules, and example values?
- What errors or failure modes are required: message text, error type, status code, fallback, or observable behavior?
- What security or data-handling behavior is required for credentials, tokens, secrets, logs, and status output?
- Where should tests live, what should be faked or mocked, and which concrete input/output proves behavior?
- What command or observable state proves this issue is complete and the repository is valid?

Do not leave final issues with phrases like "decide", "choose appropriate", "wire through", "integrate with", "handle errors", "add validation", "add tests", "etc.", or "as needed" unless the same sentence immediately defines the exact contract.

### Paste real artifacts, not pointers
Naming a symbol is not specifying it. A smaller model cannot reconstruct a signature, type, return shape, event contract, or option set from a name; it will invent one and be wrong. Therefore:

- For every existing symbol the issue depends on (function, type, DTO, hook, enum, config key, event/message shape, error shape, call site), paste the real signature or type definition copied from source, not a paraphrase.
- For every dependency/SDK integration seam, paste the verified API shape from the installed package's types or docs (option keys, callback signature, event field names).
- Never present an unverified literal as fact (event-type strings, option/param keys, enum values, routes, env vars, field names). If you have not opened the source that defines it, either verify and quote it, or mark the issue blocked pending a verification step. A confidently wrong literal makes the implementer build the wrong thing and fail silently — worse than an open question.
- When you tell the implementer to copy an existing pattern, quote the actual excerpt to copy, do not cite it by path alone.

## Required Issue Format
Each final issue must use this structure:

```md
# [Concise, action-oriented title]

## User Story
As a [persona], I want [capability] so that [benefit].

## Description
[Concrete scope, required context, expected approach, integration points, and expected files or path patterns.]

## Context Pack
- Source decisions: [decisions/defaults from the PRD or grilling that this issue relies on]
- Repo facts: [paths, existing analogs, current behavior, naming conventions]
- Non-goals: [explicit exclusions to prevent scope drift]

## Implementation Contract
- Expected files: [exact paths, intended new paths, or precise path patterns]
- Interfaces and names: [paste the real or target signature/type for each, copied from source — not just the name. e.g. `function foo(x: Bar): Promise<Baz>` plus the `Bar`/`Baz` definitions the implementer must satisfy. Use "None" only if truly none.]
- Verified external contracts: [for each dependency/SDK seam, the exact verified API shape (option keys, callback signature, event field names) and where it was verified, or "None"]
- Behavior rules: [defaults, parsing, validation, duplicate handling, edge cases]
- Error and security rules: [error contract, permission/secret/logging behavior, or "None"]

## Acceptance Criteria
- [ ] [Specific, observable outcome tied to the implementation contract]

## Test Expectations
- [Test runner/framework and exact command, test location, behavior under test, setup/fakes, concrete input, and expected output]

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

Use `None` only when a field truly does not apply. Do not omit a field because the answer is inconvenient or requires repo inspection.

## Gold Standard: pointer vs artifact
The difference between an issue that fails and one that works is whether contracts are shown, not named. Calibrate to the "after" column.

Vague / pointer (an implementer will guess and be wrong):

```md
- Interfaces and names: add `createWatchdog` that consumes the stream callback and aborts the run; reuse the detector in loop-progress.
- Verified external contracts: the run accepts a stream callback and an abort signal (confirm against the SDK).
- Behavior rules: when the same tool call repeats, abort. Tool-call events carry the tool name and args.
```

Specific / artifact (the implementer can build it from the issue alone):

```md
- Interfaces and names: paste real shapes the implementer must satisfy —
  `export function createWatchdog(opts: { abortController: AbortController; getSnapshot: () => Snapshot; threshold?: number; onEvent?: (e: unknown) => void }): (event: unknown) => void`
  Detector contract it must call (copied from loop-progress.mts):
  `observeNormalizedToolCall(state, identity, snapshot, threshold): { state: DetectorState; livelockCandidate: boolean }`
  and `initialDetectorState()` is a FUNCTION, not a constant.
- Verified external contracts (verified in node_modules/<pkg>/dist/index.d.ts): the run reads the watchdog via the `logging` option, not a top-level callback —
  `run(opts: { signal: AbortSignal; logging: { type: "file"; path: string; onAgentStreamEvent?: (e: unknown) => void } })`.
- Behavior rules: a parsed tool-call stream event has `type === "toolCall"` (NOT "tool_call"), with string fields `name` and `formattedArgs`; non-toolCall events are forwarded to logging but never advance the detector.
```

The "after" column is not longer because it is wordier; it is longer because each named thing now carries its real shape and each integration literal is verified and quoted.

## Tightening Quality Gate
You hold the PRD and repo context in your head, so a "does this look implementable?" self-check always passes — you cannot feel the gap a starved reader feels. Replace judgment with the context-free simulation plus countable checks below. Run it before review and again before finalizing.

### Context-free simulation (do this first)
Read the issue as an implementer who has ONLY this issue text. Produce the literal list of every symbol, type, signature, integration contract, or literal value the issue NAMES but does not SHOW. The issue is not done until that list is empty (each item pasted in) or every remaining item is explicitly marked blocked pending verification.

### Countable checks (each must hold; these are falsifiable, not vibes)
- Every existing/target symbol the issue depends on has its real signature or type pasted (count of named-but-not-shown symbols = 0).
- Every dependency/SDK integration seam has a verified API excerpt with where it was verified (count of unverified external seams = 0).
- Zero invented literal values stated as fact: every event name, option/param key, enum value, route, env var, and field name is either verified-and-quoted or flagged blocked.
- Any edit that adds a `continue`/`break`/return/branch pastes the enclosing control-flow skeleton it lands in; any symbol from a sibling/not-yet-merged issue includes its import path and provenance.
- Acceptance criteria are observable and deterministic, each tied to a pasted contract.
- Test expectations name the test runner/framework (not just a command) and include location, behavior under test, ≥1 concrete literal input, and its expected literal output.
- The issue ends at a valid repo state and does not depend on a later issue to restore build/test/migration/runtime validity.
- A reviewer can state exactly what is out of scope.

If a check cannot be made to pass without inventing an unverified contract, stop and ask one clarifying question, or scope a verification step into the issue, instead of finalizing.
