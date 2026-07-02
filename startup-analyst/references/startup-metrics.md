# Startup Metrics

Use this reference to define, calculate, benchmark, and diagnose metrics. Start from the business model and current company stage.

## Build a metric dictionary

For every metric, specify the formula, unit, population, period, data source, treatment of edge cases, and owner. Do not compare metrics until definitions and cohorts match.

## Common formulas

### SaaS and subscription

- `MRR = sum of normalized monthly recurring subscription revenue`
- `logo retention = retained opening customers / opening customers`
- `gross revenue retention = (opening MRR - churn - contraction) / opening MRR`
- `net revenue retention = (opening MRR - churn - contraction + expansion) / opening MRR`
- `CAC payback months = CAC / monthly gross profit from a new customer`

Exclude one-time services from MRR and state how reactivations, pauses, and annual contracts are treated.

### Marketplace

- `GMV = value of transactions completed through the marketplace`
- `take rate = marketplace revenue / GMV`
- `liquidity = successful matches or transactions / qualified attempts`
- Track buyer and supplier retention separately.

### Consumer or usage-led product

- Cohort retention at meaningful intervals
- Activation rate against a product-specific value event
- Engagement frequency and depth
- Paid conversion, contribution margin, and acquisition payback when monetized

## Diagnose before benchmarking

1. Validate data and metric definitions.
2. Segment by acquisition channel, customer type, geography, plan, or cohort.
3. Locate the funnel or cohort transition causing the aggregate result.
4. Compare against the company's history and plan before external benchmarks.
5. Use external benchmarks only when business model, stage, segment, geography, metric definition, and vintage are comparable.
6. Recommend a target, owner, review cadence, and experiment tied to the diagnosed driver.

## Stage emphasis

- **Pre-seed:** activation, retention evidence, learning velocity, and burn.
- **Seed:** repeatability by cohort or channel, unit-economic direction, and runway.
- **Series A:** durable retention, scalable acquisition, growth efficiency, forecast reliability, and operating leverage.

Report the metric value, exact definition, trend, segments, comparison basis, diagnosis, confidence, and next action. A benchmark without a causal diagnosis is not a recommendation.
