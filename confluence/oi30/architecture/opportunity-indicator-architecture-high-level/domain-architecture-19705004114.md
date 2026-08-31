---
title: "Domain Architecture"
confluence_id: 19705004114
confluence_url: https://bainco.atlassian.net/wiki/spaces/OI30/pages/19705004114
version: 1
updated: 2026-08-07T09:40:03.789Z
---

# Domain Architecture

[View in Confluence](https://bainco.atlassian.net/wiki/spaces/OI30/pages/19705004114)

# Domain Architecture

The **Opportunity Indicator (OI)** platform is organized around the business capabilities required to identify, evaluate, and communicate potential opportunities at a company level.

Rather than structuring the backend primarily around technical components or individual screens, the domain architecture reflects the lifecycle of an opportunity assessment: establishing the company universe, assembling financial and external evidence, computing indicators, identifying signals and events, evaluating companies relative to peers, and synthesizing these inputs into an actionable opportunity view.

Each domain owns its business rules, data contracts, commands, queries, and service interfaces. Shared technical capabilities—including authentication, data access, AI, observability, and infrastructure—are provided as platform services and consumed by domains through well-defined interfaces.

At a high level, the OI domain model consists of:

**Company Universe → Financial & Market Evidence → Indicators & Signals → Peer Context → Opportunity Assessment → Research & Collaboration → Outputs**

AI augments these domains through extraction, semantic retrieval, synthesis, and reasoning, while authoritative data, financial calculations, indicator methodologies, and access controls remain deterministic and governed.

## 1. Company & Entity Domain

The **Company & Entity Domain** establishes the core company universe against which Opportunity Indicator analysis is performed.

It provides the canonical representation of companies and the identifiers required to connect company information across financial, market, external, and AI-derived datasets.

Responsibilities include:

-

Company search and discovery

-

Company profiles and reference information

-

Ticker and external identifier management

-

Sector, industry, geography, and classification mappings

-

Company hierarchy and entity relationships

-

Currency and reporting metadata

-

Company eligibility and coverage

-

Company-to-dataset/entity resolution

-

Retrieval of company-level analytical context

The domain provides the common company identity used by all downstream financial, indicator, peer, intelligence, and opportunity capabilities.

## 2. Financial & Market Data Domain

The **Financial & Market Data Domain** manages the authoritative quantitative information used to evaluate companies.

It provides governed access to historical and current financial, valuation, operating, and market information required by the OI calculation and indicator framework.

Responsibilities include:

-

Financial statements and reported metrics

-

Historical company performance

-

Market and share-price information

-

Valuation metrics

-

Growth and profitability measures

-

Sector and market benchmarks

-

Currency normalization

-

Period and fiscal-calendar alignment

-

Financial-data quality and reconciliation

-

Derived financial measures

Financial transformations and calculations within this domain are deterministic, version-controlled, reproducible, and traceable to their underlying source data.

AI services consume these financial capabilities but do not act as the authoritative calculation mechanism.

## 3. Indicator & Calculation Domain

The **Indicator & Calculation Domain** represents one of the core business capabilities of Opportunity Indicator.

It encapsulates the methodologies developed by analysts for converting underlying company, financial, market, sentiment, and other evidence into standardized analytical indicators.

Responsibilities include:

-

Indicator definitions and metadata

-

Financial indicator calculations

-

Sentiment indicator calculations

-

Derived analytical measures

-

Threshold and scoring logic

-

Normalization methodologies

-

Indicator weighting and aggregation

-

Historical indicator calculation

-

Calculation versioning

-

Methodology configuration

-

Indicator explainability and provenance

Indicator definitions should be **configuration-driven wherever practical**, allowing methodologies, thresholds, weights, and other parameters to evolve without requiring structural changes to the platform.

Every material indicator result should retain sufficient provenance to identify:

**Source Data → Transformation → Calculation Methodology → Indicator Version → Result**

This provides the repeatability and auditability required for financial analysis.

## 4. External Intelligence & Evidence Domain

The **External Intelligence & Evidence Domain** manages information obtained from unstructured and semi-structured sources that may provide evidence of company developments or potential opportunity signals.

AI is particularly relevant within this domain because the underlying information may not be available in a consistently structured form.

Responsibilities include:

-

Targeted information gathering

-

Unstructured document processing

-

Information extraction

-

Company and entity association

-

Strategic-event identification

-

Sentiment evidence

-

Evidence classification

-

Source attribution

-

Temporal relevance

-

Evidence deduplication

-

Semantic retrieval

-

Evidence confidence and quality metadata

AI may be used to extract, classify, summarize, and interpret external information. However, the underlying evidence and its provenance should be retained wherever possible so that users can understand the basis for an AI-assisted conclusion.

This creates a distinction between **source evidence** and **AI-generated interpretation of that evidence**.

## 5. Peer & Benchmarking Domain

The **Peer & Benchmarking Domain** provides the comparative context required to determine whether a company's characteristics or indicators are meaningful relative to relevant companies.

Responsibilities include:

-

Standard peer groups

-

User-defined peer sets

-

Peer-set membership

-

Peer-set maintenance

-

Sector and industry benchmarks

-

Company-to-peer comparison

-

Relative financial performance

-

Relative indicator positioning

-

Ranking and percentile calculations

-

Benchmark selection

Peer sets are treated as reusable analytical objects rather than simply UI configuration.

This allows the same peer context to be consumed consistently by dashboards, calculations, opportunity assessments, AI reasoning, and exported analysis.

## 6. Opportunity Assessment Domain

The **Opportunity Assessment Domain** brings together the outputs of the underlying OI capabilities to form a consolidated view of potential opportunity at a company level.

This is the principal business domain of the platform.

It combines relevant:

-

Financial indicators

-

Market indicators

-

Sentiment indicators

-

Strategic events

-

External evidence

-

Peer positioning

-

Historical trends

-

Analyst-defined methodologies

to support identification and prioritization of companies that warrant further investigation.

Responsibilities include:

-

Opportunity signal aggregation

-

Company-level opportunity assessment

-

Opportunity scoring or prioritization

-

Signal materiality

-

Indicator convergence/divergence

-

Opportunity rationale

-

Historical opportunity evolution

-

Identification of supporting and conflicting evidence

-

Opportunity status and lifecycle

-

Explainability of assessment results

The Opportunity Assessment Domain should maintain a clear distinction between **deterministic evidence** and **AI-generated interpretation**.

For example, calculated financial indicators and peer rankings remain authoritative deterministic inputs, while AI can synthesize those inputs with external evidence to explain why a particular combination may represent an opportunity.

The objective is therefore not for an LLM to independently determine an opportunity, but for AI to augment a governed analytical framework.

## 7. Insight & Synthesis Domain

The **Insight & Synthesis Domain** transforms governed platform evidence into consumable analytical narratives and insight products.

Typical outputs may include:

-

Company summaries

-

Opportunity summaries

-

Insight cards

-

Strategic events

-

Business segments

-

Opportunity levers

-

Supporting evidence

-

Financial observations

-

Peer observations

-

Key changes and developments

The domain orchestrates AI capabilities but remains responsible for the business contract of the resulting insight.

AI-generated content should, where applicable, retain references to the underlying company data, indicators, calculations, and source evidence used to generate it.

Generated outputs may be persisted or cached where this improves performance, cost, consistency, or auditability.

AI is therefore a **technical capability used by the domain**, rather than the domain itself.

## 8. Research, Workspace & Collaboration Domain

The **Research & Collaboration Domain** supports the user journey from initial company discovery through investigation and development of an opportunity hypothesis.

Responsibilities include:

-

Company watchlists

-

Recently viewed companies

-

Saved companies

-

Saved peer groups

-

User preferences

-

Research workspaces

-

Shared projects

-

Saved analyses

-

Analyst notes and annotations

-

Collaboration around opportunity assessments

-

Persisted investigation context

A shared project can aggregate companies, peer sets, indicators, insights, evidence, and user-generated analysis into a persistent workspace.

This separates the underlying authoritative company/indicator data from the **user's research context and interpretation** of that information.

## 9. Reporting & Export Domain

The **Reporting & Export Domain** converts OI analysis into reusable outputs for downstream workflows and communication.

Responsibilities include:

-

Export request orchestration

-

Selection of companies and analysis

-

Data and insight assembly

-

Template management

-

Financial-data transformation

-

Chart and table generation

-

PowerPoint generation

-

ThinkCell integration

-

Export validation and formatting

The export domain consumes existing platform capabilities rather than independently recreating financial calculations or AI insights.

This ensures that information presented in exported materials remains consistent with information presented through the OI application.

## 10. Identity, Entitlement & Access Domain

Identity and access are implemented as cross-cutting platform capabilities.

Responsibilities include:

-

Okta integration

-

User authentication

-

JWT validation

-

User identity resolution

-

Request-level security context

-

Role and entitlement management

-

Role-Based Data Access (RBDA)

-

Service and agent identity

-

Authorization policy enforcement

-

Audit information

Authorization is enforced at appropriate application, service, and data boundaries rather than relying solely on frontend controls.

The same access principles apply regardless of whether a capability is invoked through the React application, an API, an MCP server, or an AI agent.

# CQRS and Capability Interaction

OI uses **Command Query Responsibility Segregation (CQRS)** to maintain a clear distinction between information retrieval and operations that change platform state.

CQRS is applied within the relevant business domains rather than implemented as a single monolithic application abstraction.

### Query Path

Queries represent read-oriented interactions such as:

-

Searching the company universe

-

Retrieving company profiles

-

Retrieving financial history

-

Retrieving calculated indicators

-

Comparing a company with its peers

-

Retrieving opportunity assessments

-

Retrieving source evidence

-

Retrieving generated insights

-

Reading watchlists and projects

The query path can be optimized for analytical workloads and may consume curated data products, materialized views, caches, or other read-optimized representations.

### Command Path

Commands represent operations that create or change platform state, including:

-

Creating or modifying peer sets

-

Adding or removing companies from watchlists

-

Creating or modifying research projects

-

Saving analysis

-

Initiating an indicator calculation

-

Requesting generation or refresh of an insight

-

Initiating an export

-

Recording relevant user activity

Commands are routed to domain-specific handlers that perform validation, authorization, business-rule enforcement, persistence, and appropriate downstream processing.

### Why CQRS is Appropriate for OI

The OI workload is inherently **read and analytics intensive**, while write operations tend to represent explicit business actions.

Separating the two paths provides:

-

Explicit business intent

-

Independent optimization of analytical queries

-

Clearer domain boundaries

-

Improved testability

-

Controlled state mutation

-

Better auditability

-

Independent scaling of read and write workloads

-

Flexibility to introduce caching and materialized analytical representations

# OI Data Architecture

The data architecture should reflect the analytical lifecycle of Opportunity Indicator rather than being defined solely as a collection of application tables.

Snowflake provides the primary governed analytical data platform, with complementary technologies used where appropriate for specialized processing and AI retrieval.

The logical data flow follows:

**Source Data → Raw → Standardized → Curated → Indicators & Analytical Products → AI-Ready Data → Opportunity Products**

### Source and Raw Data

The source/raw layer retains source-aligned financial, market, reference, and relevant external information with sufficient metadata to support lineage and reconciliation.

### Standardized Data

The standardized layer applies data-quality controls, entity resolution, schema standardization, currency/period normalization, deduplication, and common business definitions.

### Curated Analytical Data

The curated layer provides business-ready datasets for company analysis, financial analytics, benchmarking, and deterministic calculation.

Existing entities such as:

-

`COMPANY`

-

`COMPANY_TICKERS`

-

`FIRM_METRICS`

-

`FIRM_FINANCIALS`

-

`FIRM_PRICES_DAILY`

-

`SECTOR_METRICS`

would logically form part of this governed company and financial data landscape.

### Indicator & Opportunity Data

A dedicated analytical layer should represent the outputs of OI methodologies rather than mixing them directly with raw financial data.

Conceptually, this includes data products for:

-

Indicator definitions

-

Indicator values

-

Calculation versions

-

Indicator history

-

Company signals

-

Peer benchmarks

-

Opportunity assessments

-

Opportunity history

-

Supporting evidence

This layer becomes the governed analytical foundation of the Opportunity Indicator product.

### AI-Ready Data

An additional AI-serving layer prepares governed information for semantic retrieval and AI consumption.

It may contain:

-

Embeddings

-

Vector representations

-

Document chunks

-

Semantic metadata

-

Company context

-

Evidence indexes

-

Retrieval structures

-

AI context packages

This layer prevents AI-specific representations from being mixed unnecessarily with authoritative business data.

### AI-Generated Products

Generated outputs such as:

-

`AI_COMPANY_SUMMARY`

-

`AI_COMPANY_CARDS`

-

`AI_COMPANY_SEGMENTS`

-

`AI_COMPANY_EVENTS`

-

`AI_COMPANY_LEVERS`

-

`COMPANY_INSIGHTS`

should be treated as **derived AI products**, with appropriate metadata covering generation time, model/configuration version, source context, provenance, and lifecycle.

Where practical, AI-generated information should reference the governed evidence from which it was derived rather than becoming an isolated source of truth.

### User & Workspace Data

User-specific data remains logically separated from authoritative company and analytical data.

This includes:

-

`USER_COMPANY_WATCHLIST`

-

`USER_RECENTLY_VIEWED_COMPANY`

-

`USER_PEER_SETS`

-

`USER_PEER_SET_MEMBERS`

-

Shared projects

-

Saved analyses

-

Workspace configuration

-

User preferences

# Domain Architecture Principle

The fundamental architectural principle is that **Opportunity Indicator is the business architecture; AI is an enabling capability within it**.

The platform should therefore not evolve into a collection of AI endpoints around company data. Instead, it should expose a coherent set of reusable business capabilities:

**Company → Evidence → Financials → Indicators → Peers → Opportunity → Insight → Research → Output**

These capabilities are independently consumable through deterministic **APIs** and, where appropriate, open-ended **MCP interfaces**.

This model allows the React application, AI agents, future client experiences, and downstream integrations to consume the same governed OI capabilities while preserving domain ownership, security, calculation integrity, data lineage, and architectural separation of concerns.
