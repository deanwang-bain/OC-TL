---
role: "Lead Engineer, Opportunity Indicator → Platform Owner"
status: draft
date: 2026-09-15
driven_by: "decisions/003-run-model-and-staffing-after-mvp.md"
headcount: "1.0 FTE, permanent, Bain"
---

# Lead Engineer → Platform Owner, Opportunity Indicator 3.0

**Draft for Tech Lead and HR review.** Grade, band, location and employment terms are
deliberately absent — those are not this workspace's to set. Everything below is the shape of
the job.

## In one line

Build OI 3.0 as StatusNeo's technical counterpart on the Bain side, then own it as a live
service used by Bain partners to prepare for CEO conversations.

## Why the role is shaped this way

This is one role in two phases, and that is the point rather than a convenience.

OI 3.0's central promise is that a figure is **re-derivable exactly, years later**.
[Technology Choices §3.3](https://bainco.atlassian.net/wiki/spaces/OI30/pages/19751338017)
buys that guarantee with a closed expression grammar, a hand-written parser, and definition
versions that never overwrite — and states the residual plainly: *"We own a parser. It is
roughly a thousand lines and it is the price of the re-derivability guarantee."*

A guarantee of that kind is not maintained from documentation. Someone has to hold the
reasoning behind it: which invariants the property-based tests assert and why, what the golden
fixtures are pinned against, what a trace replay failure actually means. Hiring a run owner
after the build ends means paying to reconstruct that reasoning at exactly the moment the
people who had it have rolled off.

So the sequencing is deliberate: **the person who will run it helps build it, and spends the
build phase buying down the cost of the run.** Three build-phase deliverables exist for that
reason and are named in the accountabilities below — the observability standard, the runbook
set, and the definition self-service path. All three are cheap during the build and expensive
afterwards.

## Where the role sits

| | |
| --- | --- |
| **Reports to** | Tech Lead, OI 3.0 (Dean Wang) during build; to be confirmed for run phase |
| **Works with daily** | StatusNeo delivery squad, Product Manager (Kasia Mrowca) |
| **Works with regularly** | TSG / Andromeda platform, VCC, KM and analyst teams, data source owners (S&P, CapIQ, IRIS, LSEG) |
| **Manages** | No direct reports at MVP. Directs a contracted StatusNeo run pod and surge capacity in run phase |
| **Delivery model** | StatusNeo writes the application code. This role sets the technical bar for it, and inherits it |

## Phase one — Lead Developer, through MVP and GLS

Bain's senior technical presence inside a squad delivering a system with twenty-seven
components, two runtimes and an agent swarm.

**Accountable for**

- **Technical quality of what StatusNeo ships.** Design review, code review, and holding the
  line on the decisions that are load-bearing — business rules out of the client, calculation
  authority in one place, the deterministic/probabilistic boundary
  ([§9.1](https://bainco.atlassian.net/wiki/spaces/OI30/pages/19751338017)), and evidence
  bindings on every claim.
- **Hands-on build of the components Bain cannot afford to hold at arm's length.** Primarily
  the calculation engine, the expression grammar and the definition registry — the components
  [§10.2](https://bainco.atlassian.net/wiki/spaces/OI30/pages/19751338017) identifies as
  genuinely differentiated, and the one Bain reuses elsewhere. This is a writing-code role,
  not a reviewing-code role.
- **The evaluation harness and the golden dataset**, jointly with Bain analysts. Without them
  loop 3 of the probabilistic track has nothing to compare against, and no model can be
  changed safely afterwards. This is currently unowned.
- **Writing the operational standard that does not exist yet.** The
  [Observability](https://bainco.atlassian.net/wiki/spaces/OI30/pages/19705430028),
  [NFR](https://bainco.atlassian.net/wiki/spaces/OI30/pages/19704905798) and
  [Deployment Design](https://bainco.atlassian.net/wiki/spaces/OI30/pages/19705233507) pages
  are blank. The person who will be woken up by this system should be the one who defines what
  it emits, what "degraded" means, and what a rollback does.
- **The runbook set, written during the build.** One per failure mode, tested by someone who
  did not write it.
- **The definition self-service path.** Moving definition authoring from
  engineering-mediated to steward-authored is the largest single reduction in this role's own
  future workload — roughly 0.4 FTE-e a year, per `decisions/003`. Argue for it, then build it.

## Phase two — Platform Owner, from go-live

Single accountable owner for OI 3.0 as a live service. The full operating model, support
tiers, change lanes and RACI are in
[`decisions/003`](../decisions/003-run-model-and-staffing-after-mvp.md); the summary is that
this role owns the service and directs contracted capacity rather than a team.

**Accountable for**

- **Service health and incident command.** L2 triage, customer communication, and every ticket
  that survives the service desk.
- **The release train.** A monthly production release with a hotfix lane, and the go/no-go
  against a pre-release gate that blocks on AI red teaming, an analyst review sample and a
  full performance scenario.
- **Currency of the analysis, which is the real job.** Data sources drift, benchmarks go
  stale, model versions are deprecated on a provider's schedule. A stale figure ships with a
  confidence badge and a provenance trail attached, in front of a client — which is why this
  matters more than uptime, and why it needs a named owner.
- **Directing the StatusNeo run pod and the surge envelope**: scope, priority, quality bar,
  and the commercial conversation about the retainer.
- **Cost.** Token and model spend at the gateway, Azure consumption, retainer draw.
- **Audit and access obligations.** Digest publication, retention, entitlement reviews.
- **Keeping the architecture honest under operational pressure.** A run function under load
  reaches for the expedient fix. Container Apps was chosen specifically so that no platform
  team is needed; the closed grammar was chosen specifically to avoid an escape surface. Both
  are easy to erode one incident at a time.

## What we are looking for

### Essential

- **Senior hands-on engineer, comfortable in both Python and TypeScript.** The runtime split
  is a hard architectural boundary, not a preference — this role works across it.
- **Has personally owned something in production** that other people depended on, and can
  describe a failure they caused and what they changed afterwards. This matters more here than
  any specific technology on the list.
- **Real depth in one of the two halves and genuine competence in the other**: production
  backend and data engineering, or applied AI and agent systems. Both, at depth, is rare
  enough that we are not requiring it.
- **Has worked on a system where the numbers had to be right** and could be challenged —
  financial calculation, risk, pricing, regulatory reporting, actuarial. Not a nice-to-have.
  The whole product is an argument about defensibility, and someone who has never had a figure
  contested will underweight what that costs to build.
- **Has evaluated non-deterministic systems properly**: regression suites over model output,
  assertion on invariants and distributions rather than strings, and enough judgement to know
  when a metric moved because the model changed and when it moved because the product broke.
- **Cloud-native delivery on a managed platform**, ideally Azure — containers, managed
  identity, secret management, private networking, OpenTelemetry instrumentation.
- **Has worked effectively through a delivery partner.** This role does not command the
  squad. It sets the bar, argues for it, and gets there without authority.
- **Writes clearly.** A substantial part of both phases is written: standards, runbooks,
  reviews, recommendations. The programme's best artefacts are written ones, and its worst
  gaps are unwritten ones.

### Strongly preferred

- FastAPI and modern React/TypeScript, in that order of importance.
- Agent orchestration in production — tool contracts, streaming, effort budgeting, failure
  handling. Microsoft Agent Framework specifically is a bonus, not an expectation; the
  substrate was selected two weeks ago and nobody has years on it.
- Analytical data work: Parquet, DuckDB, dbt, warehouse layering.
- Document generation at fidelity — OOXML, headless rendering, template systems.
- Exposure to consulting or professional-services delivery, and to the tolerance senior users
  have for a tool that is wrong once.

### Explicitly not required

- Kubernetes depth. AKS was rejected precisely to avoid needing it.
- Line-management experience. This is a technical-ownership role.
- Prior Bain experience.

## What this role is not

Worth stating, because each of these is a plausible misreading that would produce the wrong
hire.

- **Not an infrastructure or platform engineer.** DevOps, cloud infrastructure and CI/CD are
  Bain-owned via TSG and Andromeda. This role consumes them.
- **Not the Product Manager.** Feature scope and priority sit with the PM.
- **Not the architecture authority.** Architecture decisions belong to the Tech Lead and the
  ADR process. This role is the strongest technical voice in that conversation and implements
  its outcome.
- **Not a team lead with reports.** Influence here comes from being the person who wrote the
  hard part and is still there a year later.

## Success measures

| By | Looks like |
| -- | ---------- |
| **3 months** | Trusted inside the StatusNeo squad. Contributing to the calculation engine directly. Observability standard drafted and the empty page filled |
| **6 months** | GLS delivered without a technical incident. Runbooks written and tested by someone else. Golden dataset v1 exists with a named curation owner |
| **12 months** | Live service with a defined and met availability commitment. Content changes routinely shipping without engineering involvement. Bus-factor test passed: another engineer made a calculation-engine change unaided |
| **18 months** | Run cost per analysis trending down. Enhancement queue predictable rather than reactive. The role is replaceable — which is the real measure |

## Risks in this role, stated plainly

A JD that hides these produces a bad hire and a short tenure.

1. **Key-person concentration is designed into this role**, and the mitigations belong in the
   job from day one, not after the first resignation: a named production-access second, a
   rehearsed deputy in the run pod, documentation as a graded deliverable, and a quarterly
   bus-factor test. `decisions/003` lists these; they are the role holder's to keep honest.
2. **The build-to-run transition is where this kind of role usually fails**, because run work
   is interrupt-driven and build work is not. The operating calendar in `decisions/003` exists
   to protect the maintenance streams from the ticket queue. It only works if it is defended.
3. **The audience is unforgiving.** The primary persona is the accountable partner, taking
   output into a client meeting. This role carries responsibility that is disproportionate to
   the headcount around it, and the candidate should want that rather than merely accept it.
4. **Several foundations are not written yet.** Five high-level design pages are empty. The
   honest framing is that this role gets to write them — which is either the most attractive
   thing about the job or a reason to decline it, and it is better to find out which at
   interview.

## Open before this is posted

| Item | Owner |
| ---- | ----- |
| Availability target — decides whether the run phase carries an out-of-hours obligation, which changes the role and the contract | Bain, [§13 item 3](https://bainco.atlassian.net/wiki/spaces/OI30/pages/19751338017) |
| Grade, band and location | HR |
| Reporting line in run phase | Tech Lead / PM |
| Whether the run retainer with StatusNeo is agreed — this role directs it, and the JD assumes it exists | Tech Lead, commercial |
