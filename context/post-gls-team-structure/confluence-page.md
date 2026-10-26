# Post-GLS team structure: moving OpCat ownership to Bain

**Status:** Proposal for decision · **Owner:** Dean Wang (Tech Lead) · **Date:** 26 October 2026

## Summary

After GLS, ownership of Opportunity Catalyst moves from StatusNeo to a Bain internal team, BCN or NGSS, and StatusNeo rolls off in waves. This page sets out three ownership models, four roll-off scenarios, and an org chart for each.

**Recommendation:**

- **How ownership ends up:** Option C. NGSS owns engineering and run. BCN owns data, the golden data set and content.
- **How StatusNeo rolls off:** Scenario 2, three waves with reverse shadowing. StatusNeo is fully off by mid-March 2027.
- **Fallback:** if NGSS cannot take production engineering, use Option A, with BCN owning everything.

**Decisions needed:**

1. Which ownership model: A, B or C.
2. Which roll-off scenario: 1, 2, 3 or 4.
3. Approval to go ahead with the Lead Engineer / Platform Owner hire. Every option depends on this role.

## Context

| Fact | Source |
| --- | --- |
| GLS was 26 Oct. Sprint 5, Support and Hardening, runs 26 Oct to 6 Nov | [Sprint 3 Retrospective](https://bainco.atlassian.net/wiki/spaces/OI30/pages/19933790220), stakeholder deck |
| Industrialisation runs from about 23 Nov 2026 for about 12 weeks, to about 15 Feb 2027, under a separate SOW | [Onboarding - StatusNeo](https://bainco.atlassian.net/wiki/spaces/OI30/pages/19640975400) |
| The 50+ partner rollout is late November or early December | [OC Dev-Staging (GLS) Deployment Tracker](https://bainco.atlassian.net/wiki/spaces/OI30/pages/19909279789) |
| The data pipeline is Bain-led (Sandeep, Siva). StatusNeo leads the AI agent layer | [VCC overview meeting](https://bainco.atlassian.net/wiki/spaces/OI30/pages/19696746551) |
| The golden data set was curated with BCN | [Sprint 3 Retrospective](https://bainco.atlassian.net/wiki/spaces/OI30/pages/19933790220) |
| "DevOps, cloud infrastructure, and CI/CD pipelines are Bain-owned" | [Andromeda](https://bainco.atlassian.net/wiki/spaces/OI30/pages/19691733117) |
| "No data engineer was onboarded for the GLS sprints" | [Sprint 3 Retrospective](https://bainco.atlassian.net/wiki/spaces/OI30/pages/19933790220) |

### What has to carry over

The Tech Lead's September run-model proposal, not yet published, recommended one accountable Bain owner backed by a StatusNeo run team. It rejected an all-Bain team because the working knowledge of the calculation engine, the expression grammar and the agents sits with the people who wrote them.

This page keeps the accountable Bain owner, the support tiers and the change classes from that proposal. It replaces the StatusNeo run team with BCN and/or NGSS. **Reverse shadowing is how that knowledge transfer gets paid for**, and it is why the recommended scenario is not the fastest one.

The run proposal estimates the steady-state run effort at **about 5.3 to 5.8 FTE-equivalent**, of which 1.0 is new Bain headcount. The other 4.3 to 4.8 is pod capacity, fractional time and existing Bain services. The estimate is pending an availability target. Building the nine [post-GLS initiatives](https://bainco.atlassian.net/wiki/spaces/OI30/pages/19800162379) comes on top of it, and its size depends on what is funded.

## Workstreams and handover risk

| Workstream | Held today by | Handover risk | Why |
| --- | --- | --- | --- |
| Frontend and BFF | StatusNeo | Low to medium | Contract and boundary tests landed in Sprint 3 |
| Backend services | StatusNeo | Medium | Services tested in Sprint 3 |
| Calculation engine, expression grammar, definition registry | StatusNeo | High | Custom-built, and the base of every defensible figure |
| Agents: peer selection, narrative, chat | StatusNeo | Highest | Specialist work, model positions not yet recorded |
| Data pipeline and integrations | Bain, with BCN | Medium | Already Bain-led, but there is no data engineer and live sources are not connected yet |
| Infra, CI/CD, Terraform | Built by StatusNeo on Bain templates | Medium | Bain-owned by rule, and well documented in the deployment tracker |
| QA, eval harness, golden data set | StatusNeo QA, BCN | Medium | Bain analysts are already required for the golden data set |
| Security and governance (OI3-21) | Tech Lead review | Unknown | The Security, NFR, Observability and Endpoints design pages are still blank |

The rule for ordering: roll off first where tests and documents protect the code, and last where the knowledge is still in people's heads.

## Org charts

Boxes are roles, not named people, except where a person is already named in this space. Figures are FTE-equivalent run estimates. Solid lines are reporting lines. Dashed lines show a team drawing on or coordinating with another.

### Today

**[Diagram: 01-today.drawio.svg]**

Bain holds product, architecture and the data pipeline. StatusNeo builds the application, the calculation engine, the agents and the infrastructure code.

### Option A: BCN owns build and run

**[Diagram: 02-option-a-bcn.drawio.svg]**

- **For:** one accountable team, closest to the domain. BCN already co-owns the golden data set.
- **Against:** BCN takes on production engineering, L2 run and incident duty. Nothing in this space shows BCN doing those today, and agent engineering is furthest from its current work.
- **Choose if:** NGSS has no capacity, or keeping a single team matters most.

### Option B: NGSS owns build and run

**[Diagram: 03-option-b-ngss.drawio.svg]**

- **For:** one engineering team, and probably the stronger run discipline. That second point is to be confirmed with NGSS.
- **Against:** domain knowledge has to be rebuilt. BCN stays involved for the golden data set anyway, so in practice this is two teams, one of them informal.
- **Choose if:** NGSS has capacity and BCN cannot commit analysts.

### Option C: NGSS engineers, BCN owns data and content (recommended)

**[Diagram: 04-option-c-split.drawio.svg]**

- **For:** each team does what it already does. BCN keeps the domain, the golden data set, content changes and data changes. NGSS takes the code, releases and incidents. The data pipeline stays on the Bain side, where it already sits.
- **Against:** two teams means an interface to govern. A data repair that needs a code change crosses both teams, and the Lead Engineer is what holds them together.

### Transition state in mid-January (Scenario 2 on Option C)

**[Diagram: 05-transition-mid-january.drawio.svg]**

Lower-risk work is Bain-led with StatusNeo shadowing. The calculation engine and agents are still StatusNeo-led with Bain shadowing. Infrastructure is handing over to TSG.

## Roll-off scenarios

Every scenario starts with **Wave 0, from now to 23 Nov**:

- Name the receiving teams.
- Start the Lead Engineer hire.
- Put Bain shadows into Sprint 5.

Nobody rolls off before the 50+ partner rollout has settled. Late December is treated as about two lost weeks.

**[Diagram: 06-roll-off-timeline.drawio.svg]**

| | Scenario 1: Hard stop | Scenario 2: Reverse shadow (recommended) | Scenario 3: Capability-gated | Scenario 4: Platform first |
| --- | --- | --- | --- | --- |
| How it works | Three waves, all inside the SOW: frontend and QA, then backend and infra, then calc engine and agents | StatusNeo leads, then Bain leads with StatusNeo shadowing, then StatusNeo leaves. Calc engine and agents go last, followed by a four-week advisory tail | Roles roll off when gates are met, not on dates | Infra goes to TSG in December, then the rest by team, with the Scenario 2 tail |
| StatusNeo fully off | ~15 Feb 2027 | ~15 Mar 2027 | ~Q2 2027 | ~15 Mar 2027 |
| Handover risk | High | Medium | Low | Medium |
| SOW change | None | Small extension for the tail | Large extension | Small extension |
| Bain staffing needed by | December | December for the Lead Engineer, January for the pod | February | December for TSG, January for the pod |
| Works with | A, B, C | A, B, C | A, B, C | C only |

**Scenario 2 waves:**

| Wave | Bain leads from | StatusNeo off | Workstreams |
| --- | --- | --- | --- |
| 1 | Early January | Mid January | Frontend and BFF, QA, content changes |
| 2 | Mid January | Early February | Backend services, infra to TSG, L2 run |
| 3 | Early February | ~15 February | Calculation engine, agents |
| Tail | — | ~15 March | Advisory hours for the calculation engine and agents only, with a hard end date |

The data pipeline is not a wave because it is already Bain-led. The data engineer StatusNeo never onboarded should be hired by Bain directly.

**Scenario 3 gates:**

- Bain ships a monthly release alone with no P0 defect.
- A Bain engineer who did not write the calculation engine makes a change to it.
- A model version change passes regression without StatusNeo.

## Preconditions for any scenario

1. **Hire the Lead Engineer / Platform Owner before Wave 1.** If the hire is not in seat by early January, every scenario becomes Scenario 3.
2. Name a Bain owner for the calculation engine and for the agents before any StatusNeo engineer on them leaves.
3. Fill the Security, NFR, Observability, and Endpoints & Interfaces design pages before Wave 2. A Bain team cannot run to a standard that has not been written.
4. Close the open staging confirmations in the deployment tracker, and move off the POC Foundry account before infra goes to TSG.
5. Record positions on the web search provider and the models in use before the agents move.

## Open inputs

| Input | Needed from | Decides |
| --- | --- | --- |
| NGSS capacity from January, and what it runs today | NGSS lead | A or B or C |
| BCN capacity, and willingness to take L2 run | BCN lead | A or C |
| StatusNeo headcount by workstream, and SOW notice terms for partial roll-off | Programme and procurement | Wave sizing, tail cost |
| Lead Engineer hire status | Tech Lead, HR | Whether Scenario 2 is achievable |
| Whether the Industrialisation and partner rollout dates hold | Product Manager | All dates above |

## Editing the diagrams

Each diagram is a `.drawio.svg` file attached to this page. It displays as an image and opens for editing in draw.io: choose **Edit** on the draw.io macro, or open the attachment at [app.diagrams.net](https://app.diagrams.net), edit it, and re-attach it under the same name.
