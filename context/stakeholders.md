# Stakeholders

Confirmed from
[Onboarding - StatusNeo](../confluence/oi30/ways-of-working/onboarding-statusneo-19640975400.md)
and
[Important Technology Contacts](../confluence/oi30/architecture/important-technology-contacts-19677053214.md).
Re-check against the mirror after a sync; this file is hand-maintained and drifts.

## Bain

Roles are from the team table on the [space home page](../confluence/oi30-19588841975.md).
Surnames are from the [VCC overview meeting](../confluence/oi30/meeting-summaries/vcc-overview-meeting-19696746551.md)
attendee list, the GitHub contributor lists shown in the 28 October workshop, and — for
Joanna — the photo filename on the home page.

| Name | Role | Reach via |
| ---- | ---- | --------- |
| Dean Wang | Tech Lead — owns this workspace | Teams |
| Kasia Mrowca | Product Manager | Teams |
| **Sandeep Uppal** | **Architect.** The "Bain architect" whose review ADR-001–009 await. Contributes Terraform to the infra repo directly. Ran the questioning in the 28 October workshop and stated several positions there (see [workshop notes](workshops/2026-10-28-system-and-data-architecture.md)) | Teams |
| Siva Vyra | Data Architect. Leads data structure "from day one", per the VCC meeting. Had no access to the core repo as of 28 October | Teams |
| Anand Kirori | DevOps. Contributor to both the core and infra repos | Teams |
| Angel | DevOps. Owner in the GLS deployment tracker. Surname not recorded anywhere | Teams |
| Joanna Soh | Design lead | Teams |
| Michelle Flood | Data Scientist | Teams |
| Raema | UX Designer | Teams |

**Sponsors:** Fritz, Stephanie and Noah. In the 28 October workshop, Stephanie and Noah were
named as the people to decide whether peer selection should force a business-unit or company
choice first.

Kick-off and vision are Kasia's agenda; UX discovery review is Joanna's; data overview
is Michelle's. See
[Meetings overview](../confluence/oi30/ways-of-working/meetings-overview-19618889880.md).

## Delivery partner

**StatusNeo (SN)** writes the OI 3.0 application code. This workspace reviews their
work; it does not contribute code to it.

### Sprint 4 planning attendees, 9 October

Read off the Teams roster in the recording — the planning sessions are the only
artefact naming who is actually in the room. Roles are not stated there, so only the
vendor markers below are from the source rather than inferred.

| Name | Noted as |
| ---- | -------- |
| Giorgi Samadashvili | Presenting — ran the backlog walkthrough |
| Dipesh Bhardwaj | Named throughout the GLS deployment tracker as decision-maker |
| Carter, Oliver | **(Vendor)** — the "Oliver" in story S4-52, peer selection sign-off |
| Bereznickis, Aleksandrs | **(Vendor)** |
| Lakshay Grover | |
| Nikolozi Metreveli | |
| Abhinav Upadhyay | |
| Mohammed Ashad Abbas | |

**Angel** appears in the deployment tracker as the DevOps owner but not in this
session. Surname not recorded anywhere in the mirror.

### Sprint 5 architecture workshop, 28 October

From the Teams roster in the recording. Dipesh Bhardwaj presented and organised. Sandeep
Uppal and Nikolozi Metreveli carry no vendor marker. **Abbas, Mohammed; Bereznickis,
Aleksandrs; Grover, Lakshay; and Samadashvili, Giorgi are all marked (Vendor)**, as is
Dipesh elsewhere in the same recording. The Sprint 4 table above lists three of them without
the marker, probably because that roster was truncated. Siva Vyra joined late.

The core repo has four contributors: Dipesh Bhardwaj, Anand Kirori, Aleksandrs Bereznickis and
Lakshay Grover. Nikolozi ("Nico") was named as the person who will work out how the analysis
steps differ by industry.

## System contacts

| Name | Role | System |
| ---- | ---- | ------ |
| Jason Barns | PM | VCC |
| Jon Allen | UI/UX | VCC |
| Zach Haris | TSG Infrastructure | MCP |

## Governance and security contacts

From the Tech Lead's Sage search, 2026-10-28. These are document owners or signatories, not
confirmed points of contact, so start with the team alias where one exists. Detail is in
[testing/standards-baseline.md](../testing/standards-baseline.md).

| Name or alias | Owns or signed | Use for |
| ------------- | -------------- | ------- |
| secAE@bain.com | TSG Security, Secure Design Principles contact | Security architecture questions, data classification confirmation |
| secrisk@bain.com (programme: John Clary, Security Risk & Compliance) | Penetration Testing Program | Booking the third-party pen test: 4–8 weeks lead time |
| Mark Waugh | Data Classification Standard v4.0, Data Handling Matrix | OpCat's classification tier |
| David Wiggs | Application Security standard | SAST, SCA and DAST gates; remediation SLAs |
| Gordon Morrison | SDLC Guidance, Hardening AI Applications | SDLC and scanning-tool questions |
| Jordi Price | Archie and the Innovation Enablement Process; public-endpoint requirements | Review process; the IEP workbook |
| Ed Moore | Approved Tools deck | Tool approvals, for example SonarQube |
| Manuel Scholz | Responsible AI page (Global Risk) | AI Data Governance Committee review |
| Ash Kanagat | Enterprise Architecture, Bain Application Framework review pack | Whether it is the same framework as ARC; the ARC owner |
| Sandeep Uppal | File owner of `AI_Architecture_Requirements v2.1` on the OI 3.0 site | Workbook provenance (storage owner, not necessarily the governing owner) |

## Upstream data systems

VCC, CapIQ, IRIS, LSEG, and Expert Search. Integration notes live under
[Data Sources summary](../confluence/oi30/data-requirements/data-sources-summary-19619676163.md).
Each is a separate integration with its own owner — identify the owner before raising a
data question.
