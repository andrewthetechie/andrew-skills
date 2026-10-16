# Review cases

Use these cases when changing the skill. They test recommendation quality, including justified decisions to retain custom code.

Run each case in a fresh context with `SKILL.md` and only the case's input.
Keep the expectations separate from the reviewing agent. Allow source lookup, but keep repository and external state unchanged.
Compare the actual findings with the expectations afterward. Equivalent solutions pass when their semantics and tradeoffs fit the input.
Record missed replacements, unsupported findings, incompatible edits, and verification gaps. Wording and finding counts alone do not establish quality.

## Proposal with several mechanisms

### Input

Review this batch executor proposal for useful replacements of custom machinery.

The worker uses Python 3.11 and PostgreSQL 15. Two worker processes share one database. Preserve existing dependencies and deployment.
The authenticated HTTP interface, JSON envelope, metrics, and deployment remain unchanged and outside this review.

`plan_batch` accepts an immutable directed graph with up to 10,000 jobs and 60,000 dependency edges.
All dependency IDs must name jobs in the batch. Any topological order is valid. Execution is sequential within each claimed batch.
Validate the whole graph before any job starts, including disconnected cycles.
The proposed function repeatedly scans remaining jobs and emits those whose dependencies are already complete.
A pass without progress raises `InvalidGraph`. Build the full result before execution starts.

Submission retries use a key unique within each tenant. Concurrent requests must receive the same job ID.
The handler checks for `(tenant_id, request_key)` inside a transaction, then inserts a job when no row exists.
A Python mutex guards this sequence within each process. Only the generated `job_id` primary key has a uniqueness constraint.
The tenant and request key columns are non-null. Existing records contain no duplicate pairs.
On an existing key, return the original job ID. The payload stays immutable after insertion.
Workers discover jobs through database queries after commit. No work starts before commit.

A fixed three-entry dictionary maps domain job types to existing handlers.
There are no plug-ins, runtime registration, or configurable transitions.
An optional diagnostic export uses a private, versioned JSON array of job IDs.
Only the worker's diagnostic command consumes it, through the standard library.

### Expectations

- Identify an established topological ordering implementation compatible with Python 3.11 and the graph contract.
  Preserve dependency orientation, missing-ID validation, whole-graph cycle rejection, and validation before execution.
  Explain which scan logic disappears. A named algorithm without an implementation edit is incomplete.
- Replace the process-local duplicate guard with database enforcement of the tenant/key pair.
  Explain atomic conflict handling and how concurrent requests return the original ID without changing its payload.
  Account for the existing-data migration. A uniqueness constraint alone does not complete the handler's behavior.
- Retain the dispatch mapping and private diagnostic format unless a concrete benefit justifies replacing them.
  Unrelated protocol, observability, and compliance recommendations fail the scope check.

## Code change with an external format

### Input

Review this Python 3.11 change for standard replacements. The caller opens the output with UTF-8 encoding and `newline=""`.
The new consumer uses CSV records with comma separators, double-quote escaping, and CRLF record endings.
Each field is already a string and can contain commas, quotes, CR, LF, Unicode, or empty content.
Rows arrive through a generator. Preserve row order and field values without materializing the whole export.
This new function replaces a placeholder. No existing consumer depends on its output.

```diff
--- a/export.py
+++ b/export.py
@@ -1,2 +1,9 @@
-def write_rows(rows, output):
-    raise NotImplementedError
+def escape_field(value):
+    if "," in value:
+        return '"' + value.replace('"', '""') + '"'
+    return value
+
+
+def write_rows(rows, output):
+    for row in rows:
+        output.write(",".join(escape_field(value) for value in row) + "\r\n")
```

### Expectations

- Replace the escaping helper and record assembly with the standard library's CSV writer.
  Specify a dialect that preserves the stated delimiters, quotes, and record endings.
- Explain a concrete failure involving quotes or line breaks without a comma.
  Cite the library contract and relevant format rules as distinct sources when both support the finding.
- Preserve streaming and the caller's newline handling.
  Validate with a CSV reader round trip over the edge cases, plus a record-ending check.
- Keep the edit local. A new framework, service, or whole export redesign needs evidence absent from this input.

## Bounded domain code

### Input

Review a C11 change that adds a fourth fixed fixture mode to a command-line program.
The program runs on an offline microcontroller test station.
The existing switch maps each mode enum to a device-specific setup function, calls it, and returns its result.
There is no transition history, asynchronous execution, or runtime registration.
The four routines cannot share their device-specific behavior. The caller validates enum values.

The program also reads a fixed 12-byte firmware record. The existing decoder checks length and reads explicit little-endian fields.
Deployed firmware controls the wire layout. This task cannot change it, and the patch leaves the decoder intact.
The project prohibits dynamic allocation and new runtime dependencies. The request is a review, not a patch.

### Expectations

Return no replacement findings, with a short explanation of the bounded domain mapping and fixed firmware contract.
A state-machine framework or replacement wire format fails the fit check.

## Missing constraint

### Input

Review a proposal to replace an ordered scan of pending jobs with a standard priority queue.
The scheduler repeatedly chooses the smallest deadline and requires FIFO behavior for equal deadlines.
Pending jobs can receive deadline updates, but the proposal does not say whether these updates must be immediate.
There are up to 100,000 pending jobs. The design must keep memory bounded.
The proposal specifies neither the implementation language nor the available libraries.

### Expectations

Separate a conditional recommendation from supported findings.
Name a concrete priority-queue variant or update strategy and the fact needed to choose it.
Preserve FIFO ties. Account for updated priorities and memory growth if entries become stale.
An unconditional basic-heap replacement or a language-specific API presented as available fails the fit check.

