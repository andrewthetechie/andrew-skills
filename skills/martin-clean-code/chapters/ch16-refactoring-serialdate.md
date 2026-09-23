# Chapter 16: Refactoring SerialDate

## Core idea

Professional refactoring begins by understanding and protecting behavior, then moves responsibilities to the abstractions that own them. The chapter reviews the open-source `SerialDate` class, expands its tests, corrects defects, and reshapes it into a smaller date abstraction with clearer types and dependencies.

## Frameworks introduced

### Make it work before making it right

Do not restructure unfamiliar code on intuition alone. Establish the current behavior, increase test coverage, and repair clear defects first. Once the tests provide confidence, improve names, ownership, and dependency direction.

### Coverage-guided characterization

Coverage reports show which paths have not been observed. They do not prove correctness, but they identify places where behavior remains unknown. Add tests around unexecuted branches, boundary dates, invalid values, and patterns near known failures.

### Put behavior with the right abstraction

Feature envy is a placement problem. If a function mainly interprets a month, weekday, or interval value, move the behavior to that type. Rich enums can replace integer constants and central switches with named, type-safe behavior.

### Make logical dependencies physical

If one value can be calculated only after another has been calculated, express that relationship in data flow or function structure. Do not rely on comments, call order conventions, or shared mutable state.

### Reverse the dependency

An abstract type should not know which concrete subtype implements it. Move construction behind a factory so clients depend on the abstraction and implementation details point inward from the concrete class.

## Key concepts

- Test independently of the implementation when possible.
- Test the boundaries around defects because nearby cases often share the same weakness.
- Delete change histories, dead code, redundant comments, and other source-control substitutes.
- Prefer domain types such as `Month` and `DayOfWeek` to integer codes.
- Use names such as `plusDays` when an operation returns a new value instead of mutating the receiver.
- Move implementation-specific fields and algorithms into the concrete implementation.
- A lower coverage percentage can accompany a better result when the class becomes much smaller and the uncovered code is well understood.

## Mental models

### Archaeology before architecture

Legacy refactoring starts as investigation. Tests, coverage, call sites, and boundary probes reveal what the code actually does. Only then can a new structure preserve the valuable behavior without preserving accidental complexity.

### Domain gravity

Behavior should move toward the concept whose data it interprets. Month validation belongs near `Month`. Interval logic belongs near `DateInterval`. This pull reduces navigation and eliminates switches distributed across unrelated classes.

### Shrinking the trusted core

The goal is not maximum line coverage at any cost. The goal is a small, comprehensible core whose important behavior is well tested. Deleting redundant code can reduce the denominator and expose the remaining risk more honestly.

## Anti-patterns

- **Refactoring blind:** changing structure before tests characterize the behavior.
- **Integer domain:** representing months, weekdays, or intervals with untyped constants.
- **Abstract-to-concrete dependency:** a base class directly constructing or naming its subtype.
- **Feature envy:** utility methods that spend most of their time examining another type's data.
- **Source-control comments:** keeping obsolete implementations or change logs inside the file.
- **Mutating names for immutable operations:** using `addDays` when the method returns a different date.
- **Coverage worship:** treating one aggregate percentage as proof of quality.

## Code example

Use domain types and a factory to keep the abstraction independent:

```java
public abstract class DayDate {
    public abstract DayDate plusDays(int days);

    public static DayDate create(int day, Month month, int year) {
        return DayDateFactory.instance().makeDate(day, month, year);
    }
}

public enum Month {
    JANUARY(31), FEBRUARY(28), MARCH(31);

    private final int normalYearDays;

    public int daysIn(boolean leapYear) {
        return this == FEBRUARY && leapYear ? 29 : normalYearDays;
    }
}
```

The example is illustrative. The design point is that callers use named domain values, while creation and calendar behavior live behind the relevant abstractions.

## Refactoring sequence

| Stage | Evidence or smell | Action |
|---|---|---|
| Characterize | Coverage begins near 50 percent | Add independent tests for observed and boundary behavior |
| Repair | Tests reveal incorrect edge cases | Fix behavior before broad restructuring |
| Clarify | Names and comments obscure intent | Rename concepts and remove obsolete material |
| Type | Integer constants drive switches | Introduce enums and move behavior into them |
| Reassign | Base class knows implementation details | Move fields down and introduce an abstract factory |
| Simplify | Static utilities inspect foreign data | Make behavior an instance method on the owning type |
| Reassess | Final coverage is 45 of 53 statements, about 84.9 percent | Judge the small remaining surface directly |

## Worked example: repair a date boundary

Suppose `plusDays(1)` fails on the last day of February in a leap year. First add tests for February 28 and 29 in leap and non-leap years, then test transitions into March. Check adjacent negative and multi-day offsets because failure patterns often extend beyond the reported example.

Once behavior is correct, replace numeric month constants with a `Month` enum. Move the leap-year day count into `Month.daysIn`. Rename the nonmutating operation from `addDays` to `plusDays`. If the abstract date class constructs a spreadsheet-specific implementation, route creation through a factory and keep implementation fields in that subtype.

Run the complete suite after every move. Coverage may rise from about 50 percent to about 92 percent during characterization, then settle lower after the class shrinks. Inspect the remaining uncovered statements instead of chasing the earlier percentage mechanically.

## Key takeaways

- Characterize legacy behavior before redesigning it.
- Use coverage to find unknowns, then apply domain judgment.
- Probe boundaries and patterns around every discovered defect.
- Replace primitive codes with types that can own behavior.
- Point dependencies from concrete implementations toward abstractions.
- Measure the clarity and risk of the remaining code, not only a percentage.

## Connects to

- [Chapter 6: Objects and data structures](ch06-objects-and-data-structures.md) for assigning behavior to objects.
- [Chapter 9: Unit tests](ch09-unit-tests.md) for fast and independent characterization tests.
- [Chapter 10: Classes](ch10-classes.md) for dependency direction and responsibility.
- [Chapter 14: Successive refinement](ch14-successive-refinement.md) for stepwise migration.
- [Chapter 17: Smells and heuristics](ch17-smells-and-heuristics.md) for feature envy, boundaries, and logical dependencies.
