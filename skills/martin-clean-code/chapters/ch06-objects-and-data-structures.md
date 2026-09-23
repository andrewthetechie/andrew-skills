# Chapter 6: Objects and Data Structures

## Core idea

Objects hide data behind behavior. Data structures expose data and contain little behavior. Choose deliberately based on whether future change is more likely to add types or operations.

## Frameworks introduced

- **Data abstraction**: Expose the essence of data and its access policy, not a field-by-field representation.
  - When to use: When designing an object interface.
  - How: Offer operations such as `getPercentFuelRemaining()` instead of accessors that reveal gallons and tank capacity.
  - Failure mode: Getters and setters can expose implementation as completely as public fields.
- **Data/Object Anti-Symmetry**: Objects and data structures optimize opposite change directions.
  - When to use: When deciding between polymorphic objects and procedural operations over records.
  - How: Use objects when new types are likely. Use data structures when new operations are likely.
- **The Law of Demeter**: A method should talk to friends, not strangers.
  - When to use: When code navigates returned objects.
  - How: A method of class `C` should call methods on `C`, objects it creates, its arguments, or its fields. Do not continue through returned objects.
- **Tell, do not navigate**: Ask an object to perform the intent instead of retrieving its internals.
  - When to use: When a call chain obtains data only to perform an operation.
  - How: Replace path extraction and stream construction with an operation such as `context.createScratchFileStream(name)`.

## Key concepts

- **Object**: A unit that hides data and exposes meaningful operations.
- **Data structure**: A unit that exposes data and contains no significant behavior.
- **Train wreck**: A chain of calls that reveals several levels of internal navigation.
- **Hybrid**: A type that exposes data while also carrying business behavior, which makes both types and operations hard to extend.
- **Data Transfer Object (DTO)**: A simple data carrier used at storage, message, or process boundaries.
- **Active Record**: A data structure mapped to persistence with navigational operations such as `save` and `find`.
- **Access policy**: Rules enforced by an abstraction, such as updating coordinates together.

## Mental models

- Do not ask whether object orientation is always better. Ask which axis of change the design should make cheap.
- Treat a getter chain as a design question. Determine whether each returned value is an object or a data structure.
- Put business rules in objects. Keep DTOs and Active Records as data carriers when possible.
- Design interfaces around user intent, not stored fields.

## Anti-patterns

- **Automatic getters and setters**: They preserve field-level coupling behind method syntax.
- **Everything is an object**: Some problems need transparent data and many operations.
- **Train wrecks**: `context.getOptions().getScratchDir().getAbsolutePath()` exposes a remote object graph.
- **Hybrids**: Public data plus meaningful business methods creates the disadvantages of both styles.
- **Business logic in Active Records**: Persistence records become coupled, hard-to-change hybrids.

## Code example

```java
// Navigation exposes structure.
String path = context.getOptions().getScratchDir().getAbsolutePath();
OutputStream out = new FileOutputStream(path + "/" + classFileName);

// Behavior hides structure.
BufferedOutputStream out = context.createScratchFileStream(classFileName);
```

- **What it demonstrates**: The caller states the desired operation. The context owns directory and stream details.

## Trade-off matrix

| Expected change | Prefer | Cost |
|---|---|---|
| Add new concrete types | Objects and polymorphism | A new operation may require changes to every type |
| Add new operations over stable records | Data structures and procedures | A new record type may require changes to every operation |
| Cross a database or message boundary | DTO | Validation and behavior must live elsewhere |
| Encapsulate a third-party representation | Object or adapter | More interface design up front |

## Worked example

A compiler helper reads a scratch directory through three getters. It builds a file path and constructs streams. The function now knows three layers of structure and a specific file layout.

Refactor by intent:

1. Identify the actual goal: create a scratch output stream for one class file.
2. Add `createScratchFileStream(classFileName)` to the owning context abstraction.
3. Move path separators, extensions, directory selection, and buffering behind that operation.
4. Test the public behavior, not the internal path traversal.

The caller loses structural knowledge. The context can change its directory representation without changing the client.

## Key takeaways

1. Hide representation with abstractions, not mechanical accessors.
2. Choose objects or data structures according to the expected direction of change.
3. Apply the Law of Demeter to objects, not to transparent data structures.
4. Replace navigation with an operation that states the caller's intent.
5. Keep DTOs and Active Records separate from business-rule objects.

## Connects to

- **Ch 8**: Boundary wrappers isolate external representations.
- **Ch 10**: Small, cohesive classes expose focused behavior.
- **Ch 11**: Dependency injection separates object construction from use.
- **Ch 17**: Avoid Transitive Navigation restates the Law of Demeter.
