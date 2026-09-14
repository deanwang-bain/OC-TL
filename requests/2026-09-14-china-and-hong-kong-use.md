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
