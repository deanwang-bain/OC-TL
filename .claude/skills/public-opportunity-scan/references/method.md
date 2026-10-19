# Method: metrics, benchmarks and sizing

Everything here is implemented in `scripts/opscan_calc.py`. This file is for explaining a number to a partner, and for checking the script does what the poster says.

## Metrics (latest fiscal year unless noted)

| Key | Formula | Better when |
| --- | --- | --- |
| `revenue_cagr` | (revenue end ÷ revenue start)^(1 ÷ years) − 1, over up to `cagr_years` | higher |
| `gross_margin` | (revenue − cost of sales) ÷ revenue | higher |
| `sga_pct` | SG&A ÷ revenue | lower |
| `rnd_pct` | R&D ÷ revenue | context only, not rated |
| `ebit_margin` | operating income ÷ revenue | higher |
| `dso` | trade receivables ÷ revenue × 365 | lower |
| `dio` | inventory ÷ cost of sales × 365 | lower |
| `dpo` | trade payables ÷ cost of sales × 365 | higher |
| `ccc` | DSO + DIO − DPO | lower |
| `tsr` | as published, same window for all | higher |
| `organic_growth` | as published by each company, latest year | higher |
| `valuation` | as published or from market data, one definition and date | higher (shown, not sized) |

Balance-sheet items are year-end values, not averages, because averages need a second balance sheet per company and add little to a sniff test.

## Benchmarks

- Peer set: every `peer` with a value for the metric, less any `exclusions`. The target is never included.
- Median, and quartiles by linear interpolation (Excel `PERCENTILE.INC`). Top quartile is the 75th percentile for higher-is-better metrics, the 25th for lower-is-better.
- Fewer than `min_peers` (default 4) peers with a value makes the benchmark n/a, with the count as the reason.
- Rating: top quartile if at least as good as the top quartile, above median if at least as good as the median, below median if at least as good as the bottom quartile, else bottom quartile.
- Rank: the target's position among peers plus target, best first.

## Sizing

Low end closes the gap to the median, high end to the top quartile. Gaps are zero where the target is already better. All amounts on the target's latest year, multiplied by `capture` (1.0 by default, meaning full gap closure).

| Bucket | Opportunity | Shown as % |
| --- | --- | --- |
| Commercial | R × [(1 + g + Δ)^h − (1 + g)^h] × margin, where R is revenue, g the target's growth (revenue CAGR, or organic growth when `sizing.growth_metric` says so), Δ the gap to the benchmark, h the horizon, margin the target's EBIT margin unless set | incremental revenue ÷ revenue the target would reach on its own trend, and the year |
| Operations | gross-margin gap × R | ÷ cost of sales, and bps of margin |
| SG&A | SG&A-% gap × R | ÷ SG&A, and bps of margin |
| R&D (opt-in) | (target R&D % − peer median or lower quartile) × R | ÷ R&D, and bps |
| Cost and margin (with `cost_lever: "ebit_margin"`, instead of Operations and SG&A) | EBIT-margin gap × R | ÷ operating costs (revenue less EBIT), and bps of margin |
| Working capital | DSO gap × R ÷ 365 + DIO gap × cost of sales ÷ 365 + DPO gap × cost of sales ÷ 365 | days |

- With a published `practitioner_ranges` leg, each end of the opportunity is the larger of the peer leg and the published leg (as OpCat does with Bain experience). Without one, the opportunity is the peer leg.
- Bucket states: `sized`; `no_gap` (already at or better than the top quartile, shown as a finding); `na` (data or benchmark missing, with the reason).
- Totals: recurring EBIT is the sum of the sized P&L buckets; cash is the working-capital bucket. They are never added.
- Bridge: latest EBIT, plus each P&L bucket, to EBIT potential. Margin with the gaps closed divides by revenue plus the commercial bucket's incremental revenue.

## Known simplifications

- With an adjusted EBIT basis, the cost-line gaps (gross margin, SG&A) are still on reported figures. Where the adjustments are mostly one-offs this is close enough; where they remove a recurring cost such as stock-based pay, the bridge would mix bases, which is why software stays on reported operating income.

Say these when asked; the method panel prints the main ones.

- Bucket sizes overlap: closing a gross-margin gap and an SG&A gap together assumes the company can do both, and growth at a higher margin is not compounded.
- The commercial bucket uses the target's EBIT margin on incremental revenue, not a contribution margin, which understates it for high fixed-cost businesses.
- A full-gap-closure range is a ceiling for a sniff test, not a plan. Real programmes capture part of it over several years; set `capture` below 1 when the user wants a planning view.
- Year-end balances can be seasonal. Note it when a company's year end falls at a seasonal peak.
