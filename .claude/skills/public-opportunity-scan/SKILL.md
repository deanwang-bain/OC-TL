---
name: public-opportunity-scan
description: Build an outside-in opportunity scan of a listed company from public information only (annual reports, 10-K/20-F filings, results releases, earnings calls, investor days, public news), benchmark it against a peer set, size where the value sits (EBIT and working capital, with $ and %), tie it to what management says it is prioritising, and deliver one A1 poster as a print-ready HTML file. Use it whenever someone wants a case for change, size of prize, peer benchmarking, value-creation sniff test, "where is the value" view, partner or CEO conversation prep, pre-proposal outside-in, or an Opportunity Catalyst / OpCat style analysis on a public company, even if they never say "poster" or "skill", and even when they only name the company and a peer or two.
---

# Public opportunity scan

This is the Opportunity Catalyst journey — target, peers, case for change, size of prize, output — rebuilt so it runs on **public information only** and ends in **one A1 poster** (841 × 594 mm landscape, HTML, prints to a single sheet). It is deliberately not interactive: the partner reads the answer, and the case file behind it lets anyone rerun it with different peers or assumptions.

It produces a sniff test of where value may sit and why management would recognise it, not a commitment. Say so on the poster and in your reply.

## What carries over from OpCat, and why

These rules are what make the output defensible in front of a client. Keep them even when shortcuts look harmless.

- **You gather; the script computes.** You collect reported figures with their sources into a case file. `scripts/build_poster.py` does every ratio, median, quartile, gap, sizing and total. Language models are unreliable at multi-step arithmetic, and a single wrong margin undermines the whole poster. Narrative text cites computed numbers with `{{tokens}}` (for example `{{median.ebit_margin}}`), so the text and the charts can never disagree.
- **Every number traces to a public source.** Each figure carries a source id; the poster numbers the sources. A missing value is `null` with a reason, shown as n/a. Never estimate, interpolate or zero-fill a gap: a guessed number that a client spots ends the conversation.
- **Benchmarks are peer median and top quartile**, from peers that report the metric. The target is never in its own benchmark. Top quartile follows the metric's direction.
- **Totals are the sum of the rows shown.** EBIT (recurring P&L) and working-capital cash (one-off) are never added together.
- **EBIT, not EBITDA**, on one basis for every company.

## What partners asked for after testing OpCat

These came out of a partner walkthrough. The poster template already handles the layout; your job is the content.

- **Management's agenda sits beside the numbers.** A case for change that is only maths does not land. Lead the situation with what the company faces and what management says it is prioritising and investing in, with short verbatim quotes, and make each framing combine a computed gap with a stated priority.
- **Show the evidence before the ask**: performance against peers comes before the size of prize. Charts are sorted best to worst.
- **Dollars and percentages together**: baseline in $, opportunity in $, and the same opportunity as % of the cost line and bps of margin (or % more revenue, with the year it is reached).
- **Lead the size of prize with the EBIT bridge**, then the table.
- **Be clear about currency and the as-of date** in the header.
- **SG&A benchmarked as one combined line**, because peers split selling, marketing and admin differently.

## What it cannot do, compared with OpCat

State these limits on the poster (the method panel covers most of them):

| OpCat has | This skill instead |
| --- | --- |
| Bain experience ranges, case studies, IRIS | Peer benchmark only. A published external range can be added as a second leg only when it has a public source (see `sizing.practitioner_ranges` in the schema) |
| CapIQ data and analyst adjustments | Figures as reported in filings. Reported operating income as EBIT unless a note says otherwise |
| Live recalculation and chat | Edit the case file and rebuild |
| Analyst reports | Only analyst views reported in public news, labelled as such |

## Workflow

**Not for banks, insurers, asset managers or REITs.** Their economics do not run through cost of sales, SG&A and working capital, so the metrics here would mislead. Say so and stop rather than force them through.

### 0. Plan the searches

A scan takes roughly 45–60 web searches, and the budget can be shared with other work in the session, so spend them in this order and stop adding peers before you starve the signals:

1. The target's latest annual income statement and balance sheet, and its prior years' revenue (4–6 searches).
2. **The target's management signals**: latest results call, annual report letter, investor day (6–10 searches). These shape the framings, so they come before the seventh peer.
3. Each peer's income statement, then balance sheet (4–6 searches each). Six well-documented peers beat nine thin ones.
4. Outside view, organic growth and valuation if the budget allows.

Search for a whole statement at once ("<company> 10-K FY2025 consolidated statements of operations net sales cost of sales selling general administrative operating income"), not one line at a time. When the annual figures will not surface, the next quarter's interim report often carries the full-year column. Keep your own numbers out of queries: search extracts sometimes echo them back as if confirmed.

### 1. Scope (ask nothing unless the company is ambiguous)

Defaults: audience is the CEO and executive committee; question is "Where is the value, and what would management recognise as its own agenda?"; currency is the target's reporting currency, in millions; latest four fiscal years for revenue, latest year for everything else; growth over three years; sizing horizon three years. Use what the user gives you instead. Only ask when the target itself is unclear (two listed entities with the same name, a parent and a subsidiary).

### 2. Peer set (6–9 peers)

Pick listed companies with comparable business model, end markets and scale; state a one-line reason per peer. Prefer peers that report on a functional basis (cost of sales, SG&A), or the cost benchmarks will be thin. Flag, rather than silently drop, a peer whose business model differs (financial services arm, franchise-heavy, a segment of a conglomerate). Fewer than four peers reporting a metric makes its benchmark n/a, so aim for at least six.

### 3. Collect financials into the case file

Read `references/case-schema.md` for the file format and `references/sources.md` for where to look and the definition traps. Work company by company: find the latest annual filing, take the income statement and the receivables, inventory and payables lines, and the prior years' revenue. Use the latest filing's comparatives for prior years, because they include restatements.

Record each value as `{"value": 1234, "src": "s3"}` in millions of the company's reporting currency; record a gap as `{"value": null, "na_reason": "costs reported by nature; no cost of sales"}`. Add each document to `sources` once, with title, publisher, date, URL and the statement or page.

Keep the target's own figures exactly as reported. Peers in another currency need `fx_to_case` with an FX source; ratios do not change, only the revenue shown in the peer table. A company reporting in thousands gets `"scale": 0.001`. Where a filing shows gross profit rather than cost of sales, record `gross_profit` and the script derives cost of sales; where only a published margin is available (no amounts), record it under `reported_ratios`.

**Pick the EBIT basis before collecting.** If any company has large impairments, restructuring or other one-offs in the latest year, reported operating income will mislead (a target with a reported loss makes the growth bucket meaningless). Then use each company's own adjusted operating income where it publishes one: `meta.ebit_basis` is `"adjusted"` when every company does, `"mixed"` when some publish none and keep their reported figure. Give each company its `ebit_basis` text ("adjusted operating income", "reported: no adjusted measure published"); it prints in the peer table.

One exception: in sectors where adjusted figures mainly remove stock-based compensation (software, internet), stay on reported operating income for everyone. The cost lines you benchmark include stock-based pay, so an adjusted EBIT base would not reconcile with them. `references/sources.md` has an industry table with the other sector rules (captive finance, retail formats, cyclicals, IFRS by nature, hyperinflation).

**Build lines from reported parts, not by hand.** When a line is the sum of reported figures (selling plus admin, three segments' operating profit, several cost lines), record it as `{"parts": [...]}` and the script adds them. When there is no operating-income line, record `pretax_income` and `net_interest_expense` and the script derives EBIT. A peer without a cited FX rate can stay in: leave `fx_to_case` out and only its revenue column is shown unconverted.

**Mark what you could not read.** When a page could not be opened and a figure or quote comes from a search-result extract, set `"checked": false` on that source. The poster then says how many sources need verifying, in the header and under Limitations. Never present search-extract figures as read from the document.

**Optional, when public and comparable across the set** (they make the poster much stronger, so look for them):
- `organic_growth` per company, as each company reports it. Reported CAGR is distorted by acquisitions and disposals; when organic figures exist for most of the set, set `sizing.growth_metric` to `"organic_growth"`.
- `valuation` per company: a multiple such as forward P/E or EV/EBIT, all on the same definition and date, with its market-data source, and `meta.valuation_label`. This adds a "what the market pays for growth" scatter, which is often the clearest way into a CEO conversation. It is shown, never sized.
- `narrative.segments`: the target's reported segments with revenue, growth and margin, each with its source.

### 4. Collect signals

(Collect the target's signals early, per step 0.) Search the latest annual report letter, the last two earnings calls, any investor day and recent public news for what management says about priorities, targets, investments and problems — forward-looking statements first, explanations of past results second. Record 6–12 signals. Quote verbatim, at most two sentences, with speaker, role, date and source; when you only have a search summary or a paraphrase, set `"verbatim": false` and it is labelled "summary". The quotes in a company's own results press release are the easiest to get verbatim, because newswires reproduce them word for word. Add analyst or industry views from public news as `kind: "analyst"` or `"industry"`. A signal used in several places prints in full once and as a pointer after that.

A signal is evidence, never a number on a chart. Numbers inside a quote stay in the quote.

### 5. First build, then read the results

Write the case file without the narrative and build once:

```bash
python scripts/build_poster.py case.json -o poster.html
```

This writes `analysis.json` beside the poster. Read `stats` (median, top quartile, rating and rank per metric) and `buckets` (state, opportunity, reason). Then write the narrative from what the numbers actually say — a company already in the top quartile on margin is never told it is "below peers", and a superlative must match its rank.

### 6. Write the narrative

The `narrative` block (schema in `references/case-schema.md`) fills the poster. Cite every computed number with a token; the build warns when it finds a typed number outside a quote, and fails on a token that does not exist. Keep to these budgets, or the poster will not fit one sheet:

- headline: one sentence that answers the question
- exec_summary: 3–4 assertions, each with its number
- situation: up to 4 bullets on what the company faces (segments, regions, market)
- priorities: up to 4, each with 1–2 signals
- framings: 3–4, ranked; each has a `lens` metric, 1–3 `metrics`, a story that joins the gap to a stated priority, 0–2 signals, and a client readiness level with its reason; mark one `lead`
- bucket_notes: why the value is real, per sized bucket, citing signals
- next_steps: up to 4 questions to test with management (printed under that heading); sharp hypotheses beat generic to-dos
- limitations: anything specific to this case (a peer on a different basis, a restated year)

Client readiness is your judgement, not a score: high when the framing restates management's own agenda with evidence, low when it contradicts what management has said publicly. Always give the reason.

### 7. Build, check, look

```bash
python scripts/build_poster.py case.json -o poster.html
python scripts/check_poster.py poster.html        # fit check and a PNG screenshot
```

The page scales its body to fill the sheet and flags any column that still overflows. Look at the screenshot: label collisions, a chart with one bar, an n/a list longer than the chart. If a column overflows, cut text in that column rather than shrinking type. If no headless browser is available, the check says so; open the HTML and look.

### 8. Deliver

Give the user `poster.html` (opens in any browser; print to PDF at A1, or A3/A4 scaled to fit), plus `case.json` and `analysis.json` for audit. In the reply: the headline, the two totals, the lead framing, and the limits that matter most for this company (for example "two peers report costs by nature, so the gross-margin benchmark rests on five peers").

## Sizing, in brief

`references/method.md` has the formulas. In short, each bucket closes the target's gap to the peer median (low end) and to the top quartile (high end), on the latest year:

- **Commercial**: grow at the benchmark growth rate (revenue CAGR, or organic growth when set) instead of the target's own for the horizon, times the target's EBIT margin.
- **Operations**: gross-margin gap × revenue.
- **SG&A**: SG&A-% gap × revenue.
- **R&D**: off by default, because lower R&D is not always better; turn on with `sizing.size_rnd` only when the user asks.
- **Working capital (cash, one-off)**: DSO, DIO and DPO day gaps × revenue or cost of sales ÷ 365.

A bucket where the target already beats the top quartile shows "no gap" rather than disappearing, because that is a finding too.

**When the cost lines are not comparable** (retail formats that trade gross margin against SG&A, peers reporting costs by nature, too few peers left after exclusions), set `sizing.cost_lever` to `"ebit_margin"`: one bucket sized on the EBIT-margin gap replaces the operations and SG&A buckets. Do this rather than leaving the biggest gap unsized. **In a cyclical industry** a three-year growth gap measures the cycle, not a lever; set `sizing.size_growth` to false with a `growth_note`, or use organic growth through a full cycle. **When a metric means nothing for the industry** (inventory days in software), list it in `meta.not_applicable` with the reason, and the chart is swapped for one that has data.

## Files

- `scripts/build_poster.py` — computes and renders; the one command to run
- `scripts/opscan_calc.py` — the calculations, metric definitions and token table
- `scripts/check_poster.py` — fit check and screenshot through headless Chromium
- `references/case-schema.md` — the case file, field by field, and the token list
- `references/sources.md` — where to find each figure and signal, and the definition traps
- `references/method.md` — metric definitions, benchmark and sizing formulas
- `assets/case.example.json` — a complete synthetic case to copy from

Colours sit in `TOKENS` at the top of `build_poster.py`; swap them for a house style without touching anything else.
