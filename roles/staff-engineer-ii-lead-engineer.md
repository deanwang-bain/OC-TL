---
role: "Staff Engineer II (Lead Engineer), Opportunity Catalyst"
function: "Software Engineering"
grade: 9
status: draft
date: 2026-09-23
headcount: "1.0 FTE, permanent, Bain"
---

# Staff Engineer II (Lead Engineer), Opportunity Catalyst

**Software Engineering · Grade 9 · 1.0 FTE, permanent**

*Draft for internal review. Follows the Staff Engineer II job series; the Opportunity
Catalyst specifics are in the responsibilities and skills below.*

As the lead engineer for Opportunity Catalyst, the Staff Engineer II **owns the codebase**
through development and into live running. They set the technical design, take the hardest
components themselves, hold the bar on what the delivery partner merges, and stay accountable
for the code once it is in production: defects, third-level support, deployments, and the
maintenance that keeps the analysis correct.

This is a hands-on engineering role, and it is deliberately continuous across build and run.
Opportunity Catalyst has to produce figures that are defensible and re-derivable exactly,
years later. That guarantee lives in a custom calculation engine, a closed expression grammar
and a hand-written parser, and it cannot be handed over to someone who did not build it. The
person who writes those components is the person who keeps them correct in production.

## Responsibilities

### Core development, support and maintenance (80%)

- **Own the codebase.** Technical design authority across Opportunity Catalyst's services, and
  the standing bar for what gets merged: design review, code review, and the decisions that
  hold the product together as it grows.
- **Take the hardest components personally.** The calculation engine, the expression grammar
  and the definition registry are where the product's defensibility lives. They stay with this
  role rather than being delegated.
- **Create the technical design and lead the development team through execution**, working with
  Bain architects to validate designs, weigh trade-offs, and keep the system scalable as data
  volumes and user concurrency grow with adoption.
- **Own the test and evaluation harness** across both halves of the system: exact assertions and
  golden fixtures for the deterministic services, and regression over model output for the
  probabilistic ones. Without a reviewed baseline, no model or prompt change can ship safely.
- **Provide third-level technical support.** Diagnose defects, lead troubleshooting, and fix
  what breaks in production.
- **Lead code deployments and the release process**, including the pre-release quality gate and
  the go or no-go call on technical readiness.
- **Keep the code current once live.** Dependency and model version upgrades, data source
  repairs when an upstream schema drifts, and performance work. Benchmarks going stale is a
  worse failure here than downtime, because a stale figure still ships looking confident.
- **Write the operational standard and the runbooks.** What the system emits, what "degraded"
  means, what a rollback does, and one runbook per failure mode, each tested by someone who did
  not write it.
- **Work as a full member of an Agile team**, with full participation in team events and
  activities.

### Other (20%)

- **Mentor and grow engineers**, both Bain and partner, and raise the standard of what the team
  ships.
- **Reduce the cost of running the product.** The largest single win available is the
  self-service path that lets a business steward change a lever range or a sector KPI without
  an engineer and a source-control change.
- **Lead technical discovery and proofs of concept** to validate new tools, technologies and
  designs.
- **Share expertise on emerging technologies and lead knowledge sharing** across the team.
- **Support recruiting**, including resume screening and interviews.

## Knowledge, skills and abilities

- Serving as a technical lead or similar, leading engineers to deliver software using Agile
  methodology.
- Experience leading third-party, near-shore and off-shore delivery partners, setting the
  technical bar without formal authority over the team.
- Hands-on front-end development with modern technologies: TypeScript, React, HTML, CSS and
  current build tooling.
- Hands-on back-end development in **both Python and Node with TypeScript**. The split between
  the two runtimes is a hard architectural boundary here, and this role works across it.
- Hands-on experience with relational databases and SQL.
- Hands-on experience developing, configuring, deploying, maintaining and supporting software on
  a major cloud provider, ideally Azure: containers, managed identity, secret management,
  private networking and OpenTelemetry instrumentation.
- Experience with source control, build pipelines and deployment tools.
- Has built systems where the numbers had to be right and could be challenged: financial
  calculation, risk, pricing, regulatory reporting or actuarial work.
- Has tested non-deterministic systems properly: regression suites over model output, assertions
  on invariants and distributions rather than exact strings, and the judgement to tell a metric
  that moved because the model changed from one that moved because the product broke.
- Strong troubleshooting and issue resolution skills.
- Strong communication and presentation skills, including documenting complex design and
  processes for long-term support and maintenance.
- Results focused, analytical, self-motivated and proactive, with the entrepreneurial instinct
  to try something new when the standard answer does not fit.

Useful but not required: agent orchestration in production (tool contracts, streaming, failure
handling); analytical data work with columnar formats, embedded query engines and warehouse
layering; document generation at fidelity with OOXML and headless rendering.

## Experience

- Developing and running software products and solutions in production.
- Demonstrated knowledge of Agile software development and processes.
- Strong performance in prior software development positions.
- Providing technical leadership to a team of engineers.
- Owning a production service, including third-level support responsibility.
- Managing conflict and dependencies to deliver results.
- Managing communication among varied stakeholders, including external vendors.
- Strong analytical and problem-solving skills.

## Education and role type

- Bachelor's degree or an equivalent combination of education, training and experience.
- Certifications: not applicable.
- People management: individual contributor.
- Travel: not applicable.

## What this role is not

Worth stating, because each is a plausible misreading that would produce the wrong hire.

- **Not the Product Owner.** Scope, priority and roadmap sit with the Product Manager. This role
  owns the code, not the product.
- **Not an architecture-only role.** Design authority here comes from writing the hard parts,
  not from reviewing what others write.
- **Not an infrastructure or platform engineer.** Cloud infrastructure, CI/CD and platform
  security are owned by our internal technology group. This role consumes them.
- **Not a people manager.** Individual contributor, with technical leadership over the team.

## Notes for reviewers

1. **The availability target is not set**, and it decides whether the run phase carries an
   out-of-hours obligation. That changes the role and should be settled before the grade is
   confirmed.
2. **Key-person concentration is designed into this role**, so the mitigations belong in the job
   from day one: a named second for production access, a rehearsed deputy, documentation as a
   graded deliverable, and a periodic test in which another engineer makes a calculation-engine
   change unaided.
