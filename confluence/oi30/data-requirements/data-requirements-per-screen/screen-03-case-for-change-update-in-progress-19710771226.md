---
title: "Screen 03: Case for Change (update in progress)"
confluence_id: 19710771226
confluence_url: https://bainco.atlassian.net/wiki/spaces/OI30/pages/19710771226
version: 8
updated: 2026-08-25T04:47:21.509Z
---

# Screen 03: Case for Change (update in progress)

[View in Confluence](https://bainco.atlassian.net/wiki/spaces/OI30/pages/19710771226)

Agent proposes 2–4 narrative angles for the CEO discussion. Partners want co-collaboration to shape framing — not a pre-determined answer. Each angle is backed by quantitative metrics and qualitative signals.

_[image: image-20260824-014521.png — not downloaded]_

| **Data Displayed**  | **Source**  | **Calculation / Logic**  | **UX / Interaction (Raema)**  | **Agent / System Behaviour (Nikolozi)**  |
| ⚠ *NOTE (Noah/Kasia meeting, Aug 11): TSR and some top-level, top-down data (Black/White/Grey) from VCC are reliable and can be used. Other financial metrics for Case for Change angles must come from raw CapIQ / OI 3.0 own calculations, not VCC-computed metrics*  |
| Narrative angle title (e.g. 'Below peers on profitability')  | Agent (LLM-generated)  | Agent proposes angles based on: target vs peer median gaps, TSR performance, qualitative signals from analyst reports and management commentary.  | Angle tile shown with title, framing, and key metric. Selectable via toggle or click.  | Agent generates 2–4 angles on entering screen. If Partner pushes back, agent re-generates angles. Agent invites reaction in chat — not just presenting a result.  |
| Key metric value (e.g. '3.1pp below peer EBITDA median')  | Derived (CapIQ + peer set)  | Gap = target metric − peer median.  | Displayed as headline metric on angle tile.  | Agent calculates gap from confirmed peer set (Screen 02). Values downstream of Screen 02 normalisation.  |
| Supporting sources (per angle)  | CapIQ / LSEG / Sage  | Financial data (CapIQ), analyst notes and earnings excerpts (LSEG), Bain IP (Sage). Each shown with icon, description, and extracted passage.  | Sources listed in angle detail. Each source drillable.  | Agent assembles supporting sources per angle. ⚠ LSEG-dependent sources unavailable if access unconfirmed.  |
| CEO / CFO qualitative quotes  | LSEG (earnings calls, annual reports)  | Key management quotes extracted by LLM. Qualitative signals as important as quantitative benchmarking.  | Displayed as pull-quotes with source label.  | Agent extracts and attributes quotes from LSEG transcripts. ⚠ LSEG access TBC.  |
| TSR vs sector (for activist angle)  | CapIQ  | Target 1Y/3Y TSR vs peer median TSR. Gap expressed as pp. TSR decomposition: Revenue + Margin + Leverage + Multiple + Dividends.  |  | Agent selects TSR angle when underperformance vs peers is significant. Gap threshold TBC with Nikolozi/SN.  |
| SG&A % vs peers (for cost angle)  | CapIQ + peer set (Screen 02)  | Target SG&A % − peer median SG&A %. Uses adjusted figures from Screen 02.  |  | Agent selects cost angle when SG&A gap is material. Gap threshold TBC with Nikolozi/SN.  |
| Selected angle(s)  | User input  | Partner selects 1 angle or combines 2. Stored and passed to Analysis as framing constraint.  | Selection persisted visually. Clear confirmation shown before proceeding.  | Selected angle(s) passed to Analysis as framing constraint. Non-linear: Partner can return and change — only affected downstream modules rerun.  |
| Chat panel (RAG-grounded)  | CapIQ (peer median gaps, TSR data) · LSEG (analyst excerpts, earnings call transcripts, CEO/CFO quotes) · Sage (Bain IP for angle support) · Peer set output (Screen 02)  | RAG retrieval scope for this screen: calculated peer median gaps per metric (from Screen 02 output), LSEG analyst excerpts and earnings call transcript passages relevant to the target and sector, CEO/CFO quotes extracted from annual reports, Bain IP assets from Sage that support or challenge each angle. Retrieval triggered by Partner query on a specific angle or metric.  | Persistent chat panel available throughout this screen. Partner can type at any point. Agent responses appear inline. Conversation history visible within session.  | Agent uses retrieved context to: explain the reasoning behind each proposed angle citing specific data gaps and qualitative signals, respond to Partner challenges and regenerate angles, clarify the metrics and sources behind a specific angle, accept Partner instructions to combine angles or weight a specific narrative direction. Responses grounded in retrieved LSEG content and peer gap calculations.  |
