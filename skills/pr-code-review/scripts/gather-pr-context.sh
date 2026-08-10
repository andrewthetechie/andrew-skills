#!/usr/bin/env bash
set -euo pipefail

fail() {
  printf 'gather-pr-context: %s\n' "$1" >&2
  exit 1
}

[[ $# -eq 1 ]] || fail 'usage: gather-pr-context.sh <github-pr-url>'
command -v gh >/dev/null 2>&1 || fail 'gh is required'
command -v jq >/dev/null 2>&1 || fail 'jq is required'

input_url=${1%%#*}
input_url=${input_url%%\?*}
input_url=${input_url%/}

if [[ $input_url =~ ^https?://([^/]+)/([^/]+)/([^/]+)/pull/([0-9]+)(/.*)?$ ]]; then
  host=${BASH_REMATCH[1]}
  owner=${BASH_REMATCH[2]}
  repository=${BASH_REMATCH[3]}
  number=${BASH_REMATCH[4]}
else
  fail 'expected a GitHub pull request URL'
fi

context_dir=$(mktemp -d "${TMPDIR:-/tmp}/code-review-pr.XXXXXX")
metadata_path="$context_dir/pull-request.json"
diff_path="$context_dir/diff.patch"
commit_pages_path="$context_dir/commit-pages.json"
commits_json_path="$context_dir/commits.json"
commits_path="$context_dir/commits.txt"
issue_pages_path="$context_dir/closing-issue-pages.json"
issues_path="$context_dir/closing-issues.json"
spec_path="$context_dir/spec.md"
manifest_path="$context_dir/manifest.json"
endpoint="repos/$owner/$repository/pulls/$number"

gh api --hostname "$host" "$endpoint" >"$metadata_path"
jq -e '
  .number and .html_url and .title and
  .base.ref and .base.sha and .head.ref and .head.sha
' "$metadata_path" >/dev/null || fail 'pull request metadata is incomplete'

gh api \
  --hostname "$host" \
  -H 'Accept: application/vnd.github.diff' \
  "$endpoint" >"$diff_path"
[[ -s $diff_path ]] || fail 'pull request diff is empty'

gh api \
  --hostname "$host" \
  --paginate \
  --slurp \
  "$endpoint/commits?per_page=100" >"$commit_pages_path"
jq '[.[][]]' "$commit_pages_path" >"$commits_json_path"
jq -r '.[] | "\(.sha[0:12]) \(.commit.message | split("\n")[0])"' \
  "$commits_json_path" >"$commits_path"

# GraphQL variables expand on the server.
# shellcheck disable=SC2016
closing_issues_query='
query($owner: String!, $repository: String!, $number: Int!, $endCursor: String) {
  repository(owner: $owner, name: $repository) {
    pullRequest(number: $number) {
      closingIssuesReferences(first: 100, after: $endCursor) {
        nodes { number title body url }
        pageInfo { hasNextPage endCursor }
      }
    }
  }
}'

gh api graphql \
  --hostname "$host" \
  --paginate \
  --slurp \
  -F owner="$owner" \
  -F repository="$repository" \
  -F number="$number" \
  -f query="$closing_issues_query" >"$issue_pages_path"

jq -e 'all(.[]; ((.errors // []) | length) == 0)' \
  "$issue_pages_path" >/dev/null || fail 'GitHub returned a GraphQL error'
jq '[.[].data.repository.pullRequest.closingIssuesReferences.nodes[]]' \
  "$issue_pages_path" >"$issues_path"
issue_count=$(jq 'length' "$issues_path")

{
  printf '# Closing issues\n\n'
  if (( issue_count == 0 )); then
    printf '_No closing issues are linked to this pull request._\n'
  else
    jq -r '
      .[] |
      "## #\(.number): \(.title)\n\nSource: \(.url)\n\n" +
      (if (.body | length) == 0 then "_No description provided._" else .body end) +
      "\n"
    ' "$issues_path"
  fi
} >"$spec_path"

jq -n \
  --arg provider 'github' \
  --arg context_dir "$context_dir" \
  --arg host "$host" \
  --arg repository "$owner/$repository" \
  --argjson number "$number" \
  --arg url "$(jq -r '.html_url' "$metadata_path")" \
  --arg title "$(jq -r '.title' "$metadata_path")" \
  --arg base_ref "$(jq -r '.base.ref' "$metadata_path")" \
  --arg base_oid "$(jq -r '.base.sha' "$metadata_path")" \
  --arg head_ref "$(jq -r '.head.ref' "$metadata_path")" \
  --arg head_oid "$(jq -r '.head.sha' "$metadata_path")" \
  --arg diff "$diff_path" \
  --arg commits "$commits_path" \
  --arg spec "$spec_path" \
  --arg issues "$issues_path" \
  --argjson closing_issue_count "$issue_count" \
  '{
    schema_version: 1,
    provider: $provider,
    context_dir: $context_dir,
    host: $host,
    repository: $repository,
    number: $number,
    url: $url,
    title: $title,
    base: {ref: $base_ref, oid: $base_oid},
    head: {ref: $head_ref, oid: $head_oid},
    closing_issue_count: $closing_issue_count,
    artifacts: {
      diff: $diff,
      commits: $commits,
      spec: $spec,
      closing_issues: $issues
    }
  }' >"$manifest_path"

jq -c . "$manifest_path"
