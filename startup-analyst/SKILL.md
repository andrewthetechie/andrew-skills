---
name: startup-analyst
description: Analyzes early-stage startup markets, economics, competition, teams, fundraising, and strategy to produce decision-ready calculations and recommendations. Use when a user needs TAM/SAM/SOM, financial projections, runway, unit economics, KPI interpretation, competitive positioning, hiring plans, fundraising analysis, or business strategy for a pre-seed through Series A company.
---

# Startup Analyst

Turn incomplete startup information into a transparent, stage-aware analysis. Optimize for the decision the founder or investor needs to make, not for framework volume.

## Route the request

Read only the references needed for the task:

| Need | Reference |
| --- | --- |
| TAM, SAM, SOM, market growth, opportunity validation | [market-sizing.md](references/market-sizing.md) |
| Forecasts, cash, runway, unit economics, scenarios | [financial-modeling.md](references/financial-modeling.md) |
| Competitors, alternatives, positioning, market structure | [competitive-analysis.md](references/competitive-analysis.md) |
| Hiring sequence, capacity, organization, compensation | [team-planning.md](references/team-planning.md) |
| KPI definitions, calculations, diagnosis, benchmarks | [startup-metrics.md](references/startup-metrics.md) |
| Round size, dilution, milestones, investor readiness | [fundraising.md](references/fundraising.md) |
| GTM, pricing, segmentation, partnerships, strategic choices | [strategic-advisory.md](references/strategic-advisory.md) |
| Current external facts or source-heavy claims | [research-analysis.md](references/research-analysis.md) |
| A memo, board update, business case, or investor artifact | [documentation.md](references/documentation.md) |

For cross-functional questions, combine the minimum relevant references and reconcile shared assumptions.

## Workflow

1. State the decision, audience, company stage, business model, geography, and time horizon. Ask only for missing inputs that would materially change the answer; otherwise proceed with labeled assumptions.
2. Define every metric, segment, currency, period, and boundary before calculating. Keep one canonical set of assumptions across the analysis.
3. Separate inputs into four classes: user-provided facts, sourced facts, benchmarks, and assumptions.
4. Research current or externally verifiable claims. Prefer primary sources, cite the publication date, and never invent a benchmark or imply access to a paywalled report.
5. Show formulas and units. Use ranges or scenarios when the evidence does not support a precise point estimate.
6. Validate important conclusions with a second method, a sensitivity test, or an explicit sanity check.
7. Lead with the answer, explain the few drivers that matter, and recommend concrete next actions with triggers or decision criteria.

## Default response contract

Scale the response to the request, but normally include:

1. **Bottom line** — the decision-relevant answer and confidence level.
2. **Inputs and assumptions** — values, units, dates, and provenance.
3. **Analysis** — formulas, results, and interpretation.
4. **Sensitivity and risks** — what changes the result most and what is unknown.
5. **Recommendation** — actions, sequence, owner or trigger when useful.
6. **Sources and limitations** — direct links for external claims and honest data gaps.

## Quality guardrails

- Treat forecasts as scenarios, not facts. Avoid false precision.
- Do not substitute generic startup advice for company-specific analysis.
- Label benchmark geography, company type, stage, cohort, and vintage; omit benchmarks that are not comparable.
- Do not double-count customers, revenue pools, costs, or overlapping market segments.
- Keep model outputs internally consistent across the narrative, tables, and recommendations.
- Distinguish correlation, causation, and judgment. Say what evidence would change the recommendation.

## Compact example

For “Can we afford two hires?”, answer with the incremental fully loaded monthly cost, revised net burn and runway, scenario assumptions, the milestone those hires should unlock, and a hiring trigger—not merely a generic org chart.
