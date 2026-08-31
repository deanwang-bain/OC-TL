---
title: "Screen 04: Analysis (update in progress)"
confluence_id: 19710705690
confluence_url: https://bainco.atlassian.net/wiki/spaces/OI30/pages/19710705690
version: 10
updated: 2026-08-25T04:47:40.251Z
---

# Screen 04: Analysis (update in progress)

[View in Confluence](https://bainco.atlassian.net/wiki/spaces/OI30/pages/19710705690)

Core analysis screen. Shows the EBIT bridge (SoP waterfall), cost bar breakdown, and ranked opportunity levers. Partners want to see the assumption behind every number and be able to adjust it. This is where the total Size of Prize is calculated.

|

**Data Displayed**

 |

**Source**

 |

**Calculation / Logic**

 |

**UX / Interaction (Raema)**

 |

**Agent / System Behaviour (Nikolozi)**

 |
|

*⚠ OPEN: EBIT vs EBITDA consistency — must use one basis consistently across all lever calculations and the final multiple. Align with Akhil.*

 |
|

*⚠ Data source hierarchies for this screen — Financial data: CapIQ → 10-K / annual report → LSEG. Qualitative data: LSEG Refinitiv (analyst reports, earnings calls) *

 |
|

*⚠ OPEN: Three SoP benchmarking approaches confirmed (gap to peer median, gap to closest peer, return to best internal year). Align with Akhil on implementation.*

 |
|

*⚠ Confirmed (Noah): Benchmarks are NOT proprietary. Bain Experience = judgment-based savings ranges, Bain IP + LLM inference — NOT a proprietary database.*

 |
|

*⚠ Confirmed (Noah): Tool must present assumptions to Partner and allow adjustment via chat.*

 |
|

*⚠ Confirmed (Stephanie): Partner can adjust cost bar assumptions via chat (e.g. 'IT is 9% not 12%') and the adjustment flows through to the lever calculation. *

 |
|

*⚠ Confirmed (Stephanie): Benchmark-driven vs Bain Experience-driven sizing must be clearly distinguished on each lever — two separate vectors for sizing.*

 |
|

*⚠ Confirmed (Stephanie): Each lever must show the metric change alongside the $ value (e.g. 'SG&A: $50M = 3pp reduction').*

 |
|

*⚠ Confirmed (Stephanie): EBIT bridge must have a toggle between EBIT $M and EBIT margin % views.*

 |
|

*⚠ Confirmed (Stephanie + Data Dictionary): NWC opportunity = one-time liquidity release, NOT recurring savings. DIO, DSO, and DPO must be presented and calculated separately. Chart must toggle per NWC metric. Drop 'supply chain' language.*

 |
|

*⚠ Confirmed: Bain Experience savings % sourced from comparable OI study on Iris (same industry). Where no comparable OI exists, use Iris benchmarks or online research. Source OI or benchmark reference must be documented.*

 |
|

*⚠ OPEN (Stephanie): Indirect procurement placement in cost bar — where does it sit relative to S&M and G&A? Confirm to ensure MECE structure.*

 |
|

Revenue ($M, FYxx) — baseline

 |

OI record (loaded in Screen 02)

 |

Read from OI record — loaded via CapIQ

 |

 |

Agent reads Revenue from OI record. Does not re-fetch from VCC/CapIQ on Screen 04. Same value used in Screen 02 target metrics column — must be identical.

 |
|

COGS ($M) — baseline

 |

OI record (loaded in Screen 02, adjusted)

 |

Read from OI record — loaded in Screen 02. NOT re-fetched on Screen 04. Adjusted for one-off items per approved adjustment list. D&A added to COGS when reported as separate line item. Same adjusted figure as used in Screen 02 Adj. Gross margin calculation.

 |

 |

Agent reads Adj. COGS from OI record. Same adjusted figure as Screen 02 — must be identical.

 |
|

Gross profit ($M / %)

 |

OI record (derived in Screen 02, adjusted metric)

 |

Gross Profit = Revenue − Adj. COGS. GP% = Adj. Gross Profit / Revenue × 100. Read from OI record — derived when adjustments were applied in Screen 02. NOT recalculated on Screen 04. If GP% > 100%, display NULL.

 |

 |

Agent reads Adj. Gross Profit from OI record. Same as Screen 02 Adj. Gross margin — must be identical. NULL rule already applied in Screen 02.

 |
|

SG&A ($M / %)

 |

OI record (loaded adjusted in Screen 02)

 |

Read from OI record — Adj. SG&A calculated when peer adjustments were applied in Screen 02. NOT re-fetched on Screen 04. Sourcing hierarchy: 1. Combined SG&A (IQ_SGA) 2. S&M + G&A 3. NULL. Never zero. Adjusted for restructuring. R&D separate where significant. Same adjusted figure as Screen 02 Adj. SG&A — must be identical.

 |

 |

Agent reads Adj. SG&A from OI record. Same adjusted figure as Screen 02 — must be identical.

 |
|

R&D ($M / %)

 |

OI record (loaded in Screen 02)

 |

Read from OI record — loaded in Screen 02. R&D sourcing hierarchy: 1. Line-item R&D (IQ_RD_EXP) 2. Footnote R&D (IQ_RD_EXP_FN) 3. NULL. Expressed as % of revenue. May sit inside or outside SG&A depending on company reporting — handled consistently across peer set in Screen 02.

 |

 |

Agent reads R&D from OI record. Same figure as used in Screen 02 cost bar.

 |
|

Adj. EBITDA ($M / %)

 |

OI record (derived in Screen 02)

 |

Read from OI record — Adj. EBIT calculated as residual in Screen 02 (Revenue − Adj. COGS − Adj. SG&A − R&D). EBITDA = Adj. EBIT + D&A. NOT recalculated on Screen 04. Residual approach ensures stack always reconciles to revenue. Use one basis (EBIT or EBITDA) consistently — confirm with Akhil.

 |

 |

Agent reads Adj. EBIT/EBITDA from OI record. Same as Screen 02 adjusted figures — must be identical. Does not recalculate from scratch.

 |
|

Cost bar sub-breakdown (per category)

 |

CapIQ / Agent (LLM inference)

 |

Where company reports sub-breakdown (e.g. Coca-Cola reports advertising separately), use reported split. Where not reported, agent infers using LLM + Bain IP + industry benchmarks. COGS breakdown into major categories required (direct materials etc. — may not be MVP). Partner can adjust any assumption via chat — confirmed by Stephanie. Indirect procurement placement to be confirmed (open item — ensure MECE with S&M and G&A).

 |

Agent shows assumed breakdown with editable fields. Reported vs inferred labelled. Partner can type in chat to adjust any assumption (e.g. 'IT is 9% not 12%') — confirmed as core interaction.

 |

Partner chat adjustment of cost bar assumptions flows through to lever recalculation — CONFIRMED by Stephanie. Agent updates affected levers automatically on each assumption change.

 |
|

Lever name + kind badge + description — on main screen

 |

Agent (derived)

 |

Each lever shown on the main Opportunities list as a card with: lever name, kind badge (Cost / Cash / Top line), optional flag badge (e.g. 'Estimated'), $ value, brief one-line description (e.g. '6pp above peer median · S&M overhead primary driver'), promote button, remove button.

 |

Lever cards on left column. Kind badge colour-coded: Cost (grey), Cash (light blue), Top line (light green). Flag badge shown in amber where applicable. Partner can drag to reprioritise, promote to top, or remove. Clicking card opens lever detail panel.

 |

Agent ranks levers by $ size and confidence. Changing a lever reruns only affected modules. Removed levers move to 'More candidates' section below.

 |
|

Lever value ($M) — point estimate + metric change

 |

Agent (derived) Peer set + adjusted financials from Screen 02 OI record Bain Experience library (Akhil) — for bottom-up sizing vector

 |

For POC, implement median AND top quartile as benchmark reference points. All options presented to user with a suggested SoP figure. The recommendation logic is not purely rule-based — should learn from past OI decks and Partner adjustments over time. Post-MVP / TBC: gap to closest peer (e.g. gap to Adidas) and return to best internal year. Alongside the $ value, the metric change must be shown (e.g. 'SG&A: $50M = 3pp reduction') — confirmed by Stephanie.

THREE benchmarking approaches (Noah confirmed): 1. Gap to peer median (most common): (target metric − peer median) × revenue base. 2. Gap to closest peer: (target − closest peer) × revenue base. 3. Return to best internal year: (current − best historical year) × revenue base. Alongside the $ value, the metric change must be shown (e.g. 'SG&A: $50M = 3pp reduction on SG&A spend'). These are the two vectors for sizing — benchmark-driven and Bain Experience-driven — and must be clearly distinguished.

 |

$ value shown prominently on lever card on main screen. Metric change shown alongside. Benchmark-driven vs Bain Experience-driven clearly distinguished — confirmed by Stephanie.

 |

MVP: Agent calculates gap to peer median only. Post-MVP: agent selects from three approaches per lever and shows assumption. Metric change calculated and displayed alongside $ value.

 |
|

Bain Experience range — shown in lever detail as part of triangulation (Gap to peer median vs Bain experience vs Recommended anchor)

 |

POC: Akhil’s library of Bain experience

MVP/Post MVP: Bain IP (Sage / comparable OI studies on Iris)

 |

Judgment-based savings % range per cost category. Sourced from comparable OI study in same industry on Iris. Where no comparable OI exists, use Iris benchmarks or online research — validate with practice area. Source OI or benchmark reference must be documented. NOT a proprietary database. Low/high end + scenario toggle.

 |

Shown in lever detail drill-down only — not visible on main screen. Displays alongside Gap to peer median and Recommended anchor as a three-way triangulation

 |

Agent surfaces Bain Experience range from Sage + comparable OI on Iris. Source reference documented. Range presented as assumption — Partner can tweak and recalculate. Two vectors (benchmark-driven vs Bain Experience) clearly distinguished on lever card.

 |
|

Overall confidence badge on total SoP (e.g. "High confidence" on $478M total). Per-lever confidence not shown on main screen — influences ranking order and flag badge only.

 |

Agent (derived)

 |

Weighted: CapIQ = high; Sage/Bain IP = high; manual = highest; other = low. Aggregate on lever card. Per-source breakdown in drill-down.

 |

Overall High/Medium confidence badge shown on total SoP summary only. Per-lever confidence not displayed on lever card — influences ranking order only

 |

Agent uses confidence values to rank levers and set overall SoP confidence badge. Per-lever confidence score not rendered on card. Design intent: dynamically calculated from source weights — not yet implemented in prototype. TBC with SN

 |
|

Lever type (Cost / Cash / Top line)

 |

Agent (rule-based)

 |

Enum: cost (SG&A or COGS) | cash (NWC release — one-time, not recurring) | topline (revenue uplift). Determines waterfall placement. Must use consistent EBIT/EBITDA basis across all lever types.

CONFIRMED (Noah/Kasia meeting): MVP SoP includes P&L (cost + topline), Cash (NWC), and Enterprise Value (apply EV/EBITDA multiple to EBITDA improvement). Priority order: P&L first, then Cash, then Enterprise Value.

 |

Colour-coded badge on lever card. Cash levers clearly labelled as one-time liquidity release.

 |

Agent classifies lever type. Cash levers are one-time liquidity release — NOT recurring savings. This distinction must be preserved throughout.

 |
|

Benchmarking approach used (per lever)

 |

Agent (derived)

 |

Which approach used: gap to peer median | gap to closest peer | return to best internal year. Label shown in lever detail so Partner can see and challenge.

 |

Label in lever detail. Partner can click to switch approach.

 |

Agent labels approach per lever. Partner switch triggers recalculation of that lever only.

 |
|

Peer benchmark values (per lever)

 |

CapIQ + peer set (Screen 02)

 |

Peer values for the metric backing this lever. Adjusted figures. Peer median and top quartile shown.

 |

Shown in lever detail drill-down.

 |

 |
|

Rationale + calculation method (per lever)

 |

Agent (derived)

 |

How lever value was derived: approach, peer gap, Bain IP, assumptions. Partners want to see this — not raw numbers. Agent shows assumption and invites Partner to adjust.

 |

Drillable from lever card. Core trust mechanism.

 |

Partners must be able to drill into any number down to source and assumption — core design principle (Noah).

 |
|

Source audit (per lever, per source)

 |

CapIQ / Bain IP / Analyst

 |

Per-lever, per-source: data used | adjustment | adjusted value | comparability note.

 |

Expandable in lever detail.

 |

Source audit persisted per lever. Must survive session.

 |
|

Audit trail / underlying data model export

 |

Agent (derived) Confirmed (Noah/Kasia meeting, Aug 11)

 |

A tabular view of all assumptions and calculations must be exportable (HTML or equivalent). Shows: the data the analysis is running off of, all assumptions made, all calculations performed. Purpose: auditability — Partners and clients must be able to verify the work.

 |

Export button available. Tabular format (HTML/Excel). Each assumption row shows: assumption, source, value, Partner override if applicable.

 |

Agent generates audit trail log from all lever calculations, assumption inputs, and source references. Export triggered on Partner request. Log is immutable and persists for full OI session.

 |
|

"What the market already expects"

 |

CapIQ (analyst consensus EBITDA forecasts) + LSEG Refinitiv (analyst reports, sell-side estimates)

 |

Analyst consensus EBITDA improvement forecast over the plan horizon — sourced from CapIQ consensus estimates and LSEG analyst reports. Shown as a pp EBITDA margin improvement already priced into the stock price. Purpose: the SoP ambition must be set above this baseline — otherwise the plan just delivers what the market already assumes and creates no incremental shareholder value. Shown as a fixed info box in the EBIT bridge detail panel at both the baseline EBITDA step and the target EBITDA step of the waterfall drill-down.

 |

Fixed info box shown in the EBIT bridge detail panel — not an interactive element. Appears at both the baseline EBITDA step and the target EBITDA step when Partner drills into the waterfall. Styled distinctly from lever cards to indicate it is market context, not a Bain-sized opportunity. Not adjustable by Partner.

 |

Agent pulls analyst consensus EBITDA forecast from CapIQ and/or LSEG. Calculates implied consensus EBITDA margin improvement over plan horizon. Displays as a fixed read-only context box — not a lever, not adjustable. Serves as a sanity check anchor: if total SoP is at or below consensus, the ambition may need to be raised before the Partner proceeds to Output.

 |
|

Sub-levers (name, description, $ range, Bain IP)

 |

Agent + Bain IP (Sage)

 |

Each lever decomposes into 2–4 sub-levers with Bain Experience savings ranges. Linked to Bain IP asset. Sub-lever ranges sum to (or contain) parent lever value.

 |

Shown in lever detail drill-down.

 |

Agent proposes sub-lever decomposition using Sage + LLM. Partner can adjust.

 |
|

NWC levers — DIO, DSO, DPO (separate)

 |

OI record (loaded in Screen 02)

 |

OI record (loaded in Screen 02)

Confirmed from Kasia methodology notes, Aug 12 -DIO/DSO/DPO improvement ranges should be based on peer median and top quartile of the confirmed peer set. The analytical basis for ranges was flagged as unclear — use peer median and top quartile as reference points. May be tailored per industry in future.

 |

DIO, DSO, DPO shown as separate levers. Each with its own $ value and days improvement. Chart above toggles per NWC metric. 'Supply chain' language removed — use 'Working Capital'.

 |

Agent calculates DIO, DSO, DPO separately. Total NWC = sum of three. Chart toggles per metric on days. Cash SoP = sum of all three NWC opportunities. One-time liquidity release only.

 |
|

EBIT bridge / waterfall chart + toggle

 |

Derived

 |

Waterfall from baseline EBIT → adjustments by lever type → implied target EBIT. Residual Adjusted EBIT approach ensures stack always reconciles to total revenue. Toggle: EBIT $M view vs EBIT margin % view — confirmed by Stephanie.

 |

Dynamic chart. Toggle between EBIT $M and EBIT margin % views — confirmed by Stephanie. Partners focused most attention on this chart in user testing.

 |

Agent renders waterfall dynamically. Toggle between $M and margin % recalculates display without changing underlying data. Updates as levers confirmed or excluded.

 |
|

P&L SoP total ($M)

 |

Derived

 |

Sum of all confirmed cost and topline lever point estimate values. Shown separately from Cash SoP on Dashboard card and Analysis screen.

*📎 Source: Email from Stephanie (executive sponsor)*

 |

Displayed prominently. Labelled as P&L SoP. Updates dynamically.

 |

Agent recalculates P&L SoP total on every lever change. Propagated to Dashboard P&L SoP card.

 |
|

Cash SoP total ($M)

 |

Derived

 |

Sum of all confirmed NWC lever values (DIO + DSO + DPO opportunities). One-time liquidity release — not recurring savings. Shown separately from P&L SoP.

*📎 Source: Email from Stephanie (executive sponsor) + OI Data Dictionary v2*

 |

Displayed prominently. Labelled as Cash SoP. Clearly marked as one-time. Updates dynamically.

 |

Agent recalculates Cash SoP from NWC levers only. Propagated to Dashboard Cash SoP card.

 |
|

Enterprise Value SoP

 |

Already in OI record

 |

Confirmed (Noah/Kasia meeting, Aug 11): Enterprise value SoP = confirmed EBITDA improvement (P&L levers) × EV/EBITDA multiple (VCC, consensus NTM basis). Third dimension of SoP alongside P&L and Cash. For MVP: apply the multiple simply. Check with Full Potential team for their approach. Both values already in OI record — no new data fetch needed.

 |

Shown separately from P&L SoP and Cash SoP. Labelled clearly as Enterprise Value uplift. Low/high end scenarios use low/high Bain Experience range from Screen 04.

 |

Agent reads EBITDA improvement from P&L levers and EV/EBITDA multiple from OI record. Calculates EV uplift. Propagates to Dashboard and Output screen waterfall.

 |
|

Sector KPI cards — industry-specific operational metrics

 |

CapIQ + peer set + Agent (derived)

 |

Industry-specific operational metrics shown as cards above the lever list. Confirmed from HTML screen comment: 'These are the metrics that a cross-industry ratio (SG&A % of revenue) can't capture.' Metric set is driven by the sector detected in Screen 01 and changes per industry. For Consumer / Retail (confirmed from HTML): Sales per sq. metre (Nike $6.8k vs peer median $8.1k, 16% behind), DTC revenue mix (42% vs peer median 51%, 9pp behind), Inventory turns (3.4x vs peer median 4.2x, 0.8x behind), Full-price sell-through (68% vs peer median 64%, 4pp ahead). Each card shows: target value, peer median, gap, and whether it is behind or ahead. Clicking a card opens a modal with explanation of whether the metric feeds into opportunity sizing and source links. Agent can export all sector KPIs with peer benchmarks to Excel on Partner request.

 |

Cards shown above lever list. Each card displays target value, peer median, and gap. Colour-coded: amber = behind peers, green = ahead. Clickable to open detail modal. Agent can export KPI set to Excel.

 |

Agent loads sector KPI set based on sector detected in Screen 01. KPI set changes per industry — Consumer / Retail KPIs confirmed from HTML. Agent explains whether each metric feeds into lever sizing or is informational only. TBC (Dipesh, UX workshop): 'flip view' on cards to show derivation on back face — confirm with Joanna for MVP.

 |
|

"More candidates" — levers ranked below the shortlist, shown as a grid below the main lever list on the main screen

 |

Agent (derived)

 |

Agent generates a longlist of all potential levers and ranks them. Top 5–6 appear in the main shortlist. Remaining candidates shown in the "More candidates" grid below. Each candidate shows: lever name and estimated prize value. Clicking opens a modal with: why it was ranked below the shortlist, condition for re-inclusion (e.g. 'Requires internal DTC channel P&L — upload to unlock'), and an "Add to shortlist" button.

 |

Grid section labelled "More candidates" shown below main lever list on main screen — visible without clicking in. Each card clickable to open detail modal. Modal shows reason for exclusion, re-inclusion condition, and Add to shortlist button.

 |

Agent generates exclusion reasoning and re-inclusion condition per candidate. "Add to shortlist" moves lever to main shortlist and triggers recalculation of SoP total.

 |
|

Lever detail panel — 'Why it's ranked #N of N'

 |

Agent (derived)

 |

When Partner clicks a lever card, detail panel opens. First section (if exists): ranking rationale — numbered badge (e.g. red '#1') + 'Why it's ranked #1 of 7' label + rationale text explaining rank position based on $ size, confidence, and speed to realise

 |

Shown at top of lever detail panel. Prominent numbered badge + ranking rationale text. Not shown if rankRationale is empty.

 |

Agent generates ranking rationale per lever based on $ size, confidence, and speed to realise. Rationale stored in OI record.

 |
|

Lever detail panel — Peer comparison chart

 |

Screen 02 output (OI record)

 |

Bar chart shown in lever detail panel — metric-specific per lever. Confirmed examples from HTML: SG&A lever → 'SG&A as % of revenue · peer comparison' bar chart; NWC lever → 'NWC days · peer comparison'; Gross margin lever → 'Gross margin % · peer comparison'. Chart shows all peers + peer median + Nike (highlighted in red). Same adjusted figures as Screen 02 — consumed from OI record, not recalculated.

 |

Bar chart shown at top of lever detail panel below header. Nike highlighted in red. Peer median shown. Chart label and metric are lever-specific.

 |

Agent renders peer comparison chart from Screen 02 adjusted figures stored in OI record. Same data as Screen 02 peer tiles — must be identical.

 |
|

Lever detail panel — Why text (narrative explanation)

 |

Agent (derived)

 |

Narrative explanation of why this lever exists and how the $ value was derived. Shown in grey box below the peer chart. Example from HTML (SG&A): 'Nike DTC discount depth runs above peer median, compressing net realised price. A 1–2% net price improvement through discount discipline and tiering is worth ~$70M, largely dropping to EBIT.' Partners want this — not raw numbers.

 |

Grey box shown below peer chart. Narrative explanation of lever rationale and sizing. Not editable — Partner can push back via chat.

 |

Agent generates why text from benchmarking gap, peer data, and Bain IP. Core trust mechanism — Partners must be able to understand any number.

 |
|

Lever detail panel — Value drivers (sub-levers)

 |

Agent + Bain IP (Sage)

 |

Numbered list of value drivers (sub-levers) shown below the why text. Each value driver card shows: number, name, description, $ impact range, Bain IP tag (e.g. 'Bain IP · Commercial Excellence Diagnostic'). Some value drivers have an 'AI lever' chip — clicking expands an AI-first lever insight with upside range and confidence note. Confirmed from HTML: SGA lever has 3 value drivers (S&M reallocation, Marketing operating model, Zero-based budgeting).

*📎 Source*

 |

Numbered value driver cards. Each shows name, description, $ impact, Bain IP tag. AI lever chip shown where applicable — tap to expand AI insight. Header shows 'tap a driver for AI levers'.

 |

Agent proposes value driver decomposition using Sage + LLM. AI lever insights surfaced where agent detects first-mover opportunities with no peer evidence. Partner can expand AI insight to explore upside beyond benchmark.

 |
|

Lever detail panel — 'Where we've done this · from Sage'

 |

Sage (Glean / Iris)

 |

Bain case references shown below value drivers. Labelled 'Where we've done this · from Sage' (purple label). Each case card shows: case name, sector, year, team (e.g. 'Okafor, Bianchi +7'), impact delivered. Optional note shown if cross-industry case is included (e.g. 'AI flagged early supplier payments — a cross-industry lever; the capability travels even though the sector differs.'). Clickable → 'Open case in Sage' link.

 |

Purple-labelled section. Each case card clickable to open in Sage. Impact shown prominently. Cross-industry cases include an explanatory note.

 |

Agent queries Sage per lever for matching case references. Results ranked by relevance. On click: agent opens case in Sage in new tab.

 |
|

Lever detail panel — Three-stat summary grid (Benchmarking gap | Bain experience range | Confidence %)

 |

Screen 02 output (OI record) + Bain IP (Sage)

 |

Three compact stat cards shown side by side below case references. 1. Benchmarking gap ($) — the point estimate value (e.g. '$172M'). 2. Bain experience range ($M–$M) — the low/high range from Bain IP (e.g. '$143M–$287M'). 3. Confidence % — numeric confidence score with colour (green = high, amber = medium). These three together give Partner a quick read of the sizing triangulation.

 |

Three grey cards shown side by side. Benchmarking gap | Bain experience range | Confidence %. Compact summary of triangulation before full detail sections.

 |

Agent populates from OI record (benchmarking gap from Screen 02), Bain IP (experience range from Sage), and confidence score algorithm. Three values displayed together as triangulation summary.

 |
|

Lever detail panel — Peer comparison (text)

 |

Screen 02 output (OI record)

 |

Text section showing peer values for the specific metric backing this lever. Labelled 'Peer comparison'. Example from HTML (SG&A lever): 'Adidas 28%, Puma 26%, UA 31%'. Same adjusted figures as Screen 02 — consumed from OI record.

 |

Text section below three-stat grid. Shows peer values for the metric. Labelled 'Peer comparison'.

 |

Agent reads peer metric values from Screen 02 OI record. Same adjusted figures — must be identical to Screen 02.

 |
|

Lever detail panel — Bain achievable

 |

Bain IP (Sage / comparable OI studies on Iris)

 |

Text section showing the achievable % range description. Labelled 'Bain achievable'. Example from HTML (SG&A lever): '10–20% of SG&A base'. This is the narrative description of the Bain Experience range — separate from the $ range shown in the three-stat grid

 |

Text section below peer comparison. Labelled 'Bain achievable'. Shows achievable % range and basis.

 |

Agent surfaces Bain achievable range from Sage + comparable OI on Iris. Same source as Bain experience range in three-stat grid — narrative description version.

 |
|

Lever detail panel — Sources (drillable)

 |

CapIQ / Bain IP / LSEG / 10-K

 |

Source list shown below Bain achievable. Labelled 'Sources — tap to see adjustments'. Each source shown as a drillable row — tapping opens the source audit sheet showing: raw value | adjustment applied | adjusted value | comparability note.

 |

Source rows shown as drillable list. Each row shows source name and detail. Tap to open source audit sheet with full adjustment log.

 |

Agent generates source audit per lever per source. Must survive session. Partners must be able to drill into any number down to source and adjustment.

 |
|

Lever detail panel — Confidence (bar + explanation)

 |

Agent (derived)

 |

Confidence section shown at bottom of lever detail. Shows: progress bar (coloured green for high, amber for medium) + explanation text. Example from HTML: High = 'All figures from public financials. Adjustments documented in each source.' Medium = 'Some figures estimated using Bain IP. Upload data to improve.' Design intent: algorithm uses source weights (CapIQ = high, Sage/Bain IP = high, manual = highest, other = low) — not yet implemented in prototype, currently hardcoded per lever.

 |

Progress bar + explanation text at bottom of lever detail. Colour-coded: green = high, amber = medium. Explanation text explains basis for confidence level and what Partner can do to improve it.

 |

Agent displays confidence bar and explanation. Design intent: dynamically calculated from source weights — not yet implemented in prototype. TBC with SN.

 |
|

EBIT bridge drill-down — 'Levers feeding this step' + 'Key assumptions' + 'Override an estimate'

 |

Screen 02 output (OI record) + Agent (derived)

 |

Clicking a waterfall bar in the EBIT bridge opens a separate drill-down view (different from clicking a lever card). Confirmed sections from HTML: 1. 'Levers feeding this step · tap to drill' — clickable list of levers contributing to that waterfall step. Each lever card is clickable to open its lever detail. 2. 'Key assumptions' — structured table of assumptions behind that step (e.g. 'SG&A rationalisation: 10–20% of the SG&A base; anchored to the 6pp gap to peer median'). 3. 'Override an estimate' (amber box — shown for estimated/medium-confidence levers only): editable input field + Apply button. Example from HTML: IT lever — 'IT has no public line item — estimated at 4% of revenue using Bain IP. If you know the real figure, change it and the lever re-sizes across the bridge and totals.'

 |

Waterfall bar click opens EBIT bridge drill-down (separate from lever card detail). Three sections: Levers feeding this step (clickable), Key assumptions table, Override an estimate (amber box — shown for estimated levers only). Override has editable input + Apply button.

 |

Agent renders EBIT bridge drill-down from lever data in OI record. 'Levers feeding this step' are clickable — opens lever detail for that lever. Override an estimate: Partner changes assumption (e.g. IT % of revenue), agent re-sizes lever and updates bridge and SoP totals in real time. Logs action in Log tab.

 |
|

Chat panel (RAG-grounded) + Log + Sources

 |

CapIQ baseline financials (via VCC pipeline) · Lever calculation outputs · Source audit log (per lever, per source) · Bain IP / Sage (Bain Experience ranges, comparable OI studies, case references) · Cost bar sub-breakdown (reported + inferred)

 |

RAG retrieval scope: all lever values and calculation inputs, source audit log entries per lever per source, Bain Experience % ranges and source OI references from Sage, Bain case references matched to each lever, cost bar sub-breakdown. Retrieval triggered by Partner query on any lever, number, or assumption.

 |

Chat panel has three tabs — all confirmed from HTML screens (Screens 01–05): • Chat tab (default): Persistent chat interface. Partner can type at any point. Agent responses appear inline. Conversation history visible within session. Attach button allows Partner to upload files directly from chat — uploaded files added to Sources tab automatically. • Log tab: Timestamped audit trail of all actions taken on this OI. Four actor types, colour-coded: System (OI created, data loaded), Agent (benchmarking run, values updated), Partner / You (levers promoted/removed, assumptions overridden), Collaborator (named collaborator actions). Log persists across the full OI session. • Sources tab: Live list of all active data sources used in the current analysis. Grouped into four categories: Financials & filings (CapIQ, 10-K, statutory filings — blue), Bain knowledge (Bain Experience, Sage case library — red), Analyst & market (LSEG analyst reports — amber), Uploaded (Partner-uploaded files — green). Each source shows: name, detail description, last updated date, confidence (High / Medium), and a Refresh button. Source count shown at top (e.g. '6 active sources'). Partner-uploaded files via chat attach automatically appear here.

 |

Agent uses retrieved context to: explain assumption behind any lever, switch benchmarking approach and recalculate, update lever values when Partner adjusts cost bar assumptions via chat (CONFIRMED), surface Bain case references, explain excluded levers, answer 'how was this number derived?' questions. Log tab: Agent automatically records every action in the Log — data loads, benchmarking runs, value updates, assumption changes, source refreshes. Log entries are immutable and persist for the full OI session. Collaborator actions also recorded. Sources tab: Agent maintains the live source list automatically. Sources added when data is loaded (CapIQ, 10-K, LSEG, Bain IP) and when Partner uploads files via chat attach. Agent updates source confidence (High / Medium) based on data quality. Refresh button triggers agent to re-pull latest data from that source and re-flag any benchmark changes.

 |
