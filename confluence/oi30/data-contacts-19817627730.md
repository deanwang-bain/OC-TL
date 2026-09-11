---
title: "Data Contacts"
confluence_id: 19817627730
confluence_url: https://bainco.atlassian.net/wiki/spaces/OI30/pages/19817627730
version: 1
updated: 2026-09-10T15:38:45.480Z
---

# Data Contacts

[View in Confluence](https://bainco.atlassian.net/wiki/spaces/OI30/pages/19817627730)

Abishek Soni - TSR Automation

Kritik Ajmani - Tech Team Lead, TSR

1. **Financial data & automation**

- **S&P MCP:** Primary route for financial data.
- **CapIQ / VCC:** Useful reference points for understanding calculations and expected outputs; VCC currently provides some of the strongest answers.

1. **10-K extraction**

- Current flow requires **three API steps per company**: search → identify/finalise the correct filing → download.
- Search can be filtered (e.g., filings from the last 3 months) and has good accuracy in identifying the correct document.
- Processing is **one company / document at a time**, with ~5–10 seconds per call and token-limit constraints. Limit per day: ~6,000 companies.
- Report structures vary significantly by **geography and sector**. US filings are relatively consistent, while EU/APAC introduce additional variation.
- Revenue extraction is easier; cost analysis is harder and often requires assumptions. Peer benchmarking similarly requires assumptions.

1. **Automation accuracy & lessons learned**

- Current approach works for individual cases but is **not yet repeatable at scale**.
- Accounting-rule changes, geography, sector differences and user-controlled assumptions make full automation difficult.
- Prompt design and extraction rules require further refinement.
- Team can share the existing framework and lessons learned to accelerate development.

1. **Technical follow-ups**

- Connect with **Kritik** on the technical implementation and API-call approach.
- Review prompts and extraction logic jointly with the team.
- Share the **API call details and access requirements** so the team can obtain access to the required APIs.
- Set up a **lessons-learned session** covering the existing 10-K automation approach and framework.
