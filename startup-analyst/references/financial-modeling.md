# Financial Modeling

Use this reference for forecasts, revenue mechanics, costs, cash, runway, unit economics, hiring affordability, and scenarios.

## Set the model frame

State the as-of date, currency, accounting basis, forecast granularity, horizon, and opening cash. Prefer monthly models for cash management. Separate actuals from forecasts and recurring from one-time items.

## Model in dependency order

1. **Operating drivers:** leads or capacity, conversion, customers, usage, pricing, churn, and expansion.
2. **Revenue:** derive from cohorts or units; do not apply an unsupported growth percentage directly to revenue when operating drivers are available.
3. **Cost of revenue:** hosting, payment fees, delivery labor, support, or other costs that scale with delivery.
4. **Operating expenses:** headcount by start date and fully loaded cost, vendors, facilities, marketing, legal, and one-time costs.
5. **Cash:** opening cash + cash inflows - cash outflows. Reflect collection timing, annual prepayments, working capital, debt, and financing separately when material.
6. **Scenarios:** conservative, base, and upside cases driven by coherent assumption sets.

## Core formulas

- `ARR = recurring MRR × 12`
- `gross margin = (revenue - cost of revenue) / revenue`
- `net burn = cash operating outflows - cash operating inflows`
- `runway months = available cash / average forward monthly net burn`
- `CAC = attributable acquisition spend / new customers acquired`
- `gross-margin LTV (simple) = ARPA × gross margin / logo churn rate`
- `CAC payback months = CAC / monthly gross profit per new customer`
- `burn multiple = net cash burn / net new ARR` over the same period

State cohort, period, and attribution rules. Do not use the simple LTV formula where churn is unstable, negative, or not meaningful; use cohort contribution margin instead.

## Validation checks

- Beginning cash plus cash movement equals ending cash.
- Customer cohorts reconcile to ending customers and revenue.
- Headcount plan reconciles to payroll and hiring dates.
- Annual and monthly recurring revenue use consistent definitions.
- Margins and working-capital behavior are plausible for the business model.
- Scenario assumptions change together where drivers are causally related.

## Report

Lead with the decision result. Include the assumption table, key monthly or quarterly outputs, cash-out date, runway, unit economics, scenario comparison, sensitivity drivers, and model limitations. For affordability questions, show the incremental case against the no-action baseline.
