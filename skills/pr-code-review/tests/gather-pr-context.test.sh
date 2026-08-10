#!/usr/bin/env bash
set -euo pipefail

skill_dir=$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)
test_dir=$(mktemp -d "${TMPDIR:-/tmp}/gather-pr-context-test.XXXXXX")
trap 'rm -rf "$test_dir"' EXIT
mkdir -p "$test_dir/bin" "$test_dir/output"

cat >"$test_dir/bin/gh" <<'MOCK_GH'
#!/usr/bin/env bash
set -euo pipefail

[[ ${1:-} == api ]] || exit 70
shift

if [[ ${1:-} == graphql ]]; then
  if [[ ${MOCK_NO_ISSUES:-0} == 1 ]]; then
    printf '%s\n' '[{"data":{"repository":{"pullRequest":{"closingIssuesReferences":{"nodes":[],"pageInfo":{"hasNextPage":false,"endCursor":null}}}}}}]'
  else
    printf '%s\n' '[{"data":{"repository":{"pullRequest":{"closingIssuesReferences":{"nodes":[{"number":7,"title":"First requirement","body":"Build the first behavior.","url":"https://github.com/acme/widgets/issues/7"},{"number":9,"title":"Second requirement","body":"Preserve the second behavior.","url":"https://github.com/acme/widgets/issues/9"}],"pageInfo":{"hasNextPage":false,"endCursor":null}}}}}}]'
  fi
  exit 0
fi

arguments=" $* "
if [[ $arguments == *' application/vnd.github.diff '* ]]; then
  printf '%s\n' 'diff --git a/a.txt b/a.txt' '--- a/a.txt' '+++ b/a.txt' '@@ -1 +1 @@' '-old' '+new'
elif [[ $arguments == *' repos/acme/widgets/pulls/42/commits?per_page=100 '* ]]; then
  printf '%s\n' '[[{"sha":"1234567890abcdef","commit":{"message":"Implement behavior\n\nDetails"}}]]'
elif [[ $arguments == *' repos/acme/widgets/pulls/42 '* ]]; then
  printf '%s\n' '{"number":42,"html_url":"https://github.com/acme/widgets/pull/42","title":"Factory refactor","base":{"ref":"main","sha":"base123"},"head":{"ref":"factory","sha":"head456"}}'
else
  exit 71
fi
MOCK_GH
chmod +x "$test_dir/bin/gh"

manifest=$(TMPDIR="$test_dir/output" PATH="$test_dir/bin:$PATH" \
  "$skill_dir/scripts/gather-pr-context.sh" \
  'https://github.com/acme/widgets/pull/42/files?diff=split')
context_dir=$(jq -r '.context_dir' <<<"$manifest")

jq -e '
  .provider == "github" and
  .repository == "acme/widgets" and
  .number == 42 and
  .base.oid == "base123" and
  .head.oid == "head456" and
  .closing_issue_count == 2 and
  (.context_dir | length > 0)
' <<<"$manifest" >/dev/null
rg -q '^diff --git a/a.txt b/a.txt$' "$context_dir/diff.patch"
rg -q '^1234567890ab Implement behavior$' "$context_dir/commits.txt"
rg -q '^## #7: First requirement$' "$context_dir/spec.md"
rg -q '^Build the first behavior\.$' "$context_dir/spec.md"
rg -q '^## #9: Second requirement$' "$context_dir/spec.md"

empty_manifest=$(MOCK_NO_ISSUES=1 TMPDIR="$test_dir/output" \
  PATH="$test_dir/bin:$PATH" \
  "$skill_dir/scripts/gather-pr-context.sh" \
  'https://github.com/acme/widgets/pull/42')
empty_context_dir=$(jq -r '.context_dir' <<<"$empty_manifest")
jq -e '.closing_issue_count == 0' <<<"$empty_manifest" >/dev/null
rg -q '^_No closing issues are linked to this pull request\._$' \
  "$empty_context_dir/spec.md"

if PATH="$test_dir/bin:$PATH" "$skill_dir/scripts/gather-pr-context.sh" \
  'https://example.com/not-a-pr' >/dev/null 2>&1; then
  printf 'invalid URL unexpectedly succeeded\n' >&2
  exit 1
fi

printf 'gather-pr-context tests passed\n'
