# The case file

One JSON file holds everything the poster shows. `assets/case.example.json` is a complete synthetic example; copy it and replace the contents.

## Top level

```json
{
  "meta": {...},
  "companies": [...],
  "financials": {...},
  "sources": [...],
  "signals": [...],
  "exclusions": [...],
  "sizing": {...},
  "narrative": {...}
}
```

## meta

| Field | Default | Meaning |
| --- | --- | --- |
| `as_of` | required | Date the data was gathered, `YYYY-MM-DD`. Printed in the header |
| `currency` | `USD` | Case currency, normally the target's reporting currency |
| `unit` | `millions` | All amounts are in millions |
| `audience` | none | For whom, e.g. "CEO and executive committee" |
| `question` | none | The question the poster answers |
| `prepared_by`, `prepared_on` | none | Footer |
| `cagr_years` | 3 | Revenue growth window |
| `min_peers` | 4 | Fewer peers reporting a metric makes its benchmark n/a |
| `charts` | ebit_margin, revenue_cagr, gross_margin, sga_pct, ccc, rnd_pct | Which six charts appear (any metric key below). TSR replaces the last one when provided |
| `fx_note` | none | Header chip, e.g. "Peer revenue at ECB rates of 30 Sep 2026" |

## companies

```json
{"id": "DE", "name": "Deere & Company", "short_name": "Deere", "role": "target",
 "ticker": "DE", "currency": "USD", "fiscal_year_end": "Oct",
 "basis_note": "Equipment operations; financial services excluded",
 "rationale": "One line on why this is a peer (peers only)",
 "fx_to_case": 1.0, "tsr": {"value": 0.42, "src": "s9"}, "tsr_window": "3y to 30 Sep 2026"}
```

- Exactly one company has `"role": "target"`; the rest are `"peer"`.
- `id` is short and used in tokens (`{{DE.ebit_margin}}`). Letters, digits, `_` and `-` only.
- `basis_note` prints under the name in the peer table: use it whenever a company's figures are on a different basis.
- `fx_to_case` multiplies the company's reported amounts into the case currency. Required when `currency` differs; cite the rate in `sources` and mention it in `meta.fx_note`.
- `tsr` is optional and taken as published (not computed); give every company the same window or leave it out.

## financials

```json
"financials": {
  "DE": {
    "FY2024": {
      "revenue":     {"value": 44759, "src": "s1"},
      "cogs":        {"value": 30775, "src": "s1"},
      "sga":         {"value": 4800,  "src": "s1"},
      "rnd":         {"value": 2290,  "src": "s1"},
      "ebit":        {"value": 9200,  "src": "s1"},
      "receivables": {"value": 5300,  "src": "s1"},
      "inventory":   {"value": 7100,  "src": "s1"},
      "payables":    {"value": 2900,  "src": "s1"}
    },
    "FY2023": {"revenue": {"value": 55565, "src": "s1"}}
  }
}
```

- Period keys contain the fiscal year (`FY2024`). The latest year per company is used for every ratio; each company keeps its own fiscal calendar, and the poster labels periods.
- Only revenue is needed for earlier years (growth). Add earlier years of other lines only if you want them in `analysis.json`.
- A value is `{"value": n, "src": "id"}`, or `{"value": null, "na_reason": "why"}`. A bare number is accepted but warns, because it has no source.
- Amounts in millions of the company's reporting currency. Costs are positive numbers.
- `sga` is the combined selling, general and administrative line. If a company reports selling and admin separately, add them and say so in the source `locator`.
- `ebit` is operating income as reported. If you use a company's adjusted operating income, do it for every company and say so in `narrative.limitations`.

## sources

```json
{"id": "s1", "title": "Deere & Company Form 10-K FY2024", "publisher": "SEC EDGAR",
 "date": "2024-12-19", "locator": "Consolidated statement of income, p. 48", "url": "https://..."}
```

Numbered on the poster in the order listed. Put the target's documents first.

## signals

```json
{"id": "g1", "kind": "management", "speaker": "John May", "role": "CEO", "date": "2025-08-14",
 "text": "Exact words from the source, at most two sentences.", "verbatim": true, "src": "s7"}
```

- `kind`: `management`, `analyst` (an analyst view reported in public news), `industry`, or `company` (a statement in a filing).
- `verbatim: false` labels the text as a summary. Use it for paraphrases and search summaries.
- Signals used in `priorities`, framings or bucket notes appear there. Up to four other `analyst` and `industry` signals appear under "Outside view"; set `"show": false` to keep one off the poster.

## exclusions

```json
{"company": "CNH", "metric": "dso", "reason": "receivables include dealer financing"}
```

Removes one company from one metric's benchmark. The company still shows in the chart, greyed and marked "excl.", and the reason prints under Limitations.

## sizing

| Field | Default | Meaning |
| --- | --- | --- |
| `horizon_years` | 3 | Years over which growth compounds; sets the bridge's end year |
| `capture` | 1.0 | Share of the gap closed. 1.0 is full gap closure; the method panel says so |
| `size_rnd` | false | Size R&D as a cost bucket |
| `commercial_margin` | target EBIT margin | Margin applied to incremental revenue; a fraction, or `"ebit_margin"` |
| `practitioner_ranges` | none | Optional second leg per bucket from a **public, cited** source: `{"sga": {"low_pct": 0.05, "high_pct": 0.10, "basis": "cost", "src": "s12"}}`. The opportunity becomes the larger of the peer and published legs at each end. Never fill this from memory |

## narrative

```json
"narrative": {
  "headline": "One sentence that answers the question, with {{tokens}}.",
  "exec_summary": ["Assertion with {{target.ebit_margin}} ...", "..."],
  "situation": ["What the company faces", {"text": "A fact from a source", "src": "s4"}],
  "priorities": [{"text": "Return core brands to volume growth", "signals": ["g1"]}],
  "framings": [{
    "title": "Growth is the gap, not margin",
    "lens": "revenue_cagr", "metrics": ["revenue_cagr", "ebit_margin"], "lead": true,
    "story": "Joins the computed gap to the stated priority, with {{rank.revenue_cagr}}.",
    "signals": ["g1"],
    "readiness": "high", "readiness_reason": "Restates management's own priority with evidence."
  }],
  "bucket_notes": {"operations": {"text": "Why the value is real", "signals": ["g2"]}, "sga": "Plain text is fine too"},
  "next_steps": ["What to test next"],
  "limitations": ["Anything specific to this case"]
}
```

`**bold**` works in narrative text. `readiness` is `high`, `moderate` or `low`.

## Tokens

Write `{{key}}` in any narrative text; the build replaces it with the formatted value and fails on an unknown key. Metric keys: `revenue_cagr`, `gross_margin`, `sga_pct`, `rnd_pct`, `ebit_margin`, `dso`, `dio`, `dpo`, `ccc`, `tsr`. Bucket ids: `commercial`, `operations`, `sga`, `rnd`, `working_capital`.

| Token | Gives |
| --- | --- |
| `target.name`, `target.period`, `case.currency`, `peers.count`, `horizon.end` | Labels |
| `target.revenue`, `target.ebit` | Latest-year amounts |
| `target.<metric>`, `<company id>.<metric>` | A company's value, e.g. `19.0%`, `62 days` |
| `median.<metric>`, `tq.<metric>` | Peer median, top quartile |
| `rating.<metric>` | `top quartile`, `above median`, `below median`, `bottom quartile` |
| `rank.<metric>` | `6 of 9` (best is 1) |
| `gap.<metric>` | Distance to the median when the target is behind, e.g. `3.0 pp`; 0 when ahead |
| `bucket.<id>` | Opportunity range, e.g. `$780M–1.6B` |
| `bucket.<id>.pct`, `bucket.<id>.bps` | The same as % of the cost line, and bps of margin |
| `total.pnl`, `total.cash` | The two totals |
| `bridge.latest_margin`, `bridge.target_margin` | EBIT margin today, and with the gaps closed |

`analysis.json`, written beside the poster, lists every fact under `facts`.
