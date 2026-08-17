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

## Locate Bundled Helpers

The scripts below belong to this skill, not to the repository being rebased. Before changing into the target repository, take the absolute path of this loaded `SKILL.md` from the harness's skill context and derive `SKILL_DIR` from it. Never run `bash scripts/...` from the target repository or hard-code a machine-specific skills directory.

```bash
# Substitute the absolute SKILL.md path reported by the current harness.
SKILL_FILE="<path reported for this loaded SKILL.md>"
SKILL_DIR="$(CDPATH= cd -- "$(dirname -- "$SKILL_FILE")" && pwd -P)"
```

Confirm the helpers exist before invoking them. If the harness does not expose a skill path or a helper is unavailable, use the inline fallback in the relevant workflow step; do not stop solely to find the scripts.

## Quick Start

```bash
export GIT_EDITOR=true
bash "$SKILL_DIR/scripts/pre-rebase-backup.sh"
git fetch origin
git rebase origin/main
bash "$SKILL_DIR/scripts/analyze-conflicts.sh"
# Resolve conflicts intelligently, then:
git add <resolved-files>
git rebase --continue
bash "$SKILL_DIR/scripts/validate-merge.sh"
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
   - Run `bash "$SKILL_DIR/scripts/pre-rebase-backup.sh"` when available. Otherwise create the backup inline:

     ```bash
     branch="$(git rev-parse --abbrev-ref HEAD)"
     timestamp="$(date +%Y%m%d_%H%M%S)"
     safe_branch="$(printf '%s' "$branch" | tr '/[:space:]' '--')"
     backup="backup/rebase-${safe_branch}-${timestamp}"
     git branch "$backup"
     ```
   - If the working tree has unrelated uncommitted changes, stop and ask before stashing or modifying them.
   - Fetch latest with `git fetch origin`.
   - Inspect divergence with `git log --oneline <target>..HEAD` and `git log --oneline HEAD..<target>`.

3. Choose strategy:
   - Use simple rebase for 1-2 straightforward commits.
   - Use squash-first for 3+ commits or repeated conflicts if the user is willing to trade per-commit history for one conflict-resolution pass.
   - Use interactive rebase when commit order, duplicate commits, or focused cleanup matters.
   - See [references/strategies.md](references/strategies.md).

### Squash First

Use this only when the user explicitly asks to squash, or has accepted squashing. After fetching and selecting `<target>`, squash all feature commits since the merge base into one local commit, then rebase that commit onto the updated target:

```bash
base="$(git merge-base HEAD <target>)"
git log --oneline "$base"..HEAD
git reset --soft "$base"
git commit -m "<concise summary of the squashed feature>"
git rebase <target>
```

Run the backup helper before `git reset --soft`. Do not use this path if the displayed range contains commits the user intends to retain separately. If the final message cannot be inferred from the commits, ask the user for it.

4. Rebase:
   - Prefer `git rebase <target>` where target is usually `origin/main`.
   - If conflicts occur, run `bash "$SKILL_DIR/scripts/analyze-conflicts.sh"` when available; otherwise run `git diff --name-only --diff-filter=U` and `git status --short --branch`.
   - Read every conflicted file before editing. Understand `ours` and `theirs` in rebase context before choosing.
   - Resolve by combining intent where possible; do not blindly choose either side.
   - If the correct result is ambiguous, stop and ask the user rather than guessing.
   - Stage resolved files and continue with `git rebase --continue`.
   - Repeat until the rebase completes.

5. Validate:
   - Run `bash "$SKILL_DIR/scripts/validate-merge.sh"` when available. Otherwise run `git diff --check`, ensure `git diff --name-only --diff-filter=U` is empty, and inspect changed files for conflict markers.
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
- Recover from the backup branch created by the helper or inline backup command.
- See [references/troubleshooting.md](references/troubleshooting.md) for repeated conflicts, bad resolutions, and force-with-lease failures.

