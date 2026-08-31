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

## Architecture

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
