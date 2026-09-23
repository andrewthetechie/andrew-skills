# Chapter 13: Concurrency

## Core idea

Concurrency separates what work occurs from when it occurs, but it multiplies execution paths and failure modes. Isolate thread-aware code, minimize shared state, and test under varied schedules and loads.

## Frameworks introduced

- **Concurrency as decoupling**: Separate work from schedule to improve structure, response time, or throughput.
  - When to use: When independent work spends significant time waiting, must serve simultaneous users, or can run in parallel.
  - Failure mode: Concurrency adds overhead and does not automatically improve performance.
- **Concurrency SRP**: Threading policy is its own reason to change.
  - When to use: In every concurrent design.
  - How: Keep domain work in thread-ignorant objects. Put scheduling, locking, and lifecycle in small thread-aware components.
- **Minimize shared data**: Reduce both the number of shared values and the places that mutate them.
  - When to use: Before adding locks.
  - How: Partition data, use immutable copies, merge results in one thread, and prefer local variables.
- **Keep critical sections small**: Protect exactly the state transition that must be atomic.
  - When to use: When shared mutation cannot be removed.
  - How: Use few synchronized regions and avoid holding locks across I/O or unrelated work.
- **Know execution models**: Recognize Producer-Consumer, Readers-Writers, and Dining Philosophers problems.
  - When to use: When threads coordinate through queues, shared read-mostly state, or multiple resources.
- **Schedule-jiggling tests**: Vary thread count, timing, load, and platform to expose rare paths.
  - When to use: From the start of concurrent work.
  - How: Add test-only yields, sleeps, randomized timing, or instrumentation. Log every failing configuration.
- **Break a deadlock condition**: Deadlock requires mutual exclusion, lock-and-wait, no preemption, and circular wait.
  - When to use: During resource-allocation design and incident diagnosis.
  - How: Remove any one condition. A global resource order is the common way to break circular wait.

## Key concepts

- **Bound resource**: A fixed-size resource such as a connection pool or buffer.
- **Mutual exclusion**: Only one thread can use a resource or state section at a time.
- **Starvation**: A thread cannot proceed for an excessive time.
- **Deadlock**: Threads wait permanently for resources held by each other.
- **Livelock**: Threads remain active but repeatedly prevent progress.
- **Critical section**: Code that must not run simultaneously for correctness.
- **Thread-safe collection**: A library type that implements composite concurrent operations correctly.
- **Monte Carlo testing**: Repeated tests with varied scheduling and tuning values.

## Mental models

- Treat threads as abstractions of schedule. A correct design must survive many legal orderings.
- Treat a sporadic failure as a concurrency defect until evidence shows otherwise.
- First prove domain logic without threads. Then test scheduling code separately.
- Prefer ownership and data partitioning over locking.
- Design shutdown as a first-class protocol, not a final cleanup task.

## Anti-patterns

- **Concurrency for assumed speed**: CPU-bound work, contention, and coordination can make it slower.
- **Embedded threading details**: Domain defects and schedule defects become hard to distinguish.
- **Broad synchronization**: Large critical sections reduce throughput and increase deadlock risk.
- **Several dependent synchronized calls**: State can change between calls unless one operation owns the whole transition.
- **Ignored one-offs**: Rare failures accumulate more code above a broken design.
- **Single-platform confidence**: Operating systems and runtimes expose different schedules.
- **Late shutdown design**: Blocked producer-consumer pairs can prevent termination forever.

## Reference tables

### Execution models

| Model | Main risk | Primary design concern |
|---|---|---|
| Producer-Consumer | Full or empty bounded queue | Correct signaling and shutdown |
| Readers-Writers | Starvation or stale data | Balance throughput with writer progress |
| Dining Philosophers | Deadlock and livelock | Resource acquisition protocol |

### Deadlock conditions

| Required condition | Typical break |
|---|---|
| Mutual exclusion | Use shareable or atomic resources where possible |
| Lock and wait | Acquire all or release and retry |
| No preemption | Let an owner release resources on request |
| Circular wait | Enforce one global acquisition order |

## Code example

```java
public String nextPageOrNull() {
    String url;
    synchronized (urls) {
        if (!urls.hasNext()) return null;
        url = urls.next();
    }
    return pageReader.getPageFor(url);
}
```

- **What it demonstrates**: Synchronization protects only iterator mutation. Slow network I/O happens outside the critical section.

## Worked example

A service has database and message-queue connection pools. Create operations acquire message then database. Update operations acquire database then message. Under load, each group can hold one pool while waiting for the other.

Prevent circular wait:

1. Define one global resource order, such as database then message queue.
2. Make every operation acquire resources in that order.
3. Keep the hold time short and release both in all failure paths.
4. Add load tests that exceed pool sizes.
5. Test cancellation and shutdown while threads wait.

The design removes one necessary deadlock condition. It still requires tests for starvation, timeout, and resource leaks.

## Key takeaways

1. Use concurrency only for a measured structural or performance need.
2. Separate thread-aware code from domain logic.
3. Avoid sharing. When sharing is necessary, minimize mutation and critical sections.
4. Learn the library and standard execution models before inventing synchronization.
5. Design and test graceful shutdown early.
6. Run concurrency tests repeatedly across thread counts, loads, and target platforms.
7. Break at least one required deadlock condition by design.

## Connects to

- **Ch 7**: Concurrent failure and shutdown paths need explicit, consistent error handling.
- **Ch 9**: Independent, repeatable tests provide the base for stress and schedule variation.
- **Ch 10**: SRP separates scheduling from domain work.
- **Appendix A**: The source expands throughput calculations, deadlock prevention, and instrumented tests.

