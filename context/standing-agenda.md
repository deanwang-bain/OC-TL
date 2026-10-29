# Standing agenda

Live items worth raising with the team, highest-consequence first. The daily digest
prints this at the top of the update, so it is the first thing read each morning.

**Maintaining this file is the point.** Change detection is mechanical; deciding what
matters is not. When an item is resolved, delete it and record the ruling in
`decisions/`. When a sync surfaces something new, add it here with an explicit ask.

Format: `### N. Headline` — the finding, why it matters now, then **Ask:** in bold.

*Last full review against the mirror: 2026-10-26.*

---

### 1. GLS is today, and the go/no-go outcome is written down nowhere

The revised plan traded one week of development for a **go/no-go decision in the week of
19 October**, a week before **GLS on 26 October**. That trade was the right call and the
team made it ahead of time rather than under pressure.

**No page in the space records what was decided.** Not which build was chosen, not on what
evidence, not by whom. The Sprint 3 stakeholder deck that defined the gate is silent on
its outcome, and nothing since has filled the gap.

This matters less today than it will in two weeks, when someone asks what was shipped and
why. A gate with no recorded outcome is not a gate.

**Ask: whatever happened at go/no-go, write it on a page today — the decision, the build
it applied to, and the known gaps it accepted. Ten minutes now, and it is the only record
that will exist.**

*Lead, 28 October:* a deck titled `OC3_Stakeholder_Update_Sprint4_mid…` appears in Dipesh's
Teams share list in the architecture workshop recording. It is not in the mirror, and a
mid-Sprint 4 stakeholder update is where a go/no-go outcome would sit. **Ask Dipesh to attach
it to the Sprint 4 page.**

### 1a. The GLS build runs on eleven waived rules, and they expire on 31 December

From the Sprint 5 architecture workshop on 28 October
([notes](workshops/2026-10-28-system-and-data-architecture.md)). The GLS build lives on the
`stage` branch, **536 commits ahead of `main`**. With GLS mode on, *"after [sign-in] no domain
service and no Postgres table is touched."* The BFF answers from Redis copies of the golden
data, and runs **a port of the calculation engine inside the BFF**.

SN recorded this honestly, as eleven exceptions (EX-0001–EX-0011), each relaxing a core rule
and each **expiring 2026-12-31**. Three bear directly on what OpCat promises:

- **EX-0002**: financial arithmetic runs in the BFF. The numbers on screen come from a
  **second implementation** of the methodology — a port of `calc.py`, tested against BCN's
  golden outputs — and not from the governed calculation engine with its derivation trace. Two
  implementations of one methodology can drift.
- **EX-0006**: case edits bypass audit-service's hash-chained trail. Transparency is a product
  requirement, and on this build the audit record of a partner's edits is a Redis mutation log.
- **EX-0008**: agents have write tools, a rule lifted for every agent by repo ADR-0045 on
  17 October.

**None of the eleven is machine-checked.** They are deliberately kept out of the governance
checker. **The 50+ partner rollout** (late November or early December, per the watch list)
falls *before* the expiry. Nothing written says which codeline it runs on.

**Ask: which build serves the partner rollout, `stage` or `main`? And put a date against
retiring each exception. If the rollout runs on `stage`, EX-0006 needs an explicit decision,
because it takes the audit trail out of the product's transparency promise.**

### 1b. The design record has moved into SN's repository, and it reverses the ruling pages

The live architecture is on a Miro board (*OI Architecture (HL)*), in SN's repo docs, and in an
HTML journey portal. **None of it is in Confluence.** SN's own ADR series runs **ADR-0001 to
ADR-0045** in `docs/engineering/decisions/`, with numbers that collide with Confluence's
ADR-001–009. Several of those repo ADRs reverse what the ruling pages say:

| Ruling page | As built |
| ----------- | -------- |
| ADR-009: Azure SQL Database | **PostgreSQL Flexible Server** |
| ADR-009 and TC §10.3 reject a hand-rolled audit hash chain | Repo **ADR-0021**: *"the audit trail is hash chained on the queryable table"* |
| TC: Azure Cache for Redis | Redis 7 **container**, plaintext with password auth, created outside Terraform (TD-033) |
| TC: APIM GenAI gateway, with Content Safety at the gateway | **No gateway at MVP**; **Portkey** designed; Content Safety not deployed |
| ADR-008: Microsoft Agent Framework for orchestration | No orchestration — *"agents are generated, governed and never services"* (ADR-0028) |
| Document Upload: *"content never leaves Germany for embedding"* | `text-embedding-3-small` in **Sweden Central** (designed) |
| TC: gRPC for the calculation hop | **REST** (ADR-0013) |

Confluence ADR-001–009 are still *"Accepted, pending Bain architect review"*, and the Bain
architect is Sandeep Uppal. In the workshop he asked for a session to review SN's ADRs against
**Bain's agentic standards**, a document not in the mirror.

**Ask: hold that session, and come out of it with one authoritative series. Either supersede
the Confluence rows the repo ADRs overturn, or reject those repo ADRs. When citing, prefix SN's
series ("SN ADR-0021") so the two cannot be confused.**

### 2. Sprint 3 held at 82%, and the burn profile has not changed in three sprints

[Sprint 3 Retrospective](https://bainco.atlassian.net/wiki/spaces/OI30/pages/19933790220),
28 September – 12 October.

| Measure | Sprint 2 | Sprint 3 |
| ------- | -------- | -------- |
| Items completed | 48 | **27** |
| Completion rate | 83% | **82%** |
| Scope added mid-sprint | 29% | **18%** |
| Carried over | 10 | **6** |

Fewer, larger items at a level rate. Two real improvements: **all five mid-sprint
additions completed**, and **no item ended blocked on a vendor** — the first sprint where
that is true. Hours reached Jira for the first time: ~450 estimated, ~370 burned.

**The shape of the burn is the standing problem.** Nothing burned down in the first four
days. Platform and agent access landed **2 October**; work then fell from ~470 to ~305
hours over six days, and **305 to 80 on the final day** — about 60% of the sprint closing
at close. That is three consecutive sprints with the same profile, and the second running
where the trigger was an access grant arriving mid-sprint.

The team's own fix is right and unchanged from Sprint 2: raise platform access a sprint
ahead. It has not happened yet.

**Ask: what does Sprint 5 depend on that has not been requested? Ask it now, not at
planning. Three sprints of evidence say the access grant sets the burn curve.**

### 3. OI3-21 has been open for three sprints, waiting on me

Sprint 2 named five items open since Sprint 1. Three closed or were removed. Two remain:

- **OI3-21** — security and governance. **In review for a third sprint.** The retro is
  explicit that the constraint is review capacity, not build effort.
- **OI3-48** — development environment and access.

OI3-27, architecture decision records, closed — the ADR review did its job.

**Ask: nothing from the team. OI3-21 is mine and it is now the longest-running item on the
board. Clear it or hand it to someone who can.**

### 3a. The architecture workshop put the dev security gaps on screen

These are concrete inputs to OI3-21 and to the blank Security Design page. Each one was visible
in the recording, not inferred:

- **WAF in detection mode, logs only**, on the shared Front Door profile.
- **An infra commit titled "Updated PostgreSQL to Public with selected IP Listyes"**, against
  the design's *"public network access disabled"*. Whether it is still in effect is not shown.
- **Secret scanning, code scanning and a security policy are all disabled** on the core repo.
  Dependabot is on, with **174 open vulnerabilities**, some critical. Technology Choices calls
  for *"Dependabot with alerts as blocking"*.
- **CI/CD secrets are GitHub Environment secrets**, not Key Vault or managed identity. Sandeep
  logged moving them as a to-do.
- **Agent tool calls cross the public internet**: Foundry in Sweden calls back in through Front
  Door. Sandeep wants Foundry in-zone, behind a private endpoint, at UAT.
- **Session Redis runs plaintext with password auth** in a container created outside Terraform.
  Service Bus is Standard tier with no private endpoint.
- **Infra `main` was pushed to directly and is untested**; dev deploys from a feature branch.
- **Wiz is attached, but only Sandeep can see it**, and its Teams alerts are not arriving.

Sprint 5 is "Support and Hardening" on the team's own plan, so this is the sprint for it.

**Ask: before any partner traffic, (1) confirm Postgres public access is off, (2) switch the WAF
to prevention, (3) enable secret scanning and push protection — on a private repo that may need
a GitHub Advanced Security licence, so find out — and (4) triage the critical Dependabot alerts.
The rest can be sequenced, but should be written into OI3-21.**

### 4. The demo runs on a golden data set, and that should be said out loud

The golden data set, curated with BCN and delivered as JSON, is why Sprint 3 had no vendor
blockers. It is good engineering under a real constraint — **no data engineer was
onboarded for the GLS sprints**, and the full-stack developer due in Sprint 2 could not
contribute a full one.

**Its shape, from the Sprint 4 planning recording**: **10 target companies and their
peers, around 100 companies in total**, loaded from BCN documents, with cost bars,
levers, size of prize and recommendations **pre-calculated and stored as each case's
default**. The default journey shows BCN's validated results *without recalculation*; the
engine only computes the delta after a user changes a peer.

The retro states the cost plainly: *"not connecting live sources narrows the GLS
functionality."*

The [October prototype set](https://bainco.atlassian.net/wiki/spaces/OI30/pages/19958562873)
covers **Nike, Adobe, Beiersdorf and Honda** — chosen to show the tool generalises across
industries. It does, across four of the ten curated companies.

**Ask: agree the sentence the team uses when someone asks "what would this do for my
client?" Better one honest answer rehearsed than four improvised. And name the date the
data engineer arrives, because live sources are the gap between this demo and the
product.**

*Update, 28 October workshop:* after GLS, the golden data set **becomes the evaluation set**
for live source connections, which is the right next use for it. It lives outside git and is
loaded by hand (a SAS URL through Cloud Shell, then a script inside the BFF container). Siva
Vyra said the data "[is] onboarded next week". That is either the data engineer starting or
the data arriving — confirm which. Siva does not yet have access to the repo that documents
the data product.

### 4a. Two artefacts exist only inside a video, and no recording of the product exists

All 13 recordings in the space are **planning sessions** — Sprint 3 and Sprint 4, about
three hours. There is no demo recording, no walkthrough, no screen capture of the running
product anywhere in OI30.

Meanwhile the **Sprint 4 backlog workbook** — `OI3-Sprint-4-Backlog-Coll…`, carrying the
58 stories, their acceptance criteria and the "Week 1 — to go/no-go" split — is shared on
screen in that recording and **attached to no page**. The same is true of whatever was
shown in Sprint 3 planning.

**Ask: attach the Sprint 4 backlog workbook to Confluence, and record the GLS demo (or
publish the walkthrough prototype as the canonical one). A three-hour video is not a
record; the spreadsheet inside it is.**

*28 October:* the same pattern repeats at a larger scale. The Sprint 5 architecture workshop
(1 h 40 m, supplied locally, not in the space) walked through four current Miro diagrams, the
repo ADRs and the GLS exceptions, and **none of them is in Confluence**. The share list in that
recording also shows a QA defect register and the MVP and post-GLS scope decks, all missing from
the mirror. **Add to the ask: export the four lane-4 Miro diagrams onto the Architecture pages.**

### 5. Sprint 4 committed 58 items against the first measured rate we have

Sprint 3 burned ~370 hours over two weeks and is the first sprint with estimates in Jira.
Sprint 4 committed **58 items** — against 28, 45 and 22 before it — with most needed by
the end of week one, after analysis, output and chat were all pulled forward.

The retro flags the arithmetic itself: Sprint 4's estimate *"should be checked against
that rate now."* No page shows that check happened.

**Ask: what was actually completed in Sprint 4 week one, against the 58? That number is
the real go/no-go evidence, and it is also the first honest input to Sprint 5 planning.**

### 6. Four design pages are blank, and 249 MUST requirements are unanswered

Security Design, NFR Design Choices, Observability, Endpoints & Interfaces Design.
Deployment Design was filled on 7 October, which shows these get written when someone owns
one.

Behind them, the
[Architecture Assessment Tracker](https://bainco.atlassian.net/wiki/spaces/OI30/pages/19853082681)
still carries **313 requirements, 249 of them MUST, with zero responses**.

Sprint 3 delivered a **security scan framework** and **logged ADRs** — so the engineering
discipline exists. What is missing is the written policy those artefacts would be assessed
against.

**Ask: with GLS behind us, Sprint 5 is "Support and Hardening" on the team's own plan.
That is the sprint to assign Security Design and NFR, and to start the ARC responses.**

### 7. Azure AI Search is built, and the ruling page still forbids it

`srch-oi-dev-gwc-nonprod-1` exists; the Document Upload architecture marks itself
*Authoritative*; Sprint 3 delivered an **AI search design document**.
[Technology Choices](https://bainco.atlassian.net/wiki/spaces/OI30/pages/19751338017) §4.2
still says *"do not add a vector store at MVP or at north star"* and is **still version 1,
dated 21 August**.

**Ask: update §4.2 to record what was decided and why. The new AI search design document
is the natural place to cite. Leaving the decision record contradicting the running system
makes it useless for the next decision.**

*28 October — now three-way.* In the workshop Dipesh said *"for the time being we are not
vectorising any data"*. The system overview marks AI Search, Document Intelligence and the
embedding model as *designed*, and puts the embeddings on `text-embedding-3-small` in **Sweden
Central**, contradicting the Document Upload page's *"content never leaves Germany"*. Sandeep
said that if embeddings are needed, *"we should use pgvector"* on the existing Postgres. The
ruling page, the authoritative design and the architect now name three different answers.

### 8. The backend runs on a search vendor nobody has approved

Unchanged since 21 September. [Future Scope](https://bainco.atlassian.net/wiki/spaces/OI30/pages/19849412714)
states *"web search runs through a **serpapi** engine"*, and the deployment tracker adds
that the narrative agent *"calls only the model and web search"*. serpapi is how
**target-company names leave Bain**, and it is in no position table, no ADR, and not in the
Data Source Catalogue.

**Ask: rule on serpapi, or name what replaces it. Two independent paths now, still no
position.**

*28 October — a possible replacement.* A commit in SN's agent contracts, last month, is
titled *"feat(peer-discovery): search the web through the Foundry model endpoint"*. That reads
as moving web search onto the model's own search tool. If so, serpapi may be gone, but target
names still leave Bain through whatever search Foundry uses. Separately, Sandeep stated a rule
in the workshop: **web data must be verified by a person before use, even from whitelisted
URLs.** Peer discovery feeds web results straight into proposals. **Confirm serpapi is out, and
ask how the verification rule applies to peer discovery.**

### 9. Open-source and third-party positions still need a ruling

Technology Choices declares 66 positions and remains **Draft for review** — eight weeks
unchanged, and demonstrably behind the build. Assessment in
`requests/2026-08-31-third-party-and-oss-positions.md`.

- **Approve as a block** — TanStack Query, Zustand, Radix, i18next, Vega-Lite, DuckDB,
  Parquet, OpenTelemetry.
- **Hold** — Zvec, AG-Grid Enterprise, Datadog, dbt, headless Chromium driver.
- **Now in production, needs a position** — **CopilotKit / AG-UI**, delivered in Sprint 3
  as the chat tool catalogue. It was on the hold list; it shipped.
- **Add to the register** — **serpapi**, **Azure AI Search**, **gpt-5.2**, **gpt-4.1**,
  the **embedding model**, **Andromeda**.
- **New from the 28 October workshop**:
  - **`claude-opus-5-5`, which writes the output deck.** An Anthropic model producing the
    client-facing artefact, under an Azure-first rubric, with no position. This is the sharpest
    of the new ones.
  - **Portkey**, designed to sit on every model call, in place of the APIM GenAI gateway that
    Technology Choices adopts.
  - **`text-embedding-3-small`**.
  - **A self-hosted Redis 7 container**, where Technology Choices adopts Azure Cache for Redis.
  - **Textual**, a dev-only scaffolder UI that needs a position only if the block approval
    covers dev tooling.
- **think-cell** — the licence (OI3-54) was removed from Sprint 3 as *not a GLS
  dependency*. Still required post-GLS; still unruled.
- **Apache ECharts is a contradiction** — rejected in §2.1 of the same page for breaking
  ADR-006, then listed in the frontend table.

**Ask: approve the block; assign the rest. And add a licence column.**

### 10. ADR-001 to ADR-009 — two structural findings still open

Full review in `reviews/2026-09-01-adr-001-to-009.md`, outcome **approve with comments**.
OI3-27 closed, but the two findings did not.

1. **No ownership rule for the shared operational store.** ADR-009 puts claims, evidence
   bindings, content nodes, deck composition and peer sets in one database with nothing
   saying who may write which tables.
2. **ADR-009 contradicts itself on chat turns** — Context calls them transactional, the
   decision table assigns them to Redis. Staging runs GLS data in Redis with **no
   persistence**, so the question is concrete.

**Ask: rule on store ownership and fix the chat-turn contradiction.**

*28 October — both answered by the build, neither written down.*
1. Each service owns its own Postgres schema; for example, peer-curation-service owns peer
   sets, runs and versions (SN ADR-0031).
2. Chat threads are in **neither** Redis nor the transactional store. Cosmos was dropped
   because *"Foundry provides its own database"*, so threads live in Foundry-managed storage in
   **Sweden Central**. The ask is now to record both, and to confirm that holding chat content
   in Sweden is acceptable under the residency position.

---

## Recently settled — no longer worth standup time

- **The revised GLS plan held.** Sprints 1–3 delivered on the re-cut timeline; go/no-go
  bought a week of stabilisation rather than a last-minute deployment.
- **Estimates are in Jira** from Sprint 3 — ~450 hours committed, ~370 burned.
- **No vendor blockers in Sprint 3**, the first sprint where that is true.
- **OI3-27 architecture decision records** closed.
- **The calculation hop is REST, not gRPC.** Settled in code by SN ADR-0013, *"the
  calculation engine exposes REST for the MVP"*, with `python-grpc` reserved (SN ADR-0005).
  Dipesh confirmed it in the 28 October workshop, and Sandeep endorsed it. The Agent Validation
  Test Plan was right. Technology Choices still says gRPC and needs correcting; that is
  tracked under 1b.
- **`decisions/002` adopted** — Container Apps with Terraform and GitHub Environments.
- **Deployment Design is written**, first of the five blank design pages to move.
- **Analysis screen came in ahead of plan**, freeing Sprint 4 for the output screen.

## Watch list

- **The product is now "OpCat"** in the overview pages, rewritten the week of 19 October —
  *Opportunity Catalyst* in the architecture tree, *Opportunity Indicator* in the older
  data pages, `OI30` as the space key. Three names live.
- **The Figma file is explicitly out of date.** Design truth is the HTML prototype zips.
- **OI3-221, the confirm peers API**, was the named go/no-go dependency and carried into
  Sprint 4.
- **Sprint 4 planning exists only as four video files**, no written summary — the same
  pattern as Sprint 3 planning's nine.
- **Zoom passcodes are in the mirror**, on the User Interviews page, and so in git history.
- **Shared Postgres compute** is accepted only until the 50+ partner rollout, late
  November or early December.
- **A technical debt register exists** and is still not in the mirror. It has reached at least
  TD-033, which the infrastructure diagram cites for the Redis sandbox exception.
- **Six pages sit outside the OI3.0 tree**, including both engineering pages and two titled
  "to be delete" that hold real design rationale.
- **ADR-001 to ADR-009** remain "Accepted, pending Bain architect review".
- **A workshop series has started** (28 October: system and data architecture). Announced
  next: database migrations, deployment, company search, agent demos, and SN's ADRs against
  Bain's agentic standards. They arrive as local Teams recordings with `.vtt` transcripts, not
  as Confluence pages — read them with `tools/transcript_text.py`.
- **Business decisions handed to Stephanie and Noah**: whether to force a business-unit or
  company choice before peer selection (peers can currently include the target's own
  subsidiaries), and whether uploaded documents can be reused across cases.
