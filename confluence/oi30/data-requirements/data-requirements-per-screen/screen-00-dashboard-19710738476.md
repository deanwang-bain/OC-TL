---
title: "Screen 00: Dashboard"
confluence_id: 19710738476
confluence_url: https://bainco.atlassian.net/wiki/spaces/OI30/pages/19710738476
version: 18
updated: 2026-08-26T13:08:18.246Z
---

# Screen 00: Dashboard

[View in Confluence](https://bainco.atlassian.net/wiki/spaces/OI30/pages/19710738476)

Home screen. The partner's project list — every OI they have created or collaborated on. OI 3.0 inverts the old model: instead of the partner receiving a finished deck at the end of a 48-hour handoff chain (Account team → OI COE → BCN India → LT → partner), the partner now governs from the front and agents execute beneath. The dashboard is where that governance begins — each OI card is a live project the partner can re-enter at any stage, not a static deliverable. For core APT partners, 20+ OIs per year is expected.

HTML file:

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

Company name

 |

User input

 |

Free text entry by Partner at OI creation. Triggers creation of a new OI record. Company name passed to Screen 01 where entity resolution runs automatically.

 |

Text input field shown at OI creation. Shown as card title on Dashboard after creation. Truncated with ellipsis if too long. Clicking the card opens the OI at Screen 01 with company name pre-populated.

 |

 System creates a new OI record on submission. Company name stored and passed to Screen 01. Entity resolution triggered automatically when Screen 01 loads.

 |
|

Sector

 |

System (OI record)

 |

Displayed from OI record. Populated automatically after Screen 01 entity resolution and Bain taxonomy mapping completes. Blank until Screen 01 is first completed.

 |

Shown as subtitle on Dashboard card. Blank or pending until Screen 01 completes. No input required from Partner on Screen 00.

 |

System reads sector from OI record and displays on card. No agent action on Screen 00 — company relevant sector is retrieved in Screen 01 and stored.

 |
|

Workflow stage (e.g. 'Peers', 'Analysis')

 |

System

 |

Ordinal: Target(0) → Peers(1) → Case(2) → Analysis(3) → Output(4). Stored in session/DB.

 |

Stage label shown on card. Colour or icon changes per stage. Clicking card resumes OI at correct stage.

 |

System stores current stage state per OI. On re-open, agent resumes workflow at last completed stage — does not refresh the system/peers/calculations from beginning.

 |
|

Progress bar %

 |

Derived

 |

(current_stage + 1) / 5 × 100. Caps at 100% when status = done.

 |

Visual progress bar on card. Colour changes to green when complete.

 |

Each stage within the user journey is assigned equal weight of completion (20%) and based on completion, calculation is displayed on the dashboard. no agent action required.

 |
|

Status (In progress / Complete)

 |

System

 |

Enum: active | done | draft | archived.

 |

Badge shown on each card. Colour-coded (e.g. amber = active, green = done).

 |

Status set to 'done' when Partner confirms Output stage. Draft status applied to OIs created/stored but not yet submitted through Target screen.

 |
|

Data vintage tag (e.g. 'FY25 Q1')

 |

CapIQ

 |

Most recent financial data period loaded for this OI. Derived from the latest data period loaded from CapIQ at time of target resolution. Allows Partner to quickly see how current the underlying data is without opening the OI.

 |

 |

 |
|

P&L size of prize ($M)

 |

Analysis output (Screen 04)

 |

Sum of all confirmed P&L lever point estimate values (cost and topline levers only). Shown as '—' until Analysis stage is complete. Displayed separately from Cash SoP.

*📎 Source: Email from Stephanie (executive sponsor)*

 |

Displayed on card separately from Cash SoP. '—' placeholder until Analysis is complete.

 |

Populated automatically when Partner confirms the case for change cards and proceeds for Analysis. Updates if Partner modifies levers within case for change — reflects latest confirmed P&L levers only.

 |
|

Cash size of prize ($M)

 |

Analysis output (Screen 04)

 |

Sum of all confirmed cash/NWC lever values (one-time liquidity release — not recurring savings). DIO + DSO + DPO opportunities aggregated. Shown separately from P&L SoP.

*📎 Source: Email from Stephanie (executive sponsor) + OI Data Dictionary v2*

 |

Displayed on card separately from P&L SoP. Clearly labelled as one-time cash release.

 |

Cash SoP represents one-time liquidity release, not recurring savings — confirmed by data dictionary. Agent populates from NWC lever outputs which is separate from the P&L.

 |
|

'Agent sizing…' placeholder

 |

System

 |

Shown in prize position when OI is in 'agent working' state — prize not yet calculated. Replaces P&L and Cash SoP with '—' and 'Agent sizing…' label with animated indicator.

 |

 |

 |
|

Estimated time remaining (e.g. '10 mins left')

 |

System

 |

Shown on card badge when OI is in 'agent working' state. Timer displayed next to 'Agent working' badge.

 |

 |

 |
|

Last updated timestamp

 |

System

 |

Timestamp of most recent action on the OI. Displayed as relative time (e.g. '2 min ago').

 |

Shown on card in relative time format. Updates on any save or action.

 |

when there is time passed (e.g. 90 days) where the fetched data becomes irrelevant, Agent needs to delete / achieve OI.

 |
|

Collaborator avatars

 |

User / permissions

 |

List of users with access. Initials derived from name. Max 4 shown, then +N overflow.

 |

Up to 4 avatar initials shown on card. +N shown for overflow. Clicking avatars opens share/permissions modal.

 |

Permissions model: Contributor vs Viewer. Confirm rules — RLS policies for what collaborators can see and edit.

 |
|

Year grouping divider (e.g. '2025')

 |

System

 |

Year of OI creation. Used to group cards: current year vs prior years.

 |

Divider label shown between year groups on the dashboard. Current year shown first.

 |

Agent flags the older OIs and achieves them, indicating it might need a refresh soon.

 |
|

Archive / hide toggle

 |

User input

 |

Partner can archive or hide OIs that are no longer active pursuits. Archived OIs hidden from main view but retrievable via filter or search.

*📎 Source: Email from Stephanie (executive sponsor)*

 |

Archive button available per card. Archived OIs accessible via 'Show archived' filter.

 |

System flags OI as archived. Hidden from default dashboard view. Agent does not surface archived OIs in active context.

 |
|

Search bar (filter OIs)

 |

User input

 |

Text input to filter visible OI cards by company name or sector. No-results state shown when no matches found. 📎 Source: HTML screen files

 |

 |

 |
|

⋯ card menu (Download / Share / Archive / Delete)

 |

User input

 |

Three-dot menu on each card. Options confirmed from HTML: Download , Share , Archive, Delete.

 |

 |

 |
