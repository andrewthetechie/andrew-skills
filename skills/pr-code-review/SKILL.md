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
- `checks` contains the captured PR check names, states, categories (`bucket`), and links.
- `spec` — the title and description of every issue in GitHub's closing relationship.

When `closing_issue_count` is positive, that `spec` artifact is the complete spec. When it is zero, use the legacy spec lookup below.

For any other argument, preserve the fixed-point flow:

Use the user's requested commit, branch, tag, or revision expression. If they omitted the fixed point, ask for it.

Run `git fetch origin` before resolving the ref. If the fetch fails, stop and report the error.

For an unqualified branch name `<name>`, prefer `origin/<name>` when `git show-ref --verify --quiet refs/remotes/origin/<name>` succeeds. For example, resolve `main` through `origin/main` when available. Preserve explicit refs, commit SHAs, tags, and revision expressions such as `HEAD~5`.

Resolve the selected ref with `git rev-parse --verify '<ref>^{commit}'`. Use that commit SHA as `<fixed-point>` in both captures: `git diff <fixed-point>...HEAD` and `git log <fixed-point>..HEAD --oneline`. Confirm that the ref resolves and the diff is non-empty before continuing.

Compare the commit list and `git diff <fixed-point>...HEAD --stat` with the user's expected commit count and described scope. If either is much larger than described, stop before spawning sub-agents and report the discrepancy. If the user gave no expected size, inspect the commit subjects and changed paths for unrelated work.

Legacy spec lookup:

1. Issue references in commit messages (`#123`, `Closes #45`, etc.), fetched through `docs/agents/issue-tracker.md`.
2. A path the user passed as an argument.
3. A spec file under `docs/`, `specs/`, or `.scratch/` matching the branch name or feature.
4. Ask the user. If no spec exists, skip the Spec sub-agent and report `no spec available`.

Run `/setup-matt-pocock-skills` if the legacy lookup needs `docs/agents/issue-tracker.md` and it is missing.

Complete this step after you freeze the verified diff and identify the spec source or record its absence.

### 2. Identify the standards sources

List every repository file that documents how code should be written, such as `CODING_STANDARDS.md` or `CONTRIBUTING.md`.

The Standards sub-agent must also read [`references/smell-baseline.md`](references/smell-baseline.md). A documented repository standard overrides the baseline; baseline smells are judgement calls.

This step is complete when every applicable standards-source path is listed.

### 3. Spawn both sub-agents in parallel

Give both sub-agents the frozen diff artifact path, or the fixed-point diff command, plus the commit-list path or command. They must inspect the artifacts themselves.

For a PR review, also give both sub-agents the `checks` artifact path.

Include these instructions in both sub-agent prompts:

- When available, read the `checks` artifact before reporting. Report every failing check (`bucket: fail`) as a finding on the axis it concerns. Include the check's name, state, and link.
- You may run the focused test files touched by the diff against the reviewed revision. Run them when the result can settle a finding. Report the exact command and result. If you cannot run a relevant test, report the command and blocker.

Standards prompt:

- Include every standards-source path and the absolute path to `references/smell-baseline.md`.
- Brief: "Read every listed standards file in full before you report. In your report, name any file you did not read in full. Report by file/hunk: (a) every documented-standard violation, citing the standards file and rule; (b) every baseline smell, naming it and quoting the hunk. Separate hard violations from judgement calls. Repository standards override the baseline. Read each existing helper, fixture, or function before recommending its use or reuse. Quote its signature or body as evidence supporting the finding. Base claims about its behaviour on its code. Use captured check results for rules enforced by tooling. Under 400 words."

Spec prompt:

- Include the spec artifact or source path.
- Brief: "Report: (a) missing or partial requirements; (b) scope creep; (c) requirements whose implementation looks wrong. Quote the spec for every finding. Under 400 words."

If the spec is missing, skip the Spec sub-agent and note this in the final report.

Complete this step after each applicable axis reports on the frozen diff, failing checks, and test commands, results, or blockers.

### 4. Aggregate

Present the reports under `## Standards` and `## Spec`, verbatim or lightly cleaned. Keep their findings separate.

End with one line containing each axis's finding count and worst issue, if any. Do not choose a winner across axes.

## Why two axes

A standards-compliant change can implement the wrong thing; a spec-compliant change can violate repository conventions. Separation keeps either axis from masking the other.

