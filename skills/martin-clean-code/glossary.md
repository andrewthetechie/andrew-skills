# Glossary

**Abstraction level:** The conceptual height of a statement, from business policy down to implementation detail.

**Active Record:** A data structure with persistence operations, often treated as data rather than a behavior-rich domain object.

**Adapter:** A boundary object that translates an external interface into the interface the application wants.

**Argument marshaler:** An object that parses and stores one command-line argument type in the chapter 14 case study.

**Boundary:** The point where application code meets a library, framework, service, subsystem, or uncertain contract.

**Boundary condition:** A rule at a minimum, maximum, transition, empty case, or index edge.

**Boy Scout Rule:** Leave code cleaner than you found it.

**Build-operate-check:** A three-part test structure: prepare the case, perform the behavior, and verify the result.

**Characterization test:** A test that records existing behavior before legacy code is changed.

**Code sense:** Learned judgment that helps an engineer notice design friction and choose an effective improvement.

**Cohesion:** The degree to which a class's fields and methods support one focused responsibility.

**Command-query separation:** The principle that a function should change state or answer a question, but usually not both.

**Composition root:** The place where concrete dependencies are constructed and connected before use.

**Critical section:** Code that accesses shared state and must be protected from unsafe concurrent execution.

**Cross-cutting concern:** A policy such as logging, persistence, transactions, or security that affects many parts of a system.

**Data transfer object:** A transparent carrier of data with little or no behavior.

**Dependency injection:** Supplying collaborators from outside an object instead of constructing them inside it.

**Dependency inversion:** Making high-level policy depend on abstractions rather than concrete low-level details.

**Double-checked locking:** A concurrency pattern whose safety depends on language memory semantics and careful implementation.

**DRY:** 'Don't repeat yourself.' Represent each piece of system knowledge in one authoritative place.

**Emergent design:** Design that improves through tests, removal of duplication, clearer expression, and minimal structure.

**Encapsulation:** Hiding representation and protecting decisions behind a purposeful interface.

**Feature envy:** Behavior located away from the data or abstraction it mainly interprets.

**F.I.R.S.T.:** Fast, independent, repeatable, self-validating, and timely qualities for unit tests.

**Flag argument:** A Boolean or mode value that makes a function select between different behaviors.

**Law of Demeter:** A guideline that an object should collaborate with close neighbors rather than traverse distant internals.

**Learning test:** A focused test used to understand and preserve relied-upon behavior of a third-party API.

**Logical dependency:** A required relationship that may exist only by convention until code makes it explicit.

**Mental mapping:** Work a reader performs to translate an unclear name or representation into the actual concept.

**News-paper metaphor:** Organizing a source file from a high-level headline and synopsis toward increasing detail.

**Output argument:** An argument that a function mutates to communicate a result.

**Polymorphism:** Selecting behavior through an object's type and interface instead of central conditional logic.

**Primitive obsession:** Representing domain concepts with raw strings, integers, or flags instead of purposeful types.

**Responsibility:** A coherent reason that a module or class must change.

**Separation of Main:** Keeping object construction in `main` or another composition boundary and runtime use elsewhere.

**Smell:** A recurring signal that invites design investigation, not an automatic defect verdict.

**Special Case pattern:** An object that implements normal protocol for an exceptional or missing case.

**Stepdown Rule:** Arrange functions so each leads into operations one abstraction level lower.

**Successive refinement:** Improving a working design through small, test-protected transformations.

**Temporal coupling:** A requirement that operations occur in a particular order.

**Test double standard:** Tests may trade some production constraints for clarity while remaining readable and maintainable.

**Test-driven development:** A cycle in which a failing test precedes the minimum code to pass, followed by cleanup.

**Train wreck:** A long chain of navigation through object internals, often exposing structure to the caller.

**Vertical density:** Keeping strongly related lines close and separating distinct concepts with whitespace.

**Vertical ordering:** Placing a concept before the details that support it so code reads from high level to low level.
