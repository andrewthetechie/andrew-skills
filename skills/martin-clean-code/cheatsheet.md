# Clean code cheatsheet

## Before changing code

- State the behavior that must remain true.
- Find or add a fast test that protects it.
- Read callers before changing an interface.
- Identify the responsibility that makes the change difficult.

## Names

- Reveal intent without a comment.
- Use one word for one concept.
- Use domain terms for domain behavior and technical terms for technical mechanisms.
- Avoid encodings, jokes, noise words, and differences that do not mean anything.
- Include surprising side effects in a function name, or remove the side effect.

## Functions

- Keep one coherent purpose at one abstraction level.
- Prefer zero, one, or two arguments. Treat more as design pressure.
- Replace Boolean flags with separate named operations.
- Return values instead of output arguments.
- Separate commands from queries.
- Extract `try` and `catch` bodies when error structure hides the main path.

## Comments and formatting

- Use a comment for intent, risk, a public contract, or information code cannot express.
- Delete obsolete, redundant, journal, and commented-out code.
- Put related lines close together.
- Order a file as a readable narrative from high-level intent to detail.
- Follow the team's formatter and layout rules consistently.

## Objects, classes, and systems

- Hide representation behind behavior, not automatic getters and setters.
- Use objects when new types should be easy to add.
- Use data structures when new operations should be easy to add.
- Keep classes small by reasons to change.
- Inject dependencies and separate construction from use.
- Prevent framework details from spreading into business policy.

## Errors and boundaries

- Prefer exceptions to returned error codes when the language supports them well.
- Add operation and input context to failures.
- Wrap third-party APIs in interfaces shaped for your application.
- Write learning tests for unfamiliar libraries.
- Use a special-case object when it removes repeated exceptional branches.
- Do not return or pass null unless an external contract forces it.

## Tests

- Keep tests fast, independent, repeatable, self-validating, and timely.
- Structure tests as build, operate, check.
- Test one concept, with as many assertions as that concept needs.
- Cover boundaries and cases adjacent to every discovered defect.
- Use coverage to locate unknown paths, not to declare correctness.

## Review prompts

| If you see | Ask | Likely move |
|---|---|---|
| Repeated switch by type | Which type should own this behavior? | Polymorphism or a strategy |
| Flags and modes | Are these separate operations? | Named functions or objects |
| Getter chains | Why does the caller know this structure? | Tell the owning object what to do |
| Shared scratch fields | Which hidden input or order do they encode? | Explicit parameters or result object |
| Repeated boundary math | What boundary concept is missing? | Named helper or value type |
| Many synchronized methods | Which shared state is truly required? | Isolate data and shrink critical sections |
| A hard new feature | Is the design trend worsening? | Stop and refine before adding more |
