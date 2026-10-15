# GLS mode: what the core repo specifies

Distilled from `docs/gls/` in `nextgen-opportunity-catalyst-core` (zip snapshot read 2026-10-15; no git
history in the archive, so no commit id). The repo's own rule is that `docs/gls/` wins over code,
findings notes and chat threads. Read the originals before relying on a detail here.

**GLS mode** is the golden-dataset build of the journey for the Global Leadership Summit: a partner walks
Dashboard, Target, Peers, Case for change, Analysis and Output on a fixed set of companies taken from
finished Bain cases, with every number recomputed from the case team's formulas.

## What the snapshot contains, and what it does not

| In the zip | Not in the zip |
| ---------- | -------------- |
| The GLS spec: `docs/gls/` api, frontend, agents and data files, about 2,500 lines | `services/experience-bff/src/gls/` (store, calc port, loader, adapters, routes, narrative). The spec describes it; the folder does not exist |
| BFF, case, audit, identity, evidence, search services and two agents (chat, peer discovery) | The SPA, which is a separate repository (spec names branch `OI3-238-205-merged`) |
| `dev/run.py` local stacks, deployment inputs | Golden data and its overlays (`.local/gls-data/`, outside git by design) |

Evidence from running the snapshot on 2026-10-15: `npm ci` and `npm test` in `services/experience-bff`
pass, **695 of 695**. The BFF's `contracts/openapi.json` lists 29 routes, **none** of them the GLS ones
(`/analysis`, `/case-for-change`, `/output`, `/target-setup` PUT, `/peer-candidates`). The local Docker stack
cannot start in the cloud session: `dev/run.py doctor --stack app` fails on "the Docker daemon is not
reachable". The stack also needs amd64 and an OpenAI key placed by hand.

The local stack in `dev/getting-started.md` is **not** the GLS demo. It serves a synthetic snapshot of
15,000 `MOCK` companies, and nothing in it carries the golden cases.

## The journey, as specified

| Stage | The partner can | Locks |
| ----- | --------------- | ----- |
| 0 Dashboard | Create, archive, restore, delete a case. Card shows stage, vintage, and prize split once sized | Delete removes the case copy and its log for good |
| 1 Target | Search the golden universe (two characters minimum), resolve one company, set audience, two framing answers and comparability criteria, propose peers | **Locks at propose.** No way back to Target. A resolve cannot be undone |
| 2 Peers | Tick and untick peers (stats recompute), read each rationale, add a deselected peer or **another golden target as a peer**, confirm | Free movement between Peers, Case for change and Analysis |
| 3 Case for change | Reorder and select framings, state an inclination, read benchmark bars, sizing preview, sources, leadership signals, client readiness; confirm or skip | As above |
| 4 Analysis | Include or exclude buckets and levers, edit **one input per lever**, switch benchmark set (where the case has peer groups), read EBIT and cash bridges, confirm | **Confirm is one way**: Target, Peers, Case for change and Analysis become read-only |
| 5 Output | Read an eight-part tabbed report, print to PDF, export one HTML file | Numbers cannot change. Only narrative can be rewritten or regenerated (by chat) |

Chat can do almost everything the screens can (select peers, set a number, switch benchmark set, rewrite a
block, undo). Two writes need the partner's yes first: deselecting more than one peer, and moving to Output.
There is no agent tool for confirming Case for change.

## Rules that matter on stage

- **Numbers.** A figure is the published deck value until touched, then the engine value, with the deck
  figure kept as "as presented". Totals always equal the sum of their rows, so a printed deck total that
  disagreed with its rows is replaced by the reconciled figure (ruling C5).
- **Recommendation rule.** A bucket's opportunity is `max(peer benchmark, Bain low end)` per range end. Levers
  have no opportunity of their own (I1). Consequence: editing a Bain savings percentage can leave the bucket's
  opportunity unchanged when the peer leg dominates.
- **Working capital only.** Bucket D is "Working capital". There is no capex lever, no payback period. Cash
  and P&L are never added together.
- **EBIT, not EBITDA.** Relabelled, not converted.
- **n/a with a reason**, never zero or an estimate. Where a web filing figure exists it appears only inside a
  citation sheet, never in a cell, a median or a sizing.
- **Currency.** Each case is in its own currency (at least one is in euros). No FX choice. Cross-set peers carry
  an FX rate and date.
- **Point in time.** Data is frozen at each case's original date and the dates differ between companies.
- **No reset.** Undo is a chat request served from the mutation log. A narrative entry is regenerated, not
  undone.
- **Leadership signals** come from the narrative agent's web search. The usual citation is a search summary,
  labelled "Search summary", not a quoted passage. They are found once and rerun only by an explicit regenerate.
- **Source chips.** `OI engine` marks computed values (`data/source-labels.md`). It is the old product name and
  a one-line label change for SN.

## Skipped by design (so do not promise it)

Business-unit and regional lens, document upload, analyst view and ratings, confidence percentages, case
studies and IRIS content, Recommended Actions and their timelines, dashboard chat, PPTX export, deck-builder chat,
Sources and Log tabs on Output, share modal, Why Bain slide, currency choice, live market data, company search
beyond the golden set. Source: `docs/gls/overview.md` section 1 and `stakeholder-communication.md`.

## Known operational risks

- **A9, Redis durability, parked.** Cases live only in Redis in GLS mode. A restart empties the dashboard with no
  error until AOF and a volume are on. Owner recommendation: turn AOF on before the summit.
- **503 `golden_not_loaded`.** If the golden bundle is not loaded every screen shows an error state. How golden
  data reaches the dev environment is "decided separately" and is outside the contract. Unknown to us.
- **Narrative is asynchronous.** It is generated at propose, again after peer changes, and for Output at confirm.
  The first open of Output usually lands in a `generating` state with skeleton lines.

## Where the 14 October tester feedback meets the spec

| Feedback | Spec position |
| -------- | ------------- |
| "Everything view only" | Intended after Analysis is confirmed. The tested case was probably a completed one |
| "Output is not available yet" | Output narrative is built at confirm and shows skeletons first. Probably not generated for that case. Unconfirmed |
| Currency and conversion date | Labelled per case, no FX, vintage per case. Gap is that the date is not prominent |
| Sort charts best to worst | Bars are served in a fixed order. Not in the spec. A gap to raise with SN |
| `% uplift` to "Impact" | Case for change sizing carries `uplift_pct` and `value_range`. Label change |
| Baseline in $, Bain experience and prize with %, benchmark view per lever, SG&A combined benchmark | Not in the spec. The analysis read gives `baseline.display`, ranges in currency. Gaps to raise with SN |
| Leadership signals above "sources", expandable proof, complete sentences | Spec has a citation sheet per signal. Placement and truncation are SN fixes |
| Analyst reports, BU and regional lens, initiatives per lever, reference cases | Explicitly out of GLS scope |
| Case for change before Analysis | Navigation is free between stages 1 to 3. Order is the design's |
| Errors on "Size of prize", Operational Excellence size, Case for Change chat | Not explained by the spec. Treat as defects |
