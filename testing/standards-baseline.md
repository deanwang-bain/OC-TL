# OpCat code quality and testing — the standards baseline

**Status:** Proposal for Tech Lead sign-off · **Prepared:** 2026-10-28 · **Revised:**
2026-10-28, after a Sage search run by the Tech Lead

**Purpose:** fix the goal post that [strategy.md](strategy.md) aims at, before the testing
engineer starts. "Good enough" should be judged against a named standard, not against
whatever the vendor's pipeline happens to do.

**The rule:** where Bain has a source, it wins. External standards fill only the areas Bain
leaves blank.

**Where the Bain material came from.** The Tech Lead ran Sage and passed the results here,
because the connector was not loaded in this workspace's sessions. Dates are Sage's
*updated* dates. Owners are Sage's owner field unless stated otherwise. Links are
Bain-internal.

---

## 1. Is there a Bain guide?

**Bain has security standards and build guidance, but no firm-wide engineering, QA or
testing standard.** Sage found:
- no firm-wide code-coverage threshold;
- no Definition of Done for vendor-built software;
- no AI/LLM testing standard;
- no Andromeda guidance.

What exists falls into four groups.

### TSG security standards — mandatory

| Source | Updated · owner | What it requires for testing and code quality |
| ------ | --------------- | --------------------------------------------- |
| [Application Security](https://bainandcompany.sharepoint.com/sites/GlobalTSGSecurity/SitePages/Application--Security.aspx) | 2025-03-24 · signed David Wiggs | For public or client-facing apps: **SAST on each PR**, **SCA before merge to a production branch**, **DAST before any production release**. Remediation within **10 / 30 / 90 / 180 days** for Critical / High / Medium / Low. Annual third-party pen test for public or client-facing apps; names TrustedSec; Bain is not licensed for Rapid7 InsightAppSec |
| [SDLC Guidance](https://bainandcompany.sharepoint.com/sites/GlobalTSGSecurity/SitePages/SDLC-Guidance.aspx) | 2025-11-06 (footer says 5 Nov 2024) · Gordon Morrison | *"No product should enter into production with any critical vulnerabilities."* Scan with Snyk and CodeQL |
| [Secure Design Principles](https://bainandcompany.sharepoint.com/sites/GlobalTSGSecurity/SitePages/Secure-Design-Principles.aspx) | 2025-09-24 · no owner field; contact secAE@bain.com | No testing rules. Dev, Test, Staging and Prod must be separated; incident response plans must be tested |
| [API Security Guidance](https://bainandcompany.sharepoint.com/sites/GlobalTSGSecurity/SitePages/API-Security-Guidance.aspx) | 2023-11-14 · signed Jeremiah Salamon | No testing section. Input validation, rate limiting, regular secret scans, OWASP API Top 10 alignment |
| [Data Handling Matrix](https://baincoprod.service-now.com/hub?id=kb_article&sysparm_article=KB0019458), "SDLC & Vulnerability Mgmt" row | 2026-03-02 · Mark Waugh | Written as a **vendor** requirement. **Confidential and Prohibited:** SAST and DAST at minimum after major code changes, monthly vulnerability assessments, a UAT or pre-production environment, **semi-annual third-party penetration testing**. **Non-Public:** annual vulnerability assessment and pen test |
| [Data Classification Standard v4.0](https://bainandcompany.sharepoint.com/sites/GlobalTSGSecurity/SiteAssets/SitePages/Data-Classification(1)/2024-STANDARD--Data-Classification-Standard.pdf?web=1) | 13 Feb 2024 · Mark Waugh, CISO-approved | Four tiers: Public, Non-Public, Confidential, Prohibited/Regulatory. **The tier decides which Matrix row applies** |
| [Penetration Testing Program](https://bainandcompany.sharepoint.com/sites/GlobalTSGSecurity/SitePages/Penetration-Testing-Program.aspx) | 2023-03-16 · John Clary, Security Risk & Compliance | Scoping questionnaire to SecRisk, who coordinate the third party. **Lead time 4–8 weeks** from questionnaire to test start; report **10 business days** after testing. The figure is from 2023, so confirm it with secrisk@bain.com |
| [Security requirements for public endpoints](https://baincoprod.service-now.com/hub?id=kb_article&sysparm_article=KB0028388) | 2026-08-13 · Jordi Price | Remediate Wiz critical and high findings *"within 48 hours"* |
| [Security Tools](https://bainandcompany.sharepoint.com/sites/GlobalTSGSecurity/SitePages/Security-Tools.aspx) and [Wiz CNAPP KB](https://baincoprod.service-now.com/hub?id=kb_article&sysparm_article=KB0018937) | 2025-03-24 and 2026-02-09 | Snyk, Wiz and GitHub Advanced Security are licensed. **Wiz is not currently used for code scanning** |
| [Approved Tools 2024.08.15](https://bainandcompany.sharepoint.com/sites/EnterpriseArchitecture/_layouts/15/Doc.aspx?sourcedoc=%7B12131D0A-68C1-4B95-AB06-73775F7CB34A%7D&file=Approved+Tools+2024.08.15.pptx&action=edit&mobileredirect=true&web=1) | 2026-10-21 · Ed Moore. *Search snippets only; the deck was not opened* | Wiz *"Required"*; **SonarQube Enterprise *"Requires Approval"*** |

### Build practice guidance — Bain practice, not a standard

| Source | What it sets |
| ------ | ------------ |
| [Guide to "Well Operated" Software Build Case](https://bainandcompany.sharepoint.com/sites/pubs/_layouts/15/Doc.aspx?sourcedoc=%7B924D0256-F1AC-4BBC-8549-412C2667043F%7D&file=Guide+to+%E2%80%9CWell+Operated%E2%80%9D+Software+Build+Case.pptx&action=edit&mobileredirect=true&web=1) (AIS, 2026-09-14; creator Jacob O'Farrell) | **Unit coverage of ~80–90%** on production builds. **PRs with at least 2 reviewers.** A Definition of Done: unit tests, a coverage report, pre-commit checks, static analysis with no high or critical issues, an approved PR, product-owner sign-off. Tasks must *"demonstrate automated security and functional tests"* |
| SDLC Training deck (2024, pubs) | **More than 70% unit coverage, more than 80% on new code** |

### Responsible AI governance — mandatory process, not test criteria

| Source | What it requires |
| ------ | ---------------- |
| [AI Responsible Use Policy](https://baincoprod.service-now.com/hub?id=policy_esc_kb_article_view&sysparm_article=KB0027990) (revised 14 May 2026; owner: Chair of the Responsible AI Council) | Internally built AI tools need **AI Data Governance Committee review** plus an **Information Security Architecture Review**. Prohibited or high-risk tools go to Bain Legal, which decides whether an AI Impact Assessment is needed |
| [Hardening AI Applications](https://bainandcompany.sharepoint.com/sites/GlobalTSGSecurity/SitePages/Hardening-AI-Applications.aspx) (2024-11-05, Gordon Morrison) | Guidance only: adversarial training, bias detection, output sanitising, model monitoring. No pass/fail criteria |

### Architecture requirement sets — mandatory review floor

These are the closest thing to an AI testing standard.

| Source | What it adds |
| ------ | ------------ |
| ARC v2 and [AI_Architecture_Requirements v2.1](https://bainandcompany.sharepoint.com/sites/GlobalOpportunityIndicator-OI3.0Development/_layouts/15/Doc.aspx?sourcedoc=%7BD341ABFA-8776-4DFA-9832-EAE269E15E93%7D&file=AI_Architecture_Requirements+v2.1.xlsx&action=default&mobileredirect=true&web=1) (file owner Sandeep Uppal; the governing owner is not established) | The rows in the first version of this document, unchanged: CQ-01, CQ-05, AD-22, SD-06, SD-15, CQ-AI-PMT-02, CQ-AI-AGT-01 and -03, CQ-AI-SEC-01, SD-AI-RAI-03. **The ARC framework's owner was not found** |
| [fw-bain-app-ai-review-pack](https://bainandcompany.sharepoint.com/sites/EnterpriseArchitecture/Shared%20Documents/Architecture%20documentation/Signal%20Support%20Chatbot%20(AI-1884)/fw-bain-app-ai-review-pack%20(1).md?web=1) (Enterprise Architecture export of the "Bain Application Framework", 2026-07-29) | **The best guide found on how to evidence a row.** Each requirement has an owner and a *Verify* checklist, for example `REQ-INPUT-VALIDATION`: *"Automated tests cover prompt, SQL, and code-execution injection."* Also `REQ-PRELAUNCH-TESTING`, `REQ-AI-PREDEPLOY-EVAL` (advisory) and `REQ-AI-REVALIDATION` (advisory). Whether this is the same framework as ARC is not confirmed |
| [Archie and the Innovation Enablement Process](https://baincoprod.service-now.com/hub?id=kb_article&sysparm_article=KB0028257) (2026-08-13, Jordi Price) | The review process around these requirement sets. It cites an "IEP Questions & Standards workbook v2026.05.15", which was not found |

**One observation for the brief.** Sage found
`OppCat_Architecture_Assessment_Tracker_Reviewed_filled.xlsx` in the Tech Lead's OneDrive.
The mirror holds the unfilled version, which is where the brief's *"0 responses
recorded"* comes from. If the filled copy carries responses, that line is stale.

---

## 2. The goal post, row by row

| # | Area | **Bain source (wins)** | External reference (only where Bain is silent) | What it means for OpCat |
| - | ---- | ---------------------- | ---------------------------------------------- | ----------------------- |
| 1 | Testing process and documentation | None found | **ISO/IEC/IEEE 29119** Parts 2–4 (2021; Part 1 2022) | Strategy, per-release test plan and completion report follow 29119-3 structure. The [Agent Validation Test Plan](../confluence/oi30/architecture/agent-validation-test-plan-19765133323.md) already broadly does |
| 2 | Testing AI systems | AI workbook rows; framework pack `REQ-PRELAUNCH-TESTING`, `REQ-AI-PREDEPLOY-EVAL`, `REQ-AI-REVALIDATION` | **ISO/IEC TS 42119-2:2025** for the method | Bain says *what* must be evaluated; 42119-2 frames *how*, risk-based |
| 3 | Quality characteristics (NFRs) | None found. The NFR page is blank | **ISO/IEC 25010:2023** | Nine characteristics become nine explicit rows in strategy WS5: each gets a threshold, "baseline first", or "not applicable" with a reason |
| 4 | **Code quality and Definition of Done** | **AIS "Well Operated" guide**: ~80–90% unit coverage, at least 2 reviewers, DoD. **SDLC Training**: >80% on new code | Sonar way thresholds (80% new-code coverage, ≤3% duplication) as a tooling reference; ISO/IEC 5055 if a contract clause is ever needed | **≥80% coverage on new deterministic code**, which is the floor every Bain source agrees on. Calculation engine at the AIS upper bound, ~90%. Agent code is judged by evals, not coverage. AIS DoD becomes SN's story DoD, with an eval-delta for agent-affecting stories |
| 5 | **Application security** | **TSG Application Security, SDLC Guidance, API Security Guidance, Data Handling Matrix, public-endpoints KB** | **OWASP ASVS 5.0 L2** as the requirement-level checklist TSG does not provide | Gates and SLAs come from TSG (§3). ASVS supplies the test cases. Cite requirements as `v5.0.0-x.y.z` |
| 6 | AI security testing | AI workbook CQ-AI-SEC-01, CQ-AI-AGT-03, SD-AI-RAI-03; framework pack `REQ-INPUT-VALIDATION`; Hardening AI Applications (guidance) | **OWASP AI Testing Guide v1** (Nov 2025); OWASP Top 10 for LLM Apps 2025 and for Agentic Apps 2026 as the threat classes | Bain names the obligation, AITG supplies the test method |
| 7 | Secure development lifecycle | **TSG SDLC Guidance; Secure Design Principles** (environment separation, tested incident-response plans) | **NIST SP 800-218A** for AI-specific practices only | — |
| 8 | AI governance and risk | **AI Responsible Use Policy**: AI Data Governance Committee review and InfoSec Architecture Review | NIST AI 600-1, only as framing for what evals measure | The two reviews are **release prerequisites** (§3, gap G2) |
| 9 | Accessibility | ARC AD-01, AD-07 | **WCAG 2.2 AA** | Unchanged |
| 10 | **Penetration testing** | **Pen Testing Program, Application Security, Data Handling Matrix** | — | Cadence depends on row 11. Lead time drives decision S3 |
| 11 | **Data classification** | **Data Classification Standard v4.0 + Data Handling Matrix** | — | OpCat must be classified. That fixes rows 5 and 10 and the test-data rule (SD-15) |

**Tester competence:** ISTQB CT-AI v2.0, on top of Foundation Level. A skills marker for
briefing the testing engineer, not a gate.

**Not adopted:** ISO/IEC 42001 (an organisation-level certification); ASVS L3 across the
board; EU AI Act conformity testing (an ARC answer to record, not assume); IEEE 829
(superseded).

---

## 3. What this changes in the strategy

### Gaps that now have a Bain source

**G1 — The pen test cannot report before the rollout.**
- The process lead time is 4–8 weeks from questionnaire to test start, plus 10 business
  days to the report.
- A questionnaire sent this week puts the earliest test start in late November and the
  earliest report in mid-December.
- That is after the rollout window either way: test start lands around the rollout itself,
  and the report after it.
- The cadence may also be **semi-annual, not annual**. That is the rule if OpCat is
  Confidential or Prohibited (row 11), and with uploads that may carry MNPI, it likely is.

So the question is no longer *when to book* but *what may go live before the report*.
That is SecRisk's decision, not this workspace's (S3).

**G2 — Two governance reviews may be missing from the plan.** The AI Responsible Use Policy
requires AI Data Governance Committee review and an Information Security Architecture
Review for internally built AI tools. ARC SD-05 asks for the same TSG Security review.
Neither appears in the strategy's release gates, and no page in the mirror records either
one happening. Add both to WS7 as release prerequisites, and confirm their status (S6).

**G3 — DAST must block release.**
- TSG Application Security requires **DAST before any production release**.
- The strategy runs ZAP nightly, with *alerts, does not block* (Technology Choices §9.7).
- Add a blocking DAST run at the pre-release gate.
- The Matrix's *"after major code changes"*, for Confidential and above, points the same
  way.

**G4 — The code-quality gate.**
- PR gate: ≥80% coverage on new deterministic code, static analysis with no high or critical
  findings, and **at least 2 reviewers**.
- The strategy's gate has none of the three.
- WP-01 checks what SN enforces today.

**G5 — Remediation SLAs.** Use TSG's 10 / 30 / 90 / 180 days in the triage policy (strategy
WS7). Use 48 hours for Wiz critical and high findings on public endpoints.
`stg.opcat-nonprod.bain.io` sits behind Front Door, so check whether it counts as a public
endpoint (C5).

**G6 — A pre-production environment.**
- The Matrix requires UAT or pre-production for Confidential and above.
- The only staging today is **GLS-only**: three apps, GLS mode, no case-service
  ([Deployment Tracker](../confluence/oi30/architecture/opportunity-catalyst-architecture-high-level/deployment-design-ai-compute-data-components-cicd/oc-dev-staging-gls-deployment-tracker-19909279789.md)).
- A rollout-grade pre-production environment is needed for the acceptance journeys and the
  pen test to mean anything.

### Conflicts between Bain sources, for TSG to rule

| # | Conflict | Reading, pending a ruling |
| - | -------- | ------------------------- |
| C1 | **Pen-test cadence.** Annual: ARC SD-06, and App Security for public or client-facing apps. **Semi-annual:** Data Handling Matrix, for Confidential and Prohibited | The Matrix is more specific about data and newer. It applies once OpCat is classified Confidential or above |
| C2 | **Pen-test vendor.** Rapid 7: ARC SD-06 and the 2019/2021 questionnaires. **TrustedSec:** App Security 2025, which also says Bain is not licensed for Rapid7 InsightAppSec | App Security is newer. ARC's "via Rapid 7" is probably stale. Confirm with secrisk@bain.com |
| C3 | **Scanning tools.** SDLC Guidance: Snyk and CodeQL. App Security: GHAS and Snyk Open Source. ARC CQ-07: *"transitioning from Snyk to Wiz"*. Wiz KB: Wiz is not used for code scanning. Technology Choices: CodeQL, Dependabot, Trivy, Defender | **SAST** is met by CodeQL/GHAS in every source. **SCA:** TSG names Snyk Open Source, never Dependabot, so ask SN to adopt it or ask TSG to accept Dependabot. **Wiz** is for cloud posture, not code. CQ-07's wording is probably wrong on that point |
| C4 | **SonarQube.** ARC CQ-01 gives it as the example; Approved Tools marks it *"Requires Approval"*; one 2026 Archie submission lists it in a scanner suite | Not required. G4's coverage and smell thresholds can be enforced by the test runners plus CodeQL. Request SonarQube approval only if SN or TSG wants it |
| C5 | **Remediation SLAs.** App Security: 10 / 30 / 90 / 180 days. ARC SD-42: high and critical *"in the sprint following discovery"*. Public-endpoints KB: 48 hours for Wiz critical and high | The strictest applicable one wins, per finding source |
| C6 | **Who owns ARC**, and whether it is the "Bain Application Framework" in the review pack | Unknown. Ask Enterprise Architecture, who exported the pack |

### Corrections to strategy.md

- **D5:** "Oliver" (S4-52) is listed as **(Vendor)** in
  [stakeholders](../context/stakeholders.md). A vendor-side reviewer cannot own reference
  answers for a held-out set. BCN owns the golden set; Oliver can contribute to the dev
  set only.
- **§11, Sage pending:** answered by this section, apart from the items still open in §5.

---

## 4. Decisions requested

| # | Decision | Recommendation |
| - | -------- | -------------- |
| **S1** | Adopt §2: Bain sources win per row, external standards only where Bain is silent | Adopt |
| **S2** | Classify OpCat under Data Classification Standard v4.0 | Propose **Confidential at minimum**, and ask whether MNPI in uploads makes it Prohibited/Regulatory. Mark Waugh's standard; secAE@bain.com to confirm |
| **S3** | Pen test | **Send the SecRisk scoping questionnaire this week.** Ask SecRisk directly whether a 50-partner internal rollout may proceed on internal evidence, with the third-party test booked. That evidence is blocking DAST plus the ASVS L2 test pass. Their answer decides whether the rollout date holds |
| **S4** | Code-quality gate | ≥80% coverage on new deterministic code, ~90% on the calculation engine, no high or critical static-analysis findings, at least 2 reviewers. Enforced with approved tools (C4) |
| **S5** | SCA tool | Raise to TSG: Snyk Open Source as TSG names it, or a recorded acceptance of Dependabot. Log it as a request in `requests/` |
| **S6** | Governance reviews | Confirm the status of the AI Data Governance Committee review and the InfoSec Architecture Review. Treat both as rollout prerequisites |

Once S1 is signed off, strategy.md takes G1–G6 and the corrections, and every test case
carries a trace to its Bain row or standard.

---

## 5. Still open

| Item | Why it matters |
| ---- | -------------- |
| **Secure Code Review Guidance** (not yet opened) | Probably answers ARC CQ-18. `checklists/code-review.md` should align with it |
| **Information Security Architecture Review Process** (not yet opened) | S6 lead time. It may be as long as the pen test's |
| **Application Vulnerability Management** (not yet opened) | C5, the definitive SLA |
| Approved Tools deck, read in full | C3, C4 |
| ARC owner; the IEP Questions & Standards workbook v2026.05.15 | C6, and the format ARC evidence must take |
| Andromeda testing or eval guidance | Nothing indexed. The docs site is referenced in email but not in Sage. Ask the platform team directly |

The first three are worth reading next. Between them they probably settle C5, the
code-review checklist and the S6 lead time.

---

## External sources

- ISO/IEC/IEEE 29119: <https://en.wikipedia.org/wiki/ISO/IEC_29119>
- ISO/IEC TS 42119-2:2025: <https://committee.iso.org/standard/84127.html>
- ISO/IEC 25010:2023: <https://committee.iso.org/standard/78176.html>
- ISO/IEC 5055:2021 (CISQ): <https://www.it-cisq.org/standards/code-quality-standards/>
- SonarQube quality gates:
  <https://docs.sonarsource.com/sonarqube-server/2025.4/quality-standards-administration/managing-quality-gates/introduction-to-quality-gates>
- OWASP ASVS 5.0: <https://owasp.org/projects/asvs>
- OWASP AI Testing Guide v1: <https://owasp.org/www-project-ai-testing-guide/>
- NIST SP 800-218A: <https://csrc.nist.gov/pubs/sp/800/218/a/final>
- NIST AI 600-1: <https://nvlpubs.nist.gov/nistpubs/ai/NIST.AI.600-1.pdf>
- ISTQB CT-AI v2.0: <https://istqb.org/help/ct-ai-v2>
