---
date: 2026-09-23
requester: "Sponsor / governance function (production approval gate, item owners: Sponsor & Technical Lead, Technical Lead, Engineering)"
subject: "Eight-item 'what we need from you' confirmation set gating production approval"
type: "design deviation"
recommendation: "blocked"
status: "awaiting sign-off"
---

# Request: Production approval confirmations (8 items)

## Asked for

A governance/approval gate has sent an 8-item confirmation list before it will approve
OI 3.0 / OC 3.0 for production. Item 1 (hosting, risk rating, data sensitivity) is marked
**blocks approval**; items 2–4 are owned by the Technical Lead, items 5–8 by Engineering.
This assesses what the mirror already answers versus what is a genuine, unresolved gap —
per CLAUDE.md, the latter goes to `context/open-questions.md` rather than being guessed
at here.

## Existing rulings, by item

**1. Hosting, risk rating, data sensitivity — blocks approval.**
Hosting is written down: [Technology Choices](../confluence/oi30/architecture/opportunity-indicator-architecture-high-level/technical-stack/technology-choices-19751338017.md)
is Azure-first throughout (Container Apps, Front Door, Azure SQL, AI Foundry), and is the
newer, controlling source over the technical-architecture diagram, which still shows
hosting as an undecided *Bedrock / Vertex / MS Foundry* choice (already tracked in
`context/open-questions.md` under "Hosting: resolved, but inconsistently"). No page
assigns a **risk rating**: [Security Design](../confluence/oi30/architecture/opportunity-indicator-architecture-high-level/security-design-processing-ai-and-data-19705167996.md)
is genuinely empty. **Sensitivity** is asserted in a meeting but not ratified on the page
meant to hold it: the
[VCC overview meeting](../confluence/oi30/meeting-summaries/vcc-overview-meeting-19696746551.md)
records "all Partner uploads are treated as red (confidential) data by default," while
the dedicated [Confidential data](../confluence/oi30/roadmap-business-requirements/confidential-data-19689340995.md)
page still reads only "To be decided how to treat it?"

**2. StatusNeo engineer access to Bain systems.**
[Onboarding — StatusNeo](../confluence/oi30/ways-of-working/onboarding-statusneo-19640975400.md)
lists Bain IT provisioning and a VRA/data-classification kick-off as Day-1/Week-1 items
with owners still "TBC." [Andromeda](../confluence/oi30/ways-of-working/onboarding-statusneo/andromeda-bains-agentic-ai-platform-19691733117.md)
confirms the split — StatusNeo owns application/agent logic, Bain owns DevOps/cloud
infra/CI/CD — but no page enumerates which Bain systems or data that access reaches.
`context/open-questions.md` already tracks the concrete blocker: the VDI-to-laptop
migration is incomplete, and access tickets OC3-2 and OC3-48 are still open into Sprint 2.
No access matrix exists anywhere in the mirror.

**3. Does the application learn from Partner input.**
Direct, unreconciled conflict. The VCC meeting rules it out for the data class that
covers all Partner uploads by default: red data must be "never exposed across Partners
and never used for model training." The technical-architecture diagram describes the
opposite for a later stage — an in-scope learning pipeline (SFT on golden cases, RLVR,
implicit RLHF from partner edits) writing to per-Partner LoRA adapters, gated by "no
training w/o opt-in" and "no cross-Partner flow." Neither Security Design nor NFR
(both empty) reconciles a blanket rule against an opt-in-gated pipeline.

**4. Is the MCP interface being published for other teams.**
Decided in principle: the VCC meeting states "OI 3.0 must expose its own MCP Server — it
will be a data provider to other Bain systems in future, not only a consumer," and
Technology Choices' north-star delta names a widening from "OI 3.0 only" to "other Bain
teams via the platform API and platinum layer" as "a new trust boundary." But the
governance checklist that would gate that exposure —
`AI_Architecture_Requirements_v2.1.xlsx`, rows TA-AI-MCP-01 through 08, attached to the
new [Architecture Assessment Tracker](../confluence/oi30/architecture/architecture-assessment-tracker-19853082681.md)
page — is unfilled. So: yes in principle, no completed review.

**5. WAF in front of the public address.**
Technology Choices §7 states it plainly: **Front Door Premium with WAF, Adopt** — an
Azure managed-service position. Whether that specific instance is Bain's shared,
centrally-run tenant or a project-provisioned one is not stated; Andromeda frames
centrally-run networking/TLS as an Andromeda capability but explicitly says OI 3.0 is
not on Andromeda yet, and StatusNeo instead provisions "from Bain's existing templates."

**6. Approved CI/CD tool, and access to Bain's internal search.**
[Deployment Design](../confluence/oi30/architecture/opportunity-indicator-architecture-high-level/deployment-design-ai-compute-data-components-cicd-19705233507.md)
is empty. The superseded Technical Stack page only says "Azure DevOps or equivalent."
This workspace's own `decisions/002-deployment-target-for-gls.md` recommends GitHub
Actions for the GLS deploy — a Tech Lead recommendation, not a Bain ruling — and the
Architecture Assessment Tracker's own reviewed tracker marks both tool and platform as
**"TOOL TBD" / "PLATFORM TBD"** as of 22 September, confirming Bain's own assessment
has this open too. Internal search: onboarding lists Glean API sandbox access as an
unconfirmed dependency (owner "KM owner TBC"); the VCC meeting's action item to confirm
with Glean/IRIS on data access was still open as of 4 August.

**7. Route to the AI models.**
Technology Choices §4 is authoritative: **API Management GenAI gateway, Adopt** — "every
model call passes the gateway, so changing a model is a configuration change and never a
code change," with model selection deliberately deferred to deployment. Andromeda names
a *different* component for the same job: "Model gateway — governed access, no data
leaving Bain" for running Claude Sonnet/Opus. The mirror never states whether these are
the same gateway under two names or two separate components.

**8. Three tools outside centrally-run platforms — monitoring, interim data store,
product analytics.**
The one item Technology Choices answers directly and completely: **Datadog** ("Alternative
APM, Buy, optional" — Azure Monitor/App Insights is the adopted central baseline),
**Pendo** ("Buy, existing" licence) for product analytics, and **Parquet** ("per-run
analytical files... in SharePoint" at MVP) as the interim data store. All three already
carry a recorded position in `tools/known_tools.json`. The only residual gap is that
Technology Choices itself is still "Draft for review," so no `decisions/` entry records
a Tech Lead sign-off on these three specifically.

## Assessment

Four items (5, 7, 8, and half of 6) are answerable today by citing Technology Choices —
routine, and citing the rubric is the correct response rather than raising a fresh
request. Four items (1, 2, 3, 4) and the CI/CD half of 6 rest on pages that are either
empty (Security Design, Deployment Design, NFR) or contain an unreconciled conflict
between an earlier meeting ruling and a later architecture diagram. Signing off on 1–4 as
"confirmed" without resolving those conflicts would be recording an answer the source
material does not actually give.

**Cost of yes (confirming 1–4 as-is):** treats a diagram detail (the learning pipeline,
the model-gateway split) as settled when it contradicts an explicit meeting ruling, and
records a risk rating and data classification that no one has actually signed.

**Cost of no (holding 1–4 open):** blocks production approval per item 1's own stated
status, and stalls confirmation of items the Technical Lead owns directly (2–4).

## Recommendation

**Split response.**

1. **Confirm now, citing Technology Choices directly:** items 5, 7 (with the caveat that
   "the gateway" needs a single canonical name — API Management GenAI gateway or
   Andromeda's model gateway, not both), and 8.
2. **Confirm partially, flag the rest:** item 6 — internal search and CI/CD platform are
   genuinely undecided (Bain's own Architecture Assessment Tracker says so), not just
   unmirrored.
3. **Cannot confirm without a ruling:** items 1, 2, 3, 4. Each needs a decision, not more
   research — the material gap is that Security Design, NFR, and Deployment Design have
   never been written, and one direct conflict (item 3, training) needs the meeting
   ruling and the architecture diagram reconciled before an answer can be given either
   way. Recommend escalating 1–4 to the architecture workshop rather than treating them
   as confirmable from what exists today.

New gaps and conflicts surfaced here that were not yet in `context/open-questions.md`
have been added there (see below) so they don't need re-discovering next time this comes
up.

## Sign-off

_Tech Lead decision and date — pending._
