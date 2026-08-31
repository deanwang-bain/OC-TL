# Stakeholders

Confirmed from
[Onboarding - StatusNeo](../confluence/oi30/ways-of-working/onboarding-statusneo-19640975400.md)
and
[Important Technology Contacts](../confluence/oi30/architecture/important-technology-contacts-19677053214.md).
Re-check against the mirror after a sync; this file is hand-maintained and drifts.

## Bain

| Name | Role | Reach via |
| ---- | ---- | --------- |
| Dean Wang | Tech Lead — owns this workspace | Teams |
| Kasia Mrowca | Product Manager | Teams |
| Sandeep Uppal | Architect | Teams |
| Joanna Soh | Designer | Teams |
| Michelle Flood | Tech Lead back-up | Teams |

Kick-off and vision are Kasia's agenda; UX discovery review is Joanna's; data overview
is Michelle's. See
[Meetings overview](../confluence/oi30/ways-of-working/meetings-overview-19618889880.md).

The [VCC overview meeting](../confluence/oi30/meeting-summaries/vcc-overview-meeting-19696746551.md)
splits the build in two: the data pipeline is Bain's, led by Sandeep and Siva; the AI
agent layer on top of it is StatusNeo's. Route a question to the side that owns the
layer it lands in.

## Delivery partner

**StatusNeo (SN)** writes the OI 3.0 application code. This workspace reviews their
work; it does not contribute code to it.

| Name | Role | Notes |
| ---- | ---- | ----- |
| Dipesh Bhardwaj | Architecture counterpart — Dean's opposite number | Architecture and platform questions come through him. Owns the CoE validation gate for the Andromeda integration scenario |

Giorgi Samadashvili, Nikolozi Metreveli and Siva Vyra appear throughout the meeting
summaries and screen specs — Nikolozi against agent and system behaviour, Siva against
VCC and LSEG access — but **the mirror never states which of them sit on which side**,
so their affiliation is unconfirmed here. Confirm before routing anything to them.

## System contacts

| Name | Role | System |
| ---- | ---- | ------ |
| Jason Barns | PM | VCC |
| Jon Allen | UI/UX | VCC |
| Zach Haris | TSG Infrastructure | MCP |

## Upstream data systems

VCC, CapIQ, IRIS, LSEG, and Expert Search. Integration notes live under
[Data Sources summary](../confluence/oi30/data-requirements/data-sources-summary-19619676163.md).
Each is a separate integration with its own owner — identify the owner before raising a
data question.
