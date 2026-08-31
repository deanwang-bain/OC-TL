---
title: "Architecture Layers"
confluence_id: 19705004106
confluence_url: https://bainco.atlassian.net/wiki/spaces/OI30/pages/19705004106
version: 1
updated: 2026-08-07T09:32:16.425Z
---

# Architecture Layers

[View in Confluence](https://bainco.atlassian.net/wiki/spaces/OI30/pages/19705004106)

### Client Experience Layer

The **Client Experience Layer** is intentionally decoupled from the underlying intelligence, data, and processing capabilities through a **headless architecture**.

The React-based frontend is responsible for navigation, workflow orchestration, data presentation, visualization, charting, and user interaction. It does not directly implement core analytical, calculation, or AI logic.

Client applications interact with platform capabilities through two primary patterns:

- **Deterministic interactions through APIs**, providing strongly defined contracts for structured workflows, queries, commands, calculations, and data retrieval.
- **Open-ended interactions through MCP**, enabling natural-language, agent-driven, and exploratory interactions with governed platform capabilities.

This separation allows alternative client experiences and channels to consume the same underlying business and intelligence capabilities without introducing dependencies on the React application.

### Gateway and Infrastructure Layer

The **Gateway and Infrastructure Layer** provides the secure entry point and runtime foundation for the platform.

Azure infrastructure services, including **Azure Front Door**, provide routing, TLS termination, edge protection, traffic management, application hosting, scalability, and integration with enterprise security controls.

Security is designed into the architecture from inception and applied across network, application, data, AI, and agent boundaries. Authentication, authorization, secrets management, encryption, workload identity, observability, and policy enforcement are treated as cross-cutting platform capabilities rather than application-specific concerns.

### Application and Capability Layer

The **Application Layer** exposes reusable business and technical capabilities independently of the client experience.

**FastAPI** provides deterministic service interfaces, while **FastMCP/MCP servers** expose selected capabilities for natural-language and agent-driven consumption.

Application functionality is organized around **business capabilities and bounded domains**, with clear separation between API contracts, domain services, CQRS command/query handlers, repositories, computation services, and shared platform infrastructure.

Business-critical operations—including financial calculations, transformations, scoring methodologies, and analytical rules—are implemented as **deterministic, version-controlled and testable services**. AI agents can invoke these capabilities through governed interfaces rather than reproducing authoritative calculation logic within the AI layer.

The architecture follows **CQRS**, separation of concerns, modular service design, and configuration-driven development to enable new business capabilities to be introduced with minimal coupling to existing domains.

### Data and Computation Layer

The **Data and Computation Layer** provides the authoritative foundation for structured data management, ingestion, transformation, quality management, financial calculations, and analytical processing.

Traditional enterprise data architecture principles are applied to capabilities including:

- Data ingestion and integration
- Data quality and reconciliation
- Structured data management
- Deterministic calculation and computation
- Reference and master data
- Metadata and lineage
- Role-Based Data Access (RBDA)
- Data security and classification
- Data contracts and schema governance
- Operational monitoring and auditability

**Snowflake** provides the primary enterprise analytical data platform, complemented by technologies such as **DuckDB and Svec** where appropriate for workload-specific processing, local analytics, vector retrieval, or AI-oriented access patterns.

Data is organized according to a **Medallion Architecture**, progressing from source-aligned/raw data through validated and standardized datasets to curated business-ready data products.

An additional **AI-ready serving layer** sits above the traditional medallion layers. This layer prepares governed information specifically for AI consumption, including semantic representations, embeddings, retrieval structures, contextual metadata, and other AI-optimized data products.

This ensures that AI-specific requirements do not compromise the integrity, governance, or deterministic nature of the core analytical data platform.

### AI and Intelligence Layer

The **AI and Intelligence Layer** provides reusable AI capabilities for extracting, retrieving, interpreting, synthesizing, and reasoning over structured and unstructured information.

The AI layer consumes governed data and deterministic platform capabilities rather than operating directly against uncontrolled source data wherever possible.

It supports capabilities such as company intelligence, financial and sentiment analysis, strategic-event identification, insight generation, summarization, semantic retrieval, and natural-language interaction.

AI capabilities are exposed independently of the client, allowing them to be consumed through APIs, MCP servers, agents, or future client channels.

Importantly, the AI layer is treated as an **augmentation layer rather than the system of record**. Authoritative financial data, calculations, business rules, permissions, and deterministic analytical outputs remain within their respective governed platform services.

### Agent Management and Orchestration Layer

Agent-based workflows are governed separately from the underlying AI models and application services.

**Agent management, orchestration, monitoring, security, and lifecycle governance are managed within Bain-hosted systems**, using the approved Azure AI/Foundry ecosystem and associated enterprise controls.

Agents operate against explicitly exposed tools and capabilities rather than having unrestricted access to underlying platform resources. Agent identity, authorization, tool access, execution, telemetry, and auditability can therefore be centrally governed.

This creates a controlled boundary between **probabilistic agent reasoning** and **deterministic enterprise capabilities**.

### Architectural Characteristics

Overall, the platform is designed as a **secure, headless, capability-based architecture** that separates client experience, deterministic business processing, governed data management, AI intelligence, and agent orchestration.

The architecture deliberately distinguishes between the **deterministic processing plane** and the **AI intelligence plane**. Core ingestion, data quality, calculations, structured data management, security, and access control follow established enterprise architecture principles, while AI and agents consume these capabilities through governed interfaces.

The resulting logical flow is:

**Source Systems → Data Ingestion & Quality → Medallion Data Platform → Deterministic Computation & Business Capabilities → AI-Ready Data → AI / Intelligence Services → APIs & MCP → Client Experiences / Agents**
