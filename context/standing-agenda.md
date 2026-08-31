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

Technology Choices is newest and most specific, and argues the position properly — what
building orchestration would have cost is stated. It should win. But until the other two
are corrected, StatusNeo can read any of the three and be following documentation.

**Ask: confirm Microsoft Agent Framework, then supersede the other two pages.**

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

### 4. CapIQ rate limits block a custom build and a scale question

Unanswered CapIQ rate limits and per-call cost block two things at once: the design of
the external rate-limiting component — one of only five builds argued as genuinely
warranted — and whether real-time fetch survives at **2300 users**. The component is
currently built to a conservative default and made configurable, which is a placeholder,
not an answer.

**Ask: who is chasing CapIQ, and what is the fallback if real-time fetch does not scale?**

### 5. Open-source and third-party positions need a ruling

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

---

## Watch list

Not yet worth standup time, but tracked.

- **Security design exists only as a colour band in an SVG.** The app-level (StatusNeo)
  versus infra-level (Bain) split is drawn in the technical architecture diagram and
  written on no page. Security Design is empty.
- **13 empty pages**, including NFR, Observability, Endpoints & Interfaces and Deployment
  CI/CD. WCAG 2.2 AA is currently the only hard non-functional target written anywhere.
- **Screens 03, 04 and 05** data requirements are marked *update in progress*.
- **ADR-001 to ADR-009** remain "Accepted, pending Bain architect review".
