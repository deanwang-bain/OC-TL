# OC-TL — Tech Lead workspace for OI 3.0

## What this project is for

This repository automates as much of the **Tech Lead role on Opportunity Indicator 3.0
(OI 3.0)** as possible. The Tech Lead is Dean Wang; Bain is the client-side owner and
**StatusNeo (SN)** is the delivery partner writing the application code.

This is a **decision and review workspace, not the product codebase.** Nothing here
ships to users. The work is reviewing what SN builds, ruling on technical requests,
keeping architecture decisions coherent, and turning the OI 3.0 documentation into
answers.

## Role boundaries — read before acting

**Never write application code for OI 3.0, and never commit to the OI 3.0 codebase.**
That is SN's job. Do not open pull requests against their repositories, push branches
there, or hand over patches framed as ready-to-merge work.

What to do instead:

| Task | How to handle it |
| ---- | ---------------- |
| Reviewing SN's code | Review it. Findings, severity, rationale — see `checklists/code-review.md` |
| Illustrating a fix | A short snippet inside a review comment is fine. It is an illustration, not a deliverable |
| A technical request (access, infra, library, design deviation) | Assess it and write a recommendation — see `requests/` |
| An architecture question | Answer from `confluence/`, citing pages. Record new rulings in `decisions/` |
| Tooling for *this* workspace | Fair game. `tools/` is ours to build |

**Recommend, don't unilaterally approve.** Produce decision-ready recommendations with
a clear recommended outcome and the reasoning behind it; the Tech Lead signs off. This
mirrors OI 3.0's own stated principle — *"AI as enabler, not decision-maker"* — from
[Vision](confluence/oi30/overview/vision-19617939629.md). Where a request is routine and
falls inside an existing written rule, say so plainly and note which rule applies.

## What OI 3.0 is

An AI-powered tool that helps Bain partners prepare for client conversations. It
automates the research, benchmarking, and deck creation that today takes a team of COEs
and consultants 2–3 days, targeting **roughly 30 minutes** end to end.

Key characteristics that shape technical decisions:

- **Partner retains judgment; agents do synthesis.** Hard gates block on critical
  missing input; soft gates proceed but flag lower confidence.
- **Transparency is a requirement, not a feature.** Any number must be drillable to its
  source, reasoning, and confidence level. This constrains how data flows are built.
- **Non-linear and modular.** Adjusting peers or context mid-analysis reruns only the
  affected modules — a real architectural constraint, not a UX preference.
- **Primary persona:** "the accountable partner", who owns what goes in front of a
  client.

Stack is a cloud-native headless architecture on **Azure**: React / TypeScript / Vite
frontend, FastAPI for deterministic REST and FastMCP for agent-driven access, with
business rules and calculations deliberately kept out of the client. The authoritative
and most decision-dense source is
[Technology Choices](confluence/oi30/architecture/opportunity-indicator-architecture-high-level/technical-stack/technology-choices-19751338017.md)
— prefer it over the older
[Technical Stack](confluence/oi30/architecture/opportunity-indicator-architecture-high-level/technical-stack-19704512648.md)
page where they disagree.

For **endpoint-level** detail on Target Setup and Peer Selection — public routes,
component swimlanes, payload contracts, journey invariants, and the tracked blocker
register — use [context/journey-portal.md](context/journey-portal.md). It distils an
artifact received outside Confluence, so its workbook citations are reported but not
verifiable from the mirror; say so when relying on them.

Third-party and open-source positions are tracked in `tools/known_tools.json`; the daily
digest flags anything new or repositioned as needing a ruling.

Delivery runs in **two-week Scrum cycles**.

## Where things live

| Path | What it holds |
| ---- | ------------- |
| `confluence/` | Generated mirror of the OI30 space. **Read-only.** Start at `confluence/INDEX.md` |
| `context/` | Distilled, hand-maintained understanding: project brief, stakeholders, open questions |
| `context/artifacts/` | Source documents received outside Confluence, kept so distilled claims stay traceable. Not synced — see its `README.md` |
| `reviews/` | Code review records, one file per review |
| `requests/` | Technical requests and their recommendations, plus `REGISTER.md` |
| `decisions/` | Tech Lead decision log for rulings made here, distinct from Confluence ADRs |
| `checklists/` | Standards applied during reviews and triage |
| `tools/` | Workspace tooling, including the Confluence sync |

## Working method

**Ground every technical claim in a source.** Cite the Confluence page (with its link)
or the code under review. When the documentation does not answer a question, say so and
add it to `context/open-questions.md` rather than filling the gap with a plausible
guess — several architecture pages are still empty (see below).

**Prefer the mirror over the connector.** `confluence/` is greppable, always available,
and works when the Atlassian connector does not. Read `confluence/INDEX.md` first.

**Keep `context/` current.** It is the distilled layer over 71 raw pages, and it only
stays useful if it is updated when the mirror changes materially.

## The Confluence mirror

| Space | Site | URL |
| ----- | ---- | --- |
| `OI30` | `bainco.atlassian.net` | https://bainco.atlassian.net/wiki/spaces/OI30/ |

`OI30` is the only space in scope. Do not treat other spaces as project context without
asking.

Each page mirrors to one markdown file matching the Confluence tree, carrying front
matter with `confluence_id`, `confluence_url`, and `version` so any claim is traceable.
Page attachments — architecture diagrams especially — download to
`confluence/_attachments/<page_id>/` and are linked inline, so diagrams can be opened
and read directly.

**Never edit files under `confluence/` by hand.** The next sync overwrites them. Change
the page in Confluence instead.

Refresh runs daily via `.github/workflows/confluence-sync.yml`, or on demand from the
Actions tab. It needs the repository secrets `CONFLUENCE_EMAIL` and
`CONFLUENCE_API_TOKEN`.

The run fires at **06:07 Singapore** so the daily briefing is waiting by 07:00 even when
GitHub schedules it late. In UTC that is `22:07` on the *previous* calendar day, so run
timestamps in the Actions tab look a day behind; the briefing itself is dated in
Singapore time. The briefing leads with `context/standing-agenda.md` and is archived to
`context/daily/`.

### Known gaps in the source material

Of 71 pages, **54 carry text, 7 hold only an attachment or diagram, and 10 are genuinely
empty**. The empty set still includes every high-level design page this role reviews
against: Security Design, NFR Design Choices, Observability, Endpoints & Interfaces
Design, and Deployment Design (CI/CD). Reviews touching those areas rest on judgment, not
written policy — say so explicitly rather than presenting a standard that does not exist.

**A page that looks empty may not be.** Several carry their content as an attached
spreadsheet or deck rather than prose. Always check
`confluence/_attachments/<page_id>/` before calling a page undocumented.

Treat a genuinely empty page as **unknown, not as "no requirement"**, and flag it when a
decision depends on one. The full breakdown is in
[context/open-questions.md](context/open-questions.md).

### Permissions

The mirror flattens Confluence's page-level permissions into repo access. Keep scope to
`OI30` and do not widen it without checking first.
