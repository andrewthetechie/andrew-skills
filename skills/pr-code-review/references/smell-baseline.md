# Standards smell baseline

Apply these Fowler code smells (_Refactoring_, ch. 3) as labelled heuristics. A documented repository standard overrides this baseline. Skip checks enforced by tooling.

- **Mysterious Name** — a function, variable, or type whose name does not reveal what it does or holds. Rename it; if no honest name emerges, the design is unclear.
- **Duplicated Code** — the same logic shape appears in more than one changed hunk or file. Extract the shared shape.
- **Feature Envy** — a method reaches into another object's data more than its own. Move the method onto the data it envies.
- **Data Clumps** — the same fields or parameters repeatedly travel together. Bundle them into one type.
- **Primitive Obsession** — a primitive or string represents a domain concept that deserves its own type. Introduce that type.
- **Repeated Switches** — the same switch or conditional cascade on one type recurs. Replace it with polymorphism or one shared map.
- **Shotgun Surgery** — one logical change requires scattered edits across many files. Gather the changing behavior into one module.
- **Divergent Change** — one file or module changes for several unrelated reasons. Split the responsibilities.
- **Speculative Generality** — an abstraction, parameter, or hook serves no requirement in the spec. Remove or inline it until a real need exists.
- **Message Chains** — navigation such as `a.b().c().d()` exposes structure the caller should not know. Hide it behind one method on the first object.
- **Middle Man** — a class or function mostly delegates onward. Call the real target directly.
- **Refused Bequest** — a subclass or implementer ignores or overrides most inherited behavior. Prefer composition.
