---
name: two-axis-review
description: 'Reviews code changes since a fixed point along two independent axes: documented standards and originating spec/issue fit. Use when the user asks to review a branch, PR, WIP diff, or changes since a commit, tag, branch, merge-base, or "main".'
---

# Review

Two-axis review of the diff between a fixed point the user supplies and the current code:

- **Standards** - does the code conform to this repo's documented coding standards?
- **Spec** - does the code faithfully implement the originating issue / PRD / spec?

Both axes run with separate context, preferably in parallel, so they don't pollute each other's findings.

The issue tracker should have been provided to you. Run `/setup-matt-pocock-skills` if `docs/agents/issue-tracker.md` is missing.

## Quick Start

For "review since main":

1. Resolve `main` as the fixed point.
2. Capture commits with `git log main..HEAD --oneline`.
3. Check `git status --short` and choose a committed-only or WIP-inclusive diff.
4. Run Standards and Spec reviews with separate context.
5. Report findings under `## Standards` and `## Spec`.

## Process

### 1. Pin the fixed point

Whatever the user said is the fixed point: a commit SHA, branch name, tag, `main`, `HEAD~5`, etc. Don't be opinionated; pass it through. If they didn't specify one, ask: "Review against what: a branch, a commit, or `main`?" Don't proceed until you have it.

Run `git status --short` before choosing the diff:

- If the working tree is clean, capture `git diff <fixed-point>...HEAD` (three-dot, so the comparison is against the merge-base).
- If staged or unstaged tracked files exist, capture the merge base with `git merge-base <fixed-point> HEAD`, then use `git diff <merge-base>` so committed and WIP tracked changes are included.
- If untracked files exist, list them from `git status --short` and read relevant untracked files separately because `git diff` will not include them.

Also note the list of commits via `git log <fixed-point>..HEAD --oneline`.

### 2. Identify the spec source

Look for the originating spec, in this order:

1. A path the user passed as an argument.
2. Issue references in the commit messages (`#123`, `Closes #45`, GitLab `!67`, etc.) - fetch via the workflow in `docs/agents/issue-tracker.md`.
3. A PRD/spec file under `docs/`, `specs/`, or `.scratch/` matching the branch name or feature.
4. If nothing is found, ask the user where the spec is. If they say there isn't one, the **Spec** sub-agent will skip and report "no spec available".

### 3. Identify the standards sources

Anything in the repo that documents how code should be written. Common locations:

- `CLAUDE.md`, `AGENTS.md`
- `CONTRIBUTING.md`
- `CONTEXT.md`, `CONTEXT-MAP.md`, per-context `CONTEXT.md` files
- `docs/adr/` (architectural decisions can be standards when they still apply to the changed code)
- `.editorconfig`, `eslint.config.*`, `biome.json`, `prettier.config.*`, `tsconfig.json` (machine-enforced standards - note them but don't re-check what tooling already checks)
- Any `STYLE.md`, `STANDARDS.md`, `STYLEGUIDE.md`, or similar at the repo root or under `docs/`

Collect the list of files. The **Standards** sub-agent will read them.

### 4. Run both review axes

Use the available multi-agent tool to run both axes in parallel. If no multi-agent tool is available, run them sequentially and keep the context separate.

**Standards sub-agent prompt** - include:

- The full diff command, commit list, and any untracked files included separately.
- The list of standards-source files you found in step 3.
- The brief: "Read the standards docs. Then read the diff. Report, per file/hunk where relevant, every place the diff violates a documented standard. Cite the standard (file + the rule). For ADR-based findings, cite why the ADR applies to this changed code. Distinguish hard violations from judgement calls. Skip anything tooling enforces. Under 400 words."

**Spec sub-agent prompt** - include:

- The diff command and commit list.
- The path or fetched contents of the spec, plus any untracked files included separately.
- The brief: "Read the spec. Then read the diff. Report: (a) requirements the spec asked for that are missing or partial; (b) behaviour in the diff that wasn't asked for (scope creep); (c) requirements that look implemented but where the implementation looks wrong. Quote the spec line for each finding. Under 400 words."

If the spec is missing, skip the Spec sub-agent and note this in the final report.

### 5. Aggregate

Present the two reports under `## Standards` and `## Spec` headings, verbatim or lightly cleaned. Do **not** merge or rerank findings: the two axes are deliberately separate so the user can see them independently.

End with a one-line summary: total findings per axis, and the worst single issue (if any) flagged.

## Why two axes

A change can pass one axis and fail the other:

- Code that follows every standard but implements the wrong thing: **Standards pass, Spec fail.**
- Code that does exactly what the issue asked but breaks the project's conventions: **Spec pass, Standards fail.**

Reporting them separately stops one axis from masking the other.

