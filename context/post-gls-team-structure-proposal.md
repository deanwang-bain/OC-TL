# Post-GLS team structure: transition from StatusNeo to Bain internal (PROPOSAL)

*Recommendation for the Tech Lead to sign off. Prepared 23 Oct 2026 from the Confluence mirror. Headcounts, contract terms and NGSS/BCN capacity are not in the mirror, so they appear below as inputs still needed, not as figures.*

## What the mirror gives us

| Fact | Source |
| --- | --- |
| Industrialisation starts ~23 Nov 2026, ~12 weeks (so to ~15 Feb 2027), under a separate SOW | [Onboarding - StatusNeo](../confluence/oi30/ways-of-working/onboarding-statusneo-19640975400.md) |
| 50+ partner rollout in late Nov / early Dec | [GLS Deployment Tracker](../confluence/oi30/architecture/opportunity-catalyst-architecture-high-level/deployment-design-ai-compute-data-components-cicd/oc-dev-staging-gls-deployment-tracker-19909279789.md), via `context/oi30-brief.md` |
| Bain-side roles today: Tech Lead (Dean), PM (Kasia), Architect (Sandeep), Designer (Joanna), Tech Lead back-up (Michelle) | Onboarding page above |
| BCN holds domain knowledge: the BCN PI team are "current OI report producers"; BCN resources already share validation of the cost-bar split | Onboarding page; [Cost bar split meeting notes](../confluence/oi30/data-requirements/cost-bar-split/meeting-notes-19799244847.md) |
| Andromeda is Bain's internal agentic platform; OI 3.0 is meant to consume it (model gateway, hosting, identity, observability) | [Andromeda](../confluence/oi30/ways-of-working/onboarding-statusneo/andromeda-bains-agentic-ai-platform-19691733117.md) |
| Bain analysts are already required for the golden dataset; other test ownership is "to be formalized" | [Agent validation test plan](../confluence/oi30/architecture/agent-validation-test-plan-19765133323.md) §17 |

**Not in the mirror:** what NGSS stands for or what it runs today, SN headcount by role, SOW notice terms, and any named BCN/NGSS engineers. I have not guessed these.

## Why the order of roll-off matters

Four things are thinly written down today, and each is knowledge SN holds that Bain will lose on roll-off:

1. Four design pages are blank (Security, NFR, Observability, Endpoints & Interfaces). The ARC tracker has 313 requirements with zero responses (standing agenda item 3).
2. The decision record lags the build (Azure AI Search, serpapi, gpt-5.2). See standing agenda items 4, 6 and 7.
3. The narrative agent does not exist yet, and GLS runs on a POC Foundry account.
4. Staging runs with shared Postgres compute and shared role names, "accepted for now" until after the partner rollout.

So I would roll off first where the code is best protected by tests and documents, and last where the knowledge lives in people's heads. That ordering is my judgment, not a documented rule.

## Workstreams and who could take them

| # | Workstream | Knowledge risk on roll-off | Natural Bain receiver |
| --- | --- | --- | --- |
| 1 | Frontend (React/TS/Vite) and BFF | Low to medium. Conventions are written down | BCN or NGSS engineers |
| 2 | Backend APIs (FastAPI REST, FastMCP) | Medium. ADR-009 store-ownership rule is unwritten | Same receiver as 1, so one team owns the stack end to end |
| 3 | Data integrations and peer selection (CapIQ, LSEG, IRIS/Glean, TSR) | High. Owners unnamed for most sources (see the post-GLS data sources draft) | BCN, who hold the domain |
| 4 | Agents (Foundry, peer discovery, narrative) | Highest. Narrative agent not built, model positions unrecorded | Needs a named Bain owner before any SN agent engineer leaves |
| 5 | Platform and run (Terraform, Container Apps, GitHub OIDC, on-call) | Medium. Tracker is unusually well documented | Whichever team already runs production apps at Bain |
| 6 | QA, agent validation, golden dataset | Medium. Bain analysts already required | BCN analysts plus one QA lead |
| 7 | Security and governance (OI3-21) | Unknown. Four design pages blank | Bain Security plus the Tech Lead |
| 8 | Product, UX, architecture | Already Bain | Unchanged |

## Ownership models (who ends up holding the keys)

| Model | Shape | For | Against |
| --- | --- | --- | --- |
| **A. BCN owns all** | One BCN team builds and runs | Single accountable team, closest to the domain | BCN takes on production run and on-call, which is a new duty |
| **B. NGSS owns all** | One NGSS team builds and runs | Run discipline likely stronger (assumption, unconfirmed) | Domain knowledge must be rebuilt in a new team |
| **C. Split by layer** | BCN owns product, data and agents (3, 4, 6). NGSS owns platform and run (5), and shares 1 and 2 | Matches where each team's strength looks to be | Two teams means an interface to govern, and the shared operational store is already an open ADR issue |

## Roll-off scenarios

Dates assume Industrialisation starts 23 Nov. "I-wk" is a week of Industrialisation. Nobody rolls off before the partner rollout has settled.

### Scenario 1: Hard stop at SOW end (fastest)

- **Wave 1, I-wk 6 (early Jan):** workstreams 1, 2, 6.
- **Wave 2, I-wk 9 (late Jan):** workstream 5.
- **Wave 3, I-wk 12 (mid Feb):** workstreams 3, 4.
- **Tail:** none.
- **Risk:** agents and data roll off with only about four weeks of shadowing. Bain would learn the highest-risk areas last and fastest. Not recommended unless the SOW cannot be extended.

### Scenario 2: Three waves with reverse shadowing (recommended)

Each workstream goes through three steps: SN leads with Bain shadowing, then Bain leads with SN shadowing, then SN is gone. Reverse shadowing is the step that proves the handover.

- **Wave 1, early Jan:** workstreams 1, 2, 6. Bain-led from I-wk 5.
- **Wave 2, early Feb:** workstream 5. Bain-led from I-wk 9, after the shared Postgres and role-name gaps are closed.
- **Wave 3, mid Feb:** workstreams 3, 4, with a named Bain agent owner in place.
- **Tail:** a four-week advisory retainer for agents and data, to mid Mar. A small, bounded SN presence, not full roles.
- **Risk:** needs a small SOW extension for the tail. The tail needs a hard end date or it becomes Scenario 3.

### Scenario 3: Capability-gated, six months

- SN roles roll off when a gate is met, not on a date. Example gate: Bain has shipped one release on its own with no P0 defect.
- Frontend and backend go first, platform second, agents and data last (around Q2 2027).
- **Risk:** cost and the Bain team never feeling ownership. Use this only if Bain cannot staff the receiving teams by February.

### Scenario 4: Split ownership with a platform-first handover

- Model C. Platform and run move to NGSS first, at I-wk 6, because the deployment tracker is well documented and Andromeda alignment is a natural NGSS task.
- BCN takes frontend, backend, data and QA in Wave 2 (early Feb). Agents follow in Wave 3 (mid Feb, with the Scenario 2 tail).
- **Risk:** the NGSS-BCN interface is new and must be written down first.

## Comparison

| | S1 Hard stop | S2 Reverse shadow | S3 Capability-gated | S4 Split, platform first |
| --- | --- | --- | --- | --- |
| SN fully off | ~15 Feb | ~15 Mar | ~Q2 2027 | ~15 Mar |
| Handover risk | High | Medium | Low | Medium |
| SOW change | None | Small extension | Large extension | Small extension |
| Bain staffing needed by | Dec | Dec for wave 1 | Feb | Dec (NGSS), Jan (BCN) |
| Fits ownership model | A or B | A, B or C | A, B or C | C |

**Recommendation:** Scenario 2, with Model C if NGSS can take the platform and run duties, and Model A if not. Scenario 4 is the same plan with the platform handed to NGSS first. Choose between them once NGSS capacity is known.

## Preconditions for any scenario

1. Name a Bain owner for the agents workstream before any SN agent engineer leaves. The narrative agent has no owner today.
2. Fill the four blank design pages before Wave 2. Roll-off is the natural deadline for them.
3. Close the three "Angel to confirm" items and move off the POC Foundry account before Bain takes over run.
4. Write the ownership rule for the shared operational store (OI3-27) before two teams share it.
5. Decide who is accountable for production incidents, and from what date.

## Inputs I need to firm this up

1. SN headcount by workstream, and the SOW's notice terms for partial roll-off.
2. What NGSS is, what it runs today, and its available capacity.
3. BCN capacity, and which BCN people could own data and agents.
4. Whether the Industrialisation SOW dates (23 Nov, ~12 weeks) still hold.
5. Whether the 50+ partner rollout date is fixed.

## Sign-off

This is a recommendation. The Tech Lead decides the scenario and the ownership model. Once decided, the ruling goes in `decisions/`.
