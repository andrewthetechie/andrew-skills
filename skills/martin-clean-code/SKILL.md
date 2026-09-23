---
name: martin-clean-code
description: Reference and application guide to Robert C. Martin's Clean Code.
disable-model-invocation: true
metadata:
  source_title: "Clean Code: A Handbook of Agile Software Craftsmanship"
  source_author: "Robert C. Martin and Object Mentor contributors"
  source_year: 2009
  source_pages: 462
  source_chapters: 17
  generated: 2026-09-21
---

# Martin clean code

Apply the book's guidance within current project constraints. When rules conflict, rank them:

1. Correctness and explicit requirements.
2. Security and data integrity.
3. Repository and language standards.
4. Tests and measured evidence.
5. Clarity for the next reader.
6. Book heuristics.

Use size and count as design signals. Base decisions on responsibility and change pressure.

## Operating loop

Follow this loop for implementation, refactoring, and review work.

1. Establish the baseline. Name the required behavior and its protecting test or validation. Record the current result.
2. Diagnose one concrete smell. Cite the code evidence and name the responsibility or concept involved.
3. Route the smell. Read each matching chapter or pattern before selecting a change.
4. Act within authority, on one path only:
   - Change task: make one scoped improvement. Preserve behavior outside the requested change.
   - Review task: record the finding as file and line, the evidence quoted from the code, the rule it breaks, and the recommended move. Account for every in-scope instance of the selected rule. Leave the code as you found it.
5. Validate the result. Run the complete relevant tests or validation commands. Record each pass, failure, or unavailable validation.
6. Compare before and after. State how the result changes readability, coupling, duplication, or change cost.

Repeat steps 2 through 6 while in-scope smells remain.

Complete the task after you cover every requested change or finding. Required validations must pass, or each remaining failure needs an explanation.

## Route by evidence

Read every file whose branch matches observed evidence, then stop.

| Evidence | Read |
|---|---|
| The task needs the book's quality or economic frame | [Clean code](chapters/ch01-clean-code.md) |
| Names hide intent, domain meaning, or side effects | [Meaningful names](chapters/ch02-meaningful-names.md) |
| Functions mix behaviors, arguments, or abstraction levels | [Functions](chapters/ch03-functions.md) |
| Comments compensate for unclear code | [Comments](chapters/ch04-comments.md) |
| File layout hides relationships or reading order | [Formatting](chapters/ch05-formatting.md) |
| Object navigation, data exposure, or class cohesion obstructs a change | [Objects and data structures](chapters/ch06-objects-and-data-structures.md) and [Classes](chapters/ch10-classes.md) |
| Error paths, exception context, or null handling obscures behavior | [Error handling](chapters/ch07-error-handling.md) |
| A third-party interface leaks into application code | [Boundaries](chapters/ch08-boundaries.md) |
| Tests or test-driven development constrain safe change | [Unit tests](chapters/ch09-unit-tests.md) |
| Construction or framework details dominate policy | [Systems](chapters/ch11-systems.md) |
| Passing code still contains duplication or unclear intent | [Emergence](chapters/ch12-emergence.md) |
| Shared state, scheduling, deadlock, or shutdown creates risk | [Concurrency](chapters/ch13-concurrency.md) |
| Each new feature makes the structure worse | [Successive refinement](chapters/ch14-successive-refinement.md) |
| Untested or unowned legacy code must change safely | [JUnit internals](chapters/ch15-junit-internals.md) and [Refactoring SerialDate](chapters/ch16-refactoring-serialdate.md) |
| A review needs a broad diagnostic catalog | [Smells and heuristics](chapters/ch17-smells-and-heuristics.md) |

## Conditional references

- Read the [topic index](chapters/index.md) when one concern spans several chapters.
- Read the [cheatsheet](cheatsheet.md) first when the task is a broad review rather than one diagnosed smell.
- Read the [patterns catalog](patterns.md) when selecting a concrete transformation after diagnosing a smell.
- Read the [glossary](glossary.md) when an unfamiliar book term affects the decision.
