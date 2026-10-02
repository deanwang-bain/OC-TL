---
title: "Design requirements (Post GLS)"
confluence_id: 19808256031
confluence_url: https://bainco.atlassian.net/wiki/spaces/OI30/pages/19808256031
version: 9
updated: 2026-10-01T03:45:28.611Z
---

# Design requirements (Post GLS)

[View in Confluence](https://bainco.atlassian.net/wiki/spaces/OI30/pages/19808256031)

This doc captures new usability requirements identified from user testing sessions with Mark, Andrew, Klaus, Alyson, Saverio, and Andrea in September 2026.

They supplement (and do not replace) the core design requirements document dated 16 July 2026.

Based on the [Design Principles]design principles: **Partner judgment**, **Radical transparency**, **Thought partner**, **Modular flow**, **Co-creation**

| **#**  | **User need**  | **Design Requirement**  | **Design Principle**  | **Design Component**  | **Feedback**  |
|---|---|---|---|---|---|
| Calculation transparency and evidence  |
| 17.1  | See how each sizing range was calculated  | Every bucket and sub-lever shows the full calculation breakdown: Bain experience range, peer benchmark range, and how they converge to the recommended figure.  | **Radical transparency**  | Calculation breakdown panel  |  |
| 17.2  | See a relevant industry example that grounds the number  | Each bucket surfaces a contextual benchmark example (e.g. peers in this sector achieved X% SG&A reduction over 3 years) alongside the sizing.  | **Thought partner**  | Inline benchmark example card  | TBD  |
| 17.3  | Substantiate the value range with evidence before presenting it  | Partner can drill into any range and see the full evidence stack — peer data points, Bain case analogues, and assumptions — that produced the floor and ceiling.  | **Radical transparency**  | Evidence stack drill-down panel  |  |
| Case studies  |
| 18.1  | See relevant Bain case studies at the top bucket level  | At bucket level (A — Commercial Excellence, B — Operational Excellence, C — SG&A Efficiency), surface 2 to 3 recommended Bain case studies from IRIS relevant to that lever category.  | **Thought partner**  | IRIS case study card at bucket level  | To merge 18.1 and 18.2  |
| 18.2  | Access transformation stories, not just case references  | IRIS integration surfaces full Bain transformation stories — what was done, what was achieved, and which team delivered it — not just case titles.  | **Thought partner**  | IRIS transformation story card  |
| 18.3  | Know where Bain has done this before at a glance  | Each opportunity and bucket links to prior Bain experience — case name, sector, impact delivered, and team — without leaving the analysis screen.  | **Thought partner** **Radical transparency**  | Prior experience inline reference  |  |
| Value realisation and impact ramp  |
| 19.1  | Understand how long it will take to realise each opportunity  | Each opportunity shows an indicative realisation timeline: quick win (0 to 6 months), medium term (6 to 18 months), or structural (18 to 36 months).  | **Partner judgment**  | Realisation timeline indicator  | Pending Steph’s confirmation  |
| 19.2  | Understand what it takes to capture each opportunity  | Each sub-lever surfaces the typical actions and initiatives required to realise the value, drawing on Bain's standard lever taxonomy blended with AI-suggested initiatives specific to the target.  | **Thought partner**  | Initiative action list per sub-lever  |  |
| AI as a lever  |
| 20.1  | See AI-enabled opportunities called out explicitly  | Where AI is an enabler of a lever — not just a tool for the analysis — this is surfaced as a distinct tag or sub-lever within the relevant bucket.  | **Thought partner**  | AI enabler tag on opportunity card  |  |
| Sector KPIs  |
| 21.1  | See the KPIs and metrics most relevant to this sector  | Analysis surfaces a sector-specific KPI set mapped to the target's performance, not a generic financial summary.  | **Thought partner**  | Sector KPI panel  |  |
| 21.2  | Understand how levers map back to those KPIs  | Each lever is explicitly linked to the KPI it moves, so the partner can explain both the financial impact and the operational driver.  | **Radical transparency**  | Lever-to-KPI mapping  |  |
| 21.2  | Work from an agreed lever taxonomy  | The lever structure under each bucket — especially Operational Excellence — is aligned to Bain's standard taxonomy. To be confirmed with **Scott Daubin**  | **Partner judgment**  | Confirmed lever taxonomy pe  | To schedule a call with Scott  |
| Data export and workings  |
| 22.1  | Download peer data to review the workings offline  | Partner can export the full peer dataset — all companies, all metrics, and all adjustments made — as an Excel file or HTML table.  | **Partner judgment** **Radical transparency**  | Peer data export (Excel or HTML table)  |  |
| Onboarding guide  |
| 23.1  | Get up to speed on the tool quickly without needing a training session  | A lightweight in-tool onboarding guide  | **Thought partner**  | Onboarding walkthrough  | We have the concept design ready.  |
| TSR  |
| 24.1  | Understand the target's TSR performance as context for the opportunity  | Analysis surfaces the target's TSR trajectory vs. peers and vs. sector index Acts as a supporting exhibit that contextualises the urgency of the opportunity and strengthens the case for change narrative.  | **Radical transparency** **Thought partner**  | TSR performance chart vs. peer set  |  |
| 24.2  | See how TSR underperformance maps to specific operational gaps  | TSR underperformance is linked to the relevant levers in the analysis so the partner can explain why the stock is lagging and what the operational fix is.  | **Radical transparency** **Thought partner**  | TSR-to-lever linkage annotation  |  |
| 24.3  | Use TSR data to strengthen the activist defence or urgency narrative  | Where the Case for Change angle selected is activist defence or below-peer performance, the TSR exhibit is automatically promoted into the case for change narrative and the output deck.  | **Thought partner** **Partner judgment**  | TSR narrative integration into Case for Change  |  |
| 24.4  | See TSR in the context of the full peer set, not just as an isolated chart  | TSR chart shows all peers ranked, with Nike's position highlighted, so the relative underperformance is immediately legible without requiring explanation.  | **Transparency**  | Peer-ranked TSR comparison chart  |  |
| Credentials, expert search  |
| 25.1  | Find relevant Bain credentials for this sector and lever without leaving the tool  | Partner can search for Bain credentials by sector, capability, or lever type directly from the tool  | **Thought partner**  | Credential search via Sage  |  |
| 25.2  | Find the right Bain expert for this client conversation  | Partner can search for internal Bain experts by sector, capability, or lever so the right person can be pulled in before a first meeting.  | **Thought partner**  | Expert search via Sage  |  |
| 25.3  | Have the most relevant credentials surfaced automatically, not just on search  | Based on the sector tag, the target, and the levers selected, the tool proactively surfaces the top 3-5 most relevant Bain credentials without the partner needing to search.  | **Thought partner**  | Auto-surfaced credential recommendations  |  |
| 25.4  | Add a Bain credential directly into the output deck from the search results  | Partner can drag a credential slide from the search results directly into the deck builder, without needing to switch screens or manually locate the slide in the library.  | **Thought partner**  | Drag-to-deck from credential search results  |  |
| 25.5  | Know when a credential has already been used in a prior OI for this client  | Credential panel flags cases that have already been presented to this client in a previous engagement, so the partner avoids repeating materials the client has already seen.  | **Radical transparency**  | Prior presentation flag on credential slide  | Feasibility to be discussed  |
