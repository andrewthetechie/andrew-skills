# Chapter 7: Error Handling

## Core idea

Robustness and readability support each other when error handling remains a separate concern. Keep the normal algorithm visible and move failure translation to explicit boundaries.

## Frameworks introduced

- **Use exceptions rather than return codes**: Let normal logic proceed without immediate nested status checks.
  - When to use: When an operation cannot fulfill its contract.
  - How: Throw an exception with context and handle it at the level that can recover, report, or translate it.
- **Write try-catch-finally first**: Define the failure boundary before filling in risky behavior.
  - When to use: For file, network, device, or transactional code.
  - How: Write a test that forces failure, create the transaction-like `try` scope, and make the handler leave a consistent state.
- **Define exception classes for callers**: Group failures by how callers respond, not only by their low-level origin.
  - When to use: When several vendor exceptions receive the same handling.
  - How: Wrap the dependency and translate related failures into one application exception.
- **Special Case Pattern**: Replace exceptional branching with an object that implements normal behavior for the special case.
  - When to use: When absence has defined domain behavior.
  - How: Return a `PerDiemMealExpenses` object or an empty collection instead of `null` or a control-flow exception.
- **Forbid null by default**: Do not return or pass `null` when a meaningful object, empty collection, or exception can state the contract.

## Key concepts

- **Normal flow**: The business path without scattered checks for exceptional states.
- **Transaction scope**: A `try` block whose handler preserves a consistent program state if any step aborts.
- **Unchecked exception**: An exception that avoids forcing low-level failure types through every intermediate signature.
- **Contextual exception**: An error that states the failed operation, relevant identifiers, and original cause.
- **Caller-oriented classification**: Exception types divided by recovery behavior.
- **Boundary wrapper**: An application-owned interface that translates vendor operations and errors.
- **Special case object**: A polymorphic value that makes an alternate case follow normal flow.

## Mental models

- Treat error handling as one job. A function that manages a `try` block should not also perform unrelated policy.
- Treat a `try` block as a transaction that can stop after any statement.
- Catch at the level that knows what to do. Do not expose vendor details through every layer.
- Treat each `null` as a contract ambiguity. Replace it with an explicit outcome.

## Anti-patterns

- **Return-code pyramids**: Each call forces another nested condition and hides the main operation.
- **Checked-exception cascades**: A low-level change forces signatures through unrelated layers and breaks encapsulation.
- **Vendor exception leakage**: Callers depend on another library's classification and upgrade decisions.
- **Catch-all without context**: A generic message loses the failed operation and relevant data.
- **Null propagation**: Every caller must remember a check, and one omission fails far from the source.
- **Passing null**: The callee rarely has a valid recovery action for an accidentally absent argument.

## Code example

```java
public void shutDown() {
    try {
        shutDownDeviceAndClearQueue();
    } catch (DeviceShutdownFailure error) {
        logger.log(error);
    }
}

private void shutDownDeviceAndClearQueue() {
    DeviceHandle handle = deviceHandleFor(PRIMARY_DEVICE);
    pause(handle);
    clearWorkQueue(handle);
    close(handle);
}
```

- **What it demonstrates**: The handler and the normal shutdown algorithm can be read independently.

## Decision table

| Situation | Preferred response |
|---|---|
| Caller can recover differently | Use distinct caller-oriented exception types |
| Several low-level failures receive one response | Wrap them in one application exception |
| Absence means an empty result | Return an empty collection |
| Absence has domain behavior | Return a Special Case object |
| Operation cannot fulfill its contract | Throw a contextual exception |
| A third-party method returns `null` | Wrap it and translate to the local contract |

## Worked example

A billing service retrieves meal expenses. The data access object throws `MealExpensesNotFound`, and client code catches it only to add a daily allowance. The exception interrupts a case that is normal in the domain.

Refactor it:

1. Define the `MealExpenses` interface around `getTotal()`.
2. Implement `PerDiemMealExpenses` for the no-expense case.
3. Make the data access object always return a `MealExpenses` value.
4. Remove the catch block from the calculation.

The client now always adds `expenses.getTotal()`. The special-case object contains the alternate rule, so normal flow remains linear.

## Key takeaways

1. Separate error handling from the normal algorithm.
2. Design `try` scopes and failure tests before adding risky details.
3. Translate dependency failures at the boundary.
4. Add operation context when throwing or wrapping an exception.
5. Use special-case values or empty collections instead of `null`.
6. Classify exceptions by the caller's response.

## Connects to

- **Ch 3**: Extracted `try/catch` functions preserve one responsibility.
- **Ch 8**: Wrappers isolate vendor APIs and their error models.
- **Ch 9**: Failure-first tests define error contracts.
- **Ch 11**: Boundaries and dependency injection improve test isolation.

