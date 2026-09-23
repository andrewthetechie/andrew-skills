# Chapter 15: JUnit internals

## Core idea

Even good, well-tested code deserves incremental cleanup. The chapter reviews JUnit's `ComparisonCompactor`, makes a sequence of small improvements, and keeps the tests passing throughout. The lesson is not that the original code is poor. It is that professional maintenance leaves code a little clearer than it was found.

## Frameworks introduced

### Boy Scout review

Approach mature code with respect and attention. Look for small opportunities to improve names, conditionals, state, and function order. A modest change can clarify the next reader's path without requiring a redesign.

### Test-protected micro-refactoring

Make one small change, run the tests, and inspect the result. High coverage supports fast feedback, but it does not replace judgment. A refactoring can preserve outputs while making the design worse, so evaluate clarity after every green step.

### Reveal temporal coupling

If one method silently depends on another method having initialized fields, make that dependency visible. Pass computed values explicitly, return a value object, or combine operations when their separation creates invalid intermediate states.

### Normalize boundary arithmetic

Repeated `+1` and `-1` adjustments are signs that the code has not named its boundary model. Store a length instead of an ending index, or encapsulate the calculation in a named helper.

## Key concepts

- Names should describe intent and side effects, not implementation history.
- Positive conditions are usually easier to read than double negatives.
- A condition deserves a named predicate when the reason for the branch is not obvious.
- Member variables should represent lasting object state, not scratch values shared between methods.
- Functions can be ordered from analysis to synthesis so the file tells a coherent story.
- It is acceptable to reverse a refactoring when the result is less clear.

## Mental models

### Refactoring as editing

Editing prose does not change the argument. It removes friction between the argument and the reader. Refactoring performs the same service for executable text. The tests protect the meaning while the engineer improves its expression.

### Hidden state as an implicit parameter

When a helper reads a field that another helper must calculate first, the field acts like an undocumented parameter. Treat it as such. Pass it explicitly or package the related values in a result that makes the dependency clear.

### Topological reading order

Arrange functions so readers encounter prerequisites before dependent synthesis, or high-level narrative before lower-level detail. Choose an order that reduces jumping and makes the transformation easy to follow.

## Anti-patterns

- **Prefix names:** member prefixes such as `fExpected` that encode scope instead of meaning.
- **Opaque predicates:** complex conditions left inline without an intention-revealing name.
- **Scattered boundary adjustments:** repeated arithmetic around indices and substring limits.
- **Scratch fields:** object fields used only to pass temporary results between methods.
- **Unquestioned refactoring:** keeping a change merely because it is structurally different.
- **Coverage complacency:** assuming fully covered code cannot benefit from design review.

## Code example

An explicit result removes hidden ordering between prefix and suffix analysis:

```java
record MatchRegion(int prefixLength, int suffixLength) {}

private MatchRegion findCommonRegion(String expected, String actual) {
    int prefixLength = findCommonPrefix(expected, actual);
    int suffixLength = findCommonSuffix(expected, actual, prefixLength);
    return new MatchRegion(prefixLength, suffixLength);
}

private String formatCompactedComparison(String expected, String actual) {
    MatchRegion region = findCommonRegion(expected, actual);
    return compact(expected, actual, region);
}
```

The caller can see that both measurements belong to one analysis. No helper relies on a field populated by a previous call.

## Review table

| Smell | Question | Typical improvement |
|---|---|---|
| Encoded field prefix | Would the name still work if storage changed? | Remove the prefix and use a descriptive noun |
| Negative compound condition | Can the successful case be stated directly? | Extract a positive predicate |
| Method called only after another | What data does the second method actually require? | Pass or return that data explicitly |
| Repeated index correction | Is the code mixing endpoints and lengths? | Choose one representation and name it |
| Vague verb such as `compact` | What result does the function produce? | Rename it to state the outcome |
| Awkward function order | What reading path explains the algorithm? | Order analysis before synthesis, or narrative before detail |

## Worked example: clarify comparison compaction

Begin with the passing test suite. Rename fields to remove scope encodings. Encapsulate the check that decides whether compaction is needed. Prefer a positive predicate. Rename the main function so it says that it formats a compacted comparison rather than merely performing an unspecified `compact` operation.

Next, inspect the prefix and suffix calculations. Replace shared temporary fields with explicit lengths. Pass the prefix length into suffix analysis so the overlap constraint is visible. Replace arbitrary `+1` corrections with length-based calculations or named helpers. Run the full suite after each step.

Finally, read the class from top to bottom. Arrange helpers so the string analysis leads naturally into construction of the final message. If an extraction makes the flow harder to understand, undo it. A green suite permits experimentation. It does not make every experiment good.

## Key takeaways

- Well-tested code is safe to improve, not exempt from improvement.
- Small cleanups compound into a clearer maintenance surface.
- Expose ordering and data dependencies in function signatures.
- Replace boundary arithmetic with named representations.
- Let names state the result and the side effects.
- Judge each refactoring by readability as well as test results.

## Connects to

- [Chapter 2: Meaningful names](ch02-meaningful-names.md) for intent-revealing identifiers.
- [Chapter 3: Functions](ch03-functions.md) for function size, order, and abstraction level.
- [Chapter 9: Unit tests](ch09-unit-tests.md) for the safety net used throughout the review.
- [Chapter 14: Successive refinement](ch14-successive-refinement.md) for incremental design migration.
- [Chapter 17: Smells and heuristics](ch17-smells-and-heuristics.md) for a broader review catalog.
