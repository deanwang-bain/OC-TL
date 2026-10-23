# Post-GLS data sources: owners and approvals (DRAFT)

*Draft for the OI30 space. Prepared 23 Oct 2026 from the Confluence mirror. Which sources count as post-GLS is inferred, not stated in Confluence. Please correct the table where it is wrong.*

## Summary

- No page in OI30 lists the data sources to add after GLS, and none records an approval request or its status.
- [Post GLS feature set](https://bainco.atlassian.net/wiki/spaces/OI30/pages/19800162379) lists only "Data Ingestion (?)" under Technical Foundations. It also lists "Further Validation, Additional Sectors, Geo Scope" under Data & Coverage Expansion. Neither names a source.
- The [MVP sign-off page](https://bainco.atlassian.net/wiki/spaces/OI30/pages/19619676190) prioritises CapIQ, LSEG, IRIS, Sage/Glean, public sources and user uploads for the MVP. The sources below are the ones that look later.

## Candidate post-GLS sources

| Source | Why it looks post-GLS | Connection owner named in OI30 | Open approval or access item |
| --- | --- | --- | --- |
| IRIS case studies and transformation stories (via Glean) | [Design requirements (Post GLS)](https://bainco.atlassian.net/wiki/spaces/OI30/pages/19808256031) items 18.1–18.3 | None | Glean API sandbox access listed as "TBD" in [Data Sources summary](https://bainco.atlassian.net/wiki/spaces/OI30/pages/19619676163) |
| Sage credential and expert search | Same page, items 25.1–25.5. Item 25.5 (flag credentials already shown to the client) is marked "feasibility to be discussed" | None | Not recorded |
| Bain/client relationship mapping (account head, past cases) | [Expert search integration](https://bainco.atlassian.net/wiki/spaces/OI30/pages/19623641173): "in PEG it is Call2Cash", other systems still to be checked | None | System to be identified |
| Aura, ARC Data, PEG expert interviews, FRWD (CPG benchmark), Glassdoor/Fishbowl | Marked `[CONFIRM INTERNALLY]` in Data Sources summary, with no date | None | Not recorded |
| S&P MCP, TSR data, 10-K extraction at scale | Design requirements 24.1–24.4 need TSR data. [Data Contacts](https://bainco.atlassian.net/wiki/spaces/OI30/pages/19817627730) says the current approach is "not yet repeatable at scale" | TSR Automation (Abishek Soni) and TSR tech team (Kritik Ajmani) | API access request and lessons-learned session still to be set up |
| CapIQ API (replacing the Excel/Parquet workaround) | Access still unavailable | None | Rate limits and per-call cost unresolved |

## Teams named elsewhere in the space

- **VCC:** Jason Barns (PM), Jon Allen (UI/UX).
- **MCP:** Zach Haris (TSG Infrastructure).
- **Staging infrastructure approvals** (Front Door private link, Entra `User.Access`): Angel, per the [GLS deployment tracker](https://bainco.atlassian.net/wiki/spaces/OI30/pages/19909279789). These are not data-source approvals.

## Follow-ups

1. Confirm who owns the Glean/IRIS connection, and get sandbox access.
2. Name an owner for each of Aura, ARC, PEG, FRWD and Fishbowl, and confirm each is wanted.
3. Identify the system behind client relationship mapping (Call2Cash or another).
4. Send the TSR team the API call details and access requirements, and book the lessons-learned session.
5. Pull the permitted-use rules from the Data Source Catalogue workbook (SharePoint, outside the mirror) onto a page.
