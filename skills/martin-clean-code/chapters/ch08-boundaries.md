# Chapter 8: Boundaries

## Core idea

Keep external interfaces at a narrow, tested edge. Application code should depend on an interface it controls, not on broad vendor APIs or unfinished subsystems.

## Frameworks introduced

- **Boundary wrapper**: Hide a third-party interface inside a class or close family of classes.
  - When to use: When an external type exposes more power or volatility than the application needs.
  - How: Offer only application operations, keep casts and configuration inside, and prevent the external type from crossing public APIs.
- **Learning tests**: Write focused experiments against a third-party API before integrating it.
  - When to use: When documentation is unclear or behavior is surprising.
  - How: State one expectation, call the dependency as production will, and keep the passing test as an upgrade check.
  - Why it works: Learning and integration become separate problems. The tests preserve discovered behavior.
- **The interface we wish we had**: Define an application-specific interface before an external or unfinished API is available.
  - When to use: When another team or vendor has not finalized its contract.
  - How: Express the client need, build against that interface, then add an Adapter when the real API arrives.
- **Outbound boundary tests**: Exercise the external system through the same path production uses.
  - When to use: Before upgrades and during integration.
  - How: Test the assumptions that matter to the application, not the dependency's entire feature set.

## Key concepts

- **Provider-user tension**: Providers want broad applicability. Users want a small interface for one need.
- **Boundary interface**: A type or protocol owned outside the application.
- **Adapter**: A component that converts the application-owned interface to an external one.
- **Seam**: A point where behavior can be replaced for testing.
- **Learning test**: A controlled experiment that records how an external API behaves.
- **Dependency spread**: The number of places that know a vendor's types, configuration, and conventions.

## Mental models

- Depend on something you control. Translate at the edge.
- Treat every external API reference as a future migration point.
- Learn a dependency in a test harness before mixing it with application logic.
- Design client intent first. Make the adapter absorb external awkwardness.

## Anti-patterns

- **Passing raw boundary types around**: A broad `Map` or vendor client leaks capabilities and change across the system.
- **Learning in production code**: Debugging cannot distinguish misunderstandings of the library from defects in integration logic.
- **Vendor-shaped domain APIs**: Application code adopts another library's types and vocabulary.
- **Waiting for an unfinished interface**: Client work stalls even though its own needs are understood.
- **Upgrading without boundary tests**: The team discovers behavior changes only after integration.

## Code example

```java
public final class Sensors {
    private final Map<String, Sensor> byId = new HashMap<>();

    public Sensor getById(String id) {
        return byId.get(id);
    }
}
```

- **What it demonstrates**: Clients receive the operation they need. They cannot clear the map, insert the wrong type, or depend on the collection choice.

## Reference table

| Boundary state | Technique | Test |
|---|---|---|
| Stable third-party API, broad surface | Wrapper or facade | Outbound boundary tests |
| Poorly understood library | Learning tests | One expectation per experiment |
| Undefined future API | Application-owned interface | Fake implementation for client tests |
| Incompatible external contract | Adapter | Contract tests across the adapter |
| Frequent dependency upgrades | Narrow wrapper plus retained learning tests | Run tests before and after upgrade |

## Worked example

A communications team needs to tell a transmitter to send a data stream at a frequency, but the transmitter team has not designed its API.

Proceed without guessing its internals:

1. Define a local `Transmitter` interface with `transmit(frequency, stream)`.
2. Build the controller against this application-owned interface.
3. Use a fake transmitter to test controller behavior.
4. When the external API appears, implement `TransmitterAdapter`.
5. Add boundary tests that verify the adapter's assumptions.

The controller remains readable and testable. All uncertainty and future API churn stays in one adapter.

## Key takeaways

1. Keep external types out of application public APIs.
2. Wrap dependencies with the smallest interface the application needs.
3. Use learning tests to discover and preserve third-party behavior.
4. Define the interface you want when an external contract does not exist yet.
5. Add adapters and boundary tests at the integration edge.

## Connects to

- **Ch 6**: Good abstractions expose intent and hide representation.
- **Ch 7**: Boundary wrappers translate external failures into local contracts.
- **Ch 9**: Learning and boundary tests must remain fast and repeatable where possible.
- **Ch 11**: Dependency injection supplies adapters without coupling construction to use.

