# Technical request triage

For requests routed to the Tech Lead: environment access, infrastructure, new
libraries or services, deviations from documented design, schema changes, third-party
integrations.

## Triage

1. **What is actually being asked?** Restate it in one sentence. Many requests
   describe a proposed solution rather than the need — surface the need.
2. **Is it already ruled on?** Search `confluence/` and `decisions/`. If a written rule
   covers it, apply that rule and cite it. This is the fast path.
3. **Who is affected?** Which layer, which upstream systems, which owners
   (`context/stakeholders.md`).
4. **What breaks if we say yes?** Check against the product constraints in
   `context/oi30-brief.md` — provenance, modularity, gates, the headless split.
5. **What breaks if we say no?** Blocked sprint work is a real cost. Name it.
6. **Is it reversible?** A library choice is cheap to undo; a schema or persistence
   change is not. Weight scrutiny accordingly.

## Recommendation

Every request gets one of:

| Outcome | Use when |
| ------- | -------- |
| **Recommend approve** | Consistent with documented design, or a reasonable call within Tech Lead discretion |
| **Recommend approve with conditions** | Acceptable given specific constraints — state each condition |
| **Recommend decline** | Conflicts with a decision or product constraint. Give the reason and a viable alternative |
| **Needs a decision above this level** | Cost, risk, or scope beyond the Tech Lead — say who decides and what they need |
| **Blocked on missing information** | Name exactly what is missing and who has it |

**The Tech Lead signs off.** Produce the recommendation and reasoning; do not record an
approval as final on their behalf. Where the request is routine and an existing written
rule plainly covers it, say so — that is the point of the fast path.

## Recording

One file per request in `requests/`, from `requests/TEMPLATE.md`, named
`YYYY-MM-DD-short-slug.md`. Add a row to `requests/REGISTER.md`. If it sets a
precedent, add it to `decisions/`.
