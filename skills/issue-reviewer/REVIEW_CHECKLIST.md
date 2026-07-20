# Issue Review Checklist

This is the authoritative reference for reviewing decomposed issue drafts. Use it with the workflow in [SKILL.md](SKILL.md). The two axes are independent: run Completeness with no outside knowledge, then run Accuracy with PRD and repo evidence.

## Axis 1 - Completeness (context-free)

Read ONLY the issue text, as an implementer with no PRD, no conversation, and no browsing. The goal is to find what the issue NAMES but does not SHOW. Repo and PRD knowledge are forbidden in this pass; using them to mentally fill a gap is the exact failure that lets a broken issue ship.

### Required sections present
Every issue must contain all of: `User Story`, `Description`, `Context Pack` (Source decisions, Repo facts, Non-goals), `Implementation Contract` (Expected files, Interfaces and names, Verified external contracts, Behavior rules, Error and security rules), `Acceptance Criteria`, `Test Expectations`, `Dependencies` (Blocked by / Blocks), `Labels`, `Estimate`, `Risk`, `Validator Stopping Point`. A field set to `None` is acceptable only when it truly does not apply; a missing field is a finding.

### Named-but-not-shown list (the core artifact of this pass)
List every symbol, type, signature, integration contract, or literal value the issue references but does not paste in full. The issue fails completeness unless this list is empty or every remaining item is explicitly marked blocked pending verification.

### Countable checks (falsifiable, not vibes; each must hold)
- Named-but-not-shown count = 0: every existing/target symbol the issue depends on has its real signature or type definition pasted, not just its name.
- Unverified-external-seam count = 0: every dependency/SDK seam has a verified API excerpt (option keys, callback signature, event field names) and states where it was verified.
- Invented-literal count = 0: every event name, option/param key, enum value, route, env var, and field name is either quoted from a named source or flagged blocked. No "assume", "should be", "likely", or "TBD" for a contract the implementer must compile or integrate against.
- Control-flow landing shown: any edit adding a `continue`/`break`/return/branch pastes the enclosing loop/try/function skeleton it lands in.
- Sibling provenance shown: any symbol delivered by another (possibly not-yet-merged) issue includes its exact import path and which issue produces it.
- Acceptance Criteria are observable and deterministic, each tied to a pasted contract; not "works correctly".
- Test Expectations name the test runner/framework (not just a command) and include location, behavior under test, at least 1 concrete literal input, and its expected literal output.
- Scope is bounded: a reviewer can state exactly what is out of scope from the issue text alone.
- The issue ends at a valid repo state and does not rely on a later issue to restore build/test/migration/runtime validity.

Anything that fails here is a completeness gap. It does not require the repo to detect, only the issue text.

Completion criterion: every issue has a required-section result, a named-but-not-shown list, and one pass/finding for each countable check before any PRD or repo evidence is opened.

## Axis 2 - Accuracy (grounded)

Now open the PRD and the repo. Treat every material claim in the issue as suspect until verified against source. Do not rely on naming; inspect the actual definition, call sites, tests, schema, and config when they affect the claim.

Material claims include artifacts, decisions, literals, dependency statements, scope boundaries, and behavioral contracts that an implementer could build against or be constrained by.

### Claim classification (use consistently)
- `Verified`: source clearly supports the claim; you opened it and it matches.
- `Contradicted`: source shows the claim is false or materially incomplete (e.g., pasted signature differs from the real one, wrong path, wrong literal, conflicts with the PRD).
- `Unsupported`: no evidence found after checking the likely sources.
- `Ambiguous`: evidence points multiple ways, or the issue uses overloaded terminology.
- `Outdated/Risky`: possibly true but depends on stale patterns, deprecated paths, TODOs, or untested assumptions.

### What to verify
- **Against the repo**: every pasted signature, type/DTO, return shape, enum, route, env var, config key, event/field name, and file path. Confirm the artifact exists and matches exactly. A pasted-but-wrong artifact is `Contradicted` and is a Critical finding; it passes the decomposer's "is it shown?" gate but builds the wrong thing.
- **Against the PRD**: every "Source decision", accepted default, requirement, and non-goal the issue cites. Confirm the issue did not invent, drop, or distort a decision, and that its scope matches what the PRD actually asked for.
- **Cite evidence**: use `path:line` for repo evidence and `PRD section`/quoted line for PRD evidence. If you checked the likely sources and found nothing, say `Unsupported`; do not invent.

Completion criterion: every material claim has a classification and evidence, or an explicit skipped-source reason. A missing PRD or repo cannot support `PASS` for claims that depend on it.

## Cross-Issue Checks
Review the set, not just each issue:
- **Dependencies**: declared `Blocked by`/`Blocks` are real, acyclic, and ordered so no issue consumes a symbol before the issue that produces it.
- **Valid-state chain**: implementing the issues in dependency order never passes through a knowingly broken repo state.
- **PRD coverage**: every PRD requirement maps to at least one issue; flag requirements with no issue (gap) and issues with no PRD basis (orphan scope).
- **No overlap**: two issues do not both own the same change, and no issue silently duplicates another's contract.

Completion criterion: every cross-issue check has a pass, finding, or skipped-source reason.

## Severity
- `Critical`: would send implementation in the wrong direction: a Contradicted contract, a missing required PRD requirement, or a dependency cycle.
- `High`: a major missing artifact, unsupported integration seam, or scope/decision mismatch with the PRD.
- `Medium`: ambiguity, weak/unobservable acceptance criteria, underspecified tests, or a sizing concern.
- `Low`: stylistic, minor wording, or non-blocking polish.

## Per-Issue Verdict
- **PASS**: completeness checks all hold and every material claim is Verified. Ready to hand to a coding model.
- **NEEDS REVISION**: fixable completeness gaps or inaccuracies; list the exact paste/correction required for each.
- **BLOCKED**: contains a Contradicted contract, an unverifiable claim the implementer must integrate against, or an unresolved upstream dependency. Must not be implemented as-is.

A single Critical finding forces BLOCKED regardless of how complete the rest of the issue looks.

## Report Template

```md
## Summary
[Issue count, verdict tally (PASS / NEEDS REVISION / BLOCKED), and the single worst finding.]
Inputs reviewed: issues [yes], PRD [yes/skipped], repo [yes/skipped].

## Verdicts
| Issue | Verdict | Critical | High | Med | Low |
|-------|---------|----------|------|-----|-----|
| [title] | [PASS/NEEDS REVISION/BLOCKED] | n | n | n | n |

## Per-Issue Review
### [Issue title] - [VERDICT]
Named-but-not-shown: [list, or "none"]

Claim Matrix
| # | Claim (artifact / decision / literal) | Classification | Evidence | Implication |
|---|----------------------------------------|----------------|----------|-------------|
| 1 | [e.g. pasted signature of `foo`] | [Verified/Contradicted/Unsupported/Ambiguous/Outdated/Risky] | [path:line or PRD section x or "not found"] | [what it means for the implementer] |

Findings
- [Severity] [Classification] [section/claim] - [problem]
  Evidence: [path:line or PRD section x]
  Fix: [exact artifact to paste or correction to make]

## Cross-Issue Findings
- [Dependency / coverage / overlap / valid-state findings with evidence.]

## PRD Coverage
- Covered: [requirement -> issue]
- Gaps: [PRD requirement with no issue]
- Orphans: [issue with no PRD basis]

## Open Questions
- [Anything unresolvable from the issues, PRD, or repo that blocks a verdict.]
```

The claim matrix is mandatory for any issue that is not a clean PASS. Keep rows compact, but include every material claim, especially Verified ones, since they are the anchors that justify advancing an issue.

## Worked Example
A filled fragment showing the calibration bar. The two rows are the anchors of every review: a `Verified` contract you opened and confirmed, and a `Contradicted` one that passed the decomposer's "is it shown?" gate but is wrong against source. Notice that the Contradicted literal is present and confident; it would survive a "did they paste it?" check, yet it builds the wrong thing.

Claim Matrix (excerpt)
| # | Claim (artifact / decision / literal) | Classification | Evidence | Implication |
|---|----------------------------------------|----------------|----------|-------------|
| 1 | Pasted signature `createWatchdog(opts: { abortController: AbortController; getSnapshot: () => Snapshot; threshold?: number }): (event: unknown) => void` | Verified | `src/watchdog.mts:12` matches exactly | Implementer can build against it as written |
| 2 | Issue states stream events use `type === "tool_call"` | Contradicted | `src/stream/parse.mts:88` emits `type === "toolCall"` | Detector never fires; livelock check is silently dead |

Findings
- Critical Contradicted - Implementation Contract / event literal: issue pastes `"tool_call"` but source emits `"toolCall"`.
  Evidence: `src/stream/parse.mts:88`
  Fix: replace the literal with `"toolCall"` (camelCase), and re-confirm the `name`/`formattedArgs` field names against the same parser before marking the seam verified.

One Contradicted contract like row 2 forces BLOCKED on the issue regardless of how complete the rest looks.
