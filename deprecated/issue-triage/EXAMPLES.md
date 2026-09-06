# Actionability Examples

Use these examples to calibrate whether missing detail is a true blocker or an ordinary implementation decision.

## Workable bug: authenticated route shows framework fallback

The issue says that visiting an unmatched `/app/*` route while signed in displays React Router's raw 404 error boundary instead of the application's chrome and a friendly not-found page. It provides a concrete URL and reproduction steps, identifies that the router has neither an `errorElement` nor an authenticated catch-all route, and expects a branded 404 inside the normal shell where applicable.

### Triage

**Classification:** bug (high confidence)

**Readiness:** ready, assuming repository inspection supports the stated route configuration

**Why it is actionable:**

- The affected user and context are known: a signed-in user navigating below `/app/`.
- Actual behavior is observable and reproducible.
- Expected behavior and its boundary are clear: unmatched authenticated routes retain the appropriate app chrome and never expose the framework fallback.
- The issue identifies a plausible code path and cause.
- Completion can be covered by a routing test for an unmatched path.

**Open questions:** None — this issue is workable as written.

Do not ask whether to use `errorElement` or a `*` route. That is an implementation choice because either may satisfy the stated outcome. Exact copy and styling are also discoverable implementation details when the repository has established not-found patterns or a design system. Ask only if the product has no relevant convention and the choice would prevent a verifiable result.

Possible acceptance criteria:

- An unmatched authenticated `/app/*` URL renders a branded not-found state.
- The normal authenticated shell remains present where the routing hierarchy supports it.
- React Router's default developer-facing fallback is not shown.
- A routing test covers at least one unmatched authenticated URL.

## Under-specified enhancement: operator services and pricing

The issue asks operators to add services such as mowing, edging, and blow-off, assign prices to individual services or packages, and add restrictions such as acreage limits or exclusions for heavy overgrowth.

### Triage

**Classification:** enhancement (high confidence)

**Readiness:** needs-info

**What is established:**

- Operators need to describe services they offer.
- A service may have basic pricing.
- The concept includes both individual services and service packages.
- Services may carry restrictions or eligibility conditions.

**Questions that must be answered, compiled as one batch after checking the repository:**

1. **Where does this catalog participate in the product workflow?** Is the first version only operator-side setup, or must services and packages also appear in estimates, bookings, invoices, or customer-facing views? This determines the integration boundary. Recommended default: scope the first version to setup plus the earliest existing downstream selection flow.
2. **Who defines service types?** Are they free-form per operator, selected from a system catalog, or a system catalog with operator-defined additions? This changes identity, deduplication, and future reporting. The wording suggests operator-defined services unless existing domain models establish a catalog.
3. **Which pricing rules are required initially?** Clarify whether each service has one fixed price, whether a package has its own fixed total, and whether a service can be sold both individually and in multiple packages. These choices determine the core data model and validation.
4. **What exactly is a package?** Clarify whether it is only a named set of services with a package price or whether it also needs quantities, optional items, nested packages, or per-item overrides. Recommended default: a flat set of existing services with one package price and no nesting. **If optional items or overrides are required:** specify who selects them and whether they change the displayed package price.
5. **Are restrictions descriptive or enforced?** Should “up to 1/2 acre” and “no heavy overgrowth” be operator-entered text shown to users, structured eligibility rules that block selection, inputs that change price, or some combination? This is the largest behavioral and implementation boundary. Recommended default: descriptive text unless the current quoting flow already has the necessary structured property data. **If restrictions are enforced:** identify the source of acreage or condition data, when eligibility is evaluated, and whether failure blocks selection or requests a custom quote. **If restrictions are descriptive:** identify where the text must be visible before selection.
6. **What are the visibility and lifecycle rules?** Identify who can view the catalog, whether operators can edit/archive/delete entries, and what happens when an in-use service changes. These rules affect permissions and historical estimates or bookings. Recommended default: operator-managed, customer-visible where selectable, and archivable rather than destructively deletable once referenced.

Do not ask which database tables, API routes, form components, or file paths to use. Those are implementer-owned decisions after the product questions above are answered.

### Future autonomous run after answers are posted

Do not wait for these answers during the current run. A later run should update the established facts from human replies, remove answered questions, inspect the repository for any newly implied constraints, and emit a new complete Markdown artifact. Do not re-ask resolved questions. Once no blocking questions remain, produce acceptance criteria and state explicitly that the issue is workable.
