---
date: YYYY-MM-DD
requester: "<name and team>"
subject: "<one line>"
type: "<access | infrastructure | library | design deviation | schema | integration>"
recommendation: "<approve | approve with conditions | decline | escalate | blocked>"
status: "<awaiting sign-off | signed off | declined | superseded>"
---

# Request: <subject>

## Asked for

One sentence, restated as the underlying *need* rather than the proposed solution.

## Existing rulings

Anything in `confluence/` or `decisions/` already covering this, with links. If a rule
plainly covers it, that is the answer — say so and stop.

## Assessment

Impact on the layers and systems involved. Check against the product constraints in
`context/oi30-brief.md`: provenance, modularity, gates, the headless split.

**Cost of yes:** what it commits us to, and how reversible it is.

**Cost of no:** what it blocks, and for whom.

## Recommendation

The recommended outcome and the reasoning. Conditions listed explicitly if any. An
alternative if declining.

## Sign-off

Tech Lead decision and date. Left blank until signed.
