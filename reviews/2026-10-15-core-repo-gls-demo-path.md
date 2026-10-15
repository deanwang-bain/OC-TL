---
date: 2026-10-15
subject: "nextgen-opportunity-catalyst-core (main, zip snapshot) — GLS demo readiness and demo path"
source: "Uploaded zip d990e8be-nextgen-opportunity-catalyst-core-main_1.zip (no git history in the archive, so no commit id)"
reviewer: Claude (for Tech Lead sign-off)
outcome: approve with comments
---

# Review: core repo snapshot, and a demo path for GLS

## Scope

Read: `README.md`, `AGENTS.md`, `dev/` docs, and all of `docs/gls/` (overview, stakeholder communication, and the api and frontend files for stages 0 to 5). Skimmed the experience-BFF and agent directory layout.

Not done: nothing was run. There is no Docker here, and the stack needs amd64 plus an OpenAI key. The SPA is in a separate repository. The golden data is deliberately outside git. Where a statement below is about behaviour rather than about the docs, it comes from the 14 October tester feedback and is marked **(tester)**. Where it is my inference, it is marked **(inferred)**.

## Outcome

The snapshot is the GLS **specification** plus the platform scaffolding. It is not the GLS implementation. `docs/gls/` describes `services/experience-bff/src/gls/` (store, calc port, loader, adapters, routes, narrative), and that folder does not exist in the zip. The BFF's `src/` has no GLS code, and nothing outside `docs/` references `OC_GLS_MODE`. The demo the tester used therefore runs from a build I cannot see. The demo path below is built on the spec and the feedback. Rehearse it on the real environment before relying on it.

## Findings that shape the demo

1. **"Analysis is view only" is the intended behaviour of a completed case, not a demo-only banner.** Confirming Analysis moves the case to Output one way, and Target, Peers, Case for change and Analysis become read-only (`docs/gls/api/04-analysis.md:65`, `docs/gls/frontend/04-analysis.md:143`, banner "This analysis is confirmed and read-only"). The Honda case was evidently a finished one **(inferred)**. This means one case cannot be both editable and showing Output. The demo needs two cases.
2. **"Output is not available yet" (tester).** Output's narrative is generated when Analysis is confirmed, in the background (`api/04-analysis.md:65`). A case seeded or confirmed without that run would show this **(inferred)**. Check that Output renders for the completed case before the demo day.
3. **No reset, undo only through chat** (`overview.md` section 4, ruling B42). A bad edit during the live segment can only be reversed by asking chat. Plan for that, and keep a spare case.
4. **Cases live only in Redis, and persistence is parked (A9).** A Redis restart empties the dashboard with no error (`frontend/00-dashboard.md` section 7). Build the completed case close to the demo, and have the exported PDF and HTML as a fallback.
5. **Currency and dates.** Each case is in its own currency, frozen at the date of its original case, with no FX and no user currency choice (`stakeholder-communication.md`). The tester's currency question has an answer on paper: labelled per case, no conversion. Say so up front and pick a USD case.
6. **"OI engine" label** is a source chip for computed values (`data/source-labels.md:34,46`). It is the old product name, so the rename the tester suggests is a one-line label change for SN.
7. **Leadership signals** are found by web search, so they vary run to run. The tester saw truncated sentences. Open the framings before the demo and do not trigger a regeneration live. Changing peers regenerates the affected narrative in the background, so leave time for it.
8. **Gaps the tester raised that the spec confirms are out of scope:** analyst reports ("no analyst ratings"), business-unit and regional lens, Bain case studies and reference cases, initiatives per lever (Recommended Actions dropped), currency selection. Do not promise them on stage.
9. **Defects seen by the tester, not in the spec: avoid on stage.** Clicking "Size of prize" opened an error screen. Clicking into the recommended size of Operational Excellence errored. The chat in Case for Change errored. Raise these with SN as bugs, and keep the demo off those clicks until they are fixed.

## Demo path

**Setup, before the day.** Both cases use the same company, so the story carries over. Pick a USD company in the golden set that has all four buckets sized, including Commercial Excellence and a peer benchmark. Two companies are known to have Commercial Excellence hidden, and some buckets have no deck recommendation (`stakeholder-communication.md`, "Empty or thin buckets"). Check the dashboard cards for the candidate before choosing it. The company is a choice to make against the loaded data, since the docs name none.

- **Case A, "completed".** Run the full journey through Confirm. Open every Output tab. Export the PDF and HTML as backup.
- **Case B, "from scratch".** Create it only on stage. Keep a third case ready in case B goes wrong.

**Act 1, from scratch (Case B), about 6 minutes.**
1. Dashboard: Create. Type two characters of the company name. Suggestions only appear after two characters.
2. Resolve the target. Point out the company panel with its source chips and the "Latest period" label. State the data date and currency here.
3. Target setup: set the audience and the two framing questions. Point out that these steer wording, not numbers. Propose peers. Say that Target locks here.
4. Peers: show the selected peers and open one drilldown. Untick one peer and watch the median recompute. Then tick it back (the recompute is the live proof).

**Act 2, case for change, about 4 minutes.** Open one framing and read its leadership signals and quotes. Open the benchmark bars. Be ready for the tester's point that the case for change comes before the supporting data. Say that the order is the design's, and that Peers and Analysis stay reachable both ways.

**Act 3, the live edit (Case B in Analysis), about 6 minutes.**
1. Show the size-of-prize table and the EBIT bridge.
2. Open one bucket, open a lever worksheet, change its single editable input, and watch the bucket, totals and bridge recompute. The "as presented" value stays available.
3. Include or exclude a bucket to show totals reconciling.
4. Ask chat to explain one number, then undo the edit through chat. This shows the audit trail and the "no reset" rule together.
5. **Do not Confirm Case B** unless you intend to show Output from it.

**Act 4, the answer (Case A), about 4 minutes.** Open Case A. Walk Output tab by tab: Executive summary, Peers, Metrics, Size of prize, Methodology. Note the read-only banner and explain it as the one-way lock. Print to PDF.

**Close, about 2 minutes: limits, said up front.** Fixed golden companies as of each case date, no live data, no document upload, no analyst reports, no PPTX. The post-GLS direction is the last section of `stakeholder-communication.md`.

## Should fix (for SN, from the tester's list, none are spec gaps)

- The three errors in finding 9.
- Output unavailable for the seeded case (finding 2).
- Truncated leadership-signal sentences; expand-for-evidence.
- Amount basis: show % alongside $ for Bain experience and size of prize, and a $ figure for the baseline.
- Sort benchmark charts best to worst by default.

## Open questions (added to `context/open-questions.md` if you want them tracked)

- Which golden companies exist, and which are USD with all four buckets sized? Needs a look at the loaded data.
- Is Redis persistence (A9) on for the demo environment?
- Which build did the tester use, since this zip lacks the GLS code?
