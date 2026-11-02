---
date: 2026-11-02
subject: "OI Catalyst — Sprint 5 & Post-GLS QA Test Strategy (SN QA, draft for team review)"
source: "PDF shared with the Tech Lead on 2026-11-02, 15 pages. Not in Confluence at the time of review"
reviewer: Claude (for Tech Lead sign-off)
outcome: "approve with comments"
---

# Review: SN's Sprint 5 & Post-GLS QA Test Strategy

## Scope

The whole document. It is a document review, not a code review, so the template's blocking
and nit sections are used loosely. The Tech Lead asked for suggestions, not challenges. The
document postdates Confluence, so differences from the mirror are treated as the mirror
lagging unless something major turns up.

## Outcome

**Approve with comments.** The strategy is specific to the product and led by risk. It
follows the journey (Target, Peers, Case for Change, Size of Prize, Output, Chat) and maps each
step to the layer that owns it.

It already makes the main calls in our own plan:
- exact checks for numbers and state;
- scored evaluation for generated text;
- "assert the numbers exactly, then score the explanation separately";
- automation at the lowest reliable layer;
- contracts as a regression gate;
- the eight seeded golden companies as a stable baseline;
- previous defects kept as permanent regression.

Its section 15 "decisions still needed" largely overlaps
[context/open-questions.md](../context/open-questions.md). The suggestions below add to it;
none replaces anything.

## Blocking

None.

## Should fix (suggestions)

1. **Add a small AI-safety and guardrail strand.** Security, prompt injection and agent permissions are
   not covered. Two of the planned changes, **+ Source attachment** and
   **Chat-to-screen workflow**, are exactly where hidden instructions and over-reaching agent
   actions would show up. No content-safety layer is deployed yet
   ([workshop notes](../context/workshops/2026-10-28-system-and-data-architecture.md)).
   Suggest:
   - a handful of injection cases in the AI evaluation set, with instructions hidden in an
     attached document or a web page;
   - checks that chat actions go only through declared, reversible tools in the user's own
     turn, and are audited as the agent acting on behalf of the user.

   Ask whether security scanning and the pen test are covered elsewhere, and where.
2. **AI evaluation: repetition, triggers and a reviewed subset.** The question set (section 6)
   is good. Suggest:
   - asking each question several times, not only paraphrased, to measure consistency;
   - running the set whenever a prompt, model or tool changes, not only per ticket. The AI
     Architecture Requirements make this a MUST before merge (CQ-AI-PMT-02);
   - keeping a small subset reviewed by BCN for release decisions;
   - aligning with each agent's existing `eval.contract.json` so there is one format.
3. **Automate "numbers match everywhere".** Extend the Output reconciliation and data-validation
   layer into one automated check per golden company. Every figure in the narrative, deck and
   chat should equal the calculated value.
4. **Use the golden pack as the safety net for stage-to-main.** As GLS code moves out of the BFF
   into services, the eight golden companies should give identical values before and after. In
   particular, the GLS exceptions EX-0001 to EX-0011 expire 31 December, and EX-0002 is the
   calculation port inside the BFF.
5. **Baseline performance and accessibility now, even without targets.** Measure full-run time
   and time to first progress on the golden companies so a target can be set from data. Add a
   light accessibility check on key screens. WCAG 2.2 AA is the one written non-functional
   target ([Technology Choices](https://bainco.atlassian.net/wiki/spaces/OI30/pages/19751338017)).

## Answers we can offer to its open decisions

- **"Which user/AI actions must write Audit and/or Evidence?"** These give a partial answer:
  [ADR-005](https://bainco.atlassian.net/wiki/spaces/OI30/pages/19751960620) (agent actions
  are declared tools with an actor), plus SN's repo ADR-0040 and ADR-0045 (an agent acts for a
  user; chat writes are reversible and decided in the user's turn).
- **"What release gate is required before the 50-partner release?"** Its "QA complete when"
  list (section 13) is a good base. Offer to define the gate together.

## Questions

- How does this relate to the
  [Agent Validation Test Plan](https://bainco.atlassian.net/wiki/spaces/OI30/pages/19765133323)
  (Confluence, v2, 7 Oct)? Does it replace it or sit beside it? Suggest publishing it to
  Confluence once agreed.
- The golden list has eight companies. The GLS data set was described as 10 targets and about
  100 peers, and Nike was the lead demo case. Is leaving Nike and the other two out deliberate?

## Standards gaps hit

Performance targets, AI-evaluation thresholds and the release gate are undefined everywhere, as
the document itself says. See [context/open-questions.md](../context/open-questions.md) and the
NFR row there.
