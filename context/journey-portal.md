# Opportunity Catalyst journey portal — architecture journeys and blocker register

**Source:** [`artifacts/2026-09-03-opportunity-catalyst-journey-portal.html`](artifacts/2026-09-03-opportunity-catalyst-journey-portal.html)
— a self-contained HTML handoff ("Opportunity Catalyst · Journey Portal"), ingested
2026-09-03. Open it in a browser: it carries rendered swimlane diagrams and Mermaid ER
models that this note cannot reproduce.

**What it is.** A screen-by-screen architecture walkthrough of the first two working
screens: user trigger, public endpoint, component swimlane with per-boundary payload
examples, data contracts as TypeScript types, journey invariants, and a tracked blocker
list with cell-level provenance. It is a *design and gap artifact*, not shipped code — it
documents what is decided, what is interim, and what is unresolved.

**Not a Confluence page.** It is not in the `OI30` mirror and is not covered by the daily
sync. Nothing here overwrites it, and nothing refreshes it either — if a newer version
arrives, replace the file in `artifacts/` and update this note.

## Coverage

| Screen | State |
| ------ | ----- |
| 01 · Login | **Journey pending** — employee SSO and RBAC stakeholder response outstanding |
| 02 · Dashboard | **Create New Case pending** — endpoint and service journey not yet defined |
| 03 · Target Setup | 6 journeys documented |
| 04 · Peer Selection | 5 journeys documented |

11 documented journeys, 2 pending screens. The portal deliberately keeps the pending
screens visible "so the catalog represents the intended product flow without inventing
architecture" — the same discipline this workspace applies to empty Confluence pages.

## The 11 journeys

| Journey | Trigger | Endpoint | Lanes |
| ------- | ------- | -------- | ----- |
| `01a-company-search` | Types 2+ characters | `GET /api/v1/companies/suggest` | 5 |
| `01b-target-resolve` | Selects a suggestion, clicks Resolve | `POST /api/v1/opportunities/{opportunityId}/target/resolve` | 12 |
| `01c-update-scope` | Changes geographic or BU scope | `PUT /api/v1/opportunities/{opportunityId}/scope` | 5 |
| `01d-update-framing` | Saves audience, trigger, priority, constraint | `PUT /api/v1/opportunities/{opportunityId}/framing` | 6 |
| `01e-upload-document` | Uploads a file | `POST /api/v1/opportunities/{opportunityId}/documents` | 13 |
| `01f-propose-peers` | Clicks Propose peers | `POST /api/v1/peer-sets/propose` | 16 |
| `02a-load-peer-set` | Screen opens or SSE completes | `GET /api/v1/peer-sets/{peerSetId}` | 6 |
| `02b-load-peer-detail` | Opens a peer tile | `GET /api/v1/peer-sets/{peerSetId}/members/{companyId}` | 10 |
| `02c-mutate-peer-set` | Changes membership or BU scope | `PATCH /api/v1/peer-sets/{peerSetId}/members` | 13 |
| `02d-load-benchmark` | Screen loads or selects a metric | `GET /api/v1/peer-sets/{peerSetId}/benchmarks/{metricId}` | 5 |
| `02e-confirm-peer-set` | Clicks Confirm peer set | `POST /api/v1/peer-sets/{peerSetId}/confirm` | 8 |

`01f-propose-peers` is the heavy one at 16 lanes and 12 tracked blockers — it spans
Screen 01 into Screen 02 and is the only agentic journey in the set.

## Journey invariants

Worth quoting, because these are the assertions a review should hold SN's code to.

- **`01b`** — compliance must clear *before* financial data is read; missing SIC, region,
  BU, filing or FX data is returned as **capability state**, not absence.
- **`01c`** — unsupported scope returns `422` with a capability reason; "it is not
  silently approximated."
- **`01d`** — the agent proposes labels only; the user confirms anything treated as a
  hard constraint.
- **`01e`** — qualitative evidence never overwrites numeric facts; only accepted
  financial overrides invoke deterministic recalculation.
- **`01f`** — agentic workers propose candidates, evidence and rationale; **deterministic
  services own IDs, arithmetic, scoring and state.**
- **`02a`** — the response is one persisted version, so tile and detail values cannot mix
  runs.
- **`02c`** — every mutation creates a new draft version; a stale `If-Match` returns
  `409`.
- **`02d`** — median includes the target and excludes stale or metric-ineligible values.
- **`02e`** — confirmation is an optimistic-concurrency state transition, **not an agent
  decision**.

These are consistent with the programme's stated principles rather than novel: the
proposes-versus-owns split and the confirm-is-not-an-agent-decision rule are
[Vision](../confluence/oi30/overview/vision-19617939629.md)'s "AI as enabler, not
decision-maker" made testable, and returning capability state instead of a silent
approximation is what
[Technology Choices](../confluence/oi30/architecture/opportunity-indicator-architecture-high-level/technical-stack/technology-choices-19751338017.md)'s
transparency requirement looks like at an API boundary.

The runtime split in the swimlanes also **matches** Technology Choices §3.2 — Node with
TypeScript for the IO-bound services (Experience BFF, Case, Evidence, Entity &
Classification, Compliance), Python for Company Search, Data Access and the Calculation
Engine. Note that Compliance Service is drawn as "owner TBD", and the calculation hop is
drawn as **gRPC/Protobuf**, which is Technology Choices' position and not the Agent
Validation Test Plan's REST — see standing agenda item 1.

## Blocker register

**42 tracked blocker instances across the 11 journeys, resolving to 18 distinct
blockers**: 8 P0, 5 P1, 4 P2, 1 Waiting. Priorities, wording and provenance are the
portal's own.

Origin labels matter for how each is actioned:

- **Source-backed** (11) — the workbook records the gap. Chase the owner.
- **Mixed** (4) — part recorded gap, part inferred design question. Needs both.
- **Derived recommendation** (3) — inferred by whoever built the portal; *not* a stated
  requirement anywhere. **These need a Tech Lead ruling, not a chase.**

### P0

| Blocker | Origin | Journeys | Unresolved | Interim in the artifact |
| ------- | ------ | -------- | ---------- | ----------------------- |
| **Adjusted EBIT tolerance** | Source-backed | **5** — `01e`, `01f`, `02b`, `02d`, `02e` | No approved pass / flag / fail threshold | Store deltas; never emit `reconciled=true` without a configured threshold |
| **Authoritative FX source** | Source-backed | 3 — `01b`, `01f`, `02d` | Rate source and FY-average date convention not approved | Keep native currency; suppress converted comparisons |
| **Licensed filing retrieval** | Source-backed | 3 — `01e`, `01f`, `02b` | Adjusted-EBIT reconciliation needs an approved 10-K / annual report source | Label values reported or unadjusted; gate filing-dependent views |
| **Peer scoring and set policy** | Mixed | 3 — `01f`, `02c`, `02e` | Weights and target anchoring are source gaps; threshold, minimum size and tie-breakers are design questions | Version the config, expose components, require partner confirmation |
| **Canonical taxonomy family** | Source-backed | 2 — `01b`, `01f` | `BAIN_*` and `LEVEL1..6` mappings materially disagree — agreement only **63%** | Preserve both with provenance until a versioned policy is approved |
| **SIC missing from CapIQ exports** | Source-backed | 2 — `01b`, `01f` | Taxonomy CSV has a SIC-side key; the company universe has no join key | Expose source-provided Bain fields only; **never fabricate the join** |
| **CapIQ derived-data licensing** | Source-backed | 2 — `01a`, `01b` | Storage, local indexing and retention rights for normalized exports unconfirmed | Restrict artifacts to the approved environment; retain snapshot metadata |
| **Compliance policy and escalation** | Source-backed | 1 — `01b` | Rules, outcomes, owner and review escalation undefined | Labelled non-production `clear` / `blocked` / `review_required` stub |

### P1

| Blocker | Origin | Journeys | Unresolved | Interim in the artifact |
| ------- | ------ | -------- | ---------- | ----------------------- |
| **Business-unit source and coverage** | Source-backed | **4** — `01c`, `01f`, `02c`, `02d` | Inspected CapIQ source has no segment or BU facts | Enable BU scope only for enumerated eligible metrics |
| **Confidence formula** | Mixed | 3 — `01d`, `01f`, `02a` | Confidence not built; weights and thresholds are proposed design questions | Return confidence inputs, withhold a composite label |
| **Private-company evidence floor** | Derived | 3 — `01f`, `02c`, `02e` | Minimum evidence for inclusion and confirmation undefined | Allow `data_required` candidates; exclude unavailable metrics |
| **Regional revenue source and coverage** | Source-backed | 3 — `01c`, `01f`, `02d` | Inspected CapIQ source has no geographic revenue mix | Disable hard filtering; allow only a confirmed directional preference |
| **Filing override implementation** | Mixed | 1 — `01e` | Hierarchy is confirmed (CapIQ → 10-K/annual report → LSEG) but the override mechanism is not implemented | Apply filing overrides only with page-level evidence |

### P2

| Blocker | Origin | Journeys | Unresolved | Interim in the artifact |
| ------- | ------ | -------- | ---------- | ----------------------- |
| **LSEG entitlement and propagation** | Source-backed | 2 — `01f`, `02b` | Licensed research access and user entitlement propagation unconfirmed | Keep the analyst path optional and disabled by default |
| **Evidence retention and legal hold** | Derived | 1 — `01e` | Deletion, retention and legal-hold behaviour undecided | Retain only within the approved environment |
| **Sage relationship data** | Source-backed | 1 — `01f` | Relationship fields, ownership and freshness unconfirmed | Treat relationship context as unavailable |
| **Search refresh and rollback SLA** | Derived | 1 — `01a` | Refresh cadence and rollback window for the immutable search artifact undecided | Expose the search snapshot ID; manual version promotion |

### Waiting

| Blocker | Origin | Journeys | Unresolved | Interim in the artifact |
| ------- | ------ | -------- | ---------- | ----------------------- |
| **Employee SSO and RBAC architecture** | Mixed | 2 — `02a`, `02e` | Application-facing issuer, federation direction, claims, role owner, assignment lifecycle | Keep the Login journey pending; **do not treat email as authorization** |

Provenance recorded as *Stakeholder follow-up — email sent 2026-09-03*, so the clock on
this one started today. It is also what keeps Screen 01 undocumented.

## Tech Lead reading

**1. The provenance chain does not resolve from this workspace.** Every source-backed
blocker cites `OI 3.0 - Data and API Mapping by Screen v3.xlsx` down to the cell
(`Spec Conflicts!B13:F13`, `Open Questions!B26:F26`, and so on). That workbook **is not in
the `OI30` mirror** and no mirrored page references it. The citations are specific enough
to be checkable — but not by anyone working from Confluence. **Twelve of the thirteen P0
and P1 blockers cite it**, so until it is attached to a page, nearly the whole register
rests on a source the team cannot open.

**2. Four data-source gaps generate most of the register.** FX, licensed filings,
SIC/taxonomy, and segment/BU-plus-regional coverage account for 17 of the 42 instances
across six blockers. They are not six separate problems to work; they are four upstream
answers. Three of the four are CapIQ-side, which is the same supplier already blocking
standing agenda item
4 on rate limits — so CapIQ is now blocking licensing, coverage and throughput at once,
and is a single owner conversation rather than three.

**3. Adjusted EBIT tolerance is the single highest-leverage item.** It touches 5 of 11
journeys and is the only blocker that reaches the confirm step. Its interim —
never emit `reconciled=true` without a configured threshold — is the right call and
means the reconciliation flag is dead until someone approves a number. It is a threshold,
not a build: one decision closes it.

**4. Three blockers are inferred, not requested.** Private-company evidence floor,
evidence retention and legal hold, and the search refresh/rollback SLA are labelled
*Derived recommendation* — the artifact is explicit that they are "not a stated workbook
requirement". They are sound proposals, and retention/legal hold lands squarely in the
empty [Security Design](../confluence/oi30/architecture/opportunity-indicator-architecture-high-level/security-design-processing-ai-and-data-19705167996.md)
page's territory. Chasing a stakeholder for these will fail, because nobody owes an
answer. They need a ruling recorded in `decisions/`.

**5. GLS exposure.** FX, licensed filings and the adjusted-EBIT tolerance all gate
benchmark numbers, and benchmark numbers are the demo. With the drillability requirement
holding, every converted or adjusted figure in a GLS run is currently either native
currency, labelled unadjusted, or suppressed. That is defensible on stage — but it is a
deliberate demo-scope decision, not a detail, and it should be made rather than
discovered.

**6. Where it overlaps what we already track.** LSEG here is a P2 entitlement question,
distinct from the empty LSEG integration page in
[open-questions](open-questions.md); Sage is recorded as "not built" in both. The
compliance-policy gap is the first concrete instance of the missing Security Design page
biting a specific endpoint — `01b` cannot define its `409 review_required` semantics
without it.
