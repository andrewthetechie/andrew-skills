# Chapter 3: Functions

## Core idea

Functions should be small, do one thing at one abstraction level, and form a top-down narrative. Their names and structure should expose the system's domain language.

## Frameworks introduced

- **Small functions**: Make functions very small. Blocks inside control structures should usually contain one descriptive function call.
  - When to use: When a function needs sections, deep indentation, or repeated explanation.
  - How: Extract named operations until each function is easy to scan. Keep indentation to one or two levels.
- **Do One Thing**: A function does one thing when all its statements are one level below the concept named by the function.
  - When to use: When deciding whether further extraction improves the design.
  - How: Describe the function as a short "TO" paragraph. Extract any step at a different abstraction level.
  - Failure mode: Extracting a function that only restates one line does not create a useful abstraction.
- **The Stepdown Rule**: Order functions so the reader descends one abstraction level at a time.
  - When to use: When a module feels like disconnected utilities.
  - How: Put the public narrative first. Place each supporting function near and below the function that introduces it.
- **Command Query Separation**: A function should change state or answer a question, not both.
  - When to use: When a call can be read as either a predicate or an action.
  - How: Split `setAndReport` behavior into a query and a command.
- **Hide switch statements behind polymorphism**: Tolerate a type switch once when it creates the correct polymorphic object.
  - When to use: When several operations branch on the same type code.
  - How: Put the switch in an Abstract Factory and dispatch behavior through an interface.
- **Refine under tests**: Write a working draft, then split, rename, reorder, and remove duplication while tests stay green.
  - When to use: During normal implementation. Clean functions rarely appear in the first draft.

## Key concepts

- **One level of abstraction**: Every statement in a function belongs at the same conceptual distance from the function name.
- **Niladic, monadic, dyadic, triadic**: Functions with zero, one, two, or three arguments.
- **Argument object**: A named object that replaces a cluster of related parameters.
- **Flag argument**: A Boolean that announces the function does more than one thing.
- **Output argument**: An argument whose state the function changes, forcing the reader to inspect the signature.
- **Temporal coupling**: A hidden requirement that operations occur in a specific order.
- **Dependency magnet**: A shared error-code type that forces many modules to change together.
- **Domain-specific language**: The vocabulary formed by classes and functions to tell the system's story.

## Mental models

- Read a function name as a promise. Hidden side effects break that promise.
- Treat arguments as cognitive load. Prefer zero, then one, then two. Require strong justification for three or more.
- Treat functions as verbs and classes as nouns in the system's language.
- View a long function as a draft. Use tests to refine it into a readable hierarchy.

## Anti-patterns

- **Mixed abstraction levels**: High-level policy and low-level string manipulation in one function obscure what matters.
- **Flag arguments**: A Boolean selects separate behaviors and reveals more than one responsibility.
- **Hidden side effects**: A method named `checkPassword` must not also initialize a session.
- **Output arguments**: `appendFooter(report)` forces the reader to discover which value changes. Prefer `report.appendFooter()`.
- **Repeated type switches**: Parallel switches violate the Single Responsibility Principle and the Open Closed Principle.
- **Error-code pyramids**: Immediate nested checks mix the happy path with error processing.
- **Function sections**: Headers such as declarations, initialization, and processing show that one function contains several jobs.

## Code example

```java
public String renderPageWithSetupsAndTeardowns(PageData page, boolean suite)
        throws Exception {
    if (isTestPage(page)) includeSetupAndTeardownPages(page, suite);
    return page.getHtml();
}
```

- **What it demonstrates**: The function contains a short narrative at one level of abstraction. Supporting details can follow under the Stepdown Rule.

## Reference table

| Decision | Default | Exception |
|---|---|---|
| Function size | Smaller than about 20 lines, often 2 to 4 | Generated or declarative structures may need another form |
| Indentation | One or two levels | Extract the nested block when it grows |
| Argument count | Zero or one | Use two when order and meaning remain obvious |
| Three or more arguments | Create an argument object or redesign ownership | A familiar, stable mathematical operation may justify three |
| Error handling | Exceptions, with `try/catch` extracted | Use a result type when the domain treats failure as normal data |
| Type branching | One hidden factory switch | Do not repeat the switch across operations |

## Worked example

The original FitNesse page-rendering method fetched pages, resolved paths, appended directives, handled suite variants, and returned HTML. It mixed policy with string operations and repeated the setup algorithm.

Refine it with this sequence:

1. Protect current behavior with tests.
2. Rename the entry point to state its purpose.
3. Extract setup, content, teardown, and update steps.
4. Move shared state into a focused `SetupTeardownIncluder` object.
5. Remove the duplicated include algorithm.
6. Order methods from the high-level render story down to path and string details.
7. Run tests after every extraction.

The result is not merely shorter. Its function hierarchy states the algorithm and defers details until the reader asks for them.

## Key takeaways

1. Keep functions small and focused at one abstraction level.
2. Use the Stepdown Rule to make the module read from policy to detail.
3. Prefer no arguments. Replace related argument clusters with named objects.
4. Separate commands from queries and normal flow from error handling.
5. Expose temporal coupling in the API or remove it.
6. Remove duplication while tests preserve behavior.

## Connects to

- **Ch 2**: Descriptive function names carry the narrative.
- **Ch 7**: Exception structure keeps the normal path readable.
- **Ch 10**: Extracting cohesive state from argument-heavy functions often creates small classes.
- **Ch 14**: The Args example demonstrates repeated function refinement under tests.

