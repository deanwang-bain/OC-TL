# Where to find the figures, and the traps

## Source order

Use the most primary source you can reach, and the same kind of source for every company.

1. **The annual filing**: 10-K (US), 20-F (foreign filers on EDGAR), or the annual report / universal registration document. The consolidated income statement and balance sheet are authoritative.
2. **The company's own results release or investor presentation**, for the latest year when the annual filing is not out yet, or for segment detail.
3. **Earnings call transcripts** (company IR sites often post them), the CEO letter, investor days and capital markets days: for signals, not for figures.
4. **Public news** (business press, trade press): for analyst views and industry context, reported as such.

Data aggregators (finance portals, screeners that standardise statements) are a fallback for finding a number fast, never the citation. A site that reproduces a filing's own text (a filing viewer, a newswire copy of a release) is different: cite the filing, and mark the source `checked: false` if you only saw the reproduction. They mix definitions — total revenues with financial services income, cost of sales with depreciation — so confirm each figure against the filing and cite the filing.

With web search and fetch, search for "<company> 10-K <year>" or "<company> annual report <year> pdf", open the filing, and read the income statement. EDGAR filing index pages and the `Financial_Report.xlsx` link beside a 10-K hold the statements as tables. Where the SEC XBRL API (`data.sec.gov/api/xbrl/companyfacts/CIK##########.json`) is reachable, it returns every reported value with its filing; check the concept and period before using one.

## Definition traps

Check these for every company before recording it. A trap that applies goes in `basis_note`, `na_reason`, `exclusions` or `narrative.limitations`.

| Trap | What to do |
| --- | --- |
| **Financial services inside the group** (captive finance, insurance, banking arms) | Use the industrial or equipment-operations figures when the company reports them separately, and say so in `basis_note`. Mixing consolidated revenue with industrial cost of sales gives a nonsense margin |
| **Costs by nature, not function** (common under IFRS: raw materials, staff costs, depreciation) | No cost of sales and no SG&A: record `null` with that reason. Do not rebuild them yourself |
| **SG&A split** into selling, marketing and admin | Add them into one `sga` figure and note it in the source `locator`. Benchmark the combined line |
| **R&D inside cost of sales or SG&A** | Record `rnd` as reported in a note if disclosed; do not take it out of the other lines |
| **Adjusted vs reported operating income** | Default to reported operating income. When impairments or one-offs distort the latest year for any company, use adjusted operating income for every company, each with its reconciliation as a source, and set `meta.ebit_basis` to `adjusted`. Note where definitions differ (one peer also excluding amortisation) |
| **Acquisitions and disposals in the growth window** | Reported CAGR then measures deals, not the business. Prefer each company's published organic growth (`organic_growth`); otherwise say which peers are distorted in `basis_note`, and consider excluding them from the growth benchmark |
| **Restatements and discontinued operations** | Use the latest filing's comparatives for earlier years |
| **Different fiscal year ends** | Keep each company's own latest year; the poster labels it. Do not shift years to line them up |
| **A peer that is a segment of a larger group** | Use segment revenue and operating profit if reported; the rest is n/a. Say so in `basis_note` |
| **Receivables including financing receivables** | Use trade receivables only. If not separable, exclude the company from DSO with the reason |
| **Only gross profit, or only a margin, is published** | Record `gross_profit` (the script derives cost of sales) or `reported_ratios`. Do not back amounts out of a margin yourself |
| **Units in thousands** | Record as reported and set `scale: 0.001` on the company |
| **Very recent listing, spin-off or merger** | Shorter growth history is allowed; the warning says so. Pro forma figures only if the company publishes them, labelled |
| **Currency** | Record in the reporting currency and set `fx_to_case`. For income-statement amounts use the year's average rate; cite it (central bank reference rates, e.g. the ECB's). A cross rate via the euro is fine: note both legs in the source `locator`. Without a cited rate, leave `fx_to_case` out: ratios are unaffected and only the peer's revenue shows unconverted |
| **Hyperinflation accounting (IAS 29)** (Turkey, Argentina and others) | Restated figures are in year-end purchasing power and converted at the closing rate; growth is not comparable. Leave such a peer out of growth, or out entirely, and say why |
| **Different units within one company** (P&L in millions, balance sheet in thousands) | Give the odd value its own `"scale"` |
| **Bills receivable and payable** (common for Chinese filers) | Note whether receivables and payables include notes and bills; exclude the company from DSO or DPO if they cannot be separated |
| **LIFO inventory** (some US industrials and retailers) | Flatters inventory days against FIFO peers; note it, and exclude from DIO if the LIFO reserve is large |

## Industry rules

| Industry | What changes |
| --- | --- |
| **Industrials with captive finance** (equipment makers) | Use the equipment or industrial operations figures; dealer and customer receivables sit with the finance arm, so exclude affected companies from DSO. Growth over three years mostly measures the cycle: consider `size_growth: false` |
| **Software and internet** | `not_applicable` for DIO and usually DPO (payables are opex and capex creditors). Stay on reported operating income: adjusted figures remove stock-based pay that the cost lines still include. Deferred revenue is the big working-capital balance and is not modelled; name it under limitations. R&D stays context, not sized |
| **Retail** | Formats trade gross margin against SG&A (clubs run low on both; occupancy sits in cost of sales for some, SG&A for others; D&A is a separate line for some). Exclude formats that differ from the gross-margin and SG&A benchmarks, or set `cost_lever: "ebit_margin"`. Keep membership fees in revenue for everyone. Note 53-week years in the growth window. Many retailers have no receivables line: DSO and CCC will be thin |
| **Consumer goods** | Prefer organic growth; reported growth is full of acquisitions and disposals. Commodity hedging can move cost of sales in one year: note it |
| **IFRS reporters by nature** (many European and Asian companies) | No cost of sales or SG&A: those benchmarks thin out. If fewer than four peers remain, use `cost_lever: "ebit_margin"` |
| **Banks, insurers, asset managers, REITs** | Out of scope for this method |

## Signals

What makes a good signal:

- **Management priorities and targets**: "we are targeting a 30% cut in production cost", "procurement is the largest lever", "inventory is a 2025 priority". These are what the framings should connect to.
- **Investments and portfolio moves**: plants, acquisitions, disposals, restructuring programmes with their stated savings.
- **Problems management admits**: a system changeover, a recall, lost share, a weak region.
- **Outside view**: an analyst's view or rating change reported in public news, an industry trend from trade press.

Rules:

- Quote verbatim, at most two sentences, and check the words against the source page. When only a summary is available, record it with `"verbatim": false`.
- When pages cannot be opened and you only see search-result extracts, mark a quote verbatim only if the same words appear in the company's own release or transcript extract, or identically in several outlets; everything else is a summary. Set `"checked": false` on those sources.
- Give speaker, role and date. A quote from two years ago is context, not a current priority.
- Never put a number from a signal on a chart or into a sizing. It can appear inside its quote.
- Do not quote paywalled analyst research. Cite the public article that reports it.
- Credentials, personal data or anything a page marks confidential stay out of the case file, even when a search turns them up.
