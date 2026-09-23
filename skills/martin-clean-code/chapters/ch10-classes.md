# Chapter 10: Classes

## Core idea

Measure class size by responsibilities, not method count. Small, cohesive classes isolate reasons to change and make extension, testing, and comprehension safer.

## Frameworks introduced

- **Single Responsibility Principle (SRP)**: A class or module should have one reason to change.
  - When to use: When naming, reviewing, or changing a class.
  - How: Write a description of about 25 words without "and," "or," "if," or "but." Each extra reason suggests another class.
- **Cohesion**: A class's methods and fields should form one logical whole.
  - When to use: When subsets of methods use separate subsets of fields.
  - How: Group the related methods and fields into a new class.
- **Open-Closed Principle (OCP)**: Keep classes open for extension but closed for modification.
  - When to use: When adding a feature requires reopening a class with stable existing behavior.
  - How: Separate variants behind a common abstraction so a new variant arrives as a new class.
- **Dependency Inversion Principle (DIP)**: Depend on abstractions, not concrete details.
  - When to use: When a client depends on volatile infrastructure or an external service.
  - How: Define the capability as an interface and inject an implementation.
- **Organize for change**: Let actual change reveal the seam. Do not split a logically complete class only for speculative purity.

## Key concepts

- **Responsibility**: A reason for a class to change.
- **God class**: A class that aggregates unrelated behavior and knowledge.
- **Weasel word**: A vague class-name term such as `Manager`, `Processor`, or `Super` that often hides multiple responsibilities.
- **Cohesive cluster**: Methods that share a focused set of instance variables.
- **Concrete dependency**: A direct tie to implementation details that makes testing and replacement harder.
- **Test double**: A controlled implementation of an abstraction used during testing.
- **Change isolation**: A structure that confines a feature or infrastructure change to one component.

## Mental models

- Count reasons to change, not public methods.
- Treat a hard-to-name class as evidence of mixed responsibilities.
- View low cohesion as a class trying to split itself into coherent parts.
- Prefer many labeled drawers over a few drawers that mix every tool.
- Split when change justifies the seam. Avoid speculative class proliferation.

## Anti-patterns

- **Few methods means small**: A five-method class can still combine unrelated responsibilities.
- **Stop when it works**: A working draft often needs a second pass for organization and cleanliness.
- **Large multipurpose classes**: Readers must understand unrelated logic before changing one concern.
- **Private helpers used by one feature family**: They often reveal a responsibility that deserves its own class.
- **Concrete service dependencies**: Tests become volatile or slow because the class controls infrastructure.
- **Interface for every class**: Dogmatic abstraction increases entity count without protecting a real seam.

## Code example

```java
public interface StockExchange {
    Money currentPrice(String symbol);
}

public final class Portfolio {
    private final StockExchange exchange;

    public Portfolio(StockExchange exchange) {
        this.exchange = exchange;
    }
}
```

- **What it demonstrates**: `Portfolio` depends on price lookup as a concept. Tests can inject fixed prices without contacting an exchange.

## Reference table

| Signal | Likely problem | Response |
|---|---|---|
| Class description needs "and" | Multiple responsibilities | Extract one responsibility |
| A subset of methods shares a subset of fields | Low cohesion | Move the cluster into a new class |
| New variant edits old conditional logic | OCP violation | Add a polymorphic implementation |
| Tests require a live service | Concrete dependency | Introduce and inject an interface |
| New feature has no plausible future use | Speculative design risk | Leave the class alone until change arrives |

## Worked example

The original prime program contains generation, pagination, formatting, and process startup in one large method. Protect its behavior with tests, then make small transformations.

1. Move startup choices into `PrimePrinter`.
2. Move page layout and output into `RowColumnPagePrinter`.
3. Move the number algorithm into `PrimeGenerator`.
4. Give each class names that state its one reason to change.
5. Run the original behavior tests after each move.

The result is longer in lines because names and class boundaries replace implicit knowledge. It is smaller in cognitive scope because each class answers one question.

## Key takeaways

1. Keep classes small by limiting reasons to change.
2. Use names and short descriptions to detect mixed responsibilities.
3. Split cohesive method-field clusters out of low-cohesion classes.
4. Extend stable behavior with new classes instead of editing unrelated code.
5. Depend on injected abstractions at volatile boundaries.
6. Let real change guide decomposition.

## Connects to

- **Ch 3**: Extracting small functions often reveals cohesive classes.
- **Ch 8**: Application-owned interfaces protect boundary code.
- **Ch 11**: Dependency injection separates construction from use.
- **Ch 12**: Simple Design balances small units against needless entity count.

