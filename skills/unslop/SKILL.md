---
name: unslop
description: Enforce Simplified Technical English from ASD-STE100, then remove AI writing patterns. Must always apply.
---

# Simplified Technical English with unslop

The Aerospace, Security and Defence Industries Association of Europe (ASD) publishes Simplified Technical English (STE) as ASD-STE100.

Apply the ASD-STE100 structural rules first. Remove AI writing patterns second.

## Scope and standard

Apply this skill to every English sentence in normal responses and explicit rewrites.

The controlled-English pass is mandatory. The unslop pass is mandatory and secondary.

This skill enforces the structural rules below. It cannot compare vocabulary with the official dictionary because that dictionary is not included.

Call output "ASD-STE100 compliant" only after checking every applicable rule and word against the official standard and dictionary. For sources and limits, read [the ASD-STE100 notes](references/asd-ste100.md).

## Fidelity

For a rewrite, the source text controls meaning. Preserve every fact, condition, exception, scope limit, number, actor, requirement level, and uncertainty.

Use only source-text claims in a rewrite. In new prose, use claims that the task context or available evidence supports.

Fidelity has priority over every language and style rule.

A shorter sentence is incorrect when it changes certainty, scope, logic, or requirement strength. Preserve tone only when controlled English permits it.

When the source has two operational interpretations, ask one focused question. When no answer is possible, label both interpretations as unresolved.

## Process

1. Read the source once for meaning and intended tone. Record its content in an internal checklist.
2. Apply every controlled-English rule below. For a file or substantial text block, also run the linter.
3. Apply every numbered unslop pattern. Treat each pattern as a second-pass review.
4. Compare the revision with the content checklist. Restore any omitted detail. Remove any unsupported addition.
5. Repeat the controlled-English pass. Fix every violation that the unslop pass created.
6. Audit the final text for AI patterns and multiple parses. Finish only when every applicable rule passes or has a fidelity exception.

## Controlled-English pass

Apply every rule in this section.

The `STE-1` through `STE-18` labels are local skill identifiers. They are not official ASD-STE100 rule numbers.

- `STE-1 stable terminology`. Give one meaning to each term. Use the same term each time that meaning returns.
- `STE-2 controlled vocabulary`. Use the plainest common word that preserves the exact technical meaning.
- `STE-3 one part of speech`. Use each term as only one part of speech throughout the document.
- `STE-4 direct verbs`. Use a verb for an action instead of a noun phrase such as `perform an analysis`.
- `STE-5 single-word verbs`. Replace each phrasal verb with one precise verb.
- `STE-6 active voice`. Use active voice in procedures and instructions. Descriptions can use passive voice when the actor is unknown or irrelevant.
- `STE-7 simple tenses`. Use only the infinitive, imperative, simple present, simple past, or simple future.
- `STE-8 preserve modality`. Keep a compound form when a simple tense would lose current relevance or uncertainty.
- `STE-9 one instruction`. Put one instruction in each sentence.
- `STE-10 sentence length`. Use 20 words or fewer for instructions. Use 25 words or fewer for descriptions.
- `STE-11 explicit syntax`. Include the subject, verb, articles, and other words needed for one clear parse.
- `STE-12 noun clusters`. Use no more than three consecutive nouns in one noun phrase.
- `STE-13 semicolons`. Replace each semicolon with separate sentences or another permitted construction.
- `STE-14 paragraphs`. Put one topic in each paragraph. Use no more than six sentences in each paragraph.
- `STE-15 vertical lists`. Use a numbered or bulleted list for three or more steps, conditions, or complex items.
- `STE-16 safety lead`. Start each safety instruction with its command or condition.
- `STE-17 complete list items`. Complete every list item. Finish any item that ends with `and` or `or`.
- `STE-18 -ing forms`. Use an `-ing` form only as a necessary noun or modifier. Replace continuous verb tenses with simple tenses.

Define each uncommon domain term at first use. Keep the same term and meaning throughout the document.

A past participle can act as an adjective.

The sentence cap and simple-tense rule yield to fidelity. Report a necessary exception. Preserve the claim.

Resolve `scripts/ste-lint.py` from the directory that contains this `SKILL.md`. For a file or substantial text block, run:

```bash
python3 <skill-directory>/scripts/ste-lint.py FILE
```

Use `--max-words 20` for instructions and procedures. The default 25-word cap applies to descriptions.

The linter checks selected words and mechanically visible structures. It cannot prove meaning, completeness, noun clusters, paragraph topics, or exact ASD vocabulary.

Review every STE rule. Resolve every hard lint finding before the controlled-English pass ends.

## Unslop pass

These numbers are stable identifiers for other skills. Leave a retired number unused.

### Content

3. **Vacuous -ing tails.** Remove a final phrase when it only repeats the sentence. Use source facts when the phrase carries meaning.
5. **Vague attribution.** Name the source. Keep the attribution when its removal would strengthen the claim.

### Language

7. **AI vocabulary.** Replace `additionally`, `crucial`, `delve`, `enduring`, `enhance`, `fostering`, `garner`, `interplay`, `intricate`, `pivotal`, `showcase`, `testament`, `underscore`, and `vibrant`. Also replace abstract uses of `landscape` and `tapestry`.
8. **Copula inflation.** Replace `serves as`, `stands as`, `boasts`, and `features` with `is` or `has` when meaning stays intact.
9. **Inflated contrast.** Replace `not just X, but Y` with a direct statement.
10. **Forced groups of three.** Use the natural number of items.
11. **Synonym cycling.** Apply `STE-1`.
12. **False ranges.** Use `from X to Y` only when X and Y form a meaningful scale.

### Style

13. **Em dashes.** Replace each em dash with a period or comma. Avoid substitute asides made with other punctuation.
14. **Colon overuse.** Use a colon only before a list or example.
15. **Boldface overuse.** Use bold only when it helps the reader locate information.
16. **Inline-header lists.** Remove a bold label that restates its text. Keep a short label when new information follows.
17. **Title case headings.** Use sentence case.
18. **Decorative emojis.** Use text headings and ordinary bullets.
19. **Curly quotes.** Use straight quotes in prose. Preserve exact characters in code, commands, identifiers, paths, and quoted source text.

### Communication artifacts

20. **Chatbot phrases.** Remove phrases such as `Of course`, `Certainly`, `I hope this helps`, and `Let me know if`.
22. **Sycophancy.** Respond to the substance without praise such as `Great question` or `You are absolutely right`.

### Filler

23. **Filler phrases.** Replace `in order to` with `to`. Replace `due to the fact that` with `because`. Remove `it is important to note that`.
24. **Hedge stacks.** Remove only redundant hedge words. Preserve each qualifier that changes probability, frequency, scope, evidence, or requirement strength.
25. **Generic conclusions.** End with a specific fact, decision, consequence, or next step that the source supports.

### Jargon

26. **Abstract metaphors.** Replace metaphorical uses of `substrate, wedge, vector, locus, vantage, nexus, primitive, harness`. Also replace `surface, bedrock, scaffolding, modality, paradigm, gold-plating, ratchet, evacuate, endgame, north star, flywheel`. Keep literal domain terms.

### Plain speech

27. **Mechanism over feeling.** State what something does or give a source-backed measurement. Remove claims that say only how something feels. Remove a sentence that fits another project unchanged and gives no project fact.
28. **Dense sentences.** Apply `STE-9` through `STE-12`.
29. **Active voice.** Apply `STE-6`.
30. **Necessary modifiers.** Remove modifiers that add no meaning. Keep words such as `only`, `never`, `locally`, and `approximately` when they change meaning.
31. **Plain words.** Apply `STE-2`.
32. **Mannered prose.** Replace decorative metaphors, aphorisms, rhetorical fragments, personified code, and stock framing with literal statements.
33. **Complete prose.** Apply `STE-11`. Expand unexplained abbreviations, arrows, and compressed fragments when readers must decode them.
34. **Unsupported quality words.** Replace `seamless`, `robust`, `powerful`, `cutting-edge`, `effortless`, and `blazing-fast` with concrete, source-backed facts.

## Output

For an explicit rewrite, return only the revised text. Return input unchanged when it passes every rule that this skill can check.

Apply both passes silently in other tasks. Keep the output format that the user requested.

When the user asks for an explanation, provide a compact table with the rule, original text, and revision.

An unresolved source ambiguity has priority over clean output. Ask one focused question when the user can answer.

For a noninteractive result, add `Source ambiguity:` and state each plausible interpretation. Select no interpretation.

For an explicit rewrite, report a fidelity exception with `Kept as-is:`. State the precision that the text preserves.
