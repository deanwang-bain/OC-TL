---
title: "VCC Overview meeting"
confluence_id: 19696746551
confluence_url: https://bainco.atlassian.net/wiki/spaces/OI30/pages/19696746551
version: 4
updated: 2026-08-05T07:21:28.625Z
---

# VCC Overview meeting

[View in Confluence](https://bainco.atlassian.net/wiki/spaces/OI30/pages/19696746551)

**OI 3.0 — VCC Overview & Architecture Alignment** **Date:** 4 August 2026

**Attendees:** Kasia Mrowca, Sandeep Uppal, Dean Wang, Michelle Flood, Siva Vyra, Giorgi Samadashvili, Nikolozi Metreveli, Dipesh Bhardwaj

**Key Decisions**

1. Batch processing only — no real-time data in OI 3.0 under any circumstances. The PE business lifecycle does not require it.
1. CapIQ is the single source of truth for all financial data. No other source provides financials.
1. CapIQ ID is the master company identifier — all data sources map back to it.
1. Each data source has a defined, non-overlapping data type — conflict is minimised by design.
1. OI 3.0 will have its own calculation engine regardless of what VCC provides, giving the project autonomy from VCC's roadmap.
1. Data structure is the highest-priority foundational work — Siva leads from day one. VCC's experience of rushing this is the cautionary reference point.
1. All Partner uploads are treated as red (confidential) data by default — the system must enforce isolation by design, not by policy.
1. Microsoft Foundry is the preferred agent orchestration platform.
1. OI 3.0 must expose its own MCP Server — it will be a data provider to other Bain systems in future, not only a consumer.
1. Architecture must accommodate new data sources and agents without requiring a rewrite — scalability by design is a firm stakeholder requirement.
1. All architecture decisions will be confirmed in the upcoming workshops once business and non-functional requirements are locked — no decisions are being made prematurely.

**Summary**

This session gave the StatusNeo delivery team a working understanding of VCC — Bain's internal financial analysis platform — and began aligning on the data and AI architecture for OI 3.0.

*What VCC is and what OI 3.0 inherits*

VCC is a database-heavy platform built on CapIQ data stored in Snowflake. It covers approximately 15,000 companies and provides pre-calculated financial metrics including TSR analysis, peer benchmarking, and stakeholder value analysis. It operates on one company at a time and generates PowerPoint outputs using ThinkCell, confirmed to run server-side in an automated pipeline.

VCC does not vectorize any data. When a user selects a company, an agent calls a fixed API, fetches all pre-calculated data, and passes it through a hardcoded sequence of agents. It works, but is rigid and was built under time pressure — resulting in architectural shortcuts the team is committed to avoiding in OI 3.0.

OI 3.0 can inherit from VCC: Bain Partner-grade financial calculations already built and validated, the CapIQ ID as master company identifier, and potentially ThinkCell for PowerPoint generation. OI 3.0 will also have access to VCC's database — either via API or a Snowflake data share — so it can consume VCC's pre-calculated outputs without waiting for a full API to be built.

*Data pipeline principles*

Sandeep framed OI 3.0 in two parts: a traditional data pipeline (Part 1, led by Sandeep and Siva) and an AI agent layer on top of it (Part 2, led by StatusNeo). Part 1 is known engineering territory and must be kept simple and correct. Part 2 is where specialist AI expertise is genuinely needed.

Every piece of data must carry three dates from day one: when it was fetched, when it was processed, and the date the source itself reports. Without this, Partners cannot defend data currency in a CEO meeting. Whether OI 3.0 retains historical versions of data after a refresh — or only keeps the latest — is a business decision that Noah and Kasia need to align on before the storage layer is designed. Regardless, an audit log of what data was used to generate each deck is non-negotiable, even where data is processed in memory and discarded.

*In-memory vectorization*

To enable intelligent, semantic search across a company and its peer set — something VCC cannot do — Sandeep proposed using ZVEC (an open-source in-memory vector database) alongside DuckDB. When a user selects a company, OI 3.0 fetches the company and peer set data, vectorizes it in memory, allows agents to run semantic and hybrid queries during the session, and discards it when done. This is designed for the small, session-scoped datasets OI 3.0 deals with and does not replace the batch pipeline.

*Data sources and company matching*

For MVP, data sources are: CapIQ via VCC for financials; LSEG for market data and analyst reports routed through Sage/Glean; Glean/IRIS for Bain IP and case materials; and Partner uploads for relationship context. Each source covers a specific, non-overlapping data type. On the longer-term roadmap: Aura (people data), Cortex (Bain's internal CRM for client relationship context), consumer and sentiment analysis, and web scraping. None are in MVP scope, but the architecture must accommodate them without a rewrite.

The primary cross-source challenge is company identity matching — the same company appears under different name formats across sources. CapIQ ID is the confirmed master identifier. A related challenge is industry taxonomy mapping: CapIQ's classification system does not directly match Bain's internal taxonomy, and a translation layer must be designed into the data structure from the start.

*Calculation engine*

VCC hard-codes calculations directly into Python with no consistent framework. OI 3.0 will have a structured, extensible calculation engine where each calculation follows a consistent interface and plugs in cleanly. Size of Prize — a core OI output — is not currently in VCC and will need to be owned by OI 3.0. An explicit mapping of which calculations live in VCC versus OI 3.0's own engine must be produced before architecture decisions are locked.

*Agent architecture*

Two components are critical for how agents retrieve and use data. A schema knowledge base gives agents a structured map of what data exists, where it lives, and what it means — so agents can construct the right queries automatically. A dynamic workflow engine determines at runtime which agents to call and in what order, based on the nature of the Partner's request. VCC uses a single hardcoded sequence; OI 3.0 needs dynamic assembly. Both must be designed from day one.

*Data governance*

The system cannot control what Partners upload. The working assumption is to treat all Partner uploads as red (confidential) by default and design accordingly — ensuring red data is never exposed across Partners and never used for model training. Bain's red/orange/green classification framework applies, mapping onto OI 3.0's three-layer data isolation architecture. Kasia is documenting full governance requirements in Confluence ahead of the workshop.

**Next Steps and Owners**

| Action  | Owner  | When  |
|---|---|---|
| Complete business and non-functional requirements document  | Kasia  | Before architecture workshop  |
| Confirm data freshness/tolerance with Partners  | Kasia  | Before architecture workshop  |
| Confirm whether sentiment analysis is in MVP scope  | Kasia  | Before architecture workshop  |
| Document data classification framework — red/orange/green  | Kasia  | Before architecture workshop  |
| Align on data history decision — store versions or latest only  | Noah + Kasia  | Before architecture workshop  |
| Locate September Excel and bring to Akhil session for validation  | Kasia  | Before Akhil session  |
| Run Akhil session — calculations walkthrough, Size of Prize, data tolerance  | Kasia + Sandeep  | Before architecture workshop  |
| Extract VCC calculation details from team chat and share with SN team  | Sandeep  | Before architecture workshop  |
| Confirm with Glean/IRIS whether they can fetch LSEG analyst reports  | Sandeep  | Before architecture workshop  |
| Confirm VCC database access method — API or Snowflake data share  | Sandeep  | Before architecture workshop  |
| Confirm whether OI 3.0 needs its own Snowflake instance — provision via CloudLaunch if so  | Sandeep + infra  | Before architecture workshop  |
| Invite Joanna or Raema to next technical session to align output format with pipeline design  | Michelle  | Before architecture workshop  |
| Validate Microsoft Foundry against Bain's approved platform list and Andromeda scope  | Sandeep + Siva  | Architecture workshop Day 2  |
| Confirm ThinkCell licence ownership and whether VCC's integration is shareable with OI 3.0  | Sandeep  | Architecture workshop Day 3  |
| Produce explicit mapping — which calculations live in VCC vs. OI 3.0's engine  | Sandeep + Kasia  | Architecture workshop Day 3  |
| Design data isolation enforcement — prevent red data from leaking or being used for training  | Siva + StatusNeo  | Architecture workshop Day 2  |
| Design audit log — inputs, outputs, and metadata captured per deck generated  | Siva + StatusNeo  | Architecture workshop Day 2  |

Here’s the transcript and zoom recording from Zoom:

**Recording**

|  | Duration: 00:40:53 Shareable link: [https://bain.zoom.us/rec/share/_zEx_VagGrlk6E2n50iAaaxhCy1OUQKyOxBQnUIfmK2MCAV1OsMk5c6Qs3UnlY7p.eEQ_YRNRDT8LyK-w](https://urldefense.com/v3/__https:/bain.zoom.us/rec/share/_zEx_VagGrlk6E2n50iAaaxhCy1OUQKyOxBQnUIfmK2MCAV1OsMk5c6Qs3UnlY7p.eEQ_YRNRDT8LyK-w__;!!AbgBjg!xw4r7Pn2fHNdKYn4FuwqasMCN23PkPvIhQ6VOwQphFLGf2D1OAllsO2fF4w-e3-jOwvPpLeKfTvcvQZ0P0A$) Passcode: %76U=y49 [View in Zoom](https://urldefense.com/v3/__https:/bain.zoom.us/launch/hub?type=recording&mid=lvvSzPQvQ*2F6l0WS7J1*2BAeA*3D*3D&origin=https*3A*2F*2Fbain.zoom.us*2Frecording*2Fdetail*3Fmeeting_id*3DlvvSzPQvQ*252F6l0WS7J1*252BAeA*253D*253D__;JSUlJSUlJSUlJSUlJSUl!!AbgBjg!xw4r7Pn2fHNdKYn4FuwqasMCN23PkPvIhQ6VOwQphFLGf2D1OAllsO2fF4w-e3-jOwvPpLeKfTvcVcfMTSs$)  |

**Meeting summary**

## Quick recap

This meeting focused on discussing the VC-C project architecture and technical approach for building an opportunity indicator system. Sandeep explained that the project would leverage existing VC-C infrastructure while adding new capabilities, including the use of tools like DuckDB and ZVEC for in-memory database operations and vectorization. The team discussed data sources including CapIQ and LSEG, with CapIQ taking precedence for financial data, and the need to address data matching across different sources. Key technical considerations included building a dynamic workflow engine rather than hard-coding processes, implementing a calculation engine for new analytics, and ensuring proper data structure and governance. The discussion covered data refresh strategies, handling confidential information, and the need for auditability in the system. The team also addressed the importance of understanding business requirements and non-functional needs, with plans for follow-up sessions to review calculations and explore current processes with the BCN team.

## Next steps

### Kasia

- Schedule a follow-up session with Jason to review the calculations from the VC\C site.
- Organize sessions to show the current Tableau dashboard and Excel used for opportunity indicators.
- Add bullets to Confluence regarding data handling framework and data classification.
- Ensure team receives access instructions by email by the end of the day.

### Sandeep

- Get access to the VC\C database for the team and explore sharing the database in Snowflake.
- Run an agent on the VC\C team chat to extract calculation details and share with the team.
- Confirm today whether Glean is handling the fetching of LSEG analyst reports.

### Siva

- Design the data structure to handle industry taxonomy matching between CapIQ and Bain.
- Think through and design the data refresh schedule and data recency/availability handling.

### Collaboration

- Team (led by Kasia/Sandeep): Have a session with Akhil (BCN team) to discuss current process, calculations, and data refresh tolerance.
- Team: Start thinking through and identifying libraries/tools for the data pipeline and AI agents.
- Team: Prepare for architectural workshops to design the system for scalability beyond MVP.

## Summary

### VC^C Project Technical Overview

Sandeep presented on the VC^C project, explaining how it differs from opportunity indicators (OI) by focusing on value creation from companies through data analysis and reporting. He outlined technical approaches including the use of DuckDB and ZVEC for in-memory database operations, and emphasized the importance of building a flexible calculation engine from the start rather than hard-coding workflows as done in the existing VC^C system. Sandeep also highlighted the need to implement proper data dating and quality management systems, noting that while the initial project will focus on batch processing rather than real-time operations, AI integration for data quality checks will be important for future scalability.

### AI Schema Knowledge Base Planning

Sandeep explained that the team needs to build a schema knowledge base for the AI agent to access data from DuckDB, starting with company-level data but eventually expanding to industry-level data. He emphasized the complexity of data management, particularly the need to align CapIQ's industry taxonomy with Bain's taxonomy. Sandeep mentioned that Siva will help design the data structure, and he will facilitate connections with data sources including CapIQ and potentially LSEG through Sage. Kasia noted that analyst reports from LSEG would also be relevant, though it's unclear if Glean will handle this data.

### Risk Register Data Challenges

The team discussed challenges with building a risk register, particularly around data refresh schedules and data source dependencies. Kasia highlighted concerns about data refresh timing and partner data uploads potentially overwriting information, while Siva noted that the project would address both data recency and availability issues. Sandeep emphasized the need to involve Joanna or Rhea to determine specific AI output requirements and suggested starting to build smaller pipeline components while exploring available libraries to streamline the process.

### Data Structure and Front-End Design

Sandeep emphasized the importance of establishing a strong data structure, expressing concern that future issues could arise if the data structure is not properly designed. He demonstrated how VC-C's front-end works by showing its functionality with company data and explained that their project could leverage existing data calculations from VC-C, including charts and company briefs. Sandeep also mentioned that the chat feature could be expanded to include both the selected company and its peer set, and that ThinkCil would be used to generate PPTs based on user requests. Nikolozi asked about the calculation front, and Sandeep confirmed that it uses Bain's partners' custom adjustment logics.

### Peer Set Data Calculation Strategies

Sandeep explained that peer set calculations can be obtained through either OpenAI or Claude APIs, though this approach carries certain risks. He detailed an alternative strategy using CAP-IQ data, which provides trusted company information including peer sets, subsidiaries, and matching capabilities. Sandeep noted that while CAP-IQ data is being used as the primary source, there remains a challenge of matching company names across different datasets, which will require further discussion.

### Data Calculations and VCcc Integration

The team discussed data calculations and integration with VCcc, where Kasia noted that some price calculations from current OIs may not be properly looped in the VCrastructure system. Sandeep confirmed they will develop their own calculation engine since some calculations will differ from what's happening in VCcc. The discussion also covered how the system currently works with company data through API calls and database access, with plans to potentially share VCcc's database in Snowflake for batch processing.

### Opportunity Size Calculation Process Review

The team discussed plans for a session with Akhil to review current processes for calculating opportunity sizes and walk through existing Excel calculations from a previous September session. Kasia noted they need to verify if the previous calculations are still accurate and address questions about data refresh tolerance and current data lag. Dipesh raised concerns about auditability and data storage, particularly regarding how to handle data changes and ensure accuracy without real-time data processing. The discussion ended with an unresolved question about CAP IQ's data refresh rate.

### CapIQ Data Source Prioritization

Sandeep clarified that CapIQ data should take precedence over other sources for financial information, and explained that real-time data consumption is only needed during specific steps in the private equity business lifecycle. Kasia discussed the need to develop a framework for handling confidential data, including classification and prevention of external exposure, while Nikolozi raised questions about data source prioritization and conflict resolution. Sandeep addressed these concerns by establishing that CapIQ would be the primary source for financial data and that different data sources would cover distinct data types, with the main challenge being company identification across sources rather than data conflicts.

### Data Pipeline Project Planning

The team discussed a data pipeline project that will be implemented in two parts: a traditional data pipeline for making data available to agents, and a second part focused on extracting and processing data to create user outputs. Kasia announced several follow-up sessions scheduled for the next day, including reviews of calculations and current Tableau dashboards, with the possibility of adjusting the timeline if needed. The team clarified that for the MVP, data will be uploaded manually by partners rather than integrated with a CRM system, though future phases may include additional data sources and integrations. Sandeep explained his preference for using Microsoft Foundry for workflow management and agent hosting due to its built-in governance and connectivity options with SharePoint and Outlook.
