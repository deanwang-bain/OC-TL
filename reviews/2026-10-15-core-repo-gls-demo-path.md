---
date: 2026-10-15
subject: "nextgen-opportunity-catalyst-core (main, zip snapshot) — GLS demo readiness and demo path"
source: "Uploaded zip d990e8be-nextgen-opportunity-catalyst-core-main_1.zip (no git history in the archive, so no commit id)"
reviewer: Claude (for Tech Lead sign-off)
outcome: approve with comments
---

# Review: core repo snapshot, and a demo path for GLS

Distilled understanding of GLS mode is in [`context/gls-mode.md`](../context/gls-mode.md). This record holds the review and the demo runbook.

## Scope

Read: `README.md`, `AGENTS.md`, `dev/` docs, and all of `docs/gls/` (overview, stakeholder communication, and the api and frontend files for stages 0 to 5, plus the agent tool list and data quirks).

Run: `npm ci` and `npm test` for `services/experience-bff`. **695 of 695 pass.** `python3 dev/run.py doctor --stack app` fails because the Docker daemon is not reachable in this session, so the stack could not start.

Not done: the GLS journey was not run, and **cannot be run from this zip**. See the outcome. Statements about behaviour come from the spec, or from the 14 October tester feedback **(tester)**, or are my inference **(inferred)**.

## Outcome

The snapshot is the GLS **specification** plus the platform scaffolding. It is not the GLS implementation. `docs/gls/` describes `services/experience-bff/src/gls/`, which does not exist in the zip. The BFF's OpenAPI contract has 29 routes and none are the GLS routes (`/analysis`, `/case-for-change`, `/output`, `/peer-candidates`, `PUT /target-setup`). The SPA is a separate repo and the golden data is outside git by design. The only thing that could run locally is the generic stack on 15,000 synthetic `MOCK` companies, which is a different product surface and would mislead if shown.

So the demo path below is built from the spec and the tester's feedback. It is a rehearsal plan for the real GLS environment, and its first job is to find out whether that environment behaves as the spec says. Section 1 is the pre-flight that settles that.

## 1. Pre-flight (do this 24 hours before, and again 1 hour before)

Each line is a yes or no. Any "no" changes the plan.

| Check | How | If no |
| ----- | --- | ----- |
| Golden data is loaded | Open the dashboard and create a case. A `503 golden_not_loaded` error state means it is not | Stop. Ask SN for the load. Nothing else can be rehearsed |
| Redis persistence is on | Ask SN (owner item A9 is **parked**). Restart-loss means an empty dashboard with no error | Build Case A the same morning, and export its PDF and HTML straight away |
| The target company is right | Search two characters of the name. Check it resolves, the company panel shows the **period label** and the **currency** | Pick another company |
| All four buckets are sized | In a throwaway case, reach Analysis. Check Commercial Excellence is present and has an Opportunity, and no bucket reads "Not sized in the deck" (two companies hide Commercial Excellence, and some buckets start unticked) | Pick another company |
| The cash side has levers | Cash tab shows one to three working-capital bars | Pick another company |
| Peers include a candidate with warnings | Open "Add a peer". Note the "Other target companies" group and its warnings (TSR window, SBC basis) | Skip the add-a-peer beat |
| Leadership signals are populated | Open a framing. Signals either show, or say "No leadership signals were found" | Open every framing in Case A now, and do not regenerate live |
| Output builds | Confirm a throwaway case, open Output, wait for the skeleton lines to resolve into all eight parts | Do not demo Output live. Use the export |
| Chat works | Ask "where does the baseline come from?" in the throwaway case. The tester saw a chat error in Case for Change | Skip chat beats. Replace the undo beat with "no reset, by design" |
| The three tester errors | Click "Size of prize" on the dashboard card, open the Operational Excellence recommended size, use chat in Case for Change | Avoid those clicks. Raise them with SN |

Pick the company by these checks, not by name. The docs deliberately name no golden company.

## 2. Case setup

Both cases use the same company so the story carries over.

- **Case A, "completed".** Create it the morning of, run it through Confirm, open every Output tab, export the PDF and the HTML. Do not edit it afterwards.
- **Case B, "from scratch".** Create it on stage.
- **Case C, spare.** Resolved and sitting at Analysis, in case an edit on B goes wrong.

**Why two cases:** the tester's "everything is view only" is the spec's one-way lock. Confirming Analysis makes stages 1 to 4 read-only. A case that shows Output can never be edited, so the live edit happens on B and the answer is shown from A.

## 3. Runbook (about 25 minutes plus questions)

Timings assume the narrative has already generated. Anything marked **(wait)** depends on a background agent, so leave slack.

### Act 1. Start from scratch on Case B (6 minutes)

| Step | Action | Say or point out | What the spec says should happen |
| ---- | ------ | ---------------- | -------------------------------- |
| 1.1 | Dashboard. Press Create | One card, single-person, no company yet | Create takes no body. Card says "Sized after analysis" until Analysis |
| 1.2 | Type two characters of the company name in the target search | Only the prepared companies exist. No live market data | Suggestions appear after two characters. An outside company gives `out_of_universe` ("not available in this demo") |
| 1.3 | Resolve the company. Read the company panel | Each figure has a source chip. Say the **period label and currency** out loud. Say the data is frozen at the original case date | Panel shows revenue, adjusted EBIT, valuation, "Latest period", "Valuation as of". Missing values are hidden, never zero |
| 1.4 | Set the audience, the two framing answers and the comparability criteria | These steer wording, not numbers | Auto-saves. Saved to the case, so chat can read it |
| 1.5 | Press Propose peers | **Target and setup now lock.** Say this before pressing | 202. Peers are all pre-selected. Narrative starts generating in the background |

### Act 2. Peers (4 minutes)

| Step | Action | Say or point out | Spec |
| ---- | ------ | ---------------- | ---- |
| 2.1 | Show the grid. Point to the **period label on each card** and the currency chip | Peers report on different fiscal calendars. Nothing is estimated to fill a gap | Per-card `ltm_label`. A value that fell back to an earlier period says so |
| 2.2 | Open one peer. Read "why included", the criteria radar and the key metrics | Rationale is written by an agent for this audience. `n/a` rows show a reason on hover | Confidence factors show, but **no percentage** (by design) |
| 2.3 | Untick one peer | Peer median and ranking recompute from the formulas. Tick it back | Every tick recomputes. The last peer cannot be unticked ("At least one peer stays selected") |
| 2.4 | Optional: Add a peer, choose from "Other target companies" | Its data is from its own case so its date and currency may differ. Its TSR is left out of the TSR median | Amber warnings show but do not block. **Skip if pre-flight showed none** |
| 2.5 | Confirm the set | | First confirm moves to Case for change. Stages 1 to 3 stay freely navigable |

### Act 3. Case for change (4 minutes)

| Step | Action | Say or point out | Spec |
| ---- | ------ | ---------------- | ---- |
| 3.1 | Read the headline and the framing list. Say which is the "Recommended lead" | Each framing is titled by its computed rating. A company already top quartile is never told it is "below peers" | Titles follow rating. Order can be changed with the arrows |
| 3.2 | Open the top framing. Show the benchmark bars and the sizing preview | The sizing preview is labelled illustrative | `baseline_basis: illustrative_profile` shows a small marker |
| 3.3 | Scroll to **Leadership signals** and open one | Found by web search. Each links to its source. The usual citation is a **search summary**, and the sheet says so | Signal citation sheet. Empty state says "No leadership signals were found" |
| 3.4 | Open "Open lineage" on one source | Any number traces to formula, inputs, peer membership and adjustments. The trail ends at the case workbook and deck, not at a filing page | Lineage sheet. This is the transparency answer |
| 3.5 | Type an **inclination** ("lean towards the cost story") | It persists and steers later wording and each framing's client readiness | Readiness and text go "refreshing" **(wait)**. Don't wait on stage. Move on |
| 3.6 | Confirm and build analysis | | Moves to Analysis. Does **not** lock anything yet |

### Act 4. Analysis and the live edit (7 minutes)

| Step | Action | Say or point out | Spec |
| ---- | ------ | ---------------- | ---- |
| 4.1 | Read the table: Baseline, Bain experience, Peer benchmark, Opportunity, by bucket | Say "P&L and cash are never added together". EBIT, not EBITDA | Section bands: P&L, then Cash release |
| 4.2 | Open the EBIT bridge, then the Cash tab | Bars are the low end, with the high end dashed | Cash bars add up to the Working capital bucket |
| 4.3 | Open one bucket and one lever worksheet | Show the derivation chain, the chart with median and top quartile, and the single editable row | Chain rows show source chips and open lineage |
| 4.4 | **Make the live edit.** See the box below for which lever to pick | Totals, bridge and prize recompute. The old figure is one tooltip away as "As presented" | Edited rows show a "recomputed" marker |
| 4.5 | Untick one bucket | Totals re-sum, footer count changes. Tick it back | Totals always reconcile with their rows |
| 4.6 | If the case has peer groups: switch the benchmark set | Every peer-based value recomputes. Hide this control otherwise | Only shown when `benchmark_set` has a named group |
| 4.7 | Go back to Peers, untick a peer, return to Analysis | Numbers moved because the peer median moved | Free movement until Confirm. Narrative goes stale **(wait)** |
| 4.8 | Ask chat: "Explain the baseline for the first bucket." Then "Undo my last change." | Undo comes from the mutation log. There is no reset button, by design | Chat reads lineage and the activity log. Needs the Log tab to show the entry |
| 4.9 | **Do not Confirm Case B.** Say why: it would lock the case | | `move_to_output` asks the partner first, always |

> **Choosing the live edit (matters).** The bucket recommendation is `max(peer benchmark, Bain low end)` per range end. So:
>
> - **Safest:** edit a **working-capital lever** (target days, or switch the anchor from median to top quartile). The Cash bucket's opportunity is the sum of the NWC peer ranges, so the Cash total and the cash bars move visibly.
> - **Also safe:** switch the anchor on a **peer-row lever** (median to top quartile). The peer leg moves and the opportunity follows.
> - **Risky:** raising a Bain savings percentage. If the peer leg already exceeds the Bain range, **the bucket's Opportunity will not move**, and the demo will look like nothing happened. Rehearse the exact lever first, and note which bucket it moves.
>
> The recompute can also move further than the edit suggests, because the published recommendation was a judgement and the rule is mechanical. "As presented" is the explanation. Have that sentence ready.

### Act 5. The answer on Case A (4 minutes)

| Step | Action | Say or point out | Spec |
| ---- | ------ | ---------------- | ---- |
| 5.1 | Open Case A from the dashboard | Stage shows as reached. Earlier stages show as done and locked | Rail marks steps 1 to 4 blocked, "Locked once the report is built" |
| 5.2 | Tour the five tabs: Executive summary, Peers, Metrics, Size of prize, Methodology | Eight parts, none cut. Text is written by an agent. Numbers are the engine's | Output is read-only for numbers |
| 5.3 | On Size of prize, press a bridge bar | The lever table opens underneath | Drill-down per bucket |
| 5.4 | On Methodology, read the limitations | Known discrepancies and exclusions are stated, not hidden | Limitations come from the case's recorded overrides |
| 5.5 | Print to PDF | Shows every tab, not only the active one (the design's default prints one) | Needs the flattened print view. **Check it in rehearsal** |

### Close (2 minutes): say the limits before they are found

Frozen at each case's date. No live data, no document upload, no analyst reports, no business-unit or regional lens, no Bain case studies, no per-lever initiatives or timelines, no PPTX. Totals and rankings follow the case formulas, and the deck's own figure stays available as "as presented". The direction after GLS is the last section of `docs/gls/stakeholder-communication.md`.

## 4. Likely questions, with the honest answer

| Question | Answer |
| -------- | ------ |
| Can I edit after the output? | No. Output is one-way and read-only. Edit on Analysis and rebuild with a new case |
| Can I change the currency? | No. Each case is in its own currency. There is no conversion choice |
| What date are the numbers? | The date of the original case. It differs between companies and peers |
| Where are the analyst reports? | Not in GLS. Management statements come from a web search with citations |
| What is "OI engine"? | The source chip for computed values. The old product name |
| Can we undo? | Yes, through chat, from the change log. No reset button |
| Where are the initiatives per lever? | Not in GLS. The lever's example levers can be listed, with no timelines |
| Can I see the benchmark behind each lever? | The lever worksheet shows the metric chart with median and top quartile. Bucket-level peer benchmarks only where peers report the line |

## Should fix (for SN)

From the tester's list. None of these are spec gaps unless marked.

- The three errors (Size of prize click, Operational Excellence size, Case for Change chat). Not explained by the spec.
- Output unavailable for the seeded case.
- Truncated leadership-signal sentences, and leadership signals sitting below the sources.
- Sort benchmark charts best to worst by default. **Spec gap**: bars are served in a fixed order.
- Show % beside $ for Bain experience and size of prize, and a $ baseline. **Spec gap.**
- Combined SG&A benchmark where advertising and other G&A have no peer benchmark. **Spec gap**; the spec shows n/a with a reason as a principle (ruling F1).
- Make the data date and currency prominent on every screen, not only in labels.
- Rename the "OI engine" chip.

## Open questions

Added to `context/open-questions.md`:

- Which build and environment did the tester use? The zip lacks the GLS code.
- How does golden data reach the dev environment, and is it loaded for the demo?
- Is Redis persistence (A9) on?
- Which golden companies are USD with all four buckets sized and a cash side?
