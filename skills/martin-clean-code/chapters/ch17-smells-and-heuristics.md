# Chapter 17: Smells and heuristics

## Core idea

Code review improves through a vocabulary of recurring signals. A smell is not an automatic verdict. It is a prompt to investigate whether the code hides intent, duplicates knowledge, weakens tests, or places responsibility in the wrong abstraction. The chapter collects heuristics from the earlier chapters into a practical review catalog.

## Frameworks introduced

### Evidence-driven review

Start with observable friction. A change may require widespread edits, a name may mislead, or a function may mix abstraction levels. Select the smallest relevant heuristic. Inspect the surrounding design and verify the improvement with tests.

### Smell clusters

One smell often exposes another. A selector argument may indicate that a function does more than one thing. That function may also have a vague name and insufficient tests. Review the cluster rather than fixing only the visible syntax.

### Precision before cleverness

Most heuristics favor explicit intent, standard conventions, named conditions, and visible data flow. Clever compression saves lines but often transfers work to every reader.

### Local rules yield to project context

Some advice is tied to Java and to the source era. For example, the chapter recommends wildcard imports to reduce long import lists. Treat such rules as prompts, not universal mandates. Current language guidance and the repository's documented standards take precedence.

## Comment heuristics

| Code | Smell | Review action |
|---|---|---|
| C1 | Inappropriate information | Move metadata, history, and administrative notes to the proper system |
| C2 | Obsolete comment | Delete or update statements that no longer describe the code |
| C3 | Redundant comment | Let clear code state what it already says |
| C4 | Poorly written comment | Make necessary comments concise, precise, and grammatical |
| C5 | Commented-out code | Delete it and rely on version control |

## Environment and function heuristics

| Code | Smell | Review action |
|---|---|---|
| E1 | Build requires multiple steps | Provide one command that performs the build |
| E2 | Tests require multiple steps | Provide one command that runs the suite |
| F1 | Too many arguments | Introduce an object, split responsibility, or remove unnecessary data |
| F2 | Output arguments | Return a value or change the receiver explicitly |
| F3 | Flag arguments | Split the alternate behaviors into named functions |
| F4 | Dead function | Remove unused behavior |

## General heuristics

| Code | Smell | Review action |
|---|---|---|
| G1 | Multiple languages in one file | Minimize embedded syntax and isolate it when practical |
| G2 | Obvious behavior is unimplemented | Honor the expectation implied by the name and context |
| G3 | Boundary behavior is incorrect | Test minimums, maximums, transitions, empty values, and off-by-one cases |
| G4 | Overridden safety | Keep compiler warnings, tests, and other safeguards active |
| G5 | Duplication | Find the knowledge or responsibility repeated by each copy |
| G6 | Code at the wrong abstraction | Move policy upward and details downward |
| G7 | Base class depends on derivatives | Reverse the dependency through a factory or interface |
| G8 | Too much information | Reduce public surface area and hide internals |
| G9 | Dead code | Delete unreachable, unused, or permanently disabled paths |
| G10 | Vertical separation | Place related definitions near their use |
| G11 | Inconsistency | Apply the same choice in the same situation |
| G12 | Clutter | Remove empty constructors, unused variables, and meaningless comments |
| G13 | Artificial coupling | Do not force unrelated concepts together for convenience |
| G14 | Feature envy | Move behavior toward the data it interprets |
| G15 | Selector arguments | Replace mode switches with separate operations or polymorphism |
| G16 | Obscured intent | Use names, temporaries, and structure to make the algorithm visible |
| G17 | Misplaced responsibility | Put a decision where readers naturally look for it |
| G18 | Inappropriate static | Prefer instance behavior when polymorphism or object state matters |
| G19 | Explanatory variables | Name intermediate results in a complex calculation |
| G20 | Function name hides behavior | Name the complete contract, including important side effects |
| G21 | Algorithm is not understood | Refactor until the code follows a deliberate, explainable model |
| G22 | Logical dependency is not physical | Express required order through data flow or structure |
| G23 | Switch selects type behavior | Prefer polymorphism when branches vary by type |
| G24 | Nonstandard convention | Follow established language and project practices |
| G25 | Unnamed constant | Name domain-significant literals. Retain obvious syntax values |
| G26 | Imprecision | Choose exact names, types, and conditions |
| G27 | Convention carries essential structure | Enforce critical relationships in code or types |
| G28 | Complex conditional | Extract a predicate that states the decision |
| G29 | Negative conditional | State the positive case when it is clearer |
| G30 | Function does more than one thing | Separate operations at one abstraction level |
| G31 | Hidden temporal coupling | Expose required order in arguments, return values, or a combined operation |
| G32 | Arbitrary structure | Make placement and shape communicate a reason |
| G33 | Scattered boundary logic | Encapsulate boundary conditions in one named place |
| G34 | Mixed abstraction levels | Make each function descend one level at a time |
| G35 | Buried configuration | Keep configurable data high and easy to find |
| G36 | Transitive navigation | Ask collaborators to do work instead of traversing their internals |

## Java and naming heuristics

| Code | Smell | Review action |
|---|---|---|
| J1 | Long explicit import list | Apply current project import rules. The book favors wildcards in this case |
| J2 | Inherited constants | Use imports, enums, or composition instead of inheriting a constant container |
| J3 | Raw constants model a domain | Use enums with names and behavior |
| N1 | Nondescriptive name | Reveal intent and distinguish the concept |
| N2 | Name at the wrong abstraction | Match vocabulary to the level of the code |
| N3 | Nonstandard nomenclature | Use established names for established patterns |
| N4 | Ambiguous name | Make the interpretation univocal in context |
| N5 | Short name over a long scope | Increase descriptive detail with scope size |
| N6 | Encoded name | Remove type, scope, and interface encodings |
| N7 | Hidden side effect | Include significant side effects in the function name or redesign the function |

## Test heuristics

| Code | Smell | Review action |
|---|---|---|
| T1 | Insufficient tests | Exercise every important behavior and decision |
| T2 | Coverage evidence ignored | Use coverage tools to locate untested paths |
| T3 | Trivial test omitted | Add cheap tests when they document or protect behavior |
| T4 | Ignored test ambiguity | Treat unclear requirements exposed by tests as design questions |
| T5 | Boundary untested | Test around transitions and extremes |
| T6 | Bug neighborhood untested | Probe nearby and structurally similar cases |
| T7 | Failure pattern ignored | Use clustered failures to infer the deeper defect |
| T8 | Coverage pattern ignored | Investigate shapes in uncovered code, not only the aggregate percentage |
| T9 | Slow test | Keep the fast path suitable for frequent execution |

## Review sequence

1. Confirm the build and test suite have simple entry points.
2. Read the public names and interfaces before the implementation.
3. Trace one behavior from caller to result.
4. Mark duplication, mixed levels, scattered boundaries, and hidden order.
5. Inspect tests for boundaries, failure patterns, speed, and independence.
6. Choose one small improvement that removes a cause, not only a symptom.
7. Run the full relevant suite and reassess the surrounding smell cluster.

## Worked example: review a mode-driven formatter

Suppose `format(data, true, false, 3)` contains a long conditional, duplicates truncation math, and updates a cache. Start with F3: the Boolean flags suggest separate named operations. G30 confirms that formatting, truncation, and caching are distinct responsibilities. G33 points to repeated boundary calculations. N7 reveals that `format` does not advertise the cache mutation.

Add boundary tests for empty data and lengths around three. Extract a named truncation policy. Replace the flags with `formatSummary` and `formatDetailed`, or introduce a strategy if callers need extensibility. Move caching behind a clearly named collaborator. The review uses several heuristics, but the solution follows the underlying responsibilities rather than applying a mechanical rule to each line.

## Key takeaways

- A smell starts an investigation. Context determines the remedy.
- Review clusters of symptoms to find the shared design cause.
- Prefer precise names, visible dependencies, and one abstraction level at a time.
- Test boundaries and patterns around failures, not only the reported case.
- Remove dead material and reduce public information.
- Let current project standards override source-era, language-specific preferences.

## Connects to

- [Chapter 2: Meaningful names](ch02-meaningful-names.md) for the naming catalog.
- [Chapter 3: Functions](ch03-functions.md) for argument, flag, and abstraction smells.
- [Chapter 4: Comments](ch04-comments.md) for comment-specific guidance.
- [Chapter 9: Unit tests](ch09-unit-tests.md) for clean and complete tests.
- [Chapter 14: Successive refinement](ch14-successive-refinement.md) and [Chapter 16: Refactoring SerialDate](ch16-refactoring-serialdate.md) for worked refactoring sequences.
