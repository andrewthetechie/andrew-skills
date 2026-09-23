# Chapter 14: Successive refinement

## Core idea

Clean code usually emerges through repeated, test-protected refinement. The first version proves that the behavior is possible. Each later version improves the design while preserving that behavior. The chapter develops this idea through a command-line argument parser that grows from a small implementation into a design with distinct concepts and responsibilities.

## Frameworks introduced

### Make it work, then make it right

Separate two forms of progress:

1. Establish working behavior with tests.
2. Improve the structure without changing that behavior.

Do not treat the first working design as the finished design. Also, do not postpone cleanup until the code has accumulated many unrelated features.

### Watch the structural trend

A design can absorb early features easily and then reach a point where each new feature requires more special cases than the last. That worsening trend is the signal to stop feature work and restructure. Continuing to add behavior at that point compounds the problem.

### Let repetition reveal concepts

Parallel maps, repeated conditionals, and type-specific branches often indicate a missing abstraction. In the parser example, separate storage for Boolean, integer, and string arguments gives way to a common `ArgumentMarshaler` concept. The abstraction is discovered from repeated structure rather than invented before any evidence exists.

### Refactor through tiny transformations

Keep the system running while changing its design. Move one responsibility, run the tests, then continue. Small transformations make failures local and allow the design to change direction when a proposed abstraction does not help.

## Key concepts

- Tests are the safety net that makes structural experimentation economical.
- A working draft can contain duplication and awkward control flow, but it must not become the permanent architecture.
- New abstractions should remove a repeated burden from the caller.
- Error reporting is a responsibility of its own and can move into a dedicated exception type.
- A large cleanup is safer when partitioned into behavior-preserving steps.
- Run the complete test suite after each meaningful transformation, not only the tests closest to the edit.

## Mental models

### Refactoring as controlled migration

Think of refinement as moving traffic from an old bridge to a new one a lane at a time. Both structures may coexist briefly. Each move must leave a usable route. Delete the old path only after the new one carries all behavior.

### Design pressure

An awkward new feature is diagnostic information. If adding a third argument type multiplies maps and conditionals, the feature has exposed a weak model. Use that pressure to identify the concept that the current design does not represent.

### Tests as an invariant boundary

The implementation can change freely inside the boundary created by the tests. If the tests express the behavior well, every green step confirms that the external contract remains intact.

## Anti-patterns

- **One-pass cleanliness:** expecting a polished design to appear in the first draft.
- **Feature momentum:** continuing to add features after every change makes the structure worse.
- **Massive rewrite:** replacing all working code at once and losing the ability to locate regressions.
- **Parallel type machinery:** maintaining a map, switch branch, and getter for every supported type.
- **Partial-suite confidence:** running only the newest tests while a refactoring affects shared behavior.
- **Cleanup debt:** promising to improve the code later without defining a stopping point for feature work.

## Code example

The refined parser delegates type-specific behavior to marshalers:

```java
public class Args {
    private final Map<Character, ArgumentMarshaler> marshalers = new HashMap<>();

    public Args(String schema, String[] args) throws ArgsException {
        parseSchema(schema);
        parseArgumentStrings(List.of(args));
    }

    public boolean getBoolean(char id) {
        return BooleanArgumentMarshaler.getValue(marshalers.get(id));
    }

    public int getInt(char id) {
        return IntegerArgumentMarshaler.getValue(marshalers.get(id));
    }
}
```

The client sees one parser and typed accessors. Each marshaler owns the rules for one data type. Adding a type no longer requires coordinated edits across several parallel data structures.

## Decision table

| Observation | Interpretation | Next move |
|---|---|---|
| New feature fits the existing design cleanly | The current abstractions still carry their weight | Add the feature and keep tests green |
| New feature repeats an existing shape | A shared concept may be emerging | Name the common responsibility and extract it |
| New feature adds branches in several places | Type knowledge is scattered | Move type behavior behind polymorphism |
| Refactoring breaks many unrelated tests | The step is too large or coupling is hidden | Revert or split the transformation |
| Error text dominates parsing logic | Reporting and parsing are mixed | Move formatting into an error abstraction |
| A helper is used only during a temporary migration | The transition is incomplete | Finish the migration and remove the bridge |

## Worked example: evolve a command-line parser

Start with a schema such as `l,p#,d*`, where each marker identifies a Boolean, integer, or string option. A rough implementation may use separate maps and switches for each type. It works for the first few cases, but every new type requires another map, another parsing branch, another accessor, and more error logic.

Freeze the observable behavior with tests for valid values, missing values, invalid formats, unknown arguments, and defaults. Then introduce an `ArgumentMarshaler` interface. Move Boolean parsing behind one implementation and run all tests. Repeat for integers and strings. Replace the parallel maps with one map from argument identifier to marshaler. Move error codes and messages into `ArgsException`. Delete obsolete branches after the new path handles every tested case.

The result is not merely shorter. The code now models the problem directly: an argument has a marshaler, and each marshaler knows how to consume and expose its value.

## Key takeaways

- A first draft is raw material, not a failure.
- Stop adding features when the design trend turns negative.
- Use tests to preserve behavior during every structural move.
- Extract abstractions from observed repetition.
- Prefer a sequence of reversible steps to a single heroic rewrite.
- Finish the migration by deleting temporary and obsolete machinery.

## Connects to

- [Chapter 2: Meaningful names](ch02-meaningful-names.md) for naming discovered concepts.
- [Chapter 3: Functions](ch03-functions.md) for decomposing mixed parsing logic.
- [Chapter 9: Unit tests](ch09-unit-tests.md) for the safety net that enables refinement.
- [Chapter 12: Emergence](ch12-emergence.md) for the test-and-refactor cycle.
- [Chapter 17: Smells and heuristics](ch17-smells-and-heuristics.md) for signals that a draft needs another pass.
