# Open questions

Questions the OI 3.0 documentation does not currently answer. Add to this file rather
than guessing; remove an entry when the mirror answers it.

Each entry: what is unknown, why it matters, who can answer, and what is blocked.

## Undocumented architecture areas

Of 95 pages, **76 carry text, 12 hold only an attachment or diagram, and 7 are genuinely
empty.** *(Recounted 2026-10-08.)* **Deployment Design was filled on 7 October**, the
first of the five high-level design pages to move. **Four are still blank.** The distinction matters: an attachment-backed page is documented, just not in
prose, while an empty page means the decision has not been written down anywhere.

Ten pages arrived during the week of 29 September, and the architecture tree was renamed
from *Opportunity-Indicator* to *Opportunity-Catalyst* on 4 October.

**Corrected 2026-09-02.** Earlier counts said 13 empty. Three of those — GLS Feature Set,
Sprint 1 stories, and Bain Taxonomy Mapping — were never empty; their content was
attached as Office files that the sync was dropping. Do not treat a bare page as
undocumented without checking `confluence/_attachments/<page_id>/`.

### Written nowhere — no text, no diagram

**These are the material gaps.** Four of the five high-level design pages the Tech Lead
reviews against are blank. Reviews in these areas rest on judgment, not policy.

| Area | Why it matters | Blocks |
| ---- | -------------- | ------ |
| [Security Design](../confluence/oi30/architecture/opportunity-catalyst-architecture-high-level/security-design-processing-ai-and-data-19705167996.md) | No written control set for processing, AI, or data | Security review of any SN PR touching auth or data handling |
| [NFR Design Choices](../confluence/oi30/architecture/opportunity-catalyst-architecture-high-level/nfr-non-functional-design-choices-19704905798.md) | No performance, availability, or scale targets | Judging whether an implementation meets the 30-minute end-to-end goal |
| [Observability & Monitoring](../confluence/oi30/architecture/opportunity-catalyst-architecture-high-level/observability-logging-notification-monitoring-design-19705430028.md) | No logging or alerting standard | Reviewing instrumentation in SN code |
| [Endpoints & Interfaces Design](../confluence/oi30/architecture/opportunity-catalyst-architecture-high-level/endpoints-interfaces-design-19704938600.md) | No API contract standard | Reviewing FastAPI surface changes |
| ~~Deployment Design (CI/CD)~~ | **Resolved 2026-10-07.** Now carries three environment diagrams and a child page, the [OC Dev-Staging (GLS) Deployment Tracker](../confluence/oi30/architecture/opportunity-catalyst-architecture-high-level/deployment-design-ai-compute-data-components-cicd/oc-dev-staging-gls-deployment-tracker-19909279789.md), which is the most operationally specific page in the space. **The page itself is still images only** — the written topology is in the child tracker | — |
| ~~LSEG~~ | **Partly resolved 2026-09-17.** The page now links example 10-K filings and a "10-K mapping (AMS)" tab in the OpCat end-to-end data map. Both are SharePoint, so outside the mirror, and the **persistence restrictions ADR-007 must enforce are still not written down** | Finding S6 of the ADR review stands |
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
| [Architecture Assessment Tracker](../confluence/oi30/architecture/architecture-assessment-tracker-19853082681.md) | `OppCat_Architecture_Assessment_Tracker_Reviewed.xlsx` and `AI_Architecture_Requirements_v2.1.xlsx` — **313 requirements, 249 of them MUST, with every response column empty.** See the brief |

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

## Conflicts to resolve

| Conflict | Detail |
| -------- | ------ |
| ~~Two different architectures~~ | **Resolved.** Architecture Layers documents two deliberate consumption patterns over one headless layer: deterministic via FastAPI, open-ended via FastMCP/MCP. The React app and the agent swarm are both clients, not rival designs |
| ~~Two different AI SDKs~~ | **Resolved by ADR-008:** Microsoft Agent Framework, with Foundry Workflows and Prompt flow rejected on cited retirement dates. Technical Stack and the architecture diagram are stale and should be marked superseded |
| **Hosting: resolved, but inconsistently** | Technology Choices sets an Azure-first rubric with Azure Front Door; the technical architecture diagram still lists Bedrock / Vertex / MS Foundry. The page is newer and more specific — the diagram should be corrected |
| ~~OpenAI named as the peer-search model~~ | **Answered 2026-09-21 by the engineering pages.** [Present working — Technical details](../confluence/present-working-technical-details-19849609338.md) shows the agent branch calling `foundry.ask_agent` — twice per discovery, plus one call per analysed peer. So "GenAI" is **Azure AI Foundry**, which Technology Choices already records as *Adopt*. No third-party provider conflict remains. **What is still unanswered is narrower: which model Foundry is configured to serve, and whether those calls traverse the API Management GenAI gateway** that §7 makes the single egress point |
| **Web search is `serpapi`, and it has no position** | [Future Scope](../confluence/future-scope-with-ai-search-19849412714.md) states plainly that "web search runs through a **serpapi engine**". serpapi is a commercial third-party search API: target-company names leave Bain to a vendor that appears in **no position table, no ADR and no data source catalogue**. This is the sharpest open third-party question in the space |
| **Azure AI Search is built, and §4.2 still forbids it** | §4.2 decided *"do not add a vector store at MVP or at north star"*, with one revisit trigger: *"measured retrieval quality against a fixed evaluation set, not a hunch"*. The [Document Upload architecture](../confluence/oi30/architecture/document-upload-indexing-and-parsing-with-real-time-progress-architecture-19899351139.md) (4 October) marks itself **Authoritative** and records `srch-oi-dev-gwc-nonprod-1` as **EXISTS** — Basic tier, 2 replicas, Entra-only auth — with `idx-case-documents` to be created. The team was granted access on the last day of Sprint 2. **Technology Choices is still version 1, dated 21 August, and §4.2 is unchanged.** This is no longer a question of whether to revisit; the architecture moved and the ruling page did not follow |
| **Event Grid contradicts §6 of Technology Choices** | §6 chose Service Bus explicitly — *"Service Bus and not Event Grid or Storage Queues"*. The Future Scope pipeline routed the new-file event through **Event Grid → queue**. The newer Document Upload page uses **Service Bus** (`document-upload` and `document-ingest` queues with dead-lettering), so the authoritative design now agrees with §6. Future Scope was not retracted, so the two proposals still disagree with each other |
| **The embedding model is a self-hosted container with no position** | Germany West Central cannot host Azure models, so embeddings run as a Container App inside the environment, weights baked into the image, model *"to be chosen"* after a top-n evaluation. Packaging is explicitly either an off-the-shelf server image — **Hugging Face text-embeddings-inference is named** — or a governed wrapper. This is a Build/Adopt decision with licence and provenance consequences, and it appears in no position table |
| **Two product names are live** | The architecture tree was renamed to **Opportunity-Catalyst** on 4 October and the repos are `nextgen-opportunity-catalyst-*`, while the space key and many pages still say Opportunity Indicator. **The Jira board is `OI3` throughout** — see the naming note in `CLAUDE.md` for the `OC3` mislabelling in the Sprint 1 deck |
| **Security split exists only in a diagram** | The app-level (StatusNeo) vs infra-level (Bain) RACI is drawn in the technical architecture SVG but written on no page, including the empty Security Design page |
| **`gpt-5.2` and `gpt-4.1` are now named, and they set the region** | The Foundry project `poc-swc-oi-sweden-test` serves both. Agents run in **Sweden Central** rather than Germany West Central *solely because gpt-5.2 is offered there and not in Germany* (owner, 2026-10-01). That is a model choice driving a residency split, and neither model appears in a position table. The China assessment separately records that OpenAI-backed features must be off in Greater China |
| **GLS will demo on a POC Foundry resource** | Both the dev and the planned staging Foundry projects sit under the account `poc-swc-oi-sweden-test`. The deployment tracker (Q11) accepts this "for now" and plans "a proper non-poc account before the partner rollout". Worth confirming the POC resource carries production quota and support before it is what the demo runs on |
| **No latency budget, with a live streaming design** | The chat-assistant architecture now specifies two separate SSE streams, and the ingestion design says a 200-page filing "takes minutes". The 30-minute end-to-end claim still has no written budget anywhere, and the NFR page is still blank |

## Housekeeping

| Item | Detail |
| ---- | ------ |
| **Six pages now sit outside the tree** | [Peer Selection Capability](../confluence/peer-selection-capability-19809534070.md), [Present working — Technical details](../confluence/present-working-technical-details-19849609338.md), [Future Scope — With ai search](../confluence/future-scope-with-ai-search-19849412714.md), [Cost Bar & Normalization methodology](../confluence/cost-bar-normalization-methodology-19888046107.md), and two pages literally titled *to be delete* ([19848954023](../confluence/to-be-delete-19848954023.md), [19849445516](../confluence/to-be-delete-19849445516.md)). Between them they hold the most detailed implementation and design-rationale content in the space, and none of it appears in the page hierarchy |
| **Two pages titled "to be delete" hold real content** | Both are earlier drafts of the two engineering pages — `19849445516` carries the Design decisions and Benefits prose that the Future Scope page now presents cleanly; `19848954023` carries the LLM-resolution walkthrough. They are not scratch. If they are deleted as their titles promise, confirm the content survived into the successor pages first; the mirror will keep a copy either way |
| **Future Scope was superseded but not retracted** | The 4 October Document Upload page marks itself *Authoritative* and differs from [Future Scope](../confluence/future-scope-with-ai-search-19849412714.md) on the broker (Service Bus, not Event Grid) and on where embeddings run (a self-hosted container, not `text-embedding-3-small`). Future Scope carries no superseded marker, so a reader can still land on the older design |
| **Sprint 3 planning is nine video files** | The [planning session](../confluence/oi30/meeting-summaries/sprint-3-planning-session-19875168265.md) is recorded as nine `.mp4` parts totalling roughly 91 MB, now committed to this repo, with no written summary. Decisions taken in that session are not searchable and not reviewable without watching two hours of video. Worth asking for written notes; worth also deciding whether the mirror should download video at all |

## Product and scope

| Question | Why it matters |
| -------- | -------------- |
| MVP is still "to be signed off" | Scope may move under active development |
| ~~Per-screen data requirements unstable~~ | **Resolved.** All six screens dropped the *update in progress* marker — Screen 03 on 2026-09-01, Screens 04 and 05 during the week of 2026-09-08. Treat the whole set as stable |
| **CapIQ API access is still unavailable** | [Peer Selection Capability](../confluence/peer-selection-capability-19809534070.md) works around it for sprints 1 and 2 using CapIQ *Excel extracts* converted to Parquet. The rate-limit question is deferred, not answered |
| ~~Peer selection weights are illustrative~~ | **Changed 2026-09-20.** Users may now prioritise buckets; unselected criteria are deprioritised rather than ignored. Weights are defaults, not fixed |
| ~~Sprint 1 closed at 44%~~ | **Superseded by Sprint 2.** 48 of 58 items (**83%**), 36 of 45 committed, scope growth down from ~127% to 29%, carryover down from 28 to 10. See the brief |
| **Five items have now been open since Sprint 1** | OI3-21 security and governance, OI3-27 architecture decision records, OI3-48 development environment and access, OI3-54 think-cell licence, OI3-82 rate and quota management. The Sprint 2 retro asks for a named owner and a date on each, or a decision to close |
| **AI platform access arrived on the last day of Sprint 2** | AI Search and document parsing — the services the peer-selection cycle depends on — were granted on the final day, which is why over half the sprint's closure landed in the last three days. The retro's own fix is to raise platform access a sprint ahead of the work |
| **Three data foundation items left the sprint rather than completing** | OI3-18, OI3-43 and OI3-65 were moved to the general backlog. The retro flags they "still require close follow-up to not become another blocker for the GLS scope", and nobody has confirmed where they now sit |
| ~~No estimates in Jira~~ | **Fixed from Sprint 3.** The team estimated in hours while the board was configured for story points, and changing it needed admin access. Hours are being entered before Sprint 3 starts, so burndown and velocity become usable for the first time |
| **The ARC architecture assessment is unanswered** | [Architecture Assessment Tracker](../confluence/oi30/architecture/architecture-assessment-tracker-19853082681.md), published 22 September, carries **313 requirements across two frameworks (ARC v2 and AI Architecture v2.1), 249 of them MUST, with zero responses recorded.** The reviewer pass reclassified priorities; nobody has answered a single requirement |
| **Mainland China is out of scope, but not written as such** | [Opportunity Catalyst in Greater China](../confluence/oi30/roadmap-business-requirements/opportunity-catalyst-in-greater-china-19853082640.md) concludes mainland is blocked and Hong Kong needs case-by-case clearance. The recommendation is to record mainland as an **explicit scope exclusion** for the demo and MVP — that has not been done on any scope page |
| ADR-001 to ADR-009 are "Accepted, pending Bain architect review" | Rulings may still change under review |
