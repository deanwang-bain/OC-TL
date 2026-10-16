# GLS walkthrough: running notes (14 Oct, completed case)

Notes in the order of the screens. Tags: **[bug]** broken, **[gap]** not in the design, **[design]** needs a decision, **[label]** wording. Items marked "by design" were checked against the GLS docs.

## Overall

- Need to start from scratch on one company in the demo, and also have a completed case ready so the answer is quick to show. **[design]** Plan is two cases, because Confirm locks a case.
- Everything looks view only. Need to make live changes and see them flow into the output. **[design]** By design after Confirm: Analysis becomes read-only and the case moves to Output. Edits are possible on an unconfirmed case.
- Currency and date are not obvious anywhere. **[label]**

## Landing page / Your Opportunities

- Click an opportunity and the screen is blank: "output is not available yet". Other tabs open fine. **[bug]** Output text is built when Analysis is confirmed, so the seeded case may never have had it built.
- "Analysis is view only" banner at the top of each tab. Is this demo-only? A partner should be able to go back and edit. **[label]** Confirmed-case lock, by design. Banner should say so.
- Currency shown: is it the output currency? Can the partner pick one at setup? Which date is used for conversion? **[design]** Today each case keeps its own currency, no conversion, no choice. Show currency and as-of date on every screen.
- Clicking "Size of prize" on the card goes to an error screen. **[bug]**

## Peers

- Data source says "OI engine". What is it? **[label]** It is the label for computed values and is the old product name. Rename. It appears all over the demo and distracts.

## Case for change

- EBIT margin vs peers: sort highest to lowest, by default or on request. Same for every other chart, best to worst. **[gap]**
- Opportunity sizing sniff test: there are several ways to size, such as % cost reduction, bps of margin, % revenue growth. **[gap]**
- "% uplift" should read "Impact", with a description in the field, e.g. "5-20% cost reduction". **[label]**
- Missing a summary of what the company faces across the business, with a business unit and regional lens, and plain statements of what management says its strategic priorities are. **[design]** Business unit and regional lens are out of this version by design.
- Leadership signals in each card start to get there, but they are thin and buried below the sources. Move them up. **[design]**
- Add an overall summary above the framings. **[design]**
- Make the signals fuller, or expandable to the direct quote and the proof behind it. **[design]**
- First and last signal sentence is cut off: "The CFO says Honda will lift earnings power by strengthening its business structure rather than." **[bug]** Common across other themes too.
- Framings are too math-led. Had to open the sources and read quotes to see that management is cutting variable costs, improving manufacturing efficiency and using more standard parts, and that one quote targets a 30% cut in hybrid production costs. Framings need to reflect stated priorities and investments. **[design]**
- Theme > Benchmarking > Margin above median: same issues as above.
- Analyst reports: are any loaded? Should be. **[design]** Analyst view is out of this version by design.
- Error in chat inside Case for change. **[bug]**

## Analysis

- Lead the visuals with the waterfall summary of value, with the value table below. **[design]**
- Baseline needs the $ figure. **[gap]**
- Bain experience needs the % change (cost reduction, revenue growth, whichever metric). **[gap]**
- Size of prize needs a % change as well as the $. **[gap]**
- Clicking "Size of prize" opens an error screen. **[bug]**
- Where is the benchmarking of the target against peers on the related metric: gross margin for Ops, SG&A for SG&A, R&D for R&D? **[gap]** The lever worksheet charts the metric, but it is not easy to find.

### Operational Excellence (double click)

- Recommended size: error on click. **[bug]**
- Need more on how the numbers were reached. **[gap]**

### SG&A Efficiency (double click)

- "No peer benchmark" for advertising and other G&A. Should be able to benchmark at the combined SG&A level and show that. **[gap]** Peers often report SG&A as one line.
- Show the same combined benchmark on Case for change, because a partner needs the underlying performance to buy into the narrative. **[gap]**

### Commercial Excellence (double click)

- Need more on how the numbers were reached, as for Ops and SG&A. **[gap]**
- Revenue projection: state the timeline it covers. **[gap]**
- Want the target and peer data underneath. **[gap]**
- This is where the Bain experience should be defended with reference cases and research that shows the value. **[design]** Case studies and reference cases are out of this version by design.

### Across the whole flow

- Case for change comes before the analysis, but to accept the case for change a partner needs the company's performance and trends first, backed by management statements and analyst commentary. Bain experience matters less there. **[design]**
- In Analysis, when getting comfortable with the $ targets, need the supporting benchmarks and Bain experience close by, plus evidence of real value from the company's situation, management reports and the industry. **[design]**

## Output

- Not available for this case. **[bug]**
- Where are the initiatives for each value lever? **[design]** Recommended actions and timelines are out of this version by design. Example levers can be listed without timelines.

## Not planned for this version (say so on stage)

Analyst reports and ratings, business unit and regional lens, Bain case studies and reference cases, initiatives with timelines, live market data.
