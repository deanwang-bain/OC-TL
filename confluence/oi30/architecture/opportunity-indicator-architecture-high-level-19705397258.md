---
title: "Opportunity-Indicator Architecture (high Level)"
confluence_id: 19705397258
confluence_url: https://bainco.atlassian.net/wiki/spaces/OI30/pages/19705397258
version: 9
updated: 2026-08-07T10:13:45.853Z
---

# Opportunity-Indicator Architecture (high Level)

[View in Confluence](https://bainco.atlassian.net/wiki/spaces/OI30/pages/19705397258)

# **Overview**

**OI** is a cloud-native application designed to support financial analysis and identify opportunities across companies. It brings together multiple financial and sentiment indicators developed by Bin analysts, leveraging AI throughout the process to gather and analyse targeted insights from both structured and unstructured data sources.

# Solution Architecture

_[image: image-20260807-101304.png — not downloaded]_

_[image: Screenshot 2026-08-07 at 10.22.56.png — not downloaded]_

### High-Level Platform Architecture

At a high level, the **OI platform** is implemented as a cloud-native, modular architecture spanning presentation, integration, processing, data, AI, agent orchestration, and infrastructure layers.

- **UI/UX Layer** – Built using **React**, **AI SDK**, and **AG Grid** to provide interactive analytical workflows, AI-enabled user experiences, and high-performance data visualization.
- **Interface Layer** – Uses **FastAPI** for service and API interfaces and **FastMCP** for exposing capabilities to AI agents and MCP-compatible clients.
- **Processing Layer** – Runs on **Microsoft Azure**, providing scalable compute and processing capabilities for financial analytics, data transformation, and AI-driven workloads.
- **Data Layer** – Uses **Snowflake**, **Svec**, and **DuckDB** to support analytical storage, vector-based retrieval, and high-performance local/in-process analytical workloads.
- **AI Platform Layer** – Built on the **Azure AI** ecosystem to provide access to foundation models, embeddings, retrieval, and other AI services.
- **Agent Management & Orchestration** – Uses **Azure AI Foundry** to develop, manage, orchestrate, and operationalize AI agents and agent-driven workflows.
- **Infrastructure Layer** – Leverages **Azure infrastructure services** for application hosting, request routing, scalability, security, observability, and operational monitoring.

### Architectural Principles

The platform is designed around a set of architectural principles intended to support extensibility, maintainability, and rapid delivery of new analytical and AI capabilities.

- **Capability-Based Architecture** – Business requirements are decomposed into discrete business capabilities and mapped to reusable technical capabilities. This enables functionality to evolve independently while promoting reuse across workflows and use cases.
- **Configuration-Driven Development / Convention over Configuration** – Application behavior is driven through standardized conventions and declarative configuration wherever possible, minimizing bespoke implementation and accelerating the introduction of new datasets, indicators, workflows, and capabilities.
- **Separation of Concerns** – Presentation, business logic, data access, AI/agent orchestration, and infrastructure responsibilities are logically separated to reduce coupling and simplify development, testing, and operations.
- **Modular Services** – Functionality is organized into independently maintainable services and components with well-defined contracts, enabling capabilities to be developed, deployed, tested, and scaled with minimal impact on the wider platform.
- **Command Query Responsibility Segregation (CQRS)** – Read and write operations are separated to allow each path to be independently designed and optimized. Query workloads can therefore be optimized for high-volume analytical access, while commands can enforce appropriate business rules, validation, and transactional behavior.

# Architecture Summary

Security is embedded into the platform architecture from the outset, rather than introduced as a downstream control. Security considerations are incorporated across application design, data access, AI services, infrastructure, identity, monitoring, and operational processes.

The platform follows a **headless architecture**, where the intelligence layer is decoupled from the client experience. This enables multiple consumers to access the same underlying analytical and AI capabilities without creating dependencies between the user interface and the core intelligence services.

The intelligence layer is exposed through two primary interaction patterns:

- **Deterministic interactions via APIs** – Well-defined APIs support structured, predictable workflows where inputs, outputs, and business logic are explicitly controlled.
- **Open-ended interactions via MCP servers** – MCP-based interfaces enable natural-language and agent-driven interactions with platform capabilities, supporting more dynamic and exploratory use cases.

**Agent management, orchestration, monitoring, governance, and security** are managed within Bain-hosted systems. This provides centralized control over agent execution, access policies, observability, lifecycle management, and compliance.

The data platform is designed using a **Medallion Architecture**, with progressive data refinement across ingestion, standardized, and curated analytical layers. An additional **AI-serving layer** is introduced to optimize data availability for AI, retrieval, agent, and semantic-search workloads.

The **client experience is separated from the underlying platform services through well-defined interfaces**. The UI communicates with the platform through APIs for deterministic interactions and supports natural-language interactions through MCP-enabled capabilities. This separation enables client applications to evolve independently while preserving consistent access to shared business, analytical, and AI capabilities.

## [Architecture Layers]Architecture Layers

[Data Management Layer]Data Management Layer

### Separation of Deterministic and AI Processing

A key architectural principle is the explicit separation between the platform's **deterministic processing plane** and its **AI intelligence plane**.

The deterministic processing plane remains the authoritative mechanism for ingestion, validation, transformation, financial calculations, structured data management, access control, and production of governed analytical datasets. The AI intelligence plane operates on top of these capabilities to perform tasks such as unstructured information extraction, semantic retrieval, synthesis, reasoning, natural-language interaction, and agent-driven workflow orchestration.

Where an AI agent requires an authoritative calculation or governed dataset, it will invoke the corresponding deterministic capability through a controlled **API, MCP tool, or service interface** rather than attempting to independently derive the result.

This approach ensures that **AI augments the established data and analytical architecture rather than becoming a substitute for it**, preserving the control, repeatability, lineage, security, and auditability required for enterprise-grade financial analysis.

[Technical Stack]Technical Stack

[Domain Architecture]Domain Architecture

[Logical Application Flows]Logical Application Flows

[Endpoints & Interfaces Design]Endpoints & Interfaces Design

[Security Design (Processing, AI and Data)]Security Design (Processing, AI and Data)

[NFR (Non-Functional) Design Choices]NFR (Non-Functional) Design Choices

[Observability, Logging, Notification & Monitoring Design]Observability, Logging, Notification & Monitoring Design

[Deployment Design (AI, Compute, Data, Components - CI/CD)]Deployment Design (AI, Compute, Data, Components - CI/CD)

# Detailed Architecture

_[image: image-20260807-101334.png — not downloaded]_
