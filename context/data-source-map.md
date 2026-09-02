# Data source map — what we pipe in, what is uploaded, and where the risk sits

**Written 2026-09-02, Tech Lead view.** Prepared in response to Fritz Jaeger's ask on the
OI3.0 Build LT thread, following Kasia's AMBER risk flag on LSEG data availability:

> *"…share an overview of all the data we are trying to either pipe in or allow for manual
> upload. I'd like to know (1) what we are planning by data source, and (2) what is the
> risk."* and *"for LSEG is there anything we can do to address it?"*

Everything below is drawn from the OI30 mirror and cited to the page it comes from.
**Risk ratings are Tech Lead judgement, not a documented rating** — the space has no risk
register page. Where the documentation does not answer something, it says so rather than
filling the gap.

Primary sources: [Data Sources summary](../confluence/oi30/data-requirements/data-sources-summary-19619676163.md),
the five [per-screen data requirement pages](../confluence/oi30/data-requirements/data-requirements-per-screen-19710771207.md),
[VCC Overview meeting](../confluence/oi30/meeting-summaries/vcc-overview-meeting-19696746551.md) (4 Aug),
[OI data_sync](../confluence/oi30/meeting-summaries/oi-data-sync-19752779777.md) (13 Aug),
[Technology Choices](../confluence/oi30/architecture/opportunity-indicator-architecture-high-level/technical-stack/technology-choices-19751338017.md).

---

## 1. The one-page answer

| # | Source | What it feeds | MVP mechanism | Risk |
| - | ------ | ------------- | ------------- | ---- |
| 1 | **CapIQ** (XpressFeed → Snowflake, reached via VCC's DB) | Every number in the product — baselines, peer medians, NWC days, CapEx, TSR inputs | **Piped.** Fully automated today: companies monthly (full), financials daily (incremental) | 🟠 |
| 2 | **VCC** (pre-computed outputs) | TSR & share price, Buy/Hold/Sell, Black/White/Grey, company description **only** | **Piped**, access method still unconfirmed (API vs Snowflake share) | 🟠 |
| 3 | **Company filings** — 10-K/10-Q, annual reports, earnings releases (SEC EDGAR + non-US equivalents) | Source of truth where CapIQ does not reconcile; non-recurring items; segment/BU data; gross trade receivables | **Piped**, on-demand per company/peer | 🟠 |
| 4 | **Iris / Bain IP via Glean (Sage)** | Bain experience ranges behind **all 14 sub-levers**, past cases, credentials, APT content on the final slide | **Piped**, *sandbox access TBD* | 🔴 |
| 5 | **Levers Library, industry map, past-OI peer file, adjustment-formula files** | The savings % ranges and industry watch-outs that turn a cost base into a size of prize | **Neither.** Curated files attached to Confluence pages | 🟠 |
| 6 | **LSEG (Refinitiv) analyst reports** | Qualitative only in the screens: peer Analyst view tab, leadership signals, referenced passages. Listed third in the financial fallback hierarchy but explicitly *"not a financial fallback"* | **Piped**, access mechanism unconfirmed | 🟠 |
| 7 | **Earnings call / CEO interview transcripts** | Management commentary, client-readiness signals | **Piped** — *"sourced via LSEG or direct public scrape"* | 🟢 |
| 8 | **Partner uploads** (PDF, Excel, Word, PPT, CSV) | Adjusted financials (override CapIQ), analyst/industry reports, framing docs | **Manual upload.** Built into Screen 01 and the Sources tab on 03/04/05 | 🟠 |
| 9 | **Bain / client relationship mapping** | Screen 01 account relationship card — key account partner, past cases | **Specced as piped** (Sage/Iris); **is actually a manual file** refreshed 6-monthly | 🟠 |
| 10 | **Aura, ARC Data, PEG expert interviews, FRWD, Glassdoor/Fishbowl, Cortex, sentiment, web scraping** | Workforce, cost-initiative benchmarks, expert validation, CPG benchmarks | **Not in MVP.** Roadmap only — architecture must accommodate without a rewrite | 🟢 |

🔴 material and unresolved · 🟠 live risk, mitigable · 🟢 low

**The short version for the LT:** three sources carry the numbers (CapIQ, filings, Bain IP
via Glean), one carries the words (LSEG), one is the escape hatch (Partner upload), and
everything else is roadmap. **LSEG sits on the qualitative side of that line** — which is
why the AMBER flag, while real, does not put the size of prize at risk. The dependency I
would watch harder is #4.

---

## 2. Piped sources, in detail

### 2.1 CapIQ — the single source of truth for financials

Confirmed at the [VCC Overview meeting](../confluence/oi30/meeting-summaries/vcc-overview-meeting-19696746551.md):
*"CapIQ is the single source of truth for all financial data. No other source provides
financials"* and *"CapIQ ID is the master company identifier — all data sources map back
to it."*

Already automated: XpressFeed loads companies monthly in full and financials daily as
incremental deltas, across ~20 million companies. This is the most mature pipe we have and
it is inherited, not built.

Four caveats that are not obvious from the pipeline being green:

1. **We must not consume CapIQ's pre-computed cost lines.** Confirmed by Akhil in the
   calculations workshop: *"Do NOT use CapIQ pre-computed COGS/SG&A. Cross-check CapIQ
   figures against company filings. Where CapIQ figures do not reconcile to reported
   figures, use the filing as source of truth."* So CapIQ is the source of *raw line
   items*; the adjustment logic is ours.
2. **Rate limits and per-call cost are still unanswered.** Technology Choices §4.3 says the
   external rate-limiting component's design *"is blocked on CapIQ rate limits and per-call
   cost, which remain unanswered. Until then it is built to a conservative default and made
   configurable."* Open item 2 ties the same unknown to *"whether real-time fetch survives
   at 2300 users."*
3. **The acquisition mechanism is specified two different ways.** Technology Choices lists
   MVP as **"Real-time fetch per run"**, moving to monthly batch at north star, and marks
   that a *mechanism change*. The VCC meeting recorded the opposite as a decision:
   *"Batch processing only — no real-time data in OI 3.0 under any circumstances."* Both are
   current. This is worth closing before Sprint work hardens around either.
4. **Taxonomy translation is a build, not a lookup.** CapIQ's classification does not match
   Bain's; a translation layer must be designed in from the start. Akhil's A1 OI mapping
   file is the available starting point.

### 2.2 VCC — deliberately narrowed

VCC was originally the intended front door for financials. **Noah's email of 12 August
changed that**, and both Screen 01 and Screen 02 now carry it as a critical update: VCC's
computed P&L metrics (EBIT margin, cost bar breakdown, SG&A, gross margin) and cash metrics
(DIO, DSO, DPO) *"have significant errors and are NOT reliable for use in OI 3.0 at
present."* The instruction is to pull **raw CapIQ data from VCC's Snowflake DB, before VCC
adjustments**, and apply our own logic.

What VCC still supplies: TSR and share price analysis, Buy/Hold/Sell analyst perspective,
Black/White/Grey analysis, and CapIQ company descriptions.

The screen note is blunt about the consequence: *"This changes the architecture materially —
OI 3.0 must be a standalone computation engine for all P&L and NWC metrics."* Access method
(API vs Snowflake data share) was an action on Sandeep before the architecture workshop and
is not recorded as closed in the space.

### 2.3 Company filings

Used three ways: to verify CapIQ, to identify non-recurring items from footnotes and MD&A,
and as the primary source for line items CapIQ does not carry cleanly (gross trade
receivables is the named example). Segment/BU data has its own hierarchy — CapIQ Segments
screen → 10-K/10-Q → Partner upload.

**The load-bearing risk here is latency, not availability.** Screen 02 carries a new
engineering flag: the three-step adjustment runs *for all proposed peers at screen load,
before the screen renders* — so 10-K parsing, non-recurring item identification and
adjustment calculations happen upfront for every peer, not lazily on panel open. With the
[NFR page](../confluence/oi30/architecture/opportunity-indicator-architecture-high-level/nfr-non-functional-design-choices-19704905798.md)
empty, there is no latency budget to hold that against, and the 30-minute end-to-end target
is the headline product claim.

### 2.4 Iris / Bain IP via Glean — the dependency I would rate above LSEG

The Data Sources summary marks Glean API access **"(sandbox access TBD)"** and calls Iris
*"Critical for Bain IP retrieval in OI 3.0."* That is not overstated. Reading Screen 04:
every one of the 14 sub-levers takes its *Bain experience range* from *"Bain savings % from
comparable OI on Iris/Sage × relevant cost base."* For five sub-levers — Share of wallet,
Manufacturing & conversion efficiency, Product cost engineering, Indirect spend, IT
rationalisation — **there is no peer benchmark at all**, so Bain IP is the only evidence
source. Screen 01's account relationship card and Screen 05's "Why Bain" slide also depend
on it.

If Glean access does not land, the product still produces peer-gap numbers but loses the
Bain half of the triangulation on every lever, and loses five levers entirely. That is a
bigger functional hole than the LSEG one, and it is tracked only as a parenthetical "TBD".

### 2.5 The curated benchmark files

The Levers Library, industry/sector map, past-OI peer set file, adjustment-formula files and
cost-bar examples are listed on
[Data sources from Current OI](../confluence/oi30/data-requirements/data-sources-from-current-oi-19727482890.md)
and referenced directly from Screens 03 and 04 as the origin of the % uplift ranges.

They are Confluence attachments. They have no pipeline, no refresh cadence, and no named
owner in the space. For GLS that is fine and probably correct. It is worth being explicit
that it is a deliberate manual dependency rather than an oversight, because the numbers
these files carry appear on the size-of-prize slide.

### 2.6 LSEG — see §5

### 2.7 Transcripts

The Data Sources summary already records the fallback: transcripts are *"sourced via LSEG or
direct public scrape."* Earnings call transcripts, CEO/chairman letters, investor day
material and press are substantially available without a licensed feed. This matters for the
LSEG mitigation — see §5.4.

---

## 3. The manual upload path

This is already designed, and it is more capable than "attach a file":

- **Where:** Screen 01 (upload nudge + chat attach) and the Sources tab on Screens 03, 04
  and 05. Accepted: PDF, Excel, Word, PowerPoint, CSV. A P&L template is downloadable.
- **What happens to a file:** the agent classifies and routes it — adjusted financials to
  the financial data layer (**these override CapIQ defaults**); analyst and industry reports
  to the qualitative layer for Screens 03/04; factor decks, RFPs and briefs to the framing
  layer. Routing is confirmed back in chat and written to the Log tab.
- **Effect on the product:** uploaded files appear automatically in the Sources tab, and the
  confidence score recalculates after each upload.
- **Private companies:** upload is the whole path. Screen 01 prompts for documents when
  entity resolution returns a private company; Screen 02's Analyst view falls back to
  statutory accounts marked directional only.

**Two gaps worth naming:**

1. **Governance is not written.** The VCC meeting decided *"All Partner uploads are treated
   as red (confidential) data by default — the system must enforce isolation by design, not
   by policy,"* and Kasia was to document the red/orange/green framework. The
   [Confidential data](../confluence/oi30/roadmap-business-requirements/confidential-data-19689340995.md)
   page still reads *"To be decided how to treat it?"*. Uploads are the one path where a
   Partner can put client-confidential material into the system, so this is the governance
   question that most needs an answer before GLS.
2. **The override rule is unstated.** An uploaded P&L takes priority over CapIQ. Nothing
   says what happens when the uploaded figures do not reconcile to the filing, or whether
   the mandatory reconciliation check against reported adjusted EBIT still applies. Kasia
   raised the same concern at the VCC meeting — *"partner data uploads potentially
   overwriting information."*

---

## 4. Risks, ranked

Ordered by what I would spend LT attention on, not by likelihood.

| # | Risk | Consequence if unresolved | Owner named in the space |
| - | ---- | ------------------------- | ------------------------ |
| R1 | **Glean/Iris access is "sandbox TBD"** | Bain experience ranges disappear from all 14 sub-levers; 5 sub-levers lose their only evidence source; "Why Bain" slide and account card degrade | Sandeep (Glean/IRIS), Siva |
| R2 | **CapIQ acquisition mechanism contradiction + unanswered rate limits/cost** | Rate limiter designed to a placeholder; the 30-minute claim and the GLS live demo both ride on real-time fetch that has never been sized | Open item 2, Technology Choices — no individual named |
| R3 | **LSEG contractual/technology restriction** (Kasia's AMBER flag) | Loses peer Analyst view, leadership signals and referenced passages; *possible* quantitative exposure via consensus estimates — see §5.2 | Escalated to Dean/Siva on the screen pages; Sandeep holds the Glean question |
| R4 | **Partner-upload governance unwritten** | Red data handling rests on an undocumented assumption; upload-vs-CapIQ override has no reconciliation rule | Kasia |
| R5 | **All-peer filing parse at screen load** | Screen 02 render time scales with peer count against no latency budget; worst case is a slow first screen in the GLS demo | Not assigned; NFR page empty |
| R6 | **Curated benchmark files have no owner or cadence** | The savings % ranges on the output deck age silently | Not assigned |
| R7 | **Relationship mapping specced as an API, delivered as a 6-monthly file** | Screen 01 account card may show stale relationship data, or not build as specced | Stephanie maintains the file; Michelle was confirming need |

R2 and R5 are the two that bite specifically at GLS, because both are latency risks in a
live demo.

---

## 5. LSEG — what is actually exposed, and what we can do

### 5.1 What the risk flag says

Kasia's flag: contractual and technology limitations may restrict how OI 3.0 can use and
process LSEG data, *"may require manual interventions limiting the automation workflows."*
Mitigation in flight: a GLS workaround using curated reports, plus assessment of alternative
sources including AlphaSense, with RDS and BCN.

This is consistent with what the space already flags. Screen 02 carries
*"OPEN (RED): LSEG access mechanism unconfirmed. Required for analyst view per peer.
Escalate to Dean/Siva."* Screens 01 and 03 carry the same warning. The
[LSEG page](../confluence/oi30/data-requirements/data-sources-summary/lseg-19618889872.md)
is **empty** — it is the only data source with no integration notes at all.

### 5.2 Exactly what breaks

| Surface | What LSEG provides | If unavailable |
| ------- | ------------------ | -------------- |
| Screen 02 — peer **Analyst view** tab | Bank, rating, report date, LLM-extracted key insight, management priorities, "Open full report" | Tab is empty for every peer. Private-peer fallback (statutory accounts, directional) already exists and would become the general case |
| Screen 03 — **Leadership signals** | Management commentary from earnings calls, annual reports, investor day, press | Degraded, **not lost** — see §5.4 |
| Screen 03 — **sources list with referenced passages** | Named broker notes (UBS, Morgan Stanley) with the extracted quote | Page already says *"LSEG-sourced passages unavailable if access not confirmed"* |
| Screens 01/04/05 — chat RAG scope and Sources tab | Qualitative context | Fewer sources listed; agent answers thinner on market view |
| **Every number** | Nothing | **No impact.** Financial hierarchy is CapIQ → 10-K/annual report → LSEG, and Screens 04 and 05 state plainly: *"LSEG used for qualitative signals only — not as financial fallback"* |

**One thing to close before we say "qualitative only" with confidence.** The Data Sources
summary attributes *"consensus analyst estimates (projected revenue growth)"* to LSEG, and
the [VCC Calculations summary](../confluence/oi30/roadmap-business-requirements/vcc-calculations-summary-19699040301.md)
builds projected revenue growth and revenue size of prize on *"analyst consensus forecasts"*.
If that consensus comes from CapIQ estimates — which is what the VCC lineage implies, since
VCC is a CapIQ platform — LSEG is genuinely qualitative-only and the flag has no numeric
blast radius. If it comes from LSEG, then a restriction touches a sized opportunity. No page
in the space resolves this. **It is a one-line answer from Akhil or Sandeep and it changes
how the risk should be rated.**

### 5.3 Why "manual intervention" is a smaller change than it sounds

The current OI process already works this way. Per the
[OI data_sync](../confluence/oi30/meeting-summaries/oi-data-sync-19752779777.md) session on
13 August, Akhil's team accesses analyst reports from banks like Barclays and JP Morgan
through the Refinitiv desktop platform — an analyst pulls the report, then it is used. There
is no automated feed today.

And the receiving path in OI 3.0 already exists: the upload flow **already classifies
analyst and industry reports and routes them to the qualitative context layer for Screens
03/04.** A curated-report workaround therefore needs no new integration — it reuses a
designed path.

### 5.4 Options

Assessed on what the documentation supports, cheapest first.

1. **Close the Glean question first — it may already be answered.**
   *"Confirm with Glean/IRIS whether they can fetch LSEG analyst reports"* has been an open
   action on Sandeep since **4 August**, due before the architecture workshop, and the
   mirror does not record an answer. The VCC meeting recorded the MVP intent as *"LSEG for
   market data and analyst reports **routed through Sage/Glean**"*. If Glean already holds
   LSEG content under Bain's existing entitlement, we inherit the entitlement instead of
   negotiating one, and the technology limitation largely evaporates. **This is a
   question, not a project, and it is four weeks old.**

2. **Adopt curated reports as the GLS path, deliberately.** Kasia's mitigation is the right
   one and I would formalise it: for GLS, analyst reports are pulled by BCN/RDS and loaded
   through the existing upload path. Two conditions — the demo target must be a public
   company anyway (MNPI, and the test plan forbids production documents in non-production
   environments), and **the 30-minute claim should be stated as excluding the manual
   retrieval step** rather than quietly absorbing it. A manual pull inside a timed
   end-to-end demo is a latency risk, not just a process one.

3. **Make the LSEG dependency a soft gate, not a hard one.** This is the design decision
   that costs least and protects most, and it is ours to take regardless of how the
   contract lands. The product already has the vocabulary: hard gates block on critical
   missing input, soft gates proceed with lower confidence. Every LSEG-fed surface should
   degrade visibly — Analyst view shows "no coverage available", leadership signals fall
   back to public transcripts, confidence badge drops — and **no LSEG condition should ever
   block a run**. Screen 02's private-company fallback is already the pattern to copy.

4. **Rebuild the recoverable part from public sources.** Leadership signals are specced
   against *"earnings calls, annual reports, investor day, press"* — largely public. The
   Data Sources summary already permits *"LSEG or direct public scrape"* for transcripts.
   Sell-side ratings and broker commentary genuinely require a licence; management
   commentary largely does not. Scoping the LSEG dependency down to *only* what is
   irreducibly licensed shrinks the exposure before we spend anything on it.

5. **On alternative vendors (AlphaSense).** Worth assessing, but it substitutes the
   *supplier*, not the *problem*: any licensed research aggregator carries persistence,
   redistribution and derived-use restrictions of the same class. So whichever vendor wins,
   the same architectural work is needed — and it is work we owe anyway:

   **ADR-007 commits us to enforcing rules we have not written down.** It states that
   *"source licensing rules, notably persistence restrictions on analyst report content, are
   enforced in one place."* That place is the evidence and provenance service, ranked #3 of
   only five builds argued as genuinely warranted. The LSEG page is empty. **A service
   cannot enforce a rule nobody has written** — this was finding S6 of the
   [ADR review](../reviews/2026-09-01-adr-001-to-009.md) and it is now the critical path
   item, not a documentation nicety.

   Three questions decide the design and should be answered by contract, not by inference:
   may report **text** be persisted (vector store, cache, audit log) or only pointers and
   short quotes? May a passage appear in an **exported PPT/HTML deck** that leaves Bain?
   May content be passed to a **third-party model endpoint**? The third is the one most
   likely to be missed, and Screen 03's *"Open full source"* plus the per-slide source
   footnotes in Screen 05 are exactly the paths where an export restriction would bite.

### 5.5 Recommendation

**Recommend, for the Tech Lead to take to the LT:**

- Treat R3 as AMBER on **feature completeness**, not on the numbers — with the §5.2
  consensus-estimates question closed first, since it is the one thing that could move it.
- Chase the Glean answer this week before any vendor assessment consumes effort (option 1).
- Accept curated reports as the GLS path, with the 30-minute claim scoped accordingly
  (option 2).
- Instruct StatusNeo now that **every LSEG-fed surface degrades softly** and no LSEG
  condition blocks a run (option 3). This does not wait on the contract.
- Get the persistence, export and model-endpoint restrictions written onto the LSEG page —
  whoever the vendor turns out to be — before the evidence service is built (option 5).

Sequenced this way, the contractual question stops being on the critical path for Sprint
work: only the persistence rules are, and those are a page of text, not a negotiation.

---

## 6. What is not written down

Flagged because a decision that rests on one of these rests on judgement, not policy.

- **LSEG page: empty.** The only data source with no integration notes.
- **IRIS integration page:** a stub asking *"Glean? or this is separate?"*.
- **Expert search integration page:** a stub asking which Bain system holds relationship data.
- **CapIQ overview page:** inherited and marked *"VERY OLD"*, with table locations still `??`.
- **Confidential data page:** *"To be decided how to treat it?"* — while uploads are already
  designed and assumed red.
- **NFR page: empty.** No latency budget behind the 30-minute claim.
- **Six sources carry `[CONFIRM INTERNALLY]`** in the refresh-type column: Aura,
  Glassdoor/Fishbowl, ARC, PEG, FRWD, relationship mapping. All are post-MVP, so this is
  not urgent — but the column reads as complete when it is not.
- **No risk register page exists in the space.** The AMBER flag lives in email and Teams. If
  the LT is going to run OI 3.0 against a RAG status, it needs somewhere to live that both
  Bain and StatusNeo read.

## 7. Asks

1. **Sandeep** — the 4 August action: can Glean/IRIS fetch LSEG analyst reports under Bain's
   existing entitlement? Four weeks open, and it is the cheapest possible resolution to R3.
2. **Akhil or Sandeep** — do consensus revenue-growth estimates come from CapIQ or LSEG?
   One line, and it decides whether R3 touches a number.
3. **Siva / StatusNeo** — write the LSEG persistence, export and model-endpoint rules onto
   the LSEG page before the evidence service is built (ADR-007 review finding S6).
4. **Kasia** — Glean/Iris sandbox access (R1) needs an owner and a date; it is a larger
   functional exposure than LSEG and is currently tracked as a parenthetical.
5. **Kasia** — the red/orange/green upload governance doc, and the rule for an uploaded P&L
   that does not reconcile to the filing.
6. **LT** — pick a home for the risk register so the RAG status is visible to StatusNeo too.
