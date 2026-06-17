# Troubleshooting

## Rebase Is Going Wrong

Abort safely:

```bash
git rebase --abort
```

Return to the backup branch if needed:

```bash
git switch <backup-branch>
```

The backup branch name is printed by `scripts/pre-rebase-backup.sh`.

## Same Conflicts Repeat

Consider enabling rerere:

```bash
git config rerere.enabled true
```

This records conflict resolutions and can replay them for repeated conflicts. Still review each replayed resolution before continuing.

## Force-With-Lease Fails

Stop. The remote branch moved after your fetch or someone else pushed. Run:

```bash
git fetch origin
git log --oneline HEAD..origin/$(git rev-parse --abbrev-ref HEAD)
```

Ask the user before overwriting or incorporating someone else's branch updates.

## Local Changes Block Checkout Or Rebase

Do not auto-stash unrelated work unless the user asked for it. Report the files and ask whether to commit, stash, or leave them alone.

## Conflict Seems Ambiguous

Stop and ask a concrete question. Include:

- The file.
- The two behaviors in conflict.
- The likely safe merge if one exists.
- The risk of choosing incorrectly.
