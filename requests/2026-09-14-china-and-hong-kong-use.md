---
date: 2026-09-14
requester: "Dean Wang, Tech Lead"
subject: "Can OI 3.0 be used in mainland China and Hong Kong"
type: "compliance"
recommendation: "Decline for mainland China; escalate for Hong Kong"
status: "awaiting sign-off"
---

# Request: Can OI 3.0 be used in mainland China and Hong Kong

## Asked for

Whether OI 3.0 can be used in China — across data sources, LLM use, and anything else
that bites — measured against the Bain regional AI guidance supplied by the Tech Lead
(the Signal / NGGS mainland China and Hong Kong rules).

## The rule being applied, and a caveat about it

The guidance supplied says three things:

| # | Rule | Region |
| - | ---- | ------ |
| 1 | AI features enabled by a **Global LLM (OpenAI, Claude, AzureAI)** must be **turned off**, for **both Bain internal users and clients**. Global LLM providers are not registered with the Chinese authorities, and only tools on local China models are permitted for case work | Mainland China |
| 2 | The client must **acknowledge and consent** to data being transferred outside mainland China, with a stated clause in the SOW. Mainland-billed cases default to **China Cloud** | Mainland China |
| 3 | AI features: **case-by-case check with Angie Wang**. Some Global AI models are supported in region (AzureAI / Copilot); **OpenAI- and Claude-backed features must still be off**, as both vendors publicly prohibit use in the region. Data transfer: no extra client consent where the case is billed out of Hong Kong, since HK-billed cases default to **Bain Global Cloud** | Hong Kong |

**Caveat, stated up front.** That guidance is written for Signal / NGGS, a product
deployed into client environments. OI 3.0 is a different shape: a partner-facing internal
tool whose persona is *"the accountable partner"*
([Persona](https://bainco.atlassian.net/wiki/spaces/OI30/pages/19618758842)) and whose
output is a deck, not a service the client logs into. That difference removes the stated
*reason* behind rule 1 — a client cannot directly access and interact with the AI
service, so Bain is not providing an AI service to the "Chinese public".

It does not remove the *rule*, which says "for both Bain internal users and clients" in
as many words. Nothing in `confluence/` or `decisions/` states a China position for
OI 3.0, so this is the nearest written rule and is treated as binding until its owner
says otherwise. Confirming that is the first ask below.

## Existing rulings

Nothing in the OI30 space addresses China, data residency beyond the EU, or regional
model routing. What does exist:

| Source | What it establishes |
| ------ | ------------------- |
| [ADR-009, persistence topology](https://bainco.atlassian.net/wiki/spaces/OI30/pages/19751960620) | *"No global distribution requirement... with servers in a single US region."* One region, and it is the US |
| [Technology Choices §4](https://bainco.atlassian.net/wiki/spaces/OI30/pages/19751338017) | Models come from **Azure AI Foundry** through an **API Management GenAI gateway** |
| [Technology Choices §4.1](https://bainco.atlassian.net/wiki/spaces/OI30/pages/19751338017) | Model selection is *deliberately not made* — it happens "at deployment against current availability, constrained by the routing policy in the gateway". Every model call passes the gateway, so changing a model is *"a configuration change and never a code change"* |
| [Andromeda](https://bainco.atlassian.net/wiki/spaces/OI30/pages/19691733117) | The Bain platform OI 3.0 is built to consume lists *"Running LLMs (e.g. Claude Sonnet/Opus)"* against its model gateway. Also: *"Andromeda is the destination, not a current dependency"* |
| [Peer Selection Capability](https://bainco.atlassian.net/wiki/spaces/OI30/pages/19809534070) | Peer candidate identification uses *"OpenAI-powered search"*, with *"web search as a fallback"* |
| [Screen 01: Target Setup](https://bainco.atlassian.net/wiki/spaces/OI30/pages/19710967811) | A pre-flight *"Conflict / blocked-target / data residency check"* exists as a **design requirement**, explicitly *"Not in current prototype"*, with *"Rules to be confirmed with Noelle and Kasia before SN builds"* |
| Logic architecture diagram (`19619840005`) | The residency gate is drawn as *"Data-residency router (EU target → EU)"* — EU is the only geography modelled |
| [Security Design](https://bainco.atlassian.net/wiki/spaces/OI30/pages/19705167996) | **Empty.** No written control set for processing, AI or data |
| [Confidential data](https://bainco.atlassian.net/wiki/spaces/OI30/pages/19689340995) | *"To be decided how to treat it? Partners would like to use the client data in their OIs."* Unanswered |

## Assessment

### 1. LLM use — the blocking issue for mainland China

Rule 1 assumes AI is a *feature* that can be switched off while the product keeps
working. In Signal / NGGS that is true. In OI 3.0 it is not.

The agent layer is the product. Peer proposal, non-GAAP adjustment extraction, claim
extraction, narrative synthesis and deck composition are all agent work
([Screen 02](https://bainco.atlassian.net/wiki/spaces/OI30/pages/19710279791),
[Technology Choices §4](https://bainco.atlassian.net/wiki/spaces/OI30/pages/19751338017)).
Turning off global-LLM features leaves the deterministic calculation engine, which is
real and valuable but has nothing to calculate over until the agents have produced a peer
set and adjusted financials. **"AI features off" and "OI 3.0" are not compatible states.**

The named providers make this concrete rather than theoretical:

- **Azure AI Foundry** is the model platform (§4). The guidance names *AzureAI* in the
  mainland prohibition, so Azure hosting does not rescue mainland use.
- **Claude** is what Andromeda's gateway serves, and Andromeda is the stated destination.
- **OpenAI** is named directly in the peer selection design.

All three appear in the mainland "turn off" list. There is no fourth option in the
record: no China-hosted model, no local provider, nothing that would satisfy *"only
tools supported by local China models"*.

The one genuinely helpful fact is §4.1 — model choice is a gateway routing policy, not
code. A **region-conditional routing policy** is technically the cheapest lever available
and is the only thing that could make Hong Kong work. It does not help mainland China,
because the constraint there is not which global model but that global models are
excluded as a class.

### 2. Data residency and cross-border transfer

Mainland-billed cases default to China Cloud. OI 3.0 runs in **a single US region**
(ADR-009). There is no China deployment, no China region, and no multi-region design —
ADR-009 says the Azure SQL choice should be revisited *only if* a multi-region
requirement appears, and records that none exists.

So every OI 3.0 run for a mainland-billed case is a transfer of client data out of
mainland China, and rule 2 applies in full: client acknowledgement plus an SOW clause.
Three things follow.

- **The consent mechanism does not exist in the product.** Nothing in the screen specs
  captures or records a client's consent to cross-border transfer, and the audit trail
  has no such event.
- **The gate that would enforce it is unbuilt and scoped to the wrong geography.** The
  pre-flight check is a design requirement only, and the diagram models *EU target → EU*.
  A China rule is a different shape anyway: it keys on **where the case is billed and
  where the user sits**, not on where the target company is. The gate as drawn routes on
  the *target*, so it would not catch a mainland-billed case analysing a US target. That
  is a real design gap worth raising with StatusNeo before they build it.
- **Uploaded client data is the sharp edge.** The Confidential data page is unanswered
  and records that partners want to put client data into OIs. A partner uploading a
  mainland client's financials is the exact scenario rule 2 exists for.

Serving mainland China properly would mean a China Cloud deployment — a separate,
operator-run cloud with its own service catalogue and its own Foundry model availability,
not an Azure region flag. That is not a configuration change; it is a second instance of
the platform, and it would be the first thing ADR-009's revisit trigger has ever been
pulled for. It is far outside GLS and MVP scope.

### 3. Data sources

Every source in the
[Data Sources summary](https://bainco.atlassian.net/wiki/spaces/OI30/pages/19619676163)
is a global or Bain-internal platform hosted outside mainland China: CapIQ XpressFeed,
SEC EDGAR, LSEG (Refinitiv), earnings transcripts, AURA, Glassdoor / Fishbowl, IRIS via
Glean, ARC, PEG expert interviews, FRWD, plus open web search as a fallback.

Two observations, and one is much more important than the other.

- **The one that matters:** because the sources and the compute both sit outside mainland
  China, there is no configuration of OI 3.0 in which a mainland case stays onshore. The
  data flow is outbound by construction. This is the same finding as §2, arrived at from
  the data side.
- **The lesser one:** several of these sources — open web search and Glassdoor in
  particular — are unlikely to be reachable from inside mainland China at all. This is a
  functional problem rather than a compliance one, and it is downstream of the compliance
  answer, so it does not change the recommendation.

Licence terms are a separate question this workspace cannot answer: whether CapIQ, LSEG
and FRWD permit use or redistribution of their data into mainland China is a contract
matter held by each source owner, not something the mirror records. Flagged, not resolved.

### 4. Hong Kong is a genuinely different answer

Hong Kong is not blocked by the same logic, and it is worth separating clearly.

| Rule | OI 3.0 position |
| ---- | --------------- |
| Data transfer | **Satisfied on the face of it.** HK-billed cases default to Bain Global Cloud, and OI 3.0 runs on Bain-managed Azure in a US region. No additional client consent is called for |
| AI features | **Unresolved, and undecidable from the record.** OpenAI- and Claude-backed features must be off; AzureAI / Copilot may be acceptable. OI 3.0's named model platform is Azure AI Foundry, which points the right way — but Andromeda serves Claude, peer selection names OpenAI, and §4.1 deliberately defers the actual model choice to deployment |

So Hong Kong turns entirely on which models the gateway routes to, and that is precisely
the thing the architecture has chosen not to write down. The guidance also requires a
case-by-case check with Angie Wang regardless, so this cannot be settled here in any
event.

### 5. Other concerns worth naming

- **Security Design is empty.** There is no written control set to check a regional
  deployment against, so any "we could make China work" argument would rest on judgment
  rather than policy. Consistent with the standing position on the empty pages: treat as
  unknown, not as "no requirement".
- **Audit.** The ledger-table audit trail records who changed what and why. It does not
  record where the user was or how the case was billed, which is what a residency
  question would need to answer after the fact.
- **The 2300-user figure.** ADR-009 sizes for 2300 partners plus teams at full scale.
  That population includes Greater China offices, so this is not an edge case that stays
  theoretical — it will be asked the first time a Greater China partner opens the tool.

**Cost of yes** (declaring OI 3.0 usable in mainland China): committing to a China Cloud
deployment, a locally-supported model path that does not exist in the design, and a
consent mechanism nobody has specified — against a GLS date roughly five weeks out. Not
reversible in any useful sense, because it is a second platform instance.

**Cost of no:** Greater China partners cannot use OI 3.0 for mainland-billed cases. Real,
but bounded, and honest: it is the position the architecture already implies. The cost of
*not deciding* is higher — a partner discovers the constraint mid-case, or does not
discover it at all.

## Addendum, 2026-09-15 — are the mainland blockers workable?

Asked as a forward-looking thought experiment rather than a live requirement: could a
China-capable Opportunity Catalyst be built with (1) a dedicated China cloud deployment,
(2) LLM calls routed to China-approved models, and (3) either new China data pipelines or
an open-ended manual upload of target and peer inputs? Is that feasible under heavy
constraints, or infeasible outright? The prompt behind it is broader than this programme:
CdV is asking the same question of several Reinvention efforts.

**Answer: not infeasible. But it is a fork of the product, not a configuration of it** —
and the honest unit of decision is a Bain platform question, not an Opportunity Catalyst
question.

### The three bullets, assessed

**1. A dedicated China cloud deployment — feasible, but it is not "a server".**

Azure's China environment is a separate sovereign cloud operated by a local entity under
Chinese licence, not a region of global Azure. It carries its own subscriptions, its own
identity tenant with no federation to the global one, and a service catalogue that trails
global availability. So the work is not relocating a server; it is re-standing the entire
managed-service substrate this architecture rests on: Container Apps and dynamic sessions,
Azure SQL plus ledger tables, immutable blob with legal hold, Redis, ADLS Gen2, Service
Bus, Front Door Premium with WAF, API Management, Key Vault, private endpoints, Defender,
AI Foundry, Content Safety and Document Intelligence. Each must exist there at a usable
version or acquire a substitute.

Two are load-bearing enough to verify before anyone commits:

- **Container Apps dynamic sessions.** This is the sandboxed execution the ad hoc dataset
  composition capability needs, and it is the specific reason App Service was rejected. No
  equivalent means hand-rolling a sandbox, which is the escape surface the closed-grammar
  decision was designed to avoid.
- **Azure SQL ledger tables.** The tamper-evident audit trail rests on them, and there is
  already an open item to confirm their regional support in the *target* subscription. A
  sovereign cloud is a stronger version of that same question.

**The sharpest break is identity.** Sign-on is Okta with Entra ID on Bain's global tenant.
A China instance cannot use it as designed and needs its own identity path — a security
decision taken against an empty Security Design page.

**The second break is the Bain-internal sources.** IRIS via Glean, AURA, ARC, PEG and
SharePoint all live in the global tenant. A China instance either cannot reach them, or
reaching them *is* the cross-border flow the deployment existed to avoid. This is the
hinge that forces bullet 3.

Engineering-feasible. The cost is not the build; it is a second production estate with its
own release train, on-call rota, penetration test and audit, forever.

**2. Routing to China-approved models — genuinely the easiest of the three, in one layer
of three.**

- **Routing is a configuration change.** Every model call passes the gateway by design, and
  the architecture states in terms that swapping a model is configuration and never code.
  This is the single most favourable fact in the whole assessment, and it is good design
  paying off rather than luck.
- **Capability is not a configuration change.** The product leans on frontier behaviour:
  multi-step tool-calling agents, long-context reading of 10-Ks and analyst reports, and
  structured extraction. The bar is concrete — the existing Claude skill for non-GAAP
  adjustments runs at roughly 70–80% accuracy and degrades as sector conditions accumulate
  in the prompt. Whether a registered Chinese model clears that bar is **not currently
  knowable, because the golden evaluation dataset does not exist.** It is an open item
  needing Bain analyst time.
- **The non-LLM AI services do not route through the gateway at all.** Content Safety is
  the prompt-injection *control*, not a test. Document Intelligence parses the filings.
  Foundry evaluations run the groundedness judges. The Microsoft Agent Framework does the
  orchestration, and Andromeda's BGE-M3 embedding and reranker do retrieval. Each needs a
  China-available equivalent or a custom build. This is the part the bullet omits and it is
  plausibly the larger half of the work.

One clean consequence: **build the golden dataset regardless.** It is already required for
the global product, and it is the only thing that converts "would a Chinese model be good
enough" from an opinion into a measurement. Low regret either way.

**3. A manual data upload — mechanically easy, and the one that quietly changes the
product.**

The upload path is not alien to the design; partners already upload financials for private
companies, and hard gates already block on missing critical input. An upload-first mode is
that existing path widened. Three things it does not solve:

- **Licensing, which it does not touch.** Exporting CapIQ, LSEG or FRWD content and
  re-uploading it into a China-hosted system is still redistribution of licensed data into
  mainland China. The vendor contract governs the data, not the transport. A manual step
  moves the question rather than answering it. **This has the longest lead time of anything
  here and can kill the idea independently of any engineering, so it is the item to start
  first.**
- **The value proposition.** Two to three days compressed to roughly thirty minutes *is*
  the business case. Reinstating a human research step returns a partially automated tool.
  That may still be worth building, but leadership should be told it is a different product
  with a different payback, not the same product with a manual input.
- **Provenance.** Transparency is a hard requirement: every figure drillable to source,
  reasoning and confidence. A hand-assembled package can carry that, but only if the upload
  schema *forces* per-figure source, as-of date and licence flag, and the structural
  invariants validate uploaded packages as strictly as fetched ones. That is real build
  work. Skipped, the drill-down guarantee quietly degrades into trusting the analyst who
  built the pack.

MNPI handling also sharpens here, because a person is now assembling and moving client
financials by hand.

### What survives a fork unchanged

Not everything is rebuilt, and the reusable part is the valuable part.

| Component | Why it ports |
| --------- | ------------ |
| **Calculation engine** | A closed expression grammar with no imports, no network and no file access, deterministic and re-derivable from pinned inputs plus a trace. Indifferent to cloud and to model. It is also the one component the architecture identifies as reusable across Bain |
| **Containerisation** | Every component is packaged as a container from day one, specifically so that moving to Andromeda is configuration rather than redesign. That same property is what makes *any* relocation tractable |
| **Frontend, content model, deck composition** | Model-agnostic and cloud-agnostic by construction |

What does not port: identity, data acquisition, the AI services layer, and the managed
substrate underneath all of it.

Preserving the first two costs nothing extra and is worth insisting on in review whether
or not China ever happens.

### The reframe that actually answers CdV's question

Every blocker above is a **Bain platform** problem, not an Opportunity Catalyst problem:
China-resident compute, a registered model gateway, a China-legal data path, a China
identity tenant. Every Reinvention tool will hit the identical four in the identical order.

So "can Reinvention tools operate in China" resolves to **"does Bain intend to stand up a
China-resident AI platform?"** If Andromeda ever gains a China instance, every tool
inherits the answer for free. If it does not, each team pays the full cost alone and
arrives at a worse result than a shared one.

**Recommendation: scope the vetting as a platform question with Opportunity Catalyst as
the worked example, not as an Opportunity Catalyst build.** It is cheaper, it is the answer
CdV actually needs across several efforts at once, and it stops each team improvising its
own.

### What would have to be true, with owners

Ordered by lead time, not by engineering sequence. The first two are answerable by
correspondence in weeks with zero engineering, and either can make the rest moot.

| # | Must be true | Owner | Note |
| - | ------------ | ----- | ---- |
| 1 | A China-resident Bain AI platform exists or is planned, with a timeline | TSG / Andromeda | Blocks everything downstream. Cheapest possible next step is a one-page feasibility check |
| 2 | Vendor licences permit use into mainland China | Each source owner: CapIQ, LSEG, FRWD, plus IRIS, AURA and ARC for whether their content may leave the global tenant | Longest lead time. Start now. Not solved by manual upload |
| 3 | A registered Chinese model clears the quality bar | Bain analyst time for the golden dataset, then measurement | Unanswerable until the dataset exists. Build it anyway |
| 4 | China-available equivalents exist for the non-LLM AI services | TSG with StatusNeo | Content safety, document parsing, embeddings and reranker, agent orchestration, evaluation harness |
| 5 | An identity path exists for a China instance | Bain security | A decision, not a lookup. Security Design is empty |
| 6 | The target state is confirmed compliant | Legal / Angie Wang | A China instance calling only registered models over China-resident data plausibly clears both rules, but that determination is Legal's, not ours |

**Sequencing:** answer 1 and 2 before committing engineering to any of it. Both are
correspondence, both are fast, and either coming back negative saves the entire programme
of work.

**Sizing, honestly:** bullet 2's routing layer is days. Bullets 1 and 3 done properly are
comparable in effort to standing the product up a second time, plus permanent duplicated
operations. A credible number is not available until items 1, 2 and 4 are answered, and
any figure offered before then would be invented.

## Recommendation

**Mainland China: recommend decline, and record it as an explicit scope exclusion rather
than leaving it undiscovered.** Three independent blockers, any one of which is
sufficient:

1. The global-LLM prohibition removes the product, not a feature. No local-model path
   exists in the design.
2. There is no China Cloud deployment and no multi-region design, so every mainland case
   is a cross-border transfer.
3. The consent capture and the residency gate that would make rule 2 enforceable are both
   unbuilt, and the gate as drawn routes on the wrong attribute.

**Hong Kong: needs a decision above this level.** The data-transfer rule appears
satisfied; the AI rule depends on gateway model routing, which §4.1 defers by design, and
the guidance requires a case-by-case check with Angie Wang. Do not assume it is blocked,
and do not assume it is clear.

### Conditions and follow-ups

1. **Confirm the rule applies to OI 3.0 at all.** The guidance is written for Signal /
   NGGS. Angie Wang is named in it for the Hong Kong check and is the natural owner;
   Noelle and Kasia own the residency rules per the Screen 01 spec. This is the first
   question, because everything else follows from it.
2. **Write the scope exclusion down.** Mainland China out of scope for GLS and MVP,
   recorded in the space rather than held in this file. It belongs on the
   [Confidential data](https://bainco.atlassian.net/wiki/spaces/OI30/pages/19689340995)
   page or a new residency page.
3. **Ask StatusNeo to widen the pre-flight gate's inputs, not to build a China rule.**
   The requirement to state is that the gate must key on the **billing entity and user
   location**, not only the target company. That is a data-model question they should
   answer before the gate is built, and it is cheap now and expensive later.
4. **Ask for the gateway routing policy to be written down.** §4.1 correctly refuses to
   name model generations, but a *region-conditional routing policy* is a different thing
   from a model name and is the only mechanism that could ever make a regional rule
   enforceable in configuration. Its absence is the reason the Hong Kong question cannot
   be answered from the record.
5. **Add the source licence question to the data owners' list** — whether CapIQ, LSEG and
   FRWD terms permit use into Greater China. One question per source owner, per
   `context/stakeholders.md`.

## Sign-off

Tech Lead decision and date:
