---
title: "OI 3.0 Architecture Decision Records"
confluence_id: 19751960620
confluence_url: https://bainco.atlassian.net/wiki/spaces/OI30/pages/19751960620
version: 1
updated: 2026-08-21T06:40:35.252Z
---

# OI 3.0 Architecture Decision Records

[View in Confluence](https://bainco.atlassian.net/wiki/spaces/OI30/pages/19751960620)

Application, orchestration and persistence layers. Companion to `oi3-capability-derivation.md`, which holds the capability model and the business-layer rulings A1 to A7.

|

Field

 |

Value

 |
|---|---|
|

Program

 |

Opportunity Indicator 3.0

 |
|

Scope of this record

 |

Application decomposition, orchestration substrate and persistence topology

 |
|

Status of the set

 |

Accepted, pending Bain architect review

 |
|

Date

 |

2026-08-21

 |

ADR-001 to ADR-008 were issued on 2026-08-20. ADR-009 was issued separately as a persistence addendum on the same date and is consolidated into this record here, without change of substance.

## Index

|

Id

 |

Decision

 |

Status

 |
|---|---|---|
|

ADR-001

 |

Service decomposition principle

 |

Accepted

 |
|

ADR-002

 |

Calculation engine deployed as a service

 |

Accepted

 |
|

ADR-003

 |

Adjustment executes inside the calculation graph

 |

Accepted

 |
|

ADR-004

 |

Assistant state is written by the client, not read from cache

 |

Accepted

 |
|

ADR-005

 |

Frontend agent actions use declared tools

 |

Accepted

 |
|

ADR-006

 |

Content model owned by a composition service, renderers are read-only consumers

 |

Accepted

 |
|

ADR-007

 |

Evidence and provenance owned by a dedicated service

 |

Accepted

 |
|

ADR-008

 |

Orchestration substrate

 |

Accepted

 |
|

ADR-009

 |

Persistence topology

 |

Accepted, product selections provisional

 |

## ADR-001 Service decomposition principle

**Status.** Accepted.

**Context.** The capability model contains eleven domains and seventy-two L2 capabilities. A decomposition principle is needed before services can be named. Three candidates were considered: decomposition by capability domain, by data affinity, and by runtime profile.

**Decision.** Decompose by capability domain, then split any domain that straddles the synchronous and asynchronous boundary.

**Rationale.** Domain alignment gives a direct trace from service to capability, which is the completeness test the whole architecture rests on. The secondary split on runtime profile is necessary because operational characteristics differ by an order of magnitude within a single domain. A company search must answer in under a second. A peer research fan-out runs for minutes across concurrent workers. Placing both in one service makes the end-to-end wall clock budget unmanageable and couples scaling decisions that have nothing in common.

**Consequences.**

-

Every service carries the id of the capabilities it realises. A service with no capability trace is removed

-

Some domains produce two services, one synchronous and one run-oriented

-

Data affinity is handled through the data foundation rather than through service boundaries

**Alternatives rejected.**

|

Alternative

 |

Reason rejected

 |
|---|---|
|

Data affinity

 |

Produces services organised around storage, which breaks capability traceability and tends to reproduce the database schema as an API

 |
|

Runtime profile alone

 |

Produces a fast tier and a slow tier with no domain meaning, so ownership and change impact become unclear

 |

## ADR-002 Calculation engine deployed as a service

**Status.** Accepted.

**Context.** The calculation engine is tagged as a platform capability, reusable by other Bain use cases. Bain has confirmed that the external programmatic interface is a post-MVP concern, with OI 3.0 the only consumer at MVP.

**Decision.** Build and deploy the calculation engine as a service from day one, with a defined API, even though it has a single consumer at MVP.

**Rationale.** Building it as an in-process library and wrapping it in a service later is a rewrite, not a refactor. The boundary determines what the engine may depend on. A library embedded in the analysis service will accumulate dependencies on case state, peer sets and user context, none of which belong to a calculation engine, and all of which have to be removed before another Bain team can call it. A service that happens to have one consumer costs a deployment unit and enforces the boundary for free.

**Consequences.**

-

One additional deployment unit at MVP

-

The engine cannot read case state, peer sets or user context. Everything it needs arrives as input

-

The post-MVP consumption interface becomes an authentication and quota concern rather than an extraction project

-

Latency of the internal call must be budgeted, though it is negligible against the research and model calls that dominate

**Alternatives rejected.** In-process library with a later extraction. Rejected on the grounds that the extraction cost is incurred anyway and grows with every dependency added in the interim.

## ADR-003 Adjustment executes inside the calculation graph

**Status.** Accepted.

**Context.** The product's recurring evidence unit is the four-part record of raw value, adjustment, adjusted value and comparability note. Adjustments have three possible authorities: a governed rule in the calculation registry, a model judgement made at run time, and a user override. A user override must propagate to every figure derived from the adjusted value.

**Decision.** Model adjustment as a node type in the calculation dependency graph, alongside source metric, derived calculation, parameter and aggregation. Adjustment does not happen as pre-processing before the graph executes.

**Rationale.** Three properties follow directly and would otherwise have to be built and maintained separately.

|

Property

 |

How it follows

 |
|---|---|
|

Adjustment appears in the derivation trace

 |

The trace already records node to operand edges. An adjustment node is traced like any other

 |
|

Override propagation is automatic

 |

Overriding an adjustment replaces a node. Every dependent figure re-executes as a subgraph

 |
|

Blast radius of an override is known

 |

Memoisation already tracks which results depend on which nodes

 |

The three authorities become one mechanism differentiated by an `authored_by` attribute on the node, rather than three separate code paths writing to the same field.

**Consequences.**

-

The calculation engine must accept nodes authored at run time by a model, not only definitions resolved from the registry. This is the main cost of the decision and needs a validation boundary

-

Adjustment provenance and calculation provenance become one system rather than two

-

A separate normalisation service is not built

**Alternatives rejected.** A dedicated normalisation and adjustment service upstream of the calculation engine. Rejected because it places adjustment outside the derivation trace, which defeats the purpose of the trace, and requires a second provenance mechanism.

## ADR-004 Assistant state is written by the client, not read from cache

**Status.** Accepted.

**Context.** The proof of concept established a pattern in which every field of the assistant's state is written by the browser and none by the agent. The browser made the recommendation call, owns the activity log, and knows which screen is open. The alternative, having the agent re-read the backend cache, was available and not taken.

**Decision.** Retain the client-writes-state pattern on the target platform, whatever the runtime substrate.

**Rationale.** The property this buys is that the assistant cannot answer about a different run than the one on screen. If the agent re-reads a cache, nothing structurally prevents it from answering about a stale or different run, and the failure is silent and plausible, which is the least acceptable failure mode for a tool whose output is presented to a client executive audience.

A second property follows: the run payload is large, roughly 200KB in the proof of concept. Carrying it in state and reading it through tools keeps it out of the prompt entirely. The model receives an outline of roughly 1KB and calls a tool for what it needs.

**Consequences.**

-

The state synchronisation must be defensive rather than fire-and-forget. Thread connection and agent resolution can both silently replace state after a write. The proof of concept writes a token and re-checks that it survived

-

The client is accountable for what the assistant can see, which aligns with the grounded context assembly capability

-

Session state is not durable across restarts unless a durable thread store is added. ADR-009 places session state in Azure Cache for Redis, which addresses restart survival without making session state a system of record

**Alternatives rejected.** Agent reads the shared backend cache. Rejected on the correctness property above.

## ADR-005 Frontend agent actions use declared tools

**Status.** Accepted.

**Context.** The proof of concept used a client-side agent framework capable of free-form manipulation of the interface. Agent actions must appear in the audit trail as agent actions, distinguishable from user and system actions.

**Decision.** All agent actions on the client are declared tools with typed schemas. Free-form document manipulation is not permitted.

**Rationale.** Actor attribution depends on the agent invoking the same named action a user click invokes, with an actor parameter. The proof of concept does exactly this: the target resolution and stage progression handlers both take an actor argument and the agent tools pass `agent`. If the agent can manipulate the interface arbitrarily, there is no named action to record, and the actor-typed audit trail collapses into an untyped change log.

A second reason emerged in testing. When a tool is unregistered because an action is no longer permitted, the model finds no tool, has no result to relay, and narrates the change it intended to make. It told the user the target had been switched while the screen still showed the original. Declared tools that remain registered and refuse with a stated reason give the model something true to say.

**Consequences.**

-

Every action the agent can take must be enumerated, which is a design cost and a governance benefit

-

Tool availability is scoped by stage and case state, and unavailable tools refuse rather than disappear

-

The agent's reachable action set is auditable as a list, which supports architecture and security review

**Alternatives rejected.** Free-form manipulation. Rejected because it breaks actor attribution, which is a stated requirement visible in the activity log.

## ADR-006 Content model owned by a composition service

**Status.** Accepted.

**Context.** The backend is required to be headless, so that one composed content model can produce multiple artifact formats. Current scope is a deck exportable as HTML, PDF and presentation. The formats need to be close to each other but not identical.

**Decision.** A composition service owns the format-neutral content model. Renderers are separate consumers with read-only access to it.

**Rationale.** If renderers can write to the content model, three format-specific variants of the content emerge and the headless property is lost within one release. Read-only renderers force every content decision back into the composition service, where it is made once.

**Consequences.**

-

Adding a format is adding a renderer, with no change to composition

-

Format-specific fidelity compromises are handled inside the renderer and are visible as such

-

In-application editing writes to the content model through the composition service, not to a rendered artifact

-

Round-trip ingestion of externally edited files, which is post-MVP, becomes a translation into the content model rather than a merge

**Alternatives rejected.** A shared content store with renderers reading and writing. Rejected on the divergence risk above.

## ADR-007 Evidence and provenance owned by a dedicated service

**Status.** Accepted.

**Context.** Claims arrive by two paths. Comprehension extracts claims from documents and research. Synthesis authors claims from completed analysis. Both produce the same object with different evidence obligations. Every claim must carry its source, and figures must be re-derivable years later.

**Decision.** A dedicated evidence and provenance service owns claims, evidence bindings, source passages and the link to derivation traces. It is not a concern realised separately inside each store.

**Rationale.** With two producers and no single owner, the two paths diverge. One will bind to a document reference and the other to a passage, or one will record a calculation trace and the other will not, and the difference will surface only when a user drills into a figure and finds no supporting evidence. A single owner makes the evidence contract uniform by construction.

**Consequences.**

-

Producers depend on the evidence service rather than writing provenance alongside their own output

-

The drill-down path from a rendered claim to a raw input is one traversal rather than several

-

Source licensing rules, notably persistence restrictions on analyst report content, are enforced in one place

-

The service is on the read path of the interface, so its latency budget is user-facing

-

Under ADR-009 the service reads from the operational store on the user-facing path and from blob storage for the underlying trace, which is consistent with that latency budget

**Alternatives rejected.** Provenance as a cross-cutting concern implemented in each producing service. Rejected on divergence risk between the two claim producers.

## ADR-008 Orchestration substrate

**Status.** Accepted.

**Context.** Two candidates were nominated during discovery: Foundry Workflows, or Azure Durable Functions if Workflows proved limiting. The platform direction is Azure managed services first, with custom build only where genuinely warranted. The orchestration requirements are concurrent fan-out across a peer set, partial failure containment, effort budget propagation, progressive delivery of partial results, and survival of frequent deployments.

**Decision.**

|

Concern

 |

Substrate

 |
|---|---|
|

Agent orchestration, research fan-out, reranking, effort budget propagation

 |

Microsoft Agent Framework

 |
|

Deterministic long-running data work: scheduled refresh, snapshot creation, calculation batch

 |

Azure Durable Functions

 |
|

Scheduled integration and connector glue

 |

Azure Logic Apps

 |

**Rationale.**

*Foundry Workflows is not viable for a new build.* The portal workflow designer never reached general availability and is being retired on 1 December 2026. Microsoft's own general availability guidance lists building new production dependencies on Workflows as something to avoid. After that date the visual designer and in-portal execution stop, although Foundry continues to run YAML workflow definitions deployed as hosted agents.

*Prompt flow is also retiring*, on 20 April 2027, with Microsoft Agent Framework named as the recommended destination. Agent Framework reached general availability on 3 April 2026 for Python and .NET.

*Agent Framework fits the requirements.* It provides build-time validation of the execution graph, catching type mismatches and unreachable nodes before runtime, and emits OpenTelemetry spans for every executor invocation and model call without additional code. Graph validation supports effort budget propagation; native tracing supports the observability capability.

*Durable Functions is a complement, not a competitor.* Its constraints sit in a different place. Orchestrator functions cannot perform input or output. Fan-in runs in a single orchestrator instance on a single machine, unlike fan-out. Changing orchestrator code after an instance has started produces a non-determinism error on replay, which rules it out for agent orchestration where prompts and tool sets change frequently and a deployment would break in-flight runs. It remains the right choice where the code is stable and replay durability is an asset.

*Rate limiting is hand-built on either substrate.* Neither provides a native concept of an external API quota. This matters because source system rate limits and per-call costs remain open, and are listed in the open items below.

**Consequences.**

-

Two orchestration substrates rather than one, with a clear rule for which work goes where

-

No dependency on a retiring product, which is defensible under an Azure managed-first rubric

-

Two platform constraints carry into the technology architecture: some features including traces and workflow agents do not yet fully support network isolation, and publishing an agent gives it its own Entra identity with existing role assignments not carrying over, so identity reassignment must be part of the release process

-

Rate limiting against external sources is a custom component in the integration layer

**Alternatives rejected.**

|

Alternative

 |

Reason

 |
|---|---|
|

Foundry Workflows

 |

Retiring 1 December 2026, never reached general availability, explicitly discouraged for new production dependencies

 |
|

Prompt flow

 |

Retiring 20 April 2027, in maintenance with no further feature development

 |
|

Durable Functions for agent orchestration

 |

Non-determinism on orchestrator code change breaks in-flight runs across deployments

 |
|

Fully custom orchestration

 |

Fails the Azure managed-first rubric with no compensating benefit

 |

**References.**

-

Microsoft Foundry portal general availability overview: [https://learn.microsoft.com/en-us/azure/foundry/concepts/general-availability](https://learn.microsoft.com/en-us/azure/foundry/concepts/general-availability)

-

Build a workflow in Microsoft Foundry (Preview), including migration guidance: [https://learn.microsoft.com/en-us/azure/foundry/agents/concepts/workflow](https://learn.microsoft.com/en-us/azure/foundry/agents/concepts/workflow)

-

Prompt flow is being retired: [https://techcommunity.microsoft.com/blog/azure-ai-foundry-blog/prompt-flow-is-being-retired/4513587](https://techcommunity.microsoft.com/blog/azure-ai-foundry-blog/prompt-flow-is-being-retired/4513587)

-

Migrate from Prompt Flow to Microsoft Agent Framework: [https://learn.microsoft.com/en-us/azure/foundry-classic/how-to/prompt-flow-migration-overview](https://learn.microsoft.com/en-us/azure/foundry-classic/how-to/prompt-flow-migration-overview)

-

Performance and scale in Durable Functions: [https://learn.microsoft.com/en-us/azure/azure-functions/durable-functions/durable-functions-perf-and-scale](https://learn.microsoft.com/en-us/azure/azure-functions/durable-functions/durable-functions-perf-and-scale)

-

Fan-out and fan-in in Durable Functions: [https://learn.microsoft.com/en-us/azure/azure-functions/durable/durable-functions-fan-in-fan-out](https://learn.microsoft.com/en-us/azure/azure-functions/durable/durable-functions-fan-in-fan-out)

**Review trigger.** Revisit if a visual authoring surface for orchestration is mandated, or if Agent Framework hosting constraints conflict with the network isolation requirements once those are defined.

## ADR-009 Persistence topology

**Status.** Accepted. Product selections are provisional pending confirmation of network isolation requirements.

**Context.** Discovery specified an analytical substrate and a document substrate. It did not specify where application state lives. Roughly nineteen objects require transactional read-write on a user-facing read path, including case and stage state, collaborator grants, peer set selections, opportunity ranking, chat turns, run status and audit events.

Snowflake carries the source numerical data from CapIQ and AURA, travelling through medallion layers with data quality maintained, refreshed monthly and largely stable. That is batch analytical data, on a different lifecycle from per-run data and from application state. The term operational data store has been applied to Snowflake in earlier material; in this record the term is reserved for the transactional application store, so that the two are not conflated.

Three distinct persistence problems therefore exist: transactional application state, per-run analytical data, and batch analytical data. A single substrate cannot serve all three well.

**Decision.** Six logical stores, separated by access pattern rather than by data domain, mapped onto four managed products at MVP: Azure SQL Database, Azure Cache for Redis, Azure Blob Storage with ADLS Gen2, and SharePoint. Snowflake is the north star batch substrate and is unchanged by this decision.

|

Logical store

 |

Holds

 |

Substrate

 |

Access pattern

 |
|---|---|---|---|
|

Operational

 |

Application state: case, stage, lineage, grants, peer sets, angles, opportunities, claims, evidence bindings, content nodes, deck composition, run status

 |

**Azure SQL Database**

 |

Transactional, per-request, user-facing read path

 |
|

Audit

 |

Audit events, override rationale, actor attribution

 |

**Azure SQL Database ledger tables**, digests published to immutable blob

 |

Append-heavy, scoped query, tamper-evident

 |
|

Session and cache

 |

Chat thread state, hot case state, run progress fan-out

 |

**Azure Cache for Redis**

 |

Ephemeral, low latency

 |
|

Per-run analytical

 |

Parquet files for a case version, bronze, silver and gold groupings under the case identifier

 |

**Azure Blob Storage, ADLS Gen2**

 |

Bulk read, loaded on demand into DuckDB

 |
|

Documents

 |

Uploads, retrieved documents, summaries

 |

**SharePoint**

 |

Retrieval by agents, role-based access control

 |
|

Batch analytical, north star

 |

CapIQ and AURA through medallion layers, plus the semantic layer

 |

**Snowflake**

 |

Monthly batch, stable

 |

**Rationale.**

*Azure SQL Database for operational state.* The objects are relational and their integrity matters. Case lineage is a graph of foreign keys. Collaborator grants and document access grants are join tables. A peer set is a selection over candidates. Losing referential integrity here produces exactly the failure the evidence model exists to prevent, a claim pointing at nothing. Scale does not argue for anything more specialised: 100 users at MVP with low concurrency, and 2300 plus their teams at full scale, sits well within the range of a managed relational database.

*Azure SQL ledger tables for the audit trail.* The tamper evidence requirement was confirmed in discovery and no named substrate provided it. Ledger tables give cryptographically verifiable tamper evidence with database digests that can be published to immutable storage, while the audit trail remains queryable through ordinary SQL. This matters because the assistant queries the audit log by scoped tool call, so a write-only archive would not serve the requirement. This satisfies the write-once, read-many obligation with a managed capability, and nothing custom is built.

*Parquet to blob storage, not SharePoint.* SharePoint earns its place for documents, because it gives agents retrieval without a custom pipeline and carries role-based access control natively. Neither property applies to parquet, which is read in bulk by a query engine and needs no per-document access control. Holding parquet in SharePoint would ask a document collaboration platform to act as a data lake. ADLS Gen2 is the data lake, DuckDB reads from it directly, and the medallion grouping within each case version is preserved unchanged.

*Redis for session and cache only.* No durable state. Chat threads in the proof of concept lived in process memory and reset on refresh, which is acceptable in a proof of concept and not on the target platform. Redis makes them survive restarts without making them a system of record.

*Snowflake stays where discovery put it.* North star, batch, monthly, separate from both operational state and per-run analytical data.

**Consequences.**

-

Four managed products at MVP rather than two. This is the cost of the separation and it is modest at this scale

-

Snapshot pinning under CF13 becomes a pointer from the operational store to a parquet path plus a set of pinned definition versions. Nothing is copied

-

The evidence service under ADR-007 reads from the operational store on the user-facing path, and from blob for the underlying trace, which is consistent with its latency budget

-

Two products carry the audit requirement, since ledger digests publish to immutable blob. Both are managed

-

The choice of Azure SQL over Cosmos DB should be revisited only if a multi-region or global distribution requirement appears. None exists today, with servers in a single US region

**Alternatives rejected.**

|

Alternative

 |

Reason

 |
|---|---|
|

SharePoint for all persistence

 |

Not a transactional store. Several ADRs become undeliverable

 |
|

Snowflake as the operational store

 |

Columnar and batch-oriented. Per-request interactive writes are not its purpose, and it is a north star substrate rather than an MVP one

 |
|

Cosmos DB for operational state

 |

No global distribution requirement, and relational integrity across lineage, grants and selections is the property that matters here

 |
|

Custom append-only audit archive with hash chaining

 |

A custom build where a managed capability exists

 |
|

Parquet in SharePoint

 |

SharePoint's two advantages, agent retrieval and per-document access control, do not apply to parquet

 |

**Review trigger.** Revisit product selections once network isolation requirements are confirmed, since they affect private endpoint configuration across every store.

## Open items arising

|

#

 |

Item

 |

Owner

 |

Related

 |
|---|---|---|---|
|

1

 |

Source system rate limits and per-call cost, which determine the rate limiting component's design

 |

Bain

 |

ADR-008

 |
|

2

 |

Network isolation requirements, which interact with the known tracing and agent hosting gaps and determine private endpoint configuration across the stores

 |

Bain

 |

ADR-008, ADR-009

 |
|

3

 |

Audit retention period, which determines digest publication cadence

 |

Bain

 |

ADR-009

 |
|

4

 |

Validation boundary for model-authored adjustment nodes

 |

StatusNeo

 |

ADR-003

 |
|

5

 |

Agent identity reassignment step in the release process

 |

StatusNeo

 |

ADR-008

 |
|

6

 |

Confirm current availability and regional support of Azure SQL Database ledger tables in the target subscription

 |

StatusNeo

 |

ADR-009

 |
|

7

 |

Durability requirement for assistant sessions beyond cache-backed restart survival, if any

 |

Joint

 |

ADR-004, ADR-009

 |
