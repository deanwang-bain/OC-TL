# OI 3.0 / OC 3.0 — Tech Lead brief

Distilled from the OI30 mirror. Every claim links to its source page. When this
disagrees with `confluence/`, the mirror wins — and this file needs updating.

## Naming: the product is now Opportunity Catalyst

As of September the artefacts say **Opportunity Catalyst (OC 3.0)**, not Opportunity
Indicator. The Jira board is **OC3** and tickets are **OC3-nn**
([Sprint 1 Retrospective](../confluence/oi30/sprint-1-retrospective-19838042157.md));
the new [Data Source Catalogue](../confluence/oi30/architecture/data-architecture/data-source-catalogue-19839025154.md)
speaks of "Opportunity Catalyst data" and its workbook is "OpCat end-to-end data map".

The Confluence space key is still `OI30` and most older pages still say Opportunity
Indicator, so **both names are live**. This repository's own name, OC-TL, matches the
new one. No page announces the change, so treat it as observed rather than ruled.

## The product

An AI-powered tool helping Bain partners prepare for client conversations. It automates
research, benchmarking, and deck creation that today takes a team of COEs and
consultants **2–3 days**, compressing it to **roughly 30 minutes**, so a partner walks
into a CEO meeting confident.
([Vision](../confluence/oi30/overview/vision-19617939629.md),
[Persona](../confluence/oi30/overview/persona-19618758842.md))

Beyond the MVP it is envisaged as an ongoing portfolio tool: after a partner exports a
deck, it keeps monitoring peers for earnings, news, and strategic moves, surfacing an
overnight digest. Whether that lives here or in Cortex is undecided.

## Constraints that drive technical decisions

These are product commitments with direct architectural consequences. Treat a change
that erodes one as significant, not cosmetic.

1. **Transparency is mandatory.** A partner must be able to drill into any number and
   see data sources, confidence levels, and reasoning. Every calculation path needs to
   carry provenance — this cannot be retrofitted.
2. **Non-linear and modular.** Adjusting peers or context mid-analysis must rerun *only
   affected modules*. This demands real dependency tracking between analysis steps.
3. **Hard gates and soft gates.** Hard gates block until the partner resolves something
   critical (e.g. uploading financials for a private company); soft gates proceed while
   flagging lower confidence. Gate behaviour is product logic, not UI polish.
4. **Partner retains judgment.** *"AI as enabler, not decision-maker."* Partners are
   accountable for what reaches clients.
5. **Client-ready export.** PPT in Bain / ThinkCell format.

Known friction being designed against: existing tools are too linear, offer no
reasoning visibility, and leave a trust gap on numbers.

## Architecture as drawn

The three architecture diagrams carry far more detail than any text page, and some of
it does not match the written pages. They are the most authoritative statement of the
design that currently exists. Read them directly — they are SVGs, so their labels are
searchable:

- `confluence/_attachments/19619479668/OI_3_0_Technical_Architecture_v2.svg`
- `confluence/_attachments/19619840013/OI_3_0_Data_Architecture.svg`
- `confluence/_attachments/19619840005/OI_3_0_Technical_Architecture.svg` (the *logical*
  view, despite the filename)

What they establish:

**The system is an agent swarm, not a conventional web app.** A Claude SDK orchestrator
plans agent calls and streams SSE to a chat-first UI. Named agents: Research,
IP-Retrieval, Benchmark, SoP Composer, Skeptic, Persona, Slide Composer, VoiceApply,
3-Takeaway Optimizer. A sector micro-swarm router lazy-loads a different agent stack per
sector — the diagram notes *"shallow-across-all-sectors is impossible"*.

**The security RACI is a band split in the diagram.** StatusNeo owns **app-level**
security (authN/Z at the boundary, guardrails, provenance hooks, secure SDLC); Bain owns
**infra-level** security (VPC, IAM/KMS, IdP, SIEM, retention), validated via TRA →
Archie. This is the only place that division is written down.

**Three-tier knowledge isolation.** Public → Partner-Private → Firm-Shared, with
one-way reads and a KM-controlled Curation Gate for opt-in promotion. Partner-Private is
session-scoped, *"evaporates on close"*, and carries *"no training w/o opt-in"*.
Per-Partner LoRA adapters have *"no cross-Partner flow"*.

**VCC is a hard dependency with a hard rule.** The VCC deterministic data plane is
Umbrage-owned and *"consumed at runtime for canonical calc only — never re-derived"*.
The diagram marks the VCC runtime API/MCP a *"critical-path dependency"* and notes
*"runtime vs batch determines dynamism"*. Mitigations shown: a thin swappable adapter, a
contract-first data-package schema, and permanent CI stubs plus outage-resilience tests.

**Gates are services, not UI.** A pre-flight gate service (conflict-of-interest engine,
blocked-target list, data-residency router) runs before agents; an Eval Gate service
runs pre-render with an explicit fail→loop back to the agents.

**State is an append-only event log.** A typed DOM store holds
Deck → Section → Slide → Block → Claim (with `confidence` and `provenance_class`) →
Evidence; *"deck = projection over events"*, which is what makes time-travel, restore,
branch, and promote possible. The diagram calls the DOM *"Bain's IP in
machine-readable form"*.

**A learning pipeline is in scope.** SFT on golden cases, RLVR, and implicit RLHF from
partner edits, reading the event store and writing the per-Partner adapter store.

Hosting is listed as *Bedrock / Vertex / MS Foundry* — three options, so read this as
undecided rather than settled.

## Architecture as written

Cloud-native, **headless** architecture. Technology choices map to distinct capability
layers: client experience, interfaces, deterministic processing, data management,
AI/agent services, security, infrastructure.
([Technical Stack](../confluence/oi30/architecture/opportunity-indicator-architecture-high-level/technical-stack-19704512648.md))

**Frontend** — React 18, TypeScript, Vite, TanStack Query, AG Grid, Apache ECharts,
React Router v6, TailwindCSS, Bain Design System, Okta React SDK, AI SDK (ai-sdk.dev).
Owns navigation, application state, dashboards, grids, visualisations.

**Interfaces** — FastAPI provides deterministic REST for structured workflows,
commands, queries, calculations, and retrieval. AI capabilities are reached through
governed conversational and service interfaces.

**The load-bearing rule:** business rules, authoritative calculations, and core
intelligence are *deliberately kept out of the client*. A PR putting calculation logic
in the frontend contradicts a stated architectural decision — flag it, with this
reference.

Decisions ADR-001 to ADR-009 are **Accepted, pending Bain architect review** (dated
2026-08-21), covering application decomposition, orchestration substrate, and
persistence topology.
([ADRs](../confluence/oi30/architecture/oi-30-architecture-decision-records-19751960620.md))

### The two interface patterns, and how the views reconcile

[Architecture Layers](../confluence/oi30/architecture/opportunity-indicator-architecture-high-level/architecture-layers-19705004106.md)
resolves most of what looked like a contradiction between the written stack and the
diagrams. The client reaches the platform two ways, by design:

- **Deterministic interactions through APIs** (FastAPI) — structured workflows, queries,
  commands, calculations, retrieval.
- **Open-ended interactions through MCP** (FastMCP / MCP servers) — natural-language,
  agent-driven, exploratory.

So the React app and the agent swarm are not competing designs; they are the two
consumption patterns over one headless capability layer. The assistant surface is a
bought component — **AG-UI protocol with CopilotKit** — which is what makes the
"chat-first" framing concrete.

The backend follows **CQRS** with bounded domains, each owning its rules, contracts,
commands, queries and services. Business-critical operations — financial calculations,
transformations, scoring, analytical rules — are **deterministic, version-controlled,
testable services**; agents invoke them through governed interfaces rather than
reproducing calculation logic in the AI layer.

**Still genuinely unreconciled:** the Technical Stack page names **AI SDK (ai-sdk.dev)**
while the technical architecture diagram names the **Claude SDK** as orchestrator. Both
cannot be right. Flag it rather than assuming either.

## Technology choices

[Technology Choices](../confluence/oi30/architecture/opportunity-indicator-architecture-high-level/technical-stack/technology-choices-19751338017.md)
is the most decision-dense page in the space. Status: **Draft for review**.

The governing rubric is **Azure managed services first, custom build only where
genuinely warranted**, resolved into three positions: **Build** (StatusNeo writes and
operates), **Adopt** (Azure managed service plus integration code), **Buy** (existing
Bain or third-party system under licence).

Every choice must survive four tests: **fit, rubric, reversibility, operability.** The
page states the principle worth quoting back in any review — *"A choice with no rejected
alternative is usually a choice that was never made."*

Frontend selections: React + TypeScript + Vite; **Azure Front Door CDN** for static
assets; TanStack Query for server state; **Zustand** for client state; **AG-UI /
CopilotKit** for the assistant surface; **AG-Grid Enterprise** on Bain's existing
licence; **Vega-Lite and Apache ECharts** for exhibits; **Radix** with a Bain-token theme
layer; SSE for streaming; **WCAG 2.2 AA**; i18next, English only at MVP.

Two things to carry into reviews:

- **Hosting is Azure**, not the open Bedrock / Vertex / MS Foundry list in the diagram.
  Where they disagree, this page is newer and more specific.
- **WCAG 2.2 AA is the one hard non-functional target written anywhere.** The NFR page
  is empty, so this is the only NFR with a citable source.

## Testing and release governance

[Agent_Validation_Test_Plan](../confluence/oi30/architecture/agent-validation-test-plan-19765133323.md)
is the most mature governance artefact in the space — an explicit release-governing
reference. Status: **Updated draft for architecture/test-strategy review.**

It runs **two tracks**, because the architecture deliberately mixes deterministic and
probabilistic components: deterministic boundaries get exact assertions; probabilistic
behaviour gets structural invariants, quality metrics, distributions, regression
baselines and human judgement — so model variation does not become false failures.

Objectives OBJ-01 to OBJ-05: structural integrity (every claim has evidence, every
figure has traceability), agent correctness (no fabricated success), groundedness and
faithfulness, regression safety against golden baselines, and deterministic
defensibility (pinned inputs reproduce figures exactly).

Constraints that bind reviews directly:

- **Production documents must never be copied into test environments** — uploads may
  contain MNPI or PII. Synthetic companies for functional tests, recorded responses for
  integration, a pinned snapshot for golden evaluation, masked subsets for warehouse
  validation.
- **MVP protocol boundary:** plain REST over HTTP. gRPC/Protobuf and buf are excluded.
- **IaC validation is out of QA scope** — Terraform, Bicep, PSRule, Checkov belong to the
  deployment/platform team.
- Coverage is explicitly multi-dimensional; code coverage counts only for deterministic
  unit logic.

Its governance note is a good model for this workspace: where the architecture prescribes
no threshold or owner, it defines the measurement method and marks the threshold for
approval **rather than silently inventing policy.**

## Domain model

The backend is organised around the **lifecycle of an opportunity assessment**, not
around screens or technical components
([Domain Architecture](../confluence/oi30/architecture/opportunity-indicator-architecture-high-level/domain-architecture-19705004114.md)):

**Company Universe → Financial & Market Evidence → Indicators & Signals → Peer Context →
Opportunity Assessment → Research & Collaboration → Outputs**

Each domain owns its business rules, data contracts, commands, queries and service
interfaces. Authentication, data access, AI, observability and infrastructure are
platform services consumed through defined interfaces. AI augments domains through
extraction, retrieval, synthesis and reasoning, while authoritative data, financial
calculations, indicator methodologies and access controls stay deterministic and
governed.

A PR that organises backend code by screen rather than by domain runs against this.

## The methodology that makes OI defensible

[Non-negotiable adjustments in OI](../confluence/oi30/meeting-summaries/non-negotiable-adjustments-in-oi-19751993421.md)
(21 August, Michelle / Sharma / Nikolozi) captures what actually differentiates an OI
report from a generic financial comparison — and therefore what the calculation layer
must implement faithfully:

- Removing **non-recurring items**, typically **5–25% of total**.
- Excluding other operating income/expense outside core operations, and
  transaction-related expenses.
- **Standardising cost line items** — freight, SBC, COGS and SG&A categories — across
  peer companies.
- Judgement calls on recurring-but-extraordinary costs, decided on whether the expense
  is part of the normal operating model and how peers treat it.

Sector difficulty is uneven: healthcare and software in North America are cleanest thanks
to standardised non-GAAP disclosure; oil and gas needs substantial manual work. This is
the concrete reason the architecture uses **sector micro-swarms** rather than one
general-purpose agent.

An existing **Claude skill** already extracts non-GAAP adjustments at roughly **70–80%
accuracy**, degrading as sector-specific conditions accumulate in the prompt. Not yet
deployed. It is prior art for the Research and Benchmark agents and worth pulling in
rather than rebuilding.

Note the **GLS** variant: a distinct version alongside MVP and post-MVP, with its own
acceptance bar. Its feature set page is empty.

## Peer selection — the first capability specified end to end

[Peer Selection Capability](https://bainco.atlassian.net/wiki/spaces/OI30/pages/19809534070)
(new, September) is the most concrete implementation spec in the space, and the first to
describe an algorithm rather than a requirement.

**Sprint 1 and 2 work around missing CapIQ API access.** Existing CapIQ *Excel extracts*
are converted into a **Parquet dataset indexed by CapIQ ID** rather than waiting for the
API. That is consistent with ADR-009's per-run analytical store, and it means the CapIQ
rate-limit question is deferred rather than answered.

Six weighted peer-selection buckets, with deliberately simple arithmetic
(`bucket weight = importance points ÷ total points`):

| Bucket | Weight |
| ------ | ------ |
| Business Model Similarity | 30% |
| Revenue Scale | 20% |
| Regional Footprint | 20% |
| Product / Service Mix | 10% |
| End-Market Similarity | 10% |
| Growth & Maturity | 10% |

**Rewritten 20 September (v7 → v10), and two things changed.**

*User weighting is now allowed.* The earlier text said custom weights were "not to be
allowed now"; the page now says users "can define which buckets they want to prioritize",
with unselected criteria **deprioritised rather than ignored** so the comparison stays
balanced. Weights remain defaults rather than fixed.

*OpenAI is no longer named.* Peer discovery is now described as combining "a
deterministic CapIQ-based approach and GenAI/web search ranking, followed by enrichment
and reranking".

### What "GenAI" actually is — answered by the engineering pages

[Present working — Technical details](https://bainco.atlassian.net/wiki/spaces/OI30/pages/19849609338)
(21 September) documents the running backend behind that sentence, and it is the most
specific implementation description anywhere in the space. `POST /peers/discover` fans
out into two branches that run side by side and **neither of which ever raises**:

| Branch | What it does | Survivors |
| ------ | ------------ | --------- |
| **Agent** | `foundry.ask_agent` proposes peer names → `parse_candidates` (capped at 25) → each name shortlisted against our snapshot → a **second** Foundry call picks one `cap_id` or null → `resolve` drops fabricated IDs | 25 → 18 |
| **Deterministic** | vector the target on the criteria columns → `candidate_pool` filtered to same sector and region → rank by distance | 500 → 47 → 20 |

Merged by `cap_id` (agent entries win and keep their flag) → **31** → first `analysis_limit`
of 10 → `analyse_pair`, **one Foundry call per peer**, on a thread pool of 8 → rerank by
comparability. Peers past the limit stay **unanalysed, not dropped**. HTTP 503 only when
*both* branches fail.

**So "GenAI" is Azure AI Foundry**, which Technology Choices already records as *Adopt*.
The provider conflict is closed. Two narrower questions replace it: which model Foundry
serves, and whether these calls traverse the API Management GenAI gateway that §7 makes
the single egress point.

**Web search is `serpapi`** — stated outright on the Future Scope page. That one has no
position anywhere, and it is how target-company names leave Bain.

The matching engine is documented to a level that is rare and genuinely useful for
review: **BM25 over character 3–4 grams on the name, word tokens on location and sector**;
weights name 0.50 / business 0.35 / location 0.15, **renormalised over the parts that
actually matched**; `b = 0.5` rather than the textbook 0.75, and the page says that was
**measured, not chosen by taste**. Embeddings are used on `business_model` only, at
`match_semantic_weight = 0.6` — *"a company name is a label, not a concept"*. The
deterministic side uses **no model and no network**, so it is reproducible.

One design note worth carrying into review: the match scores are **min-max normalised per
query**, so the top hit always returns 1.000 *even when the company is absent from the
snapshot*. That is precisely why the second Foundry call exists — `match()` supplies
recall, the model decides identity, and null is an allowed answer. It is a sound split,
and it means any future attempt to replace that call with a score threshold will
reintroduce the bug it was built to avoid.

### The proposed successor, and where it contradicts the ruling page

[Future Scope — With ai search](https://bainco.atlassian.net/wiki/spaces/OI30/pages/19849412714)
proposes moving document handling from chat-time processing to an **event-driven ingestion
pipeline**: upload → Event Grid → queue → Azure AI Document Intelligence → chunk by
section → embed (`text-embedding-3-small`) → **Azure AI Search**, one index filtered by
`project_id` and `user_id`, hybrid keyword + vector with the semantic reranker. Parse
failures dead-letter rather than vanish; extracted JSON is kept so re-chunking never
re-runs the expensive step.

**The engineering reasoning is good** — tables do not survive naive chunking, blob cannot
serve a filtered hybrid query, a 200-page filing cannot block an upload response. But two
of its choices contradict decisions already recorded in Technology Choices:

- **§4.2 decided against a vector store**, at MVP *and* at north star, because AI Search
  "would mean building the embedding pipeline the native path exists to avoid". The
  decision is revisitable — AI Search is named as the first candidate — but the trigger is
  *"measured retrieval quality against a fixed evaluation set, not a hunch"*, and no
  measurement is cited.
- **§6 chose Service Bus explicitly over Event Grid**, for both commands and events.

Neither page acknowledges the other. See `open-questions.md`.

The framing also shifted from a sprint workaround ("before API access") to a durable
"methodology overview" designed to be reusable across companies, sectors and future
CapIQ datasets. The current CapIQ **Excel** files still provide the initial field set, so
the API dependency has not gone away — it has been designed around.

## Financial data access

[Data Contacts](https://bainco.atlassian.net/wiki/spaces/OI30/pages/19817627730)
(new, September) records the first hard numbers on data acquisition. Contacts are
**Abishek Soni** (TSR Automation) and **Kritik Ajmani** (Tech Team Lead, TSR).

- **S&P MCP is the primary route** for financial data. CapIQ and VCC are reference points
  for understanding calculations, with VCC currently giving "the strongest answers".
- **10-K extraction takes three API steps per company** — search, identify the filing,
  download — processed one company at a time at **5–10 seconds per call**, with a limit of
  roughly **6,000 companies per day**.
- Filing structure varies by geography and sector: US is consistent, EU and APAC less so.
  Revenue extraction is easy; **cost analysis is harder and often needs assumptions**.
- The existing approach "is **not yet repeatable at scale**". The team offers to share its
  framework and lessons learned.

These are the first concrete throughput figures anywhere in the space, and they should
inform the NFR page whenever it is written.

## Cost bar and taxonomy

[Cost bar split](https://bainco.atlassian.net/wiki/spaces/OI30/pages/19792560136) and its
[meeting notes](https://bainco.atlassian.net/wiki/spaces/OI30/pages/19799244847) settle
several things that were previously open:

- **Bain taxonomy (L1–L4) becomes the master structure**, aligned to how content is tagged
  in IRIS/Glean. Breakdown stops at whatever level stays meaningful and evidence-backed —
  L4 is not required.
- **Business units are limited to publicly reported segments.** No product, channel or
  operating-model segments that are not publicly reported, to avoid excessive assumptions.
  Parent cost structure is the fallback where BU detail is missing.
- Check for an **existing CapIQ → Bain taxonomy mapping** before building one; where none
  exists, use **fuzzy or LLM-assisted matching plus business validation** rather than
  manual row-by-row review.
- V1 anchors on **cost buckets** with drill-down into value levers. **AI transformation is
  explicitly in scope** as a lever, following user interviews.

## Data source governance

[Data Source Catalogue](../confluence/oi30/architecture/data-architecture/data-source-catalogue-19839025154.md)
(new, September) is the artefact several earlier gaps were waiting on. Its stated purpose
is *"one agreed view of where Opportunity Catalyst data comes from, so that anyone using
the platform's output can see what sits behind a number"*.

Per source it records what it is, why it is needed, how it is obtained and how often,
whether that is automated or manual today, **how sensitive it is, and what we are and
aren't permitted to do with it**.

That last item is precisely the licensing enforcement ADR-007 assigns to the evidence and
provenance service. **The content lives in a SharePoint workbook, not in Confluence**, so
it is outside the mirror and cannot be cited from here — worth pulling the permitted-use
rules onto the page itself.

## Data

Upstream sources: **VCC, CapIQ, IRIS, LSEG, Expert Search**.
([Data Sources summary](../confluence/oi30/data-requirements/data-sources-summary-19619676163.md))

Requirements are specified **per screen** — Dashboard, Target Setup, Peer Review, Case
for Change, Analysis, Output & Deck Builder — with the last three marked *update in
progress*, so treat them as unstable.
([Data Requirements per Screen](../confluence/oi30/data-requirements/data-requirements-per-screen-19710771207.md))

Confidential-data handling has its own page; check it before any review touching data
persistence or export.
([Confidential data](../confluence/oi30/roadmap-business-requirements/confidential-data-19689340995.md))

## Design requirements from September user testing

[Design requirements cont.](https://bainco.atlassian.net/wiki/spaces/OI30/pages/19808256031)
captures usability requirements from September 2026 sessions with six partners — Mark,
Andrew, Klaus, Alyson, Saverio and Andrea. It **supplements rather than replaces** the
core design requirements of 16 July.

Requirement groups 17 to 21, each mapped to a design principle:

- **Calculation transparency** — every bucket and sub-lever shows the full breakdown:
  Bain experience range, peer benchmark range, and how they converge. Partners can drill
  into any range for the full evidence stack.
- **Case studies** — IRIS surfaces 2–3 relevant Bain case studies per bucket, and full
  transformation stories rather than case titles.
- **Value realisation** — indicative timelines per opportunity: quick win (0–6 months),
  medium term (6–18), structural (18–36).
- **AI as a lever** — where AI enables a lever rather than merely powering the analysis,
  it is tagged as such.
- **Sector KPIs** — sector-specific KPI sets with explicit lever-to-KPI mapping.

Two items carry named owners: realisation timelines are **pending Stephanie's
confirmation**, and the Operational Excellence lever taxonomy is **to be confirmed with
Scott Daubin**.

## The ARC architecture assessment — 249 MUSTs, none answered

[Architecture Assessment Tracker](https://bainco.atlassian.net/wiki/spaces/OI30/pages/19853082681)
(22 September) is an empty page carrying two workbooks. It is the formal Bain architecture
governance gate, and it is the most consequential thing to arrive in the space this month.

| Workbook | Requirements | MUST | Responses recorded |
| -------- | ------------ | ---- | ------------------ |
| `OppCat_Architecture_Assessment_Tracker_Reviewed.xlsx` (ARC v2) | 180 | 136 | **0** |
| `AI_Architecture_Requirements_v2.1.xlsx` | 133 | 113 | **0** |

**ARC v2** spans Technical Architecture (65), Application Design (28), Code Quality (40)
and Software Development Principles (47). A reviewer pass on 22 September classified every
row and **re-prioritised 51 of them** — 14 MUST→SHOULD, 13 MUST→CONDITIONAL — on the
argument that the framework mandates patterns rather than outcomes (microservices, Istio,
Kafka, circuit breakers, RDBMS-to-NoSQL portability). That reclassification is defensible
and worth defending: **53 of 180 rows are marked "Questionable Requirement"**, and 33 more
are **External Dependency**, owned by Bain/TSG rather than the delivery team.

But the columns that matter — Design response, Arch/Engineering response, Status, Owner —
are **empty in all 180 rows**. The Summary sheet computes it without comment:
*MUST requirements 136, MUST not yet Addressed 136.* The Action Items sheet is still a
template stub, so the "Concerns and Disagreements" list has not been started either.

**The AI requirements workbook is the more interesting half**, and it is newer ground:
Model Serving & Abstraction, RAG & AI Data Architecture, Tools, Skills, MCP Servers &
Connectors, and twelve Agentic sections covering control, delegated identity, memory,
sandboxing, multi-agent systems and governance. Several map directly onto decisions this
workspace has already reviewed:

- **TA-AI-MOD-01** requires a model gateway so the provider can be swapped without
  touching business logic — Technology Choices already has this (API Management GenAI
  gateway), and the China assessment confirms it pays off.
- **TA-AI-RAG-DA-04** requires retrieval to respect source-document access control. The
  Future Scope pipeline filters on `project_id` and `user_id`, which is folder scoping,
  **not document ACL inheritance**.
- **TA-AI-MCP-04** requires MCP responses to be treated as data, never instructions.
- **TA-AI-TUL-03** requires a reviewable tool catalogue with risk classification and owner.

None of it is answerable from the five blank high-level design pages. **Security Design,
NFR, Observability, Endpoints and Deployment are precisely the evidence this assessment
asks for**, which makes those five blanks a gate on a governance milestone rather than
only a review inconvenience.

## Greater China — mainland excluded, Hong Kong conditional

[Opportunity Catalyst in Greater China](https://bainco.atlassian.net/wiki/spaces/OI30/pages/19853082640)
(22 September) is a full regional assessment, and the first page in the space to reckon
with where the product may legally run.

- **Mainland China: no.** Bain's regional AI guidance requires global-LLM features to be
  off for internal users and clients alike; only locally registered models are permitted.
  The page notes the guidance was written for Signal / NGGS, a client-deployed product,
  and that Opportunity Catalyst is an internal tool whose output is a deck — which removes
  the *reason* behind the rule but not the rule. It treats it as binding until its owner
  says otherwise, which is the right call.
- **Hong Kong: yes, with case-by-case clearance.** HK-billed cases default to Bain Global
  Cloud, so no extra consent is needed — but OpenAI- and Claude-backed features must still
  be off, and *which models the tool actually calls has never been written down*.
- **Nothing in the product enforces any of this.** The planned pre-flight check keys on
  where the *target company* sits, not on billing entity or user location, so it would not
  stop a mainland case analysing a US company.

The page's own recommendation is the cheap part: **record mainland as an explicit scope
exclusion** for the demo and MVP rather than letting it be discovered mid-case, and ask
StatusNeo to widen the pre-flight check's inputs now, while it is still unbuilt.

Two findings here matter beyond China. First, **the calculation engine and the
containerised packaging are named as the parts that carry over unchanged** to any
relocation — independent confirmation of `decisions/001`'s reasoning for keeping the
calculation engine separate from day one. Second, **the quality benchmark does not
exist**, and the page is blunt that without it "would a China-approved model be good
enough" is unanswerable. The current extraction skill is cited at **70–80% accuracy,
degrading as sector conditions accumulate** — the first accuracy figure recorded anywhere
in the space.

## Scope after GLS

[Post-GLS Feature Set](https://bainco.atlassian.net/wiki/spaces/OI30/pages/19800162379)
(new) splits nine initiatives out of the GLS demo scope: Technical Foundations, Scaling,
Cost Efficiency, Business Unit Handling, Data & Coverage Expansion, OI Lifecycle &
Versioning, Output Iteration & Editing, Collaboration & Governance, and a UX feedback
stream.

**This answers a finding from the ADR review.** Approval flows and real-time
collaboration are listed post-GLS, so ADR-004's client-writes-state pattern does not have
to account for two concurrent viewers at MVP. Finding S4 in
`reviews/2026-09-01-adr-001-to-009.md` is resolved by scope rather than by design.

## Delivery — what Sprint 1 actually did

[Sprint 1 Retrospective](../confluence/oi30/sprint-1-retrospective-19838042157.md)
covers **1–14 September 2026**, the first hard evidence of delivery pace. Content is in
`OC3_Sprint1_Retrospective.pptx`; the page itself is empty.

| Measure | Value |
| ------- | ----- |
| Committed at sprint start | 22 |
| Added mid-sprint | 28 |
| Completed | 22 of 50 (**44%**) |
| Of the committed 22, completed | **9** |
| Scope growth during the sprint | **~127%**, with no agreed gate |

**28 items carried into Sprint 2** — 9 in progress, 7 in review, 5 on hold or blocked, 7
not started. The carryover includes data foundation items OC3-18, 42, 43 and 45.

**What landed** is genuinely foundational: monorepo and service scaffolding (OC3-61),
Experience BFF with Entra SSO (OC3-68), app shell and routing (OC3-69), a Bain-token
library on Radix (OC3-71), an agent skeleton with standards (OC3-96), initial data
ingestion (OC3-44), company search and disambiguation (OC3-77), and a file archive for
Glean (OC3-103). A **technical debt register** was published in the sprint.

**Four constraints absorbed the capacity**, and the first two are unresolved going into
Sprint 2:

1. **Developer environment migration** — the team is moving off VDI onto Bain laptops
   because the VDI is *"materially slower for development work"*. Began in Sprint 1,
   **not complete**.
2. **Access provisioning** — Bain and Azure access was being granted in parallel with
   delivery. OC3-2 (service provisioning) and OC3-48 (development environment and
   access) **remain open**.
3. **Unplanned feasibility work** — Andromeda and **think-cell** had to be assessed
   mid-sprint, by the same people building.
4. **Late design decisions** — user journeys and design elements arrived after build
   began.

The team's own "what to try next" list: get admin access so estimates are captured in
Jira, track epics at programme level rather than on the board, name an owner and date
per blocker, confirm journeys and designs ahead of the sprint that builds them, and
finish the laptop migration.

**Two-week Scrum cycles.**
([Ways of Working](../confluence/oi30/ways-of-working-19588612195.md))

SN writes the application code; Bain holds product and architecture ownership. The
MVP sprint map is an explicit *draft based on initial scope assumptions*, and the MVP
itself is still **to be signed off** — scope may move under active development.

## What this brief cannot tell you

Security design, NFR targets, observability standards, API contract standards, and
CI/CD topology are **undocumented** — those pages are empty. See
[open-questions.md](open-questions.md). Do not infer a standard that has not been
written down; flag the gap instead.
