# Open questions

Questions the OI 3.0 documentation does not currently answer. Add to this file rather
than guessing; remove an entry when the mirror answers it.

Each entry: what is unknown, why it matters, who can answer, and what is blocked.

## Undocumented architecture areas

Of 71 pages, **54 carry text, 7 hold only an attachment or diagram, and 10 are genuinely
empty.** The distinction matters: an attachment-backed page is documented, just not in
prose, while an empty page means the decision has not been written down anywhere.

**Corrected 2026-09-02.** Earlier counts said 13 empty. Three of those — GLS Feature Set,
Sprint 1 stories, and Bain Taxonomy Mapping — were never empty; their content was
attached as Office files that the sync was dropping. Do not treat a bare page as
undocumented without checking `confluence/_attachments/<page_id>/`.

### Written nowhere — no text, no diagram

**These are the material gaps.** Every one of the high-level design pages the Tech Lead
reviews against is blank. Reviews in these areas rest on judgment, not policy.

| Area | Why it matters | Blocks |
| ---- | -------------- | ------ |
| [Security Design](../confluence/oi30/architecture/opportunity-indicator-architecture-high-level/security-design-processing-ai-and-data-19705167996.md) | No written control set for processing, AI, or data | Security review of any SN PR touching auth or data handling |
| [NFR Design Choices](../confluence/oi30/architecture/opportunity-indicator-architecture-high-level/nfr-non-functional-design-choices-19704905798.md) | No performance, availability, or scale targets | Judging whether an implementation meets the 30-minute end-to-end goal |
| [Observability & Monitoring](../confluence/oi30/architecture/opportunity-indicator-architecture-high-level/observability-logging-notification-monitoring-design-19705430028.md) | No logging or alerting standard | Reviewing instrumentation in SN code |
| [Endpoints & Interfaces Design](../confluence/oi30/architecture/opportunity-indicator-architecture-high-level/endpoints-interfaces-design-19704938600.md) | No API contract standard | Reviewing FastAPI surface changes |
| [Deployment Design (CI/CD)](../confluence/oi30/architecture/opportunity-indicator-architecture-high-level/deployment-design-ai-compute-data-components-cicd-19705233507.md) | No documented pipeline or environment topology | Release and rollback decisions |
| [LSEG](../confluence/oi30/data-requirements/data-sources-summary/lseg-19618889872.md) | Integration undocumented, unlike its sibling sources | LSEG integration review |
| [Jobs to be done](../confluence/oi30/overview/jobs-to-be-done-19619577898.md) | Feature trade-offs lack a stated yardstick | Prioritisation calls |

Three further empty pages — [Architecture](../confluence/oi30/architecture-19589234692.md),
[Overview](../confluence/oi30/overview-19618758834.md), and
[Roadmap / Business Requirements](../confluence/oi30/roadmap-business-requirements-19588546617.md)
— are parents whose children hold the content. Those are structural, not gaps.

### Documented as an attachment or diagram only

Content exists but carries no prose, so it will not turn up in a search. Open the file.

| Page | Attachment |
| ---- | ---------- |
| [Technical Architecture](../confluence/oi30/architecture/technical-architecture-19619479668.md) | `OI_3_0_Technical_Architecture_v2.svg` |
| [Data Architecture](../confluence/oi30/architecture/data-architecture-19619840013.md) | `OI_3_0_Data_Architecture.svg` |
| [Logic Architecture](../confluence/oi30/architecture/logic-architecture-19619840005.md) | `OI_3_0_Technical_Architecture.svg` (the logical view, despite the name) |
| [GLS Feature Set](../confluence/oi30/gls-feature-set-19761725586.md) | `OI_3.0_Feature_Overview_1.pptx` |
| [Sprint 1 stories](../confluence/oi30/mvp-sprint-map/sprint-1-stories-dependencies-and-decisions-19763003424.md) | `OI3-Sprint_1_planning.xlsx` |
| [Success metrics](../confluence/oi30/overview/success-metrics-19618758856.md) | `image-20260712-213758.png` |
| [Onboarding tracker](../confluence/oi30/ways-of-working/onboarding-statusneo/onboarding-tracker-19705593880.md) | `image-20260807-111345.png` |

Attachments live in `confluence/_attachments/<page_id>/`. A diagram or spreadsheet cannot
state a threshold or a rule precisely, so where one is the sole source for a decision,
confirm the reading before relying on it.

Other substantive attachments now mirrored, not tied to an empty page: the OI data
dictionary (v1 and v2), `VCC_Calculations.xlsx`, `Industry_Map.xlsx`, the levers library,
cost bar breakdown examples, `A1OI_companies_2025.csv`, and the onboarding and kick-off
decks.

## Undocumented, and asked about

| Question | Status |
| -------- | ------ |
| **Repository structure** — monorepo versus repo-per-service | No page in the space mentions it. Recommendation in `decisions/001` |
| **Can Glean/IRIS fetch LSEG analyst reports under Bain's existing entitlement?** | Action on Sandeep from the [VCC Overview meeting](../confluence/oi30/meeting-summaries/vcc-overview-meeting-19696746551.md), 4 Aug, due before the architecture workshop. No answer recorded. It is the cheapest possible resolution to the LSEG AMBER flag — see [data-source-map.md](data-source-map.md) §5.4 |
| **Do consensus revenue-growth estimates come from CapIQ or LSEG?** | The [Data Sources summary](../confluence/oi30/data-requirements/data-sources-summary-19619676163.md) attributes consensus estimates to LSEG; the [VCC Calculations summary](../confluence/oi30/roadmap-business-requirements/vcc-calculations-summary-19699040301.md) builds projected revenue growth on "analyst consensus forecasts" via a CapIQ platform. Decides whether the LSEG restriction touches a sized opportunity or only qualitative surfaces. Akhil or Sandeep can answer in a line |
| **Glean / Iris sandbox access** — owner and date | Marked only as "(sandbox access TBD)". All 14 Screen 04 sub-levers draw their Bain experience range from Iris/Sage, five with no peer benchmark at all. Larger functional exposure than LSEG, tracked as a parenthetical |
| ~~What GLS actually is~~ | **Answered by the Tech Lead 2026-08-31:** the Global Leadership Summit, mid-to-late October, where OI 3.0 is demonstrated. The [GLS Feature Set](../confluence/oi30/gls-feature-set-19761725586.md) page carries `OI_3.0_Feature_Overview_1.pptx` but no prose — the date and demo scope should be written on the page itself |

## Conflicts to resolve

| Conflict | Detail |
| -------- | ------ |
| ~~Two different architectures~~ | **Resolved.** Architecture Layers documents two deliberate consumption patterns over one headless layer: deterministic via FastAPI, open-ended via FastMCP/MCP. The React app and the agent swarm are both clients, not rival designs |
| ~~Two different AI SDKs~~ | **Resolved by ADR-008:** Microsoft Agent Framework, with Foundry Workflows and Prompt flow rejected on cited retirement dates. Technical Stack and the architecture diagram are stale and should be marked superseded |
| **Hosting: resolved, but inconsistently** | Technology Choices sets an Azure-first rubric with Azure Front Door; the technical architecture diagram still lists Bedrock / Vertex / MS Foundry. The page is newer and more specific — the diagram should be corrected |
| **Data acquisition: real-time or batch** | [Technology Choices](../confluence/oi30/architecture/opportunity-indicator-architecture-high-level/technical-stack/technology-choices-19751338017.md) gives MVP as "Real-time fetch per run", moving to monthly batch at north star, and marks that a *mechanism change*. The [VCC Overview meeting](../confluence/oi30/meeting-summaries/vcc-overview-meeting-19696746551.md) recorded the opposite as a decision: "Batch processing only — no real-time data in OI 3.0 under any circumstances." Both are current |
| **Security split exists only in a diagram** | The app-level (StatusNeo) vs infra-level (Bain) RACI is drawn in the technical architecture SVG but written on no page, including the empty Security Design page |

## Product and scope

| Question | Why it matters |
| -------- | -------------- |
| MVP is still "to be signed off" | Scope may move under active development |
| Two per-screen data requirement pages are still marked *update in progress* | Analysis and Output & Deck Builder. **Screen 03 Case for Change dropped the marker on 2026-09-01** and should now be treated as stable |
| ADR-001 to ADR-009 are "Accepted, pending Bain architect review" | Rulings may still change under review |
