---
title: "Post-GLS data sources: owners and approvals (DRAFT)"
confluence_id: 19973996610
confluence_url: https://bainco.atlassian.net/wiki/spaces/OI30/pages/19973996610
version: 4
updated: 2026-10-26T03:49:17.915Z
---

# Post-GLS data sources: owners and approvals (DRAFT)

[View in Confluence](https://bainco.atlassian.net/wiki/spaces/OI30/pages/19973996610)

*Refreshed 26 Oct 2026. Please correct the tables where they are wrong.*

### Summary

- **GLS runs on a golden data set, not live sources.** The set was curated with BCN and delivered as JSON. It removed the LSEG and CapIQ dependencies, so Sprint 3 was the first sprint with nothing blocked on a vendor.
- The live connections are therefore the main post-GLS data work: CapIQ, LSEG and S&P MCP for financials, and IRIS/Glean and Sage for Bain content.
- [Post GLS feature set]Post GLS feature set lists only “Data Ingestion (?)” under Technical Foundations.

### Candidate post-GLS sources

| Source  | What’s needed post GLS  | Connection owner named inOpCat  | Open approval or access item  |
|---|---|---|---|
| CapIQ (XpressFeed, or the API)  | Replace the golden data set with live company financials. API access is still unavailable, and Sprints 1–2 worked around it with Excel extracts converted to Parquet  | None  | Rate limits and per-call cost unresolved  |
| LSEG (analyst reports, 10-K filings)  | Replace the golden data set with live analyst reports and filings. The [LSEG]LSEG page links example filings, but the persistence restrictions that ADR-007 must enforce are not written down  | None  | Licence and persistence rules  |
| S&P MCP, TSR data, 10-K extraction at scale  | Primary route for financial data, plus TSR data for design requirements 24.1–24.4. [Data Contacts]Data Contacts says the current approach is “not yet repeatable at scale”  | TSR Automation (Abishek Soni) and TSR tech team (Kritik Ajmani)  | API access request and lessons-learned session still to be set up  |
| IRIS case studies and transformation stories (via Glean)  | Surface 2–3 Bain case studies per bucket, and full transformation stories, per [Design requirements (Post GLS)]Design requirements (Post GLS) items 18.1–18.3. Sprint 1 delivered only a file archive for Glean  | None  | Glean API sandbox access  |
| Sage credential and expert search  | Search and auto-surface Bain credentials and experts, and drag a credential into the deck (design items 25.1–25.5). Item 25.5 (flag credentials already shown to the client) is marked “feasibility to be discussed”  | None  | Glean API sandbox access  |
| Bain/client relationship mapping (account head, past cases)  | Pull account head and past-case data into the output. [Expert search integration (?)]Expert search integration says “in PEG it is Call2Cash”, with other systems still to be checked  | None  | System to be identified  |
| Aura, ARC Data, PEG expert interviews, FRWD (CPG benchmark), Glassdoor/Fishbowl  | Decide whether each is wanted and how it connects. All are marked `[CONFIRM INTERNALLY]` in Data Sources summary, with no date  | None  | Not recorded  |

Already running without approval

- **Web search through serpapi.** The staging narrative agent calls only the model and web search. Target-company names leave Bain this way. serpapi is in no position table, no ADR and not in the Data Source Catalogue, so it needs a ruling or a named replacement.

### Follow-ups

1. Name an owner for the live CapIQ, LSEG and S&P MCP connections, and a data engineer to build them.
1. Confirm who owns the Glean/IRIS connection, and get sandbox access.
1. Name an owner for each of Aura, ARC, PEG, FRWD and Fishbowl, and confirm each is wanted.
1. Identify the system behind client relationship mapping (Call2Cash or another).
1. Send the TSR team the API call details and access requirements, and book the lessons-learned session.
1. Rule on serpapi, and pull the permitted-use rules from the Data Source Catalogue workbook (SharePoint, outside the mirror) onto a page.
