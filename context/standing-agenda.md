# Standing agenda

Live items worth raising with the team, highest-consequence first. The daily digest
prints this at the top of the update, so it is the first thing read each morning.

**Maintaining this file is the point.** Change detection is mechanical; deciding what
matters is not. When an item is resolved, delete it and record the ruling in
`decisions/`. When a sync surfaces something new, add it here with an explicit ask.

Format: `### N. Headline` — the finding, why it matters now, then **Ask:** in bold.

*Last full review against the mirror: 2026-10-08.*

---

### 1. Two items are blocked on my review, not on build effort

The Sprint 2 retrospective names ten spillover items and classifies each. Two sit in
review *"waiting on review capacity, not build effort"*:

- **OI3-21** — security and governance
- **OI3-27** — architecture decision records

Both are mine. They have been open since Sprint 1, and they are on a list the team is
being asked to explain. The ADR review in `reviews/2026-09-01-adr-001-to-009.md` is
written; what is missing is the ruling on its two structural findings (item 8).

**Ask: nothing — this one is on me. Clearing OI3-21 and OI3-27 is the first thing to do
this week, before asking anyone else for dates.**

### 2. Sprint 2 hit 83%, and the reason it did is the thing to protect

[Sprint 2 Retrospective](https://bainco.atlassian.net/wiki/spaces/OI30/pages/19883720705),
15–27 September.

| Measure | Sprint 1 | Sprint 2 |
| ------- | -------- | -------- |
| Items completed | 22 | **48** |
| Completion rate | 44% | **83%** |
| Of those committed | 9 of 22 | **36 of 45** |
| Scope added mid-sprint | ~127% | **29%** |
| Carried over | 28 | **10** |

Both sprints are counted on the same basis, so this is a real improvement: the team
doubled its commitment *and* raised the hit rate, and 12 of 13 mid-sprint additions
finished inside the sprint.

**The burn profile is the part worth reading.** Remaining work fell from 43 to 36 across
all of week two, then from 36 to 11 in the final three days — around 25 items, more than
half the sprint's output, closing once **AI platform access arrived on the last day of
the sprint**. The throughput is genuine; it was also gated on one access grant, and would
have looked entirely different had that grant slipped a week.

The team's own fix is the right one: *raise platform access requests a sprint ahead of
the work.*

**Ask: congratulate the team on this properly — it is a large, real improvement. Then ask
what Sprint 3 depends on that has not been requested yet, because that is the question
Sprint 2 answered the hard way.**

### 3. Four design pages are still blank, and the ARC assessment needs them

Security Design, NFR Design Choices, Observability, and Endpoints & Interfaces Design.
**Deployment Design was filled on 7 October** — the first of the five to move, and proof
these get written when someone owns one.

Still unanswered behind them: the
[Architecture Assessment Tracker](https://bainco.atlassian.net/wiki/spaces/OI30/pages/19853082681)
carries **313 requirements, 249 of them MUST, with zero responses** across both ARC v2
and the AI Architecture v2.1 workbook. The evidence it asks for is exactly what these
four pages would contain.

And the gap now has a concrete cost: the chat assistant streams over SSE, the ingestion
design says a 200-page filing "takes minutes", and **the 30-minute end-to-end claim still
has no latency budget written anywhere**. GLS demos that claim this month.

**Ask: assign Security Design and NFR to named people this week. Deployment Design shows
it takes one owner and a few days.**

### 4. Azure AI Search is built, and the ruling page still forbids it

The [Document Upload architecture](https://bainco.atlassian.net/wiki/spaces/OI30/pages/19899351139)
(4 October) marks itself **Authoritative** and records `srch-oi-dev-gwc-nonprod-1` as
**EXISTS** — Basic tier, 2 replicas, Entra-only auth — with `idx-case-documents` to be
created. Access was granted to the team on the last day of Sprint 2.

[Technology Choices](https://bainco.atlassian.net/wiki/spaces/OI30/pages/19751338017) §4.2
says *"Do not add a vector store at MVP or at north star, unless retrieval quality is
measured to be insufficient"*, with one revisit trigger: *"measured retrieval quality
against a fixed evaluation set, not a hunch."* **The page is still version 1, dated 21
August.** No evaluation is cited anywhere.

**The build is probably right** — a filtered hybrid query is not something SharePoint's
native index does, and the new design is careful work. The problem is that the decision
record now describes a system that does not exist, which makes it useless as a reference
for the next decision.

One good sign: the same page uses **Service Bus**, not Event Grid, which quietly brings
it back in line with §6 and resolves the conflict the September proposal opened.

**Ask: update §4.2 to record what was actually decided and why. If the evaluation was
run, cite it; if it was not, say the decision was taken on design grounds. Either is
fine — leaving the page contradicting the running system is not.**

### 5. The GLS staging environment is good work with three unconfirmed answers

[OC Dev-Staging (GLS) Deployment Tracker](https://bainco.atlassian.net/wiki/spaces/OI30/pages/19909279789)
(7 October) stands staging up as a **second Container Apps environment** —
`acae-oppcat-stg-gwc-nonprod-1`, own subnet, own identities, Terraform-provisioned,
deployed from GitHub Environments with OIDC. **This settles `decisions/002`: Container
Apps, not a VM, and with more pipeline than that recommendation thought affordable.**

Seventeen questions, answered the same day, each with a recommendation, a named decider
and a rationale. Where corners were cut they were written down rather than smoothed over.
This is the standard other pages should be held to.

Three things still open:

1. **Three answers say "Angel to confirm"** — Q7 audit blob container, Q10 new staging
   identities, Q15 whether the shared App Service plan carries a third app.
2. **The narrative agent does not exist yet.** Narrative blocks show "unavailable" until
   the agent team builds it, and it is on the demo path.
3. **GLS will run on a POC Foundry account**, `poc-swc-oi-sweden-test`, accepted "for now"
   with a proper one planned before the partner rollout.

**Ask: get Angel's three confirmations closed, and confirm the POC Foundry account carries
the quota and support the demo needs. Also: who owns the narrative agent, and by when?**

### 6. A model availability fact is splitting the system across two regions

Everything runs in **Germany West Central** except the Foundry agents, which run in
**Sweden Central** *because `gpt-5.2` is only offered there* (owner, 2026-10-01).

The design handles this well — document content, extraction, embedding and the index all
stay in Germany, and because Germany cannot host Azure models at all, the embedding model
runs as a Container App inside the environment with weights baked into the image. That is
a sound answer to a real constraint.

But two governance threads run through it and neither has a position recorded:

- **`gpt-5.2` and `gpt-4.1`** are now named models. Neither is in a position table, and
  the Greater China assessment separately records that OpenAI-backed features must be off
  in that region.
- **The embedding model is "to be chosen"**, with packaging explicitly either an
  off-the-shelf **Hugging Face text-embeddings-inference** image or a governed wrapper.
  That is a Build/Adopt decision with licence and provenance consequences.

**Ask: record positions for gpt-5.2, gpt-4.1 and whatever the embedding model turns out
to be. The top-n evaluation that picks it is the right moment to write the ruling.**

### 7. The backend runs on a search vendor nobody has approved

Unchanged since 21 September. [Future Scope](https://bainco.atlassian.net/wiki/spaces/OI30/pages/19849412714)
states that *"web search runs through a **serpapi** engine"*. serpapi is a commercial
third-party API and it is how **target-company names leave Bain**. It appears in no
position table, no ADR and not in the Data Source Catalogue.

The deployment tracker adds a second instance: the narrative agent *"calls only the model
and web search"*, with web search as the model's built-in tool.

**Ask: rule on serpapi, or name what replaces it. Web search is now in two independent
paths and still has no recorded position.**

### 8. ADR-001 to ADR-009 — two structural findings, now enforceable

Full review in `reviews/2026-09-01-adr-001-to-009.md`, outcome **approve with comments**.
This is OI3-27, one of the two items in item 1.

1. **No ownership rule for the shared operational store.** ADR-001 decomposes by domain;
   ADR-009 puts claims, evidence bindings, content nodes, deck composition and peer sets
   in one Azure SQL database with nothing saying who may write which tables. The monorepo
   exists and staging now has per-environment identities and separated blob containers —
   the discipline is clearly there, so this is a good moment to write the rule down.
2. **ADR-009 contradicts itself on chat turns** — Context calls them transactional, the
   decision table assigns them to Redis. Staging runs GLS data in Redis database 1 with
   **no persistence**, which makes the question concrete rather than theoretical.

**Ask: rule on store ownership and fix the chat-turn contradiction — then OI3-27 closes.**

### 9. Open-source and third-party positions still need a ruling

Technology Choices declares 66 Build / Adopt / Buy positions and remains **Draft for
review** — unchanged in six weeks, and now demonstrably behind the build. Assessment in
`requests/2026-08-31-third-party-and-oss-positions.md`.

- **Approve as a block** — TanStack Query, Zustand, Radix, i18next, Vega-Lite, DuckDB,
  Parquet, OpenTelemetry.
- **Hold** — Zvec, CopilotKit, AG-Grid Enterprise, Datadog, dbt, headless Chromium driver.
- **Add to the register** — **serpapi**, **Azure AI Search**, **gpt-5.2**, **gpt-4.1**,
  the **embedding model**, **think-cell** (OI3-54, open since Sprint 1) and **Andromeda**.
- **Apache ECharts is a contradiction** — rejected in §2.1 of the same page for breaking
  ADR-006, then listed in the frontend table.

**Ask: approve the block; assign the rest. And add a licence column.**

### 10. Three data foundation items left Sprint 2 without completing

OI3-18, OI3-43 and OI3-65 were removed from the sprint rather than finished, and moved to
the general backlog. The retro's own words: they *"still require close follow-up to not
become another blocker for the GLS scope."*

**Ask: who owns these now, and are any of them on the GLS path?**

### 11. The calculation hop is still specified two different ways

Unchanged since 2026-09-01, now five weeks old.

[Technology Choices](https://bainco.atlassian.net/wiki/spaces/OI30/pages/19751338017)
specifies **gRPC with protobuf**. The
[Agent Validation Test Plan](https://bainco.atlassian.net/wiki/spaces/OI30/pages/19765133323)
specifies **plain REST over HTTP** and excludes gRPC from MVP testing.

**Ask: which protocol, and who corrects the other page?**

---

## Recently settled — no longer worth standup time

- **`decisions/002` is adopted** — Container Apps with Terraform and GitHub Environments,
  not a VM. Worth formalising; no longer worth debating.
- **Deployment Design is written** — first of the five blank design pages to move.
- **Estimates reach Jira from Sprint 3** — two sprints ran on issue count because the
  board was configured for story points and changing it needed admin access.
- **Event Grid vs Service Bus** — the authoritative ingestion design uses Service Bus,
  agreeing with §6. Only the un-retracted Future Scope page still says otherwise.
- **"GenAI" is Azure AI Foundry** — answered by the September engineering pages.
- **The product rename reached the architecture tree** on 4 October.

## Watch list

- **The Jira board is `OI3`, not `OC3`.** The Sprint 1 deck relabels every ticket to
  `OC3-nn`; nothing else does. `OC3-48` and `OI3-48` are the same ticket. An earlier
  version of `CLAUDE.md` recorded `OC3` as fact — corrected 2026-10-08.
- **Zoom passcodes are in the mirror.** The [User Interviews](https://bainco.atlassian.net/wiki/spaces/OI30/pages/19883524168)
  page lists recording passwords in plain text beside nine partner interviews, so they are
  now in this repo's git history. The fix is on the Confluence side.
- **Sprint 3 planning exists only as nine video files**, ~91 MB, no written summary. The
  decisions taken there are not searchable.
- **Shared Postgres compute** is accepted only until the 50+ partner rollout, late
  November or early December.
- **Five items have been open since Sprint 1** — OI3-21, OI3-27, OI3-48, OI3-54, OI3-82.
- **Two items are blocked on vendor limits** — OI3-82 rate and quota, OI3-147 Data Access
  Service. The retro suggests escalating vendor rate limits as a single ask.
- **A technical debt register exists** and is still not in the mirror.
- **Six pages sit outside the OI3.0 tree**, including both engineering pages, the cost bar
  methodology, and two titled "to be delete" that hold real design rationale.
- **ADR-001 to ADR-009** remain "Accepted, pending Bain architect review".
