---
name: setup-andrew-skills
description: Configure this repo for the andrew-skills — set up issue tracker, domain docs, and preferred workflows. Run once before first use of the other skills.
disable-model-invocation: true
---

# Setup Andrew's Skills

Scaffold the per-repo configuration that these skills assume:

- **Issue tracker** — where issues live (GitHub, GitLab, or local markdown)
- **Domain docs** — where `CONTEXT.md` and ADRs live
- **Review base** — default branch for code review comparisons

## Process

### 1. Explore

Look at the current repo to understand its starting state:

- `git remote -v` and `.git/config` — is this a GitHub repo?
- `CONTEXT.md` at the repo root
- `docs/adr/` directory
- `AGENTS.md` or `CLAUDE.md` at the repo root

### 2. Ask and configure

Present findings and ask one section at a time.

**Section A — Issue tracker.**

> Where does this repo track issues? Skills like `issue-triage`, `issue-decomposer`, and `prd-review` read from the issue tracker.

- **GitHub** (recommended if remote is GitHub)
- **GitLab** (recommended if remote is GitLab)
- **Local markdown** — issues as files under `.scratch/`
- **Other** (describe the workflow)

Write the choice to `docs/agents/issue-tracker.md`.

**Section B — Domain docs.**

> Where should domain documentation live? Default: `CONTEXT.md` and `docs/adr/` at the repo root.

Write the layout to `docs/agents/domain.md`.

**Section C — Review base.**

> What branch do you compare against for code reviews? (default: `main`)

Write to `docs/agents/review-base.md` if non-default.

### 3. Write

Write a `## Agent skills` block to `AGENTS.md` or `CLAUDE.md` (whichever exists, or ask which to create).

### 4. Done

Tell the user setup is complete and which skills will use the configuration. They can edit `docs/agents/*.md` directly later.
