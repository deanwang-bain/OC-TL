---
title: "Meeting notes"
confluence_id: 19799244847
confluence_url: https://bainco.atlassian.net/wiki/spaces/OI30/pages/19799244847
version: 1
updated: 2026-09-04T07:43:05.101Z
---

# Meeting notes

[View in Confluence](https://bainco.atlassian.net/wiki/spaces/OI30/pages/19799244847)

1. **Cost bar approach**

- Use the **Bain taxonomy (L1–L4)** as the master structure for cost bar breakdowns, aligned with how content is tagged in IRIS/Glean.
- Start with the **publicly reported company cost structure** and use Bain IP / existing examples to determine the appropriate additional breakdown.
- The level of detail does **not need to consistently reach L4**. We should stop at the level where the breakdown remains meaningful and sufficiently supported by available IP/data.
- For initial development, the team primarily needs representative examples showing **what components sit within each cost bar and the indicative percentage split**.
- Avoid manually extracting large volumes of chart data where this can be automated. The team can explore automated extraction from existing PowerPoint/Excel materials, followed by business validation.

1. **Business units**

- Business units will initially be limited to **publicly reported business segments**.
- We will not create additional product-, channel- or operating-model-level segments where these are not publicly reported, as this would introduce excessive assumptions.
- Where detailed cost information is unavailable for a business unit, the **parent company cost structure can be used as the initial fallback**, with targeted adjustments where relevant sector/IP evidence exists.
- For diversified companies, reported business units may need to be mapped independently to the most relevant Bain industry taxonomy (example: pharma).

1. **Industry taxonomy and mapping**

- The **Bain taxonomy currently being used for the cost-bar work will become the master taxonomy**, particularly for navigating internal content.
- First check whether an existing **CapIQ → Bain taxonomy mapping** already exists across current OI / related workstreams to avoid recreating it.
- Where no mapping exists, we can use **fuzzy/LLM-assisted matching**, followed by business validation for the key sectors rather than manually reviewing every row.
- Validation can be done collaboratively between the business/IP team and BCN resources where required.

1. **Value levers **->* this have changed a bit based on feedback from Stephanie, hence adding here point:*

- Direction agreed for V1 — anchor the primary view around **cost buckets**, with the ability to drill down into the **relevant value levers** and associated opportunity within each bucket.
- **AI transformation** should be explicitly considered given feedback from user interviews.

**Data logic / analysis**

- **Cost bar:** Direction agreed for V1 — anchor the primary view around **cost buckets**, with the ability to drill down into the relevant value levers and associated opportunity within each bucket.
- **Lever split:** Further work is required to define sufficiently granular levers, including industry-specific levers where relevant. An initial direction and examples are sufficient to begin development; the structure does not need to be exhaustive at this stage.
- **Target:** Have an initial point of view ready ahead of the planned **14 September development start**.
- **Triangulation:** Start codifying rules that can be implemented independently of final data access, e.g. when historical years should or should not be used as benchmarks.
- **Contingency:** If IRIS/Glean or analyst-report access becomes a blocker, pivot development capacity towards automating the existing OI calculations, detailed analysis-slide templates and triangulation logic.
- **Case study experience:** Ensure the UX includes the ability to create the **case-study page used in CEO materials**, enabled by Glean.
