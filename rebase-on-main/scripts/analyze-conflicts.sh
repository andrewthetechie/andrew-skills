#!/usr/bin/env bash
set -euo pipefail

if ! git rev-parse --is-inside-work-tree >/dev/null 2>&1; then
  echo "Not inside a Git repository." >&2
  exit 1
fi

conflicts="$(git diff --name-only --diff-filter=U || true)"
if [ -z "$conflicts" ]; then
  echo "No unmerged files detected."
  git status --short --branch
  exit 0
fi

echo "Unmerged files:"
printf '%s\n' "$conflicts"
echo

printf '%s\n' "$conflicts" | while IFS= read -r file; do
  [ -n "$file" ] || continue
  echo "== $file =="
  git status --short -- "$file"
  markers="$(grep -nE '^(<<<<<<<|=======|>>>>>>>)' -- "$file" || true)"
  if [ -n "$markers" ]; then
    echo "$markers"
  else
    echo "No textual conflict markers found. This may be a binary, delete/delete, rename, or mode conflict."
  fi
  echo
done

echo "Rebase state:"
git status --short --branch
echo
echo "Next step: read each file, resolve intentionally, git add resolved files, then git rebase --continue."
