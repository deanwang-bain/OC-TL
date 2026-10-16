# Opportunity Catalyst: GLS demo path

About 25 minutes plus questions. Written from the GLS design documents and the partner feedback of 14 October. It has not been rehearsed on the live environment, so treat the "expected" behaviour as what the design says should happen, and confirm each step in rehearsal.

## The idea

Show one company twice: built from scratch on stage, and already completed.

- **Case A, completed.** Run through to the end, so the answer can be shown instantly.
- **Case B, from scratch.** Created live. It stays editable because it is never confirmed.
- **Case C, spare.** Parked at Analysis in case an edit on B goes wrong.

**Why two cases.** Confirming the Analysis stage is one way. It makes Target, Peers, Case for change and Analysis read-only and moves the case to Output. A case that shows Output can never be edited, which is why a finished case reads "view only". The live edit therefore happens on B, and the answer is shown from A.

## Before the day

Create a throwaway case and check each line. Pick the company by these checks, not by name.

| Check | How | If it fails |
| ----- | --- | ----------- |
| Data is loaded | Create a case. A "golden data not loaded" error means it is not | Stop and get the data loaded |
| Cases survive a restart | Cases live only in Redis. A restart empties the dashboard with no error | Build Case A the same morning and export it straight away |
| Company suits the demo | USD. The company panel shows a period label and currency | Choose another company |
| All four buckets are sized | At Analysis, Commercial Excellence is present with an Opportunity, and no bucket reads "Not sized in the deck". Two companies hide Commercial Excellence | Choose another company |
| Cash side exists | The Cash tab shows one to three working-capital bars | Choose another company |
| Add-a-peer has candidates | "Other target companies" lists at least one, with its warnings | Skip step 2.4 |
| Leadership signals present | A framing shows signals, or says none were found | Open every framing in Case A beforehand. Do not regenerate live |
| Output builds | Confirm a throwaway case. All eight parts load after the skeleton lines | Do not show Output live. Use the exports |
| Chat works | Ask "where does the baseline come from?" | Skip the chat beats |
| Known error clicks | Size of prize on the dashboard card. The Operational Excellence recommended size. Chat inside Case for change | Avoid any that still fail |

Then build Case A: run it through Confirm, open every Output tab, and export the PDF and HTML. Do not edit it afterwards. Repeat the checks an hour before the demo.

## Act 1. Start from scratch on Case B (6 min)

| Step | Action | Say |
| ---- | ------ | --- |
| 1.1 | On the dashboard, press Create | One card, no company yet. The prize reads "Sized after analysis" |
| 1.2 | Type two characters of the company name | Only prepared companies exist. There is no live market data |
| 1.3 | Resolve the company and read the company panel | Say the period label, the currency and the data date out loud. Each figure has a source chip. Missing values are hidden, never shown as zero |
| 1.4 | Set the audience, the two framing answers and the comparability criteria | These steer the wording, not the numbers. They save automatically |
| 1.5 | Press Propose peers | Say first: this locks the target and the setup |

## Act 2. Peers (4 min)

| Step | Action | Say |
| ---- | ------ | --- |
| 2.1 | Show the grid. Point to each card's period label and the currency chip | Peers report on different fiscal calendars. Nothing is estimated to fill a gap |
| 2.2 | Open one peer. Read the rationale, the criteria radar and the key metrics | Rationale is written by an agent for this audience. `n/a` rows give a reason on hover. There is no confidence percentage, by design |
| 2.3 | Untick one peer, then tick it back | Peer median and ranking recompute from the case formulas. At least one peer must stay selected |
| 2.4 | Optional: add a peer from "Other target companies" | Its data is from its own case, so its date and currency can differ. Its TSR is left out of the TSR median. Warnings show but do not block |
| 2.5 | Confirm the set | Peers, Case for change and Analysis stay freely navigable from here until Confirm on Analysis |

## Act 3. Case for change (4 min)

| Step | Action | Say |
| ---- | ------ | --- |
| 3.1 | Read the headline and framing list. Name the recommended lead | Each framing is titled by its computed rating. A top-quartile company is never told it is "below peers". Order can be changed with the arrows |
| 3.2 | Open the top framing. Show the benchmark bars and the sizing preview | The sizing preview is marked illustrative |
| 3.3 | Scroll to Leadership signals and open one | Found by web search, each linked to its source. The usual citation is a search summary, and the sheet says so |
| 3.4 | Open "Open lineage" on a source | Any number traces to its formula, inputs, peer membership and adjustments. The trail ends at the case workbook and deck, not at a filing page |
| 3.5 | Type an inclination, for example "lean towards the cost story" | It persists and steers later wording and each framing's client readiness. Text refreshes in the background, so move on without waiting |
| 3.6 | Confirm and build the analysis | Nothing locks yet |

## Act 4. Analysis and the live edit (7 min)

| Step | Action | Say |
| ---- | ------ | --- |
| 4.1 | Walk the table: Baseline, Bain experience, Peer benchmark, Opportunity, by bucket | P&L and cash are never added together. Everything is EBIT, not EBITDA |
| 4.2 | Open the EBIT bridge, then the Cash tab | Solid bars are the low end, dashed the high end. Cash bars add up to the Working capital bucket |
| 4.3 | Open one bucket, then one lever worksheet | Show the derivation chain, the chart with median and top quartile, and the single editable row |
| 4.4 | **Make the live edit** (see the box below) | Totals, bridge and prize recompute. The original figure stays one tooltip away as "As presented" |
| 4.5 | Untick one bucket, then tick it back | Totals always equal the sum of their rows |
| 4.6 | If the case has peer groups, switch the benchmark set | Every peer-based value recomputes. Skip if the control is not shown |
| 4.7 | Go back to Peers, untick a peer, return to Analysis | The numbers moved because the peer median moved |
| 4.8 | Ask chat: "Explain the baseline for the first bucket." Then: "Undo my last change." | Undo is served from the change log. There is no reset button, by design |
| 4.9 | **Do not confirm Case B** | Confirming would lock the case |

> **Choosing the live edit.** A bucket's recommended size is the larger of the peer benchmark and the Bain low end, per end of the range.
>
> - **Safe:** change a working-capital lever's target days, or switch a peer-row lever's anchor from median to top quartile. Cash bars and totals visibly move.
> - **Risky:** raising a Bain savings percentage. If the peer figure is already higher, the bucket's Opportunity does not move and the demo looks broken. Rehearse the exact lever first and note which bucket it moves.
>
> A recompute can also move further than the edit suggests, because the published recommendation was a judgement and the rule is mechanical. "As presented" is the explanation, so have that sentence ready.

## Act 5. The answer on Case A (4 min)

| Step | Action | Say |
| ---- | ------ | --- |
| 5.1 | Open Case A from the dashboard | Earlier stages show as done and locked |
| 5.2 | Tour the five tabs: Executive summary, Peers, Metrics, Size of prize, Methodology | Eight parts, none cut. Text is written by an agent. Numbers come from the case formulas |
| 5.3 | On Size of prize, press a bridge bar | The lever table opens underneath |
| 5.4 | On Methodology, read the limitations | Known discrepancies and exclusions are stated, not hidden |
| 5.5 | Print to PDF | Confirm in rehearsal that every tab prints, not only the active one |

## Close (2 min): state the limits first

- Data is frozen at each case's date. Dates differ between companies and peers.
- No live market data, document upload, analyst reports, or business-unit and regional lens.
- No Bain case studies, per-lever initiatives or timelines, or PowerPoint export.
- Currency cannot be changed. Each case is in its own currency.

## Likely questions

| Question | Answer |
| -------- | ------ |
| Can I edit after the output? | No. Output is one way and read-only. Edit on Analysis, and build a new case if needed |
| Can I change the currency? | No. Each case keeps its own currency, with no conversion choice |
| What date are the numbers? | The date of the original case. It differs between companies |
| Where are the analyst reports? | Not in this version. Management statements come from a web search with citations |
| What is "OI engine"? | The source label for computed values. It is the old product name |
| Can we undo? | Yes, through chat, from the change log. There is no reset button |
| Where are the initiatives for each lever? | Not in this version. Example levers can be listed, without timelines |
| Where is the benchmark behind each lever? | The lever worksheet charts the metric against median and top quartile. Peer benchmarks sit at bucket level where peers report only the cost line |
