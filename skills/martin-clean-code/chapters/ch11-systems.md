# Chapter 11: Systems

## Core idea

Apply separation of concerns at system scale. Keep domain logic independent from construction, infrastructure, and cross-cutting policies so architecture can grow incrementally.

## Frameworks introduced

- **Separate construction from use**: Build and wire objects in a startup area. Let runtime code assume valid dependencies already exist.
  - When to use: When classes instantiate their own services or scatter lazy initialization.
  - How: Use `main`, a construction module, a factory, or a dependency-injection container.
- **Separation of Main**: Put all object construction on one side of a boundary, with dependencies pointing from startup toward the application.
  - When to use: When the application does not need runtime control over construction.
- **Abstract Factory**: Let application logic control when an object is created without knowing how it is built.
  - When to use: When runtime behavior must request new domain objects.
- **Dependency Injection (DI)**: Make objects passive about resolving dependencies. Supply dependencies through constructors or setters.
  - When to use: When construction choices vary by environment or test.
- **Modularize cross-cutting concerns**: Keep persistence, transactions, security, caching, and similar policies outside domain objects.
  - When to use: When one policy touches many domain classes.
  - How: Use minimally invasive decorators, proxies, aspects, or framework configuration while preserving plain domain objects.
- **Test-drive system architecture**: Start with the simplest decoupled architecture and add infrastructure when demonstrated needs appear.
  - When to use: During system growth.
  - How: Deliver current stories, preserve seams, measure constraints, and postpone irreversible choices.

## Key concepts

- **Startup concern**: Object construction, configuration, and dependency wiring.
- **Inversion of Control**: Transfer a secondary responsibility, such as dependency creation, to an authoritative mechanism.
- **Plain Old Java Object (POJO)**: Domain code without framework inheritance or infrastructure dependencies.
- **Cross-cutting concern**: A policy that intersects many natural domain boundaries.
- **Aspect**: A modular specification of where a cross-cutting behavior applies.
- **Big Design Up Front (BDUF)**: Attempting to decide the complete architecture before implementation evidence exists.
- **Just-in-time decision**: A choice delayed until the latest responsible point, when more evidence is available.
- **Domain-Specific Language (DSL)**: A small language or API that expresses domain intent at its natural abstraction level.

## Mental models

- Treat startup like construction scaffolding. Runtime logic should not carry it.
- Keep domain objects ignorant of containers and frameworks so tests can instantiate them directly.
- Delay choices when clean seams preserve options. Delay is useful only while change remains cheap.
- Select standards for demonstrated value, not status or popularity.
- Make infrastructure disappear from the main domain story.

## Anti-patterns

- **Scattered lazy initialization**: Runtime getters hard-code construction, hide a global policy, and add test branches.
- **Invasive frameworks**: Domain objects inherit container types or implement lifecycle methods unrelated to the domain.
- **Architecture-first overbuilding**: The team pays for scale and flexibility that current stories do not require.
- **Standard by default**: A heavy standard replaces a simpler solution without measured benefit.
- **Framework-shaped domain logic**: User stories become hard to read and test because infrastructure dominates the code.
- **Premature irreversible decisions**: Early choices use less feedback and narrow future options.

## Code example

```java
public final class OrderService {
    private final LineItemFactory lineItems;

    public OrderService(LineItemFactory lineItems) {
        this.lineItems = lineItems;
    }

    public void addItem(Order order, Product product, int quantity) {
        order.add(lineItems.create(product, quantity));
    }
}
```

- **What it demonstrates**: Runtime code controls when a line item is needed. A construction module controls how it is built.

## Decision table

| Need | Mechanism |
|---|---|
| Startup chooses all implementations | Separation of Main and constructor injection |
| Runtime chooses creation time | Abstract Factory |
| Environment selects dependency graph | DI container or configuration module |
| One policy wraps many calls | Decorator, proxy, or aspect-like mechanism |
| Framework logic obscures domain rules | Move domain behavior into POJOs |
| Future scale is uncertain | Start simple, measure, and evolve behind seams |

## Worked example

A service method lazily creates `MyServiceImpl` when its field is null. The method now selects an implementation, resolves constructor dependencies, caches state, and returns the service. Tests must manipulate its internal field before the first call.

Refactor it:

1. Add a constructor parameter for the service abstraction.
2. Move `MyServiceImpl` construction into `main` or a configuration module.
3. Pass a test double directly in unit tests.
4. If delayed construction is measured as necessary, inject a provider or factory.
5. Keep runtime code unaware of the concrete implementation.

The application now has one construction strategy. The service class has one runtime responsibility.

## Key takeaways

1. Separate object construction and dependency wiring from runtime use.
2. Keep dependency arrows pointed from construction toward application policy.
3. Use factories when runtime code controls creation time.
4. Keep domain objects independent from infrastructure frameworks.
5. Evolve architecture from simple, decoupled parts as needs become concrete.
6. Delay decisions while clean boundaries keep alternatives available.
7. Use standards only when they add demonstrated value.

## Connects to

- **Ch 8**: Adapters protect domain code from boundary APIs.
- **Ch 10**: DIP and SRP provide the class-level foundation.
- **Ch 12**: Simple Design supplies the incremental architecture discipline.
- **Ch 13**: Concurrency is a separate system concern with its own lifecycle.

