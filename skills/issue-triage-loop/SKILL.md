---
name: issue-triage-loop
description: Batch-process issues through improve → triage → retitle, one subagent per issue, sequentially. Invoke with the issue tracker CLI, project identifier, and issue selection criteria.
disable-model-invocation: true
---

# Issue Triage Loop

A relay: each issue runs its own subagent leg — improve, triage, retitle — one at a time, so the main context never accumulates per-issue state.

## Orient

Establish before starting:

- **Tracker CLI** — tool and invocation pattern (e.g. `gh` for GitHub, `glab` for GitLab, or any user-provided CLI)
- **Project** — repo or project reference (e.g. `owner/repo` for GitHub, `group/project` for GitLab)
- **Commands** — how to: fetch an issue with its body and labels; update its body; update its labels; post a comment; update its title
- **Selection** — which issues to process: a numeric range, a label filter, "all open", or any expression the CLI supports

Ask for any missing piece before continuing. Do not guess CLI syntax — wrong commands silently corrupt issues.

## Enumerate

In the main context, run the CLI to fetch every issue ID matching the selection. Produce an ordered list.

Confirm the count with the user before starting the relay.

Completion criterion: every matching issue ID is in the list and the user has confirmed.

## Relay

For each issue ID in order:

1. Fill in the relay brief below with this issue's CLI context.
2. Spawn one subagent with that brief.
3. Wait for it to finish before continuing.
4. Log the result — issue ID, outcome, new title — before moving to the next.

### Relay brief template

Fill every `{PLACEHOLDER}` before sending.

```
You are processing issue {ISSUE_ID} in {PROJECT} using {CLI_TOOL}.

CLI commands for this issue:
  Fetch:          {GET_COMMAND}
  Update body:    {UPDATE_BODY_COMMAND}
  Update labels:  {UPDATE_LABELS_COMMAND}
  Add comment:    {ADD_COMMENT_COMMAND}
  Update title:   {UPDATE_TITLE_COMMAND}

Fetch the issue now (body, title, current labels). Then run these three steps in order. Complete each step fully before starting the next.

Step 1 — Improve
Invoke the issue-improver skill on the fetched issue body. Apply its output by updating the issue body in place using the update-body command.
Done when: the issue body on the tracker matches the improver's output.

Step 2 — Triage
Invoke the issue-triage skill on the issue. Apply its output: update the issue's labels using the update-labels command; post the triage output as a comment using the add-comment command.
Done when: labels are updated and the triage comment is posted on the tracker.

Step 3 — Retitle
Read the current issue (improved body, triage comment). Write a new title as a conventional commits message: type(scope): description. Update the title using the update-title command.
Done when: the title on the tracker is a valid conventional commits message.

Return one line: issue ID | old title | new title | labels applied
```

## Wrap up

After all issues: report total processed, any failures with issue IDs and error details.

