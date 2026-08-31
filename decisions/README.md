# Decision log

Technical rulings made in this workspace — precedents set while reviewing code or
triaging requests, which are not yet written up as Confluence ADRs.

One file per decision, named `NNN-short-slug.md`, numbered sequentially.

## Relationship to Confluence ADRs

[OI 3.0 ADRs](../confluence/oi30/architecture/oi-30-architecture-decision-records-19751960620.md)
are the authoritative record for application decomposition, orchestration, and
persistence. ADR-001 to ADR-009 are Accepted, pending Bain architect review.

This log is the staging area: smaller rulings, and decisions taken before they are
formalised. **A ruling here that proves durable belongs in Confluence** — promote it,
then leave a pointer behind. Do not let this become a shadow architecture record.

## Format

```
---
id: NNN
date: YYYY-MM-DD
status: proposed | accepted | superseded by NNN
---

# NNN — <decision>

## Context
What forced a decision. Link the review or request that raised it.

## Decision
What was decided, stated so it can be applied to a future case.

## Consequences
What this commits us to, including the costs.

## Promotion
Whether this should become a Confluence ADR, and its status if so.
```
