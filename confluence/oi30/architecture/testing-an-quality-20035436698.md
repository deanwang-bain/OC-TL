---
title: "Testing an Quality"
confluence_id: 20035436698
confluence_url: https://bainco.atlassian.net/wiki/spaces/OI30/pages/20035436698
version: 1
updated: 2026-11-12T13:07:17.784Z
---

# Testing an Quality

[View in Confluence](https://bainco.atlassian.net/wiki/spaces/OI30/pages/20035436698)

## QA Strategy

The goal of QA is to make sure we do not lose the quality achieved during GLS as Opportunity Catalyst continues to change.

We will use the golden companies as our regression baseline, validate deterministic calculations exactly, test AI outputs separately for quality and consistency, and automate the most important checks needed for future releases.

## 1. Purpose

QA will cover the complete OC journey:

Target → Peers → Case for Change → Size of Prize → Output

Chat is available throughout the journey.

Testing will cover both the visible user flow and the technical layers behind it, including Experience BFF, services, data, real-time events and AI agents.

The existing golden companies and known expected results will continue to be used as the regression baseline.

## 2. Main QA Objectives

- Protect the complete end-to-end journey.
- Protect calculation correctness.
- Protect saved state and refresh behaviour.
- Make sure important values and AI explanations are traceable to the correct source.
- Validate AI quality, grounding and consistency.
- Validate final deck/PPT/HTML output.
- Increase automation so QA does not need to manually validate every company.

## 3. Testing Approach

### Deterministic Testing

Examples:

- Peer count and selected peers
- Target exclusion
- Opportunity values
- Working-capital calculations
- Rounding
- API schemas
- State persistence
- Exported numeric values

These checks must match the expected result exactly.

### AI / Non-Deterministic Testing

Examples:

- Peer rationale
- Case for Change narrative
- Chat answers
- Recommended actions
- Executive/deck narrative

These will be evaluated for:

- Accuracy
- Grounding
- Completeness
- Relevance
- Consistency
- Hallucination

Exact wording is not required.

### Mixed Testing

Where deterministic numbers and AI explanations appear together, QA will validate the number/state exactly and evaluate the generated explanation separately.

## 4. Golden Regression

The existing golden companies remain the regression baseline:

- Adobe
- Carrier
- General Mills
- Beiersdorf
- Graphic Packaging
- Dow
- Adidas
- Honda

Golden regression will be used to validate calculations, user-flow behaviour, AI responses and generated output before important releases.

As the dataset grows, automated validation will cover the wider dataset while detailed manual review remains focused on golden companies and anomalies.

## 5. API, Contract and Integration Testing

QA will validate:

- BFF and service contracts
- Required fields and data types
- Invalid/malformed responses
- Case lifecycle and persistence
- Peer creation and duplicate prevention
- Target exclusion
- Real-time events
- Retry and reconnect behaviour
- Stale responses
- Concurrent changes
- Audit and evidence where applicable

Contract checks should be part of normal regression coverage.

## 6. UI and End-to-End Testing

UI automation will focus on critical journeys rather than automating every screen.

Main E2E flow:

Target → Peers → Case for Change → Size of Prize → Output

Additional checks include:

- Refresh persistence
- Navigation
- Real-time loading
- Chat/source behaviour
- Export smoke testing
- Error and empty states
- Important browser coverage

## 7. AI Safety

QA will include:

- Prompt-injection scenarios
- Documents containing malicious instructions
- Unsupported or unsafe tool use
- Grounding validation
- Agent actions performed only in the requesting user's context
- Audit/evidence for agent actions where supported

## 8. Automation Strategy

Automation will be added at the layer where behaviour can be proved most reliably:

- Contract/schema tests
- Service/API tests
- Data validation
- Cross-output reconciliation
- AI evaluation
- Critical UI E2E
- Browser coverage
- Visual/export checks

The goal is not to automate every screen, but to protect the calculations, state and service boundaries that drive OC.

## 9. QA Execution for New Tickets

For each new OC ticket QA will:

1. Understand which product journey is changing.
1. Identify the BFF/service/data/event/agent layers involved.
1. Select the relevant regression risks.
1. Choose appropriate test/golden data.
1. Separate deterministic and AI checks.
1. Run relevant exploratory scenarios.
1. Validate downstream impact.
1. Attach concise evidence and remaining risks.

## 10. QA Readiness and Sign-off

A story is ready for QA when:

- Acceptance criteria are testable.
- Required contracts are available.
- The agreed QA environment is available.
- Required test data exists.
- Developer smoke testing is complete.
- Known limitations are documented.

QA is complete when:

- Acceptance criteria pass.
- Relevant deterministic checks pass.
- Relevant AI evaluations meet the agreed threshold.
- Contract/integration/regression checks pass.
- No unresolved blocker or high-risk issue remains unless accepted.
- Jira/report contains evidence, defects and deferred risks.

## 11. Reporting

During active testing QA will provide:

- PR/CI results
- Golden regression results
- AI evaluation results
- Short daily status during active testing
- Pre-release QA summary

The release summary should clearly show what passed, known issues, deferred risks and whether the agreed QA gate is met.

## 12. Open Decisions

The following still need team agreement:

- Official post-GLS QA environment and deployment cadence
- Mandatory contract gates
- Business Unit rules
- Final peer/search limits
- AI evaluation thresholds
- Authoritative production data sources
- Audit/evidence requirements
- Trace/correlation access for QA
- Final release gate
- Supported browser matrix
- Golden-data storage location
- Final QA reporting ownership/cadence

This strategy should be updated as these decisions are finalised.

## References

The detailed original QA Test Strategy document is attached to this page for reference.
