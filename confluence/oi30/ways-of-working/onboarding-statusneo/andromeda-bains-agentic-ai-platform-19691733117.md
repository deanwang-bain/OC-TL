---
title: "Andromeda - Bain's Agentic AI Platform"
confluence_id: 19691733117
confluence_url: https://bainco.atlassian.net/wiki/spaces/OI30/pages/19691733117
version: 1
updated: 2026-08-04T06:55:02.665Z
---

# Andromeda - Bain's Agentic AI Platform

[View in Confluence](https://bainco.atlassian.net/wiki/spaces/OI30/pages/19691733117)

**Andromeda — Bain's Agentic AI Platform**

**What it is**

Andromeda is Bain's internal platform for building, deploying, and operating AI agent solutions. It provides shared infrastructure that any Bain solution team plugs into, rather than each team building their own cloud infrastructure from scratch. It covers model serving, application hosting (Kubernetes), agent execution and governance, security, and observability.

**How OI 3.0 uses it**

OI 3.0 is built as a consumer of Andromeda — where Andromeda provides a capability, OI 3.0 uses it rather than duplicating it.

| What OI 3.0 needs  | Andromeda capability  |
|---|---|
| Running LLMs (e.g. Claude Sonnet/Opus)  | Model gateway — governed access, no data leaving Bain  |
| Embedding model for retrieval  | BGE-M3 + reranker, served on Andromeda GPU compute  |
| Application hosting  | Managed Kubernetes — networking, scaling, TLS, isolation  |
| Security and identity  | Workload identity, SSO via Bain IdP (OIDC/SAML)  |
| Logging and monitoring  | Shared observability via OpenTelemetry standard  |

StatusNeo owns the application and agent logic — the orchestrator, agent swarm, VCC integration, retrieval pipeline, and deck rendering. Andromeda provides the infrastructure those components run on.

**Important: Andromeda is the destination, not a current dependency**

OI 3.0 is not waiting for Andromeda to be ready before building. All application components are being packaged as containers from day one, which means migrating to Andromeda later is a configuration change — not a redesign. This is a deliberate decision to avoid Andromeda readiness becoming a blocker to the October pilot.

**What StatusNeo needs to know**

To be Andromeda-compatible, all application components must:

- Run as containers (Docker, Kubernetes-ready) — non-root, stateless, with health endpoints exposed
- Externalise all configuration and secrets (nothing hardcoded in the image)
- Emit OpenTelemetry-compatible traces, metrics, and logs across every service boundary
- Use Bain's workload identity model — no embedded API keys or credentials

DevOps, cloud infrastructure, and CI/CD pipelines are Bain-owned. StatusNeo provisions from Bain's existing templates during Discovery rather than building infrastructure independently.

**What is still to be confirmed**

| Open item  | Owner  | Status  |
|---|---|---|
| Andromeda programmatic/API access confirmed  | Bain (Felipe / Sandeep/ Michelle)  | Meeting held; Sandeep follow-up with Andromeda PM pending  |
| CoE validation gate — Andromeda integration scenario  | Dipesh Bhardwaj (SN)  | Discovery deliverable  |
