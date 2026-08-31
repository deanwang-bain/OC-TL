---
title: "Agent_Validation_Test_Plan"
confluence_id: 19765133323
confluence_url: https://bainco.atlassian.net/wiki/spaces/OI30/pages/19765133323
version: 1
updated: 2026-08-26T07:22:48.250Z
---

# Agent_Validation_Test_Plan

[View in Confluence](https://bainco.atlassian.net/wiki/spaces/OI30/pages/19765133323)

**AGENT VALIDATION**
**TEST PLAN**

**Opportunity Indicator 3.0**

*Expanded “speaking document” edition*

| **Core test philosophy** Two tracks are required because the architecture intentionally combines deterministic components with probabilistic agent/model behavior. Deterministic boundaries are proven with exact assertions; probabilistic behavior is evaluated through structural invariants, quality metrics, distributions, regression baselines and human judgement. The strategy therefore measures quality without turning natural model variation into false test failures.  |

| **Document field**  | **Value**  |
| Document purpose  | Define the complete test strategy, coverage model, measurements, tooling, execution model, non-functional strategy and release evidence for validating agents.  |
| Primary focus  | Agent orchestration, tool use, evidence/trace integrity, groundedness, faithfulness, deterministic calculation boundaries, regression, security, auditability, performance and operational quality.  |
| Source basis  | Attached Opportunity Indicator 3.0 Testing Architecture and the existing Agent Validation Test Plan.  |
| Intended use  | Release-governing reference (“Bible”) for planning, execution, coverage reporting, triage and sign-off.  |
| Status  | Updated draft for architecture/test-strategy review.  |
| Governance note  | Where the source architecture does not prescribe a numeric threshold or owner, this document defines a practical measurement method and marks the actual release threshold/owner for approval rather than silently inventing policy.  |

# 1. Executive summary

This document converts the supplied testing architecture into a test plan that can be executed, measured and governed. It explains what is tested, why it is tested, how coverage is derived, which tools are used, how non-functional requirements are validated, how quality is measured, and how evidence flows into release decisions. The objective is not merely to list tests; it is to make every test layer traceable to an architectural responsibility, business risk, user journey, tool contract, trust boundary or quality characteristic.

The strategy is risk-based and traceability-driven. Coverage is established by decomposing the architecture into testable capabilities, mapping each capability to functional and non-functional risks, identifying applicable test levels, defining measurable assertions, and linking them to automated suites or human evaluation. A feature is not considered covered because “a test exists”; it is considered covered only when its required behaviors, failure modes and relevant quality attributes are represented and the corresponding evidence is measurable.

| **What “coverage” means here** Coverage is multi-dimensional. Code coverage is useful only for deterministic unit logic. Agent quality needs requirement/capability coverage, tool and contract coverage, journey coverage, risk coverage, invariant coverage, golden-dataset coverage, adversarial coverage, NFR coverage and audit/trace coverage. No single percentage is sufficient on its own.  |

# 2. Purpose, scope and quality objectives

The plan validates the agent-enabled system across deterministic and probabilistic behavior while protecting the deterministic calculation boundary highlighted in the architecture. The system is considered release-ready only when blocking functional, evaluation, security, auditability and NFR criteria are satisfied for the change being released.

## 2.1 In scope

- Agent orchestration, stage progression and state transitions, including successful, retry, fallback and failure paths.
- Tool selection, tool-call arguments, typed contracts, authorization boundaries, response handling, retries and failure behavior.
- Claims, evidence bindings, figures, calculation traces and adjustment authorities produced or referenced by an agent.
- Groundedness and faithfulness of model-assisted claims and narratives.
- Peer-set selection, opportunity ranking, claim extraction and other golden-dataset regression measures.
- Calculation engine determinism, cycle rejection, unit/currency invariants, golden fixtures and trace replay.
- Frontend/service/data integration used by the agent journey. Deployment and infrastructure-as-code validation are owned by the deployment/platform team and are outside QA MVP scope.
- End-to-end journeys including stage progression, drill-down, assistant actions, export and collaborator flows.
- Actor attribution in the audit trail for user, system and agent actions.
- Security and adversarial resistance: prompt injection, jailbreak, exfiltration, tool abuse, application and supply-chain security.
- Cross-format fidelity across HTML, PDF and presentation outputs.
- Non-functional quality: accessibility, performance, resilience, reliability, observability and operational readiness.

## 2.2 Boundaries

Production documents must not be copied into test environments because uploads may contain MNPI or PII. Functional tests use synthetic companies, integration tests use recorded source responses, the golden evaluation uses a pinned source snapshot, and warehouse validation uses masked subsets. Human-review thresholds, exact statistical quality thresholds and ownership assignments must be approved as governance decisions; the measurement mechanisms are defined here so those values can be inserted without changing the strategy.

MVP protocol and deployment boundary: The calculation engine uses plain REST over HTTP. gRPC/Protobuf and buf are excluded from MVP testing. Terraform, Bicep, PSRule and Checkov are also excluded because deployment/IaC validation is owned by the deployment/platform team. These items will be added only if QA scope changes later.

## 2.3 Test objectives

| **ID**  | **Objective**  | **What success means**  |
| OBJ-01  | Structural integrity  | Every claim has evidence, every figure has traceability, adjustments name authority and metric references resolve.  |
| OBJ-02  | Agent correctness  | The agent follows the intended stage flow, chooses valid actions/tools and handles errors without fabricating success.  |
| OBJ-03  | Groundedness and faithfulness  | Claims are supported by source passages and narrative remains faithful to the analysis it summarizes.  |
| OBJ-04  | Regression safety  | Prompt, tool or model changes do not cause unacceptable degradation against approved golden baselines.  |
| OBJ-05  | Deterministic defensibility  | Pinned inputs and definition versions reproduce figures exactly; invariants hold across calculation paths.  |
| OBJ-06  | Security  | Gateway and application controls resist prompt injection, jailbreak, exfiltration and tool abuse.  |
| OBJ-07  | Auditability  | Every tested action is attributable to user/system/agent and initiating user is retained alongside agent actions.  |
| OBJ-08  | Operational quality  | The system remains accessible, performant, resilient and observable within approved NFR bands.  |
| OBJ-09  | Coverage transparency  | Every in-scope capability and high/critical risk maps to test evidence and a measurable coverage status.  |

# 3. Architecture reference and testing principles

The supplied architecture explicitly states that a conventional single test pyramid is not sufficient. The probabilistic layer sits inside the product rather than only at the top of the test stack, so model/agent behavior requires a different assertion model. The calculation engine remains deterministic on purpose and is therefore expected to receive exhaustive exact testing.

_[image: att_0_for_19765133323.png — not downloaded]_

Figure 1 — Supplied Opportunity Indicator 3.0 testing architecture used as the source for this plan.

| **Principle 1 — protect deterministic boundaries** If the same inputs and pinned definition versions should produce the same result, use exact assertions. A mismatch is a defect, never a model fluctuation. This applies especially to calculation logic, data constraints, contracts and infrastructure policy.  |

| **Principle 2 — evaluate probabilistic behavior** For agents and models, do not assert exact sentences. Assert structural invariants, judge groundedness/faithfulness, compare distributions and golden baselines, and use human review for the residual question of whether the output is actually useful.  |

| **Principle 3 — traceability is a quality property** Every claim, figure and action must be explainable after execution. Evidence bindings, calculation traces and actor attribution are therefore test assertions, not optional logging.  |

# 4. Overall test strategy

The test strategy uses seven complementary strategies. Together they provide breadth (all capabilities and risks), depth (multiple test levels), and release confidence (blocking gates plus trend-based evaluation). Each strategy has a different purpose; substituting one for another creates blind spots.

| **Strategy**  | **What it validates**  | **Primary assertion style**  | **Primary tools**  |
| 1. Deterministic verification  | Frontend/service logic, REST contracts, calculation engine and data rules.  | Exact expected result, schema/property assertion, invariant.  | Vitest, Testing Library, pytest, Hypothesis, Schemathesis, dbt.  |
| 2. Agent functional validation  | Orchestration, state transitions, tool selection/calls, retries/fallbacks, user-visible actions.  | Expected state/action/contract and safe failure behavior.  | Vitest/pytest, MSW, Testcontainers, Playwright.  |
| 3. AI quality evaluation  | Groundedness, faithfulness, peer set, ranking, extraction quality.  | Judge score, overlap/recall/ranking metrics, baseline comparison.  | Foundry Evaluations, golden dataset, analyst rubric.  |
| 4. Integration and E2E  | System behavior across services, data stores, sources, UI, exports and collaboration.  | Scenario outcome plus evidence/audit assertions.  | Testcontainers, recorded responses, Playwright.  |
| 5. Security/adversarial  | Application security and AI-specific attack paths.  | Blocking security controls and red-team findings.  | CodeQL, SonarQube, Dependabot, secret scan, Trivy, ZAP, Defender for Cloud, PyRIT, injection corpus.  |
| 6. NFR validation  | Accessibility, performance, resilience, reliability, observability and format fidelity.  | Threshold/SLO, recovery expectation, telemetry assertion, visual/structural comparison.  | axe-core, k6, Azure Load Testing, Playwright, logs/traces/metrics, PDF rasterization.  |
| 7. Human assurance  | Business usefulness and nuanced output quality not fully capturable by automation.  | Structured analyst rubric and sampled review.  | Analyst review workflow / scorecard.  |

## 4.1 Test design techniques

- Risk-based testing: prioritize P0/P1 flows, trust boundaries, irreversible actions and defects with client/financial/audit impact.
- Equivalence partitioning and boundary-value analysis: apply to deterministic inputs, limits, data ranges, time windows and contract fields.
- State-transition testing: cover allowed and disallowed agent stage transitions, retries, fallback, cancellation and resume behavior.
- Decision-table testing: cover tool routing, permissions, source availability, confidence/threshold decisions and error handling combinations.
- Pairwise/combinatorial testing: reduce combinations across model/tool/source/role/environment configurations while retaining interaction coverage.
- Property-based testing: generate broad calculation and API input spaces to expose cases not represented by hand-written examples.
- Golden-set regression: compare probabilistic behavior against analyst-approved reference cases and approved baselines.
- Adversarial testing: deliberately inject malicious instructions, contradictory evidence, malformed tool responses and unauthorized action attempts.
- Exploratory testing: focus on emergent agent behavior, unusual conversation context, ambiguous instructions and multi-step recovery paths.
- Trace replay: prove re-derivability of completed calculations using stored trace plus pinned versions.

# 5. Coverage model — how coverage is identified

Coverage is derived systematically from the architecture instead of being estimated from the number of test cases. The following process is mandatory for every release scope. It ensures that the team can explain why a capability is covered and can identify gaps before execution begins.

1. Create a capability inventory from architecture components and user journeys: frontend assistant, services, calculation engine, data, model/evaluation layer, security controls, export/renderers and audit trail. Deployment and infrastructure-as-code capabilities are excluded from QA MVP coverage unless scope changes.
1. Decompose each capability into positive behavior, negative behavior, boundary conditions, failure modes and authorization/trust-boundary concerns.
1. Link each item to requirements/acceptance criteria, architecture decisions, contracts, data rules and NFRs.
1. Assign risk based on business impact, likelihood, detectability and recoverability. Critical/high risks require explicit test evidence.
1. Select applicable test levels and techniques. A high-risk capability should normally have lower-level deterministic checks plus integration/E2E or evaluation evidence where applicable.
1. Identify the test data and environment needed to make the behavior reproducible.
1. Map the item into the traceability/coverage matrices and link it to automated suite IDs, evaluation cases or human-review rubrics.
1. Calculate coverage metrics and review uncovered P0/P1 items before release. Coverage is accepted only when exclusions are documented and approved.

## 5.1 Coverage dimensions

| **Coverage dimension**  | **Definition**  | **How it is measured**  | **Target principle**  |
| Requirement / acceptance coverage  | Whether every in-scope requirement or acceptance criterion has test evidence.  | Covered requirements ÷ in-scope requirements × 100.  | 100% for release scope; explicit approved exclusions only.  |
| Capability coverage  | Whether each architectural/agent capability has positive, negative and failure-path validation.  | Capabilities with required scenario classes ÷ in-scope capabilities × 100.  | 100% of P0/P1 capabilities.  |
| Risk coverage  | Whether identified risks have mitigating tests and evidence.  | Risks with at least one effective test/control assertion ÷ total in-scope risks × 100.  | 100% critical/high risks.  |
| Tool/contract coverage  | Whether every agent-callable tool and contract path is validated.  | Tools with success + invalid input + authorization + failure handling tests ÷ in-scope tools × 100.  | 100% release-scope tools.  |
| Journey coverage  | Whether priority user journeys and state transitions are exercised.  | Covered journey/state edges ÷ planned journey/state edges × 100.  | 100% critical journeys and stage transitions.  |
| Invariant coverage  | Whether every structural invariant is asserted where it can occur.  | Implemented invariant assertions ÷ defined invariants × 100.  | 100%; invariant failure is not tolerated.  |
| Golden-dataset coverage  | Whether important agent output patterns are represented in the reference corpus.  | Covered intent/theme/source/risk buckets ÷ planned buckets; plus case count trend.  | Risk-balanced; gaps reviewed before release.  |
| Adversarial coverage  | Whether known threat classes and attack surfaces are represented.  | Threat classes/corpus categories covered ÷ in-scope threat classes × 100.  | 100% named threat classes; corpus grows continuously.  |
| NFR coverage  | Whether each applicable quality attribute has scenarios and measurable thresholds.  | NFRs with defined scenario + measurement + threshold ÷ applicable NFRs × 100.  | 100% applicable P0/P1 NFRs.  |
| Code coverage (deterministic only)  | Execution of deterministic code by unit/component tests.  | Statement/branch/function coverage from test runners.  | Supporting metric, not a proxy for agent quality.  |
| Trace/audit coverage  | Whether agent actions and generated artifacts are attributable/re-derivable.  | E2E steps with expected audit/evidence assertions ÷ auditable steps × 100.  | 100% critical actions/figures/claims.  |

# 6. Coverage matrices

The matrices below are the operational mechanism for proving coverage. They should live as maintained artifacts in the QA repository or test-management system and be updated as requirements, agents, tools and risks evolve.

## 6.1 Requirement / capability traceability matrix

| **Capability / requirement**  | **Key risks**  | **Required test evidence**  | **Coverage status**  |
| Agent stage progression  | Wrong state, skipped approval, loop/stall.  | State-transition unit tests + integration + Playwright critical journeys + audit assertion.  | Measured per release.  |
| Tool selection and execution  | Wrong tool, wrong args, unauthorized action, fabricated success.  | Routing/contract tests + negative/permission tests + failure injection + E2E.  | Measured per tool.  |
| Claims and evidence  | Unsupported or orphan claim.  | Structural invariant + groundedness judge + golden claim cases.  | 100% invariant; quality trend.  |
| Figures and calculations  | Wrong number or unreproducible figure.  | Golden fixtures + Hypothesis properties + trace replay.  | Exact pass required.  |
| Peer/opportunity generation  | Quality drift after prompt/model change.  | Golden overlap/ranking/recall regression + human sample.  | Threshold-based.  |
| Exports/renderers  | Format divergence or stale content.  | Cross-format scenario + screenshot/PDF raster comparison + semantic checks.  | Per changed renderer/composition.  |
| Audit trail  | Missing actor/initiator or incomplete lineage.  | Audit assertion in every E2E action.  | 100% critical actions.  |
| Trust boundaries  | Public access, secret/network misconfiguration.  | Application security and authorization tests; deployment/IaC controls owned by deployment/platform team.  | Blocking.  |
| Prompt/content safety  | Instruction hijack through upload/retrieval.  | Curated injection corpus + gateway validation + PyRIT.  | All named threat shapes.  |
| Accessibility/performance  | Unusable UI or excessive wall-clock time.  | axe-core + k6/Azure Load Testing.  | Release thresholds.  |

## 6.2 Test level / tool / cadence matrix

| **Test level**  | **Coverage focus**  | **Tooling**  | **Cadence**  | **Gate**  |
| Unit / component  | Assistant client behavior, service domain logic, deterministic functions.  | Vitest + Testing Library; pytest/Vitest.  | Every PR.  | Blocking.  |
| Contract  | REST/OpenAPI compatibility and schema/property behavior.  | Generated clients, Schemathesis.  | Every PR / contract change.  | Blocking.  |
| Integration  | Wire-level client behavior and real SQL Server/Redis/Azurite substrates.  | MSW, Testcontainers, recorded responses.  | Merge to main.  | Blocking.  |
| Calculation  | Properties, golden fixtures, trace replay.  | Hypothesis, pinned fixtures, replay harness.  | Merge + nightly.  | Blocking for merge fixtures; replay alerts/escalates.  |
| E2E  | Stage progression, agent actions, export/collaboration, audit attribution.  | Playwright.  | Staging.  | Blocking.  |
| AI evaluation  | Groundedness/faithfulness per run; offline golden regression on changes.  | Foundry Evaluations + golden dataset.  | Run-time/change/nightly.  | Release-governing.  |
| Security  | Static/supply-chain, DAST, AI red team, injection corpus.  | CodeQL, SonarQube, Dependabot, secret scan, Trivy, ZAP, Defender, PyRIT.  | PR/nightly/release/change.  | Blocking per architecture gate.  |
| NFR  | Accessibility, performance, resilience, observability, fidelity.  | axe-core, k6/Azure Load Testing, Playwright, telemetry assertions.  | Staging/nightly/pre-release.  | Blocking for release-defined thresholds.  |

## 6.3 Agent/tool coverage matrix template

For every tool the agent can call, the matrix must contain at least the following scenario classes. This makes tool coverage measurable rather than relying on a single happy-path test.

| **Tool / action**  | **Happy path**  | **Invalid args/schema**  | **Auth / permission**  | **Timeout / 5xx**  | **Partial / malformed result**  | **Retry / fallback**  | **Audit**  |
| <tool name>  | Required  | Required  | Required  | Required  | Required where possible  | Required if supported  | Required  |
| Source retrieval  | ✓  | ✓  | ✓  | ✓  | ✓  | ✓  | ✓  |
| Calculation invocation  | ✓  | ✓  | ✓  | ✓  | ✓  | ✓  | ✓  |
| Export/composition  | ✓  | ✓  | ✓  | ✓  | ✓  | As designed  | ✓  |

## 6.4 Risk coverage matrix

| **Risk class**  | **Example failure**  | **Primary tests**  | **Coverage measure**  | **Release rule**  |
| Financial / calculation  | Incorrect opportunity figure.  | Golden fixtures, property tests, trace replay.  | 100% planned deterministic cases + exact replay pass.  | Blocking.  |
| Evidence / hallucination  | Claim not supported by source.  | Structural invariant, groundedness judge, golden claims.  | Invariant 100%; judge score/baseline.  | Blocking if invariant; threshold for quality.  |
| Agent control  | Wrong/unauthorized tool action.  | Tool contract, auth negatives, adversarial, E2E.  | 100% in-scope tool permissions and critical actions.  | Blocking.  |
| Security/privacy  | Prompt injection or protected-data exposure.  | Injection corpus, PyRIT, CodeQL/SonarQube/ZAP/Trivy.  | Named threat classes + finding severity.  | No unresolved release-blocking finding.  |
| Auditability  | Missing actor/trace/evidence.  | Audit assertions + trace replay.  | 100% critical actions/artifacts.  | Blocking.  |
| Reliability  | Timeout, retry loop, partial dependency failure.  | Failure injection, bounded retries, fallback tests.  | Critical failure modes represented.  | Threshold/SLO based.  |
| User experience  | Broken accessibility or long latency.  | axe-core, Playwright, load/performance.  | Route coverage + latency/wall-clock percentiles.  | Threshold based.  |

# 7. Detailed test strategies

## 7.1 Agent functional and orchestration strategy

The agent is tested as a stateful workflow, not as a text generator. Tests assert the state entered, the action chosen, the tool invoked, the arguments produced, the response handling and the resulting next state. The suite must cover normal progression as well as retry, fallback, cancellation, unavailable dependency, duplicate response, stale context and invalid-transition paths. State-transition coverage is maintained as a graph: each allowed critical edge must have at least one positive scenario and each prohibited high-risk edge must have at least one negative scenario.

Primary tooling: Vitest/pytest for orchestration logic, MSW for frontend network boundaries, Testcontainers for realistic service substrates, and Playwright for full user-visible journeys. Exact response wording is not used as a pass condition unless the text itself is deterministic product copy.

## 7.2 Tool and contract strategy

Every agent-callable tool is treated as an externalized capability with an explicit contract. Validation covers tool discovery/availability, schema compatibility, argument typing, required/optional fields, authorization, invalid values, timeout/5xx behavior, malformed/partial responses, retries, fallback behavior and audit emission. The required coverage matrix in section 6.3 must be completed for each tool in release scope.

The MVP calculation engine and agent-facing service contracts use plain REST over HTTP; gRPC/Protobuf validation is not part of the MVP scope. OpenAPI-generated clients provide compile/build-time safety where applicable, and Schemathesis performs property-based REST API fuzzing and schema validation. Tool failures are deliberately injected to verify that the agent does not fabricate success or silently continue with invalid state.

## 7.3 Evidence, retrieval and grounding strategy

Any claim extracted or generated from source content must remain linked to evidence. Structural tests first assert the absolute properties—evidence binding exists, references resolve, figures have traces. Runtime evaluation then measures whether the evidence actually supports the claim. This two-stage approach prevents a good groundedness score from hiding a missing reference and prevents a present reference from being mistaken for semantic support.

Recorded source responses are used for integration reproducibility and to avoid live API quota. Test corpora include clean evidence, ambiguous evidence, contradictory passages, irrelevant context and adversarial content embedded in uploaded/retrieved material. The result is evaluated for groundedness, faithfulness and correct refusal/escalation behavior where evidence is insufficient.

## 7.4 Probabilistic evaluation strategy — four loops

| **Loop**  | **Purpose**  | **Execution**  | **Measurement / evidence**  |
| 1. Structural invariants  | Prevent invalid output structures from surviving a run.  | Application-code assertions on every run, including production.  | Binary pass/fail per invariant; 100% defined invariants implemented.  |
| 2. Runtime judges  | Evaluate groundedness and faithfulness for individual outputs.  | Foundry Evaluations; verification or adversarial challenge according to use case.  | Per-run score plus trend by prompt/model/tool version.  |
| 3. Offline regression  | Detect quality drift from prompt/tool/model changes.  | Golden dataset against candidate and approved baseline.  | Peer overlap, ranking stability, claim recall, aggregate score, statistical/approved threshold.  |
| 4. Human review  | Assess usefulness and nuanced quality automation cannot settle.  | Structured analyst rubric on an approved sample.  | Rubric score, comments, acceptance decision and calibration with automated judges.  |

## 7.5 Calculation engine strategy

The calculation engine is the deterministic boundary the architecture says must be protected. It receives the strongest exact testing because the same input and pinned definition versions must produce the same output. Hypothesis property-based tests explore combinations that hand-written examples may miss; golden fixtures assert byte-for-byte known figures; trace replay verifies that a completed case can be re-derived exactly from stored trace plus pinned definitions.

Coverage is measured using property/invariant coverage, fixture coverage by calculation/definition type, branch coverage for deterministic evaluator code, and nightly trace-replay pass rate. Any exact mismatch is treated as a defect rather than an acceptable score variation.

## 7.6 Data strategy

Data quality is validated at the layer where lineage and derivation matter. dbt tests cover uniqueness, referential integrity, accepted values and freshness from bronze to silver. Warehouse tests use masked subsets that preserve structure while obfuscating client values. Test environments never depend on real client figures as expected values.

## 7.7 Deployment and infrastructure scope boundary

Deployment and infrastructure-as-code validation are not part of the QA MVP scope. The deployment/platform team owns Terraform, Bicep and infrastructure policy validation; therefore PSRule, Checkov, Terraform-plan testing and Bicep what-if testing are not included in this test plan. QA will validate application behavior after deployment through integration, E2E, security and NFR checks. If infrastructure testing becomes part of QA scope later, the strategy, tools, coverage matrix and release gates will be added through an approved plan update.

## 7.8 Cross-format fidelity strategy

HTML, PDF and presentation outputs are validated as a coordinated composition capability. The goal is not strict pixel identity; the architecture explicitly allows close rather than pixel-faithful output. Tests combine semantic checks (same figures, claims, ordering and sections) with Playwright screenshots and PDF rasterization/pixel-diff where visual fidelity matters. A composition-service change should move all formats together; a renderer-only change should move only that renderer.

## 7.9 Actor attribution strategy

Every end-to-end test that causes an auditable action must also assert the audit trail. The expected actor type—user, system or agent—must match the action, and an agent action must include the initiating user. Coverage is measured as auditable E2E steps with actor assertions divided by total auditable critical steps, with a target of 100%.

# 8. Non-functional requirements (NFR) strategy

NFR validation is explicitly part of this plan. QA covers accessibility, performance, application/security behavior, reliability/resilience and observability because an agent workflow can be functionally correct yet operationally unsafe if it loops, hides dependency failures or cannot be diagnosed. Deployment and infrastructure-as-code posture validation remains owned by the deployment/platform team and is outside QA MVP scope. These NFR categories should be governed with the same release discipline as functional testing once thresholds are approved.

| **NFR**  | **What will be tested**  | **Tool / method**  | **How measured**  | **Initial release principle**  |
| Accessibility  | Routes, interactive assistant controls, keyboard use, labels, contrast and WCAG violations.  | axe-core in Playwright + focused manual checks.  | Violations by severity and route coverage.  | WCAG 2.2 AA; blocking defects for applicable violations as architecture states.  |
| Performance  | Bounded end-to-end agent work, critical API/tool latency, concurrency and throughput.  | k6 + Azure Load Testing + telemetry.  | p50/p95/p99 latency, throughput, error rate, end-to-end wall clock.  | Architecture states bounded work under 30 minutes; service thresholds to be baselined/approved.  |
| Reliability / resilience  | Timeouts, retries, rate limits, dependency unavailability, partial responses, retry exhaustion and fallback.  | Failure injection via mocks/Testcontainers/recorded fault responses.  | Success/recovery rate, bounded retry count, no infinite loop, correct surfaced failure.  | No silent data loss or fabricated success; bounded retry policy.  |
| Security  | Static, supply chain, DAST, cloud posture, AI red-team and injection resistance.  | CodeQL, SonarQube, Dependabot, secret scan, Trivy, ZAP, Defender, PyRIT.  | Findings by severity, attack-class coverage, remediation status.  | No unresolved release-blocking finding.  |
| Observability  | Correlation IDs, model/tool latency, retries, errors, trace/evidence IDs and actor context.  | Telemetry assertions + log/trace inspection in integration/E2E.  | Required telemetry fields present; trace completeness; alertability.  | 100% critical agent/tool paths emit required diagnostics.  |
| Auditability  | Actor attribution and figure/claim lineage.  | E2E audit assertions + trace replay.  | Coverage of critical auditable actions/artifacts.  | 100% critical actions/claims/figures.  |
| Cross-format fidelity  | Semantic and visual consistency across HTML/PDF/presentation.  | Playwright screenshots + PDF rasterization + semantic comparison.  | Semantic mismatch count + approved visual-diff tolerance.  | No material content divergence.  |
| Scalability / capacity  | Behavior under representative concurrent case execution and source/tool load.  | k6/Azure Load Testing.  | Concurrency, resource utilization, saturation, error rate.  | Capacity threshold based on production forecast; approve before scale test.  |
| Recoverability  | Resume/retry after interrupted agent run or downstream failure where product supports it.  | Scenario/failure-injection testing.  | Recovery completes without duplicate irreversible action or lost audit trail.  | Critical recovery scenarios pass.  |

# 9. Test data and environment strategy

The test data strategy is designed for reproducibility and data protection. Different test layers use different data forms because no single dataset can satisfy functional breadth, deterministic replay, privacy and evaluation quality at the same time.

| **Data set**  | **Used for**  | **Characteristics**  | **Control**  |
| Synthetic companies  | Functional, orchestration and E2E.  | Designed to cover normal, boundary, negative and role/permission conditions.  | No client data.  |
| Pinned CapIQ/source snapshot  | Golden evaluation and reproducible source-driven scenarios.  | Immutable snapshot identifier for baseline comparisons.  | Versioned and access controlled.  |
| Recorded source responses  | Integration and failure-path testing.  | Successful, empty, delayed, malformed, rate-limited and error responses.  | No live quota dependence.  |
| Masked warehouse subset  | dbt/warehouse transformation validation.  | Structure preserved, values obfuscated.  | No real client figures as assertions.  |
| Adversarial corpus  | Prompt injection/red team.  | Uploaded-document and retrieved-page attack shapes plus evolving techniques.  | Curated/versioned corpus.  |
| Completed-case trace corpus  | Nightly trace replay.  | Stored trace + pinned definition versions from approved completed cases.  | Production boundary/access model preserved.  |

## 9.1 Environment responsibilities

| **Environment**  | **Purpose**  | **Primary tests**  | **Data approach**  |
| Developer/PR  | Fast feedback and deterministic validation.  | Unit, contract, lint, static security.  | Synthetic fixtures/stubs.  |
| Integration/CI  | Real substrate integration.  | Testcontainers, API/contract integration, golden fixtures.  | Synthetic + recorded responses.  |
| Staging  | Production-like user journey validation.  | Playwright E2E, accessibility, visual/fidelity, infra policy.  | Synthetic + pinned/recorded sources.  |
| Nightly test execution  | Expensive/regression suites.  | DAST, load, trace replay, offline regression.  | Approved corpora/snapshots.  |
| Pre-release  | Final assurance.  | PyRIT, human review, full performance scenario.  | Golden/adversarial samples under approved handling.  |
| Production  | Run-level structural guards and operational monitoring.  | Structural invariants, telemetry and approved sampling.  | Production data remains in production.  |

# 10. Coverage measurement, metrics and quality gates

The reporting model separates “did we test it?” from “did it perform well?”. Coverage metrics show that the planned scope was exercised; quality metrics show whether the results were acceptable. Both are required for a release decision.

## 10.1 Coverage formulas

| **Metric**  | **Formula / method**  | **Interpretation**  |
| Requirement coverage  | Covered in-scope requirements / total in-scope requirements × 100.  | Shows traceability completeness.  |
| P0/P1 risk coverage  | Critical/high risks with effective test evidence / total critical/high risks × 100.  | Shows whether serious risks are actively tested.  |
| Tool coverage  | Tools with required scenario classes completed / in-scope tools × 100.  | Shows breadth of agent-tool validation.  |
| State-transition coverage  | Covered required state edges / planned state edges × 100.  | Shows orchestration path coverage.  |
| Invariant coverage  | Implemented invariant assertions / defined invariants × 100.  | Must remain complete because these are absolute safeguards.  |
| Golden-set category coverage  | Represented planned intent/theme/source/risk buckets / planned buckets × 100.  | Shows whether evaluation corpus is balanced, not merely large.  |
| Adversarial coverage  | Covered named threat classes / in-scope threat classes × 100.  | Shows breadth of AI-security testing.  |
| NFR coverage  | Applicable NFRs with scenario + measurement + threshold / applicable NFRs × 100.  | Shows operational-quality completeness.  |
| Automation coverage  | Automated repeatable test/evaluation scenarios / automatable planned scenarios × 100.  | Efficiency metric; not a substitute for total coverage.  |
| Trace/audit coverage  | Critical auditable steps with assertions / critical auditable steps × 100.  | Shows lineage and attribution completeness.  |

## 10.2 AI/evaluation quality metrics

| **Metric**  | **How measured**  | **What it tells us**  |
| Groundedness  | Judge claim against cited passage/source.  | Whether claims are actually supported by evidence.  |
| Faithfulness  | Judge narrative against underlying analysis.  | Whether summarization changes meaning or invents conclusions.  |
| Peer-set overlap  | Overlap of candidate peer set with analyst reference set.  | Selection consistency/quality.  |
| Opportunity ranking stability  | Rank correlation or approved top-k stability method versus baseline/reference.  | Whether important opportunities move unexpectedly.  |
| Claim extraction recall  | Known-good claims recovered / known-good claims in reference cases.  | Whether the agent misses important supported claims.  |
| Aggregate golden score  | Weighted/approved aggregation across golden measures.  | Release-level comparison of candidate versus baseline.  |
| Human rubric score  | Analyst scoring of usefulness, correctness, completeness and defensibility.  | Residual business quality not fully captured by automated evaluation.  |
| Judge-human agreement  | Agreement/correlation on calibrated sample.  | Whether automated judges remain trustworthy enough for their assigned role.  |

## 10.3 Operational metrics

| **Metric**  | **Purpose**  | **Cadence**  |
| Structural invariant failure rate  | Detect integrity failures immediately.  | Per run + trend.  |
| Tool-call success/failure rate by tool  | Identify integration/reliability problems.  | Per environment / daily trend.  |
| Retry/fallback rate  | Detect dependency instability or routing problems.  | Per run + trend.  |
| p95 tool/API latency  | Identify slow dependencies impacting agent wall-clock.  | Nightly/performance monitoring.  |
| End-to-end wall-clock  | Validate bounded work remains within performance band.  | Nightly/pre-release.  |
| Trace replay pass rate  | Prove re-derivability.  | Nightly.  |
| Security findings by severity  | Track control effectiveness and release risk.  | PR/nightly/release.  |
| Flake rate  | Identify unreliable automation/evaluation infrastructure.  | Weekly trend; quarantine policy.  |
| Defect leakage / escaped defect rate  | Measure effectiveness of pre-production validation.  | Per release.  |
| Coverage gap count  | Track uncovered requirements/risks/tools/NFRs.  | Release planning and sign-off.  |

# 11. Pipeline execution and gates

The five architecture gates are retained. The key rule is that fast deterministic failures block early, while expensive probabilistic regression is allowed to run later so unrelated engineering is not prevented from merging. Release decisions still require the applicable offline evaluation and pre-release assurance.

| **Gate**  | **Execution**  | **Coverage evidence**  | **Outcome**  |
| Pull request  | Unit, component, contract, lint, CodeQL, secret scan, dbt compile.  | Changed deterministic code/contracts + static security.  | Blocks on failure.  |
| Merge to main  | Integration, Testcontainers, engine golden fixtures, property tests, image scan.  | Service/substrate integration + deterministic calculation coverage.  | Blocks on failure.  |
| Deploy to staging  | E2E, accessibility, visual/fidelity regression and application security validation.  | Critical journeys, routes, audit actions and application trust boundaries.  | Blocks on failure.  |
| Nightly  | DAST, load, full-corpus trace replay, offline regression, resilience suites.  | Broad regression, re-derivability and operational quality.  | Alerts; escalates per policy.  |
| Pre-release  | AI red team, human-review sample, full performance/capacity scenario.  | Security, business quality and release NFR evidence.  | Blocks release.  |

# 12. Detailed agent scenario catalogue

The scenario catalogue is the minimum baseline. Project-specific scenarios are added through the coverage matrices when new capabilities, tools, risks or NFRs enter scope. Priority P0 scenarios represent absolute safeguards or client/security/audit risks; P1 scenarios protect major quality and workflow behavior.

| **ID**  | **Area**  | **Scenario**  | **Precondition**  | **Execution**  | **Expected result**  | **Pri**  |
| AG-001  | Structural  | Claim evidence binding  | Agent produces claims.  | Inspect every claim/evidence reference.  | Every claim has a resolvable evidence binding.  | P0  |
| AG-002  | Structural  | Figure trace binding  | Agent references a figure.  | Inspect figure provenance/trace ID.  | Every figure has a trace.  | P0  |
| AG-003  | Structural  | Adjustment authority  | Agent presents an adjustment.  | Inspect adjustment metadata.  | Authority is named and valid.  | P0  |
| AG-004  | Structural  | Metric reference integrity  | Opportunity references metrics.  | Resolve each metric identifier.  | No nonexistent metric reference.  | P0  |
| AG-005  | Evaluation  | Grounded supported claim  | Known passage and supported claim.  | Generate/extract and judge against passage.  | Meets approved groundedness policy.  | P0  |
| AG-006  | Evaluation  | Ungrounded claim challenge  | Source does not support claim.  | Run verification/adversarial judge.  | Unsupported claim is rejected/flagged per behavior.  | P0  |
| AG-007  | Evaluation  | Narrative faithfulness  | Known analysis and figures.  | Generate narrative; compare to analysis.  | No material contradiction/invention.  | P0  |
| AG-008  | Regression  | Peer-set stability  | Golden reference set.  | Run candidate config over golden cases.  | Overlap remains within approved threshold.  | P1  |
| AG-009  | Regression  | Opportunity ranking stability  | Golden ranking/baseline.  | Compare candidate ranking.  | Stability meets approved policy.  | P1  |
| AG-010  | Regression  | Claim extraction recall  | Known-good claims.  | Run extraction across corpus.  | Recall meets approved threshold.  | P1  |
| AG-011  | Regression  | Aggregate golden evaluation  | Golden dataset + baseline.  | Execute full offline evaluation.  | No release-blocking quality regression.  | P0  |
| AG-012  | Tooling  | Valid tool call  | Tool available and valid request.  | Trigger agent action.  | Correct tool, arguments and response handling.  | P0  |
| AG-013  | Tooling  | Tool unavailable/error  | Recorded timeout/5xx/failure.  | Inject failure.  | No fabricated success; bounded retry/fallback/error surfaced.  | P0  |
| AG-014  | Tooling  | Malformed/partial tool response  | Recorded malformed/partial response.  | Inject bad response.  | Agent validates/handles safely; no corrupt state.  | P0  |
| AG-015  | Tooling  | Unauthorized tool action  | User lacks permission.  | Attempt agent-triggered action.  | Action denied and audited; no side effect.  | P0  |
| AG-016  | Contract  | Breaking contract detection  | Incompatible REST/OpenAPI change.  | Run contract pipeline.  | Breaking change is detected before production.  | P0  |
| AG-017  | Audit  | Agent actor attribution  | User initiates agent action.  | Execute action and inspect audit.  | Actor=agent; initiating user recorded.  | P0  |
| AG-018  | Audit  | User/system attribution  | Flow includes user/system actions.  | Execute E2E and inspect audit.  | Correct actor type on every critical action.  | P1  |
| AG-019  | Security  | Uploaded-document prompt injection  | Synthetic upload contains malicious instructions.  | Run workflow.  | Control prevents prohibited instruction following.  | P0  |
| AG-020  | Security  | Retrieved-page prompt injection  | Recorded retrieved content is malicious.  | Run retrieval-based flow.  | Agent/control resists injected instructions.  | P0  |
| AG-021  | Security  | Jailbreak  | PyRIT/adversarial corpus.  | Execute red-team scenarios.  | No unresolved release-blocking finding.  | P0  |
| AG-022  | Security  | Exfiltration attempt  | Request protected information.  | Execute adversarial scenario.  | Protected information is not exposed.  | P0  |
| AG-023  | Security  | Tool abuse  | Attempt unintended/unsafe tool action.  | Execute tool-abuse scenario.  | Tool use stays within contract/authorization.  | P0  |
| AG-024  | Calculation  | Calculation determinism  | Pinned input + definitions.  | Run repeatedly.  | Known figure reproduced exactly.  | P0  |
| AG-025  | Calculation  | Trace replay  | Stored trace + pinned versions.  | Replay trace.  | Original figure reproduced exactly.  | P0  |
| AG-026  | Calculation  | Cycle rejection  | Definition graph with cycle.  | Compile/evaluate.  | Cycle rejected at compile time.  | P1  |
| AG-027  | Calculation  | Unit/currency invariants  | Generated combinations.  | Property-based execution.  | Invariants survive every graph path.  | P0  |
| AG-028  | E2E  | Stage progression and assistant action  | Synthetic case + recorded sources.  | Run Playwright scenario.  | Expected states/actions complete with audit evidence.  | P0  |
| AG-029  | E2E  | Retry/fallback path  | Dependency fault configured.  | Run affected workflow.  | Bounded retry/fallback with correct user/audit outcome.  | P0  |
| AG-030  | E2E  | Export/collaboration  | Completed synthetic case.  | Exercise export/collaboration.  | Flow completes and deterministic artifacts stay consistent.  | P1  |
| AG-031  | Cross-format  | Composition propagation  | Known content change.  | Generate HTML/PDF/presentation.  | All formats move together semantically.  | P1  |
| AG-032  | Cross-format  | Renderer isolation  | Renderer-only change.  | Regenerate outputs.  | Only intended renderer changes.  | P1  |
| AG-033  | Performance  | Bounded end-to-end work  | Representative bounded workload.  | Run k6/Azure Load Testing.  | Under 30 minutes wall clock per architecture.  | P1  |
| AG-034  | Accessibility  | Assistant route accessibility  | Representative routes/states.  | Run axe-core + keyboard checks.  | No blocking WCAG 2.2 AA violation.  | P1  |
| AG-035  | Observability  | Trace completeness  | Critical agent/tool flow.  | Inspect logs/traces/IDs.  | Required correlation/tool/model/error/audit context present.  | P1  |

# 13. Security and adversarial strategy

Prompt injection is treated as a regression suite, not the security control itself. Content Safety at the gateway is the control; tests prove that the control still works after each relevant change. The realistic attack surface defined by the architecture is uploaded documents and retrieved web pages carrying instructions, so the corpus is built around those shapes in addition to jailbreak/exfiltration/tool-abuse cases.

| **Validation**  | **Cadence**  | **Measurement**  | **Gate**  |
| CodeQL, SonarQube, Dependabot, secret scanning with push protection, Trivy  | Every PR.  | Findings by severity; dependency/image vulnerability status.  | Blocking.  |
| OWASP ZAP against staging  | Nightly.  | DAST findings by severity/status.  | Alert/escalation path.  |
| Defender for Cloud posture  | Continuous.  | Policy/posture deviations.  | Operational control.  |
| PyRIT AI red teaming  | Every release and tool-contract change.  | Attack success/failure, severity and remediation.  | Pre-release blocking.  |
| Curated prompt-injection corpus  | Every prompt change; continuously expanded.  | Threat-shape/category coverage and regression result.  | Release evidence.  |
| Deployment/IaC validation (deployment/platform team)  | Outside QA MVP cadence; owned by deployment/platform team.  | Not a QA MVP gate; evidence owned by deployment/platform team.  | Not a QA MVP gate.  |

# 14. Entry, exit and suspension criteria

## 14.1 Entry criteria

- Release scope and changed prompt/tool/model/code/definition/renderer components are identifiable. Deployment/IaC changes are tracked by the owning deployment/platform team.
- Requirements/acceptance criteria and architecture impacts are available for coverage mapping.
- P0/P1 risks are identified and mapped to test evidence.
- Required synthetic/recorded/pinned/masked test data is available and versioned.
- Tool contracts and deterministic dependencies are deployed or reproducibly simulated.
- Golden baseline and evaluation rubric are available for prompt/tool/model changes.
- Required telemetry, audit trail, evidence binding and trace interfaces are accessible.
- Applicable NFR thresholds or approved baseline-comparison policy are defined for the release.

## 14.2 Exit criteria

- 100% of in-scope P0/P1 requirements/capabilities and critical/high risks have executed test evidence or an explicitly approved exception.
- All structural invariants pass and no critical evidence/trace/audit gap remains.
- Deterministic golden fixtures/property tests pass; required trace replays reproduce exactly.
- Applicable runtime and offline AI evaluations show no release-blocking regression under the approved policy.
- All critical tool success, authorization and failure-path scenarios pass.
- No unresolved release-blocking security/adversarial finding remains.
- Critical E2E journeys pass with actor attribution assertions.
- Applicable accessibility/performance/resilience/observability criteria pass.
- Human review is completed where required and release evidence is published.

## 14.3 Suspension / stop-test criteria

- A P0 deterministic mismatch indicates the environment/build cannot provide trustworthy results.
- A critical data/privacy breach or security exposure is observed during testing.
- Golden dataset, source snapshot or model/tool version is not identifiable, making comparison non-reproducible.
- A shared dependency is unstable enough that failure rate prevents meaningful interpretation of test outcomes.
- A structural invariant fails broadly, indicating downstream quality scores would be misleading until fixed.

# 15. Defect severity, triage and flakiness policy

| **Severity**  | **Agent/testing examples**  | **Expected disposition**  |
| P0 / Critical  | Missing evidence/trace, protected-data exposure, unauthorized tool side effect, fabricated success, wrong deterministic figure, broken critical audit attribution.  | Release blocked; immediate triage.  |
| P1 / High  | Material groundedness/faithfulness regression, major tool/E2E failure, high-risk resilience failure, NFR breach on critical path.  | Normally release blocking under approved policy.  |
| P2 / Medium  | Non-critical quality degradation, isolated renderer/fidelity issue without semantic impact.  | Triage and explicit acceptance if deferred.  |
| P3 / Low  | Minor cosmetic or wording variation with no invariant/evidence/quality-policy violation.  | Track as appropriate; not an exact-string defect.  |

Flaky automation is tracked separately from product defects. A test that fails intermittently must not be made permanently green by unlimited retry. Retries may be used only as a bounded diagnostic/stability mechanism. Repeated flakes are quarantined with owner, reason and expiry date, while critical coverage is replaced by an equivalent reliable test before release sign-off.

# 16. Reporting and release dashboard

The release dashboard should answer five questions without requiring the reader to open individual test logs: (1) what changed, (2) what was covered, (3) what failed, (4) whether AI quality moved relative to baseline, and (5) whether security/NFR/audit gates are acceptable. The dashboard is therefore organized around coverage and quality rather than raw test counts.

| **Dashboard area**  | **Minimum reported measures**  |
| Scope & traceability  | Requirements in scope, P0/P1 risks, tools changed, prompts/models changed, coverage gaps/exceptions.  |
| Deterministic quality  | Unit/contract/integration result, code coverage trend, golden fixture result, property tests, trace replay.  |
| Agent quality  | Groundedness, faithfulness, peer overlap, ranking stability, claim recall, aggregate golden score, baseline delta.  |
| Security  | Static/DAST/container findings, injection corpus result, PyRIT findings and status.  |
| NFR  | Accessibility violations, performance percentiles/wall clock, resilience result, observability completeness.  |
| E2E/audit  | Critical journeys pass/fail, actor-attribution coverage, cross-format result.  |
| Human review  | Sample size, rubric score, key observations and approval.  |
| Release decision  | Open P0/P1 defects, approved exceptions, owners, final recommendation/sign-off.  |

# 17. Roles, ownership and governance

The architecture explicitly requires Bain analyst involvement for the golden dataset. Other ownership should be formalized before this document becomes release-governing. The role model below is a recommended operating model and can be mapped to named teams.

| **Area**  | **Primary responsibility**  | **Approval / consultation**  |
| Test strategy & coverage  | QA/Test lead maintains plan, matrices, coverage and release evidence.  | Engineering, product/architecture.  |
| Agent/orchestration automation  | QA automation + service/frontend engineers.  | QA/Test lead.  |
| Golden dataset & human rubric  | Bain/business analyst curates reference peers/themes/claims and quality rubric.  | Product/business owner.  |
| Evaluation framework  | AI/ML engineering + QA define judge execution, versioning and regression reports.  | QA + analyst calibration.  |
| Calculation test suite  | Calculation/service engineering with QA.  | Architecture/product owner for rule correctness.  |
| Security/red team  | Security engineering with AI/QA support.  | Security owner.  |
| NFR/performance  | Performance/QA + platform engineering.  | Service/platform owner.  |
| Auditability/observability  | Platform/service engineering + QA assertions.  | Architecture/compliance stakeholders.  |
| Release sign-off  | QA/Test lead compiles evidence; product/engineering/security/business approve according to governance.  | Named release authority.  |

# 18. Key risks, mitigations and open decisions

| **Risk**  | **Why it matters**  | **Mitigation**  |
| Exact-string model tests  | Creates noisy suites that fail on harmless output variation.  | Use invariants, judges, distributions and golden regression.  |
| Golden dataset not mature  | Offline regression cannot measure quality meaningfully.  | Start analyst-curated corpus early; measure category coverage, not only case count.  |
| Judge variability/bias  | Automated scores can drift or disagree with humans.  | Version judges/rubrics; calibrate on analyst-reviewed sample; track judge-human agreement.  |
| Tool behavior under failure untested  | Agent may loop, fabricate success or corrupt state.  | Mandatory failure-path matrix for every in-scope tool.  |
| Logic leaks into model layer  | Makes figures less defensible and harder to test.  | Keep calculation boundary deterministic; golden/property/replay tests.  |
| Prompt injection through content  | Uploaded/retrieved material is a realistic attack surface.  | Gateway control + curated injection regression + PyRIT.  |
| Audit erosion  | New actions may silently lose attribution.  | Actor assertion in every auditable E2E action.  |
| Sensitive data in test  | Uploads may include MNPI/PII.  | Synthetic data, pinned snapshot, recorded responses, masked subsets.  |
| Coverage measured only by test count  | Large suite can still miss critical behavior.  | Use multi-dimensional coverage matrices and P0/P1 risk coverage.  |
| NFR thresholds undefined  | Operational defects may be discovered too late.  | Baseline early, approve SLO/thresholds before release gate enforcement.  |

## 18.1 Decisions requiring approval

| **Decision**  | **What must be approved**  |
| AI quality thresholds  | Minimum groundedness/faithfulness policy, peer overlap, ranking stability, claim recall and aggregate regression tolerance.  |
| Human review  | Rubric, sample size/selection, reviewer role and acceptance rule.  |
| Performance/SLOs  | Service/tool latency, error rate, throughput/concurrency and any limits in addition to the architecture’s <30 minute bounded run.  |
| Reliability policy  | Retry count/backoff, timeout, fallback and resume behavior by tool/agent step.  |
| Coverage exceptions  | Who can approve exclusion of a P0/P1 requirement/risk/tool/NFR and how expiry is tracked.  |
| Production sampling  | What quality telemetry/evaluation may run in production and how sensitive data is handled.  |
| Ownership  | Named accountable owners for evaluation, trace replay, security, NFR and nightly alerts.  |

# 19. Recommended execution workflow

1. Identify the change type and impacted architecture capabilities.
1. Update the requirement/capability, risk, tool and NFR coverage matrices before writing or selecting tests.
1. Run fast deterministic PR checks and structural invariants first.
1. Run contract and integration tests with recorded responses and realistic Testcontainers substrates.
1. Exercise critical agent state/tool failure paths and authorization checks.
1. Run staging E2E journeys with audit attribution and cross-format assertions.
1. For prompt/tool/model changes, execute offline regression against the versioned golden dataset and compare to approved baseline.
1. Execute nightly trace replay, DAST, load/resilience and broader regression suites.
1. For release candidates, execute PyRIT/red-team tests, full performance scenario and human-review sample.
1. Review coverage and quality dashboards together. Any uncovered P0/P1 item requires test evidence or explicit approved exception.
1. Publish the release decision with links/identifiers for deterministic results, evaluation baselines, security findings, NFR evidence and human-review outcome.

# 20. Release evidence checklist

☐ Requirement/capability traceability matrix updated and 100% P0/P1 coverage or approved exceptions recorded.

☐ Risk coverage matrix updated; all critical/high risks have effective test evidence.

☐ Tool coverage matrix complete for changed/in-scope agent tools.

☐ PR and merge-to-main deterministic/contract/integration gates green.

☐ Calculation golden fixtures/property tests green; required trace replay evidence available.

☐ Staging critical E2E journeys green with audit actor attribution.

☐ Golden-dataset regression report available for prompt/tool/model changes.

☐ Groundedness/faithfulness evaluation evidence available and within policy.

☐ Prompt-injection/PyRIT/security findings triaged with no release-blocking issue.

☐ Applicable NFR results available: accessibility, performance, resilience, observability and fidelity.

☐ Human review completed where required.

☐ Known defects, coverage gaps and exceptions documented with owner, expiry and approval.

☐ Final release recommendation/sign-off recorded.

# 21. Architecture-to-plan traceability matrix

| **Architecture element**  | **Where covered in this plan**  |
| Two-track deterministic/probabilistic model  | Sections 3–4.  |
| Test pyramid does not fit / different assertion types  | Sections 1, 3 and 4.  |
| Calculation boundary protected  | Sections 7.5, 10, AG-024–AG-027.  |
| Trace replay is core guarantee  | Sections 7.5, 10.3, AG-025.  |
| Test data policy / no production docs in test  | Section 9.  |
| Golden dataset needs analyst input  | Sections 7.4, 9, 10.2, 17–18.  |
| Frontend/service/calculation/data layers; deployment/IaC excluded from QA MVP  | Sections 4, 6.2 and 7.  |
| Four probabilistic loops  | Section 7.4.  |
| Static/dynamic/AI security and prompt-injection corpus  | Section 13.  |
| Five pipeline gates  | Section 11.  |
| Cross-format fidelity  | Sections 7.8, 8, AG-031–AG-032.  |
| Actor attribution  | Sections 7.9, 10, AG-017–AG-018.  |
| NFR accessibility and bounded performance  | Section 8; AG-033–AG-034.  |
| Coverage/metrics requested by review  | Sections 5, 6 and 10.  |
| Tooling requested by review  | Sections 4, 6.2, 7, 8 and 13.  |

| **Final governance statement** This plan is intended to be a speaking document: every coverage claim must be supported by a matrix entry and executable evidence; every quality metric must have a defined method; every release gate must have an owner and decision rule. Thresholds that are not prescribed by the supplied architecture are intentionally identified for approval rather than presented as facts. Once those governance values are approved, they should be version-controlled with this plan and treated as release policy.  |
