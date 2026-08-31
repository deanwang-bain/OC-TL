---
title: "Screen 05: Output & Deck Builder (update in progress)"
confluence_id: 19710705698
confluence_url: https://bainco.atlassian.net/wiki/spaces/OI30/pages/19710705698
version: 10
updated: 2026-08-25T04:47:53.775Z
---

# Screen 05: Output & Deck Builder (update in progress)

[View in Confluence](https://bainco.atlassian.net/wiki/spaces/OI30/pages/19710705698)

Final screen. Agent assembles a CEO-ready PowerPoint. Three ways to add slides: pre-created Bain slides, Bain slides from Sage, and direct search. Partner can also ask agent in chat to build specific slides. Sticky notes is a preferred feature.

|

**Data Displayed**

 |

**Source**

 |

**Calculation / Logic**

 |

**UX / Interaction (Raema)**

 |

**Agent / System Behaviour (Nikolozi)**

 |
|

*⚠ OPEN DECISION: ThinkCell vs python-pptx — current OI process uses ThinkCell (Noah confirmed). *

 |
|

*⚠ Confirmed (UX workshop): Two export formats most relevant (PPTX + HTML). Sticky notes are confirmed priority.*

 |
|

⚠ *CONFIRMED (Noah/Kasia meeting, Aug 11): The deck should pull in existing Bain slides from Glean archives (not recreate them). System searches Glean, surfaces matching slide(s) for Partner to confirm and pull in as-is.*

 |
|

⚠ *CONFIRMED (Noah/Kasia meeting, Aug 11): Case study slides follow a templated three-panel structure: Situation, Complication, and Results. Three actual applicable case studies pulled dynamically from Glean each time.*

 |
|

⚠ *CONFIRMED (Noah/Kasia meeting, Aug 11): Read vs Write permission model for deck collaboration. When a collaborator changes an assumption, the Partner who made the original assumption should be notified. Multiple scenarios can be explored and branched before one is published as the confirmed version.*

 |
|

Slide selection (which slides to include)

 |

User input + Analysis output

 |

Standard OI slide loop: Cover, Exec Summary, Case for Change, SoP waterfall, SG&A deep dive, NWC, EV/EBIT(DA) uplift, Next Steps. Partner can add, remove, reorder.

 |

Slide sorter on left. Drag-and-drop reorder. Toggle to include/exclude.

 |

Default slide set generated from confirmed Analysis output. Changes to Analysis propagate to affected slides automatically.

 |
|

Pre-created Bain slides (from tool)

 |

System (pre-built templates)

 |

Standard OI deck slides pre-created based on analysis output. Mapped to OI deck template used by Cost Diagnostic COE.

 |

Slides shown in sorter. Template mapping exercise needed (confirm wtih Akhil/Noah?).

 |

Agent populates slide templates from Analysis data model. ⚠ Template mapping exercise needed — (confirm wtih Akhil/Noah?).

 |
|

Slide sorter — pre-built OI analysis slides available to add to deck. Default deck auto-loaded based on analysis output. Additional slides available in library to drag in as needed.

 |

OI record (Analysis output — slides populated from confirmed Screen 04 data)

 |

Slides pre-built from OI analysis output stored in OI record — NOT generated fresh on Screen 05. Agent auto-loads a recommended default set based on the analysis (e.g. cover, exec summary, case for change, size of prize, key cost levers, NWC, next steps). Additional slides available in the library for Partner to add as needed (e.g. cost bar breakdown, peer set overview, TSR, long list). Exact slide set varies by analysis — confirmed slide groups: Setup, Analysis, Appendix. Partner can drag any library slide into the deck or remove slides back to library.

 |

Default tab in Slide library left panel. Recommended slides auto-loaded in deck on screen entry. Additional slides shown in library. Each slide shown as thumbnail with title and meta description. Drag from library into deck or click + to add. Drag within deck to reorder.

 |

Agent auto-populates recommended deck from OI record on entering Screen 05. Slide selection based on analysis output — varies per OI. All slide content reads from OI record — does not recalculate. Agent message on load confirms deck structure and invites Partner to reorder or add.

 |
|

Bain IP slides from Glean archive

 |

Sage (Glean) Confirmed (Noah/Kasia meeting, Aug 11)

 |

Partner can search for specific Bain IP slides (e.g. APT programme performance slide) and pull them directly into the deck from Glean archives — without recreating them. Agent searches Glean, surfaces matching slide(s) for Partner to choose from. Partner confirms and the existing Bain slide is inserted as-is.

 |

Search bar to find specific Bain IP slides. Preview shown before adding. Partner confirms insertion.

 |

Agent executes Glean search on Partner instruction. Does not recreate existing slides — pulls them directly.

 |
|

Direct slide search (within tool)

 |

Sage (Glean)

 |

Search within Output screen. Less comprehensive than native Sage search.

 |

Search bar in slide library panel.

 |

Agent executes Sage search from within tool. Less powerful than native Sage — noted by Joanna.

 |
|

Agent-built slides (via chat)

 |

Agent (LLM-generated)

 |

Partner asks agent in chat to build a specific slide. Agent generates and adds to deck.

 |

Chat interface available throughout screen.

 |

Post-mvp: Agent generates slide from Partner prompt and inserts at selected position. Partner can request edits via chat. in the mvp: user downloads the powerpoint presentation and makes the changes.

 |
|

Case study slides

 |

Sage (Glean / Iris) Confirmed (Noah/Kasia meeting, Aug 11)

 |

Case study slides follow a templated three-panel structure: Situation, Complication, and Results. Three actual applicable case studies pulled dynamically from Glean each time — NOT hardcoded.

 |

Three-panel case study slide template: Situation | Complication | Results. Dynamic content pulled from Glean per analysis. Partner can replace or swap individual case studies.

 |

Agent queries Glean for the three most applicable case studies based on lever type, sector, and context. Populates three-panel template.

 |
|

Analysis slide content (metrics, charts)

 |

Analysis output (Screen 04)

 |

Slides populated from confirmed Screen 04 data. Same data model — not regenerated.

 |

Slides render confirmed Analysis data. Must be consistent with Screen 04.

 |

Agent uses same data model as Analysis. Lever changes propagate to Output slides automatically.

 |
|

Exec summary text

 |

Agent (LLM-generated)

 |

LLM synthesis: top 3 levers, total SoP, case for change angle, next steps.

 |

Editable text block. Partner can request rewrites via chat.

 |

Agent generates exec summary on entering Output screen. Regenerates if Partner changes levers in Analysis.

 |
|

TSR performance data

 |

CapIQ

 |

Target vs peer TSR across 1Y, 3Y, 5Y. Same data as Screens 02/03.

 |

 |

Must be consistent with Screen 02/03 — pulled from same data model.

 |
|

Revenue growth chart data

 |

OI record (loaded in Screen 02 + peer CAGR from Screen 02 output)

 |

Read from OI record — NOT re-fetched from CapIQ on Screen 05. Target revenue by year ($B) from Screen 01/04 baseline. Target CAGR vs peer median CAGR (FY19–FY24) from Screen 02 peer output. Same figures as used in Screen 02 and Screen 04 — must be identical.

 |

 Revenue growth chart shown on relevant slide. Same data as Screens 02/04.

 |

Agent reads from OI record. Does not re-fetch from VCC/CapIQ. Same figures as Screen 02 peer comparison and Screen 04 baseline — must be identical.

 |
|

SG&A peer benchmark chart data

 |

CapIQ + peer set (Screen 02)

 |

SG&A % for target vs each peer. Adjusted figures. Must match Screen 04 lever data.

 |

 |

Must use same adjusted figures as Screen 04. Agent pulls from same data model.

 |
|

EV/EBIT(DA) uplift waterfall

 |

OI record (Screen 04 lever outputs)

 |

Read from OI record — NOT recalculated on Screen 05. EV uplift = Confirmed EBITDA improvement (Screen 04 P&L levers) × EV/EBITDA multiple (VCC, consensus NTM basis). Both values already in OI record — no new data fetch needed. Low/high end scenarios use low/high Bain Experience range from Screen 04

 |

Scenario toggle on slide: low / high end.

 |

Agent renders EV uplift waterfall from Analysis lever values. Scenario toggle synced with Analysis screen.

 |
|

Cost bar sub-breakdown slide

 |

Analysis output (Screen 04)

 |

OI record (Screen 04 cost bar sub-breakdown output).Slide showing cost bar sub-breakdown by category with Bain Experience ranges. Where reported, use reported. Where inferred, show assumption label.

 |

Assumption label shown where data is inferred.

 |

Agent populates slide from cost bar sub-breakdown agreed in Analysis. Partner-adjusted assumptions reflected.

 |
|

Source footnote (per slide)

 |

Derived

 |

Auto-generated from data sources used in that slide. Confidence label shown.

 |

Auto-populated on each slide. Partner can edit.

 |

Agent generates source footnote from data provenance log. Updates if slide content changes and references to the source documents.

 |
|

Sticky notes (colour-coded by user)

 |

User input

 |

Partner and collaborators can add sticky notes to any slide. Colour-coded by user. Confirmed priority feature.

 |

Sticky note overlay on slides. Tap/click to add. Colour = user identity.

 |

Multiple users can add sticky notes simultaneously. Notes persisted per slide per user. Colour assigned by system based on user identity.

 |
|

Deck collaboration & versioning

 |

Confirmed (Noah/Kasia meeting, Aug 11)

 |

Read vs Write/Edit permissions at deck level (not line-by-line). When a collaborator changes an assumption, the original Partner should be notified / see that numbers have changed. Multiple scenarios / versions can be explored and branched before one is published as the confirmed version.

 |

Edit mode for assumption changes. Published version clearly marked. Notification when collaborator changes Partner's assumptions.

 |

System maintains version history. Collaborator actions recorded in Log tab. Published version = confirmed output for export.

 |
|

Deck metadata (target, date, methodology)

 |

System + Analysis output

 |

Cover page and footer: target company, analysis date, peer count, benchmarking approaches used, methodology note.

 |

Auto-populated on deck generation.

 |

Agent populates metadata from Analysis output on deck generation. Updates if Analysis changes.

 |
|

Export file

 |

System

 |

Two formats most relevant: PPTX + HTML). Current OI process uses ThinkCell.

 |

Download button. Format options shown.

 |

⚠ ThinkCell vs python-pptx decision needed urgently. Export triggered on Partner confirmation.

 |
|

Chat panel (RAG-grounded)

 |

Analysis output data model (Screen 04) · Sage slide library (Bain cases, benchmarking slides) · Source footnotes per slide · Exec summary content · Deck metadata

 |

RAG retrieval scope for this screen: full confirmed Analysis output data model (lever values, peer benchmarks, SoP total, EBIT bridge), Sage slide library indexed by sector, topic, and lever type, source footnotes and data provenance per slide, exec summary draft and slide text. Retrieval triggered by Partner slide request or question — relevant slides from Sage ranked by relevance and passed as context for agent to suggest or insert.

 |

Persistent chat panel available throughout this screen. Partner can type at any point. Agent responses appear inline. Conversation history visible within session.

 |

Agent uses retrieved context to: add, edit, or remove slides on Partner instruction using Analysis data model, rewrite exec summary or slide text on request grounded in confirmed Analysis output, search Sage slide library and suggest relevant Bain slides, answer questions about why a specific number appears on a slide by referencing source footnote, make final narrative adjustments before export. All slide content grounded in Analysis data model — not re-derived.

 |
