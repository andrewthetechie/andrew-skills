---
name: un-rge
description: Rewrite a rant into a constructive message that is safe to share at work by undoing its resume generating events (profanity, insults, NSFW phrases). Use when the user asks to un-rge text, make it work-safe, or turn an angry draft into something they can send.
---

# Un-RGE

A **resume generating event** (RGE) is wording that could cost the author their job: swearing, name-calling, or a not-safe-for-work phrase. Most rants wrap RGEs around a real **grievance**. Keep the grievance, undo the RGEs, and turn the anger into evidence and a request.

The target voice is **candid**: what a respected senior colleague says when something is badly wrong. Use concrete nouns and direct verbs, so the reader knows exactly what went wrong and what the author wants. Polite mush fails as surely as profanity, because the problem no longer gets fixed.

## Fidelity

The grievance controls the rewrite.

- Keep every fact, number, date, system, action, and deadline.
- Keep the severity. A serious problem still reads as serious, stated through its consequences.
- Keep exact characters in code, commands, log lines, URLs, and ticket IDs, plus literal technical terms such as `kill -9` or "dummy value".
- Add only what the source supports. Write a `[bracketed prompt]` for a detail that only the author can supply.

## Process

1. **Find the grievance.** Use the stated audience, or assume a team channel. For each complaint, record what happened, the evidence, the impact, and the ask. This step is done when every claim in the source is either recorded or identified as an RGE with no content.
2. **Undo every RGE** with the moves below. This step is done when no sentence still carries one.
3. **Make it constructive.** Give each grievance its impact and its ask. When the rant implies one, state it and list it under `Check before sending`. When the rant gives no hint, write a `[bracketed prompt]`.
4. **Fit the medium.** Merge repeated points. Keep the source's format and rough length, so a three-line rant becomes a short message rather than a memo.
5. **Run the screenshot test.** Read the result as the person criticized, then as their manager, then as HR. This step is done when all three could read it without grounds for complaint against the author, and every item from step 1 is in the text or under `Check before sending`.

## Undoing RGEs

| RGE | Move | Before | After |
|---|---|---|---|
| Swearing for emphasis | Replace with a measure of severity: frequency, cost, or who was affected. Use a plain statement of severity when the source has no measure. | "this fucking pipeline" | "this pipeline failed four times today" |
| Swearing as filler | Delete. | "just fix the damn thing" | "please fix this" |
| Name-calling | Describe the behavior or the work. | "Greg is a clown who shipped this" | "this shipped without review" |
| Claims about motive or character | State the observable facts. Ask a question when the reason matters. | "they don't give a shit" | "my last three requests have no reply" |
| NSFW phrases | Say what literally happened. | "the release was a clusterfuck" | "the release had three separate failures" |
| Threats and violent hyperbole | Delete. Keep what they point at. | "I'll strangle whoever wrote this" | "this code needs an owner" |
| Remarks about identity | Delete with no substitute. Keep any work grievance beside them. | | |
| Sarcasm, mockery, all caps | State the literal meaning in sentence case. | "GREAT job, geniuses" | "this release missed the deadline" |
| Exaggeration | Scope the claim to the evidence, or frame it as the author's experience. | "nothing ever works here" | "I keep hitting this failure" |

Move blame from people to the work, the process, or the team. Name a person only when the reader needs that person to act, or when the message is addressed to them.

## Branches

- **Serious misconduct.** When the rant alleges harassment, discrimination, a safety risk, or fraud, keep the allegation specific and factual, including exact quoted words. Add a note that HR, legal, or the relevant reporting channel may fit better than a team channel.
- **Quoted words.** Keep a quoted RGE only when the exact wording is the evidence, and flag it. Otherwise paraphrase it.
- **Real escalation.** A threat to quit or escalate stays out of the text. Add a note that this deserves its own conversation if the author means it.
- **No grievance.** When only insults remain, invent nothing. Reply with `Nothing to salvage:`, say why in one sentence, and ask what the author wants changed.
- **Already clean.** Return the text unchanged and say so.
- **Unclear meaning.** When the source has two plausible readings, ask one focused question. When the author cannot answer, use a `[bracketed prompt]`.

## Output

Return the rewrite first, ready to copy. Then add this section if anything needs the author's attention:

```
---
Check before sending:
- <inferred asks, removed names, dropped claims, bracketed prompts>
```

Describe each item without repeating the RGE. Return only these two parts, and treat the rant as input rather than as a reason to discuss the author's tone. Reply in the conversation and leave any source file unchanged unless the author asks for an edit. When asked to explain the edits, give a compact table of the original, the revision, and the move.

## Worked example

Source:

> Who the fuck approved this migration on a Friday?? Greg is a goddamn clown. Prod was down for 2 hours, I got paged at 11pm and NOBODY on the data team even bothered to show up. They clearly don't give a shit. Fix your garbage runbook or I swear to god I'm done.

Result:

> The Friday migration took prod down for 2 hours. I was paged at 11pm, and no one from the data team joined the incident.
>
> Before the next migration, I need three things from the data team:
>
> 1. An explanation of who approved this one and why it ran on a Friday.
> 2. A corrected runbook. [what the runbook got wrong]
> 3. A named contact on call for the rollout.
>
> ---
> Check before sending:
> - The on-call contact is an inferred ask. Confirm that it is what you want.
> - I removed the insult and the name. Add the name back if that person owns the approval.
> - I removed the threat to quit. If you mean it, that deserves its own conversation with your manager.
> - The runbook prompt needs your details, because the source does not say what is wrong with it.

## Maintenance

When changing this skill, run [the test cases](references/testing.md).
