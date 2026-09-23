# Chapter 2: Meaningful Names

## Core idea

Names are the primary interface between code and its readers. A good name exposes intent, domain meaning, and distinctions without requiring comments or mental translation.

## Frameworks introduced

- **Use intention-revealing names**: A name should explain why an entity exists, what it does, and how callers use it.
  - When to use: For every variable, function, argument, class, package, and file.
  - How: Replace implementation-shaped labels with the concept, measurement, and unit. If a comment must explain a name, improve the name.
- **Avoid disinformation**: Do not use names that imply the wrong platform, type, behavior, or relationship.
  - When to use: During naming and review.
  - How: Remove false type hints such as `accountList` when the value is not a list. Avoid visually confusable names and subtly different long names.
- **Make meaningful distinctions**: Two names should differ because the concepts differ, not because the compiler requires unique tokens.
  - When to use: When names gain numbers, filler words, or arbitrary prefixes.
  - How: State the semantic difference. Replace `a1` and `a2` with `source` and `destination`. Remove noise such as `Info`, `Data`, or `Object` unless it changes meaning.
- **Pick one word per concept**: Use one stable term for one operation or role across an API.
  - When to use: When equivalent methods use `fetch`, `retrieve`, and `get`, or equivalent classes use `manager`, `controller`, and `driver`.
  - How: Maintain a project lexicon and apply it consistently.
- **Use solution and problem domain names**: Name technical mechanisms with standard technical terms. Name domain behavior with the vocabulary of domain experts.
  - When to use: When choosing between a generic label and a recognized concept.
  - How: Use names such as `AccountVisitor` for the Visitor pattern and domain terms for business behavior.
- **Add meaningful context**: Place values in a class, function, or namespace that supplies their shared meaning.
  - When to use: When a local name is clear only after reading an entire algorithm.
  - How: Prefer an `Address` object over repeated `addr` prefixes. Use a prefix only as a last resort.

## Key concepts

- **Searchable name**: A name that can be found reliably across the codebase.
- **Pronounceable name**: A name teammates can discuss without decoding characters.
- **Mental mapping**: The reader's translation from a weak label to the actual concept.
- **Encoding**: Type or scope information embedded in a name, such as Hungarian notation or member prefixes.
- **Conceptual consistency**: Stable vocabulary for equivalent operations and roles.
- **Semantic pun**: Reusing one word for different operations only to appear consistent.
- **Scope-length relationship**: Longer scopes need more descriptive and searchable names. A short loop counter can remain short.
- **Gratuitous context**: Redundant application or module prefixes that obscure the useful part of a name.

## Mental models

- Treat each name as a compressed explanation. If it omits intent, every reader must reconstruct that explanation.
- Let scope set name length. A two-line loop can use `i`. A widely used value needs a unique, searchable name.
- Use nouns or noun phrases for classes. Use verbs or verb phrases for methods.
- Prefer a shared lexicon over local cleverness. Code should support a quick skim, not an archaeological study.

## Anti-patterns

- **Noise words**: Names such as `ProductInfo`, `ProductData`, or `CustomerObject` create differences without meaning.
- **Number-series naming**: `a1`, `a2`, and similar labels hide roles.
- **Type encodings**: Prefixes and suffixes drift when types change and force readers to decode stale information.
- **Cute or cultural names**: Jokes and slang such as `whack()` make behavior unclear to future readers.
- **One word, several meanings**: Calling both arithmetic combination and collection insertion `add` hides different semantics.
- **Long shared prefixes**: Application initials on every class make completion lists noisy and reduce reuse.

## Code example

```java
// Implicit context
List<int[]> getThem();

// Intent and domain are explicit
List<Cell> getFlaggedCells() {
    List<Cell> flaggedCells = new ArrayList<>();
    for (Cell cell : gameBoard) {
        if (cell.isFlagged()) flaggedCells.add(cell);
    }
    return flaggedCells;
}
```

- **What it demonstrates**: Naming the board, cell type, result, and predicate removes the need to know array positions and magic values.

## Reference table

| Entity | Preferred form | Avoid |
|---|---|---|
| Class or object | Noun or noun phrase, such as `Customer` or `AddressParser` | Verbs and vague roles such as `Manager`, `Data`, or `Info` |
| Method | Verb or verb phrase, such as `postPayment` | Ambiguous nouns or slang |
| Predicate | `is...`, `has...`, or another clear question | A command-shaped name |
| Factory | A name that describes the result or argument | An overloaded constructor with unclear meaning |
| Constant | Searchable domain name with its unit | A repeated literal |
| Interface | Unadorned concept name | Encoding the interface only to expose implementation detail |

## Worked example

The mine-sweeper example starts with `theList`, `list1`, `x[0]`, and the value `4`. Nothing states the domain or the meaning of the index and value.

Refactor it in three steps:

1. Rename `theList` to `gameBoard`, `list1` to `flaggedCells`, and `x` to `cell`.
2. Replace `0` and `4` with `STATUS_VALUE` and `FLAGGED`.
3. Replace the integer array with a `Cell` object and move the test behind `cell.isFlagged()`.

The control flow does not become simpler. The concepts become explicit, so the reader no longer reconstructs hidden context.

## Key takeaways

1. Change a name whenever a better one becomes clear.
2. Encode intent, measurement, and unit in the name when they matter.
3. Use project-wide words consistently and avoid semantic puns.
4. Prefer searchable and pronounceable names over abbreviations.
5. Put related values in a named concept instead of relying on prefixes.
6. Use refactoring tools to rename safely and often.

## Connects to

- **Ch 3**: Small functions make descriptive names easier to choose.
- **Ch 6**: Data abstractions give related values a meaningful context.
- **Ch 10**: Class names should state one responsibility at the right abstraction level.
- **Ch 17**: The naming heuristics consolidate these rules into review checks.
