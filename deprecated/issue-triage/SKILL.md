---
name: issue-triage
description: Autonomously classifies and investigates incoming issues, validates and diagnoses bugs, outlines enhancements, and compiles every implementation-blocking question into one issue-ready Markdown output. Use when an issue, ticket, bug report, or feature request needs non-interactive, repository-aware triage before it can be worked.
---

# Issue Triage

Autonomously determine whether an issue can be handed to an implementer now. Each run must investigate available evidence and compile every unresolved question into one final batch. Never pause to interview the user or emit questions incrementally. A valid, non-duplicate issue with no open questions is workable; say so explicitly. An issue may instead be `not-actionable` when evidence shows there is no work to do.

Issue-tracker access is strictly read-only. Never invoke tracker write, mutation, or commenting tools, even when they are available. Do not edit code, change labels, close issues, or post comments. Emit exactly one final Markdown artifact after the analysis is complete; an external system is responsible for posting it. Never emit partial findings or multiple rounds of questions during one run.

## Reference

Read [EXAMPLES.md](EXAMPLES.md) when calibrating actionability or drafting open questions. It contrasts a workable bug with an under-specified enhancement.

## Inputs

Accept pasted issue text, an issue URL, or an issue identifier. When tracker access is available, read the full body, comments, labels, attachments, and prior triage notes. Otherwise, complete the best possible triage from supplied material and name inaccessible evidence in the final artifact; do not stop to request access.

## Workflow

1. **Understand the claim.** Restate the affected user, current behavior, desired outcome, reproduction or workflow, constraints, and success conditions. Separate reporter claims from established facts.
2. **Gather repository evidence.** Read project guidance, domain docs, ADRs, implementation, and tests. Search by domain concept, not only the issue's wording. Check for an existing implementation, duplicate, or recorded prior rejection. Cite relevant symbols and commands; locations are evidence, not implementation prescriptions.
3. **Classify.**
   - `bug` — existing intended or documented behavior is incorrect, regressed, or errors unexpectedly.
   - `enhancement` — the request adds capability or deliberately changes intended behavior.
   - `mixed` — separable bug and enhancement claims exist; recommend splitting them.
   - If intent is unclear, recommend the most likely category and name what would change the classification.
4. **Investigate the matching branch.** Follow the bug or enhancement workflow below.
5. **Build the actionability inventory.** Record what is established, what the repository answers, and every remaining decision or fact that changes observable behavior, scope, domain rules, compatibility, or acceptance criteria.
6. **Convert every material gap into a specific open question.** Do not silently choose product behavior. Do not ask the reporter to make ordinary implementation decisions. Include foreseeable conditional follow-ups in this same batch.
7. **Assess readiness.** `needs-info` means at least one open question blocks work. `ready` means the issue and triage findings provide a clear outcome and verification boundary with no blocking questions. `not-actionable` means evidence demonstrates a duplicate, already-implemented request, invalid bug, or previously rejected request.
8. **Complete the run.** Re-read the issue as a context-starved implementer, perform a second gap pass, then emit one final Markdown artifact. Do not wait for answers. On a later autonomous run, treat human replies as evidence, remove answered questions, and compile any still-open questions into a new complete batch without re-asking resolved ones.

## What makes an issue actionable

An implementer working from the issue and repository must be able to determine:

- who encounters the problem or uses the capability, and in what workflow;
- current behavior and the observable desired outcome;
- the intended scope and important boundaries;
- the domain rules and product choices that materially affect behavior;
- how completion can be verified with concrete acceptance criteria.

Actionable does **not** require file-by-file instructions, a chosen internal design, or answers to questions the repository and its conventions already settle. Root cause is valuable but not required when a bug is reliably reproducible. An implementation preference is not an open question when multiple approaches can satisfy the same outcome.

## Bug workflow

1. Derive the smallest reproducible case and compare actual behavior with documented, tested, or clearly intended behavior.
2. Reproduce on a supported configuration when feasible. Run the narrowest relevant tests or commands and record exact results. If execution is impossible, perform static verification and say so.
3. Report validation as `confirmed`, `probable`, `unconfirmed`, or `invalid`. Failure to reproduce is not proof of invalidity; identify environment differences or missing inputs.
4. Trace the path from trigger to failure. State an evidence-backed root cause or ranked hypotheses and the next discriminating check.
5. Define the expected behavior, affected boundary, regression scenarios, and acceptance criteria. Ask for missing reproduction inputs or product behavior only when an implementer cannot proceed safely without them.

## Enhancement workflow

1. Confirm the capability does not already exist and surface related or previously rejected designs.
2. Define the user outcome and end-to-end workflow, including where information is created, viewed, changed, and consumed.
3. Map the request to existing domain concepts, interfaces, data flow, permissions, and extension points.
4. Resolve or question material rules: data ownership, lifecycle, combinations, limits, validation, visibility, failure behavior, compatibility, migration, and rollout. Include only dimensions relevant to this request.
5. Propose coherent, testable implementation slices and acceptance criteria after product choices are known. If answers would substantially change the plan, present a conditional outline rather than pretending the plan is settled.

## Writing open questions

Search issue history, docs, code, tests, and configuration before asking. Each question must:

- ask one concrete decision or missing fact in language the answerer can resolve;
- explain why the answer changes or blocks the work;
- offer an evidence-backed recommended default when possible;
- identify the likely answerer when evident.

Do not ask generic “provide more detail” questions, questions answered by the repository, or questions about naming, file placement, component choice, and other implementer-owned details. Combine tightly coupled questions, but do not hide independent decisions inside one broad question. The list must be exhaustive, not merely the first few questions noticed. For answer branches that predictably create another decision, include a labeled conditional follow-up now rather than deferring it to another conversation. If none remain, write `None — this issue is workable as written` or `None — this issue is workable with the established triage findings`.

## Output

Emit one issue-ready Markdown document in this shape:

```markdown
> *This was generated by AI during autonomous issue triage.*

## Triage
**Classification:** bug | enhancement | mixed (confidence)
**Readiness:** ready | needs-info | not-actionable

### What I established
### Validation and diagnosis | Implementation outline
### Acceptance boundary
### Questions that must be answered
### Recommended next action
```

Include concise evidence and commands under “What I established.” For `needs-info`, number every question, explain its impact, give a recommended default when supported, and include conditional subquestions. Do not invent acceptance criteria for disputed behavior. For `ready`, write `None — this issue is workable ...` under questions and state that implementation can begin. For `not-actionable`, explain the evidence and recommended disposition. Print only the completed Markdown document, with no conversational preamble. Do not post it.
