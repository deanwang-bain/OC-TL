# Open questions

Questions the OI 3.0 documentation does not currently answer. Add to this file rather
than guessing; remove an entry when the mirror answers it.

Each entry: what is unknown, why it matters, who can answer, and what is blocked.

## Undocumented architecture areas

These pages exist in Confluence but have no body text as of the first sync. Each is a
gap the Tech Lead role depends on.

| Area | Why it matters | Blocks |
| ---- | -------------- | ------ |
| [Security Design](../confluence/oi30/architecture/opportunity-indicator-architecture-high-level/security-design-processing-ai-and-data-19705167996.md) | No written control set for processing, AI, or data | Security review of any SN PR touching auth or data handling |
| [NFR Design Choices](../confluence/oi30/architecture/opportunity-indicator-architecture-high-level/nfr-non-functional-design-choices-19704905798.md) | No performance, availability, or scale targets | Judging whether an implementation meets the 30-minute end-to-end goal |
| [Observability & Monitoring](../confluence/oi30/architecture/opportunity-indicator-architecture-high-level/observability-logging-notification-monitoring-design-19705430028.md) | No logging or alerting standard | Reviewing instrumentation in SN code |
| [Endpoints & Interfaces Design](../confluence/oi30/architecture/opportunity-indicator-architecture-high-level/endpoints-interfaces-design-19704938600.md) | No API contract standard | Reviewing FastAPI surface changes |
| [Deployment Design (CI/CD)](../confluence/oi30/architecture/opportunity-indicator-architecture-high-level/deployment-design-ai-compute-data-components-cicd-19705233507.md) | No documented pipeline or environment topology | Release and rollback decisions |
| [Technical Architecture](../confluence/oi30/architecture/technical-architecture-19619479668.md) | Empty | General grounding |
| [Data Architecture](../confluence/oi30/architecture/data-architecture-19619840013.md) | Empty | Data-layer review |
| [Logic Architecture](../confluence/oi30/architecture/logic-architecture-19619840005.md) | Empty | Calculation-layer review |

Some of these may hold diagrams rather than text. Attachments now download to
`confluence/_attachments/`, so re-check after the next sync before treating one as
genuinely unwritten.

## Product and scope

| Question | Why it matters |
| -------- | -------------- |
| [Success metrics](../confluence/oi30/overview/success-metrics-19618758856.md) is empty | No agreed definition of done for the MVP |
| [Jobs to be done](../confluence/oi30/overview/jobs-to-be-done-19619577898.md) is empty | Feature trade-offs lack a stated yardstick |
| [Sprint 1 stories, dependencies and decisions](../confluence/oi30/mvp-sprint-map/sprint-1-stories-dependencies-and-decisions-19763003424.md) is empty | Sprint 1 scope not captured where the team can see it |
| MVP is still "to be signed off" | Scope may move under active development |
