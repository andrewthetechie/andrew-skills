# Chapter 9: Unit Tests

## Core idea

Tests preserve the ability to change production code. They must be as readable and maintainable as production code, while remaining fast enough to run continuously.

## Frameworks introduced

- **The Three Laws of TDD**: Start production code only after a test fails. Write only enough test to fail and only enough code to pass.
  - When to use: During feature work and defect repair.
  - How: Alternate between a very small failing test and the smallest passing implementation, then refactor.
- **Build-Operate-Check**: Structure each test as setup, one operation, and verification.
  - When to use: When test intent is buried under fixtures and API details.
  - How: Extract a testing language that makes the three phases visible.
- **Domain-Specific Testing Language**: Build helpers that state scenarios and outcomes in domain terms.
  - When to use: When tests repeat low-level construction, requests, parsing, or assertions.
  - How: Refactor repeated mechanics into named helpers. Let the language emerge from real tests.
- **Single Concept per Test**: Each test should prove one behavioral rule.
  - When to use: When a test contains unrelated examples or several reasons to fail.
  - How: Split by concept. Minimize assertions, but use several when they support one conclusion.
- **F.I.R.S.T.**: Tests should be Fast, Independent, Repeatable, Self-Validating, and Timely.
  - When to use: When evaluating a test suite's operational quality.
  - How: Remove slow dependencies, shared state, environmental assumptions, manual checks, and delayed test writing.

## Key concepts

- **Test cleanliness**: Clear names, small functions, focused fixtures, and low duplication in test code.
- **The -ilities**: Flexibility, maintainability, and reusability enabled by a trusted test suite.
- **Dual standard**: Test code can trade runtime efficiency for expression, but it cannot trade away cleanliness.
- **Boolean outcome**: A self-validating test passes or fails without human interpretation.
- **Documentation by example**: Tests show how a unit behaves in concrete scenarios.

## Mental models

- Treat test code as production infrastructure. Dirty tests eventually make production changes unsafe.
- Optimize a test for the reader who needs to diagnose its failure.
- Let tests create design pressure toward small, decoupled classes.
- Distinguish "one assertion" from "one concept." Several checks can support one behavioral claim.

## Anti-patterns

- **Throwaway tests**: Manual drivers prove one moment and provide no regression protection.
- **Second-class test code**: Weak names and duplication make the suite expensive, so the team stops maintaining it.
- **Detail-heavy tests**: Parsing and setup mechanics hide the behavior under test.
- **Dependent tests**: One failure cascades into unrelated failures and prevents isolated execution.
- **Environment-bound tests**: Network, machine, or ordering assumptions create excuses for failures.
- **Manual validation**: Logs or file comparisons make pass or fail subjective.
- **Miscellaneous test methods**: Several rules in one test obscure missing boundary cases.

## Code example

```java
@Test
public void symbolicLinksAreNotInXmlPageHierarchy() throws Exception {
    Page page = makePage("PageOne");
    makePages("PageOne.ChildOne", "PageTwo");
    addLinkTo(page, "PageTwo", "SymPage");

    submitRequest("root", "type:pages");

    assertResponseIsXml();
    assertResponseContains("PageOne", "PageTwo", "ChildOne");
    assertResponseDoesNotContain("SymPage");
}
```

- **What it demonstrates**: Test helpers remove irrelevant APIs and leave one readable scenario.

## Reference table

| F.I.R.S.T. rule | Failure signal | Corrective action |
|---|---|---|
| Fast | Developers avoid the suite | Isolate I/O and reduce scope |
| Independent | Order changes results | Give each test its own fixture |
| Repeatable | A test needs one machine or network | Replace environmental dependencies |
| Self-Validating | A person reads logs to decide | Assert the outcome in code |
| Timely | Production code is hard to test | Write the test immediately before the behavior |

## Worked example

A date test adds one month, two months, and a nested pair of one-month additions in one method. The test appears comprehensive, but it mixes three rules and omits February behavior.

Refactor it:

1. State each rule in domain language.
2. Create one test for clamping a 31st day into a 30-day month.
3. Create one test for preserving the 31st when the target month supports it.
4. Create one test for preserving a 30th when the target supports more days.
5. Add the revealed boundary case for February 28.

Splitting by concept exposes the general rule: after adding months, the day cannot exceed the target month's last day.

## Key takeaways

1. Keep test code as clean as production code.
2. Use the Three Laws of TDD for short feedback cycles.
3. Build a domain-specific testing language through refactoring.
4. Test one concept per method and minimize assertions per concept.
5. Enforce F.I.R.S.T. so developers run tests continuously.
6. Use tests to preserve the freedom to improve production design.

## Connects to

- **Ch 1**: Code without tests does not meet the book's clean-code standard.
- **Ch 10**: Test pressure promotes small classes and dependency inversion.
- **Ch 12**: Passing tests are the first and highest-priority rule of Simple Design.
- **Ch 14**: Successive refinement depends on a continuously passing suite.
