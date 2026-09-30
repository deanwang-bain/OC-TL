---
date: 2026-09-29
requester: "StatusNeo engineer (forwarded chat screenshot; sender not named, references teammate Dipesh)"
subject: "Deviation proposal: LangGraph over Microsoft Agent Framework; Postgres over Azure SQL for permanent memory"
type: design deviation
recommendation: decline
status: awaiting sign-off
---

# Request: LangGraph + Postgres/Redis instead of Microsoft Agent Framework + Azure SQL

## Asked for

A StatusNeo engineer proposes, informally over chat: replace Microsoft Agent Framework
with LangGraph for agent orchestration, and avoid Cosmos DB (said to be Azure AI
Foundry's default) by using Postgres for permanent memory and Redis for temporal
memory, with LangSmith/Langfuse for tracing. Stated reasons: Cosmos is expensive,
LangGraph is "stable for deployment on Azure Foundry" and works well with
Postgres/Redis, and MAF is "not stable version yet" (explicitly flagged as opinion,
"Just IMO").

Restated as a need: keep memory/persistence cost down, and use an orchestration
substrate with mature tracing and stateful-graph support.

## Existing rulings

This isn't a gap — it reopens two accepted decisions directly:

- [ADR-008](../confluence/oi30/architecture/oi-30-architecture-decision-records-19751960620.md)
  (Orchestration substrate): **Microsoft Agent Framework**, Accepted. Cites GA on
  3 April 2026 for Python and .NET, chosen for build-time graph validation (supports
  effort-budget propagation) and native OpenTelemetry spans with no added code.
  LangGraph was not one of the nominated alternatives (Foundry Workflows, Prompt flow,
  Durable Functions, fully custom were).
- [ADR-009](../confluence/oi30/architecture/oi-30-architecture-decision-records-19751960620.md)
  (Persistence topology): **Azure SQL Database** for operational/application state,
  **Azure Cache for Redis** for session and cache. Cosmos DB was already considered and
  explicitly rejected for the operational store — "no global distribution requirement,
  and relational integrity across lineage, grants and selections is the property that
  matters here." Redis for session/cache is exactly what's proposed here; that part is
  already aligned, not a deviation.
- `tools/known_tools.json` records Azure SQL Database as Adopt for application state.
  Postgres, LangGraph, LangSmith, and Langfuse have no recorded position anywhere in
  this workspace.

## Assessment

**One factual claim needs correcting before it's used to justify anything.** ADR-008
states Agent Framework reached general availability on 3 April 2026. Today is
2026-09-29 — nearly six months past GA. "MAF is not stable version yet" is not
correct as of the ADR's own cited source and should not carry weight in this decision
unless there's a newer, specific instability being observed in practice (a bug, a
missing feature, a hosting gap) rather than a general maturity concern.

**The Cosmos DB framing conflates two different decisions.** "Cosmos is the default DB
for Azure Foundry" is plausible as a statement about Agent Framework's own default
thread-storage backend — a narrower, framework-internal concern. ADR-009's rejection of
Cosmos DB was about the *application's* operational store (case, stage, lineage,
grants, peer sets, claims, evidence bindings, run status), a different and much larger
scope. If the actual concern is only "what backs MAF's own conversation/thread state,"
that's a narrower question than "replace the application's persistence topology," and
the two should not be resolved by the same choice. This distinction isn't addressed in
the chat message and needs to be pinned down before Postgres vs. Azure SQL is even the
right question.

**Postgres is not a response to the stated cost problem.** ADR-009 already avoids
Cosmos DB's cost/complexity for the operational store by choosing Azure SQL Database —
a managed, non-globally-distributed relational store, for the same "relational
integrity" reason now being cited. Azure Database for PostgreSQL is a second managed
relational product with no stated advantage over Azure SQL here, and it isn't on the
Technology Choices position table at all. Introducing it doesn't avoid Cosmos-style
cost (Azure SQL already does that) — it just adds a second relational substrate that
StatusNeo would now own alongside Azure SQL, or would replace Azure SQL with something
ADR-009 didn't evaluate.

**LangGraph vs. MAF touches real, cited requirements, not just preference.** ADR-008's
case for MAF rests on two specific properties: build-time graph validation feeding
effort-budget propagation, and native OpenTelemetry spans per executor/model call
supporting the transparency requirement in
[Vision](../confluence/oi30/overview/vision-19617939629.md) ("any number must be
drillable to its source, reasoning, and confidence level"). The chat message asserts
LangGraph's stateful graph and LangSmith/Langfuse "can be the better tracing and memory
management" but gives no comparison against those two specific properties — it's an
assertion about general orchestration quality, not a rebuttal of the reasons MAF was
picked. It may still be right, but nothing here shows it.

**Cost of yes:** reopens two Accepted ADRs on an unverified factual premise (MAF
stability) and an unevaluated substitute (Postgres) that doesn't obviously solve the
stated problem. Real rework cost if StatusNeo has already started building against
MAF/Azure SQL per the ADRs.

**Cost of no:** none beyond continuing on the documented path. If Foundry's own default
Cosmos-backed thread storage is genuinely a cost concern, that's answerable narrowly
(configure MAF's thread store to Redis/Azure SQL, which ADR-009 already provisions)
without touching the orchestration substrate at all.

## Recommendation

**Decline as framed.** ADR-008 and ADR-009 stand. Specifically:

1. Correct the record with StatusNeo: MAF has been GA since April 2026; "not stable"
   isn't the right framing for a reopen request. If there's a concrete instability
   they've hit (a specific bug, missing feature, or hosting/network-isolation gap —
   note ADR-008's own review trigger already covers "if Agent Framework hosting
   constraints conflict with network isolation requirements"), name it and route it as
   its own request.
2. Separate the actual question: is this about Agent Framework's own default
   thread-storage backend, or about the application's operational store? Only the
   former is plausibly a live, narrow cost concern — and ADR-009 already gives it an
   answer (Redis for session/cache, no Cosmos anywhere in the topology).
3. Postgres has no case made for it that Azure SQL doesn't already answer. Don't adopt
   it without a specific, written gap Azure SQL can't cover.
4. If StatusNeo wants to make a real case for LangGraph over MAF, ask for it against
   ADR-008's own stated criteria (graph validation for effort-budget propagation,
   native OTel tracing) rather than general stability/ecosystem claims.

## Sign-off

_Tech Lead decision and date — pending._
