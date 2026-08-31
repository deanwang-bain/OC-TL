---
title: "Technology Choices"
confluence_id: 19751338017
confluence_url: https://bainco.atlassian.net/wiki/spaces/OI30/pages/19751338017
version: 1
updated: 2026-08-21T06:40:59.856Z
---

# Technology Choices

[View in Confluence](https://bainco.atlassian.net/wiki/spaces/OI30/pages/19751338017)

Opportunity Indicator 3.0. Frontend, backend and data, with the build versus buy position and the MVP to north star delta.

| Field  | Value  |
|---|---|
| Program  | Opportunity Indicator 3.0  |
| Rubric  | Azure managed services first, custom build only where genuinely warranted  |
| Status  | Draft for review  |

## 1. How to read this

### 1.1 Three positions

Bain's stated rubric is a binary: managed first, custom only where warranted. Three positions read it more accurately, and the reframing is flagged rather than assumed.

| Position  | Meaning  |
|---|---|
| **Build**  | StatusNeo writes and operates the code  |
| **Adopt**  | An Azure managed service, configured, with integration code only  |
| **Buy**  | An existing Bain or third-party system consumed under licence  |

### 1.2 What a choice has to survive

Every selection below answers four questions. Where a credible alternative exists, it is named and the reason for rejecting it is given. A choice with no rejected alternative is usually a choice that was never made.

| Test  | Question  |
|---|---|
| Fit  | Does it do the job the capability model asks for  |
| Rubric  | Is it managed, and if not, is the custom build warranted  |
| Reversibility  | What does it cost to change our mind in eighteen months  |
| Operability  | Who runs it, and with what expertise  |

## 2. Frontend

| Concern  | Choice  | Position  | Phase  |
|---|---|---|---|
| Framework and language  | React with TypeScript, built with Vite  | Build  | Both  |
| Hosting  | Static assets from Azure Front Door CDN  | Adopt  | Both  |
| Server state  | TanStack Query  | Build on OSS  | Both  |
| Client state  | Zustand  | Build on OSS  | Both  |
| Assistant surface  | AG-UI protocol, CopilotKit  | Buy, licence  | Both  |
| Tabular inspection and export  | AG-Grid Enterprise  | Buy, existing Bain licence  | Both  |
| Exhibit rendering  | Vega-Lite, Apache ECharts  | Build on OSS  | Both  |
| Component primitives  | Radix with a Bain-token theme layer  | Build  | Both  |
| Streaming  | Server-sent events  | Adopt  | Both  |
| Accessibility  | WCAG 2.2 AA  | Build  | Both  |
| Internationalisation  | i18next, English only at MVP  | Build  | Both  |

### 2.1 The three choices that carry weight

**AG-Grid Enterprise for every tabular surface.**

Bain already holds the licence, which makes this a Buy at no marginal cost that removes a real custom build. Raw data inspection, the peer candidate long list, cost bar decomposition, metric drill-down and dataset export all need virtualised rows, column grouping, aggregation, master-detail expansion and Excel export. Building that to a standard a partner would accept is weeks of work that produces something worse.

It also satisfies dataset export natively, so that capability needs no separate implementation.

*Rejected: TanStack Table with custom virtualisation.* A good headless library, but grouping, pivoting, master-detail and Excel export would all be ours to write, and the licence that removes that work is already paid for.

**AG-Grid and Vega-Lite are not competing, and the split is a rule.**

| Surface  | Tool  | Why  |
|---|---|---|
| Interactive tables inside the product  | AG-Grid  | Ephemeral. The user inspects, filters, expands and exports. Nothing persists into the content model  |
| Exhibits that travel into the deck  | Vega-Lite, Apache ECharts  | An Exhibit is a specification bound to data. It serialises, versions with the case, and renders identically into HTML, PDF and presentation  |

**Do not use AG-Grid Integrated Charts for exhibits.** They are grid-bound rather than specification-bound, so an exhibit built that way could not leave the browser as an object. The rule is that anything reaching the composition service is Vega-Lite, and anything the user only looks at is AG-Grid.

**Vega-Lite for exhibits, and not a charting component library.**

The business object model defines an Exhibit as a chart specification bound to data, not a rendered image. Vega-Lite is a specification grammar, so an Exhibit serialises to JSON, versions with the case, travels into the content model, and renders identically in HTML, PDF and presentation from one definition. A component library such as Recharts or ECharts is imperative: the chart exists only as React that has already run, so the Exhibit object would have no serialisable form and the format-neutral content model under ADR-006 would be broken by the first chart.

*Rejected:* Recharts, ECharts, Chart.js. All are good libraries and all would force the exhibit to become a rendering rather than a specification.

**Server-sent events, and not WebSocket.**

Run progress and partial results flow one direction. SSE survives Front Door without special configuration, reconnects itself, and needs no connection state on the server. WebSocket buys bidirectionality that nothing in the design uses, and costs sticky sessions and a connection registry.

*Rejected:* WebSocket, and polling. Polling at a four-minute run length either wastes calls or delays results.

### 2.2 Rejected framework alternative

**Next.js.** Server-side rendering buys nothing for an authenticated single-tenant workspace behind SSO, where no page is public and no page is indexed. It adds a Node rendering tier that has to be secured, scaled and patched, and it blurs the boundary the BFF exists to hold. Vite gives a faster build and a simpler threat surface.

## 3. Backend and compute

| Concern  | Choice  | Position  | Phase  |
|---|---|---|---|
| Service hosting  | Azure Container Apps  | Adopt  | Both  |
| Sandboxed execution  | Container Apps dynamic sessions  | Adopt  | Both  |
| IO-bound services  | Node with TypeScript  | Build  | Both  |
| Compute and AI services  | Python  | Build  | Both  |
| Default API style  | REST with JSON, OpenAPI first  | Build  | Both  |
| Calculation hop  | gRPC with protobuf  | Build  | Both  |
| Deck rendering  | Headless Chromium for HTML and PDF, OOXML writer for presentation  | Build  | Both  |
| Secrets  | Azure Key Vault references  | Adopt  | Both  |

### 3.1 Why Container Apps

*Rejected: AKS.* Kubernetes is the right answer at a scale this programme does not have. Concurrency is expected low, the component count is twenty-seven, and adopting AKS means adopting cluster upgrades, node pools, ingress controllers and a platform team to run them. None of that produces a better product here.

*Rejected: App Service.* No dynamic sessions, which the ad hoc dataset composition capability needs. Weaker per-revision mTLS and weaker event-driven scaling.

### 3.2 Two runtimes, split on a rule

The split is not preference. Node handles services whose work is IO and whose types are shared with the frontend: case, composition, rendering, evidence, audit, peer curation. Python handles services whose ecosystem is Python: the calculation engine, document parsing, the agent workers, and anything on a model path. A service that would need both is a service drawn wrong.

*Cost, stated:* two toolchains, two dependency scanners, two base images. Accepted, because forcing the calculation engine or the agent workers into Node would cost far more.

### 3.3 The calculation engine expression model

This answers the open question about what graph engineering means concretely, and it is the most consequential build decision in the programme.

**Decision.** A closed expression grammar with spreadsheet-familiar surface syntax, parsed to an abstract syntax tree, compiled into typed nodes in a dependency graph.

| Property  | Detail  |
|---|---|
| Node types  | Source metric, derived calculation, parameter, aggregation, adjustment, normalisation  |
| Grammar  | Arithmetic, comparison, conditional, a fixed function library, named references to semantic metrics  |
| Deliberately absent  | Loops, recursion, imports, file or network access, arbitrary function definition  |
| Authoring surface  | Looks like a spreadsheet formula, because the people authoring it live in spreadsheets  |
| Execution  | Deterministic. Memoised. Topologically ordered with cycle detection at compile time  |

**Why a closed grammar and not sandboxed Python.**

The absolute requirement is that a figure be re-derivable exactly, years later. A definition that can import a library cannot make that guarantee, because reproducing the figure in 2031 would require reproducing the interpreter and every transitive dependency as they stood in 2026. A closed grammar has no such surface: the AST is the definition, and the pinned definition version plus the pinned inputs plus the trace is a complete record.

Safety follows for free. There is no sandbox escape to defend against when there is no sandbox, which also removes the validation boundary problem for model-authored adjustment nodes down to a schema check rather than a security review.

*Rejected: sandboxed Python via RestrictedPython or asteval.* Familiar to authors, but determinism across years is not achievable and the escape surface is real.

*Rejected: a full custom DSL with unfamiliar syntax.* The grammar is custom either way; making it look unfamiliar buys nothing and costs adoption by the Bain stewards who will eventually author in it.

**The residual, named.** We own a parser. It is roughly a thousand lines and it is the price of the re-derivability guarantee. Every alternative that avoids writing it also breaks the guarantee.

## 4. Orchestration and AI

| Concern  | Choice  | Position  | Phase  |
|---|---|---|---|
| Agent orchestration  | Microsoft Agent Framework  | Adopt  | Both  |
| Deterministic long-running work  | Azure Durable Functions  | Adopt  | North star  |
| Scheduled connector glue  | Azure Logic Apps  | Adopt  | North star  |
| Models  | Azure AI Foundry  | Adopt  | Both  |
| Model gateway  | API Management GenAI gateway  | Adopt  | Both  |
| Content safety and PII  | Azure AI Content Safety  | Adopt  | Both  |
| Document parsing  | Azure AI Document Intelligence  | Adopt  | Both  |
| Tool contract  | MCP over streamable HTTP  | Adopt protocol, Build servers  | Both  |
| Agent delegation  | A2A over HTTPS  | Adopt  | Both  |
| Runtime evaluation  | Foundry evaluations  | Adopt  | MVP  |
| Offline regression  | Custom harness  | Build  | North star  |
| Semantic cache  | Redis semantic cache  | Adopt  | Both  |
| In-process vector similarity  | Zvec, in-memory, run-scoped  | Adopt OSS  | Both  |

### 4.1 Model selection is deliberately not made here

Named model generations go stale faster than this document will be read. Selection happens at deployment against current availability, constrained by the routing policy in the gateway rather than by a diagram. What is fixed is that every model call passes the gateway, so changing a model is a configuration change and never a code change.

### 4.2 No dedicated vector store, closing that open decision

**Decision.** Do not add a vector store at MVP or at north star, unless retrieval quality is measured to be insufficient.

SharePoint indexes documents natively for grounded generation and Foundry agents retrieve from it directly, which is the reason SharePoint earned its place at all. Adding AI Search, pgvector or Cosmos DiskANN would mean building the embedding pipeline the native path exists to avoid, plus a second copy of every document to keep in sync and to govern.

*Revisit trigger:* measured retrieval quality against a fixed evaluation set, not a hunch. If it fails, Azure AI Search is the first candidate because it keeps the managed-first position.

**The in-process exception.** Where a service needs vector similarity inside a single run, for example deduplicating peer candidates across discovery routes or clustering extracted passages before synthesis, it uses **Zvec** as an in-memory vector cache within the service process. This is a cache, not a store: it lives for the run, holds nothing durable, and appears on no data architecture. The distinction matters, because an in-memory index that survives a request would be a vector store by another name and would carry every governance obligation this decision avoided.

### 4.3 Rate limiting is a custom component, and that is a known cost

Neither orchestration substrate has a native concept of an external API quota. The rate limiting component in the integration layer is a genuine custom build that ADR-008 identified and that nothing since has removed. Event Hubs flow control and Service Bus can reduce it but not eliminate it.

Its design is blocked on CapIQ rate limits and per-call cost, which remain unanswered. Until then it is built to a conservative default and made configurable.

## 5. Data

| Concern  | Choice  | Position  | MVP  | North star  |
|---|---|---|---|---|
| Application state  | Azure SQL Database  | Adopt  | Serverless General Purpose  | Provisioned  |
| Audit trail  | Azure SQL ledger tables  | Adopt  | Yes  | Yes  |
| Audit immutability  | Immutable blob with a legal hold policy  | Adopt  | Yes  | Yes  |
| Session and cache  | Azure Cache for Redis  | Adopt  | Yes  | Yes  |
| Per-run analytical files  | Parquet  | Adopt format  | In SharePoint  | In ADLS Gen2  |
| Query engine  | DuckDB, embedded in process  | Adopt OSS  | Yes  | Yes  |
| Documents  | SharePoint  | Buy, existing  | Documents and parquet  | Documents only  |
| Warehouse  | Snowflake  | Buy  | Absent  | Bronze to platinum  |
| Bronze to silver transformation  | dbt  | Build on OSS  | Absent  | Yes  |
| Silver to gold  | The calculation engine  | Build  | Per run only  | Warehouse gold  |

### 5.1 Why DuckDB and not a query service

DuckDB is a library, not a server. It runs inside the Data Access Service process, reads parquet directly, and stores nothing. That means no cluster to size, no service to secure, and no additional store on the data architecture. At this scale, loading a case version's parquet into memory and querying it is faster than any round trip to a query service would be.

*Rejected: Azure Synapse Serverless, Databricks SQL.* Both are the right answer for a warehouse workload. Neither is the right answer for reading one case's files.

### 5.2 dbt for bronze to silver, the engine for silver to gold

This is a genuine decision with a real alternative, so it is stated as one.

Silver's job is to answer, for any figure, exactly how it was derived. Lineage is dbt's native output rather than something built alongside it, and the transformations at that layer are declarative SQL that a data engineer should be able to read without reading application code.

Gold stays in the calculation engine because there must be one calculation authority. Splitting calculation between a warehouse transformation tool and the engine would recreate exactly the problem that bypassing VCC removed.

*Rejected: hand-written SQL orchestrated by Durable Functions.* Fewer tools, but lineage becomes something we maintain by hand at the one layer whose purpose is lineage.

*Rejected: putting silver in the engine too.* The engine would then need to run as a batch job over the whole warehouse, which is a different operational profile from a service on a user-facing path.

### 5.3 Serverless SQL at MVP

Concurrency is expected low and usage is likely bursty around deal cycles. Serverless pauses when idle and bills for what is used, which suits an MVP with a hundred partners better than a provisioned tier sized for a peak nobody has measured. Auto-pause is disabled to avoid a cold start on the user-facing path.

*Revisit trigger:* sustained load making provisioned cheaper, or a latency floor that pause and resume cannot meet.

## 6. Integration and messaging

| Concern  | Choice  | Position  | Phase  |
|---|---|---|---|
| Command and event transport  | Azure Service Bus  | Adopt  | Both  |
| Progress fan-out  | Redis pub/sub to SSE  | Adopt  | Both  |
| Notification  | Microsoft Graph, Outlook  | Buy, existing  | Both  |
| Controlled egress  | NAT Gateway with a static IP  | Adopt  | Both  |
| External source rate limiting  | Custom component  | Build  | Both  |
| Source credentials  | Key Vault references  | Adopt  | Both  |

**Service Bus and not Event Grid or Storage Queues.** Run commands need competing consumers, dead-lettering, sessions and delivery guarantees. Progress events need topic fan-out. Service Bus does both, and using one broker for both rather than two products is worth more than the marginal cost difference.

## 7. Identity and security

| Concern  | Choice  | Position  | Phase  |
|---|---|---|---|
| Single sign-on  | Okta  | Buy, existing  | Both  |
| Authorisation and tokens  | Microsoft Entra ID  | Buy, existing  | Both  |
| Service to service  | Entra managed identities  | Adopt  | Both  |
| Platform consumer identity  | OAuth2 client credentials, separate audience  | Adopt  | North star  |
| Warehouse identity  | Entra external OAuth to Snowflake  | Adopt  | North star  |
| Perimeter  | Front Door Premium with WAF  | Adopt  | Both  |
| Gateway  | API Management  | Adopt  | Both  |
| Network  | Private endpoints, Private DNS, public access disabled  | Adopt  | Both  |
| Posture management  | Microsoft Defender for Cloud  | Adopt  | Both  |
| Document-level access  | SharePoint, Entra-backed  | Buy, existing  | Both  |

**No password exists anywhere in the system** except source API keys, which sit in Key Vault as references and are never materialised into configuration. This is the single sentence to put in front of a CISO.

## 8. Observability

| Concern  | Choice  | Position  | Phase  |
|---|---|---|---|
| Traces, metrics, logs  | Azure Monitor with Application Insights  | Adopt  | Both  |
| Instrumentation standard  | OpenTelemetry  | Adopt  | Both  |
| Agent and model tracing  | Agent Framework native spans  | Adopt  | Both  |
| Token and cost accounting  | At the model gateway  | Adopt  | Both  |
| Product analytics  | Pendo  | Buy, existing  | Both  |
| Warehouse access lineage  | Snowflake access history  | Buy  | North star  |
| Alternative APM  | Datadog  | Buy, optional  | Both  |

**Audit is not telemetry.** The audit trail answers who changed what, when, and why they said they did. Telemetry answers what the system did. They have different retention, different immutability and different readers. Putting the audit trail in the observability stack is a mistake that is expensive to reverse, and it is why they appear as different stores on the data architecture.

## 9. Testing

### 9.1 Why the standard pyramid does not fit

In a conventional system the expensive, slow, unreliable tests sit at the top and there are few of them. Here the unreliable layer is in the middle: the agents and models that produce peer sets, claims and narrative are non-deterministic by design, and no amount of test engineering makes them otherwise.

**Two tracks, tested differently.**

| Track  | Covers  | Assertion style  |
|---|---|---|
| **Deterministic**  | Frontend, services, calculation engine, data transformations, infrastructure  | Exact. Same input, same output, every time  |
| **Probabilistic**  | Agents, model output, retrieval, ranking  | Invariants and distributions. Never exact strings  |

The boundary between them is a design property worth protecting. The calculation engine is deterministic on purpose, which is what makes a figure defensible and also what makes it exhaustively testable. Anything that moves logic across that line from the deterministic side to the probabilistic side makes the system both less defensible and less testable at once.

### 9.2 Deterministic track

| Layer  | Stage  | Tool  | What it asserts  |
|---|---|---|---|
| Frontend  | Unit and component  | Vitest with Testing Library  | Component behaviour, state transitions, tool-call handling  |
| Frontend  | Accessibility  | axe-core inside Playwright  | WCAG 2.2 AA on every route  |
| Frontend  | End to end  | Playwright  | Stage progression, drill-down, assistant actions, export  |
| Frontend  | Visual regression  | Playwright screenshots  | Deck rendering fidelity across HTML, PDF and presentation  |
| Services, Node  | Unit  | Vitest  | Domain logic in isolation  |
| Services, Python  | Unit  | pytest  | Domain logic in isolation  |
| Services  | API contract  | Schemathesis against OpenAPI  | The implementation matches the schema, including cases nobody wrote a test for  |
| Services  | gRPC contract  | buf breaking-change detection  | The calculation contract cannot break a consumer silently  |
| Services  | Integration  | Testcontainers: SQL Server, Redis, Azurite  | Real substrates, not mocks. DuckDB is in process and needs no container  |
| Calculation engine  | Property based  | Hypothesis  | Determinism, commutativity where claimed, cycle rejection, unit and currency invariants  |
| Calculation engine  | Golden fixtures  | pytest with pinned cases  | A known set of inputs produces a known set of figures, byte for byte  |
| Calculation engine  | Re-derivation  | Trace replay  | A stored trace plus pinned definition versions reproduces the original figure exactly  |
| Data  | Transformation  | dbt tests  | Uniqueness, referential integrity, accepted values, freshness, at bronze to silver  |
| Infrastructure  | Policy  | PSRule for Azure, Checkov  | Private endpoints present, public access disabled, no inline secret  |
| Infrastructure  | Plan review  | Terraform plan or Bicep what-if in the pipeline  | No unreviewed change reaches an environment  |

**The three engine test types are the important ones.** Property-based tests find the cases nobody thought of. Golden fixtures catch a regression the moment a definition or the evaluator changes. Trace replay is the only test that directly verifies the re-derivability guarantee the whole evidence model rests on, and it should run against a growing corpus of real completed cases rather than synthetic ones.

### 9.3 Probabilistic track

Four loops, in increasing cost and decreasing frequency.

| #  | Loop  | When  | Tool  | What it asserts  |
|---|---|---|---|---|
| 1  | **Structural invariants**  | Every run, in production  | Application code  | Every claim has an evidence binding. Every figure has a trace. Every adjustment names its authority. No opportunity references a metric that does not exist. These are cheap, absolute, and fail the run rather than the deployment  |
| 2  | **Runtime judges**  | Every run, in production  | Foundry evaluations  | Groundedness of extracted claims against their source passage. Faithfulness of narrative to the analysis it summarises. Verification intensity scales with the effort budget  |
| 3  | **Offline regression**  | Every prompt, tool or model change  | Custom harness against a golden dataset  | Peer set overlap against a reference set above a threshold. Opportunity ranking stability. Claim extraction recall. Aggregate scores, never individual strings  |
| 4  | **Human review**  | Before a release and on a sample  | Structured review by an analyst  | Whether the output is any good. Nothing above answers this and nothing will  |

**Assert on invariants, not on strings.** A test expecting a specific sentence from a model is a test that fails on an unrelated prompt improvement. A test asserting that peer set overlap against a reference set stays above a threshold survives model changes and still catches a real regression.

**The golden dataset is a deliverable, not a by-product.** A fixed set of target companies with reviewed reference peer sets, expected opportunity themes and known-good claims. It has to be built deliberately and versioned, and without it loop 3 has nothing to compare against.

### 9.4 Security and adversarial

| Concern  | Tool  | Cadence  |
|---|---|---|
| Static analysis  | CodeQL via GitHub Advanced Security  | Every pull request  |
| Dependency vulnerabilities  | Dependabot with alerts as blocking  | Continuous  |
| Container image scanning  | Microsoft Defender for Cloud, Trivy in the pipeline  | Every build  |
| Secret scanning  | GitHub secret scanning with push protection  | Every push  |
| Dynamic application testing  | OWASP ZAP against staging  | Nightly  |
| AI red teaming  | PyRIT  | Every release, and on any change to the tool contract  |
| Prompt injection corpus  | Curated regression suite  | Every prompt change  |

**Prompt injection is a test suite, not a control.** Content Safety at the gateway is the control. The regression suite exists to prove the control still works after every change, and to grow whenever a new technique appears. The realistic attack surface here is an uploaded document or a retrieved web page carrying instructions, so the corpus is built from those two shapes specifically.

### 9.5 Performance

| Assertion  | Target  | Tool  |
|---|---|---|
| Synchronous path  | 2s at p95  | Azure Load Testing with k6  |
| Full run, end to end  | Under 30 minutes wall clock  | Scenario test against a reference case  |
| Peer fan-out  | Measured against the proof of concept baseline of 10 to 12 peers in 3.5 to 4 minutes  | Scenario test  |
| Progressive delivery  | First partial result visible within 30 seconds of run start  | Playwright with timing assertions  |

The 2s ceiling is a StatusNeo assumption rather than a Bain requirement, and the test suite is where it stops being an assumption and becomes a commitment. If it turns out to be wrong, this is where that surfaces.

### 9.6 Test data policy

| Rule  | Reason  |
|---|---|
| No production document ever reaches a test environment  | Uploads may carry MNPI or PII. There is no safe way to hold them outside production  |
| Synthetic companies for functional tests  | Named fictitiously, with a full metric profile, so tests do not depend on a live source  |
| One pinned CapIQ snapshot for the golden dataset  | Real data, frozen, licensed for internal use, small enough to version  |
| Source responses recorded and replayed  | Integration tests must not consume live API quota, which is a constrained resource  |
| Warehouse tests run against a masked subset  | Structure preserved, values obfuscated  |

### 9.7 Pipeline gates

| Stage  | Runs  | Blocks merge  |
|---|---|---|
| Pull request  | Unit, contract, lint, CodeQL, secret scan, dbt compile  | Yes  |
| Merge to main  | Integration with Testcontainers, engine golden fixtures, property tests, image scan  | Yes  |
| Deploy to staging  | End to end, accessibility, visual regression, infrastructure policy  | Yes  |
| Nightly  | DAST, load, trace replay against the full corpus, offline model regression  | Alerts, does not block  |
| Pre-release  | AI red team, human review sample, full performance scenario  | Yes  |

**Offline model regression does not block a merge.** It is a signal about model behaviour rather than about code correctness, and blocking on it would mean a model provider's change could stop the team shipping unrelated work. It blocks a release instead, which is the point at which it matters.

## 10. Build versus buy

### 10.1 The count

| Position  | Components  | Share  |
|---|---|---|
| Build  | 24 of 27  | Includes the domain services, which are custom by definition  |
| Adopt  | 3 of 27  | Model gateway, orchestration platform, batch orchestrator  |
| Buy  | 11 external systems  | Of which only three realise a capability outright  |

That count flatters the custom build, because a domain service is custom by definition and says nothing about differentiation. The useful question is narrower.

### 10.2 Where custom is genuinely warranted

Five builds where no managed option exists and the capability is differentiated. Everything else is either domain code sitting on adopted infrastructure, or adopted outright.

| #  | Build  | Why no managed option fits  |
|---|---|---|
| 1  | **Calculation engine**  | Governed, versioned, scope-resolved deterministic calculation with a derivation trace as a first-class output. No managed service does this. It is also the one component Bain can reuse, which is the argument for building it as a service on day one  |
| 2  | **Definition registry**  | Business-authored definitions with versioning that never overwrites, scope binding with inheritance, and dry-run validation. Adjacent products exist for feature stores and metric layers; none carries the scope hierarchy or the authoring lifecycle this needs  |
| 3  | **Evidence and provenance service**  | Two claim producers, one evidence contract, licensing enforcement in one place, and drill-down from a rendered claim to a raw input in one traversal. This is the product's defensibility and it has no off-the-shelf shape  |
| 4  | **Composition and template engine**  | Bain supplies brand assets; the engine that turns a format-neutral content model into HTML, PDF and presentation is ours. Confirmed by Bain  |
| 5  | **External source rate limiting**  | Neither orchestration substrate has a native external quota concept. A known residual cost, not a preference  |

### 10.3 Where we deliberately did not build

| Concern  | What we adopted instead  | What building it would have cost  |
|---|---|---|
| Tamper-evident audit  | SQL ledger tables with digests to immutable blob  | A hand-rolled hash chain, and the burden of proving it correct  |
| Vector retrieval  | Native SharePoint indexing  | An embedding pipeline, a second copy of every document, and a sync problem  |
| Agent orchestration  | Microsoft Agent Framework  | Graph validation, tracing, and effort budget propagation, all rebuilt  |
| Document parsing  | Azure AI Document Intelligence  | A parser per format, maintained forever  |
| Content safety and PII redaction  | Azure AI Content Safety at the gateway  | Redaction logic duplicated in every service that touches a model  |
| Query engine  | DuckDB embedded  | Nothing sensible. This one was never a real question  |

## 11. MVP to north star delta

Phase tags alone would show 31 new capabilities and understate this transition badly. The realisation change is the larger half of it.

| Layer  | MVP  | North star  | Nature of change  |
|---|---|---|---|
| Frontend  | Guided workspace and assistant  | Plus self-service authoring surface, branch and compare  | Additive  |
| Compute  | Container Apps  | Unchanged  | None  |
| Orchestration  | Agent Framework only  | Plus Durable Functions and Logic Apps  | Additive substrate  |
| Data acquisition  | Real-time fetch per run  | Monthly batch for CapIQ, VCC and AURA; run-time for the rest  | **Mechanism change**  |
| Analytical substrate  | Parquet in SharePoint under a case  | ADLS Gen2 plus a Snowflake warehouse  | **Mechanism change**  |
| Semantic layer  | Absent  | Platinum layer serving business meaning  | New  |
| Lineage  | Inside a case version  | Across the warehouse, in silver  | **Mechanism change**  |
| Definition authoring  | Engineering-mediated through source control  | Self-service for a Bain steward  | **Mechanism change**  |
| Application state  | Azure SQL, ledger, Redis  | Unchanged  | None  |
| Consumers  | OI 3.0 only  | Plus other Bain teams via the platform API and platinum layer  | **New trust boundary**  |
| Evaluation  | Foundry evaluations at runtime  | Plus adversarial judges and offline regression  | Additive  |
| Trust boundaries  | Five  | Six  | New boundary  |

**The four mechanism changes are the story.** A delta view showing only new capabilities would miss all four and would be the first thing a Bain architect challenged.

## 12. Decisions taken in this document

Choices that no ADR covered and that are settled here. Each is open to reversal, and each names what it would cost.

| #  | Decision  | Reversibility  |
|---|---|---|
| T1  | Vega-Lite, Apache Echarts for exhibits  | High cost. The exhibit object shape depends on it  |
| T2  | Server-sent events over WebSocket  | Low cost. Transport only  |
| T3  | React with Vite, not Next.js  | Moderate. A rewrite of the shell, not the app  |
| T4  | Container Apps, not AKS  | Moderate. Containers move; the environment does not  |
| T5  | Two runtimes split on IO versus compute  | High cost to unify later  |
| T6  | Closed expression grammar for calculation definitions  | Very high. Every authored definition depends on it  |
| T7  | No dedicated vector store  | Low. Adding one later is additive  |
| T8  | dbt for bronze to silver  | Moderate. Transformations are portable SQL  |
| T9  | Serverless SQL at MVP  | Low. A tier change  |
| T10  | Separate APIM product for platform consumers  | Low, and much higher if deferred  |
| T11  | AG-Grid for tables, Vega-Lite for exhibits, with a rule between them  | Low for AG-Grid, high for Vega-Lite  |
| T12  | Zvec as a run-scoped in-memory vector cache, never a store  | Low. It holds nothing  |
| T13  | Two testing tracks, deterministic and probabilistic, asserted differently  | High. It shapes what the suite even measures  |
| T14  | Offline model regression blocks a release, not a merge  | Low. A pipeline setting  |

## 13. Open items

Each blocks a specific decision rather than the document as a whole. All are now StatusNeo-owned.

| #  | Item  | What it blocks  |
|---|---|---|
| 1  | **Foundry network isolation**  | Some features, tracing and workflow agents among them, do not yet fully support network isolation. This decides whether the AI zone can be fully private or needs a compensating control. Largest unresolved item in the set  |
| 2  | CapIQ rate limits and per-call cost  | The rate limiting component's design, and whether real-time fetch survives at 2300 users  |
| 3  | Availability target  | Whether anything needs a second availability zone  |
| 4  | Audit retention period  | Digest publication cadence, and storage sizing  |
| 5  | Role set per case and what each role gates  | Entitlement enforcement logic at the BFF  |
| 6  | MNPI enforcement in product or by policy  | Whether per-document access control is MVP or later  |
| 7  | Case state machine, archival and deletion semantics  | Retention and disposal behaviour  |
| 8  | The golden dataset for offline evaluation  | Loop 3 of the probabilistic track. It needs Bain analyst time to build reference peer sets, and nothing substitutes for that  |
