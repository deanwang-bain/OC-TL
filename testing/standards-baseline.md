# OpCat code quality and testing — the standards baseline

**Status:** Proposal for Tech Lead sign-off · **Prepared:** 2026-10-28

**Purpose:** fix the goal post that [strategy.md](strategy.md) aims at, before the testing
engineer starts. "Good enough" should be judged against a named standard, not against
whatever the vendor's pipeline happens to do.

**Sage was not consulted.** The connector is connected for the org but not loaded in this
session, for the third session running. Everything below on Bain's standards comes from
what the OI30 mirror holds. §5 lists what Sage still needs to answer.

---

## 1. Is there a Bain guide? Partly — a review bar, not a testing standard

**What exists in the mirror** is Bain's formal architecture governance gate, attached to
the [Architecture Assessment Tracker](https://bainco.atlassian.net/wiki/spaces/OI30/pages/19853082681)
page as two workbooks:

| Workbook | Rows | What it covers on quality and testing |
| -------- | ---- | ------------------------------------- |
| [ARC v2](../confluence/_attachments/19853082681/OppCat_Architecture_Assessment_Tracker_Reviewed.xlsx) | 180, including **Code Quality (40)** and **Software Development Principles (47)** | Pipeline gates, secure coding, repository standards, security practice, test data |
| [AI Architecture Requirements v2.1](../confluence/_attachments/19853082681/AI_Architecture_Requirements_v2.1.xlsx) | 133 | Prompt eval in CI, online evaluation, injection testing, agent trajectory evals, red teaming |

The rows that bear directly on testing:

| ID | Requirement, condensed | Priority after the 22 Sept review |
| -- | ---------------------- | --------------------------------- |
| CQ-01 | Quality metrics enforced in CI: **coverage thresholds**, code smells, style (*"e.g. SonarQube"*) | MUST |
| CQ-02 | Security checks in the pipeline; **high and critical defects block delivery** | MUST |
| CQ-03 | Licence and dependency scanning enforced | MUST |
| CQ-04 | Static analysis enforced | MUST |
| CQ-05 | **Unit and integration tests on every PR** | MUST |
| CQ-06 | ZAP dynamic scan on every PR | MUST → SHOULD |
| CQ-07 | Snyk or Wiz continuously (*"Bain is currently transitioning from Snyk to Wiz"*); SonarQube and CodeQL SHOULD | MUST (capability); tool to be decided |
| CQ-09 | A defined promotion process across dev, QA, staging and production | MUST |
| CQ-18 | A code review checklist | MUST |
| AD-07 | Accessibility tested regularly; frequency and method documented | SHOULD |
| AD-22 | **Unit and integration tests cover access-control scenarios** | MUST |
| SD-06 | **Independent penetration test, at least annually, via Rapid 7** | MUST (external dependency) |
| SD-15 | Client data used in test needs **consent, a contract and anonymisation** | MUST (external dependency) |
| SD-41 | A defined bug triage and prioritisation process | MUST |
| CQ-AI-PMT-02 | Prompt changes regression-tested against an eval set **before merge** | MUST |
| CQ-AI-AGT-01 | End-to-end trajectory evals with **statistical pass rates over multiple seeds** | MUST |
| CQ-AI-SEC-01 | Direct and indirect prompt-injection tests in the security pipeline | MUST |
| SD-AI-RAI-03 | Red teaming before launch and periodically after | MUST |

**What it is not.** ARC says *that* things must be tested. It does not say:
- which test levels;
- what coverage number;
- how an AI output is judged good;
- how test evidence is documented.

CQ-01 requires "coverage thresholds" but sets none. The reviewer's own pass recorded that
the framework *"mandates patterns rather than outcomes"*
([brief](../context/oi30-brief.md), ARC section).

**Bain documents ARC cites but the mirror does not hold.** Sage should find these:
- the TSG Secure Design Principles (SD-10, MUST);
- the TSG API Security Guidance (SD-09);
- the TSG Cyber Incident Management Policy (SD-47);
- the Bain Data Classification Standards (SD-18, MUST).

These may be where Bain's real engineering standard lives.

**So: Bain sets the floor, and it is mandatory.** No Bain document in the mirror defines
what "well tested" means above that floor. That needs a commonly established standard (§2).

---

## 2. The proposed goal post

**The rule:**
- **ARC and the AI workbook are the floor.** They are Bain-mandated, so every MUST gets an
  answer with evidence.
- **The standards below define "good"** wherever ARC is silent or only names a pattern.
- **Adopt each standard as a reference, not as a certification target.** Nothing here
  needs auditing or buying a certificate. Each one supplies a structure, a checklist or a
  number that would otherwise be invented.

| # | Area | Goal post | Version (verified 2026-10-28) | Why this one | How OpCat uses it |
| - | ---- | --------- | ----------------------------- | ------------ | ----------------- |
| 1 | **Testing process and documentation** | ISO/IEC/IEEE 29119: Part 2 processes, Part 3 documentation, Part 4 techniques | Part 1 2022; Parts 2–4 2021; Part 5 2024 | The international software testing standard; it superseded IEEE 829. The existing [Agent Validation Test Plan](../confluence/oi30/architecture/agent-validation-test-plan-19765133323.md) already follows its shape: strategy, techniques, entry and exit criteria, coverage | Structure the strategy, the per-release test plan and the completion report on 29119-3 templates. Use 29119-4 names for techniques, as the test plan's §4.1 already does |
| 2 | **Testing AI systems** | ISO/IEC TS 42119-2, *Testing of AI — Overview of testing AI systems* | 2025 (published Nov 2025), a Technical Specification | Applies 29119 to AI systems on a risk basis: exactly the deterministic-plus-probabilistic split OpCat has | The frame for the probabilistic track: risk-based selection of eval practices, with 29119 processes carried over |
| 3 | **Product quality model (NFRs)** | ISO/IEC 25010 | 2023, nine characteristics | The [NFR Design page](../confluence/oi30/architecture/opportunity-catalyst-architecture-high-level/nfr-non-functional-design-choices-19704905798.md) is blank. 25010 gives the checklist of what needs a threshold, so a gap is visible rather than silent | Each characteristic gets a row in WS5: a threshold, "baseline first", or "not applicable" with a reason. Confirm the 2023 names against the standard |
| 4 | **Code quality** | SonarQube **"Sonar way"** quality gate, backed by ISO/IEC 5055 for structural quality | Sonar way: current SonarSource docs. ISO/IEC 5055:2021 | ARC CQ-01 names SonarQube. Sonar way gates **new code** (80% coverage, 3% duplication, security hotspots reviewed), which is fair to an in-flight codebase. ISO 5055 exists to *"set quality targets for contractor code"*, which is exactly a vendor arrangement | The PR quality gate: Sonar way on new code. **Coverage applies to deterministic code only**, as the test plan §5.1 already says. ISO 5055 is the reference if a contractual quality clause is ever needed |
| 5 | **Application security verification** | OWASP ASVS 5.0, **Level 2** | 5.0.0, May 2025 | L2 is the level for apps handling sensitive data; OpCat holds client-confidential data and possibly MNPI. L3 targets high-assurance systems such as financial ones; adopting it wholesale would be over-scoped | Security test cases are traced to ASVS requirement IDs, cited with the version (`v5.0.0-x.y.z`). Raise individual access-control and data-protection requirements to L3 where the case-isolation design needs it |
| 6 | **AI security testing** | OWASP AI Testing Guide; threat classes from the OWASP Top 10 for LLM Applications 2025 and the Top 10 for Agentic Applications 2026 | AITG v1, 26 Nov 2025 | The only established *test methodology* for AI security; it extends the Web Security Testing Guide. The Top 10s give the named threat classes the test plan's adversarial-coverage formula needs | WS3 test cases traced to AITG test IDs; adversarial coverage measured against the two Top 10 lists |
| 7 | **Secure development lifecycle** | NIST SSDF SP 800-218, plus the generative-AI profile SP 800-218A | 800-218 v1.1; 800-218A, July 2024, updated June 2025 | 800-218A has explicit tasks for an *AI system producer*, which is what SN is. It maps cleanly onto ARC's Software Development rows | The practice checklist the ARC SD and SD-AI answers are written against |
| 8 | **AI risk measurement** | NIST AI RMF 1.0, plus the GenAI profile, NIST AI 600-1 | AI 600-1, July 2024 | Its **Measure** function is what the eval loops produce evidence for. Confabulation and information integrity are named risks there | The eval report maps metrics to the AI 600-1 risks they measure. Governance framing only; it is not a test method |
| 9 | **Accessibility** | WCAG 2.2 **AA** | 2.2 | Already in Technology Choices §2 and ARC AD-01 and AD-07. The one non-functional target written anywhere | axe-core in Playwright, plus a documented manual pass (AD-07 asks for frequency and method) |

**Tester competence.** **ISTQB CT-AI v2.0**, which covers testing ML and generative-AI
systems, on top of the Foundation Level certificate. This is a reasonable profile to hire
or brief the testing engineer against. It is a skills marker, not a gate.

### Deliberately not adopted

| Standard | Why not |
| -------- | ------- |
| ISO/IEC 42001 (AI management system) | Certifies an organisation's AI management system, not a product's testing. Bain-level if anything. Whether Bain holds it could not be confirmed publicly; a Sage question |
| ISO/IEC 25010 measurement series (25023) | Too heavy for a project-level baseline; 25010's characteristics are enough |
| ASVS Level 3 across the board | Disproportionate for an internal tool; selective L3 instead (row 5) |
| EU AI Act conformity testing | OpCat informs client conversations; it does not make decisions. Whether any high-risk category applies is an ARC answer (SD-AI-RAI-05, SD-AI-DAT-06) to record, not assume |
| IEEE 829 | Superseded by 29119-3 |

---

## 3. What this changes in the strategy

Holding [strategy.md](strategy.md) against the baseline shows four gaps and two conflicts.

**Gaps:**
1. **No code-quality gate.** Technology Choices §9.4 runs CodeQL but no SonarQube, and the
   strategy's PR gate has no coverage, smell or duplication condition. ARC CQ-01 requires
   one. **Add Sonar way on new code to the PR gate.**
2. **No independent penetration test.** SD-06 requires one at least annually through
   Rapid 7. It is an external dependency, so it needs **requesting now** if it is to land
   before the partner rollout; the Sprint 3 lesson is that access and vendor lead times set
   the pace.
3. **No standard for test documentation.** Adopt 29119-3 for the per-release test plan and
   completion report, which WS7's evidence page becomes.
4. **No NFR checklist.** Row 3 turns the blank NFR page into nine explicit rows in WS5.

**Conflicts to raise with SN:**
5. **Snyk / Wiz versus Dependabot, Trivy and Defender.** ARC CQ-07 says Bain is moving
   from Snyk to Wiz. Technology Choices §9.4 names neither. A tool ruling is needed, or at
   least confirmation that the chosen tools satisfy the capability.
6. **Test data.** SD-15 requires consent, a contract and anonymisation for client data used
   in test. This strengthens decision D8 (may the GLS golden data set seed the evals?) from
   "check" to "must clear before use".

**Re-framing, once signed off:**
- Every test case in the strategy carries **one trace to a standard**: an ARC or AI-workbook
  row ID, an ASVS requirement, an AITG test ID, or a 25010 characteristic.
- The coverage report then answers two questions: *"which mandatory rows have evidence?"*
  and *"how far are we from the goal post?"*

---

## 4. Decision requested

| # | Decision | Recommendation |
| - | -------- | -------------- |
| **S1** | Adopt the §2 baseline as OpCat's goal post: ARC as the mandatory floor, standards 1–9 as the reference for "good" | Adopt |
| **S2** | ASVS level | L2, with selected L3 access-control and data-protection requirements |
| **S3** | Code-quality gate | Sonar way on new code. Coverage applies to deterministic code only |
| **S4** | Request the SD-06 penetration test now, targeting completion before the partner rollout | Request this week |

Once S1 is signed off, strategy.md gets the §3 changes and the per-test-case trace column.

---

## 5. Still needs Sage

| Query | Could change |
| ----- | ------------ |
| The TSG Secure Design Principles, TSG API Security Guidance and Bain Data Classification Standards: their content and owners | Could replace rows 5 and 7 with a Bain standard, which should then win |
| Any Bain or TSG engineering, testing or QA standard: test levels, coverage numbers, a definition of done for vendor-built software | Could replace rows 1, 3 and 4 |
| Any Bain Responsible AI review process or AI testing standard (Andromeda, TSG) | Could replace rows 2, 6 and 8 |
| The status of the Snyk-to-Wiz transition, and whether SonarQube is a Bain-provided service | Conflict 5; S3 tooling |
| Who books the Rapid 7 penetration test, and the lead time | S4 |

**Rule if Sage finds a Bain standard:** it replaces the external one in the same row. The
external standards are the fallback, not a preference.

---

## Sources

- ARC v2 and AI Architecture Requirements v2.1 workbooks, on the
  [Architecture Assessment Tracker](https://bainco.atlassian.net/wiki/spaces/OI30/pages/19853082681)
  page.
- ISO/IEC/IEEE 29119 editions: <https://en.wikipedia.org/wiki/ISO/IEC_29119> ·
  <https://www.evs.ee/en/iso-iec-ieee-29119-1-2022>
- ISO/IEC TS 42119-2:2025: <https://committee.iso.org/standard/84127.html> ·
  <https://www.evs.ee/en/iso-iec-ts-42119-2-2025>
- ISO/IEC 25010:2023: <https://committee.iso.org/standard/78176.html>
- ISO/IEC 5055:2021 (CISQ): <https://www.it-cisq.org/standards/code-quality-standards/>
- SonarQube quality gates, Sonar way:
  <https://docs.sonarsource.com/sonarqube-server/2025.4/quality-standards-administration/managing-quality-gates/introduction-to-quality-gates>
- OWASP ASVS 5.0: <https://owasp.org/projects/asvs> ·
  <https://github.blesdmm.dns-dynamic.net/OWASP/ASVS/blob/master/CONTRIBUTING.md>
- OWASP AI Testing Guide v1: <https://owasp.org/www-project-ai-testing-guide/>
- NIST SP 800-218A: <https://csrc.nist.gov/pubs/sp/800/218/a/final>
- NIST AI 600-1: <https://nvlpubs.nist.gov/nistpubs/ai/NIST.AI.600-1.pdf>
- ISTQB CT-AI v2.0: <https://istqb.org/help/ct-ai-v2>
