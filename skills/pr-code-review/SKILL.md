---
name: pr-code-review
description: Review a GitHub pull request URL or changes since a fixed point along two independent axes — repository standards and originating spec — using parallel sub-agents. Use for pull requests, branches, work-in-progress changes, or review since a commit, branch, tag, or merge-base.
---

Review a change on two independent axes:

- **Standards** — does the code conform to this repo's documented coding standards?
- **Spec** — does the code faithfully implement the originating issue / spec?

Run both axes as parallel sub-agents, then report them side by side.

## Process

### 1. Freeze the review context

For a GitHub pull request URL, run this exactly once:

```bash
<skill-directory>/scripts/gather-pr-context.sh '<pull-request-url>'
```

The command prints one compact manifest. Keep the large artifacts out of the parent context; pass their paths from the manifest to the sub-agents:

- `diff` — the changes in the pull request.
- `commits` — every pull-request commit.
- `spec` — the title and description of every issue in GitHub's closing relationship.

When `closing_issue_count` is positive, that `spec` artifact is the complete spec. When it is zero, use the legacy spec lookup below.

For any other argument, preserve the fixed-point flow:

Whatever the user said is the fixed point — a commit SHA, branch name, tag, `main`, `HEAD~5`, etc. If they didn't specify one, ask for it.

Capture `git diff <fixed-point>...HEAD` and `git log <fixed-point>..HEAD --oneline`. Confirm the fixed point resolves and the diff is non-empty before continuing.

Legacy spec lookup:

1. Issue references in commit messages (`#123`, `Closes #45`, etc.), fetched through `docs/agents/issue-tracker.md`.
2. A path the user passed as an argument.
3. A spec file under `docs/`, `specs/`, or `.scratch/` matching the branch name or feature.
4. Ask the user. If no spec exists, skip the Spec sub-agent and report `no spec available`.

Run `/setup-matt-pocock-skills` if the legacy lookup needs `docs/agents/issue-tracker.md` and it is missing.

This step is complete when the exact diff is frozen and the spec source is identified or explicitly absent.

### 2. Identify the standards sources

List every repository file that documents how code should be written, such as `CODING_STANDARDS.md` or `CONTRIBUTING.md`.

The Standards sub-agent must also read [`references/smell-baseline.md`](references/smell-baseline.md). A documented repository standard overrides the baseline; baseline smells are judgement calls.

This step is complete when every applicable standards-source path is listed.

### 3. Spawn both sub-agents in parallel

Give both sub-agents the frozen diff artifact path, or the fixed-point diff command, plus the commit-list path or command. They must inspect the artifacts themselves.

Standards prompt:

- Include every standards-source path and the absolute path to `references/smell-baseline.md`.
- Brief: "Report by file/hunk: (a) every documented-standard violation, citing the standards file and rule; (b) every baseline smell, naming it and quoting the hunk. Separate hard violations from judgement calls. Repository standards override the baseline. Skip checks enforced by tooling. Under 400 words."

Spec prompt:

- Include the spec artifact or source path.
- Brief: "Report: (a) missing or partial requirements; (b) scope creep; (c) requirements whose implementation looks wrong. Quote the spec for every finding. Under 400 words."

If the spec is missing, skip the Spec sub-agent and note this in the final report.

This step is complete when each applicable axis returns a report grounded in the same frozen diff.

### 4. Aggregate

Present the reports under `## Standards` and `## Spec`, verbatim or lightly cleaned. Keep their findings separate.

End with one line containing each axis's finding count and worst issue, if any. Do not choose a winner across axes.

## Why two axes

A standards-compliant change can implement the wrong thing; a spec-compliant change can violate repository conventions. Separation keeps either axis from masking the other.
