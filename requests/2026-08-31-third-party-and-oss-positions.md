---
date: 2026-08-31
requester: StatusNeo (implied by Technology Choices, draft for review)
subject: "Third-party and open-source positions declared in Technology Choices"
type: library
recommendation: approve with conditions
status: awaiting sign-off
---

# Request: Third-party and open-source positions declared in Technology Choices

## Asked for

[Technology Choices](https://bainco.atlassian.net/wiki/spaces/OI30/pages/19751338017)
declares a full technology position set for OI 3.0 and is marked **Draft for review**.
Sixty-six entries carry a Build / Adopt / Buy position. This assesses the subset that
commits Bain to someone else's code or licence terms.

No separate request has been raised for any of these. They arrive as a documented set,
which is the right way round — but the set has not been ruled on.

## Existing rulings

The governing rubric on the page itself: **Azure managed services first, custom build
only where genuinely warranted**, with each choice tested for fit, rubric, reversibility
and operability. Nothing in `decisions/` covers these yet. ADR-001 to ADR-009 are
themselves "Accepted, pending Bain architect review".

## Assessment

### Routine — mainstream permissive licences, inside the rubric

TanStack Query, Zustand, Radix, i18next, Vega-Lite, DuckDB, Parquet, OpenTelemetry.

All widely adopted, permissively licensed, low reversibility cost. DuckDB is embedded
in-process and the page's own note is fair — this was never a real question. **Recommend
approve as a block.**

### Needs a specific answer before approval

| Item | Position | The question |
| ---- | -------- | ------------ |
| **Zvec** | Adopt OSS | Obscure relative to everything else in the set. Needs licence, maintainer and release-cadence confirmation. It is described as a run-scoped in-memory cache, so blast radius is small and it is genuinely replaceable — but it is the one dependency here nobody will recognise |
| **Apache ECharts** | Build on OSS | **The same page rejects it.** §2.1 lists "Rejected: Recharts, ECharts, Chart.js" because they force an exhibit to be a rendering rather than a specification, which would break the format-neutral content model under ADR-006. Yet the frontend table lists "Vega-Lite, Apache ECharts". One of these is wrong |
| **CopilotKit** | Buy, licence | Recorded as a licence purchase, but CopilotKit is open-core. Which tier is intended, and is the licence budgeted and bought? Reversibility is poor — it shapes the assistant surface |
| **AG-Grid Enterprise** | Buy, existing Bain licence | Approval rests entirely on "existing". Confirm the existing licence covers this application, this deployment model and this seat count before treating it as free |
| **dbt** | Build on OSS | North star only, so not urgent. Confirm dbt Core rather than a commercial tier when it becomes live |
| **Datadog** | Buy, optional | "Optional" means undecided. Azure Monitor with Application Insights is already Adopted for the same concern. Duplicate observability spend unless there is a stated reason |
| **Headless Chromium** | Build | The renderer is named but the driver is not (Playwright, Puppeteer, or direct CDP). Licensing is unproblematic; the omission is a gap in the record rather than a risk |

### Cost of yes

Twenty-four of twenty-seven components are Build, which the page itself concedes
"flatters the custom build". Five are argued as genuinely differentiated: calculation
engine, definition registry, evidence and provenance service, composition and template
engine, external source rate limiting. Those arguments hold — each names what a managed
option fails to do.

### Cost of no

Blocking the whole set stalls Sprint 1. The routine block should not wait on the seven
specific questions.

## Recommendation

**Approve with conditions**, in two parts:

1. **Approve the mainstream permissive set now** so implementation is unblocked.
2. **Hold the seven items above** pending answers. Only two carry real risk —
   **Zvec** (unknown provenance) and **CopilotKit** (licence tier and cost, poor
   reversibility). ECharts is a documentation contradiction rather than a technology
   risk, but it must be resolved because it decides whether an Exhibit is a
   specification or a rendering, and ADR-006 depends on the answer.

Ask StatusNeo to add a licence column to the table. The page tests every choice for fit,
rubric, reversibility and operability but never records the licence — which is the one
thing a third-party approval actually turns on.

## Sign-off

_Tech Lead decision and date — pending._
