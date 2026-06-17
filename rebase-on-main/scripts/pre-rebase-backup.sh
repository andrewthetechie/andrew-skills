#!/usr/bin/env bash
set -euo pipefail

if ! git rev-parse --is-inside-work-tree >/dev/null 2>&1; then
  echo "Not inside a Git repository." >&2
  exit 1
fi

branch="$(git rev-parse --abbrev-ref HEAD)"
if [ "$branch" = "HEAD" ]; then
  echo "Detached HEAD. Refusing to create a branch backup without a current branch." >&2
  exit 1
fi

timestamp="$(date +%Y%m%d_%H%M%S)"
safe_branch="$(printf '%s' "$branch" | tr '/[:space:]' '--')"
backup="backup/rebase-${safe_branch}-${timestamp}"

git branch "$backup"

echo "Created backup branch: $backup"
echo "Current branch: $branch"
echo "Current commit: $(git rev-parse --short HEAD)"
echo "Recover with: git switch $backup"
