---
name: rebase-on-main
description: Safely rebase the current Git branch onto the repository's mainline branch with backups, conflict analysis, validation, and force-with-lease pushing. Use when the user asks to rebase, sync, update, replay, or force-push a feature branch on top of main or master.
---

# Rebase On Main

## Non-Negotiables

- Prefer safety over completion. If resolving a conflict could overwrite work, remove functionality, or requires product/code intent you cannot infer, stop and ask the user a specific question.
- Always create a backup before rewriting history.
- Always use `--force-with-lease`, never `--force`.
- Do not rebase shared branches, protected branches, or branches with unknown ownership unless the user explicitly approves.
- Preserve functionality from both sides when possible. Never silently drop behavior from either mainline or the feature branch.
- Before a normal rebase or `git rebase --continue`, set `GIT_EDITOR=true`. Keep it set through the rebase so Git accepts the existing commit message instead of opening vim, nano, or another interactive editor.
- Report what changed at the end: target branch, commits rebased, conflicts resolved, validation run, and push result.

## Quick Start

```bash
export GIT_EDITOR=true
bash scripts/pre-rebase-backup.sh
git fetch origin
git rebase origin/main
bash scripts/analyze-conflicts.sh
# Resolve conflicts intelligently, then:
git add <resolved-files>
git rebase --continue
bash scripts/validate-merge.sh
git push origin "$(git rev-parse --abbrev-ref HEAD)" --force-with-lease
```

Use `origin/master` instead of `origin/main` only when master is the repository mainline.

## Workflow

1. Establish context:
   - Run `git status --short --branch`.
   - Save the current branch with `git rev-parse --abbrev-ref HEAD`.
   - Refuse to proceed from detached HEAD.
   - Identify mainline from `origin/HEAD`, then fall back to `origin/main`, `origin/master`, `main`, or `master`.

2. Check safety:
   - Run `bash scripts/pre-rebase-backup.sh`.
   - If the working tree has unrelated uncommitted changes, stop and ask before stashing or modifying them.
   - Fetch latest with `git fetch origin`.
   - Inspect divergence with `git log --oneline <target>..HEAD` and `git log --oneline HEAD..<target>`.

3. Choose strategy:
   - Use simple rebase for 1-2 straightforward commits.
   - Use squash-first for 3+ commits or repeated conflicts if the user is willing to trade per-commit history for one conflict-resolution pass.
   - Use interactive rebase when commit order, duplicate commits, or focused cleanup matters.
   - See [references/strategies.md](references/strategies.md).

4. Rebase:
   - Prefer `git rebase <target>` where target is usually `origin/main`.
   - If conflicts occur, run `bash scripts/analyze-conflicts.sh`.
   - Read every conflicted file before editing. Understand `ours` and `theirs` in rebase context before choosing.
   - Resolve by combining intent where possible; do not blindly choose either side.
   - If the correct result is ambiguous, stop and ask the user rather than guessing.
   - Stage resolved files and continue with `git rebase --continue`.
   - Repeat until the rebase completes.

5. Validate:
   - Run `bash scripts/validate-merge.sh`.
   - Run project-specific checks discovered from the repo, such as tests, lint, typecheck, or targeted tests for changed areas.
   - If validation fails, fix the merged code before continuing or pushing.

6. Push:
   - Push only after validation: `git push origin "$(git rev-parse --abbrev-ref HEAD)" --force-with-lease`.
   - If `--force-with-lease` fails, stop. Someone else may have pushed to the branch.

## Conflict Resolution Rules

- Keep mainline fixes such as security, migrations, API changes, dependency updates, and bug fixes unless there is a clear reason not to.
- Keep feature-branch behavior that implements the user's work unless it is made obsolete by mainline.
- Remove duplicate code created by combining both sides.
- Add short comments only when the merged logic would otherwise be unclear.
- Do not continue a rebase with unresolved conflict markers, failing syntax checks, or unexplained test failures.

## Recovery

- Abort an unsafe rebase with `git rebase --abort`.
- Recover from the backup branch created by `scripts/pre-rebase-backup.sh`.
- See [references/troubleshooting.md](references/troubleshooting.md) for repeated conflicts, bad resolutions, and force-with-lease failures.

