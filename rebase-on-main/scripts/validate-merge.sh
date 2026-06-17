#!/usr/bin/env bash
set -euo pipefail

if ! git rev-parse --is-inside-work-tree >/dev/null 2>&1; then
  echo "Not inside a Git repository." >&2
  exit 1
fi

failed=0

if git diff --name-only --diff-filter=U | grep . >/dev/null 2>&1; then
  echo "Unmerged files remain:" >&2
  git diff --name-only --diff-filter=U >&2
  failed=1
fi

tracked_files="$(git diff --name-only --cached && git diff --name-only)"
if [ -n "$tracked_files" ]; then
  marker_hits="$(printf '%s\n' "$tracked_files" | sort -u | while IFS= read -r file; do
    [ -f "$file" ] || continue
    grep -nE '^(<<<<<<<|=======|>>>>>>>)' -- "$file" || true
  done)"
  if [ -n "$marker_hits" ]; then
    echo "Conflict markers remain:" >&2
    echo "$marker_hits" >&2
    failed=1
  fi
fi

if ! git diff --check; then
  failed=1
fi

if [ "$failed" -ne 0 ]; then
  echo "Merge validation failed." >&2
  exit 1
fi

echo "Merge validation passed: no unmerged files, no conflict markers, and git diff --check is clean."
