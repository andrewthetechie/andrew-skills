---
name: issue-reviewer
description: Issue-readiness review for decomposed issue drafts - check context-free completeness for a starved implementer and grounded PRD/repo accuracy. Use when the user asks whether issue drafts or a decomposition are ready for implementation or safe to hand to a small/local coding model.
---

# Issue Reviewer

## Quick Start
Use this skill as an issue-readiness gate before implementation. It makes two independent proofs:

- **Starved implementer**: the issue is workable from its text alone, with no PRD, repo, conversation, or browsing.
- **Grounded audit**: every material claim in the issue is true against PRD and repository evidence.

The output is a review report only. Do not edit issues, implement code, change tracker state, or change project files unless the user explicitly asks for a follow-up task.

Start by stating:

```text
ISSUE REVIEW STATE: Read Inputs
```

If the issue drafts are missing or empty, stop and ask for them.

## Inputs
Establish these inputs before reviewing:

- **Issue drafts** (required): the issues to review. They may arrive as GitHub issues selected by a label, a folder of markdown files (one issue per file), or pasted text. If missing, stop and ask.
- **PRD / source** (for the grounded audit): the document the issues were decomposed from. If missing, still run the available checks and note that PRD fact-checking was skipped.
- **Repo** (for the grounded audit): the codebase the issues target. If unavailable, still run the available checks and note that repo grounding was skipped.

Do not mark an issue `PASS` when a missing PRD or repo prevents verification of material claims the implementer must rely on.

## Workflow
Read [REVIEW_CHECKLIST.md](REVIEW_CHECKLIST.md) before reviewing. It is the authoritative reference for exact checks, claim classification, severity, verdicts, and the report template. Do not read or defer to any other skill's files.

State the current loop state before each major action:

```text
ISSUE REVIEW STATE: [Read Inputs | Completeness Pass | Accuracy Pass | Cross-Issue Checks | Verdicts | Report]
```

1. **Read Inputs**: Confirm the issue drafts, PRD, and repo per the Inputs section, and read REVIEW_CHECKLIST.md. Identify the issue count and declared dependency graph. Complete when the input inventory says issues yes, PRD yes/skipped, repo yes/skipped, and the dependency graph is known or explicitly absent.
2. **Completeness Pass (context-free)**: For each issue, read only that issue's text as a starved implementer. Run the required-section, named-but-not-shown, and countable checks in REVIEW_CHECKLIST.md. Freeze these results before opening PRD or repo evidence. Complete when every issue has a required-section result, named-but-not-shown list, and completeness finding or pass.
3. **Accuracy Pass (grounded)**: Open the PRD and repo if available. Treat every material claim as suspect until verified. Classify each claim and verify pasted signatures, types, paths, literals, decisions, scope, and non-goals against source evidence. Complete when every material claim has a claim-matrix row with `Verified`, `Contradicted`, `Unsupported`, `Ambiguous`, `Outdated/Risky`, or a skipped-source reason.
4. **Cross-Issue Checks**: Validate dependencies, dependency order, valid repo-state chain, PRD coverage, orphan scope, and overlap. Complete when each cross-issue check has a pass, finding, or skipped-source reason.
5. **Verdicts**: Assign each issue `PASS`, `NEEDS REVISION`, or `BLOCKED` using REVIEW_CHECKLIST.md. Complete when every issue has a verdict and exact fixes required to advance it; any Critical finding forces `BLOCKED`.
6. **Report**: Produce the report using the template in REVIEW_CHECKLIST.md. Complete when the report includes summary, verdict table, per-issue review, required claim matrices, cross-issue findings, PRD coverage, and open questions.

## Two Axes, Separated
Run the two passes with separate context so they do not pollute each other. If subagents are available, split Completeness and Accuracy. If not, write the frozen Completeness notes before opening PRD or repo evidence.

- **Completeness**: is the issue self-contained enough for a small model to implement from the issue text alone? Judge against the required sections and completeness checks in REVIEW_CHECKLIST.md, with zero outside knowledge.
- **Accuracy**: are the issue's facts true? Judge against the PRD (decisions, scope, requirements) and repo (signatures, types, paths, literals, conventions).

These are independent. An issue can be perfectly self-contained yet confidently wrong (Completeness pass, Accuracy fail), or every fact true yet missing half the contract a starved reader needs (Accuracy pass, Completeness fail). Report them separately so one axis never masks the other.

## Hard Rules
- Keep the Completeness pass context-free; repo/PRD knowledge cannot patch a gap the issue text leaves open.
- Do not invent codebase or PRD facts. If you cannot find evidence, classify the claim `Unsupported` or `Ambiguous`; never guess.
- Do not rubber-stamp an issue because it reads plausibly; require pasted-and-verified evidence before marking a claim `Verified`.
- A pasted-but-wrong artifact is worse than an omitted artifact: classify wrong signatures, literals, paths, routes, env vars, enum values, and field names as Critical `Contradicted` findings.
- If issue drafts are missing, or evidence conflicts in a way that prevents a verdict, stop with one clarifying question.
