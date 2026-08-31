---
title: "Methodology questions"
confluence_id: 19714834434
confluence_url: https://bainco.atlassian.net/wiki/spaces/OI30/pages/19714834434
version: 5
updated: 2026-08-11T21:31:42.836Z
---

# Methodology questions

[View in Confluence](https://bainco.atlassian.net/wiki/spaces/OI30/pages/19714834434)

|

Area

 |

Context / why we need a decision

 |

Methodology question

 |

Initial answer / working hypothesis from partner feedback

 |

**Methodology**

 |
|---|---|---|---|---|
|
1.

**Peer comparability criteria**

 |

Revenue, region and EBIT margin were highlighted as important for judging comparability.

 |

**What dimensions should determine peer comparability, and which should carry the greatest weight?**

 |

**Revenue and region are primary comparison vectors. EBIT margin should also be considered**, particularly where industry definitions produce companies with materially different margin profiles. Other dimensions remain to be confirmed.

**Sector**

**See margin profile (I can unselect it), not need to be the proposal criteria**

 |

Primary: Revenue / Region / Sector

Optional: EBITA margin

 |
|
1.

**Peer confidence / rationale**

 |

The peer positioning needs to translate into an understandable reason for inclusion.

 |

**How should the individual comparison dimensions translate into an overall peer recommendation / confidence?**

 |

Each dimension should contribute to an **explainable assessment**, with the positioning linked to a clear conclusion/rationale. **Exact weighting methodology remains open.**

 |

TBC - let’s iterate on peers confidence and select one that does good outcomes (CapIQ - exact example of what we don’t want, overweights region and deprioritised sector/business)

Good enough list - team has a claude skill

plus 1500 historical OIs for the peerset comparison

 |
|
1.

**Target-relative comparison**

 |

Partner wants to see target metrics alongside potential peers to judge whether differences are material.

 |

**Should peer comparability be explicitly assessed relative to the target? Which metrics and thresholds matter?**

 |

**Yes.** At minimum, show target vs. peer **revenue and EBIT margin**, alongside region. Material differences should inform the user's judgment on whether to include/exclude the peer. **Thresholds remain open.**

 |

Primary: Revenue / Region / Sector / Bain classification

Optional: EBITA margin

 |
|
1.

**Business-unit comparability**

 |

BU selection improves relevance but reduces available comparable metrics.

 |

**Do we allow BU-level peer selection when it limits downstream analysis?**

 |

**Yes, BU selection is valuable**, but the methodology needs to recognise that BU data is limited. Typically **revenue and EBIT margin may be available; gross margin and SG&A often are not.**

 |

BU - reported business unit by a company (from CapIQ)

When relevant, when user asks as to do so.

 |
|
1.

**BU impact on analysis**

 |

Excluding BUs changes the analytical basis for subsequent comparisons.

 |

**How should selecting/excluding BUs affect downstream calculations?**

 |

**The BU choice should flow through the rest of the analysis.** Analysis should only use comparison points feasible at the selected level. We still need to decide whether company-level metrics can supplement unavailable BU metrics.

 |

It is ok to compare business unit to full a company for specific metrics (data needs to be available, if we have EBITA but not other metrics let’s not make up the metrics).

Full company vs BU only → needs to be very clear on the selection and analysis through out

Example: Nike full company and Nike only one BU can be selected together

Make very clear to the user the selections and what will be included

Exception: when target is a BU - we can make some assumptions/ estimations, depending how confident we are in those we might not benchmark them to peers

We are not making assumptions on peers BUs to show in Benchmarking on BU level

 |
|
1.

**Size-of-prize definition**

 |

A single value does not represent the full opportunity.

 |

**What standard dimensions should size of prize include?**

 |

**At minimum two distinct dimensions: P&L size of prize and Cash size of prize.**

 |

Enterprise value (share price opportunity is)

Check with full potential - check later

For MVP: P&L, Cash, enterprise value (apply the multiple)

 |
|
1.

**EBIT opportunity representation**

 |

Absolute EBIT impact alone makes it difficult to assess the magnitude of improvement.

 |

**How should EBIT opportunity be represented?**

 |

Show **both $ impact and EBIT margin % / bps impact**. The user should be able to move between or see both views.

 |

ok

 |
|
1.

**Opportunity sizing methodology**

 |

Partner explicitly identifies two vectors for sizing opportunities.

 |

**What methodologies should be used to size opportunities?**

 |

Two core methodologies: **(1) benchmark-driven and (2) Bain experience-driven.** The product should make clear which methodology supports each opportunity. **How the two are combined remains open.**

 |

Show both options to the user

Top down / bottom up (explain it bottom up, as this is Bain experience)

Train based past decks?

Not a rule based

Learn over time

 |
|
1.

**Opportunity transparency**

 |

$ value alone is insufficient to gut-check the size of an opportunity.

 |

**What operational metric should accompany the $ value for each opportunity?**

 |

Show the **underlying magnitude of change** alongside $. Examples: SG&A = % spend reduction; Pricing/CE = margin bps/% improvement; Gross Margin = margin bps/% improvement; IT = % spend reduction.

 |

talk about it per metric / what are the combination of metrics we show

 |
|

**10. Benchmark methodology**

 |

Benchmark-driven sizing requires a consistent reference point.

 |

**What benchmark should determine the improvement potential?**

 |

**Not answered by the feedback.** Need to confirm whether sizing uses peer median, top quartile, best-in-class, etc.

 |

Create the logic (some of this is in VCC),

POC: median, top quartile

Akhil (potentially to chat about)

 |
|

**11. NWC methodology**

 |

NWC is not a single operational lever.

 |

**How should NWC opportunity be calculated?**

 |

**Calculate DIO, DPO and DSO separately and sum their value impact to determine total NWC opportunity.** Each metric should remain individually visible.

 |

we have a good page to calculate → take from VCC for POC

We might to tailor it per industry later on

 |
|

**12. NWC improvement ranges**

 |

Current design contains ranges, but their analytical basis is unclear.

 |

**How should the DIO/DPO/DSO improvement ranges be determined?**

 |

**Open question.** Partner explicitly flagged that it is unclear how the ranges are calculated.

 |

median / top quartile

 |
|

**13. NWC presentation**

 |

Users need to understand both value and operational movement.

 |

**How should NWC be presented?**

 |

Show **$ value plus days improvement separately for DIO, DPO and DSO**. Remove **“supply chain”** terminology from NWC.

 |

 |
|

**14. Cost-base taxonomy**

 |

Cost opportunities need a MECE structure across COGS, SG&A, R&D, procurement, etc.

 |

**What standard cost taxonomy should OI use?**

 |

Include at least **COGS, SG&A and R&D**, with further decomposition where feasible. **Exact MECE taxonomy remains open**, particularly treatment of indirect procurement.

 |

Spike on depth of this topic - there won’t be one. We need to be able to adapt to the peer set and target (build the adjustment logic) to the framing we need to make it comparable.

This is from the top down.

From the bottom up - we take what they report and build to our thinking (Bain IP), can look different from company to company

POC - go revenue, COGS, SG&A,

Check for the companies that has the comparable cost structure

 |
|

**15. Indirect procurement**

 |

Procurement opportunity overlaps with functional cost categories such as S&M and G&A.

 |

**Where should indirect procurement sit to avoid double counting?**

 |

**Open question.** Partner specifically flagged uncertainty around making indirect procurement MECE with S&M and G&A.

 |

tailored by case by case basis

this might be part of the context setting (from the chat from partner)

What is the default here - to discuss with Fritz

What are the archetypes/default for the cost breakdown for a starting point

Check proposals/ diligence decks - can be good for the process

Dynamic data model is important - as we do the dynamic updates

You can download to verify

 |
|

**16. R&D classification**

 |

R&D reporting differs across companies.

 |

**How should R&D be normalised across companies?**

 |

**R&D must be included as a distinct analytical category**, while recognising that reported financials may show it separately or within SG&A. Normalisation rule remains to be defined.

 |

 |
|

**17. COGS decomposition**

 |

High-level COGS may not provide enough information to identify opportunities.

 |

**What level of COGS decomposition is required?**

 |

Break COGS into **major categories**. Potentially break **direct materials into major spend categories**,

 |

Beyond what is reported, we need to go level deeper

Proposals / Diligence decks

→ get the decks example with COGS breakdown tailored company by company with industry specifics

 |
|

**18. Dynamic cost decomposition**

 |

Partners may want to investigate individual categories beyond the standard breakdown.

 |

**Should users be able to request further decomposition of a cost category?**

 |

**Yes.** The product should ideally support further breakdown on request, e.g. deeper decomposition of S&M, subject to data availability.

 |

as above

 |
|

**19. User-adjusted assumptions**

 |

Partners may have better account-specific knowledge than the initial system estimate.

 |

**Can users override assumptions, and what happens downstream?**

 |

**Yes.** Partners should be able to update assumptions through chat; e.g. change IT spend from 12% to 9%. **The revised assumption should automatically flow through the resulting size-of-prize calculation.**

 |

 |
|

**20. Assumption provenance**

 |

User overrides create a difference between system-generated and partner-adjusted analysis.

 |

**Should we retain the original assumption and record user overrides?**

 |

**Not explicitly answered.** Given the requested ability to adjust assumptions, this needs confirmation from business.

 |

Track and audit

No need to undo button

But they can see and adjust the numbers

For full scale can we do scenario branching? and compare and select

Make this known and show this was the partner assumptions (flag that assumptions were made, do you want to revisit assumptions etc)

 |

**Peer methodology:** Sector, Region, Revenue are primary dimensions, with EBIT margin added. Confirm the remaining dimensions, weights and acceptable variance versus the target.

**BU methodology:** BU selection is desirable, but it limits available metrics. Confirm whether company-level data can be mixed with BU-level data when detailed BU information is unavailable.

**Sizing methodology:** Establish the rules for the two sizing vectors — **benchmark-driven vs. Bain experience-driven** — including when each applies and how they interact.

**Benchmark methodology:** Define the reference point used for sizing: **median, top quartile, best-in-class, etc.** This is the biggest unanswered methodological item.

**Cost & cash methodology:** Confirm the MECE cost taxonomy, especially **COGS / SG&A / R&D / indirect procurement**, and codify **NWC = DIO + DPO + DSO**, with each component independently benchmarked and sized.

**Assumption methodology:** Partners can override assumptions and calculations should dynamically update. Confirm what can be overridden and whether original/system values need to be retained for transparency.

Company to check for POC: PepsiCo, International Paper, Nike, Lear
