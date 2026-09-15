---
id: 003
date: 2026-09-15
status: proposed
---

# 003 — How OI 3.0 is run after initial development

## Context

The programme is funded and staffed to build. Nothing written anywhere says who runs the
result. A search of the OI30 space for hypercare, handover, BAU, service level, on-call or
runbook returns nothing, and the five pages that would normally carry the answer —
[Security Design](https://bainco.atlassian.net/wiki/spaces/OI30/pages/19705167996),
[NFR Design Choices](https://bainco.atlassian.net/wiki/spaces/OI30/pages/19704905798),
[Observability](https://bainco.atlassian.net/wiki/spaces/OI30/pages/19705430028),
[Endpoints & Interfaces](https://bainco.atlassian.net/wiki/spaces/OI30/pages/19704938600)
and [Deployment Design (CI/CD)](https://bainco.atlassian.net/wiki/spaces/OI30/pages/19705233507)
— are all empty. So this is reasoning from decisions that *are* written down, not the
application of an existing rule.

The question was asked as three: how the tool is run, what resource that needs, and how one
FTE plus temporary staff divide the work. They are one question, because the answer to the
third constrains the first.

### The failure mode this has to be designed against

For most internal tools the thing you protect against is downtime. Here it is not.

OI 3.0's entire claim is that a number is defensible —
[Design Principles](https://bainco.atlassian.net/wiki/spaces/OI30/pages/19628884086) makes
trust the central adoption barrier, and every figure drillable to its source, confidence and
reasoning. A tool that is *down* embarrasses nobody: the partner reverts to the COE team and
the two-to-three-day path. A tool that is **quietly stale** renders a peer benchmark from a
superseded CapIQ extract, attaches a confidence badge and a provenance trail to it, and puts
it in front of a CEO.

**Silent degradation is the expensive failure, and it is invisible to uptime monitoring.**
That single fact is what shapes everything below: the run function is mostly about keeping
the analysis correct and current, not about keeping servers up. Roughly three-quarters of the
recurring effort sits in content, data and model maintenance, and the conventional
availability work is the small remainder — which is the reason a one-FTE-owner model is
credible at all.

### What the record already fixes

Four things are settled and materially reduce the ask.

| Already decided | Consequence for run |
| --------------- | ------------------- |
| *"DevOps, cloud infrastructure, and CI/CD pipelines are Bain-owned"* ([Andromeda](https://bainco.atlassian.net/wiki/spaces/OI30/pages/19691733117)) | No platform team to stand up. The run function consumes TSG/Andromeda, it does not replace them |
| Container Apps, not AKS, because *"adopting AKS means adopting cluster upgrades, node pools, ingress controllers and a platform team to run them"* ([§3.1](https://bainco.atlassian.net/wiki/spaces/OI30/pages/19751338017)) | The compute layer was explicitly chosen to need no operator. That choice has to be honoured, not quietly reversed by a busy run team |
| Managed services throughout, 3 Adopt to 5 genuinely-warranted Builds ([§10](https://bainco.atlassian.net/wiki/spaces/OI30/pages/19751338017)) | Patching, scaling and availability of the substrate are Microsoft's problem. Only five components are ours to keep alive |
| Definition versioning *"never overwrites"* ([§10.2](https://bainco.atlassian.net/wiki/spaces/OI30/pages/19751338017)) | A content change cannot retro-break a delivered deck. This is what makes a fast content-change lane safe, and it is load-bearing for the whole model below |

### What the record leaves as a run burden

And five things that make it heavier than a normal internal tool.

1. **Content changes need an engineer, at MVP.**
   [§11](https://bainco.atlassian.net/wiki/spaces/OI30/pages/19751338017) records definition
   authoring as *engineering-mediated through source control* at MVP, becoming *self-service
   for a Bain steward* at north star. The levers library, the Bain L1–L4 taxonomy, sector KPI
   sets and Bain experience ranges are live Bain IP that moves continuously — the
   [Screen 04 spec](https://bainco.atlassian.net/wiki/spaces/OI30/pages/19710705690) sources
   fourteen sub-levers from it. Every one of those edits is an engineering ticket until that
   mechanism change lands. **This is the largest single line of avoidable run cost in the
   programme.**

2. **Every release carries a fixed, non-trivial gate.**
   [§9.7](https://bainco.atlassian.net/wiki/spaces/OI30/pages/19751338017) makes AI red
   teaming (PyRIT), a human review sample and a full performance scenario **blocking** at
   pre-release. [§9.3](https://bainco.atlassian.net/wiki/spaces/OI30/pages/19751338017) loop 4
   states it plainly: *"Whether the output is any good. Nothing above answers this and nothing
   will."* A structured analyst review is a permanent, per-release staffing obligation that no
   automation removes.

3. **Model and prompt drift is a maintenance category most tools do not have.** Model
   selection *"happens at deployment against current availability"*
   ([§4.1](https://bainco.atlassian.net/wiki/spaces/OI30/pages/19751338017)), so a provider
   deprecation is a routine, externally-timed event. Each one needs offline regression against
   the golden dataset before it ships.

4. **The upstream data path is not yet repeatable.**
   [Data Contacts](https://bainco.atlassian.net/wiki/spaces/OI30/pages/19817627730) records
   10-K extraction at three API calls per company, one company at a time, 5–10 seconds a call,
   capped near 6,000 companies a day, and states the approach *"is not yet repeatable at
   scale"*. CapIQ API access still is not there, and sprints 1–2 run on a manual Excel extract
   converted to Parquet. Five upstream sources — VCC, CapIQ, IRIS, LSEG, Expert Search — each
   drift on someone else's schedule.

5. **Demand is bursty, not flat.**
   [§5.3](https://bainco.atlassian.net/wiki/spaces/OI30/pages/19751338017) expects usage
   *"bursty around deal cycles"*, and scale runs from *"100 users at MVP with low concurrency"*
   to *"2300 plus their teams at full scale"*
   ([ADR-009](https://bainco.atlassian.net/wiki/spaces/OI30/pages/19751960620)). A flat team
   sized for the peak is wasteful; a flat team sized for the trough fails in deal season. A
   permanent core plus surge is the shape the demand curve actually has — which is what makes
   the one-FTE-plus-temporary-staff framing in the question the right instinct.

## Decision

**One accountable Bain FTE owns the service. Execution capacity sits in a contracted
StatusNeo run pod and a budgeted surge envelope. Neither half works without the other.**

### Options considered

| # | Option | Why not |
| - | ------ | ------- |
| A | Build a Bain-internal run team | No such team exists, twenty-seven components, and the working knowledge of the calculation engine, the expression parser and the agent swarm sits with the people who wrote them. Rebuilding that knowledge costs more than renting it |
| B | Managed service, fully outsourced to StatusNeo | The levers library, the Bain taxonomy and the golden dataset are Bain IP and the product's actual differentiator. Handing the definition registry to a vendor hands over the thing the tool exists to protect — and leaves no Bain owner accountable for what a partner puts in front of a client, against the [Vision](https://bainco.atlassian.net/wiki/spaces/OI30/pages/19617939629)'s *"AI as enabler, not decision-maker"* |
| C | **Bain-accountable owner plus contracted run pod** | **Recommended.** Bain holds the IP, the decisions and the accountability; StatusNeo holds the code knowledge and the elastic capacity |
| D | No run function; absorb into the delivery squad indefinitely | The squad is funded to a date. More importantly this is the option that produces silent degradation, because nobody's name is against "is the benchmark still current" |

Stating the rejected options is deliberate —
[Technology Choices](https://bainco.atlassian.net/wiki/spaces/OI30/pages/19751338017) sets the
bar: *"A choice with no rejected alternative is usually a choice that was never made."*

### The support tiers

| Tier | Who | Handles | Target |
| ---- | --- | ------- | ------ |
| **L0** | The product itself | *"Why is this number what it is"* — answered by the drill-down the architecture already requires | The largest single deflection available |
| **L1** | Bain internal service desk | Access, SSO, entitlements, how-do-I, known issues | Resolve or deflect ≥60% without touching the run team |
| **L2** | Platform Owner (the FTE) + run pod | Triage, diagnosis, configuration, data refresh, known-defect workaround, all customer comms | Own every ticket that survives L1 |
| **L3** | StatusNeo run pod | Code fixes: engine, agents, extractors, rendering | Fix under the retainer; escalate scope to the Owner |
| **L4** | Platform and vendors | Andromeda/TSG, Azure, S&P/CapIQ, Okta/Entra, VCC | Raised by the Owner, never by a temp |

**L0 deserves the emphasis.** Transparency was specified as a trust requirement, but it is
also the support model's largest cost lever: a partner who can see how a figure was built does
not raise a ticket asking. Any change that weakens drill-down raises the run cost, and that
should be said out loud in review.

### The four change classes

"Ad hoc update" is where run budgets die, because everything arrives as one undifferentiated
stream of Teams messages. Split it into four lanes with different paths, different gates and
different approvers.

| Class | Example | Gate | Cadence | Approves |
| ----- | ------- | ---- | ------- | ------- |
| **1. Content** | A lever range, a sector KPI, a taxonomy node, a peer weight | Golden fixtures and trace replay. **No red team, no perf scenario** — no code changed | Continuous, batched weekly | Bain content steward |
| **2. Data** | Schema drift repair, snapshot refresh, new source field | Data tests, freshness checks | As needed; monthly batch calendar at north star | Platform Owner |
| **3. Model / prompt** | Provider deprecation, prompt improvement, tool-contract change | Offline regression (loop 3) **and** AI red team — [§9.4](https://bainco.atlassian.net/wiki/spaces/OI30/pages/19751338017) requires it on any tool-contract change | Bundled, at most monthly | Platform Owner + Tech Lead |
| **4. Feature** | New lever type, new export, new screen behaviour | Full pre-release gate | Quarterly planning, monthly train | Product Manager |

Class 1 is the one that matters. It is the highest-volume, lowest-risk lane, and it is safe to
run fast *because* definition versions never overwrite — a delivered deck re-derives against
its pinned version whatever is authored afterwards. Routing content changes through the
feature lane would be the single most expensive mistake available here, and it is the default
that happens if nobody separates them.

### Release cadence

**A monthly production train with a permanent hotfix lane — not the two-week build cadence.**

This is a deliberate departure from the two-week Scrum cycle in
[Ways of Working](https://bainco.atlassian.net/wiki/spaces/OI30/pages/19588612195), and the
reason is arithmetic. [§9.7](https://bainco.atlassian.net/wiki/spaces/OI30/pages/19751338017)
makes AI red team, human review sample and full performance scenario blocking at pre-release.
That is a few person-days every time. Twenty-six times a year in run phase is a standing tax
paid for a release frequency that a stable internal tool does not need. Twelve is
proportionate.

Hotfixes ship on demand and skip the pre-release gate; they do not skip the merge gates
(integration, golden fixtures, property tests, image scan), which is where the re-derivability
guarantee is actually protected.

### Resource envelope

Annualised FTE-equivalent, first full year after MVP. **These are estimates, and they cannot
be validated until the availability target is set** — open item 3 in
[§13](https://bainco.atlassian.net/wiki/spaces/OI30/pages/19751338017) is undefined, so no
availability commitment exists to size against.

| Stream | FTE-e | Source of capacity | New Bain headcount |
| ------ | ----: | ------------------ | ------------------ |
| Accountable ownership, L2 triage, release management, stakeholders | **1.0** | Platform Owner | **Yes — the one FTE** |
| L3 application fixes and defect burn-down | 0.8 | SN run retainer | No |
| Data source maintenance: extractors, schema drift, batch calendar | 0.6 | SN run retainer | No |
| Model and prompt regression, eval harness operation | 0.4 | SN run retainer | No |
| Content and definition changes, at MVP | 0.5 → 0.1 | SN run retainer, collapsing once self-service ships | No |
| Golden dataset curation, per-release output review (loop 4) | 0.3 | Bain analyst / KM, fractional | No — existing claim |
| Business ownership of levers, ranges, taxonomy | 0.2 | Bain content steward, fractional | No — existing claim |
| Infrastructure, CI/CD, substrate patching, security posture | 0.3 | TSG / Andromeda | No — already Bain-owned |
| L1 user support | 0.2 | Bain service desk | No — existing function |
| Ad hoc enhancements (class 4) | 1.0–1.5 | Surge, drawn per quarter | No |
| **Total** | **≈5.3–5.8** | | **1.0** |

Three things to read off that table.

- **One new permanent Bain head.** Everything else is contracted, fractional, or an existing
  function with a named claim on it. That is the substance of the recommendation.
- **The 0.5 → 0.1 line is the business case for the definition self-service surface.** It
  repays roughly 0.4 FTE-e a year, every year, and it removes the queue between a Bain
  steward's judgement and the number a partner sees. It is already scoped as *OI Lifecycle &
  Versioning* and *Technical Foundations* in
  [Post-GLS Feature Set](https://bainco.atlassian.net/wiki/spaces/OI30/pages/19800162379) —
  the recommendation is to prioritise it inside that set on run-cost grounds, not just
  product grounds.
- **This is lean, not padded.** Twenty-seven components, two runtimes, five genuinely custom
  builds including a hand-written expression parser, five upstream integrations, and an
  audience of Bain partners. If it has to be cut, cut the surge envelope and accept a longer
  enhancement queue — do not cut the eval and review streams, because those are the ones
  holding the line against silent degradation.

### Roles and responsibilities

Nine parties, one accountable owner per activity.

**A** accountable (one only, owns the outcome) · **R** responsible (does the work) ·
**C** consulted · **I** informed

| Activity | Platform Owner (FTE) | SN run pod | Surge / temp | Content steward | Analyst / KM | TSG / Andromeda | Service desk | PM | Tech Lead |
| -------- | :-: | :-: | :-: | :-: | :-: | :-: | :-: | :-: | :-: |
| Service health, incident command | **A** | R | – | – | – | R | I | I | I |
| L1 intake and deflection | C | – | – | – | – | – | **A**/R | I | – |
| L2 triage and diagnosis | **A**/R | C | – | – | – | C | I | – | – |
| L3 code fix | **A** | R | R | – | – | – | – | I | C |
| Release train and go/no-go | **A** | R | – | C | C | C | I | C | C |
| Pre-release output review (loop 4) | C | – | – | C | **A**/R | – | – | I | – |
| AI red team, per release | **A** | R | – | – | – | C | – | – | C |
| Golden dataset: build and curate | C | C | – | C | **A**/R | – | – | I | – |
| Model version change | **A** | R | – | – | C | C | – | I | C |
| Content / definition change | R | R | – | **A** | C | – | – | I | – |
| Data source repair and refresh | **A** | R | R | C | C | C | – | I | – |
| Security patching, dependency currency | **A** | R | – | – | – | R | – | – | C |
| Infrastructure, CI/CD, network, identity | C | C | – | – | – | **A**/R | – | – | C |
| Access grants and entitlement review | **A** | – | – | – | – | R | R | I | – |
| Audit digest publication, retention | **A**/R | C | – | – | – | C | – | – | C |
| Architecture change | R | C | – | – | – | C | – | C | **A** |
| Backlog priority, feature scope | C | – | – | C | – | – | – | **A** | C |
| Run budget and retainer scope | **A** | – | – | – | – | – | – | C | C |

#### What the FTE must never be the only person for

A one-person run function has one structural defect, and pretending otherwise is how it
fails at the first resignation or the first two-week holiday. Four things need a named
second from day one:

1. **Production access.** A second Bain individual holds break-glass. One person with sole
   production access is an audit finding as well as a continuity risk.
2. **Incident command.** A named deputy in the SN run pod, rehearsed, not nominated on paper.
3. **Release go/no-go.** The Tech Lead or PM can release without the Owner present.
4. **Working knowledge of the calculation engine and the expression grammar.** Documented to
   the standard where a competent engineer who has never seen it can make a change — and
   tested by having someone do exactly that, once a quarter.

#### What temporary staff must never own

Temporary and surge capacity is real engineering capacity, but four things stay with
permanent, accountable parties regardless of how busy the queue is:

- **The definition registry and the levers library.** Bain IP, and the thing the product's
  defensibility rests on. Steward-owned, always.
- **The golden dataset.** [§9.3](https://bainco.atlassian.net/wiki/spaces/OI30/pages/19751338017)
  calls it *"a deliverable, not a by-product"*. A reference set curated by whoever was
  available that quarter is not a baseline.
- **Production secrets, access grants and entitlement decisions.**
- **Their own release approval.** Surge staff propose; the Owner or the Tech Lead disposes.

One more, specific to this product: the
[Agent Validation Test Plan](https://bainco.atlassian.net/wiki/spaces/OI30/pages/19765133323)
forbids production documents in any test environment, because uploads may carry MNPI or PII.
That constraint binds hardest on temporary staff debugging a live incident, and it needs to be
in the onboarding of every surge engineer rather than discovered during one.

### Operating calendar

The calendar is what makes a one-owner model work. Without a fixed rhythm the Owner spends the
year interrupt-driven, and the maintenance streams — which are the ones preventing silent
degradation — are the first to be dropped.

| Cadence | What happens |
| ------- | ------------ |
| **Daily** | Overnight job review: trace replay against the case corpus, offline model regression, DAST. All alert rather than block ([§9.7](https://bainco.atlassian.net/wiki/spaces/OI30/pages/19751338017)), so someone has to actually read them — that someone is the Owner |
| **Weekly** | Ticket review with the run pod. Content-change batch ships. Data freshness check against all five sources |
| **Monthly** | Release train. Pre-release gate: red team, analyst review sample, performance scenario. Dependency and model currency review. Run-cost and token-spend review at the model gateway ([§8](https://bainco.atlassian.net/wiki/spaces/OI30/pages/19751338017) puts cost accounting there) |
| **Quarterly** | Surge envelope drawn and prioritised with the PM. Golden dataset extended. Access and entitlement review. Bus-factor test. Audit digest published — cadence to be set once retention is decided |
| **Annually** | Retainer scope reset against measured demand. Availability target revisited against actual usage |

### Freeze discipline

Demand is bursty around deal cycles and the tool is used to prepare for CEO meetings. Two
rules:

- **No class 3 or class 4 change ships inside a declared high-stakes window.** Content and
  hotfix lanes stay open.
- **The Owner declares the windows**, from the PM's view of the deal calendar. GLS in October
  is the first one, and demo readiness there already needs an owner distinct from MVP delivery
  — see `context/standing-agenda.md` item 7.

## Consequences

- **One new permanent Bain role**, defined in `roles/lead-engineer-platform-owner-oi.md`. That
  person joins the build as lead developer, which is the point — see the JD for why that
  sequencing is load-bearing rather than convenient.
- **A run retainer has to be negotiated with StatusNeo before the build contract ends**, not
  after. Renegotiating from a standing start once the delivery squad has dispersed is the
  expensive path, and the knowledge it is buying decays from the day the last developer rolls
  off.
- **Three claims on existing Bain capacity need to be named, not assumed**: analyst/KM time
  for the golden dataset and per-release output review, a business content steward for the
  levers library, and the service desk for L1. All three are currently nobody's, and the
  golden dataset one is already flagged as unowned in the daily briefing.
- **A monthly release train is slower than the build cadence.** Accepted deliberately: the
  cost is queued enhancements, the benefit is not paying the pre-release gate twenty-six times
  a year.
- **The observability gap is now a run blocker, not just a review gap.** A run team cannot
  operate to a standard that has not been written. Whoever owns the
  [Observability page](https://bainco.atlassian.net/wiki/spaces/OI30/pages/19705430028) is now
  on the critical path to this model working.

### What has to be decided before this can be costed

Five of these are already open items on other people's lists; the point here is that they all
land on the run model, and four of them make it impossible to price.

| # | Open item | Where it sits | What it blocks here |
| - | --------- | ------------- | ------------------- |
| 1 | **Availability target** | [§13 item 3](https://bainco.atlassian.net/wiki/spaces/OI30/pages/19751338017) | Whether this is business-hours support or an out-of-hours rota. That is the difference between one FTE and three, and it is the single largest uncertainty in the table above |
| 2 | **Observability and alerting standard** | [page empty](https://bainco.atlassian.net/wiki/spaces/OI30/pages/19705430028) | There is no defined signal set, so there is nothing for L2 to watch and no definition of "degraded" |
| 3 | **NFR targets** | [page empty](https://bainco.atlassian.net/wiki/spaces/OI30/pages/19704905798) | No latency budget means no way to say whether a slow run is an incident |
| 4 | **Audit retention period** | [§13 item 4](https://bainco.atlassian.net/wiki/spaces/OI30/pages/19751338017) | Digest publication cadence and storage sizing — both recurring run obligations |
| 5 | **Golden dataset owner** | Unowned; flagged in `context/daily/2026-09-15.md` | Loop 3 has nothing to compare against, so **the run team cannot safely change a model**. A build-phase gap with a direct run-phase consequence |
| 6 | **CapIQ API access and rate limits** | [§13 item 2](https://bainco.atlassian.net/wiki/spaces/OI30/pages/19751338017) | The size of the data-maintenance stream, and whether the manual extract becomes a permanent run task |
| 7 | **Deployment topology and rollback** | [page empty](https://bainco.atlassian.net/wiki/spaces/OI30/pages/19705233507) | What a hotfix actually does. `decisions/002` deferred multi-environment promotion and blue/green for GLS; run phase is when that deferral comes due |

Items 1 and 2 are the two to chase first. Neither is expensive to write, and between them
they set the shape of the whole function.

## Promotion

Should become a Confluence page in its own right — the space has no operations or service
section at all, which is itself worth noting. Items 2, 3, 4 and 7 above would also populate
four of the empty high-level design pages, so writing this up creates pressure in a useful
direction.
