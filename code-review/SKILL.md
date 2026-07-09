---
name: code-review
description: Run an extremely strict maintainability review for abstraction quality, structural simplification, giant files, and spaghetti-condition growth. Use for a thermo-nuclear code quality review, thermonuclear review, deep code quality audit, harsh maintainability review, or review since a base commit/branch with aggressive architecture scrutiny.
disable-model-invocation: false
---

# Thermo-Nuclear Code Quality Review

Use this skill for an unusually strict review focused on implementation quality, maintainability, abstraction quality, and codebase health.

Above all, push the reviewer to be ambitious about structure. Do not stop at local cleanup. Look for restructurings that preserve behavior while making the implementation smaller, simpler, more direct, and easier to reason about.

For the expanded rubric, load [REFERENCE.md](REFERENCE.md).

## Workflow

1. **Pin the review base.**
   - If the user supplied a commit, branch, tag, or range base, pass it through exactly.
   - If the user did not supply one, ask: `Review against what - a branch, a commit, or main?`
   - Review the branch diff with `git diff <fixed-point>...HEAD`.
   - Note commits with `git log <fixed-point>..HEAD --oneline`.
   - Check `git status --short`; if the user asked for WIP review, include staged and unstaged changes too.

2. **Collect local standards before judging architecture.**
   - Read relevant repo guidance such as `AGENTS.md`, `CLAUDE.md`, `CONTRIBUTING.md`, `CONTEXT.md`, `CONTEXT-MAP.md`, `docs/adr/`, `STYLE.md`, `STANDARDS.md`, and similar docs.
   - Note machine-enforced configs such as `.editorconfig`, `eslint.config.*`, `biome.json`, `prettier.config.*`, and `tsconfig.json`, but do not spend review space restating what tooling already enforces.
   - Prefer documented canonical layers, helpers, and ownership boundaries over generic advice.

3. **Review for maintainability and structural quality.**
   - Start from the baseline prompt below.
   - Apply the non-negotiable standards in [REFERENCE.md](REFERENCE.md).
   - Treat this as a maintainability / architecture axis, separate from ordinary standards compliance or spec correctness.

4. **Optionally add other review axes.**
   - If the user asks for spec correctness or provides an issue, PRD, or requirements doc, run a separate Spec review and keep it separate from Maintainability.
   - For broad reviews, you may run Standards, Spec, and Maintainability reviews in parallel sub-agents, then aggregate them under separate headings.
   - Do not merge or rerank findings across axes; separation makes tradeoffs visible.

## Baseline Prompt

Perform a deep code quality audit of the current branch's changes.

Rethink how to structure and implement the changes to meaningfully improve code quality without changing behavior. Work to improve abstractions, modularity, succinctness, and legibility. Reduce spaghetti code. Be ambitious when there is a clear path to a better structure.

## Proof Bar

Be strict, but do not invent speculative architecture work.

- Only flag a structural rewrite when you can describe the simpler shape and why behavior can remain unchanged.
- Distinguish hard maintainability regressions from judgement calls.
- Cite the local standard or changed code that supports the finding.
- Skip low-value nits when larger structural issues exist.
- Do not approve merely because behavior appears correct.

## Output Contract

Lead with findings. Order by severity and maintainability impact.

For each finding, include:

- severity
- file and line, when available
- the issue
- why it harms maintainability or architecture
- a concrete remedy
- whether it is a hard blocker or a judgement call

If there are no findings, say that clearly and mention any residual risk or test gap.

Use these headings when relevant: `## Maintainability`, `## Standards`, and `## Spec`.

End with a one-line summary: total findings per axis and the worst single issue, if any.

