# OC-TL — Tech Lead workspace for OI 3.0 / OC 3.0

**Naming.** The product is **Opportunity Catalyst**, and since late October the working
name in the space is **OpCat**. The architecture tree was renamed on 4 October and the
overview pages — Vision, High Level Requirements, Design requirements & components —
were rewritten in the week of 19 October to say *OpCat* wherever they said *OI 3.0*.
The space key is still `OI30` and the older architecture and data pages still say
Opportunity Indicator, so all three names are live. Repositories are
`nextgen-opportunity-catalyst-core` and `-ui`.

**The Jira board is `OI3`, and tickets are `OI3-nn`.** The Sprint 1 retrospective deck
calls it `OC3` and renumbers every ticket to `OC3-nn`, which is where an earlier version
of this file took its claim from — that was wrong. The same ticket appears in the Sprint 1
deck as `OC3-48` and in the Sprint 2 and 3 decks as `OI3-48`, all labelled "development
environment and access". Every other artefact uses `OI3`. Cite `OI3-nn`.

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
[Technology Choices](confluence/oi30/architecture/opportunity-catalyst-architecture-high-level/technical-stack/technology-choices-19751338017.md)
— prefer it over the older
[Technical Stack](confluence/oi30/architecture/opportunity-catalyst-architecture-high-level/technical-stack-19704512648.md)
page where they disagree.

Third-party and open-source positions are tracked in `tools/known_tools.json`; the daily
digest flags anything new or repositioned as needing a ruling, and separately flags
external model or data providers named in prose rather than in a position table.

Delivery runs in **two-week Scrum cycles**.

## Where things live

| Path | What it holds |
| ---- | ------------- |
| `confluence/` | Generated mirror of the OI30 space. **Read-only.** Start at `confluence/INDEX.md` |
| `context/` | Distilled, hand-maintained understanding: project brief, stakeholders, open questions, and `workshops/` notes |
| `videos/` | Recordings and transcripts handed over directly, not from Confluence. **Gitignored** |
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

**Keep `context/` current.** It is the distilled layer over the raw pages, and it only
stays useful if it is updated when the mirror changes materially. `tools/drift.py` is
what tells you it has slipped.

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

If the sync fails, it files an issue titled **"Confluence sync is failing"** assigned to
the repository owner, quoting the error, and comments on that same issue on subsequent
failures rather than opening a new one. A 401 or 403 in that notice means the
`CONFLUENCE_API_TOKEN` secret needs rotating — Atlassian API tokens expire, so this
recurs. Create a replacement at
<https://id.atlassian.com/manage-profile/security/api-tokens>.

Before the update is sent, `tools/drift.py` checks whether this distilled layer has
fallen behind the mirror: new pages not yet referenced in `context/`, page counts here
that no longer match, model providers named in prose with no recorded ruling, **named
services and model identifiers with no position in `tools/known_tools.json`**, pages
changed since the standing agenda's *Last full review* date, and pages filed outside the
OI3.0 tree that are not already recorded in `context/`. It is silent when there is
nothing to report, and its output appears in the briefing under **Knowledge base drift**.

The service check exists because `serpapi` reached the running peer-discovery backend and
was found by reading a page, not by any check — the provider list only knew model vendors,
and a search API is not one. When a service turns up with no recorded position, add its
name to `SERVICES` in `tools/drift.py`.

**Diagrams are scanned too.** Every other check reads prose, so a decision drawn rather
than written was invisible to all of them — the technical architecture SVG names a
**Claude SDK** orchestrator, against ADR-008's Microsoft Agent Framework, and no page says
so. The scan reads the text inside every SVG in the mirror and reports providers or
services with no recorded position.

**The scan finds staleness; it cannot fix it.** Clearing a drift finding means reading
the pages and updating `context/`, then moving the *Last full review against the mirror*
date in `context/standing-agenda.md`. That date is what the staleness check measures
against, so moving it without doing the reading disables the check.

The run fires at **06:07 Singapore** so the daily briefing is waiting by 07:00 even when
GitHub schedules it late. In UTC that is `22:07` on the *previous* calendar day, so run
timestamps in the Actions tab look a day behind; the briefing itself is dated in
Singapore time. The briefing leads with `context/standing-agenda.md` and is archived to
`context/daily/`.

### Known gaps in the source material

Of 98 pages, **76 carry text, 15 hold only an attachment or diagram, and 7 are genuinely
empty**. Deployment Design was filled on 7 October — the first of the five high-level
design pages to move. **Four still carry nothing**: Security Design, NFR Design Choices,
Observability, and Endpoints & Interfaces Design. Reviews touching those areas rest on
judgment, not
written policy — say so explicitly rather than presenting a standard that does not exist.

**A page that looks empty may not be.** Several carry their content as an attached
spreadsheet or deck rather than prose. Always check
`confluence/_attachments/<page_id>/` before calling a page undocumented.

**Attachments are readable without leaving the repo.** The mirror links them; these
read them:

| Command | Covers |
| ------- | ------ |
| `python3 tools/attachment_text.py --list` | What is readable, by type |
| `python3 tools/attachment_text.py <file>` | pptx, xlsx, xlsm, docx, html, csv |
| `python3 tools/diagram_text.py` | Refreshes the SVG text extracts in `context/diagrams/` |
| `python3 tools/video_frames.py --list` | The 13 mirrored recordings plus anything in `videos/`, with durations |
| `python3 tools/video_frames.py <file.mp4>` | Scene-change frames into `context/video-frames/` |
| `python3 tools/video_frames.py <file.mp4> --at 04:40,1:31:58` | Full-resolution frames at given times |
| `python3 tools/transcript_text.py <file.vtt>` | A Teams transcript as one timestamped line per utterance |

The sprint retrospectives are decks, the ARC assessment is two workbooks, and the GLS
output sample is an HTML file — none of that is in prose anywhere. Raster diagrams (PNG)
need a model that can see them; `context/diagrams/README.md` ranks the ones worth a pass
and says which to skip. PDF attachments cannot be read here at all.

**The recordings are planning sessions, not demos.** All 13 `.mp4` files are the Sprint 3
and Sprint 4 planning meetings, about three hours with no written summary. There is **no
recording of the product or the GLS demo** anywhere in the space. There is also no
speech-to-text here, so the tool takes the shared screen instead: `video_frames.py`
extracts scene-change frames, which is where the Sprint 4 backlog and its acceptance
criteria turned out to be. It needs ffmpeg — `pip install imageio-ffmpeg` — which nothing
else in `tools/` requires and the daily sync never runs. Extracted frames are gitignored
because they are regenerable and large; put what you learn in `context/` instead.

**Workshops arrive outside the space, with transcripts.** From Sprint 5, SN runs a workshop
series, and the recordings are handed over directly, as an `.mp4` plus a Teams `.vtt`, into
`videos/`. That folder is **gitignored**: the files are over GitHub's size limit, and they are
meeting recordings rather than OI30 pages. Read the transcript with `transcript_text.py` first
— it is auto-captioned with no speaker labels, so names come out garbled — then fetch the
screen with `video_frames.py --at` at the moments the speech points to. Scene detection alone
missed most of the code walkthrough in the first workshop. Distil each workshop into
`context/workshops/`; the first, on system and data architecture (28 October), is there and
is the most detailed account of the as-built system anywhere in this repo.

**Unlike scene frames, a workshop's cited frames are committed**, in
`context/video-frames/<date>-workshop/`, full resolution as JPEG and named `HHMMSS-what.jpg`,
with each one linked from the notes. Check every frame before adding it. Leave out anything
showing secrets, and anything that only shows identifiers (tenant, client or app IDs,
internal hostnames) — record what such a frame teaches as text instead.

Treat a genuinely empty page as **unknown, not as "no requirement"**, and flag it when a
decision depends on one. The full breakdown is in
[context/open-questions.md](context/open-questions.md).

### Permissions

The mirror flattens Confluence's page-level permissions into repo access. Keep scope to
`OI30` and do not widen it without checking first.

**Pages sometimes carry credentials, and the mirror copies them.** The
[User Interviews](confluence/oi30/user-interviews-19883524168.md) page lists Zoom
recording passcodes in plain text beside each partner interview, so they are now in git
history. Nothing here can redact a page — the fix is on the Confluence side. When a page
like this appears, raise it rather than quietly mirroring it, and never repeat a
credential into `context/`, a review, or a briefing.
