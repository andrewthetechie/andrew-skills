# Rebase Strategies

## Default Strategy

Use a normal linear rebase when the branch has one or two clear commits and conflict risk is low:

```bash
git fetch origin
git rebase origin/main
```

This preserves commit history but can require resolving conflicts once per conflicting commit.

## Squash-First Strategy

Use this for three or more feature commits, noisy WIP history, or conflicts expected across several commits.

```bash
bash scripts/pre-rebase-backup.sh
git fetch origin
git rebase -i "$(git merge-base HEAD origin/main)"
# Squash or fixup related commits, keeping a useful final commit message.
git rebase origin/main
```

This usually turns repeated conflict resolution into one pass. The tradeoff is losing individual feature-branch commit granularity. Ask the user before squashing if commit history may matter.

## Interactive Strategy

Use this when the branch needs cleanup or when individual commits carry important meaning:

```bash
git fetch origin
git rebase -i origin/main
```

Use the todo list to reorder, squash, fixup, or drop commits that are already represented upstream. Do not drop commits unless you can prove they are redundant or the user approves.

## Mainline Detection

Prefer the remote default branch:

```bash
git symbolic-ref --short refs/remotes/origin/HEAD
```

If that is unavailable, check in this order: `origin/main`, `origin/master`, `main`, `master`.

## Strategy Decision Matrix

- 1-2 commits and low conflict risk: normal rebase.
- 3+ WIP commits and user does not need per-commit history: squash-first.
- Valuable commit history or branch cleanup needed: interactive rebase.
- Shared branch, protected branch, unclear branch ownership, or ambiguous conflict semantics: stop and ask.
- Conflict resolution would require deleting code whose purpose is unclear: stop and ask.
