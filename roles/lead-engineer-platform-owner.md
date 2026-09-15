---
role: "Lead Engineer, Opportunity Catalyst → Platform Owner"
status: draft
date: 2026-09-15
headcount: "1.0 FTE, permanent, Bain"
---

# Lead Engineer → Platform Owner, Opportunity Catalyst

**Draft for internal review.** Grade, band, location and employment terms are deliberately
absent, because those are not for this document to set.

## The role

Build Opportunity Catalyst as our senior technical counterpart to the delivery partner, then
own it as a live service.

One role, two phases, and the sequencing is the point. Opportunity Catalyst has to produce
figures that are defensible and re-derivable exactly, years later. That guarantee is bought
with a custom calculation engine, a closed expression grammar and a hand-written parser, and
it is not maintained from documentation: someone has to hold the reasoning behind it. Hiring a
run owner after the build ends means paying to reconstruct that reasoning at exactly the moment
the people who had it have rolled off.

So the person who will run the service helps build it, and spends the build phase buying down
the cost of the run. Three build-phase deliverables exist for that reason: the observability
and alerting standard, the runbook set, and the path that lets a business steward change a
definition without an engineer.

| | |
| --- | --- |
| **Headcount** | 1.0 FTE, permanent, Bain |
| **Reports to** | Tech Lead during the build. To be confirmed for the run phase |
| **Works with daily** | The delivery partner's squad, and the Product Manager |
| **Works with regularly** | Internal platform and infrastructure teams, knowledge management and analyst teams, and upstream data source owners |
| **Manages** | No direct reports. Directs a contracted run pod and surge capacity in the run phase |

## Phase one: Lead Developer, through MVP

- **Technical quality of what the delivery partner ships.** Design review, code review, and
  holding the line on the load-bearing decisions: business rules kept out of the client,
  calculation authority in one place, the deterministic and probabilistic boundary respected,
  and an evidence binding on every claim.
- **Hands-on build of what we cannot hold at arm's length:** the calculation engine, the
  expression grammar and the definition registry. This is a writing-code role, not a
  reviewing-code role.
- **The evaluation harness and the golden dataset**, jointly with our analysts. Without a
  reviewed reference set there is no baseline to regress model and prompt changes against, and
  no model can be changed safely once the service is live.
- **The operational standard, which does not exist yet.** There is currently no written
  observability standard, no non-functional targets and no documented deployment topology. The
  person who will be woken up by this system should define what it emits, what "degraded"
  means, and what a rollback does.
- **Runbooks, written during the build.** One per failure mode, each tested by someone who did
  not write it.
- **The definition self-service path.** At MVP, changing a lever range, a sector KPI or a
  taxonomy node needs an engineer and a source-control change. Moving that to steward authoring
  is the single largest reduction in this role's own future workload.

## Phase two: Platform Owner, from go-live

- **Service health and incident command.** Second-line triage, customer communication, and
  every ticket that survives the first-line service desk.
- **The release train.** A monthly production release with a hotfix lane, and the go or no-go
  decision against a gate that blocks on AI red teaming, an analyst review of output quality,
  and a performance scenario.
- **Currency of the analysis, which is the real job.** Data sources drift, benchmarks go stale,
  and model versions are deprecated on a provider's schedule rather than ours. The expensive
  failure here is not downtime: a stale figure ships with a confidence badge and a full
  provenance trail attached, in front of a client, and no uptime monitor sees it.
- **Directing the run pod and the surge budget:** scope, priority, quality bar, and the
  commercial conversation about the retainer.
- **Cost and compliance.** Model and cloud spend, audit digest publication, retention, and
  entitlement reviews.

## What we are looking for

### Essential

- **Senior hands-on engineer, comfortable in both Python and TypeScript.** The split between
  the two runtimes is a hard architectural boundary, and this role works across it.
- **Has personally owned something in production** that other people depended on, and can
  describe a failure they caused and what they changed afterwards. This matters more than any
  specific technology below.
- **Real depth in one of production backend and data engineering, or applied AI and agent
  systems, and genuine competence in the other.** Both at depth is rare enough that we are not
  requiring it.
- **Has worked where the numbers had to be right and could be challenged:** financial
  calculation, risk, pricing, regulatory reporting or actuarial work. Someone who has never had
  a figure contested will underweight what defensibility costs to build.
- **Has evaluated non-deterministic systems properly:** regression suites over model output,
  assertions on invariants and distributions rather than exact strings, and the judgement to
  tell a metric that moved because the model changed from one that moved because the product
  broke.
- **Cloud-native delivery on a managed platform, ideally Azure:** containers, managed identity,
  secret management, private networking, and OpenTelemetry instrumentation.
- **Has worked effectively through a delivery partner.** This role does not command the squad.
  It sets the bar and gets there without formal authority.
- **Writes clearly.** A substantial part of both phases is standards, runbooks and reviews.

### Strongly preferred

- FastAPI, and modern React with TypeScript.
- Agent orchestration in production: tool contracts, streaming, effort budgeting and failure
  handling. Framework-specific experience is a bonus rather than an expectation.
- Analytical data work: columnar formats, embedded query engines, warehouse layering.
- Document generation at fidelity: OOXML, headless rendering, template systems.
- Exposure to consulting delivery, and to the tolerance senior users have for a tool that is
  wrong once.

### Not required

- Kubernetes depth. A managed container platform was chosen precisely to avoid needing it.
- Line-management experience. This is a technical-ownership role.
- Prior Bain experience.

## What this role is not

- **Not an infrastructure or platform engineer.** DevOps, cloud infrastructure and CI/CD are
  owned by our internal technology group. This role consumes them.
- **Not the Product Manager.** Feature scope and priority sit with the PM.
- **Not the architecture authority.** Architecture decisions belong to the Tech Lead and the
  decision-record process. This role is the strongest technical voice in that conversation and
  implements the outcome.
- **Not a team lead with reports.** Influence comes from having written the hard part and still
  being there a year later.

## Success measures

| By | Looks like |
| -- | ---------- |
| **3 months** | Trusted inside the delivery squad. Contributing to the calculation engine directly. Observability standard drafted and agreed |
| **6 months** | First major demo delivered without a technical incident. Runbooks written and tested by someone else. Golden dataset v1 exists, with a named curation owner |
| **12 months** | Live service with a defined and met availability commitment. Content changes shipping without engineering involvement. Another engineer has made a calculation-engine change unaided |
| **18 months** | Run cost per analysis trending down. Enhancement queue predictable rather than reactive. The role is replaceable, which is the real measure |

## Two things to settle before this is posted

1. **Key-person concentration is designed into this role**, so the mitigations belong in the job
   from day one: a named second for production access, a rehearsed deputy in the run pod,
   documentation as a graded deliverable, and a quarterly test in which someone else makes a
   change unaided.
2. **The availability target is not set**, and it decides whether the run phase carries an
   out-of-hours obligation. That changes both the role and the contract, and it is the one
   open item that materially affects what we are hiring.

Also outstanding: grade and band with HR, the run-phase reporting line, and whether the run
retainer with the delivery partner is agreed, since this role directs it.
