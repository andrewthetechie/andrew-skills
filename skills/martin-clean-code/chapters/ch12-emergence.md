# Chapter 12: Emergence

## Core idea

Good design can emerge through a strict priority: keep behavior verified, remove duplication, express intent, then minimize structure. Refactor after each small behavior change.

## Frameworks introduced

- **Beck's four rules of Simple Design**: In order, the system runs all tests, contains no duplication, expresses intent, and minimizes classes and methods.
  - When to use: During every implementation and refactoring cycle.
  - How: Preserve the order. Never reduce structure at the cost of tests, duplication, or expression.
- **Refactor after green**: Once tests pass, inspect the few lines just added and restore design quality.
  - When to use: After every small TDD step.
  - How: Improve cohesion, coupling, names, responsibilities, and abstractions. Run the tests after each change.
- **Reuse in the small**: Remove even small duplicated mechanics to reveal a concept that may deserve a name or class.
  - When to use: When two short operations repeat cleanup, conversion, or state changes.
- **Template Method**: Place a stable algorithm in a base method and let variants supply one differing step.
  - When to use: When several workflows share the same sequence but differ at one policy point.

## Key concepts

- **Emergent design**: Design improved through repeated feedback and refactoring, not fully predicted before coding.
- **Verification pressure**: The need to test behavior pushes classes toward low coupling and high cohesion.
- **Implementation duplication**: Different code paths that maintain the same rule or state.
- **Expression**: Names, structure, patterns, and tests that make design intent visible.
- **Entity count**: The number of classes and methods, minimized only after higher-priority rules hold.
- **Dogmatic structure**: Interfaces or class splits created by rule rather than a real responsibility or seam.

## Mental models

- Treat the four rules as ordered constraints, not equal preferences.
- Let tests create freedom to improve structure without fear.
- Look for the idea hidden inside duplication. Extraction often reveals a responsibility.
- Minimize concepts, not merely lines. A few clear classes can be simpler than one tangled class.

## Anti-patterns

- **Paper-perfect but unverifiable design**: An elegant diagram cannot substitute for passing behavior.
- **Duplicated state definitions**: `size` and `isEmpty` should not maintain independent truths.
- **Working-code abandonment**: Moving on immediately after green preserves avoidable design damage.
- **Pattern name without need**: Structure added for fashion raises entity count and navigation cost.
- **Premature minimization**: Combining classes to reduce count can reintroduce duplication and unclear intent.

## Code example

```java
int size() { return elements.size(); }

boolean isEmpty() {
    return size() == 0;
}
```

- **What it demonstrates**: One operation derives from the other, so the collection has one definition of emptiness.

## Priority table

| Priority | Rule | Decision test |
|---:|---|---|
| 1 | Runs all tests | Is behavior continuously verified? |
| 2 | No duplication | Does one rule or mechanism have one representation? |
| 3 | Expresses intent | Can the next reader infer the design quickly? |
| 4 | Minimal classes and methods | Can an entity disappear without harming the first three rules? |

## Worked example

Two image operations both create a replacement image, dispose the old one, request cleanup, and assign the replacement. Only the image transformation differs.

Refactor after tests pass:

1. Extract `replaceImage(newImage)` for the shared lifecycle.
2. Leave scaling and rotation responsible only for producing their transformed image.
3. Run the tests.
4. Ask whether the extracted operation belongs in the current class or reveals another responsibility.

The small duplication exposed an invariant: every replacement must dispose and update the image in one way.

## Key takeaways

1. Keep Beck's four rules in their stated order.
2. Use tests to make continual refactoring safe.
3. Remove duplication in logic, state, and workflow.
4. Express intent through names, small units, standard nomenclature, and tests.
5. Minimize classes and methods only after higher-priority design needs are met.

## Connects to

- **Ch 9**: Clean tests provide the verification and freedom this method requires.
- **Ch 10**: Refactoring applies SRP, OCP, DIP, cohesion, and coupling decisions.
- **Ch 14**: The Args case shows emergent design through successive refinement.
- **Ch 15**: The JUnit case demonstrates small, test-preserving improvements.

