# Chapter 4: Comments

## Core idea

Use a comment only when code cannot express essential intent, rationale, or consequences. Comments decay separately from code, so clear code is safer than an explanation of unclear code.

## Frameworks introduced

- **Explain yourself in code**: Replace a comment that restates intent with a named function, variable, class, or data structure.
  - When to use: Before adding any explanatory comment.
  - How: Write the intended explanation, then test whether that sentence can become a name or abstraction.
- **Comment value test**: Keep a comment when it supplies information the code cannot state locally and accurately.
  - When to use: During review and cleanup.
  - How: Ask whether the comment explains intent, a consequence, a legal requirement, a public contract, or an unavoidable external constraint.
- **Truth locality**: Put information beside the code that controls it.
  - When to use: When a local comment describes system-wide configuration or remote behavior.
  - How: Move the rule to the owning abstraction, test, type, or documentation source.
- **Delete recoverable history**: Use version control for old code, authorship, and change journals.
  - When to use: When code is commented out or files contain manual history logs.
  - How: Delete the clutter. Recover it from version control if it becomes necessary.

## Key concepts

- **Explanation of intent**: A comment that records why a non-obvious decision exists.
- **Clarification**: A translation of an obscure external argument or return value that the local code cannot change.
- **Warning of consequences**: A precise note that prevents a plausible but unsafe change.
- **Amplification**: A note that marks an easily missed detail as operationally significant.
- **Public API documentation**: Consumer-facing contract information that cannot rely on implementation knowledge.
- **Noise comment**: A comment that restates syntax or adds no information.
- **Nonlocal information**: A comment about behavior controlled elsewhere and likely to become stale.
- **Inobvious connection**: A comment whose relationship to the adjacent expression remains unclear.

## Mental models

- Treat every comment as a second source of truth that must stay synchronized with code.
- Ask whether a reader can verify the comment from the adjacent code. If not, the comment has high drift risk.
- Prefer a small function with a precise name over a block comment that explains tangled control flow.
- Use comments for "why" and external constraints. Let code state "what" and "how" when it can.

## Anti-patterns

- **Comments that compensate for bad code**: They preserve the mess and add another maintenance burden.
- **Mumbling**: Vague notes such as an unexplained empty catch block force readers to search elsewhere.
- **Redundant and mandated comments**: Required comments on every field or function hide useful information in noise.
- **Journal comments and bylines**: Version control already records authors and changes.
- **Commented-out code**: Readers cannot know whether it is important, so it remains indefinitely.
- **Position markers and closing-brace comments**: They compensate for files and functions that are too large.
- **HTML in source comments**: Markup makes the source hard to read and assigns presentation work to the author.
- **Private Javadocs**: Formal documentation on internal details adds clutter without serving API consumers.

## Code example

```java
// Before
// Check whether the employee qualifies for full benefits.
if ((employee.flags & HOURLY_FLAG) != 0 && employee.age > 65) { ... }

// After
if (employee.isEligibleForFullBenefits()) { ... }
```

- **What it demonstrates**: A named predicate expresses the rule in executable code and cannot drift away from its implementation.

## Reference table

| Comment type | Default action | Keep only when |
|---|---|---|
| Legal notice | Keep or link to the standard license | Policy requires it |
| Public API contract | Keep and maintain | Consumers cannot infer the contract from code |
| Intent or rationale | Keep briefly | The decision is not expressible in code |
| Consequence warning | Keep near the hazard | A reasonable cleanup could break behavior |
| TODO | Track and review | It names a real deferred job and is not an excuse for bad code |
| Restatement of code | Delete | No exception |
| Commented-out code | Delete | Version control can recover it |
| Change history or author | Delete | Version control owns the information |

## Worked example

The prime generator begins as one long method with section comments for declarations, initialization, sieving, counting, and result construction. The comments make the file look documented, but they expose that the function contains several responsibilities.

Refactor it as follows:

1. Extract `uncrossIntegersUpTo`, `crossOutMultiples`, and `putUncrossedIntegersIntoResult`.
2. Replace comments such as "bump count" with precise names such as `numberOfUncrossedIntegers`.
3. Keep only the algorithm description and the reason the square root limits iteration.
4. Verify that each remaining comment adds information the code cannot express.

The result has fewer comments and more executable explanation. The algorithm's rationale remains where a name alone cannot carry it.

## Key takeaways

1. Rewrite unclear code before explaining it with comments.
2. Keep comments that state intent, constraints, consequences, or public contracts.
3. Delete redundant, stale, historical, and commented-out material.
4. Keep each comment local to the code that controls its truth.
5. Review TODO comments and remove them when the deferred work becomes possible.
6. Make every remaining comment precise enough to verify.

## Connects to

- **Ch 2**: Better names remove many explanatory comments.
- **Ch 3**: Small functions replace section headers and closing-brace notes.
- **Ch 7**: Explicit error handling is safer than comments in empty catch blocks.
- **Ch 17**: Comment smells provide a compact review checklist.

