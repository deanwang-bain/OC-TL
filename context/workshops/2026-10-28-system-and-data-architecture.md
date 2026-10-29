# Sprint 5 workshop — system and data architecture, 28 October 2026

*Source: `videos/Sprint 5 workshop System and data architecture (Dipesh)-20261028_150650-Meeting Recording.mp4`
(1 h 40 m) and its Teams transcript `…-en-US.vtt`, supplied locally — **not in Confluence, and
gitignored**. The transcript is auto-captioned with no speaker labels, so attributions below come
from context, and names are garbled in it ("Deepesh", "Port Key", "Cloud Opus 55", "intro ID").
Everything read off the shared screen is cited by timestamp; see the table at the end.*

**Presenter:** Dipesh Bhardwaj (SN). **Main questioner:** Sandeep Uppal, named *Architect* on the
[space home page](../../confluence/oi30-19588841975.md). Also present: Nikolozi Metreveli, and
Abbas Mohammed, Aleksandrs Bereznickis, Lakshay Grover and Giorgi Samadashvili, all marked
**(Vendor)**. Siva Vyra (Data Architect) joined late. The Tech Lead was not on the call.

This is the **first of a workshop series**; Sandeep said the later ones "build on top of it". Named
as coming: database migrations, deployment, company search, agent demos, and a session reviewing
SN's ADRs against **Bain's agentic standards**, a set of files Sandeep has shared with SN that are
not in the mirror.

## What matters, in eight lines

1. **The architecture that is being built is documented outside Confluence**: a Miro board
   (*OI Architecture (HL)*), SN's in-repo docs, and an HTML "Architecture journey portal". The
   Confluence diagrams are older than all three.
2. **SN keeps its own ADR series, ADR-0001 to ADR-0045**, in `docs/engineering/decisions/`. The
   numbers collide with Confluence's ADR-001–009, and several of them reverse those ADRs.
3. **The GLS build runs under eleven waived invariants** (EX-0001–EX-0011), all expiring
   **31 December 2026**. The BFF holds the domain data, does the financial arithmetic and bypasses
   the hash-chained audit trail. None of these waivers is machine-checked.
4. **Agents call `gpt-5.2` and `claude-opus-5-5` directly**, with no gateway. Claude Opus 5.5
   *writes the output deck*. The intended gateway is **Portkey**, not the APIM GenAI gateway that
   Technology Choices adopts.
5. **The build departs from ADR-009 and Technology Choices in at least seven places**: Postgres
   rather than Azure SQL, a hand-rolled audit hash chain, a Redis container, the gateway, embedding
   residency, no agent orchestration, and REST rather than gRPC. Table below.
6. **The dev security posture is visibly below target**: WAF in detection mode, a Postgres
   "public with selected IP" commit, secret and code scanning off, **174 open Dependabot alerts**,
   CI secrets in GitHub rather than a vault, and agent tool calls crossing the public internet.
7. **gRPC is settled.** The calculation engine exposes REST for the MVP (repo ADR-0013).
8. **Several product questions were handed to the business**, Stephanie and Noah: business-unit
   versus company-level peers, parent/subsidiary handling, and document reuse across cases.

## Where the real architecture lives

| Artefact | What it holds | In the mirror? |
| -------- | ------------- | -------------- |
| Miro board *OI Architecture (HL)* | Lane 3: component diagrams (company search). Lane 4: the current diagrams — *system overview*, *MVP Azure infrastructure reference*, *dev and GLS staging on Azure*, *where data lives*. Also a two-year-old Azure service-broker reference architecture Sandeep shared, kept for comparison | No |
| `nextgen-opportunity-catalyst-core/docs/` | `engineering/` (ADRs, per-service engineering notes, e.g. the audit trail), `gls/` (the GLS source of truth, including its exceptions), `agents/`, stakeholder communication | No |
| `utilities/journey-docs/journey-portal` | An HTML portal: 11 logical services, journeys `00a-employee-login` to `02g-stream-case-events`, a data catalogue (14 datasets, 293 columns), lineage (4 DAGs), the medallion layers per column, and a list of 21 blockers | No |
| Infra repo `nextgen-opportunity-catalyst-infra` | Terraform (HCL). README still titled *…opportunity-indicator-infra* | No |

Siva Vyra asked for repo access to read the medallion HTML because **"the data [is] onboarded next
week"**. That wording is ambiguous: it is either a data engineer starting or the data arriving.
Either way, the Data Architect does not yet have access to the repository that documents the data
product.

## The system as built

### Edge and identity *(system overview, 04:40; infrastructure reference, 26:36)*

- **Azure Front Door Premium with WAF.** Routes go over Private Link: `/*` to the SPA App Service,
  `/bff/*` to Experience BFF, and `/internal/v1/companies/*` to company-search. Agent-callable
  services get "one route per service, added as they are exposed".
- **Entra ID**: user SSO (OIDC), with experience-bff as the confidential client. **Tokens never
  reach the browser**, and the session is held server-side. Every service and every agent has its
  own managed identity, and *"each service checks the caller's Entra token: audience and role."*
- Sandeep's standing security requirement: **every API registered as an Entra app, with the user
  re-authenticated on every call**. Dipesh replied "that's exactly how we do it".
- **No API gateway in front of the BFF**, on the reasoning that there is one browser-facing
  surface. MCP is coming, so APIs should be designed with it in mind.
- Target domain `<env>.opcat.bain.com`. Dev has **no custom domain yet** and signs in on the
  `azurefd.net` endpoint; staging is `bain.io`.

### Services — Container Apps, Germany West Central

| Service | What it does today |
| ------- | ------------------ |
| experience-bff | The only browser-facing service. Orchestrates everything behind it; also the BFF for the chat agent. **TypeScript** (`src/app.ts`, `*.test.ts`), not FastAPI |
| identity-service | The token handshake |
| case-service | Case lifecycle and case metadata. Target-setup settings live here |
| compliance-service | **An empty pass-through.** Meant as the gate for policies such as "this partner may not work on these companies". No policy exists to put in it |
| audit-service | Write-once audit, **hash-chained** (each row carries the previous row's hash), with digests to WORM storage. Transactional outbox, so a write and its audit record commit together |
| company-search-service | In-memory index loaded at start-up via DuckDB from blob Parquet. Ticker, fuzzy, BM25 and character-trigram search. **The alias index has 0 rows**: there is no alias data, so a company cannot be found by another name |
| evidence-service | Claims and their evidence — overrides, which source won, and so on. Same immutability as audit |
| peer-curation-service | The whole propose-peers journey. Calls the peer-discovery agent |
| realtime-service | SSE. Consumes the Service Bus case stream and pushes to the browser through the BFF |
| document-service | **Designed, not hosted.** Upload is a basic blob write today |

Plus `bff-session-redis`, a container app (below). Each service owns its own Postgres schema, so
*"if you federate the database tomorrow, that can be easily done."* That is the operating answer to
the store-ownership finding in `reviews/2026-09-01-adr-001-to-009.md`. It is not written on any
Confluence page.

### Agents and models *(system overview, 04:40 and 22:52)*

- **Foundry Agent Service, Sweden Central**: peer-discovery, chat-assistant, gls-narrative,
  deck-planner and deck-writer, matching the `agents/` folder in the repo. Called over HTTPS with an
  Entra token. *"Agents read platform data only through governed tools via Front Door, and hold no
  data stores of their own."*
- **Model deployments, Sweden Central**: `gpt-5.2` for chat and reasoning, **`claude-opus-5-5`,
  which "writes the output deck"**, and `text-embedding-3-small` (*designed*) for embeddings. The
  2 October infrastructure diagram also lists `gpt-4.1`.
- **No agent orchestration.** One agent per job; services call agents, and agents make tool calls
  back to services. Fan-out is plain async Python that waits for all results, with *"no very fancy
  orchestration or graph behind the scenes."* A2A or agent-as-tool are possible later.
- **Tool calls return over the public internet.** Foundry sits outside the VNet: egress goes out
  through one static IP, and agent tool calls come back in through Front Door. Sandeep called this a
  security risk and wants Foundry in the same zone, behind a private endpoint, at UAT.
- **Portkey AI gateway "will sit on every model call"**, covering agent chat and reasoning plus
  document-service embeddings. It is *designed*, not built. Sandeep: *"all model calls have to go
  via Portkey."* Whether Portkey also serves as the MCP registry is undecided; there is no central
  Bain MCP registry.
- **Cosmos is dropped.** *"Foundry provides its own database"* for agent threads, so chat threads
  live in Foundry-managed storage in Sweden Central. The 2 October diagram still shows Cosmos for
  agent threads.

### Data *(where data lives, 35:30)*

- **Company data, built offline**: CapIQ Excel export → `data-product` (bronze → silver → gold,
  **calculation engine in-process**) → search index builder → blob `company-search` (index plus
  silver/gold Parquet) → company-search-service loads it in memory. Every search artefact carries a
  version, a snapshot ID and per-segment SHA-256 fingerprints, as does the entity normaliser.
- **Case data, written as people work**: BFF → case-service and peer-curation-service (Postgres) →
  peer-discovery agent → evidence-service (Postgres plus blob) → case stream on Service Bus →
  realtime-service → browser.
- **Postgres** holds frequently changing, relational data, with Alembic migrations hash-tracked in
  one `database/` project. **Snowflake** is for slow-moving data such as CapIQ (north star).
  **Blob** holds case documents under the case ID. **Redis** holds *"just sessions"*, plus the
  golden data set on stage.
- **No vectors today.** Company search does not need semantic search. Sandeep: *"if we ever use
  embeddings, since we are already using Postgres, we should use pgvector."* That contradicts the
  authoritative Document Upload design (Azure AI Search). Event Grid appears only as *blob-created
  events into Service Bus* (designed), so Service Bus remains the broker.
- **Observability**: every service emits OpenTelemetry to Azure Monitor and Application Insights,
  queryable with KQL. The backend is "a configuration choice", Azure Monitor or Datadog. This is
  the as-built answer the blank Observability page does not give, though it is still not a
  standard.

### GLS mode — the `stage` branch *(docs/gls/overview.md, 1:30:40–1:31:05)*

`stage` is **536 commits ahead of `main`**. With `OC_GLS_MODE=on` the BFF answers its existing
routes from GLS adapters: *"after [sign-in] no domain service and no Postgres table is touched."*
All GLS code is in `services/experience-bff/src/gls/`. Its `calc/` folder is **a port of `calc.py`
into the BFF**, tested against BCN's golden reference outputs; `services/calculation-engine/` is
not touched. Case copies, mutation logs, idempotency replay and per-turn agent grants are stored as
Redis keys (`gls:case:<case-id>:<user-id>`, `gls:grant:*`), and events go to a Redis Stream per
case — *"no realtime-service, no Service Bus."*

The golden data lives **outside git**. It is loaded by hand: a SAS URL from blob through Azure
Cloud Shell, then the `gls:load` script run inside the BFF container. It arrived from BCN as Excel
and PowerPoint, which SN converted to JSON. **After GLS it becomes the evaluation set** for live
source connections. That is a sound plan, and it answers part of standing agenda item 4.

**The eleven exceptions.** Each one is listed in `services/experience-bff/service.json`, with
"owner ruling B33" as the authority, and each expires **2026-12-31T00:00:00Z**. They are
deliberately *not* filed under `governance/service-standards/exceptions/`, because *"a waiver
there must name a control the checker implements, and none of these rules is one."*

| Id | The rule GLS relaxes |
| -- | -------------------- |
| EX-0001 | The BFF owns no domain database |
| EX-0002 | **No financial formula or arithmetic in the BFF, not even rounding** |
| EX-0003 | Peer sets belong to peer-curation-service |
| EX-0004 | Domain owners enforce permissions, versions and idempotency |
| EX-0005 | Every BFF answer comes from a named, frozen owner operation |
| EX-0006 | **The case audit trail is audit-service's hash-chained record** |
| EX-0007 | The case stream is realtime-service's, one producer per event type |
| EX-0008 | **Agents have no write tools** (lifted for every agent by ADR-0045 on 17 October) and the chat bridge holds no state or logic |
| EX-0009 | Every BFF route except the login pair sits behind the session hook |
| EX-0010 | No data served by configuration other than domain services outside the local tier |
| EX-0011 | A relay returns the owner's reply as the owner's own contract defines it |

Sandeep framed this table as the checklist for the rewrite, and Dipesh agreed. Alex ("Alex" in
the transcript; Aleksandrs Bereznickis) added the follow-on cost:
the chat assistant's tool catalogue points at BFF endpoints, so when GLS code moves into its
services, the tool catalogue and the agent's context management must move with it. SN plans that
as a migration task.

### Contracts and enforcement *(52:20–1:16:45)*

`contracts/` has four folders: `audit-events`, `case-stream`, `search-artifact` and `agents`.
Schemas are JSON Schema (json-schema.org), written by hand without a library. They are checked at
four points: **the CI gate, tests, build, and runtime**, where a non-conforming event, or one from
the wrong producer, goes to the dead-letter queue.

- **The audit envelope** carries `schema_version`, `event_id` (the outbox receipt),
  `correlation_id` / `causation_id` / `traceparent`, `occurred_at` (fixed lexical form, hashed
  byte for byte), `producer`, `tenant_id`, `resource`, and
  `actor {actor_id, kind: human|agent|service, on_behalf_of}`. The actor is derived from the
  verified caller, never from input. **An agent acting for a user is recorded as the agent, on
  behalf of the user**; it never assumes the user's identity. Sandeep pressed this point and it is
  built.
- **Case stream** events: peer run started, completed and failed; member changed; confirmed; audit
  recorded; agent notes (reserved, unused).
- **Ordering**: Service Bus delivers at least once, with no sequence numbers. Consumers process
  events as they arrive. **No dependency graph exists**, which bears directly on the "re-run only
  the affected modules" constraint in the brief.
- **Agent contracts** (`budget`, `eval`, `delegation`, `model-gateway`, `policy-catalog` 1.3.0,
  `tool-catalog`, `progress-stream`, `foundry-compatibility`, `control-coverage`) are baked in by
  the scaffolder. **At runtime the only check is that the budget and eval files exist.** Dipesh
  called that "the gap we need to fulfil".

### Scaffolder and shared packages *(1:17:20–1:25:10)*

- `tools/service-scaffolder` is a Textual terminal UI. It asks for a profile (for example a Python
  API service) and a capability set (plain, Postgres, Postgres inbox/outbox and so on), then a
  service name, capability ID, purpose, non-goals, owner, data classes and journeys. It generates
  the Dockerfile, AGENTS file, contracts and source. A policy-version template and a SHA hash catch
  drift.
- **There is one owner for every service**, `opportunity_catalyst_team`: *"small team, everyone
  owns everything."*
- **Data classification does not change what gets generated.** *"Recorded in service.json for
  review; the generator does not change its output by class."* Against the VCC meeting's rule that
  partner uploads are red by default and isolated *by design*, the classification is a label, not a
  control.
- **Duplication is the known cost**: scaffolded code is copied into all ten services. The planned
  fix is for services to read scaffolder code by repo path, injected at build time; eventually it
  becomes an SDK package once a registry exists (repo ADR-0026).
- **`entity-normaliser`** turns "The Coca-Cola Company" into "coca-cola", transliterates
  (Nestlé → nestle) and builds character trigrams. Pitched as a package any Bain team could reuse.

### The second ADR series *(docs/engineering/decisions.md, 1:31:58)*

*"Short stable entries… numbers stay global and are never reused."* The decisions that matter most
for this workspace:

| Repo ADR | Decision | Bears on |
| -------- | -------- | -------- |
| 0004 | `python-agentic-worker` is rejected, not deprecated | — |
| 0005 | `python-grpc` stays reserved | Standing agenda 11 |
| **0013** | **The calculation engine exposes REST for the MVP** | Settles standing agenda 11 |
| 0016 | The BFF terminates TLS locally and nowhere else | — |
| **0021** | **The audit trail is hash chained on the queryable table** | Reverses ADR-009 and Technology Choices §10.3 |
| 0022 | Company search is an in-process matcher; the bake-off is waived | — |
| 0024 | company-search-service absorbs entity-data-service and is reclassified confidential | — |
| 0025 | Company search emits no audit event | — |
| **0028** | **Agents are generated, governed and never services** | ADR-008's orchestration |
| **0029** | **The model is one configured Responses endpoint** | Gateway question |
| 0031 | peer-curation-service owns peer sets, runs and versions | Store ownership |
| 0040 / 0042 / 0043 | An agent acts for a user and the user's case role decides; owners verify a signed case grant; a chat is bound to its person and case | — |
| 0041 | Agent chat streams Responses and only reads | — |
| **0045** | **A chat write is a reversible backend tool decided in the user's own turn** (17 October) | Lifts the agents-read-only rule |

Sandeep asked for a dedicated session to go through these against Bain's agentic standards. They
are, in effect, the live design record. Confluence ADR-001–009 are still "pending Bain architect
review", and the Bain architect is Sandeep.

### Delivery and security posture

- **Repository**: `Bain/nextgen-opportunity-catalyst-core`, private, 173 branches, 1,497 commits,
  334 deployments, 32 issues, 7 PRs. Four contributors: Dipesh Bhardwaj, Anand Kirori, Aleksandrs
  Bereznickis and Lakshay Grover.
- **SN builds with Claude Code.** `.claude/skills/codebase-security-review` sits at the repo root,
  commits are co-authored by `claude`, and the editor status bar shows Claude Code. This is not a
  finding by itself; it is worth knowing when reviewing.
- **GitHub security**: Dependabot is on, with **174 open vulnerabilities**, some critical, "mostly
  on one package" (garbled in the transcript; probably aiohttp), to be cleared in Sprint 5.
  **Secret scanning, code scanning, code quality and a security policy are all disabled.** Wiz is
  attached; Sandeep can see the dashboard, the team cannot, and the promised Teams alerts have not
  arrived.
- **CI/CD secrets** are GitHub Environment secrets (for example the BFF OIDC client secret).
  Non-sensitive configuration lives in `deploy/azure/settings/{example,dev}`. Sandeep's concern is
  that no one can read a GitHub secret back, so a lost value cannot be recovered. *"We need a proper
  HSM solution"* is recorded as a to-do; Key Vault or managed identity is the target.
- **Infra repo** (HCL; contributors Anand Kirori and Sandeep Uppal; 8 branches): dev deploys from
  `feature/oi-dev-phase2-services`, not `main`. A speaker said they had pushed to `main` directly
  "rather than creating a branch", and that `main` "was created by Anand earlier… Angel did not test
  this either." One commit on the feature branch is titled **"Updated PostgreSQL to Public with
  selected IP Listyes"**, against the diagram's *"public network access disabled"*. Another branch
  is `feature/OI3-54-thinkcell-vm`.
- **The "Dev today" box** on the 2 October infrastructure diagram:
  - WAF in **detection mode, logs only**.
  - Egress through a landing-zone NAT gateway, not Azure Firewall.
  - **Service Bus Standard with no private endpoint.**
  - Redis as a **Redis 7 container**, because Azure Managed Redis is not available to the
    subscription in Germany West Central. It runs *plaintext with password auth*, was created
    **in the portal rather than Terraform**, and has a sandbox exception logged as tech debt
    **TD-033**.
  - Not deployed: Cosmos DB, AI Search, Content Safety, Document Intelligence, the dynamic sessions
    pool, MCP tool servers, Bastion and AMPLS.
  - Real resource names: subscription `nextgenoi01`, `rg-oi-dev-gwc-nonprod-1`,
    `acae-oi-dev-gwc-nonprod-1`, `fd-oi-dev-nonprod-1`.

## Where the build departs from the ruling pages

| Topic | Ruling page | As built or drawn on 28 October |
| ----- | ----------- | ------------------------------- |
| Operational store | ADR-009: **Azure SQL Database**; TC §5.3 serverless SQL | **Azure Database for PostgreSQL Flexible Server**, per-service schemas |
| Tamper-evident audit | ADR-009 rejects *"custom append-only audit archive with hash chaining"*; TC §10.3 adopts SQL ledger tables and rejects *"a hand-rolled hash chain, and the burden of proving it correct"* | Hand-rolled hash chain on the queryable table (repo ADR-0021), digests to WORM blob |
| Session store | TC: Azure Cache for Redis, Adopt | Redis 7 container, plaintext with password auth, created outside Terraform |
| Chat threads | ADR-009: Redis | Foundry-managed thread storage in Sweden Central; Cosmos dropped |
| Model gateway | TC: **API Management GenAI gateway**, Adopt; Content Safety "at the gateway" | **None at MVP**; **Portkey** designed for every model call; APIM "later phase, beyond MVP"; Content Safety not deployed |
| Models | Technology Choices names none | `gpt-5.2`, `gpt-4.1`, **`claude-opus-5-5`** (writes the deck), `text-embedding-3-small` (designed) — none has a position |
| Embedding residency | Document Upload (4 Oct, *Authoritative*): self-hosted container; *"document content never leaves Germany for embedding"* | `text-embedding-3-small` in **Sweden Central**, via Portkey (designed) |
| Vector store | TC §4.2: none; AI Search as first candidate | "Not vectorising any data"; Sandeep: *pgvector* if ever |
| Agent orchestration | ADR-008: Microsoft Agent Framework, chosen for graph validation and budget propagation | No orchestration; direct Foundry calls; "agents are generated… never services" (ADR-0028) |
| Calculation hop | TC: gRPC with protobuf | **REST** (repo ADR-0013); `python-grpc` reserved (ADR-0005). The infra diagram still labels its services "REST and gRPC" |
| Interfaces | Technical Stack: FastAPI | The BFF is TypeScript; Python services elsewhere |
| Dependency alerts | TC §9: *"Dependabot with alerts as blocking"* | 174 open alerts |

## Positions Sandeep stated, verbally, in the session

None of these is written down anywhere. They are the Bain architect's stated view and may be worth
recording in `decisions/` once confirmed.

1. Every API is an Entra app registration, and the user is re-authenticated on every call.
2. All model calls go through Portkey.
3. If embeddings are ever needed, use pgvector on the existing Postgres.
4. Avoid gRPC unless contracts are centrally governed. *"Industry realised it's too complex to
   manage."*
5. Documents uploaded to a case, and anything extracted from them, are scoped to that case and
   deleted with it — not part of the global data set.
6. **Web data must be verified by a person before use, even from whitelisted URLs.** *"It's been
   given to us as a rule of thumb for any AI or any web data."* Whitelisting, which SN offered as
   the current partial solution, is not enough.
7. For 10–30 industries, write one deterministic workflow file per industry; consider LLM-generated
   workflows only beyond 30–50. Nikolozi to work out how different the industries really are.
8. CI/CD secrets move to a vault or HSM — "one of the to-dos".
9. At UAT, Foundry goes into the same zone behind a private endpoint, with no whitelisted IPs and no
   Front Door hop.

## Questions handed to the business

- **Business unit versus company before peer selection.** Peers are proposed before the user picks
  region or BU level, so selection is *"blind"*. It can propose a subsidiary of the target as a
  peer; the Beiersdorf set had both P&G and P&G Personal Care. Proposal: force that choice up front.
  **Stephanie and Noah** to decide.
- **Parent/child relationships**: CapIQ provides them, but how the practice wants to use them is
  undecided. Aliases need data before search can use them.
- **Document reuse**: if a partner has uploaded a company's documents once, should they "save
  globally or just for this OC"? The same question applies to web-fetched documents (store or
  re-fetch). Note the tension with *red by default, isolated by design*.
- **Roles**: there are three today — contributor, owner, and a third the transcript garbles
  (probably viewer). Platform-admin roles and an admin portal are needed — *"ultimately everyone is going to have access to this product."*

## Artefacts glimpsed on screen and not in the mirror

From the Teams share list at 00:05:
- `OC3_Stakeholder_Update_Sprint4_mid…` — **probably where the go/no-go outcome is recorded**
- `Opportunity_Catalyst_MVP_Scope_and…`
- three `Opportunity_Catalyst_Post-GLS_Scope…` decks
- `OC3_Product_and_Architecture_Overview`
- `Opportunity_Catalyst_Planning_Starter` (Excel)
- `QA_Defect_Register` (Excel)

The mirror holds only the Sprint 2 and Sprint 3 stakeholder updates.

## Frames — what was on screen

All 46 frames are full resolution (1920×1080, JPEG) in
[`../video-frames/2026-10-28-workshop/`](../video-frames/2026-10-28-workshop/), named
`HHMMSS-what.jpg` by their time in the recording. Open them directly: the diagrams are legible.

Scene detection (`tools/video_frames.py`, threshold 0.15) spent its whole cap on Miro zooms between
22:00 and 34:30 and missed most of the code walkthrough, so these were taken with `--at` at the
moments the transcript pointed to. The 120 scene frames stay gitignored; their index is in
`video-frames/`.

**One frame is deliberately left out.** At 47:30, `.github/deploy/settings/dev/experience-bff.json`
is on screen. It has no secret values — secrets are mounted as files under `/mnt/secrets/` — but it
shows the Entra tenant ID, app and client IDs, managed-identity IDs and internal hostnames.
Identifiers, not credentials, but nothing this workspace needs. What it adds to the notes:
- **`OC_GLS_MODE` is `on` in the shared dev environment** (tier `development`). That is
  consistent with the GLS doc ("local and development tiers only"), but it means dev serves the
  same Redis-backed GLS path as staging. The domain services are only exercised after sign-in
  where GLS mode is off.
- **The OTel exporter is `console`**, so dev telemetry goes to container logs.
- The chat agent endpoint sits on the POC Foundry project `poc-swc-oi-sweden-test`.

| Time | Frame |
| ---- | ----- |
| 00:05 | [Teams roster and share list](../video-frames/2026-10-28-workshop/000005-teams-roster-and-share-list.jpg) |
| 02:20 | [Miro board lanes](../video-frames/2026-10-28-workshop/000220-miro-board-lanes.jpg) |
| 04:40 | [System overview, whole](../video-frames/2026-10-28-workshop/000440-system-overview.jpg) |
| 13:40 | [System overview, services and agents](../video-frames/2026-10-28-workshop/001340-system-overview-services.jpg) |
| 20:10 | [System overview, data platform and Portkey](../video-frames/2026-10-28-workshop/002010-system-overview-data-platform-and-portkey.jpg) |
| 22:22 | [Journey portal, home](../video-frames/2026-10-28-workshop/002222-journey-portal-home.jpg) |
| 22:24 | [Journey portal, database](../video-frames/2026-10-28-workshop/002224-journey-portal-database.jpg) |
| 22:52 | [System overview, models (`claude-opus-5-5` writes the deck)](../video-frames/2026-10-28-workshop/002252-system-overview-models.jpg) |
| 26:36 | [Infrastructure reference, edge and services](../video-frames/2026-10-28-workshop/002636-infra-reference-edge-and-services.jpg) |
| 27:41 | [Infrastructure reference, Redis and data](../video-frames/2026-10-28-workshop/002741-infra-reference-redis-and-data.jpg) |
| 30:46 | [Infrastructure reference, Foundry](../video-frames/2026-10-28-workshop/003046-infra-reference-foundry.jpg) |
| 31:35 | [Infrastructure reference, subnets and *Dev today*](../video-frames/2026-10-28-workshop/003135-infra-reference-subnets-and-dev-today.jpg) |
| 33:42 | [Infrastructure reference, title and legend](../video-frames/2026-10-28-workshop/003342-infra-reference-title-and-legend.jpg) |
| 34:20 | [Dev and GLS staging on Azure](../video-frames/2026-10-28-workshop/003420-dev-and-gls-staging.jpg) |
| 35:30 | [Where data lives, from source files to screens](../video-frames/2026-10-28-workshop/003530-where-data-lives.jpg) |
| 43:30 | [Roster and data platform panel](../video-frames/2026-10-28-workshop/004330-roster-and-data-platform-panel.jpg) |
| 46:20 | [Core repo root, `stage`](../video-frames/2026-10-28-workshop/004620-core-repo-root-stage.jpg) |
| 51:00 | [`agents/`](../video-frames/2026-10-28-workshop/005100-agents-folder.jpg) |
| 52:20 | [`contracts/`](../video-frames/2026-10-28-workshop/005220-contracts-folder.jpg) |
| 54:10 | [`case.created` schema](../video-frames/2026-10-28-workshop/005410-case-created-schema.jpg) |
| 55:40 | [Audit event envelope](../video-frames/2026-10-28-workshop/005540-audit-event-envelope.jpg) |
| 57:00 | [Case-stream registry](../video-frames/2026-10-28-workshop/005700-case-stream-registry.jpg) |
| 1:04:50 | [Search-artifact manifest](../video-frames/2026-10-28-workshop/010450-search-artifact-manifest.jpg) |
| 1:16:00 | [Agent contracts](../video-frames/2026-10-28-workshop/011600-agent-contracts.jpg) |
| 1:16:45 | [`budget.contract.json`](../video-frames/2026-10-28-workshop/011645-budget-contract.jpg) |
| 1:18:05 | [Scaffolder, profile](../video-frames/2026-10-28-workshop/011805-scaffolder-profile.jpg) |
| 1:19:15 | [Scaffolder, details and data classes](../video-frames/2026-10-28-workshop/011915-scaffolder-details.jpg) |
| 1:20:00 | [Scaffolder, plan](../video-frames/2026-10-28-workshop/012000-scaffolder-plan.jpg) |
| 1:20:55 | [Scaffolder, files to create](../video-frames/2026-10-28-workshop/012055-scaffolder-plan-files.jpg) |
| 1:25:10 | [Entity normaliser tests](../video-frames/2026-10-28-workshop/012510-entity-normaliser-tests.jpg) |
| 1:26:40 | [`utilities/`](../video-frames/2026-10-28-workshop/012640-utilities-folder.jpg) |
| 1:28:30 | [Journey portal, data and storage](../video-frames/2026-10-28-workshop/012830-journey-portal-data-and-storage.jpg) |
| 1:29:55 | [`docs/`](../video-frames/2026-10-28-workshop/012955-docs-folder.jpg) |
| 1:30:40 | [GLS overview, architecture](../video-frames/2026-10-28-workshop/013040-gls-overview-architecture.jpg) |
| 1:30:45 | [GLS invariant exceptions, EX-0001 to 0008](../video-frames/2026-10-28-workshop/013045-gls-invariant-exceptions-1.jpg) |
| 1:31:00 | [GLS invariant exceptions, to EX-0011](../video-frames/2026-10-28-workshop/013100-gls-invariant-exceptions-2.jpg) |
| 1:31:40 | [GLS docs index](../video-frames/2026-10-28-workshop/013140-gls-docs-index.jpg) |
| 1:31:58 | [Engineering decisions, index](../video-frames/2026-10-28-workshop/013158-engineering-decisions-index.jpg) |
| 1:32:04 | [Engineering decisions, sign-in and case records](../video-frames/2026-10-28-workshop/013204-engineering-decisions-sign-in-and-case-records.jpg) |
| 1:32:09 | [Engineering decisions, search, agents and deck](../video-frames/2026-10-28-workshop/013209-engineering-decisions-search-agents-deck.jpg) |
| 1:32:20 | [`docs/engineering/`](../video-frames/2026-10-28-workshop/013220-engineering-folder.jpg) |
| 1:33:45 | [`docs/engineering/decisions/`](../video-frames/2026-10-28-workshop/013345-decisions-folder.jpg) |
| 1:36:30 | [Core repo root, with the late roster](../video-frames/2026-10-28-workshop/013630-core-repo-root-and-late-roster.jpg) |
| 1:37:45 | [Security and quality](../video-frames/2026-10-28-workshop/013745-security-and-quality.jpg) |
| 1:38:58 | [Core repo, `main`](../video-frames/2026-10-28-workshop/013858-core-repo-main.jpg) |
| 1:39:40 | [Infra repo and its branches](../video-frames/2026-10-28-workshop/013940-infra-repo-branches.jpg) |
