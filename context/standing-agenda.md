# Standing agenda

Live items worth raising with the team, highest-consequence first. The daily digest
prints this at the top of the update, so it is the first thing read each morning.

**Maintaining this file is the point.** Change detection is mechanical; deciding what
matters is not. When an item is resolved, delete it and record the ruling in
`decisions/`. When a sync surfaces something new, add it here with an explicit ask.

Format: `### N. Headline` — the finding, why it matters now, then **Ask:** in bold.

---

### 1. The journey portal's 42 blockers cite a workbook that is not in the space

The [journey portal](journey-portal.md) (ingested 2026-09-03, source in
`context/artifacts/`) documents 11 API journeys across Target Setup and Peer Selection
and tracks **42 blocker instances, resolving to 18 distinct blockers** — 8 P0, 5 P1,
4 P2, 1 waiting on a stakeholder.

Every source-backed blocker cites `OI 3.0 - Data and API Mapping by Screen v3.xlsx` down
to the cell — `Spec Conflicts!B13:F13`, `Open Questions!B26:F26`, and so on. **That
workbook is in no page in the OI30 space**, and no mirrored page references it. Twelve of
the thirteen P0 and P1 blockers cite it. The citations are precise enough to verify and
nobody working from Confluence can open them.

Three things fall out of the register itself:

1. **Adjusted EBIT tolerance is the highest-leverage single item** — it touches 5 of the
   11 journeys and is the only blocker reaching the confirm step. It needs an approved
   number, not a build. Until then `reconciled=true` is never emitted, which is correct.
2. **Four upstream data answers generate 17 of the 42 instances** — FX, licensed filings,
   SIC/taxonomy, and segment/BU-plus-regional coverage. Three are CapIQ-side, the same
   supplier already in item 5 for rate limits. That is one owner conversation, not three.
3. **Three blockers are inferred, not requested** — the private-company evidence floor,
   evidence retention and legal hold, and the search refresh/rollback SLA are labelled
   *Derived recommendation* and are explicitly "not a stated workbook requirement".
   Chasing a stakeholder for these will fail; they need a ruling here.

FX, filings and the EBIT tolerance all gate benchmark numbers, and benchmark numbers are
the GLS demo. Under the drillability requirement, every adjusted or converted figure in a
demo run today is native-currency, labelled unadjusted, or suppressed.

**Ask: attach the mapping workbook to a page in the space. Name an owner and date for the
adjusted-EBIT tolerance. And confirm the three derived blockers are ours to rule on, not
to chase.**

### 2. The calculation hop is specified two different ways

[Technology Choices](https://bainco.atlassian.net/wiki/spaces/OI30/pages/19751338017)
specifies **gRPC with protobuf** for the calculation hop, in both MVP and north star.
The [Agent Validation Test Plan](https://bainco.atlassian.net/wiki/spaces/OI30/pages/19765133323)
states the calculation engine uses **plain REST over HTTP**, with gRPC, protobuf and buf
*"excluded from MVP testing"*.

Both are current, and this is the calculation engine — the component the page itself
calls the most consequential build in the programme. Whichever is wrong, someone is
building or testing against the wrong contract.

**Ask: which protocol is Sprint 1 building, and who corrects the other page today?**

### 3. Three different answers for agent orchestration

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

### 4. An open item marked StatusNeo-owned is actually a Bain commitment

Technology Choices §13 lists eight open items and states *"All are now StatusNeo-owned."*
Item 8, the golden dataset for offline evaluation, says it *"needs Bain analyst time to
build reference peer sets, and nothing substitutes for that."*

That cannot be closed by StatusNeo. It gates Loop 3 of the probabilistic test track, so
agent quality cannot be measured against a baseline until it exists — and analyst time
needs scheduling, not just assigning.

Item 1, Foundry network isolation, is flagged as the largest unresolved item in the set
and decides whether the AI zone can be fully private or needs a compensating control.

**Ask: name a Bain owner and a date for the golden dataset. Confirm item 1 has a driver.**

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

The unresolved gRPC-versus-REST contradiction (item 2) and the orchestration ambiguity
(item 3) are also more urgent than they looked yesterday: seven weeks is not long enough
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
- **10 empty pages**, including NFR, Observability, Endpoints & Interfaces and Deployment
  CI/CD. WCAG 2.2 AA is currently the only hard non-functional target written anywhere.
  *(Was 13 here; corrected 2026-09-02 — three pages carry attachments the sync was
  dropping.)*
- **The compliance policy gap is the first place an empty page bites a live endpoint.**
  `01b-target-resolve` cannot define its `409 review_required` semantics until Security
  Design says what the rules and escalation are.
- **Screens 03, 04 and 05** data requirements are marked *update in progress*.
- **ADR-001 to ADR-009** remain "Accepted, pending Bain architect review".
