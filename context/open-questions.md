# Open questions

Questions the OI 3.0 documentation does not currently answer. Add to this file rather
than guessing; remove an entry when the mirror answers it.

Each entry: what is unknown, why it matters, who can answer, and what is blocked.

## Undocumented architecture areas

Of 77 pages, **60 carry text, 7 hold only an attachment or diagram, and 10 are genuinely
empty.** *(Recounted 2026-09-15.)* Six pages were added during September and the empty
set did not shrink by one: the same ten pages are still blank, including all five
high-level design pages. The distinction matters: an attachment-backed page is documented, just not in
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
| ~~Bain Taxonomy Mapping~~ | **Resolved September.** The page now carries text plus `Bain_Taxonomy_-_Cost_bar_reference.xlsx`, and the [cost bar meeting notes](../confluence/oi30/data-requirements/cost-bar-split/meeting-notes-19799244847.md) make the Bain L1–L4 taxonomy the master structure | — |
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
| ~~What GLS actually is~~ | **Answered by the Tech Lead 2026-08-31:** the Global Leadership Summit, mid-to-late October, where OI 3.0 is demonstrated. The [GLS Feature Set](../confluence/oi30/gls-feature-set-19761725586.md) page carries `OI_3.0_Feature_Overview_1.pptx` but no prose — the date and demo scope should be written on the page itself |
| **"BAP" — raised 2026-09-17 by an external team (BAP LT / PEG) asking how much of OI 3.0 ("OC") will be built on it, and whether the VCC MCP server will be deployed via it** | The string "BAP" appears nowhere in the mirror. The only Bain agent-hosting platform documented anywhere in the space is [Andromeda](../confluence/oi30/ways-of-working/onboarding-statusneo/andromeda-bains-agentic-ai-platform-19691733117.md) — "Bain's internal platform for building, deploying, and operating AI agent solutions" — and Microsoft Foundry is separately named as the preferred *orchestration* platform in the [VCC Overview meeting](../confluence/oi30/meeting-summaries/vcc-overview-meeting-19696746551.md). Whether "BAP" is a rename of Andromeda, a distinct platform, or a team-specific abbreviation is unknown from written sources. Needs a ruling on which name is current before answering the external question or writing it back to Confluence |
| **Enumerated taxonomy of distinct agent types and their individual data access/scope** | No page names discrete agent types (e.g. "peer discovery agent", "financial analysis agent") with a stated tool/data grant per type. The architecture pages describe a single generic "AI agent" / "agent swarm" pattern that reaches data only through governed API/MCP tool calls ([Opportunity-Indicator Architecture (high Level)](../confluence/oi30/architecture/opportunity-indicator-architecture-high-level-19705397258.md), [Logical Application Flows](../confluence/oi30/architecture/opportunity-indicator-architecture-high-level/logical-application-flows-19705135241.md)) — access is governed at the tool/capability layer, not documented per named agent |

## Conflicts to resolve

| Conflict | Detail |
| -------- | ------ |
| ~~Two different architectures~~ | **Resolved.** Architecture Layers documents two deliberate consumption patterns over one headless layer: deterministic via FastAPI, open-ended via FastMCP/MCP. The React app and the agent swarm are both clients, not rival designs |
| ~~Two different AI SDKs~~ | **Resolved by ADR-008:** Microsoft Agent Framework, with Foundry Workflows and Prompt flow rejected on cited retirement dates. Technical Stack and the architecture diagram are stale and should be marked superseded |
| **Hosting: resolved, but inconsistently** | Technology Choices sets an Azure-first rubric with Azure Front Door; the technical architecture diagram still lists Bedrock / Vertex / MS Foundry. The page is newer and more specific — the diagram should be corrected |
| **OpenAI named as the peer-search model** | [Peer Selection Capability](../confluence/peer-selection-capability-19809534070.md) specifies *"OpenAI-powered search"* to identify peer candidates. Technology Choices sets an **Azure managed-first** rubric with **Azure AI Foundry** for models and a gateway through which *"every model call passes"*; ADR-008 selects **Microsoft Agent Framework**. OpenAI appears in no technology table and in `tools/known_tools.json` not at all. It also sits against the Andromeda note that the model gateway means *"no data leaving Bain"* |
| **Web search as a data fallback** | The same page triggers web search where CapIQ lacks a field. Not in any technology position table, and it puts target-company queries to an external service |
| **Security split exists only in a diagram** | The app-level (StatusNeo) vs infra-level (Bain) RACI is drawn in the technical architecture SVG but written on no page, including the empty Security Design page |

## Housekeeping

| Item | Detail |
| ---- | ------ |
| **An orphan page sits outside the tree** | [Peer Selection Capability](../confluence/peer-selection-capability-19809534070.md) is filed at the space root rather than under OI3.0, so it does not appear in the page hierarchy alongside the rest. Worth moving — it is the most detailed implementation spec in the space |

## Product and scope

| Question | Why it matters |
| -------- | -------------- |
| MVP is still "to be signed off" | Scope may move under active development |
| ~~Per-screen data requirements unstable~~ | **Resolved.** All six screens dropped the *update in progress* marker — Screen 03 on 2026-09-01, Screens 04 and 05 during the week of 2026-09-08. Treat the whole set as stable |
| **CapIQ API access is still unavailable** | [Peer Selection Capability](../confluence/peer-selection-capability-19809534070.md) works around it for sprints 1 and 2 using CapIQ *Excel extracts* converted to Parquet. The rate-limit question is deferred, not answered |
| **Peer selection weights are illustrative** | The six-bucket weights are marked directional, and user-set custom weights are explicitly *"not to be allowed now"*. Expect them to move before they are final |
| ADR-001 to ADR-009 are "Accepted, pending Bain architect review" | Rulings may still change under review |
