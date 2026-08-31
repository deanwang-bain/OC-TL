---
id: 001
date: 2026-08-31
status: proposed
---

# 001 — One repository, a small number of independently deployable services

## Context

Dipesh Bhardwaj, StatusNeo's architecture counterpart, asked which services are created
separately versus in a single monorepo at MVP.

**Nothing in the OI30 space addresses repository structure.** A search across all 71
pages returns no mention of monorepo, repository layout, or repo-per-service. This is
an undocumented area, so the recommendation below is reasoning from decisions that *are*
written down, not the application of an existing rule.

The two questions are also separable, and worth separating before answering: **how the
code is stored** is not **how it is deployed**. A monorepo can produce many deployables;
many repos can produce one. Conflating them is what usually makes this argument hard.

## Decision

**One repository. Roughly three to six independently deployable services at MVP, not
twenty-seven.**

### Why one repository

[Technology Choices §3.2](https://bainco.atlassian.net/wiki/spaces/OI30/pages/19751338017)
splits the backend across two runtimes and states the cost plainly: *"two toolchains, two
dependency scanners, two base images. Accepted."* A single repository is what keeps that
accepted cost from compounding — one place for the OpenAPI contracts, one CI definition
per gate, one dependency-scanning configuration per ecosystem.

The Node services are described as those *"whose types are shared with the frontend"*.
Shared types across a repository boundary need a published package and a version
lockstep; inside one repository they are an import. That argument is made by the source
itself, not invented here.

The programme has **twenty-seven components**. Twenty-seven repositories at MVP, with the
delivery team currently onboarding, would mean coordinating twenty-seven release cycles
to ship one feature.

### Why not one deployable

Three things in the written record force real service boundaries:

1. **The calculation engine must be a service on day one.** §10.2 states it is *"the one
   component Bain can reuse, which is the argument for building it as a service on day
   one."* This is the strongest boundary statement in the space.
2. **The runtime split is a hard boundary.** §3.2: *"A service that would need both is a
   service drawn wrong."* Node and Python cannot share a deployable, so the split is
   forced regardless of preference.
3. **Deferring boundaries is the expensive option.** T10 records the separate APIM
   product for platform consumers as *"Low, and much higher if deferred."* §11 adds a
   **new trust boundary** at north star when other Bain teams consume the platform API.
   A boundary drawn late is drawn through running code.

### The rule to apply

Rather than prescribing a decomposition — that is StatusNeo's to draw — apply two tests:

- **Runtime test.** Python for the calculation engine, document parsing, agent workers,
  and anything on a model path. Node for IO-bound services whose types are shared with
  the frontend: case, composition, rendering, evidence, audit, peer curation. These
  cannot merge.
- **Consumer test.** Anything another Bain team will consume independently is its own
  service now. Today that is the calculation engine. Everything else can start merged
  inside its runtime and split when a reason appears.

Domains from
[Domain Architecture](https://bainco.atlassian.net/wiki/spaces/OI30/pages/19705004114)
remain module boundaries inside a service — CQRS handlers and bounded domains do not
each need a deployment.

## Consequences

- A monorepo needs path-filtered CI from the start, or every change runs every gate.
  Cheap to set up now, painful to retrofit.
- Independent deployability must be real, not notional: no shared database schema
  written by two services, no import across a service boundary that should be an API
  call. This is worth checking in review, because a monorepo makes the violation easy.
- Splitting a service out later is routine. Merging two that should never have been
  split is not — which is why the consumer test errs toward fewer services, except where
  the record already names one.

## Promotion

Should become a Confluence ADR. Repository and deployment topology is exactly the kind
of decision the ADR set covers, and its absence is a gap rather than an omission.
