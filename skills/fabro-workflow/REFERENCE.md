# Fabro workflow reference

Condensed from `docs/public/reference/dot-language.mdx`, `docs/public/workflows/*.mdx`, and
`docs/public/execution/run-configuration.mdx` in the fabro repo. When in doubt, those files win.

## File structure

Only `digraph` is supported — no `graph` (undirected), no `strict`. The graph name is
required. Semicolons are optional. Comments are `//` and `/* */`.

Node IDs: letter or underscore, then letters/digits/underscores.

Value types: quoted string (`\"`, `\\`, `\n`, `\t` escapes), integer, float, `true`/`false`,
duration (`250ms`, `30s`, `15m`, `2h`, `1d`), bare identifier.

## Node types

| Shape | Handler | Purpose |
|---|---|---|
| `Mdiamond` | start | Entry point (exactly one) |
| `Msquare` | exit | Terminal (exactly one) |
| `box` (default) | agent | Multi-turn LLM with tool access |
| `tab` | prompt | Single LLM call, no tools |
| `parallelogram` | command | Shell/Python script |
| `hexagon` | human | Human-in-the-loop gate |
| `diamond` | conditional | Route on conditions |
| `component` | parallel | Fan-out to concurrent branches |
| `tripleoctagon` | parallel.fan_in | Merge branch results |
| `insulator` | wait | Pause for a duration |
| `house` | stack.manager_loop | Sub-workflow orchestration |

`type="..."` overrides shape-based mapping. Start also matches ID `start`/`Start`; exit
matches `exit`/`Exit`/`end`/`End`.

Inference when both `shape` and `type` are omitted: a node with `script` is a command node;
everything else is an agent node. An explicit `shape`/`type` always wins (`shape=box` with a
`script` is an agent node and the `script` is ignored).

## Graph attributes

| Attribute | Type | Description |
|---|---|---|
| `goal` | String | Workflow objective; guides agents. Templated. |
| `rankdir` | Ident | `LR` or `TB` |
| `model_stylesheet` | String | CSS-like model assignment rules. Root value is templated with `inputs`/`vars` only. |
| `default_max_retries` | Int | Default retry count (default 0) |
| `on_failure` | String | `route` (default), `exit`, `succeed` |
| `retry_target` | String | Default node ID to jump to on retry |
| `fallback_retry_target` | String | Fallback if primary retry target fails |
| `default_fidelity` | String | Default context fidelity |
| `default_thread` | String | Default thread ID |
| `max_node_visits` | Int | Max visits per node per run (0 = unlimited) |
| `stall_timeout` | Duration | Default `1800s`; 0 disables |
| `loop_restart_signature_limit` | Int | Repeat-failure abort threshold (default 3) |

## Node attributes — all nodes

| Attribute | Type | Description |
|---|---|---|
| `label` | String | Display name; also human-gate option matching |
| `shape` / `type` | Ident / String | Handler selection |
| `class` | String | Stylesheet classes, space-separated |
| `timeout` | Duration | Execution timeout; waiting on human input doesn't consume it |
| `max_visits` | Int | Per-node override of `max_node_visits` |
| `on_failure` | String | `route` / `exit` / `succeed`; overrides graph level |
| `max_retries` | Int | Override default retry count |
| `retry_policy` | String | `none`, `standard`, `aggressive`, `linear`, `patient` |
| `retry_target` / `fallback_retry_target` | String | Node IDs |
| `goal_gate` | Bool | Run fails unless this node ends `succeeded`/`partially_succeeded` |
| `allow_partial` | Bool | On retry exhaustion, promote to `partially_succeeded` (default false) |
| `selection` | String | `deterministic` (default) or `random`; incompatible with conditional edges |
| `auto_status` | Bool | **Deprecated** alias for `on_failure="succeed"` |

## Agent and prompt nodes

| Attribute | Type | Description |
|---|---|---|
| `prompt` | String | Instructions. Templated. Supports `@path/to/file.md`. |
| `reasoning_effort` | String | `low` / `medium` / `high` (default `high`) |
| `max_tokens` | Int | Max output tokens |
| `fidelity` | String | `compact`, `full`, `summary:high|medium|low`, `truncate` |
| `thread_id` | String | Shared conversation thread. **Requires `fidelity="full"`.** |
| `model` | String | Explicit model ID (overrides stylesheet) |
| `provider` | String | Explicit provider (auto-inferred from catalog when omitted) |
| `project_memory` | Bool | Include `AGENTS.md`/`CLAUDE.md` as system prompt (default true) |
| `output_schema` | String | `routing`, `@path/to/schema.json`, or inline JSON Schema |
| `output_retries` | Int | Corrective structured-output turns (default 2); *not* `max_retries` |
| `backend` | String | `api` (default) or `acp`. Prompt nodes are API-only. |
| `acp.command` / `acp.config` | String | For `backend="acp"`; mutually exclusive |

### Structured output

- `output_schema="routing"` requires a JSON object with at least one of
  `preferred_next_label`, `outcome`, `failure_reason`, `suggested_next_ids`,
  `context_updates`.
- Custom schema output lands in context at `output.{node_id}`. Routing output updates
  routing fields and merges `context_updates` into flat context keys that conditions read.
- Command nodes validate merged stdout+stderr **only after exit code 0**, selecting the last
  JSON object. Print the intended JSON last. A schema failure there is deterministic and
  non-retryable — no repair turn, no `status.json` fallback.
- `backend="acp"` + `output_schema` is unsupported.

## Command nodes

| Attribute | Type | Description |
|---|---|---|
| `script` | String | Required. Presence infers a command node. |
| `language` | String | `shell` (default) or `python` |
| `stdin_source` | String | Flat context key piped to stdin; `context.NAME` then bare `NAME` |
| `output_schema` | String | Same as above |

`script` substitution quotes each value as **one shell argument** (or, for Python, one string
literal). Put the token where one word/expression is valid; do not add your own quotes.
`{{ env.X }}` and `{{ secrets.X }}` are **rejected** — use `$NAME` / `os.environ["NAME"]` and
supply the value via `[environments.<slug>.env]`, where `{{ secrets.* }}` does resolve.

## Parallel (fan-out) nodes

| Attribute | Type | Description |
|---|---|---|
| `max_parallel` | Int | Max concurrent branches (default 4); always waits for all |
| `for_each` | String | Flat context key holding a JSON array |

With `for_each`: exactly one outgoing edge, target must be agent or prompt, no nesting, hard
cap of 1000 items. Each clone gets the prompt plus the item as pretty JSON inside a fresh
`<untrusted-{16 hex}>` fence — **there is no item interpolation syntax**. The fence does not
restrict tools, so give the target only appropriate tool access. Results keep input order and
carry `index` and `item_label` (from the item's `name`, then `label`, then index). An empty
array skips straight to fan-in.

Concurrent branches cannot share sessions: on a fork-to-branch edge, explicit `full` degrades
to `summary:high` and branch-level `thread_id` is inert. Fidelity resolves edge, then node.

## Wait, human, and manager-loop nodes

| Node | Attribute | Description |
|---|---|---|
| wait | `duration` | Required, e.g. `"30s"` |
| human | `question_type` | `yes_no`, `confirmation`, `multiple_choice`, `multi_select`, `freeform` |
| human | `review_target` | Bool; present a typed review target as the primary link |
| human | `human.default_choice` | Target node on timeout |
| manager | `stack.child_workflow` | Path to child `.fabro` (or `stack.child_dot_source`) |
| manager | `manager.poll_interval` | Default `45s` |
| manager | `manager.max_cycles` | Default 1000 |
| manager | `manager.stop_condition` | Expression; true stops the child early |

## Edge attributes

| Attribute | Type | Description |
|---|---|---|
| `label` | String | Display text; human-gate option matching |
| `condition` | String | Boolean expression (see below) |
| `weight` | Int | Tiebreak priority, higher wins (default 0) |
| `fidelity` | String | Per-transition override |
| `thread_id` | String | Per-transition override; inert on fork-to-branch edges |
| `loop_restart` | Bool | Restart from the target: clears stage history, retry counts, and context (visit counts kept). Failed outcomes may only take it for `transient_infra` failures. |
| `freeform` | Bool | On a human-gate edge, accept free text instead of fixed choices |

## Condition grammar

```
Expr      ::= OrExpr
OrExpr    ::= AndExpr ('||' AndExpr)*
AndExpr   ::= UnaryExpr ('&&' UnaryExpr)*
UnaryExpr ::= '!' UnaryExpr | Clause
Clause    ::= Key Op Value | Key          // bare key = truthiness check
Op        ::= '=' | '!=' | '>' | '<' | '>=' | '<=' | 'contains' | 'matches'
```

Keys: `outcome` (`succeeded` / `failed` / `partially_succeeded` / `skipped`),
`preferred_label`, `context.KEY`, or bare `KEY` (context shorthand).

`&&` binds tighter than `||`. A bare key passes when the value is non-empty, not `"false"`,
and not `"0"`.

```dot
gate -> deploy    [condition="outcome=succeeded && context.tests_passed=true"]
gate -> proceed   [condition="outcome=succeeded || outcome=partially_succeeded"]
gate -> alert     [condition="context.log contains error"]
gate -> v2        [condition="context.version matches ^v2\\."]
gate -> slow_path                              // unconditional fallback
```

## Transition cascade

After a node completes (retries run first), Fabro picks the next step in this order:

1. **Direct jump** — the outcome's `jump_to_node` bypasses edge selection.
2. **Condition match** — highest `weight` wins, lexical tiebreak on target node ID.
3. **Preferred label** — matched against edge `label`s. `[A]`-style accelerator prefixes are
   stripped before matching.
4. **Suggested next** — edge pointing at a suggested node ID.
5. **Failure policy** — for a failed outcome with no explicit route: `exit` skips the
   unconditional fallback; `succeed` promotes to `succeeded` and routes as success; `route`
   (default) continues to step 6.
6. **Unconditional fallback** — `weight`, then lexical tiebreak.
7. **Retry target** — node-level then graph-level `retry_target` / `fallback_retry_target`.

No next node ⇒ the run ends. Conditioned edges, matching preferred labels, and matching
suggested IDs are *explicit recovery routes* and take priority under every policy; an
**unmatched** label or node ID does not make an unconditional edge explicit.

`selection="random"` only changes the pick-one-from-candidates step within a tier; the
cascade order is unchanged. Edges with weight ≤ 0 count as weight 1.

### Agent-driven routing

Agent and prompt nodes influence routing by emitting the last JSON object in their response
containing any recognized field. You must instruct the model to emit it — Fabro scans
automatically but does not prompt for it.

```json
{ "preferred_next_label": "fix", "suggested_next_ids": ["implement"], "context_updates": { "tests_passed": true } }
```

Agent routing fallbacks: response text, then `status.json`, then the last file the agent
touched (only `.json`/`.md`, whose final JSON object holds the directive, with only
whitespace after). Custom schemas and prompt nodes validate response text only.

## Templating

Rendered as full MiniJinja: graph `goal`, node `prompt`, root `model_stylesheet`.
Value substitution only: command `script`. Everything else is literal.

| Expression | Available in |
|---|---|
| `{{ goal }}` | prompts and scripts (a goal cannot reference itself — `goal_self_reference` is an error) |
| `{{ inputs.NAME }}` | goal, prompt, stylesheet, script |
| `{{ vars.NAME }}` | goal, prompt, stylesheet, script (server-managed, snapshotted at run creation) |

Secrets are never available in these templates.

Render order: parse DOT and imports → resolve literal `import`/`@file`/child refs → render
`goal` → render `prompt`s (with the rendered goal) → render and parse `model_stylesheet` →
substitute `script` values. Substituted text is never rescanned.

Undefined variables render empty and record `template_undefined_variable` — a *warning* from
`fabro validate`, an *error* at run creation. In a `script`, the token is left in place so
validation output shows what is unbound. Offline validation cannot read the server's variable
store, so `{{ vars.* }}` always warns there.

Includes: `{% include "partial.md" %}` resolves relative to the template file and may nest.
Dynamic include expressions (`{% include inputs.partial %}`) are rejected.

Escape with `{% raw %}...{% endraw %}` or `{{ '{{' }}`.

Input precedence (highest first): CLI `-I/--input` (sparse per-key merge) → `workflow.toml`
`[run.inputs]` → `.fabro/project.toml` → `~/.fabro/settings.toml`. **TOML layers replace the
whole `[run.inputs]` map**; only CLI flags merge per key.

## File references

`@path` loads a file relative to the workflow file; `~` and `..` are supported. Validated at
parse time. Untracked `@file` references are inlined into the DOT source at prepare time so
they survive sandboxes that only see the git tree.

```dot
simplify [prompt="@prompts/simplify.md"]
audit    [shape=tab, output_schema="@schemas/audit-result.schema.json"]
shared   [prompt="@~/shared-prompts/review.md"]
```

## Imports

A node with `import="./validate.fabro"` splices that graph in at parse time. Imported node
IDs are prefixed with the placeholder ID and a dot (`lint` → `validate.lint`), so the same
file can be imported multiple times. The placeholder's start/exit sentinels are discarded and
its incoming/outgoing edges rewire to the subgraph's entry and exit.

Contract for an imported file — violation "poisons" the placeholder (`import` becomes
`import_error`) and `fabro validate` reports a graph error:

- Exactly one start with exactly one outgoing edge.
- Exactly one exit with exactly one incoming edge.
- Boundary edges carry no semantic attributes (`condition`, `label`, `weight`, `fidelity`,
  `thread_id`, `loop_restart`, `freeform`).

Imports are a parse-time merge with no runtime boundary. For real runtime delegation to a
separate durable run, use child runs instead.

## Subgraphs and stylesheets

A subgraph's `label` becomes a CSS class on all its nodes (`"Implementation"` → `.implementation`,
`"Loop A"` → `.loop-a`). Node and edge defaults inside a subgraph are scoped and don't leak.
Edges may cross subgraph boundaries.

```dot
graph [model_stylesheet="
    *       { model: claude-haiku-4-5; reasoning_effort: low; }
    .coding { model: claude-sonnet-4-5; reasoning_effort: high; }
    #review { model: claude-sonnet-4-5; reasoning_effort: high; }
"]
```

Selectors: `*` (all), `.class`, `#node_id`. Node-level `model`/`provider` attributes override
the stylesheet.

## Validation rules

`fabro validate` enforces:

- Exactly one start node and one exit node; all nodes reachable from start.
- No incoming edges to start, no outgoing edges from exit.
- Every edge target is a declared node.
- Condition expressions parse; stylesheet syntax is valid.
- Agent and prompt nodes have a `prompt`.
- `@file` references exist.
- Conditional nodes have multiple outgoing conditioned edges.
- Retry targets reference existing nodes; goal gates have retry configuration.
- `thread_id` requires `fidelity="full"`.
- Known handler types only.

## workflow.toml

| Field | Required | Description |
|---|---|---|
| `_version` | No (defaults 1) | Schema version; must be `1` |
| `[workflow].graph` | No | Path to the `.fabro`, relative to the TOML. Defaults to `workflow.fabro`. |
| `[run].goal` | No | What the run should accomplish |

Goal precedence: CLI `--goal`/`--goal-file` > `[run].goal` > graph `goal` attribute.

Sections: `[run.model]` (`name`, `[run.model.controls]`, `[run.model.fallbacks]`),
`[[run.prepare.steps]]`, `[run.clone]` (`depth = 0` for full history),
`[run.run_branch]`, `[run.meta_branch]`, `[run.environment]` + `[environments.<slug>]`
(`provider`, `[.image].dockerfile`, `[.resources]`, `[.env]`),
`[run.integrations.github.permissions]`, `[run.notifications.<name>]`,
`[run.checkpoint]` (`exclude_globs`), `[run.inputs]`, `[run.artifacts]` (`include` globs),
`[run.agent]`, `[run.agent.mcps.<name>]`, `[run.pull_request]`, `[[run.hooks]]`.

```toml
_version = 1

[workflow]
graph = "code-review.fabro"

[run.inputs]
mode = "changes"
effort = "medium"

[run.clone]
depth = 0                  # full history

[run.run_branch]
enabled = false            # read-only run: never create a branch
[run.pull_request]
enabled = false

[run.model.fallbacks]
"kimi-k3" = ["moonshot:kimi-k3", "modal:kimi-k3", "claude-opus-5"]

[run.environment]
id = "code-review"

[run.integrations.github.permissions]
pull_requests = "write"    # mints a scoped GITHUB_TOKEN into the sandbox

[run.artifacts]
include = ["CODE-REVIEW-*/CODE-REVIEW-RESULTS.md"]

[environments.code-review]
provider = "daytona"
[environments.code-review.resources]
cpu = 2
memory = "4GB"
```

Set `[run.run_branch].enabled = false` and `[run.pull_request].enabled = false` on read-only
workflows so a host project's `.fabro/project.toml` defaults cannot turn the run into a
branch or PR.

## CLI

Authoring: `fabro validate <file.fabro>`, `fabro preflight <workflow.toml>`,
`fabro graph <workflow> [-o out.svg] [-d lr|tb] [--allow-invalid]`,
`fabro workflow list`, `fabro workflow create <name> [-g goal]`.

Running: `fabro run <workflow>` with `--dry-run`, `-d/--detach`, `--auto-approve`,
`--preserve-sandbox`, `-I key=value`, `--goal`, `--model`, `--environment`,
`--target owner/repo[@branch]`, `--label k=v`.
`fabro create` stops at the submitted state; `fabro start <run>` then launches it.

Inspecting: `fabro inspect`, `fabro events [-p|-f|--since|-n]`, `fabro logs [-n]`,
`fabro attach`, `fabro ask`, `fabro wait`, `fabro dump -o <dir>`, `fabro artifact list/cp`,
`fabro sandbox ssh|cp|preview`.

Intervening: `fabro steer <run> "text" [--interrupt]`, `fabro approve`, `fabro deny`,
`fabro resume`, `fabro rewind`, `fabro fork`, `fabro rm`, `fabro archive`.

`<run>` accepts a run ID prefix or a workflow name (its most recent run).

Hidden commands (real, but `hide = true` so they are absent from `--help` and the generated
CLI docs):

- `fabro parse <file.fabro>` — parse a DOT file and print its AST. The fastest way to see how
  Fabro actually interpreted a node's shape/type inference or an attribute you're unsure about.
- `fabro ps` — list workflow runs.
- `fabro exec` — run a one-off agentic coding session (no workflow). `--verbose` prints tool
  calls and the transcript; `--permissions read-only|read-write|full`.

