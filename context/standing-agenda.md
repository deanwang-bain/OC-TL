# Standing agenda

Live items worth raising with the team, highest-consequence first. The daily digest
prints this at the top of the update, so it is the first thing read each morning.

**Maintaining this file is the point.** Change detection is mechanical; deciding what
matters is not. When an item is resolved, delete it and record the ruling in
`decisions/`. When a sync surfaces something new, add it here with an explicit ask.

Format: `### N. Headline` — the finding, why it matters now, then **Ask:** in bold.

*Last full review against the mirror: 2026-09-15.*

---

### 1. Peer selection specifies OpenAI, which no technology decision allows

[Peer Selection Capability](https://bainco.atlassian.net/wiki/spaces/OI30/pages/19809534070)
— new in September, and the most detailed implementation spec in the space — identifies
peer candidates using **"OpenAI-powered search"**, with **web search as a fallback** where
CapIQ lacks a field.

Nothing else in the programme points there:

| Source | Says |
| ------ | ---- |
| Technology Choices | **Azure managed services first**; models via **Azure AI Foundry**; *"every model call passes the gateway"* |
| ADR-008 | **Microsoft Agent Framework** |
| Andromeda page | The model gateway exists so there is *"no data leaving Bain"* |

OpenAI appears in no technology position table. Web search is not there either. Both put
target-company queries to an external service, which is a data-governance question before
it is a technology one — particularly against the Partner-Private isolation tier that is
supposed to evaporate on close with no training without opt-in.

This may be a deliberate sprint-1 expedient, or wording that outran the decision. Either
is fine; neither is recorded.

**Ask: is OpenAI approved for peer search, and does it go through the Bain gateway? If it
is a sprint-only expedient, say so on the page and name what replaces it.**

### 2. The calculation hop is still specified two different ways

Unchanged since 2026-09-01, and now roughly four to six weeks from GLS.

[Technology Choices](https://bainco.atlassian.net/wiki/spaces/OI30/pages/19751338017)
specifies **gRPC with protobuf** for the calculation hop. The
[Agent Validation Test Plan](https://bainco.atlassian.net/wiki/spaces/OI30/pages/19765133323)
specifies **plain REST over HTTP**, with gRPC, protobuf and buf *"excluded from MVP
testing"*. This is the calculation engine — the component the page itself calls the most
consequential build in the programme.

Two weeks have passed with neither page corrected.

**Ask: which protocol is being built, and who corrects the other page this week?**

### 3. CapIQ API access still is not there, and the workaround is now load-bearing

The picture is clearer than it was, and worse in one respect.

**What is now known** — [Data Contacts](https://bainco.atlassian.net/wiki/spaces/OI30/pages/19817627730)
(new) records **S&P MCP as the primary route** for financial data, with hard numbers:
10-K extraction takes **three API calls per company**, runs **one company at a time** at
**5–10 seconds per call**, capped near **6,000 companies per day**. The team states the
approach is *"not yet repeatable at scale"* and offers to share its framework. Contacts
are Abishek Soni and Kritik Ajmani.

**What is still missing** — CapIQ API access. Peer selection works around it for sprints
1 and 2 using CapIQ **Excel extracts** converted to Parquet. So the rate-limit question
that blocks the custom rate-limiting component is deferred rather than answered, and a
manual extract now sits on the critical path to GLS.

These are also the first throughput figures anywhere in the programme, and the NFR page is
still empty.

**Ask: who owns getting CapIQ API access, and what happens at GLS if the Excel extract is
stale? Take the lessons-learned session TSR offered.**

### 4. Ten pages are still blank, and none of them moved in two weeks

Six pages were added during September. The empty set did not shrink by one. Still blank:
**Security Design, NFR Design Choices, Observability, Endpoints & Interfaces Design,
Deployment Design (CI/CD)**, plus LSEG and Jobs to be Done.

These are the five pages every technical review leans on. The team demonstrably writes
well when it writes — the ADRs, Technology Choices and the test plan are all strong — so
this is a prioritisation gap, not a capability one.

**Ask: assign owners for Security Design and NFR. Those two gate the most and are the
cheapest to write, since the content largely exists in the architecture diagram.**

### 5. Open-source and third-party positions still need a ruling

Technology Choices declares 66 Build / Adopt / Buy positions and remains **Draft for
review**. Assessment in `requests/2026-08-31-third-party-and-oss-positions.md`. Now also
add **OpenAI** and **web search** from item 1, neither of which is in any table.

- **Approve as a block** — TanStack Query, Zustand, Radix, i18next, Vega-Lite, DuckDB,
  Parquet, OpenTelemetry.
- **Hold** — Zvec (obscure, needs licence and maintainer confirmed), CopilotKit (recorded
  as "Buy, licence" but open-core, tier unstated, expensive to reverse), AG-Grid
  Enterprise (rests on "existing Bain licence" — confirm it covers this), Datadog
  (duplicates Azure Monitor), dbt, headless Chromium driver.
- **Apache ECharts is a contradiction, not a risk** — the page rejects it in §2.1 because
  a component library forces an Exhibit to be a rendering rather than a specification,
  breaking ADR-006, then lists it in the frontend table.

**Ask: approve the block; assign the rest. And add a licence column — the table tests fit,
rubric, reversibility and operability but never records the licence, which is what a
third-party approval turns on.**

### 6. Two topology rulings are still awaiting sign-off

`decisions/001` and `decisions/002`, both **proposed** since 2026-08-31: one repository
with three to six deployables, keeping the calculation engine separate from day one; and
Container Apps with a thin pipeline rather than a VM.

StatusNeo asked both questions directly and has had no answer for two weeks.

**Ask: confirm both, or tell me what to change.**

### 7. GLS is four to six weeks out

GLS is the **Global Leadership Summit, mid-to-late October**. Scope has firmed up:
[Post-GLS Feature Set](https://bainco.atlassian.net/wiki/spaces/OI30/pages/19800162379)
(new) moves nine initiatives out of the demo — Technical Foundations, Scaling, Cost
Efficiency, Business Unit Handling, Data & Coverage Expansion, OI Lifecycle & Versioning,
Output Iteration & Editing, Collaboration & Governance, UX feedback.

Still open, and now dated rather than merely open:

1. **The 30-minute claim gets its first public test** with no latency budget written down.
   Time a full end-to-end run well before the week of the demo.
2. **Peer selection depends on a manual CapIQ extract** — see item 3.
3. **Demo target must be a public company.** A real client brings MNPI, and the test plan
   forbids production documents in non-production environments. Nike is already used
   throughout the screen specs.
4. **Cold start** — set Container Apps minimum replicas to 1 for the demo window.
5. **Live versus pre-baked**, with a recorded fallback either way.

**Ask: name an owner for demo readiness, distinct from MVP delivery.**

### 8. ADR-001 to ADR-009 — two structural findings still open

Full review in `reviews/2026-09-01-adr-001-to-009.md`. Outcome **approve with comments**.

1. **No ownership rule for the shared operational store.** ADR-001 decomposes by domain;
   ADR-009 puts claims, evidence bindings, content nodes, deck composition and peer sets
   into one Azure SQL database, with nothing saying who may write which tables.
2. **ADR-009 contradicts itself on chat turns** — listed in Context as needing
   transactional read-write, then assigned to Redis, which it calls ephemeral.

*Resolved since the review:* finding **S4** (ADR-004's client-writes-state pattern not
accounting for concurrent viewers) is answered by scope — Post-GLS Feature Set puts
real-time collaboration and approval flows after GLS, so MVP is single-viewer.

**Network isolation remains the highest-leverage open item**, Bain-owned, leaving both
ADR-008 and ADR-009 provisional.

**Ask: rule on store ownership, fix the chat-turn contradiction, name an owner and date
for network isolation.**

---

## Recently settled — no longer worth standup time

- **All six screen specs are stable.** Screens 04 and 05 dropped *update in progress*
  during the week of 8 September; Screen 03 on 1 September.
- **Bain taxonomy is settled.** Bain L1–L4 becomes the master structure, aligned to IRIS
  and Glean tagging. Business units limited to publicly reported segments; parent cost
  structure is the fallback. Breakdown stops where evidence stops — L4 is not required.
- **Agent orchestration** is settled by ADR-008 (Microsoft Agent Framework). Only the
  stale Technical Stack page and architecture diagram still need marking superseded.

## Watch list

- **Design requirements grew** — [Design requirements cont.](https://bainco.atlassian.net/wiki/spaces/OI30/pages/19808256031)
  adds requirement groups 17–21 from September user testing with six partners. Two carry
  named owners: realisation timelines pending **Stephanie**, Operational Excellence lever
  taxonomy to confirm with **Scott Daubin**.
- **Security design still exists only as a colour band** in the technical architecture SVG.
- **ADR-001 to ADR-009** remain "Accepted, pending Bain architect review".
- **Peer Selection Capability is filed outside the OI3.0 page tree**, at the space root.
