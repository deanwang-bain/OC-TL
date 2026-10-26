# OpCat testing strategy — plan and scope

**Status:** Draft for Tech Lead sign-off · **Prepared:** 2026-10-26 (GLS day) ·
**Target milestone:** the 50+ partner rollout, late November or early December
([Deployment Tracker](../confluence/oi30/architecture/opportunity-catalyst-architecture-high-level/deployment-design-ai-compute-data-components-cicd/oc-dev-staging-gls-deployment-tracker-19909279789.md),
as summarised in [the brief](../context/oi30-brief.md)).

**Audience:** the Tech Lead first. Once the decisions in §2 are signed off, this becomes the
brief for the testing engineer, and §8 becomes their backlog.

**Sources.** The OI30 mirror, Bain's AI Architecture Requirements workbook, and external
research (§12). **Sage was not consulted:** the connector is connected for the org but not
loaded in the session that wrote this. §11 lists the queries still to run and what each
could change.

---

## 1. Bottom line

1. **Do not write another test plan.** The
   [Agent Validation Test Plan](../confluence/oi30/architecture/agent-validation-test-plan-19765133323.md)
   (v2, 7 October) already sets out a sound method:
   - two tracks: deterministic and probabilistic;
   - four evaluation loops;
   - five pipeline gates;
   - a coverage model.

   It is generic, though. It names no agents, sets no thresholds, assigns no owners, and
   has no list of guardrails. **This document is the layer that scopes that method to what
   is actually built.**
2. **The method conflicts with Bain's own governance gate.**
   - [Technology Choices](../confluence/oi30/architecture/opportunity-catalyst-architecture-high-level/technical-stack/technology-choices-19751338017.md)
     T14 says offline model regression blocks a *release, not a merge*, and §4 dates
     offline regression to *north star*.
   - The AI Architecture Requirements workbook says
     prompt changes **MUST** be regression-tested against an eval set **before merging**
     (CQ-AI-PMT-02, MUST).
   - §7 reconciles them with a small smoke eval that blocks merge only on agent-affecting
     changes.
3. **What OpCat most needs to test is that the numbers are right, not the wording.** A
   partner's trust rests on every number tracing back to the calculation engine. That
   check can be **deterministic**: every figure in the UI, the narrative and the deck must
   match a value the calculation API returned. It does not need an LLM judge. Judges are
   kept for the prose around the numbers.
4. **Guardrails are mostly unverified, and one may not be on the agents' call path.**
   - Content Safety at the API Management gateway is *the* prompt-injection control
     (Technology Choices §9.4).
   - Nobody has confirmed that the Foundry agents' calls pass through that gateway
     ([brief](../context/oi30-brief.md), peer-selection section).
   - If they do not, the injection corpus would be testing a control that is not there.
   - Several controls already exist in code and deserve tests: the `cap_id` allow-list, the
     chat answer's citation check, and declared tools that refuse.
5. **Recommended split of ownership:**
   - **StatusNeo owns the in-repo tests** (unit, contract, integration, MCP tool tests) as
     part of the definition of done.
   - **A Bain-side testing engineer owns an independent acceptance and evaluation layer:**
     the golden eval set, the held-out set SN never sees, the red-team corpus, acceptance
     journeys run against staging, and the release evidence pack.
   - That way the vendor does not grade its own homework on AI quality, and the Bain
     engineer never writes application code, which is the workspace's role boundary.

---

## 2. Decisions needed before the testing engineer starts

Recommended outcome first. Each can be signed off independently.

| # | Decision | Recommendation | Why |
| - | -------- | -------------- | --- |
| **D1** | Who the testing engineer works for | **Bain-side**, owning the independent layer in §5 | Independence on AI quality. SN already has a QA stream (§3) |
| **D2** | Where the eval harness and corpora live | **A Bain-controlled repo**, separate from SN's two repos. SN's CI calls a published smoke-eval action or container; the held-out set never leaves Bain | A vendor that can see the test can tune to it. Keeps the role boundary in `CLAUDE.md` |
| **D3** | How to square T14 with CQ-AI-PMT-02 | **Two eval tiers** (§7): a smoke eval blocks merge on changes to prompts, tools, agent config or model deployment; the full golden regression blocks release | Satisfies the MUST without letting a model provider's drift block unrelated merges, which was T14's concern |
| **D4** | Thresholds for v0 | **Relative to an approved baseline, not absolute.** Structural invariants stay at 100%. Absolute targets are set after the first round calibrated against SME labels | An absolute threshold set before any data exists is invented policy, and the existing plan rightly refuses to invent it |
| **D5** | Who curates the golden eval set | **A named BCN analyst with booked hours**, plus Oliver for peer-set references (S4-52 already involves both) | Technology Choices open item 8: *"nothing substitutes for that"* |
| **D6** | Whether Foundry agent calls pass through the API Management gateway | **Ask SN to confirm, with a trace, before WP-10 starts** | Decides whether the Content Safety control exists on the path being tested |
| **D7** | Autonomy level per agent (SD-AI-AGT-01) | Peer discovery **T0** (suggests; the partner confirms through OI3-221). Chat assistant **T1 or T2**, to confirm: it changes the peer set on request | Red-team intensity and human-in-the-loop requirements scale with the level |
| **D8** | Whether the GLS golden data set may be used in test environments | **Check permitted use against the Data Source Catalogue** before it seeds evals | It is real company data from BCN documents. The test-data policy allows one pinned, licensed snapshot |
| **D9** | Which model judges | **Pinned, versioned, and a different deployment from the generator** where one is available (`gpt-4.1` judging `gpt-5.2`, or the reverse). Re-calibrate whenever it changes | Judges drift with their model. A judge grading its own output is biased toward it |
| **D10** | Which database the integration tests run on | **Match what is deployed.** The test plan says Testcontainers with SQL Server and Technology Choices §5 says Azure SQL; the deployment tracker runs **Postgres** | An integration test on the wrong substrate proves nothing about the real one |

---

## 3. Starting point — what exists today

| Artefact | State | Gap this plan closes |
| -------- | ----- | -------------------- |
| [Agent Validation Test Plan](../confluence/oi30/architecture/agent-validation-test-plan-19765133323.md) v2 | *"Updated draft for architecture/test-strategy review."* 35 scenarios (AG-001 to AG-035), coverage formulas, gates | No agents named, no thresholds, no owners, no list of named threat classes, no statistics for repeat runs |
| [Technology Choices §9](../confluence/oi30/architecture/opportunity-catalyst-architecture-high-level/technical-stack/technology-choices-19751338017.md) | The testing architecture the plan was derived from | Still lists `buf`, PSRule and Checkov, which the test plan excludes. Offline regression is *north star* only |
| SN quality stream ([Sprint 3 Retro deck](../confluence/_attachments/19933790220/Opportunity_Catalyst_Sprint3_Retro.pptx)) | Frontend contract and boundary tests; audit, BFF and case services tested; peer-selection agents tested; a security scan framework *"run on demand"*; OI3-230 (QA for peer service) and OI3-227 (QA for peer selection screen) | Unknown which §9.7 gates are actually **enforced** in CI rather than run by hand. WP-01 finds out |
| [Dev streaming and chat-agent checks](../confluence/oi30/architecture/opportunity-catalyst-architecture-high-level/chat-assistant-architecture/dev-streaming-and-chat-agent-checks-summary-19899842692.md) (4 Oct) | A careful manual test report: SSE through Front Door, resume, 429 at four streams, the agent's silent start, web answers withheld | The model for non-functional evidence. Its open items become test cases (§6, WS5) |
| GLS golden data set (Sprint 4 planning, in [the brief](../context/oi30-brief.md)) | 10 targets, about 100 peers, BCN pre-calculated cost bars, levers, size of prize and recommendations | **A calculation fixture, not an eval set.** It has no expected themes, no known-good claims and no negative or adversarial cases. It is the right seed for one |
| [Testing architecture diagram](../confluence/_attachments/19765133323/att_0_for_19765133323.png) | Says the golden dataset is *"1 of 10 open items, and the only one that needs Bain analyst time"* | Same. D5 |
| AI Architecture Requirements v2.1 ([Assessment Tracker](https://bainco.atlassian.net/wiki/spaces/OI30/pages/19853082681)) | 113 MUSTs, **0 responses** | About 25 of them can only be answered with test evidence (§9) |

---

## 4. Scope — the system under test

### In scope for the partner rollout

| Component | What is built | Track |
| --------- | ------------- | ----- |
| **Peer discovery agent** | `POST /peers/discover`. An agent branch: Foundry proposes names, then a second call resolves each to a `cap_id` or null, then `resolve()` drops invented IDs. A deterministic branch: BM25 plus embeddings. Then `analyse_pair` once per peer ([Present working — technical details](../confluence/present-working-technical-details-19849609338.md)) | Probabilistic, with deterministic guardrails |
| **Chat assistant agent** | Foundry-hosted, `gpt-5.2`. A tool catalogue; acts on the case through service APIs; checks every citation against the case sources ([Chat assistant architecture](../confluence/oi30/architecture/opportunity-catalyst-architecture-high-level/chat-assistant-architecture-19899809824.md)) | Probabilistic |
| **Narrative agent** | Landed in Sprint 3. Writes the narrative blocks over calculated figures | Probabilistic, but its numbers are deterministic |
| **Calculation engine** | GLS engine; cost-bar recalculation after a peer change (S4-12); peers with a missing metric are excluded and flagged (S4-02) | Deterministic |
| **UI** | Six screens: Dashboard, Target Setup, Peer Review, Case for Change, Analysis, Output & Deck Builder. A CopilotKit / AG-UI chat panel; case stream A and agent stream B over SSE; AG Grid; ECharts / Vega-Lite | Deterministic, plus streaming |
| **Platform** | Experience BFF, audit-service (ledger plus blob seal), case-service, document ingestion into Azure AI Search, filtered by `case_id` | Deterministic |
| **Export** | PPT in Bain / think-cell format | Deterministic structure, visual fidelity |
| **Guardrails** | Everything in §6 WS3 | Both |

### Out of scope until built — do not claim coverage

The rest of the nine-agent swarm in the technical architecture diagram:
- Research, IP-Retrieval and Benchmark;
- SoP Composer, Skeptic and Persona;
- Slide Composer, VoiceApply and 3-Takeaway Optimizer.

Also out of scope until built:
- the **Eval Gate** service;
- the **pre-flight gate**;
- the learning pipeline (SFT, RLVR, partner-edit RLHF);
- per-partner adapters;
- the Greater China variant.

Each is added through the coverage matrix when it lands. The plan must never report
coverage for a component that does not exist.

### Excluded by existing agreement

- **IaC validation** (Terraform, PSRule, Checkov) belongs to the platform team, per the
  test plan §2.2.
- **gRPC/buf** is out because MVP is REST-only.

These exclusions stand. Technology Choices §9.2 should be corrected to match; that is an
ask to SN.

---

## 5. Operating model

| Layer | Owner | Runs where | Evidence |
| ----- | ----- | ---------- | -------- |
| Unit, component, contract (Schemathesis), FastMCP in-memory tool tests, integration (Testcontainers), calculation golden fixtures, property tests, trace replay | **SN** — part of each story's definition of done | SN CI | CI results; the testing engineer audits enforcement (WP-01) |
| Smoke eval on agent-affecting PRs | **SN runs it, Bain owns it** | SN CI, calling the Bain-published action | Pass/fail plus an eval-delta report on the PR |
| Golden eval set, judges, rubrics, thresholds, **held-out set** | **Bain testing engineer**, with BCN as domain owner | Bain-controlled runner against staging | Nightly regression report; held-out results at release |
| Acceptance journeys (Playwright) against staging | **Bain testing engineer** | Bain-controlled runner | Journey pass/fail with audit and provenance assertions |
| Guardrail register, injection corpus, red team | **Bain testing engineer**, with SN fixing what is found | Bain-controlled runner | Findings by severity; attack-class coverage |
| Human review | **SME panel**: BCN, plus a partner sample | Review sessions | Rubric scores; agreement between judges and humans |
| Release evidence pack and go/no-go record | Testing engineer compiles it; **the Tech Lead recommends, the named release authority signs** | Confluence page | One page per release |

**Every sprint review includes a 30–50-trace error-analysis session** with an SME.
Reading real transcripts is how graders get checked and new cases get found. External
practice is consistent on this: *"you won't know if your graders are working well unless
you read the transcripts"* (Anthropic, §12).

---

## 6. Workstreams

### WS1 — UI and end-to-end

**Goal:** prove the partner journey works, and that the UI never shows an untraceable
number.

- **Acceptance journeys in Playwright against staging, on the GLS data set:**
  - set up a target;
  - discover, then edit, then confirm peers (OI3-221);
  - Case for Change;
  - Analysis drill-down to evidence;
  - a chat-driven action ("remove Adidas, add Asics");
  - export.

  Each journey asserts three things:
  - the expected state;
  - **the audit actor** (user, system or agent, plus the initiating user; ADR-005,
    AG-017);
  - **provenance**: every figure element links to a source that resolves.
- **Two ways to run the stream:**
  1. *Replayed*: a mock SSE server, owned by a Playwright fixture, replays recorded AG-UI
     and case-stream event sequences on cue. Playwright's `route.fulfill` cannot stream,
     so it can't be used for this. This mode tests loading, partial, error and reconnect
     states deterministically.
  2. *Live*: a small smoke suite against real agents, asserting invariants only and never
     exact text.
- **Stream behaviour cases taken from the 4 October checks:**
  - a fourth stream returns 429; what does the UI do? (*"we haven't checked"*);
  - resume after reconnect using `Last-Event-ID`;
  - an expired cursor after 72 hours;
  - access removed mid-stream should end the stream within 60 seconds;
  - the agent's silent start;
  - the answer arriving as a single block.
- **Gates as product logic:**
  - a private company with no financials hits a **hard gate** and blocks;
  - low-confidence data hits a **soft gate**, which proceeds and flags
    ([Vision](../confluence/oi30/overview/vision-19617939629.md));
  - a hard gate downgraded to a warning is a P0 defect.
- **Components:** Vitest, React Testing Library and MSW `sse()` replaying recorded AG-UI
  traces. This is SN's layer; the testing engineer reviews coverage.
- **Grid and charts:** AG Grid virtualisation needs a real browser, not jsdom. ECharts is
  snapshotted as server-rendered SVG with animation off.
- **Accessibility:** `@axe-core/playwright` on every route, against WCAG 2.2 AA, which is
  the one non-functional target written anywhere (Technology Choices §2). Add a manual
  keyboard and screen-reader pass on the chat panel.
- **Progressive delivery:** first partial result **within 30 seconds** of run start, a
  Playwright timing assertion (Technology Choices §9.5).

### WS2 — Agent evaluation

**Goal:** measure whether agent output is right, consistently, and catch regressions
before partners do.

**Harness shape:**
- Structure: tasks, trials, graders, transcripts.
- It is black-box: it drives agents through the same BFF and agent endpoints the UI uses,
  with a test identity, and records full trajectories.
- Every result is tagged with the **agent version manifest** (WP-02): prompt hash, tool
  schema version, model deployment and Foundry project. Without it, a regression cannot be
  attributed to a change, and the test plan's own suspension criteria apply (§14.3).

**Graders, cheapest first:**
1. **Code graders.** Structural invariants (AG-001 to AG-004); right tool, right
   arguments; state after the run matches the expectation. Binary and absolute.
2. **Deterministic numeric reconciliation.** Every number in chat, narrative, grid and
   deck matches a calculation API value for that request, within a stated rounding rule. A
   number with no match is treated as **re-derived**, which breaks the VCC and
   calculation-authority rule, and fails.
3. **LLM judges**, for prose only: groundedness, faithfulness, task adherence. Use
   `azure-ai-evaluation` evaluators run nightly. Binary rubrics rather than 1–5 scales;
   one judge per dimension; the judge may answer "unknown". A judge may gate a release
   only after WP-12 has calibrated it against SME labels.

**Per-agent measures for v0:**

| Agent | Measures |
| ----- | -------- |
| Peer discovery | Recall@10 and overlap against the BCN or Oliver reference peer set. `cap_id` resolution precision. **Null-correctness** (a company absent from the snapshot resolves to null). Fabricated-ID rate, which must be 0 because `resolve()` guarantees it. Stability of the peer set across k runs. Wall clock against the proof-of-concept baseline of 10–12 peers in 3.5–4 minutes |
| Chat assistant | Tool selection and argument accuracy. Task completion, judged by the resulting case state, not by what the reply says. **Narration matches state**: the agent never claims an action the screen does not show (the ADR-005 failure). Citation validity. Correct refusal when a tool refuses |
| Narrative | Numeric reconciliation (grader 2), faithfulness to the analysis, no conclusion the figures do not support |
| Non-GAAP extraction, when it lands | Field-level precision and recall against analyst labels. The prior-art skill is at **70–80%** and degrades as sector conditions accumulate; that is the baseline to beat |

**Non-determinism:**
- Every case runs **k times**: k=3 in the smoke eval, k=5 nightly.
- P0 invariants gate on **pass^k**: every trial passes.
- Quality metrics gate on the mean, with a paired confidence interval against the
  baseline.
- This is CQ-AI-AGT-01 (statistical pass rates over multiple seeds) and CQ-AI-SEC-04
  (deterministic settings where supported).
- Separate *capability* evals, which start low and climb, from *regression* evals, which
  should sit near 100%.

**Golden eval set v0 (WP-06):**
- Seeded from the 10 GLS targets.
- Content:
  - reference peer sets;
  - expected opportunity themes;
  - known-good claims;
  - 20–50 chat tasks drawn from **real failures** in error analysis;
  - negatives: subsidiary or parent confusion, a company not in the snapshot, ambiguous
    names, a private company, and sectors with poor disclosure (oil and gas,
    per [Non-negotiable adjustments](../confluence/oi30/meeting-summaries/non-negotiable-adjustments-in-oi-19751993421.md)).
- Split into a **dev set** that SN may see and a **held-out set** that it may not.
- Versioned. Coverage is measured by bucket (sector, region, failure type), not by case
  count (test plan §5.1).

**Online evaluation after rollout:**
- Foundry continuous evaluation on sampled production traffic, plus partner feedback
  (CQ-AI-PMT-03, SHOULD).
- A comparison of fallback and primary models when the gateway reroutes (OR-AI-QLT-02).

### WS3 — Guardrails and AI security

**Goal:** prove every control blocks what it is meant to block, and keep proving it after
every change. *"Prompt injection is a test suite, not a control"* (Technology Choices
§9.4).

**Guardrail control register v0 (WP-03).** Each control gets a test ID and an owner.

| # | Control | Where | Status | What the test proves |
| - | ------- | ----- | ------ | -------------------- |
| G1 | `cap_id` must come from the offered shortlist | Peer discovery, `resolve()` | Built | An invented ID becomes `unresolved`; an absent company becomes null |
| G2 | Citation check before an answer is shown | Chat assistant | Built, **over-blocks**: web answers are withheld | Unsupported answers are withheld. Once fixed, answers sourced from tools show |
| G3 | Declared tools refuse with a stated reason (ADR-005) | Chat and frontend tools | Built | No narration of an action that was not taken |
| G4 | Services authorise from the signed case grant | Every service | Built | Cross-case and wrong-role tool calls are refused and audited; no side effect |
| G5 | Impersonation needs a role | Foundry agent | Built | Regression |
| G6 | Search filtered to `case_id`, failing closed | AI Search tool ([Document Upload](../confluence/oi30/architecture/document-upload-indexing-and-parsing-with-real-time-progress-architecture-19899351139.md)) | Built | A cross-case retrieval attempt returns nothing (TA-AI-RAG-DA-04) |
| G7 | BFF re-checks access every 60 s; three streams per session | BFF | Built | Revoke access and the stream stops within 60 s; the 429 is handled |
| G8 | **Content Safety / Prompt Shields**, user and document attacks | API Management gateway | Adopted on paper; **path unconfirmed (D6)** | Direct and indirect injection is detected or blocked |
| G9 | PII detection on prompts and responses (CQ-AI-OBS-02) | Gateway | Unknown | Synthetic PII is caught both ways |
| G10 | Egress control on web search (TA-AI-AGT-SBX-02) | Foundry built-in web search | Unknown. **Target names leave Bain through search** | No client-confidential content in outbound queries; no following of URLs the model generated |
| G11 | Run budgets and termination (TA-AI-AGT-CTL-04); denial-of-wallet (OR-AI-COST-01) | Orchestration and gateway (`llm-token-limit`) | Unknown | A runaway loop stops on a machine-checkable condition, within a cost ceiling |
| G12 | Chat panel rendering | UI | Unknown | A model-generated image or link URL is not fetched automatically (an exfiltration route) |
| G13 | Pre-flight gate: conflict of interest, blocked target, residency | Service | **Not built**. Inputs need widening to billing entity and user location ([Greater China](../confluence/oi30/roadmap-business-requirements/opportunity-catalyst-in-greater-china-19853082640.md)) | Deterministic fixtures: aliases, misspellings, subsidiaries of blocked targets |
| G14 | Eval Gate loop-back | Service | **Not built** | The retry cap holds; the cost ceiling holds |

**Threat classes.** The test plan's *"100% named threat classes"* needs named classes. Use
two lists:
- **OWASP Top 10 for LLM Applications 2025**, especially:
  - LLM01 Prompt Injection;
  - LLM02 Sensitive Information Disclosure;
  - LLM06 Excessive Agency;
  - LLM08 Vector and Embedding Weaknesses;
  - LLM09 Misinformation.
- **OWASP Top 10 for Agentic Applications 2026**, especially ASI01 Goal Hijack and ASI02
  Tool Misuse.

Add the agent-specific scenarios Bain's workbook requires (CQ-AI-AGT-03):
- goal hijacking;
- scope creep across steps;
- memory poisoning;
- sub-agent privilege escalation;
- reflection loops;
- side effects from chained tool calls.

**Injection corpus v0 (WP-10).** Built around the two shapes the architecture names,
uploaded documents and retrieved web pages, plus a third:
- **Uploaded documents:** hidden instructions in white text in a PDF, in PPT speaker
  notes, in Excel comments, in Word tracked changes.
- **Retrieved web pages:** poisoned pages fed to the web-search path.
- **Tool and MCP responses carrying instructions:** they must be treated as data
  (TA-AI-MCP-04).

Run the corpus through PyRIT's cross-domain injection (XPIA) workflow, or the Foundry AI
Red Teaming Agent, which wraps PyRIT. Both are in preview; keep them in their own virtual
environment because of a dependency conflict (§12).

**The lethal-trifecta check.** A research agent with case context, untrusted web content
and an outbound search channel has all three ingredients for data exfiltration. G10 is the
control that breaks the chain, which makes it the highest-value item in this workstream
after G8.

**Conventional application security** stays as in Technology Choices §9.4: CodeQL,
Dependabot, secret scanning, Trivy, nightly ZAP. Add one concrete check now: secrets reach
the apps from GitHub Environment secrets, and staging **reuses dev's database role names
and passwords** (Deployment Tracker). That should be a recorded finding with an expiry,
not a silent acceptance.

### WS4 — Deterministic and data (SN-owned; Bain verifies)

The test plan §7.5–7.6 covers this well. Scope it to what is built:
- **Calculation golden fixtures from BCN's pre-calculated GLS results.** The default
  journey shows BCN's figures without recalculating, so the fixture is *the engine
  recalculates BCN's numbers exactly*.
- **Recalculation after a peer change** (S4-12): peers missing a metric are excluded,
  **and that is visible to the user**, not silent.
- **Hypothesis property tests** on unit and currency invariants and on cycle rejection.
- **Trace replay** once completed cases exist.
- **BM25 matcher regression.** It is deterministic, so it gets exact assertions. Include
  the case where a company is absent from the snapshot: min-max normalisation makes the
  top hit score 1.000 regardless.

The testing engineer's role here is to audit that these gates are **enforced** in CI, not
to write them.

### WS5 — Non-functional

| Assertion | Target and source | Method |
| --------- | ----------------- | ------ |
| Synchronous API path | 2 s at p95. *An SN assumption, not a Bain requirement*; this test makes it a commitment (Technology Choices §9.5) | k6 or Locust in Azure Load Testing |
| Full run, end to end | Under 30 minutes (Vision) | Scenario against a reference case |
| First partial result | Within 30 s | Playwright timing (WS1) |
| Streaming | Time to first token, time between tokens and time to last byte, measured separately | A streaming load client; a plain request duration hides time to first token |
| Concurrency at rollout | 50+ partners. The concurrency figure is **not written anywhere**, so it needs a decision | Load scenario on shared Postgres compute, which is accepted only *"for now"* |
| Model rate limits | Behaviour when Foundry returns 429 | Fault injection at the gateway or a mock. No Chaos Studio fault exists for Azure OpenAI |
| Fallback model | *"Fallbacks MUST be tested"* (TA-AI-MOD-03). **No fallback is documented** | Flag as a gap; test once defined |
| SSE settings | Heartbeat 15 s, BFF maximum 60 s, Front Door timeout 120 s: dependent values, regression-tested together | Configuration assertion plus the 4 October probe, automated |
| Cost per run | Tokens and cost per completed case, from the gateway's token metrics | Budget asserted on every eval run |

The NFR Design page is blank, so every threshold except WCAG 2.2 AA, the 2 s figure and
the 30-minute target is **unknown, not "no requirement"**. Each needs a decision before it
can gate anything (D4 approach: baseline first, then set).

### WS6 — Human review and domain acceptance

- **SME panel.** BCN for methodology correctness, plus 2–3 partners for usefulness. The
  September user testing with six partners
  ([Design requirements cont.](https://bainco.atlassian.net/wiki/spaces/OI30/pages/19808256031))
  is the precedent and the obvious pool.
- **Rubric.** Binary checks per dimension:
  - correctness;
  - completeness;
  - defensibility (*"could I say this to a CEO?"*);
  - transparency (*"can I see why?"*).

  One principal SME arbitrates disagreements so the panel does not stall.
- **Calibration (WP-12).** SMEs label 100–200 outputs. Measure the judges' true-positive
  and true-negative rates against those labels. A judge does not gate a release until it
  agrees with the SMEs. Re-check whenever the judge's model, prompt or rubric changes,
  because rubrics drift as reviewers see more outputs.
- **Bain's workbook requirement.** Human review is mandatory for AI output used in
  financial decision contexts (SD-AI-RAI-05). OpCat's output informs client conversations
  rather than making decisions. Whether this applies is an ARC answer to record, not to
  assume.

### WS7 — Release governance and evidence

- **One release evidence page per release**, following the test plan §16 and §20
  checklists, ending in a **recorded go/no-go**. The GLS go/no-go was never written down
  ([standing agenda](../context/standing-agenda.md) item 1). This workstream prevents a
  repeat.
- **Each test suite maps to the AI Architecture Requirement IDs it evidences** (§9), so
  testing answers ARC rows as a by-product.
- **AI incident triage with severity tiers** (SD-AI-OPS-01 and SD-AI-OPS-03). The test
  plan §15 severity table is a good start; extend it to production incidents.

---

## 7. Gates, reconciled

| Stage | Runs | Effect |
| ----- | ---- | ------ |
| PR, any change | SN: unit, component, contract, lint, CodeQL, secret scan, FastMCP tool tests | Blocks merge |
| **PR touching prompts, tool schemas, agent configuration or model deployment** (path-filtered) | All of the above, **plus the smoke eval**: 20–30 dev-set cases, k=3, code graders and invariants only, under about 10 minutes | **Blocks merge.** Satisfies CQ-AI-PMT-02 |
| Merge to main | Integration on the deployed substrate (D10), calculation golden fixtures, property tests, image scan | Blocks merge |
| Deploy to staging | Playwright acceptance journeys, axe, numeric reconciliation, injection corpus | Blocks promotion |
| Nightly | Full dev-set regression, k=5, with judges; ZAP; trace replay; load smoke; red-team scan | Alerts, escalates by policy |
| **Model or provider change** (new deployment or version) | Full regression plus the held-out set, before the switch in staging | Blocks the switch. Keeps T14's protection |
| Pre-release | Held-out set; SME panel; full red team; full performance scenario; resilience drills | Blocks release |
| Production | Structural invariants on every run; sampled online evaluation | Fails the run; raises an incident |

The smoke eval deliberately uses **code graders only**. It is cheap, fast and
deterministic enough to block a merge without the model-variance problem T14 was written
to avoid.

---

## 8. Phased plan and work packages

These dates assume the two-week cadence holds: Sprint 4 started 12 October, so Sprint 5
runs 26 Oct – 6 Nov, Sprint 6 runs 9–20 Nov, and Sprint 7 runs 23 Nov – 4 Dec. The
rollout window falls in or just after Sprint 7.

### Phase 0 — Sprint 5: foundations

| WP | Output | Done when |
| -- | ------ | --------- |
| **WP-01** Test inventory | For each §9.7 gate: specified, implemented, **enforced** in CI. Read access to SN's repos and Actions | Table published; gaps raised to SN as requests |
| **WP-02** Agent version manifest | A specification of what SN emits per run and per trace: prompt hash, tool schema version, model deployment, Foundry project | SN has accepted the spec; it is visible in one trace |
| **WP-03** Guardrail register | §6 WS3 table, maintained, with an owner per control | Every control has a status and a test ID; D6 answered |
| **WP-04** Harness skeleton | A Bain repo (D2): runner, task and trial schema, result store, pass^k report, manifest tagging | One peer-discovery case runs k=3 end to end against staging |
| **WP-05** Error analysis, round 0 | 30–50 traces from dev and GLS rehearsal, open-coded with an SME into a failure taxonomy | Taxonomy written; each category has at least one seed case |

### Phase 1 — Sprint 6: first suites running

| WP | Output | Done when |
| -- | ------ | --------- |
| **WP-06** Golden eval set v0 | §6 WS2 scope, a dev and held-out split, versioned | BCN signs off the reference sets; bucket coverage reported |
| **WP-07** Smoke eval in SN CI | A published action or container; a path filter agreed with SN | Blocks a deliberately broken prompt PR in a dry run |
| **WP-08** Numeric reconciliation | Extract figures from UI, narrative and deck; match them to calculation API values | Runs on staging deploy; zero unmatched figures on the GLS cases |
| **WP-09** Acceptance journeys | §6 WS1 journeys in both stream modes, plus axe | Green on staging, with audit and provenance assertions |
| **WP-10** Injection corpus v0 and first red-team run | §6 WS3 corpus; PyRIT XPIA or the Foundry Red Teaming Agent | Findings triaged; attack-class coverage reported |
| **WP-11** Performance baseline | §6 WS5 measurements on staging | Baseline published; thresholds proposed for D4 |

### Phase 2 — Sprint 7: release readiness

| WP | Output | Done when |
| -- | ------ | --------- |
| **WP-12** Judge calibration | SME-labelled sample; true-positive and true-negative rates per judge | Judges that agree with SMEs are approved to gate; the rest stay advisory |
| **WP-13** Human review, round 1 | SME panel on the held-out set | Rubric scores recorded; findings fed back into cases |
| **WP-14** Pre-release red team | Full corpus plus agent-specific scenarios (CQ-AI-AGT-03) | No unresolved release-blocking finding |
| **WP-15** Resilience drills | Foundry 429 and outage, source outage, SSE reconnect, expired cursor | No fabricated success; bounded retries; failures shown to the user |
| **WP-16** Release evidence and go/no-go | §6 WS7 page; ARC rows answered from evidence | Go/no-go **recorded** by the named authority |

### Phase 3 — after rollout

- Online evaluation sampling.
- Turning production failures into new cases.
- Model-swap regression.
- Growing the held-out set across sectors.
- Bringing the Eval Gate, pre-flight gate, Skeptic and the other drawn agents into scope as
  each is built.

**Capacity, estimated rather than sourced:**
- **One testing engineer, full time**, is enough for Phases 0–2.
- **SME time is the binding constraint:**
  - about 2–3 analyst days for golden set v0;
  - about 1 day per human-review round;
  - about 1–2 hours per sprint for error analysis.

  Book it now. Sprint 3's evidence is that access grants set the burn curve, and SME time
  is the same kind of dependency.

---

## 9. Evidence this produces for the ARC assessment

| Workstream | AI Architecture Requirement IDs it evidences |
| ---------- | -------------------------------------------- |
| WS2 Agent evaluation | CQ-AI-PMT-02, CQ-AI-PMT-03, CQ-AI-AGT-01, CQ-AI-SEC-04, OR-AI-QLT-01, OR-AI-QLT-02, TA-AI-AGT-PLN-02, SD-AI-AGT-03 |
| WS3 Guardrails and security | CQ-AI-SEC-01, CQ-AI-AGT-03, SD-AI-RAI-03, TA-AI-MCP-04, TA-AI-RAG-DA-04, TA-AI-AGT-SBX-02, TA-AI-AGT-CTL-01, TA-AI-AGT-CTL-04, TA-AI-AGT-MEM-02, AD-AI-CFG-02, CQ-AI-OBS-02, OR-AI-COST-01 |
| WS1 UI | AD-AI-UX-03 (inline citations), AD-AI-UX-06 (graceful refusals, no leaked model errors) |
| WS5 NFR | TA-AI-MOD-03 (tested fallback), TA-AI-MOD-07 (context bounding) |
| WS6 Human review | SD-AI-RAI-05 |
| WS7 Governance | SD-AI-OPS-01, SD-AI-OPS-03, SD-AI-AGT-01 (autonomy classification, D7) |

That is about 30 rows, each answered with evidence rather than by assertion. Most are
MUSTs.

---

## 10. Risks to the plan

| Risk | Mitigation |
| ---- | ---------- |
| SME time is not booked, so golden set v0 slips and loop 3 has nothing to compare against | D5 now, with named hours |
| The Content Safety path does not exist for agent calls | D6 before WP-10. If absent, it becomes a security finding, not a test gap |
| The vendor tunes to the eval set | Held-out set (D2) and dev-set rotation |
| Judges disagree with SMEs | Judges stay advisory until WP-12 passes them |
| Eval cost grows unchecked | Code graders first; judges nightly only; a gateway token budget per run |
| The GLS data set cannot legally sit in test | D8; fall back to synthetic companies plus a licensed pinned snapshot |
| Preview-status tooling changes under us (Foundry agent evaluators, Red Teaming Agent, Agent Framework evals are `@experimental`) | Pin versions; the harness owns its own task and result schema, so an evaluator can be swapped out |
| The plan claims coverage for unbuilt components | §4 rule: no coverage reported for anything not built |

---

## 11. Sage — pending

Not run, because the Sage connector is not loaded in this session. Each query could change
a decision:

| Query | Could change |
| ----- | ------------ |
| A Bain standard for testing and evaluating LLM and agent products: a Responsible AI review, a red-teaming process, Andromeda or TSG eval requirements, and their owners | D1, D9, WS3. There may be a mandated tool or process that overrides PyRIT or promptfoo choices |
| How other Bain AI products (Sage/Glean, Signal / NGGS, Cortex) were tested and evaluated, and what they learned | WS2 harness shape; possibly a reusable harness |
| SN's OpCat QA artefacts: OI3-230 and OI3-227 outputs, the tech-debt register, the security scan framework | WP-01 scope. It may already be partly done |
| Domain reviewers: BCN contacts on the cost-bar methodology, Oliver (S4-52), partners from the September testing | D5, WS6 panel |
| An owner and process for answering the AI Architecture Requirements workbook | WS7 format and §9 |

---

## 12. External sources

The research subagent could not open several sites directly. Claims marked † come from
search excerpts of the primary page, not a full read.

- Anthropic, *Demystifying evals for AI agents* (Jan 2026): tasks, trials and graders;
  start with 20–50 real failures; capability versus regression evals; grade outcomes, not
  paths; read transcripts. <https://www.anthropic.com/engineering/demystifying-evals-for-ai-agents>
- Anthropic, statistical approach to model evals: paired differences and confidence
  intervals. <https://www.anthropic.com/research/statistical-approach-to-model-evals>
- τ-bench, the pass^k metric. <https://arxiv.org/abs/2406.12045>
- Husain and Shankar, evals FAQ†: error analysis first; binary over Likert scales.
  <https://hamel.dev/blog/posts/evals-faq/>. Shankar et al., criteria drift.
  <https://arxiv.org/abs/2404.12272>
- `azure-ai-evaluation`: agent, groundedness and indirect-attack evaluators. Agent
  evaluation is still marked preview on Learn†. <https://pypi.org/project/azure-ai-evaluation/>
- Foundry continuous evaluation† and the AI Red Teaming Agent†.
  <https://learn.microsoft.com/en-us/azure/ai-foundry/how-to/continuous-evaluation-agents> ·
  <https://devblogs.microsoft.com/foundry/assess-agentic-risks-with-the-ai-red-teaming-agent-in-microsoft-foundry/>
- Microsoft Agent Framework evaluation API (`evaluate_workflow`, `LocalEvaluator`), read
  in the 1.23.0 source and marked `@experimental`.
  <https://pypi.org/project/agent-framework-core/>
- Prompt Shields, user and document attacks†; MSRC on indirect prompt injection.
  <https://learn.microsoft.com/en-my/Azure/foundry/openai/concepts/content-filter-prompt-shields> ·
  <https://www.microsoft.com/msrc/blog/2025/07/how-microsoft-defends-against-indirect-prompt-injection-attacks>
- OWASP Top 10 for LLM Applications 2025† and Top 10 for Agentic Applications 2026†.
  Confirm the ASI names at source. <https://genai.owasp.org/llm-top-10/> ·
  <https://genai.owasp.org/resource/owasp-top-10-for-agentic-applications-for-2026/>
- PyRIT cross-domain injection (XPIA) workflow. <https://microsoft.github.io/PyRIT/latest/code/executor/workflow>
- Willison, the lethal trifecta. <https://simonwillison.net/2025/Jun/16/the-lethal-trifecta/>
- FinanceBench: numeric hallucination in financial QA. <https://arxiv.org/abs/2311.11944>
- Playwright mocking (no streaming in `route.fulfill`) and accessibility testing.
  <https://playwright.dev/docs/mock> · <https://playwright.dev/docs/accessibility-testing>
- MSW `sse()`. <https://mswjs.io/docs/sse/>
- AG-UI Dojo testing with Agent Framework†.
  <https://learn.microsoft.com/en-us/agent-framework/integrations/ag-ui/testing-with-dojo>
- AG Grid testing guidance. <https://www.ag-grid.com/react-data-grid/testing/>
- FastMCP testing. <https://gofastmcp.com/deployment/testing>
- Schemathesis with FastAPI. <https://schemathesis.readthedocs.io/en/stable/guides/python-apps/>
- APIM GenAI gateway: token limits and metrics†.
  <https://learn.microsoft.com/azure/api-management/genai-gateway-capabilities>
- promptfoo indirect-injection plugin. Note that OpenAI agreed to acquire Promptfoo in
  March 2026, which is a neutrality consideration if it is adopted.
  <https://promptfoo.dev/docs/red-team/plugins/indirect-prompt-injection>
