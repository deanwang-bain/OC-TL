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

## The unknown that could change this

**What GLS actually is has not been written down.** The
[GLS Feature Set](https://bainco.atlassian.net/wiki/spaces/OI30/pages/19761725586) page is
empty. [MVP - to be signed off](https://bainco.atlassian.net/wiki/spaces/OI30/pages/19619676190)
says only: *"Balance speed with scalability to be discussed based on discovery finding.
Clear assessment of what feasible needed to make strategic decision on GLS presentation."*

If GLS is a **throwaway demonstration** — no client data, no persistence beyond the
session, nothing carried forward — a VM spike is defensible, and this recommendation
should be revisited on that basis. If GLS is a **version people will use**, or if any
real client financial data touches it, the recommendation stands unchanged.

That distinction should be settled before the deployment decision, not after.

## Consequences

- Container Apps from the start means the GLS environment is the MVP environment. No
  migration, and the security posture holds by default rather than by effort.
- A thin pipeline needs an explicit written list of what was deferred, or "defer" becomes
  "forget". The deferred items above are that list.
- If GLS turns out to be a throwaway demo, this decision is reversed cheaply — nothing
  here is expensive to undo, which is the point of taking it now.

## Promotion

Should become a Confluence ADR, and would partly populate the empty
[Deployment Design (CI/CD)](https://bainco.atlassian.net/wiki/spaces/OI30/pages/19705233507)
page.
