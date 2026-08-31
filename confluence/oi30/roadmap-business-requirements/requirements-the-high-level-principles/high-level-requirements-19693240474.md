---
title: "High Level Requirements"
confluence_id: 19693240474
confluence_url: https://bainco.atlassian.net/wiki/spaces/OI30/pages/19693240474
version: 3
updated: 2026-08-05T13:36:23.708Z
---

# High Level Requirements

[View in Confluence](https://bainco.atlassian.net/wiki/spaces/OI30/pages/19693240474)

## What is OI3.0?

OI 3.0 will evolve the current 48-72 hour, expert-intensive Opportunity Indicator process beyond current analytical capabilities (both from a data processing and hypothesis generation perspective) with a partner-led, self-service and collaborative product that delivers a CEO-ready initial point of view in less than 30 minutes, while preserving expert judgement, traceability and enterprise controls.

## Requirements

**Partner self-service: **Enable Partners to launch a company assessment with minimal setup and without mandatory CoE involvement (though can be called upon and inserted into the process where more specificity or precision is needed).

**Answer-first experience: **Generate a synthesized, evidence-backed opportunities view rather than only displaying source data or charts.

**Rapid turnaround: **Produce an initial, CEO-ready assessment and editable output in approximately 30 minutes for standard use cases (timing less important than “feel” to maximize user adoption).

**18–24 month opportunity horizon: **Identify value creation opportunities that are relevant and realistically deliverable over the next approximately 18–24 months.

**Holistic answer across all value levers:** Provide a synthesized answer that sufficiently captures all levers available to a company, incl. revenue, stock price / enterprise value - NOT just cost. Should be inclusive and balanced between quantitative and qualitative assessment

**AI trust:** ensure the confidence level metrics and clear sources are always shared when analysis is prepared. No black boxes, human control and visibility.

**Integrated data foundation (scalable): **Combine Capital IQ, LSEG, analyst reports, IRIS/GLEAN and future sources such as Aura through an extensible connector framework.

**Modular AI answer design (scalable):** Enable a framework where SMEs can provide business logic / predefined skills (e.g., Claude) to deepen oustide-in, AI-generate answer within certain value areas to avoid deploying resources on nuanced use cases and being outpaced by cross-firm development [perhaps Andromeda will solve for us, but we should be ready to manage the integration on our end]

**User-uploaded data: **Allow users to upload structured and unstructured project or client data, including sensitive materials. With sensitive materials, must flag appropriately to shared users and in generated output

**Secure-by-default handling: **Classify, isolate, encrypt and govern data according to sensitivity, licensing, confidentiality and project access.

**No training on uploaded data: **Ensure Partner- or client-uploaded data is never used to train or improve foundation models.

**Partner-controlled sharing: **Let users decide whether content remains private or is shared with selected individuals, a project team, a workspace or a broader authorised audience.

**Collaboration: **Provide persistent project workspaces, shared editing, comments, mentions, tasking, review, approval, notifications and version history.

**Robust user management: **Support enterprise SSO, role-based access control, project/workspace administration, user groups, ownership transfer and full auditability.

**Peer selection and validation: **Recommend relevant peer sets, explain comparability, expose limitations, and require user review or approval before downstream analysis.

**Data standardisation: **Automate detection and treatment of reporting differences, non-recurring items, inconsistent cost bucketing and period mismatches.

**Manual correction and overrides: **Allow authorised users to correct source data, preserve the original value, capture rationale and history, and define refresh behaviour.

**Opportunity sizing: **Calculate value at stake using peer benchmarks, Bain experience, company context and explicit assumptions.

**Industry tailoring: **Apply sector-specific metrics, cost structures, adjustment logic and watch-outs for industries where standard P&L analysis is insufficient.

**Cost efficient industry scaling:**

- Design architecture of OI 3.0 **to scale across all industries** from the start (testing with selected one industry, clear path to **scale across all in cost efficient way**).
- Build a common core with industry-specific adaptations where needed (e.g., FS specific vs. Manufacturing/Energy close enough for model to learn)

**Natural-language investigation: **Allow users to ask questions, inspect evidence, refine assumptions, change benchmarks and customise the storyline through chat.

**Client-ready deliverables: **Generate editable PowerPoint and supporting outputs such as Executive Summary, Case for Change, Size of Prize, value levers, credentials and case studies.

**Living assessments: **Persist assessments as refreshable projects that highlight changes, preserve collaboration history and reconcile new source data with manual edits.

**Traceability and responsible AI: **Clearly distinguish sourced facts, calculations, AI synthesis, user-authored content and manual overrides, with source-level evidence.

**Scalable architecture: **design the OI3.0 for scale, ensure architecture allows to add new data sources easily, ensure the solid data foundations, ensure the calculations framework is robust and can be evolved in the future to deepen the analysis.

**AI Agents learning & adaptation: **with use of the system, ensure the AI is learning and deepening the knowledge.
