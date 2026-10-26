# Post-GLS data sources: owners and approvals (DRAFT)

*Draft for the OI30 space. Refreshed 26 Oct 2026 (GLS day) from the Confluence mirror as of the Sprint 3 refresh. Which sources count as post-GLS is inferred, not stated in Confluence. Please correct the tables where they are wrong.*

## Summary

- No page in OI30 lists the data sources to add after GLS, and none records an approval request or its status.
- **GLS runs on a golden data set, not live sources.** The set was curated with BCN and delivered as JSON. It removed the LSEG and CapIQ dependencies, so Sprint 3 was the first sprint with nothing blocked on a vendor. The [Sprint 3 retrospective](https://bainco.atlassian.net/wiki/spaces/OI30/pages/19933790220) says *"not connecting live sources narrows the GLS functionality"*. The demo set is four named companies against that data.
- The live connections are therefore the main post-GLS data work: CapIQ, LSEG and S&P MCP for financials, and IRIS/Glean and Sage for Bain content.
- [Post GLS feature set](https://bainco.atlassian.net/wiki/spaces/OI30/pages/19800162379) lists only "Data Ingestion (?)" under Technical Foundations. It also lists "Further Validation, Additional Sectors, Geo Scope" under Data & Coverage Expansion. Neither names a source.
- **No data engineer was onboarded for the GLS sprints** (Sprint 3 retro). Nothing recorded says who builds the live connections.
- The go/no-go decision planned for the week of 19 October is not recorded on any page.

## Candidate post-GLS sources

| Source | Why it looks post-GLS | Connection owner named in OI30 | Open approval or access item |
| --- | --- | --- | --- |
| CapIQ (XpressFeed, or the API) | Replaced by the golden data set for GLS. API access is still unavailable. Sprints 1–2 worked around it with Excel extracts converted to Parquet | None | Rate limits and per-call cost unresolved |
| LSEG (analyst reports, 10-K filings) | Replaced by the golden data set for GLS. The [LSEG page](https://bainco.atlassian.net/wiki/spaces/OI30/pages/19618889872) links example filings, but the persistence restrictions that ADR-007 must enforce are not written down | None | Licence and persistence rules |
| S&P MCP, TSR data, 10-K extraction at scale | Design requirements 24.1–24.4 need TSR data. [Data Contacts](https://bainco.atlassian.net/wiki/spaces/OI30/pages/19817627730) says the current approach is "not yet repeatable at scale" | TSR Automation (Abishek Soni) and TSR tech team (Kritik Ajmani) | API access request and lessons-learned session still to be set up |
| IRIS case studies and transformation stories (via Glean) | [Design requirements (Post GLS)](https://bainco.atlassian.net/wiki/spaces/OI30/pages/19808256031) items 18.1–18.3. Sprint 1 delivered only a file archive for Glean | None | Glean API sandbox access listed as "TBD" in [Data Sources summary](https://bainco.atlassian.net/wiki/spaces/OI30/pages/19619676163) |
| Sage credential and expert search | Same design page, items 25.1–25.5. Item 25.5 (flag credentials already shown to the client) is marked "feasibility to be discussed" | None | Not recorded |
| Bain/client relationship mapping (account head, past cases) | [Expert search integration](https://bainco.atlassian.net/wiki/spaces/OI30/pages/19623641173): "in PEG it is Call2Cash", other systems still to be checked | None | System to be identified |
| Aura, ARC Data, PEG expert interviews, FRWD (CPG benchmark), Glassdoor/Fishbowl | Marked `[CONFIRM INTERNALLY]` in Data Sources summary, with no date | None | Not recorded |

## Already running without approval

- **Web search through serpapi.** [Future Scope](https://bainco.atlassian.net/wiki/spaces/OI30/pages/19849412714) says *"web search runs through a serpapi engine"*. The staging narrative agent calls only the model and web search. Target-company names leave Bain this way. serpapi is in no position table, no ADR and not in the Data Source Catalogue, so it needs a ruling or a named replacement.

## Teams named elsewhere in the space

- **BCN:** curated the golden data set.
- **VCC:** Jason Barns (PM), Jon Allen (UI/UX).
- **MCP:** Zach Haris (TSG Infrastructure).
- **Staging infrastructure approvals** (Front Door private link, Entra `User.Access`): Angel, per the [GLS deployment tracker](https://bainco.atlassian.net/wiki/spaces/OI30/pages/19909279789). These are not data-source approvals.

## Related open Jira items

- **OI3-18, OI3-43, OI3-65:** data foundation items removed from Sprint 2 and moved to the general backlog. The Sprint 2 retro warned they "still require close follow-up to not become another blocker for the GLS scope".
- **OI3-82:** rate and quota management, blocked on vendor limits in Sprint 2. Sprint 3 lists rate and quota management as delivered.
- **OI3-147:** Data Access Service, blocked on vendor limits in Sprint 2.
- **OI3-48:** development environment and access, open since Sprint 1.

## Follow-ups

1. Record the go/no-go outcome and what GLS actually demonstrated, so the golden-data caveat is on the record.
2. Name an owner for the live CapIQ, LSEG and S&P MCP connections, and a data engineer to build them.
3. Confirm who owns the Glean/IRIS connection, and get sandbox access.
4. Name an owner for each of Aura, ARC, PEG, FRWD and Fishbowl, and confirm each is wanted.
5. Identify the system behind client relationship mapping (Call2Cash or another).
6. Send the TSR team the API call details and access requirements, and book the lessons-learned session.
7. Rule on serpapi, and pull the permitted-use rules from the Data Source Catalogue workbook (SharePoint, outside the mirror) onto a page.
