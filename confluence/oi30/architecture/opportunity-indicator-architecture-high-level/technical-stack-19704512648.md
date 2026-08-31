---
title: "Technical Stack"
confluence_id: 19704512648
confluence_url: https://bainco.atlassian.net/wiki/spaces/OI30/pages/19704512648
version: 1
updated: 2026-08-07T09:36:49.585Z
---

# Technical Stack

[View in Confluence](https://bainco.atlassian.net/wiki/spaces/OI30/pages/19704512648)

## Technology Stack

The OI platform is implemented using a **cloud-native, headless technology architecture**. Technology choices are aligned to distinct architectural capabilities across client experience, interfaces, deterministic processing, data management, AI/agent services, security, and infrastructure.

### Frontend / Client Experience

The primary web client is implemented as a modern single-page application using **React and TypeScript**. The frontend is intentionally decoupled from the underlying business, analytical, data, and AI capabilities through well-defined service interfaces.

Primary technologies include:

-

**React 18**

-

**TypeScript**

-

**Vite**

-

**TanStack Query**

-

**AG Grid**

-

**Apache ECharts**

-

**React Router v6**

-

**TailwindCSS**

-

**Bain Design System**

-

**Okta React SDK**

-

**AI SDK (ai-sdk.dev)**

The client layer is responsible for navigation, application state, dashboards, company and peer views, interactive data grids, financial and analytical visualizations, and AI-assisted user experiences.

Business rules, authoritative calculations, and core intelligence capabilities are intentionally kept outside the client. The frontend primarily consumes deterministic platform capabilities through APIs and AI/intelligence capabilities through governed conversational and service interfaces.

### Interface and Service Layer

The platform exposes business and technical capabilities through two complementary interface patterns:

-

**FastAPI** provides deterministic REST/API interfaces for structured application workflows, commands, queries, calculations, and data retrieval.

-

**FastMCP / MCP Servers** expose governed platform capabilities for open-ended, natural-language, and agent-driven interactions.

Primary technologies include:

-

**FastAPI**

-

**FastMCP**

-

**Python 3.12+**

-

**Pydantic v2**

-

**OpenAPI**

-

**MCP (Model Context Protocol)**

This dual-interface model allows the same underlying capabilities to be consumed by the React client, AI agents, natural-language experiences, and potentially other future clients without coupling business functionality to a specific presentation channel.

### Application and Deterministic Processing

The application layer is primarily implemented in **Python** and organized around modular business and technical capabilities.

The backend follows **CQRS, separation of concerns, capability-based architecture, modular service design, and configuration-driven development**.

Core financial calculations, business rules, transformations, indicators, scoring methodologies, and other authoritative processing are implemented as deterministic services. These capabilities remain independently testable, version-controlled, reproducible, and auditable.

Primary technologies and engineering tooling include:

-

**Python 3.12+**

-

**FastAPI/FastMCP**

-

**Pydantic v2**

-

**Pytest**

-

**Ruff**

-

**MyPy**

-

**UV**

-

**Docker**

Where appropriate, asynchronous processing patterns are used for long-running data, analytical, and AI workloads.

### Data Platform

The data architecture follows established enterprise data-management principles, with **Snowflake** providing the primary analytical data platform.

Primary technologies include:

-

**Snowflake**

-

**Snowflake Python Connector**

-

**DuckDB**

-

**Svec / vector storage and retrieval capabilities**

The data platform supports:

-

Data ingestion and integration

-

Structured data management

-

Data validation and quality management

-

Data transformation and enrichment

-

Deterministic computation and calculations

-

Reference and master data

-

Metadata and data lineage

-

Role-Based Data Access (RBDA)

-

Data security and classification

-

Auditability and reconciliation

Data is logically organized using a **Medallion Architecture**, progressing through raw/source-aligned, validated/standardized, and curated/business-ready data layers.

An additional **AI-ready serving layer** provides AI-optimized representations of governed platform data, including embeddings, semantic structures, retrieval indexes, contextual metadata, and other structures required for AI and agent workloads.

### AI and Intelligence Platform

The AI layer provides reusable intelligence capabilities for processing both structured and unstructured information.

Primary technologies include:

-

**Azure AI services**

-

**Azure AI Foundry**

-

**Foundation / Large Language Models**

-

**Embedding models**

-

**Vector and semantic retrieval**

-

**Retrieval-Augmented Generation (RAG) patterns**

-

**MCP-based tool integration**

The AI layer supports capabilities such as information extraction, company summarization, strategic-event identification, financial and sentiment insight generation, semantic retrieval, synthesis, and natural-language interaction.

AI services consume governed data products and deterministic platform capabilities through defined interfaces. Authoritative financial calculations and business rules remain within the deterministic application and computation layers rather than being delegated to generative models.

### Agent Management and Orchestration

Agent capabilities are managed as a distinct architectural concern from the underlying application and AI model layers.

**Agent management, orchestration, monitoring, security, and lifecycle governance are managed within Bain-hosted systems**, leveraging approved Azure AI/Foundry capabilities and enterprise controls.

Agents interact with the platform through explicitly exposed APIs, MCP tools, and governed data services rather than unrestricted access to underlying infrastructure or databases.

This provides centralized control over:

-

Agent identity and authorization

-

Tool and capability access

-

Agent orchestration

-

Execution policies

-

Model configuration

-

Prompt and agent lifecycle

-

Monitoring and telemetry

-

Auditability

-

Security and governance

### Cloud Infrastructure and Platform Services

The platform is hosted on **Microsoft Azure**, which provides the runtime, networking, routing, security, observability, and operational foundation.

Primary infrastructure components include:

-

**Azure Front Door** – edge routing, TLS termination, traffic management, and edge protection

-

**Azure App Service / approved Azure compute services** – application and service hosting

-

**Docker** – application packaging and deployment portability

-

**Azure identity and security services** – workload identity, authentication, authorization, secrets, and policy enforcement

-

**Azure Application Insights** – application telemetry, tracing, performance monitoring, and diagnostics

-

**Azure Monitor / associated monitoring services** – infrastructure and operational observability

-

**Snowflake** – enterprise analytical data platform

-

**Azure AI / Azure AI Foundry** – AI and agent platform services

-

**Azure DevOps or equivalent CI/CD tooling** – automated build, test, security validation, and deployment

### Security and Engineering Controls

Security is treated as a **cross-cutting architectural capability** and is incorporated from the start of the platform lifecycle rather than applied as a downstream control.

Security controls span the client, API/MCP interfaces, application services, data platform, AI services, agents, and infrastructure. These include identity-based authentication, role-based authorization, least-privilege access, encryption, secrets management, network controls, data classification, RBDA, logging, monitoring, and auditability.

CI/CD pipelines provide automated quality gates covering unit and integration testing, static analysis, type checking, dependency/security scanning, and deployment validation.

### Technology Architecture Summary

The technology stack therefore supports a logical separation of:

**React Client Experience → API / MCP Interfaces → Deterministic Business & Computation Services → Governed Data Platform → AI-Ready Data → AI & Intelligence Services → Agent Orchestration**

Azure provides the common infrastructure, security, hosting, routing, and observability foundation across these layers.

This separation allows individual technologies and capabilities to evolve independently while maintaining **clear architectural boundaries, governed interfaces, enterprise security, testability, observability, and extensibility**.
