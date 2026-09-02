# Standing agenda

Live items worth raising with the team, highest-consequence first. The daily digest
prints this at the top of the update, so it is the first thing read each morning.

**Maintaining this file is the point.** Change detection is mechanical; deciding what
matters is not. When an item is resolved, delete it and record the ruling in
`decisions/`. When a sync surfaces something new, add it here with an explicit ask.

Format: `### N. Headline` — the finding, why it matters now, then **Ask:** in bold.

---

### 1. The calculation hop is specified two different ways

[Technology Choices](https://bainco.atlassian.net/wiki/spaces/OI30/pages/19751338017)
specifies **gRPC with protobuf** for the calculation hop, in both MVP and north star.
The [Agent Validation Test Plan](https://bainco.atlassian.net/wiki/spaces/OI30/pages/19765133323)
states the calculation engine uses **plain REST over HTTP**, with gRPC, protobuf and buf
*"excluded from MVP testing"*.

Both are current, and this is the calculation engine — the component the page itself
calls the most consequential build in the programme. Whichever is wrong, someone is
building or testing against the wrong contract.

**Ask: which protocol is Sprint 1 building, and who corrects the other page today?**

### 2. Three different answers for agent orchestration

| Source | Says |
| ------ | ---- |
| [Technology Choices](https://bainco.atlassian.net/wiki/spaces/OI30/pages/19751338017) | **Microsoft Agent Framework** (Adopt) |
| [Technical Stack](https://bainco.atlassian.net/wiki/spaces/OI30/pages/19704512648) | **AI SDK (ai-sdk.dev)** |
| Technical Architecture diagram | **Claude SDK** |

**ADR-008 settles this**, and settles it well: Microsoft Agent Framework, with Foundry
Workflows rejected as retiring 1 December 2026 and Prompt flow as retiring 20 April 2027,
both cited. Technology Choices agrees. So this is not an open decision — the other two
sources are simply stale, and StatusNeo can still read either and believe they are
following documentation.

**Ask: mark Technical Stack and the architecture diagram as superseded by ADR-008.**

### 3. An open item marked StatusNeo-owned is actually a Bain commitment

Technology Choices §13 lists eight open items and states *"All are now StatusNeo-owned."*
Item 8, the golden dataset for offline evaluation, says it *"needs Bain analyst time to
build reference peer sets, and nothing substitutes for that."*

That cannot be closed by StatusNeo. It gates Loop 3 of the probabilistic test track, so
agent quality cannot be measured against a baseline until it exists — and analyst time
needs scheduling, not just assigning.

Item 1, Foundry network isolation, is flagged as the largest unresolved item in the set
and decides whether the AI zone can be fully private or needs a compensating control.

**Ask: name a Bain owner and a date for the golden dataset. Confirm item 1 has a driver.**

### 4. Data sources answered end to end — and the LSEG flag is not the worst of them

Fritz asked on the Build LT thread for an overview of everything we pipe in or allow to be
uploaded, by source and by risk, after Kasia's AMBER flag on LSEG. Full map, with per-source
detail and a ranked risk table, in [context/data-source-map.md](data-source-map.md).

Three sources carry the numbers (CapIQ, company filings, Bain IP via Glean), one carries the
words (LSEG), one is the escape hatch (Partner upload). Everything else is roadmap.

**LSEG is the flagged risk; Glean/Iris is the larger one.** LSEG feeds qualitative surfaces
only — Screens 04 and 05 state plainly that it is *"not a financial fallback"* — so the size
of prize does not move if it goes away. Glean access is marked only as *"sandbox access
TBD"*, and every one of Screen 04's **14 sub-levers** takes its Bain experience range from
Iris/Sage, with **five having no peer benchmark at all**. That is a bigger functional hole,
tracked as a parenthetical.

**On LSEG specifically, three things are cheap and should happen before any vendor
assessment:**

1. **The Glean answer is four weeks old.** *"Confirm with Glean/IRIS whether they can fetch
   LSEG analyst reports"* was an action on Sandeep from 4 August, due before the
   architecture workshop, and the space records no answer. If Glean holds LSEG content under
   Bain's existing entitlement, we inherit it rather than negotiate it.
2. **Curated reports need no new integration.** The upload path already classifies analyst
   reports and routes them to the qualitative layer — Kasia's workaround reuses a designed
   path. Two conditions: the demo target is public anyway, and the 30-minute claim should be
   stated as excluding the manual retrieval step rather than quietly absorbing it.
3. **LSEG must be a soft gate.** Every LSEG-fed surface degrades visibly and no LSEG
   condition blocks a run. Screen 02's private-company fallback is already the pattern. This
   is ours to decide and does not wait on the contract.

**AlphaSense substitutes the supplier, not the problem** — any licensed research aggregator
carries the same class of persistence and redistribution restrictions. ADR-007 already
commits the evidence service to enforcing *"persistence restrictions on analyst report
content"*, and the LSEG page is empty. That was finding S6 of the ADR review and it is now
the critical path, not a documentation nicety.

One open question changes the rating: the Data Sources summary attributes **consensus
analyst estimates (projected revenue growth)** to LSEG, while the VCC calculation lineage
implies CapIQ. If it is LSEG, the flag touches a sized opportunity rather than only
qualitative surfaces.

**Ask: chase the Glean answer; confirm whether consensus estimates come from CapIQ or LSEG;
name an owner and date for Glean/Iris sandbox access; and get the LSEG persistence and
export rules written onto the page before the evidence service is built.**

### 5. CapIQ rate limits block a custom build and a scale question

Unanswered CapIQ rate limits and per-call cost block two things at once: the design of
the external rate-limiting component — one of only five builds argued as genuinely
warranted — and whether real-time fetch survives at **2300 users**. The component is
currently built to a conservative default and made configurable, which is a placeholder,
not an answer.

**Ask: who is chasing CapIQ, and what is the fallback if real-time fetch does not scale?**

### 6. Open-source and third-party positions need a ruling

Technology Choices declares 66 Build / Adopt / Buy positions and is still **Draft for
review**. No request had been raised for any of them. Full assessment in
`requests/2026-08-31-third-party-and-oss-positions.md`.

Recommended split, so Sprint 1 is not held up by a licence question:

- **Approve as a block** — TanStack Query, Zustand, Radix, i18next, Vega-Lite, DuckDB,
  Parquet, OpenTelemetry. Mainstream, permissive, cheap to reverse.
- **Hold seven** — Zvec, Apache ECharts, CopilotKit, AG-Grid Enterprise, Datadog, dbt,
  headless Chromium driver.

Only two carry real risk. **Zvec** is the one dependency nobody will recognise and needs
licence, maintainer and release cadence confirmed. **CopilotKit** is recorded as
"Buy, licence" but is open-core, so the tier and cost are unstated, and it shapes the
assistant surface, making it expensive to reverse.

**Apache ECharts is a contradiction, not a risk:** the same page rejects it in §2.1
because a component library forces an Exhibit to be a rendering rather than a
specification, which would break the format-neutral content model under ADR-006 — then
lists it in the frontend table anyway.

**Ask: approve the block; assign the seven. And add a licence column — the table tests
fit, rubric, reversibility and operability, but never records the licence, which is what
a third-party approval actually turns on.**

### 7. Two topology questions from StatusNeo, both needing a ruling

Asked directly: which services are separate versus one monorepo at MVP, and whether to
run a proper pipeline on Container Apps or deploy to a VM to protect GLS focus.

Recommendations in `decisions/001` and `decisions/002`, both **proposed, pending
sign-off**. In short: one repository with three to six deployables, keeping the
calculation engine separate from day one because §10.2 calls it the one component Bain
reuses; and Container Apps with a thin pipeline rather than a VM, cutting CD scope rather
than the platform, because Container Apps was chosen for dynamic sessions and the whole
security posture assumes managed infrastructure.

**Repository structure is documented nowhere in the space** — no page mentions it.

**Ask: confirm both rulings.**

### 8. GLS is roughly seven weeks out and the date is not in the documentation

GLS is the **Global Leadership Summit, mid-to-late October**, where OI 3.0 is
demonstrated to Bain's most senior internal audience. The MVP is still "to be signed off",
so the hardest date in the programme is not recorded in the space.

*Corrected 2026-09-02:* [GLS Feature Set](https://bainco.atlassian.net/wiki/spaces/OI30/pages/19761725586)
and [Sprint 1 stories](https://bainco.atlassian.net/wiki/spaces/OI30/pages/19763003424)
are **not** empty — both carry attachments (`OI_3.0_Feature_Overview_1.pptx` and
`OI3-Sprint_1_planning.xlsx`) that the sync was dropping until today. Their content
exists; it is just not on the page or in any search.

Five things now have a deadline attached rather than an open question mark:

1. **The 30-minute claim gets its first public test.** The NFR page is empty, so there is
   no latency budget to build against. Time a full end-to-end run well before October.
2. **CapIQ latency** (open item 2, unresolved) bites hardest in a live demo, because MVP
   fetches in real time per run.
3. **Demo target must be a public company.** A real Bain client brings MNPI, and the test
   plan forbids production documents in non-production environments. Nike is already used
   throughout the screen specs.
4. **Cold start** — set Container Apps minimum replicas to 1 for the demo window.
5. **Live versus pre-baked** needs a deliberate decision, with a recorded fallback either
   way.

The unresolved gRPC-versus-REST contradiction (item 1) and the orchestration ambiguity
(item 2) are also more urgent than they looked yesterday: seven weeks is not long enough
to build the wrong contract and recover.

**Ask: put the GLS date and demo scope on the GLS Feature Set page, and name an owner
for demo readiness as distinct from MVP delivery.**

### 9. ADR-001 to ADR-009 reviewed — two structural findings

Full review in `reviews/2026-09-01-adr-001-to-009.md`. Outcome **approve with comments**:
the reasoning quality is high and none of the nine decisions looks wrong.

Two findings should be resolved before the set is treated as final:

1. **No ownership rule for the shared operational store.** ADR-001 decomposes by domain;
   ADR-009 puts claims, evidence bindings, content nodes, deck composition and peer sets
   into one Azure SQL database. Those belong to different services and nothing says who
   may write which tables. Left unstated, the ADR-006 and ADR-007 ownership guarantees
   hold by convention rather than construction.
2. **ADR-009 contradicts itself on chat turns** — listed in Context as needing
   transactional read-write, then assigned to Redis, which is explicitly ephemeral.

The highest-leverage open item is **network isolation**, which is Bain-owned and leaves
both ADR-008 and ADR-009 provisional. Seven weeks from GLS, that is a schedule risk.

**Ask: rule on the store ownership question, fix the chat-turn contradiction, and name an
owner and date for network isolation.**

## Watch list

Not yet worth standup time, but tracked.

- **Security design exists only as a colour band in an SVG.** The app-level (StatusNeo)
  versus infra-level (Bain) split is drawn in the technical architecture diagram and
  written on no page. Security Design is empty.
- **13 empty pages**, including NFR, Observability, Endpoints & Interfaces and Deployment
  CI/CD. WCAG 2.2 AA is currently the only hard non-functional target written anywhere.
- **Screens 03, 04 and 05** data requirements are marked *update in progress*.
- **ADR-001 to ADR-009** remain "Accepted, pending Bain architect review".
