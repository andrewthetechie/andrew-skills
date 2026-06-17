# Conflict Resolution

## Rebase Context

During a rebase, conflict labels can be counterintuitive:

- `ours` / `HEAD` is the branch state you are rebasing onto, usually `origin/main`.
- `theirs` is the commit from the feature branch currently being replayed.

Verify with `git status` and the current rebase message before choosing a side.

## Decision Framework

1. Identify what mainline changed and why.
2. Identify what the feature branch changed and why.
3. Preserve both when they are compatible.
4. Prefer mainline for platform-wide changes such as security fixes, migrations, renamed APIs, generated files, and dependency updates.
5. Prefer feature logic for the user's intended behavior unless mainline made it obsolete.
6. Stop and ask if a choice would remove functionality, change behavior silently, or rely on unknown domain intent.

## Common Patterns

- Same function edited on both sides: combine validation, side effects, and return behavior intentionally; remove duplicate calls.
- File renamed on one side and edited on the other: keep the rename if it matches current structure, then apply the edits to the renamed file.
- Dependency or lockfile conflict: preserve required dependencies from both sides, then regenerate the lockfile with the project package manager when possible.
- Generated files: regenerate instead of hand-merging if the repo provides a deterministic generator.
- Deleted on one side, edited on the other: ask if unsure. Deletion often signals a replacement or architectural move.

## Required Checks Before Continue

Before `git rebase --continue`:

- No conflict markers remain.
- `git diff --check` passes.
- The resolved file still contains the important behavior from both sides or the reason for dropping behavior is explicit.
- Relevant syntax, type, lint, or test commands have been run when available.
