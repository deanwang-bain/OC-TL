---
role: "Lead Engineer, Opportunity Indicator → Platform Owner"
status: draft
date: 2026-09-15
headcount: "1.0 FTE, permanent, Bain"
---

# Lead Engineer → Platform Owner, Opportunity Indicator 3.0

**Draft for Tech Lead and HR review.** Grade, band, location and employment terms are
deliberately absent, because those are not for this document to set. Everything below is the
shape of the job.

## About Opportunity Indicator 3.0

OI 3.0 is an AI-powered tool that helps Bain partners prepare for client conversations. It
automates the research, benchmarking and deck creation that today takes a team of COEs and
consultants two to three days, targeting roughly 30 minutes end to end.

Four characteristics make it an unusual engineering problem:

- **Transparency is a requirement, not a feature.** Any number a partner sees must be
  drillable to its data sources, its reasoning and its confidence level. Provenance has to be
  carried through every calculation path, and it cannot be retrofitted.
- **Figures must be re-derivable exactly, years later.** A pinned set of inputs plus a pinned
  definition version must reproduce the original figure byte for byte.
- **The system mixes deterministic and probabilistic components by design.** Financial
  calculations are deterministic, version-controlled services. Research, synthesis and
  narrative are produced by an orchestrated set of AI agents. The boundary between the two is
  a deliberate design property, and it is what keeps the output defensible.
- **The partner retains judgment.** The stated principle is "AI as enabler, not
  decision-maker". Partners are accountable for what reaches a client.

The architecture is cloud-native and headless, on Azure: a React and TypeScript front end,
Python and Node services in containers, a custom calculation engine, and an agent layer
reaching the same capability set through governed interfaces. There are roughly 27 components
and five genuinely custom builds, of which the calculation engine is the most consequential.

**Delivery model.** StatusNeo, a delivery partner, writes the application code. Bain holds
product and architecture ownership. Cloud infrastructure, CI/CD and platform security are
owned by Bain's internal technology group. This role is Bain's senior technical presence
inside that arrangement.

**Scale.** About 100 users at MVP with low concurrency, rising to 2,300 partners plus their
teams at full scale. Usage is expected to be bursty around deal cycles rather than flat.

## In one line

Build OI 3.0 as StatusNeo's technical counterpart on the Bain side, then own it as a live
service used by Bain partners to prepare for CEO conversations.

## Why the role is shaped this way

This is one role in two phases, and that is the point rather than a convenience.

The re-derivability guarantee is bought with a closed expression grammar and a hand-written
parser of roughly a thousand lines. That is a deliberate trade: a definition language that
could import a library could not promise to reproduce a 2026 figure in 2031, because doing so
would mean reproducing the interpreter and every transitive dependency as they stood.

A guarantee of that kind is not maintained from documentation. Someone has to hold the
reasoning behind it: which invariants the property-based tests assert and why, what the golden
fixtures are pinned against, and what a failed trace replay actually means. Hiring a run owner
after the build ends means paying to reconstruct that reasoning at exactly the moment the
people who had it have rolled off.

So the sequencing is deliberate. **The person who will run the service helps build it, and
spends the build phase buying down the cost of the run.** Three build-phase deliverables exist
for that reason, and they appear in the accountabilities below: the observability and alerting
standard, the runbook set, and the path that lets a business steward author definitions
without an engineer. All three are cheap during the build and expensive afterwards.

## Where the role sits

| | |
| --- | --- |
| **Reports to** | Tech Lead, OI 3.0, during the build. To be confirmed for the run phase |
| **Works with daily** | StatusNeo delivery squad, Product Manager |
| **Works with regularly** | Internal platform and infrastructure teams, knowledge management and analyst teams, and the owners of the upstream financial data sources |
| **Manages** | No direct reports at MVP. Directs a contracted StatusNeo run pod and surge capacity in the run phase |

## Phase one: Lead Developer, through MVP and first demo

Bain's senior technical presence inside a squad delivering a system with 27 components, two
runtimes and an agent layer.

**Accountable for**

- **Technical quality of what StatusNeo ships.** Design review, code review, and holding the
  line on the decisions that are load-bearing: business rules kept out of the client,
  calculation authority in one place, the deterministic and probabilistic boundary respected,
  and an evidence binding on every claim.
- **Hands-on build of the components Bain cannot afford to hold at arm's length.** Primarily
  the calculation engine, the expression grammar and the definition registry. These are the
  genuinely differentiated builds, and the calculation engine is the one component other Bain
  teams are expected to reuse. This is a writing-code role, not a reviewing-code role.
- **The evaluation harness and the golden dataset**, jointly with Bain analysts. The golden
  dataset is a fixed set of target companies with reviewed reference peer sets, expected
  opportunity themes and known-good claims. Without it there is no baseline to regress model
  and prompt changes against, and no model can be changed safely once the service is live.
- **Writing the operational standard, which does not exist yet.** There is currently no
  written observability standard, no non-functional targets beyond accessibility, and no
  documented deployment topology. The person who will be woken up by this system should be the
  one who defines what it emits, what "degraded" means, and what a rollback does.
- **The runbook set, written during the build.** One per failure mode, each tested by someone
  who did not write it.
- **The definition self-service path.** At MVP, changing a lever range, a sector KPI or a
  taxonomy node requires an engineer and a source-control change. Moving that to steward
  authoring is the largest single reduction in this role's own future workload, worth roughly
  0.4 FTE a year. Argue for it, then build it.

## Phase two: Platform Owner, from go-live

Single accountable owner for OI 3.0 as a live service, directing contracted capacity rather
than managing a team.

**Accountable for**

- **Service health and incident command.** Second-line triage, customer communication, and
  every ticket that survives the first-line service desk.
- **The release train.** A monthly production release with a hotfix lane, and the go or no-go
  decision against a gate that blocks on AI red teaming, a structured analyst review of output
  quality, and a full performance scenario.
- **Currency of the analysis, which is the real job.** Data sources drift, benchmarks go
  stale, and model versions are deprecated on a provider's schedule rather than ours. The
  expensive failure here is not downtime: a stale figure ships with a confidence badge and a
  full provenance trail attached, in front of a client, and no uptime monitor sees it. That is
  why the role exists and why it is owned at Bain.
- **Directing the StatusNeo run pod and the surge budget:** scope, priority, quality bar, and
  the commercial conversation about the retainer.
- **Cost.** Model and token spend at the gateway, cloud consumption, and retainer draw.
- **Audit and access obligations.** Audit digest publication, retention, and entitlement
  reviews.
- **Keeping the architecture honest under operational pressure.** A run function under load
  reaches for the expedient fix. The hosting platform was chosen specifically so that no
  dedicated platform team is needed, and the closed grammar was chosen specifically to avoid an
  execution escape surface. Both are easy to erode one incident at a time.

## What we are looking for

### Essential

- **Senior hands-on engineer, comfortable in both Python and TypeScript.** The split between
  the two runtimes is a hard architectural boundary, not a preference, and this role works
  across it.
- **Has personally owned something in production** that other people depended on, and can
  describe a failure they caused and what they changed afterwards. This matters more here than
  any specific technology on the list.
- **Real depth in one of the two halves and genuine competence in the other:** production
  backend and data engineering, or applied AI and agent systems. Both at depth is rare enough
  that we are not requiring it.
- **Has worked on a system where the numbers had to be right** and could be challenged, such
  as financial calculation, risk, pricing, regulatory reporting or actuarial work. This is not
  a nice-to-have. The whole product is an argument about defensibility, and someone who has
  never had a figure contested will underweight what that costs to build.
- **Has evaluated non-deterministic systems properly:** regression suites over model output,
  assertions on invariants and distributions rather than exact strings, and enough judgement to
  tell a metric that moved because the model changed from one that moved because the product
  broke.
- **Cloud-native delivery on a managed platform**, ideally Azure: containers, managed identity,
  secret management, private networking, and OpenTelemetry instrumentation.
- **Has worked effectively through a delivery partner.** This role does not command the squad.
  It sets the bar, argues for it, and gets there without formal authority.
- **Writes clearly.** A substantial part of both phases is written work: standards, runbooks,
  reviews and recommendations.

### Strongly preferred

- FastAPI, and modern React with TypeScript, in that order of importance.
- Agent orchestration in production: tool contracts, streaming, effort budgeting, and failure
  handling. Experience of a specific framework is a bonus rather than an expectation, since the
  orchestration substrate was selected recently and nobody has years on it.
- Analytical data work: columnar file formats, embedded query engines, and warehouse layering.
- Document generation at fidelity: OOXML, headless rendering, and template systems.
- Exposure to consulting or professional-services delivery, and to the tolerance senior users
  have for a tool that is wrong once.

### Explicitly not required

- Kubernetes depth. A managed container platform was chosen precisely to avoid needing it.
- Line-management experience. This is a technical-ownership role.
- Prior Bain experience.

## What this role is not

Each of these is a plausible misreading that would produce the wrong hire.

- **Not an infrastructure or platform engineer.** DevOps, cloud infrastructure and CI/CD are
  owned by Bain's internal technology group. This role consumes them.
- **Not the Product Manager.** Feature scope and priority sit with the PM.
- **Not the architecture authority.** Architecture decisions belong to the Tech Lead and the
  architecture decision record process. This role is the strongest technical voice in that
  conversation, and it implements the outcome.
- **Not a team lead with reports.** Influence here comes from being the person who wrote the
  hard part and is still there a year later.

## Success measures

| By | Looks like |
| -- | ---------- |
| **3 months** | Trusted inside the StatusNeo squad. Contributing to the calculation engine directly. Observability standard drafted and agreed |
| **6 months** | First major demo delivered without a technical incident. Runbooks written and tested by someone else. First version of the golden dataset exists, with a named curation owner |
| **12 months** | Live service with a defined and met availability commitment. Content changes shipping routinely without engineering involvement. Bus-factor test passed: another engineer made a calculation-engine change unaided |
| **18 months** | Run cost per analysis trending down. Enhancement queue predictable rather than reactive. The role is replaceable, which is the real measure |

## Risks in this role, stated plainly

A job description that hides these produces a bad hire and a short tenure.

1. **Key-person concentration is designed into this role.** The mitigations belong in the job
   from day one rather than after the first resignation: a named second for production access,
   a rehearsed deputy in the run pod, documentation treated as a graded deliverable, and a
   quarterly test in which someone else makes a change unaided.
2. **The build-to-run transition is where this kind of role usually fails**, because run work
   is interrupt-driven and build work is not. A fixed operating calendar protects the
   maintenance streams from the ticket queue, and it only works if it is defended.
3. **The audience is unforgiving.** The primary user is an accountable partner taking output
   into a client meeting. This role carries responsibility that is disproportionate to the
   headcount around it, and the right candidate should want that rather than merely accept it.
4. **Several foundations are not written yet.** The security, non-functional, observability,
   interface and deployment design standards are all still blank. The honest framing is that
   this role gets to write them, which is either the most attractive thing about the job or a
   reason to decline it. Better to find out which at interview.

## Open before this is posted

| Item | Owner |
| ---- | ----- |
| The availability target, which decides whether the run phase carries an out-of-hours obligation. This changes both the role and the contract | Bain |
| Grade, band and location | HR |
| Reporting line in the run phase | Tech Lead and PM |
| Whether the StatusNeo run retainer is agreed. This role directs it, and the description assumes it exists | Tech Lead, with commercial |
