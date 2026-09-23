# Patterns from Clean Code

## Boy Scout cleanup

**Use when:** touching an existing file for any reason.

**Method:** make one nearby improvement that is protected by tests. Rename a misleading identifier, remove dead code, clarify a condition, or reduce duplication. Keep the scope proportional to the change.

**Avoid:** unrelated redesign that makes the requested change hard to review.

## Stepdown narrative

**Use when:** a function mixes policy with detail.

**Method:** write the function as a sequence of operations one abstraction level below its name. Put supporting functions beneath it so a reader can descend through the file.

**Check:** each function can be described without using 'and then' to join separate responsibilities.

## Command-query split

**Use when:** a call both changes state and returns information that controls the caller.

**Method:** separate the state-changing command from the side-effect-free query, or give the combined operation a contract that makes both effects unmistakable.

## Exception boundary

**Use when:** repeated error checks obscure the successful path.

**Method:** convert low-level failures at one boundary, add operation context, and expose exceptions meaningful to the caller. Keep `try` blocks narrow and extract their bodies when useful.

## Special case

**Use when:** callers repeat the same missing-value or exceptional branch.

**Method:** provide an object that implements the normal protocol with the special behavior. Callers then execute one flow.

**Avoid:** using a special case when absence is itself important information that the caller must handle.

## Boundary wrapper

**Use when:** a third-party API is broad, unstable, or shaped differently from the application.

**Method:** expose only the operations the application needs. Translate types, errors, and lifecycle behind the wrapper. Test the wrapper against the real library when practical.

## Learning test

**Use when:** adopting or upgrading an unfamiliar dependency.

**Method:** write focused tests that demonstrate the behavior your code relies on. Keep them as executable compatibility checks.

## Build-operate-check test

**Use when:** a test is hard to scan.

**Method:** build the fixture, perform one conceptual operation, and check its result. Extract a small testing DSL when setup or assertions repeat domain ideas.

## Characterization before refactoring

**Use when:** legacy behavior is important but poorly documented.

**Method:** exercise representative paths, boundaries, and known failures. Use coverage to find unexplored branches. Refactor only after the observed contract has protection.

## Responsibility split

**Use when:** a class changes for unrelated reasons or has groups of low-cohesion fields and methods.

**Method:** identify each actor or policy that causes change. Move one coherent group behind a narrow interface and inject its dependencies.

## Construction-use separation

**Use when:** object creation, configuration, and runtime policy are interleaved.

**Method:** assemble the object graph in a composition root, factory, or `main`. Pass ready-to-use abstractions into application code.

## Emerging abstraction

**Use when:** a new feature creates parallel maps, branches, or nearly identical functions.

**Method:** first confirm the repeated responsibility. Name it, implement one variant behind the new interface, and migrate the remaining variants through small green steps.

## Physical dependency

**Use when:** correctness depends on an undocumented calculation or call order.

**Method:** pass the prerequisite value, return a structured result, combine the operations, or encode the valid sequence in a type.

## Boundary encapsulation

**Use when:** `+1`, `-1`, minimums, maximums, or transition rules recur.

**Method:** choose one representation, such as length instead of final index, and centralize the rule in a named function or value object. Test both sides of each transition.

## Concurrency isolation

**Use when:** independent work can overlap but introduces shared-state risk.

**Method:** separate concurrency policy from domain behavior. Minimize shared data, copy values when affordable, keep critical sections small, and model shutdown early.

**Check:** vary scheduling, processor count, load, and execution order. Diagnose rare failures instead of ignoring them.

## Smell-cluster review

**Use when:** a local problem appears to have several labels.

**Method:** list the related smells, then search for the shared cause. A flag argument, vague name, large function, and duplicated conditional may all point to one missing responsibility.

**Avoid:** mechanical rewrites that satisfy a rule without improving the model.
