# Diagrams in the OI30 mirror

Several OI 3.0 decisions exist only as a box on a diagram. The technical
architecture SVG names a **Claude SDK** orchestrator, which no Confluence page
states in prose and which sits against ADR-008's choice of Microsoft Agent
Framework. Every drift check reads markdown, so anything drawn rather than
written was invisible to all of them until this directory existed.

Two kinds of diagram, two ways in.

## SVG — extracted automatically, already here

```
python3 tools/diagram_text.py            # refresh the .txt files in this directory
python3 tools/diagram_text.py --check    # report what is missing, write nothing
python3 tools/diagram_text.py <file.svg> # print one
```

An SVG is XML, so its labels are plain text. The mirror holds **36 SVGs that are
only 13 distinct diagrams** — the two "to be delete" drafts carry full copies of
the Future Scope and Present Working sets under export filenames. The extractor
keeps the best-named copy and skips the rest.

`tools/drift.py` now scans these for providers and services with no recorded
position, so the next Claude-SDK-shaped surprise surfaces in the daily briefing
rather than in a reading pass months later.

**Layout and arrows are lost.** The text tells you what the boxes say, not what
points at what. Open the SVG when the relationships matter.

## PNG — needs a reading pass, one at a time

57 PNGs, and most are not worth it. The Read tool renders an image directly, so
the cost is one call and a large context hit per diagram. Work down this list
rather than across the directory.

### Tier 1 — read these

| Page | File | Why |
| ---- | ---- | --- |
| Chat Assistant Architecture | `19899809824/image-20261004-114142.png` | **The densest artefact in the space.** Carries a "Dev today" box of temporary deviations and a "Not deployed yet" list that appear on no page: Redis as a container-app stopgap against a managed target, Service Bus Standard with no private endpoint, NAT gateway instead of Azure Firewall for egress, and Stream B not deployed end to end. Also states agents reach models "through the project's OpenAI endpoint" |
| OC Dev-Staging Deployment Tracker | `19909279789/image-20261007-144216.png` | Target state for the GLS staging environment |
| Deployment Design | `19705233507/image-20261007-144130.png`, `-20261004-062709.png`, `-20261004-062849.png` | Three tabs — Dev Environments, Target, Revised Dev-Staging (GLS). The page is images only; this *is* the deployment design |
| Document Upload & Parsing | `19899351139/image-20261004-053747.png`, `-053922.png` | The two ingestion options: Foundry-hosted embedding (authoritative) versus self-hosted in a Container App |
| Opportunity-Catalyst Architecture | `19705397258/image-20260807-101304.png`, `-101334.png` | The high-level view the ADRs are reviewed against |
| Logical Application Flows | `19705135241/image-20260807-102546.png` | Only source for the end-to-end flow |

### Tier 2 — read when the topic comes up

| Page | Files | Why |
| ---- | ----- | --- |
| Peer Selection Capability | 7 PNGs, ~16 MB total | Heaviest set in the mirror, but the same subject is covered in prose on *Present working — Technical details* and in its six SVGs, which are already extracted here. Read only for what the prose omits |
| Cost Bar & Normalization | `19888046107/image-20261001-055744.png` | The methodology page is prose-rich; the diagram is supporting |
| OpCat Process overview | `19688849601/image-20260804-201432.png` | Process flow |
| Agent Validation Test Plan | `19765133323/att_0_for_19765133323.png` | Relevant to the unresolved gRPC-versus-REST question |
| Data Dictionary, MVP Sprint Map, Data sources from Current OC | one each | Reference tables as images |

### Skip

- **Screen mockups** (Screens 00–05, ~20 PNGs). Superseded: the October prototype
  page states *"The Figma file is out of date. The current designs are the HTML
  links and zip files."*
- **People and process photos** — `IMG_7980.JPG`, `Joanna_Soh.jpeg`,
  `photo_new_joiner_1_.jpg`, Meetings overview, Ways of Working, Onboarding
  tracker. No technical content.

## Everything else in the mirror

```
python3 tools/attachment_text.py --list     # what is readable, by type
python3 tools/attachment_text.py <file>     # pptx, xlsx, xlsm, docx, html, csv
```

The decision-dense artefacts are mostly *not* diagrams, and several hang off
pages that look empty:

- **Sprint retrospectives** are decks. Sprint 1, 2 and 3 delivery data exists
  nowhere else.
- **The ARC architecture assessment** is two workbooks — 313 requirements, 249
  MUST, every response column blank.
- **The GLS output sample**, `19958562873/OI3_Output_HTML_Export_Sample_Nike_9.html`,
  is the real demo output and extracts as ~14,000 words of readable text. It is
  the fastest way to see what GLS actually showed.

**Not readable from here:** 13 `.mp4` files (both sprint planning sessions, ~2
hours, no transcript), one `.pdf`, and five prototype `.zip` archives — unzip
each into its own empty directory before reading, and pass paths as arguments
rather than running anything from inside.
