# OI 3.0 — Tech Lead brief

Distilled from the OI30 mirror. Every claim links to its source page. When this
disagrees with `confluence/`, the mirror wins — and this file needs updating.

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

## Delivery

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
