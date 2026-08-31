---
id: 002
date: 2026-08-31
status: proposed
---

# 002 — Container Apps with a thin pipeline, not a VM, for GLS

## Context

StatusNeo asked whether to stand up a proper CI/CD pipeline on Azure Container Apps, or
deploy to a VM to keep focus on core functionality for GLS.

The instinct behind the question is sound: GLS has a date, and pipeline work is not
product work. But the question bundles two things — **which platform** and **how much
pipeline** — and they have different answers. The platform is already decided and decided
for a capability reason; the pipeline scope is genuinely adjustable.

## Decision

**Deploy to Container Apps. Cut the pipeline, not the platform.**

### Why not a VM

Four things in the record argue against it, in descending order of weight.

1. **Container Apps was selected for a capability, not a preference.**
   [Technology Choices §3.1](https://bainco.atlassian.net/wiki/spaces/OI30/pages/19751338017)
   rejects App Service with: *"No dynamic sessions, which the ad hoc dataset composition
   capability needs. Weaker per-revision mTLS and weaker event-driven scaling."*
   Sandboxed execution via Container Apps dynamic sessions is a listed choice for **both**
   phases. A VM has no equivalent — sandboxing would be hand-rolled, which is the kind of
   escape surface the closed-grammar decision (T6) was explicitly designed to avoid.

2. **The security posture assumes managed infrastructure.** §7 specifies private
   endpoints with public access disabled, Front Door Premium with WAF, Entra managed
   identities, and Key Vault references. On a VM each is rebuilt by hand or silently
   dropped. The
   [Security Design](https://bainco.atlassian.net/wiki/spaces/OI30/pages/19705167996)
   page is **empty**, so there is no written control set to fall back on and no baseline
   to check the shortcut against.

3. **It creates a mechanism change where the record says there is none.** §11 lists
   Compute as MVP *Container Apps* → north star *Unchanged*, nature of change *None*. It
   also says the four mechanism changes *"are the story"* and would be *"the first thing
   a Bain architect challenged."* A VM adds a fifth, in the layer that currently has
   zero.

4. **Reversibility runs the wrong way.** T4 records Container Apps as *"Moderate.
   Containers move; the environment does not."* Building on a VM and migrating later
   means redoing deployment, networking, identity and secrets — after GLS, under more
   time pressure, not less.

### Why "no CI/CD" is not actually available

[§9.7](https://bainco.atlassian.net/wiki/spaces/OI30/pages/19751338017) already defines a
gate table where pull-request and merge stages **block merge**: unit, contract, lint,
CodeQL, secret scan, dbt compile, then integration, golden fixtures, property tests and
image scan. Those are CI, and they exist to protect the calculation engine's
re-derivability guarantee. They are not the expensive part and they are not optional.

The expensive part is CD: multi-environment promotion, blue/green, infrastructure as
code. That is where to economise.

### What to build for GLS

**Keep:** PR gates (unit, contract, lint, secret scan), image scan on merge, one-command
deploy to a single environment. `az containerapp up` from GitHub Actions is a working
deploy in an afternoon.

**Defer:** multi-environment promotion, blue/green and revision traffic splitting,
nightly DAST and load, visual regression, and infrastructure as code. The
[Agent Validation Test Plan](https://bainco.atlassian.net/wiki/spaces/OI30/pages/19765133323)
already places IaC validation outside QA MVP scope and excludes Terraform, Bicep, PSRule
and Checkov, so deferring it is consistent with an agreed boundary rather than a
shortcut.

This is roughly a day or two of setup — materially less than hand-building sandboxing,
identity and secret handling on a VM.

## What GLS is, confirmed

**GLS is the Global Leadership Summit, mid-to-late October, where OI 3.0 will be
demonstrated.** Confirmed by the Tech Lead on 2026-08-31; the
[GLS Feature Set](https://bainco.atlassian.net/wiki/spaces/OI30/pages/19761725586) page is
still empty and should carry this.

That is roughly **seven weeks** from this decision, in front of Bain's most senior
internal audience.

### It is a demo, but not a throwaway

This is the case that would most have favoured a VM, and it does weaken one of the four
arguments above — a demo on public company data does not need the full §7 posture, so
argument 2 carries less weight than it would for a production release.

It strengthens the others, though:

- **GLS work carries forward.** The
  [non-negotiable adjustments meeting](https://bainco.atlassian.net/wiki/spaces/OI30/pages/19751993421)
  discusses *"different versions, including GLS, MVP, and post-MVP"* — GLS is a version
  in the sequence, not a spike off to one side. A VM built for October is redone for MVP
  weeks later, inside the same programme. T4's *"containers move; the environment does
  not"* is paid twice, and the second payment lands while MVP scope is still moving.
- **The VM does not actually save time.** A container deployed by `az containerapp up`
  is an afternoon. Reaching demo-ready on a VM is not slower by much, but it is not
  faster, and it buys a migration.
- **Reputational cost replaces security cost.** A demo that falls over in front of
  global leadership is the expensive failure here, and revision-based rollback is worth
  more in that setting than SSH access.

**The recommendation is unchanged: Container Apps, thin pipeline.**

## Demo-specific risks, which now matter more than the platform choice

The deployment question is the smaller half of what the October date implies.

| Risk | Why it bites at GLS | Mitigation |
| ---- | ------------------- | ---------- |
| **Cold start** | Container Apps scaling to zero adds latency at the worst possible moment | Set minimum replicas to 1 for the demo window. Cheap, and easy to forget |
| **The 30-minute claim** | GLS is the first public test of the end-to-end target. The [NFR page](https://bainco.atlassian.net/wiki/spaces/OI30/pages/19704905798) is empty, so no latency budget exists to build against | Time a full run end to end well before October, not in demo week |
| **CapIQ latency** | Open item 2 — rate limits and per-call cost — is unresolved, and MVP uses real-time fetch per run. A live demo is exactly where a slow upstream shows | Resolve, or pre-warm a fixed demo dataset |
| **Demo data choice** | If the target is a real Bain client rather than a public company, MNPI applies. The test plan is explicit that production documents must not enter non-production environments | Choose a public company. Nike already appears throughout the screen specs |
| **Live versus pre-baked** | A leadership audience is unforgiving of a failed live run | Decide deliberately, and have a recorded fallback regardless |

## Consequences

- The GLS environment is the MVP environment. Nothing is thrown away, no migration sits
  between October and MVP, and the security posture holds by default rather than by
  effort.
- A thin pipeline needs an explicit written list of what was deferred, or "defer" becomes
  "forget". The deferred items above are that list.
- Minimum replicas and a fixed demo dataset are demo-week configuration, not
  architecture. They need an owner or they will be discovered on the day.

## Promotion

Should become a Confluence ADR, and would partly populate the empty
[Deployment Design (CI/CD)](https://bainco.atlassian.net/wiki/spaces/OI30/pages/19705233507)
page.
