# Opportunity Catalyst in Greater China

**Status:** Draft for review · **Owner:** Dean Wang (Tech Lead) · **Last updated:** 22 September 2026
**Decision needed:** Confirm the scope exclusion for mainland China, and decide whether to commission a localisation feasibility study.

---

## Summary

- **Mainland China: the tool cannot be used today.** Three independent blockers, any one of which is sufficient on its own.
- **Hong Kong: not blocked, but not cleared either.** The data question is satisfied; the AI question depends on a model-routing decision that has never been written down.
- **Localisation is feasible, but it is a second product, not a setting.** None of the proposed workarounds is a dead end. Together they amount to building and operating a separate China version.
- **There is precedent.** Sage went through China-specific development to localise, so the firm has walked this path before. A China engineering team can be mobilised if leadership wants to pursue it.
- **The useful question is firm-wide, not tool-specific.** Every blocker below is a Bain platform problem that any Reinvention tool will hit identically.

---

## 1. What we assessed against

Bain's regional AI guidance sets three rules:

| # | Rule | Region |
| - | ---- | ------ |
| 1 | AI features enabled by a global LLM (OpenAI, Claude, Azure AI) must be **turned off**, for **both Bain internal users and clients**. Global providers are not registered with the Chinese authorities; only tools on locally supported China models are permitted for case work | Mainland China |
| 2 | The client must **acknowledge and consent** to data being transferred outside mainland China, with a stated clause in the SOW. Mainland-billed cases default to **China Cloud** | Mainland China |
| 3 | AI features: **case-by-case check required**. Some global models are supported in region (Azure AI / Copilot); **OpenAI- and Claude-backed features must still be off**, as both vendors prohibit use in the region. Data transfer: no additional client consent where the case is billed out of Hong Kong, as HK-billed cases default to **Bain Global Cloud** | Hong Kong |

> **Caveat worth stating.** That guidance was written for Signal / NGGS, a product deployed into client environments. Opportunity Catalyst is a partner-facing internal tool whose output is a deck, not a service clients log into. That difference removes the stated *reason* behind rule 1 (a client cannot directly access the AI service), but not the *rule*, which says "both Bain internal users and clients" explicitly. No page in this space states a China position, so this is the nearest written rule and is treated as binding until its owner says otherwise. **Confirming that is the first action below.**

---

## 2. Where we stand today

| | Mainland China | Hong Kong |
| --- | --- | --- |
| **Data residency** | Cases billed in mainland China sit on Bain's China Cloud by default. Opportunity Catalyst runs entirely from a single US region, so every run moves client data offshore. That requires written client consent plus a data-transfer clause in the SOW before work can start. | Cases billed out of Hong Kong sit on Bain's Global Cloud by default, which is where Opportunity Catalyst already runs. No additional client consent and no SOW clause are needed. |
| **Server accessibility** | There is no mainland deployment and no design to support one. Serving mainland cases would mean standing up a second, separate instance of the platform on a different cloud: a new build, not a regional setting. | Nothing to change. Hong Kong users reach the same platform, the same sign-on and the same network as every other office. |
| **LLM availability** | Global LLMs (OpenAI, Claude, Azure AI) must be off for Bain staff and clients alike. All three are in the current design, and only locally supported Chinese models are permitted. The AI here is not a toggle: switch it off and no product remains. | OpenAI- and Claude-backed features must be off, as both vendors prohibit use in the region. Azure AI and Copilot may be permitted. Which models the tool actually calls is set at deployment and has never been written down, so this cannot be answered yet. Case-by-case clearance is required regardless. |
| **Data sources and licences** | Every source (CapIQ, LSEG, SEC filings, AURA, IRIS content, open web search) is hosted outside mainland China, so the offshore data flow is structural rather than a setting. Several would also be unreachable from inside the country. | All sources are reachable. The CapIQ, LSEG and FRWD licences have not been confirmed to permit use into Greater China; each sits with a different vendor owner and needs checking before first use. |
| **Enforcement today** | Nothing in the product enforces any of this. No step captures client consent, and the planned pre-flight check is unbuilt and designed around where the *target company* sits, not where the case is billed or where the user is. It would not stop a mainland case analysing a US company. | The same gap. Any case-by-case clearance happens outside the product and leaves no record, so there is no way to evidence afterwards that it was obtained. |

**Scale note.** The platform is sized for roughly 2,300 partners plus their teams at full scale. That population includes Greater China offices, so this will be asked the first time one of them opens the tool rather than remaining hypothetical.

---

## 3. Could the mainland blockers be worked around?

Three options have been proposed. Assessed individually, none is infeasible.

### Option A — A dedicated China cloud deployment

**Workable, but it is not "a server".** China operates as a separate cloud from the rest of Bain, run by a local entity under Chinese licence, with its own sign-on system and its own catalogue of available services. The work is not relocating a server; it is re-standing the whole managed-service platform underneath the product.

Two dependencies to verify before committing anything:

- **Sandboxed execution** for ad hoc dataset composition. Our current platform was chosen specifically for it. No equivalent means building it by hand, which reintroduces a security surface the design deliberately avoids.
- **Tamper-evident audit storage.** The audit trail depends on a specific database capability, and there is already an open item to confirm it in the *target* subscription, let alone a separate cloud.

Two harder breaks:

- **Identity.** Sign-on runs on Bain's global tenant and does not extend. A China instance needs its own identity path, decided against an empty Security Design page.
- **Bain-internal sources.** IRIS, AURA, ARC and SharePoint all live in the global tenant. A China instance either cannot reach them, or reaching them *is* the cross-border flow the deployment existed to avoid. **This is what forces Option C.**

The cost is not the build. It is a second production estate with its own release train, on-call rota, penetration testing and audit, permanently.

### Option B — Route LLM calls to China-approved models

**The easiest of the three, in one layer out of three.**

| Layer | Assessment |
| ----- | ---------- |
| **Routing** | **Genuinely a configuration change.** Every model call passes through a single gateway by design, and swapping a model is configuration, never code. This is good design paying off. |
| **Capability** | **Not a configuration change.** The product relies on frontier-model behaviour: multi-step agents, long-context reading of 10-Ks and analyst reports, structured extraction. The bar is concrete — our existing extraction skill runs at roughly 70–80% accuracy and degrades as sector conditions accumulate. Whether a China-approved model clears that bar is **not knowable today, because the quality benchmark does not exist yet.** |
| **Supporting AI services** | **Do not route through the gateway at all.** Content safety (the prompt-injection control), document parsing, runtime quality judges, agent orchestration and the retrieval embedding model are not LLM calls. Each needs a China-available equivalent or a custom build. This is plausibly the larger half of the work. |

**One low-regret action falls out:** build the quality benchmark regardless. It is already required for the global product, and it is the only thing that turns "would a Chinese model be good enough" from an opinion into a measurement.

### Option C — Manual data upload for China users

**Mechanically easy, and the option that quietly changes the product.** An upload path already exists for private-company financials, so this is that path widened. Three things it does not solve:

1. **Licensing, which it does not touch.** Exporting CapIQ or LSEG content and re-uploading it into a China-hosted system is still redistribution of licensed data into mainland China. The vendor contract governs the data, not the transport. **This has the longest lead time of anything on this page and can rule the idea out on its own.**
2. **The value proposition.** Two to three days compressed to roughly thirty minutes is the business case. Reinstating a human research step returns a partially automated tool. It may still be worth building, but it is a different product with a different payback and should be presented as such.
3. **Provenance.** Every figure must be drillable to source, reasoning and confidence. A hand-assembled pack can carry that, but only if the upload format *forces* per-figure source, as-of date and licence flag, and the system validates uploads as strictly as it validates fetched data. Skipped, the drill-down guarantee degrades into trusting whoever built the pack.

MNPI handling also sharpens here, because a person is now assembling and moving client financials by hand.

---

## 4. What would carry over, and what would be rebuilt

A fork is not a rewrite. The reusable part is the valuable part.

| Carries over unchanged | Would be rebuilt or re-sourced |
| ---------------------- | ------------------------------ |
| **Calculation engine** — deterministic, no network or imports, reproducible from pinned inputs. Indifferent to cloud and to model, and already identified as the one component Bain reuses | Identity and sign-on |
| **Containerised packaging** — every component is already packaged so that moving hosting is configuration rather than redesign. The same property makes any relocation tractable | Data acquisition and all upstream source connections |
| **Frontend, content model and deck composition** — model-agnostic and cloud-agnostic by construction | The supporting AI services layer |
| | The managed-service platform underneath everything |

Preserving the first two costs nothing extra and is worth holding to in review whether or not China ever proceeds.

---

## 5. Precedent and resourcing

This is not unprecedented at Bain. **Sage went through China-specific development to localise**, so there is a path already walked and lessons to borrow rather than a first-of-kind build. *(Scope of that localisation — hosting, models, data, or all three — to be confirmed with the Sage team before this is cited to leadership.)*

**A China engineering team can be mobilised** to scope and build, if leadership decides to pursue it. Resourcing is therefore not the binding constraint; the binding constraints are the licence and platform questions in section 6.

---

## 6. What would have to be true

Ordered by lead time rather than engineering sequence. **The first two are correspondence, not engineering — both are fast, and either coming back negative saves the entire programme of work.**

| # | Must be true | Owner | Note |
| - | ------------ | ----- | ---- |
| 1 | A China-resident Bain AI platform exists or is planned, with a timeline | TSG / Andromeda | Blocks everything downstream. Cheapest next step is a one-page feasibility check |
| 2 | Vendor licences permit use into mainland China | Each source owner: CapIQ, LSEG, FRWD, plus IRIS, AURA and ARC for whether their content may leave the global tenant | Longest lead time. Not solved by manual upload. Start now |
| 3 | A China-approved model clears the quality bar | Bain analyst time to build the benchmark, then measurement | Unanswerable until the benchmark exists. Build it anyway |
| 4 | China-available equivalents exist for the supporting AI services | TSG with StatusNeo | Content safety, document parsing, embeddings and reranking, agent orchestration, evaluation |
| 5 | An identity path exists for a China instance | Bain security | A decision, not a lookup. Security Design is currently empty |
| 6 | The target state is confirmed compliant | Legal / Risk | A China instance calling only registered models over China-resident data plausibly clears both rules, but that determination is Legal's, not ours |

**On sizing:** the routing layer of Option B is days of work. Options A and C done properly are comparable in effort to standing the product up a second time, plus permanently duplicated operations. A credible number is not available until items 1, 2 and 4 are answered, and any figure offered before then would be invented.

---

## 7. Recommendation

**For now:**

1. **Record mainland China as an explicit scope exclusion** for the October demo and the MVP, rather than leaving it to be discovered mid-case.
2. **Treat Hong Kong as requiring case-by-case clearance** until the model-routing question is answered and written down.
3. **Ask StatusNeo to widen the pre-flight check's inputs** so it keys on billing entity and user location, not only the target company. Cheap now, expensive after it is built.

**If leadership wants to pursue localisation:**

4. **Scope it as a platform question with Opportunity Catalyst as the worked example, not as an Opportunity Catalyst build.** Every blocker on this page is shared by any Reinvention tool facing the same question. Solved once centrally, every tool inherits the answer; solved tool by tool, each team pays the full cost and gets a worse result.
5. **Start items 1 and 2 immediately.** Neither requires engineering, both are weeks not months, and either can make the rest moot.
6. **Do not commit build effort until those two return.**

---

## 8. What this page does not answer

- Whether the Signal / NGGS guidance formally binds Opportunity Catalyst, or only client-deployed products.
- Exact service availability in Bain's China cloud environment — requires confirmation with TSG.
- Whether any specific China-approved model meets the analytical quality bar; unanswerable until the benchmark exists.
- Vendor licence positions for Greater China; each sits with a different source owner.
- Cost and timeline for localisation; not estimable until the above are answered.

---

*Basis: Bain regional AI guidance for mainland China and Hong Kong; OI 3.0 Technology Choices, Architecture Decision Records, Andromeda, Peer Selection Capability and Screen 01 Target Setup pages in this space. Full technical assessment held by the Tech Lead.*
