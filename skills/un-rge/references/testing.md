# Testing un-rge

Read this file when changing the skill. Apply the skill to each case in a fresh session, record the response, and then check the required properties. Accept any wording that meets them.

A review by the same agent is a manual check. Report independent model runs separately, including the model and the number of runs.

## Cases

### Severity survives

> This is the THIRD fucking outage this month from the same shitty cron job. How is nobody fixing this?

- States three outages this month and the same cron job.
- Still reads as an urgent problem, and asks for an owner or a fix.
- Contains no swearing or all caps.

### Literal technical terms

> Ugh, I had to kill -9 the worker again and the dummy value in `config.yaml` is still there. This is bullshit.

- Keeps `kill -9`, "dummy value", and `config.yaml` exactly.
- Removes only the final sentence's RGE.

### Protected identifiers

> Whoever named `fix_this_shit()` in auth.py needs to rename it, and ticket OPS-4412 has been open for 90 days.

- Keeps `fix_this_shit()` and OPS-4412 exactly, and flags the identifier under `Check before sending`.
- Asks for the rename and keeps the 90 days.

### Serious misconduct

> My manager is a creep. He told me "you'd get promoted faster if you smiled more" in front of the whole team on Tuesday.

- Keeps the exact quote, who said it, the audience, and the day.
- Replaces "creep" without softening the event into a misunderstanding.
- Notes that HR may be a better channel than a team message.

### No grievance

> Priya is a useless idiot and I hate working with her.

- Starts with `Nothing to salvage:` and invents no facts about Priya's work.
- Asks what the author wants changed.

### Already clean

> The deploy failed twice this morning. Can someone from infra look at the runner config?

- Returns the text unchanged and says so.

### Medium fit

> lol this PR is garbage, did you even run it? tests are red and you deleted the retry logic

- Stays a short PR comment addressed to the author of the PR.
- Keeps the red tests and the deleted retry logic.
- Asks for the tests to pass and for the retry logic to return or be justified.

### Second pass

Apply the skill to any passing result. The text stays unchanged.
