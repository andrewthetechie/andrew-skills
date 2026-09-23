# Chapter 5: Formatting

## Core idea

Formatting communicates structure before a reader interprets individual statements. A team should use a consistent, automated style that makes conceptual relationships visible.

## Frameworks introduced

- **The Newspaper Metaphor**: Organize a source file from headline and synopsis to increasing detail.
  - When to use: When ordering classes, methods, and declarations in a file.
  - How: Put high-level policy first. Place called methods below callers. Leave low-level details near the end.
- **Vertical openness and density**: Use blank lines to separate concepts and compact layout to show close association.
  - When to use: When code looks like one continuous block or related declarations are scattered.
  - How: Separate package, imports, fields, and methods. Keep strongly related lines together.
- **Vertical distance**: Keep related concepts physically close so readers do not search and retain remote details.
  - When to use: When readers scroll between callers, callees, fields, and dependent logic.
  - How: Declare variables near use, group related methods, and put a caller above its callee.
- **Horizontal openness and density**: Let spaces reveal association and operator structure.
  - When to use: In expressions, assignments, calls, and argument lists.
  - How: Separate assignment sides and arguments. Keep function names attached to their parentheses.
- **Team Rules**: The team owns one formatting style, even when individual preferences differ.
  - When to use: On every shared codebase.
  - How: Agree on a small rule set, encode it in an automatic formatter, and apply it consistently.

## Key concepts

- **Visual hierarchy**: Indentation exposes nested scopes and lets readers skip irrelevant blocks.
- **Conceptual affinity**: Related code belongs close together even without a direct call dependency.
- **Vertical ordering**: Dependencies normally point down the file from policy to detail.
- **Horizontal alignment**: Column-based spacing that often emphasizes syntax instead of intent.
- **Dummy scope**: An empty control body that must remain visually obvious if it cannot be removed.
- **Formatting precedent**: The style of current code guides later changes after the original implementation is gone.

## Mental models

- Treat a file as an article that supports skimming. A reader should understand its purpose from the top.
- Treat blank lines as paragraph breaks and dense groups as sentences within one thought.
- Make distance express relationship. Strong dependence means short distance.
- Use formatting tools to remove personal negotiation from routine edits.

## Anti-patterns

- **Large files by default**: Thousands of lines hide concepts and increase navigation cost.
- **Remote declarations**: Fields or locals hidden far from their use force readers to search.
- **Horizontal alignment**: Aligned columns hide overly long declaration lists and create formatter churn.
- **Collapsed scopes**: One-line classes and control blocks conceal hierarchy.
- **Invisible empty loops**: A trailing semicolon can look accidental. Put any required empty body on its own indented line.
- **Individual styles in shared code**: Inconsistent gestures force readers to relearn the visual grammar in each file.

## Code example

```java
public Response makeResponse(Context context, Request request) throws Exception {
    String pageName = getPageNameOrDefault(request, "FrontPage");
    loadPage(pageName, context);
    if (page == null) return notFoundResponse(context, request);
    return makePageResponse(context);
}

private String getPageNameOrDefault(Request request, String defaultName) {
    String pageName = request.getResource();
    return isBlank(pageName) ? defaultName : pageName;
}
```

- **What it demonstrates**: The entry point presents the story. Its first supporting method follows directly below.

## Reference table

| Concern | Book guidance | Practical default |
|---|---|---|
| File length | Prefer small files. Many useful systems keep most files below 200 lines and rarely exceed 500 | Split when a file carries several concepts |
| Line length | Short lines dominate readable projects | Aim below 100 to 120 characters |
| Local variables | Declare near first use | Place them at the top of a short function or block |
| Instance variables | Keep in one known location | Put them at the top of the class |
| Function order | Caller before callee | Read from policy down to implementation |
| Indentation | Preserve visible scope hierarchy | Never collapse structure only to save lines |

## Worked example

A responder class contains fields in the middle, methods in alphabetical order, and helper functions far above their callers. A reader must search repeatedly to understand the response path.

Reformat and reorder it:

1. Move instance variables to the team's standard location.
2. Put the public response method first.
3. Place each directly called helper below the caller.
4. Group conceptually similar overloads together.
5. Add blank lines only between distinct concepts.
6. Apply the team formatter.

No runtime behavior changes, but the source now presents a predictable route from request policy to response details.

## Key takeaways

1. Use formatting to communicate relationships and abstraction levels.
2. Keep files small enough to scan and lines short enough to read without horizontal navigation.
3. Put related declarations and functions near each other.
4. Order functions from high-level policy to low-level detail.
5. Use one automated team format.

## Connects to

- **Ch 3**: The Stepdown Rule determines function order.
- **Ch 10**: Small classes usually produce small, coherent files.
- **Ch 17**: Vertical separation and configurable-data heuristics extend these rules.

