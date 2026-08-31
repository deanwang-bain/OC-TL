# Open questions

Questions the OI 3.0 documentation does not currently answer. Add to this file rather
than guessing; remove an entry when the mirror answers it.

Each entry: what is unknown, why it matters, who can answer, and what is blocked.

## Undocumented architecture areas

Of 71 pages, **53 carry text, 5 are diagrams only, and 13 are genuinely empty.** The
distinction matters: a diagram-only page is documented, just not in prose, while an
empty page means the decision has not been written down anywhere.

### Written nowhere — no text, no diagram

**These are the material gaps.** Every one of the high-level design pages the Tech Lead
reviews against is blank. Reviews in these areas rest on judgment, not policy.

| Area | Why it matters | Blocks |
| ---- | -------------- | ------ |
| [Security Design](../confluence/oi30/architecture/opportunity-indicator-architecture-high-level/security-design-processing-ai-and-data-19705167996.md) | No written control set for processing, AI, or data | Security review of any SN PR touching auth or data handling |
| [NFR Design Choices](../confluence/oi30/architecture/opportunity-indicator-architecture-high-level/nfr-non-functional-design-choices-19704905798.md) | No performance, availability, or scale targets | Judging whether an implementation meets the 30-minute end-to-end goal |
| [Observability & Monitoring](../confluence/oi30/architecture/opportunity-indicator-architecture-high-level/observability-logging-notification-monitoring-design-19705430028.md) | No logging or alerting standard | Reviewing instrumentation in SN code |
| [Endpoints & Interfaces Design](../confluence/oi30/architecture/opportunity-indicator-architecture-high-level/endpoints-interfaces-design-19704938600.md) | No API contract standard | Reviewing FastAPI surface changes |
| [Deployment Design (CI/CD)](../confluence/oi30/architecture/opportunity-indicator-architecture-high-level/deployment-design-ai-compute-data-components-cicd-19705233507.md) | No documented pipeline or environment topology | Release and rollback decisions |
| [Bain Taxonomy Mapping](../confluence/oi30/data-requirements/bain-taxonomy-mapping-19619577930.md) | Mapping undefined | Reconciling upstream data to Bain taxonomy |
| [LSEG](../confluence/oi30/data-requirements/data-sources-summary/lseg-19618889872.md) | Integration undocumented, unlike its sibling sources | LSEG integration review |
| [GLS Feature Set](../confluence/oi30/gls-feature-set-19761725586.md) | Scope undefined | Feature planning |
| [Sprint 1 stories, dependencies and decisions](../confluence/oi30/mvp-sprint-map/sprint-1-stories-dependencies-and-decisions-19763003424.md) | Sprint 1 scope not captured where the team can see it | Sprint execution |
| [Jobs to be done](../confluence/oi30/overview/jobs-to-be-done-19619577898.md) | Feature trade-offs lack a stated yardstick | Prioritisation calls |

Three further empty pages — [Architecture](../confluence/oi30/architecture-19589234692.md),
[Overview](../confluence/oi30/overview-19618758834.md), and
[Roadmap / Business Requirements](../confluence/oi30/roadmap-business-requirements-19588546617.md)
— are parents whose children hold the content. Those are structural, not gaps.

### Documented as diagrams only

Content exists but carries no prose, so it is not greppable. Open the linked image.

- [Technical Architecture](../confluence/oi30/architecture/technical-architecture-19619479668.md)
- [Data Architecture](../confluence/oi30/architecture/data-architecture-19619840013.md)
- [Logic Architecture](../confluence/oi30/architecture/logic-architecture-19619840005.md)
- [Success metrics](../confluence/oi30/overview/success-metrics-19618758856.md)
- [Onboarding tracker](../confluence/oi30/ways-of-working/onboarding-statusneo/onboarding-tracker-19705593880.md)

A diagram cannot state a threshold or a rule precisely. Where one of these is the sole
source for a decision, confirm the reading before relying on it.

## Conflicts to resolve

| Conflict | Detail |
| -------- | ------ |
| ~~Two different architectures~~ | **Resolved.** Architecture Layers documents two deliberate consumption patterns over one headless layer: deterministic via FastAPI, open-ended via FastMCP/MCP. The React app and the agent swarm are both clients, not rival designs |
| **Two different AI SDKs** | Technical Stack names **AI SDK (ai-sdk.dev)**; the technical architecture diagram names the **Claude SDK**. Both cannot be the orchestrator |
| **Hosting: resolved, but inconsistently** | Technology Choices sets an Azure-first rubric with Azure Front Door; the technical architecture diagram still lists Bedrock / Vertex / MS Foundry. The page is newer and more specific — the diagram should be corrected |
| **Security split exists only in a diagram** | The app-level (StatusNeo) vs infra-level (Bain) RACI is drawn in the technical architecture SVG but written on no page, including the empty Security Design page |

## Product and scope

| Question | Why it matters |
| -------- | -------------- |
| MVP is still "to be signed off" | Scope may move under active development |
| Three per-screen data requirement pages are marked *update in progress* | Case for Change, Analysis, and Output & Deck Builder specs are unstable |
| ADR-001 to ADR-009 are "Accepted, pending Bain architect review" | Rulings may still change under review |
