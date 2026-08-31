---
title: "Design requirements & components"
confluence_id: 19627835552
confluence_url: https://bainco.atlassian.net/wiki/spaces/OI30/pages/19627835552
version: 5
updated: 2026-07-17T03:08:46.386Z
---

# Design requirements & components

[View in Confluence](https://bainco.atlassian.net/wiki/spaces/OI30/pages/19627835552)

16 July - Synthesized across all documents

- interviews with Danielle, Klaus, Charles, Timm, BCN
- Discussion with Noah
- Confirmation of the vision with Stephanie
- The VCC workshop

Based on the [Design Principles]design principles: **Partner judgment**, **Radical transparency**, **Thought partner**, **Modular flow**, **Co-creation**

| **#**  | **User need**  | **Design Requirement**  | **Design Principle**  | **Design Component**  | **Feedback**  |
|---|---|---|---|---|---|
|  1. Dashboard & portfolio   |  |
| 1.1  | See all my active OIs  | Show all active OIs with size of prize, stage, and last-updated timestamp  | **Modular flow**  | Portfolio grid cards  |  |
| 1.2  | Know which proj needs my attention  | Show clear status indicator (e.g., input needed)  | **Partner judgement**  | Status badge  |  |
| 1.3  | Start a new analysis  | Start a new proj  | **Modular flow**  | Entry point  |  |
| 1.4  | Be pulled back into the tool by what changed while I was away  | Dashboard mental model is a “feed” not a static workspace, frequency of updates to be evolved over time post-mvp  | **Thought partner**  | Feed, activity strip, signal notifications  |  |
|  1. Collaboration   |  |
| 2.1  | Share analysis with my team without rebuilding it  | Partner can invite collaborators to a project at the point of creation  | **Co-creation**  | Share / invite modal  |  |
| 2.2  | Work on the same OI with another partner simultaneously  | Collaborators can view and contribute to the same project simultaneously  | **Co-creation**  | Multi-user presence indicator  |  |
| 2.3  | Know who has touched what in a shared project  | Display who else is working on a project and what changes they have made  | **Co-creation**  | Change log / collaborator activity trail  |  |
|  1. Non-linear, modular nav   |  |
| 3.1  | Go back and adjust my peer set mid-analysis without losing my work  | Partner can return to any prior step and re-run only the affected modules  | **Modular flow** **Partner judgement**  | Non-linear module grid  |  |
| 3.2  | Instantly see which modules are done vs. still needed  | Completed modules are visually distinct from pending and blocked modules  | **Modular flow**  | Module state indicators (done / pending / blocked)  |  |
| 3.3  | Change audience framing without rebuilding the whole analysis  | Re-entry loops are targeted: changing audience re-weights narrative only; changing peers re-runs benchmarking only  | **Modular flow**  | Surgical rerun trigger on module edit  |  |
|  1. Gate system   |  |
| 4.1  | Know exactly what I need to do when the tool cannot proceed  | Hard gate blocks progress and provides a specific, actionable upload prompt (not a generic error)  | **Partner judgement** **Radical transparency**  | Hard gate block card with upload CTA  |  |
| 4.2  | Proceed with partial data while staying aware of the risk  | Soft gate allows analysis to proceed but surfaces a clear, persistent caveat flag  | **Partner judgement** **Radical transparency**  | Soft gate caveat flag / banner  |  |
| 4.3  | Never be confused about why I am stuck  | UI distinguishes hard-blocked, soft-proceed, and fully-resolved gate states visually  | **Radical transparency**  | Gate state visual system (red / amber / green)  |  |
|  1. Confidence score & actionable feedback   |  |
| 5.1  | Know how much to trust each opportunity before acting on it  | Every opportunity card and module shows a confidence score: High / Medium / Low  | **Radical transparency**  | Confidence badge on opportunity card  |  |
| 5.2  | Understand exactly why confidence is low and what is missing  | Confidence score is drillable, clicking shows which sources were used, which are missing, and what would raise the score  | **Radical transparency** **Thought partner**  | Confidence drill-down panel/ modal  |  |
| 5.3  | Get a specific prompt for what to upload to improve confidence  | When confidence is low, system surfaces a targeted upload prompt identifying the exact document type needed  | **Partner judgement** **Thought partner**  | Actionable confidence score with upload CTA  |  |
| 5.3b  | Upload a P&L when structured databases have no data on a company  | Provide a templated P&L upload as the primary fallback when external databases are insufficient. (The template shall be strict at MVP for accuracy, with progressive relaxation post-MVP to accept varied structures and document types)  | **Partner judgement**  | Templated P&L upload  |  |
| 5.4  | See confidence update live as I add data  | Confidence score updates dynamically when partner uploads documents or changes peers  | **Radical transparency** **Modular flow**  | Live confidence score recalculation  |  |
|  1. Peer set quality   |  |
| 6.1  | Understand why each peer was included in the set  | Suggested peer set shows the rationale for each peer (e.g., "Adidas — suggested by CapIQ + 10-K + past OI").  | **Radical transparency**  | Peer set card with source rationale  |  |
| 6.2  | Use the data source I trust most (TBD Post-MVP)  | Partner can set a data source preference (e.g., CapIQ vs. Crunchbase) per project or as a default  | **Partner judgement**  | Data source preference picker  |  |
|  1. Bain relationship context   |  |
| 7.1  | Know who at Bain owns this client before I start the analysis  | On target entry, tool surfaces Bain relationship data: billing partner, active cases, past OIs  | **Radical transparency** **Thought partner**  | Bain relationship context modal  |  |
| 7.2  | Use existing client context to inform peer selection and narrative  | Relationship context is an input to peer set and narrative framing, not just a read-only display  | **Thought partner**  | Relationship-informed peer and narrative inputs  |  |
| 7.3  | Access past case materials and selling decks without leaving the tool (TBD Post-MVP)  | Full Sage integration allows access to client heads, case materials, and selling decks in-context  | **Thought partner**  | Sage integration panel (Post-MVP)  |  |
|  1. Confidential document handling   |  |
| 8.1  | Know that sensitive client documents I upload stay within this project and go no further  | Uploaded confidential documents (CIM, internal P&L, client email chains, management memos) shall be scoped strictly to the project they are uploaded into and shall not persist beyond it or be accessible from any other project or user session  | **Radical transparency**  | Clearly indicate project-scoped document vault (no cross-project bleed)  |  |
| 8.2  | See exactly what the tool extracted from a confidential document (and what it ignored)  | After any document upload, the tool shall surface a clear ingestion confirmation showing: what was extracted and routed to which layer (context / financials / qualitative), what was not used and why, and the resulting confidence score change. Partner must be able to verify the extraction before the analysis proceeds  | **Radical transparency** **Thought partner**  | Document ingestion confirmation panel (extracted / routed / ignored)  |  |
| 8.3  | Remove or replace a confidential upload if I change my mind or uploaded the wrong file  | The partner shall be able to remove or replace any uploaded document at any point. Removal shall trigger a recalculation of confidence scores and flag any analysis that was dependent on the removed document  | **Partner judgement** **Modular flow**  | Document remove / replace control with downstream recompute  |  |
| 8.4  | Know when a citation in the deck is sourced from a confidential document, not a public one  | The tool shall visually distinguish citations sourced from confidential uploads vs. public data sources. When exporting the deck, the partner shall be prompted to review any slides that cite confidential material, so they can decide whether to include, paraphrase, or remove those references before sharing externally  | **Partner judgement** **Radical transparency**  | Confidential source badge on citations; pre-export confidential reference review  |  |
|  1. Transparency & source attribution   |  |
| 9.1  | Trace every number back to its source before putting it in front of a client  | Every data point, benchmark figure, and insight is linked to its source (CapIQ, IR page, analyst report, Bain experience)  | **Radical transparency**  | Inline source citation on data points  |  |
| 9.2  | See all the data sources powering my analysis in one place  | Display a "bibliography": a visible list of all active sources and documents in the current project  | **Radical transparency**  | Bibliography / source panel  |  |
| 9.3  | Track what I changed vs. what the agent recommended  | Partner overrides are logged and visible, original agent recommendation vs. what was changed is always surfaced  | **Radical transparency** **Partner judgement**  | Override change log  |  |
| 9.4  | Never accept an output I cannot interrogate  | Never present a conclusion the partner cannot drill into  | **Radical transparency**  | Full drill-down on all outputs  |  |
|  1. Persistent chat strip   |  |
| 10.1  | Challenge the agent's thinking at any point without leaving the screen  | Persistent chat panel is available across all layers, allowing the partner to question, challenge, or refine reasoning at any time  | **Thought partner** **Modular flow**  | Persistent chat strip  |  |
| 10.2  | Push back on the agent like I would push back on a consultant  | Chat behaves like querying a knowledgeable consultant, partner can ask for alternatives or request re-runs  | **Thought partner** **Partner judgement**  | Conversational challenge interface  |  |
| 10.3  | Edit the deck through conversation, not just by clicking (TBD post mvp)  | Chat remains live during deck editing, enabling natural-language commands to update slides  | **Thought partner**  | Chat-based deck editing  |  |
|  1. Opportunity module & deep dive   |  |
| 11.1  | Drill into any opportunity to see the full picture behind it  | Opportunities are expandable cards: clicking reveals insight, data sources, reasoning, confidence, and available actions  | **Partner judgement** **Radical transparency**  | Expandable opportunity card  |  |
| 11.2  | Refine, reorder, or remove individual opportunities based on my judgment  | Inside each module, partner can add sources, adjust hypothesis, reorder, promote/demote, or remove  | **Partner judgement**  | Opportunity module action controls  |  |
| 11.3  | Access the full longlist, not just the agent's top picks  | Full candidate list is accessible so partner can promote agent-ranked items  | **Partner judgement**  | Full candidate list view (expand beyond top X)  |  |
| 11.4  | Tell at a glance which items are agent-suggested vs. ones I promoted  | Display clearly distinguishes agent-recommended vs. partner-overridden opportunities  | **Partner judgement** **Radical transparency**  | Agent vs. partner-override indicator badge  |  |
|  1. Live case for change preview   |  |
| 12.1  | See how the case for change narrative is shaping up as I refine the opportunity list  | Surface a live case for change narrative preview, updating in real time or as triggered as the partner promotes, removes, reorders, or refines opportunity candidates. Reflect the current shortlist and framing at all times, so the partner can sense-check the story  | **Thought partner** **Partner judgement** **Radical transparency**  | Live case for change narrative preview  |  |
|  1. Anchor recommendation & size of prize   |  |
| 13.1  | See not just what the agent recommends, but why it chose that anchor and not another  | Anchor recommendation shows: chosen reference point, dollar figure, alternatives considered, and reasons each was rejected  | **Partner judgement** **Radical transparency**  | Anchor recommendation card with rejected alternatives  |  |
| 13.2  | Override the anchor with my own judgment and see the number update live  | Partner can switch reference point, peer, feasibility ceiling, or override distortion flag, each recalculates downstream live.  | **Partner judgement** **Radical transparency**  | Anchor override controls  |  |
| 13.3  | See one clear, defensible number that triangulates all the evidence  | Size of prize waterfall shows benchmarking math and Bain experience ranges converging to a single anchor value  | **Radical transparency**  | Size of prize waterfall visualisation  |  |
| 14. Deck assembly, QC, export  |  |
| 14.1  | Not be shown a deck with errors already in it  | Partner sees nothing until automated QC has run: catching orphan claims, number mismatches, conflicts of interest  | **Radical transparency** **Partner judgement**  | Pre-render QC gate  |  |
| 14.2  | Fix QC issues in context (TBD post mvp)  | QC flags surface inline on the relevant slide with the specific issue and suggested fix  | **Radical transparency**  | Inline QC flag on slide canvas  |  |
| 14.3  | Export to PowerPoint in Bain format ready to present  | Primary export is PowerPoint in native Bain Think-cell format  | **Co-creation**  | PowerPoint export  |  |
| 14.4  | Export to other formats e.g., HTML, memo (word doc)  | Alternative export options  | **Co-creation**  | Alternative export options selection  |  |
|  1. Post-export monitoring & feed (Post-MVP)   |  |
| 15.1  | Know when something in the market has changed my OI  | After export, tool monitors target company and peers in background for relevant signals  | **Thought partner**  | Background monitoring engine  |  |
| 15.2  | See a feed ranked by what actually matters to my active OIs  | Feed surfaces events ranked by their impact on active OIs — not a generic news stream.  | **Thought partner**  | Impact-ranked signal feed  |  |
| 15.3  | Get a morning summary of everything that changed across my portfolio  | Overnight digest summarises changes across all active projects since last login.  | **Thought partner**  | Overnight digest panel / email  |  |
| 15.4  | Reopen only the affected part of a project when a signal fires  | Significant feed events allow re-entry to re-run only affected modules from the relevant layer.  | **Thought partner** **Modular flow**  | Feed-triggered surgical rerun  |  |
| 15.5  | Be warned proactively about anomalies, not discover them after the fact  | Agent proactively surfaces outlier intelligence cards (e.g., peer COGS distorted by M&A event).  | **Thought partner** **Radical transparency**  | Intelligence / outlier card  |  |
| 16. Agent personality & tone of voice  |  |
| 16.1  | Talk to an agent that sounds like a Bain consultant, not a chatbot  | Agent communicates like a well-prepared, concise consultant: direct, precise business language, no hedging or filler.  | **Thought partner**  | Agent voice / response style guidelines  |  |
| 16.2  | Get the answer up front, not buried in a paragraph  | Agent leads with the answer first, then supporting reasoning: never buries the key number.  | **Thought partner**  | Answer-first response format  |  |
| 16.3  | Hear a clear, specific explanation when something looks off  | When flagging issues or outliers, agent tone is matter-of-fact and specific: states exactly what was found and why it matters  | **Thought partner** **Radical transparency**  | Outlier / flag messaging tone  |  |
| 16.4  | Get language tuned to whoever I am presenting to  | Agent adapts language register to audience context (CFO → P&L language; supply chain lead → operational language)  | **Thought partner**  | Audience-adaptive narrative generation  |  |
