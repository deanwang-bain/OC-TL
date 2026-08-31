---
date: YYYY-MM-DD
subject: "<PR title, branch, or description>"
source: "<link to the PR or commit>"
reviewer: Claude (for Tech Lead sign-off)
outcome: "<approve | approve with comments | request changes>"
---

# Review: <subject>

## Scope

What was reviewed, and what was deliberately not.

## Outcome

One paragraph: the recommendation and the single most important reason for it.

## Blocking

Architectural violations, broken product constraints, data/security risks, correctness
bugs. Each with file:line, what breaks, and why it matters. Empty section is a good
outcome — say "None."

## Should fix

Real problems that are not release-blocking.

## Nits

Optional. Clearly marked as such.

## Standards gaps hit

Anything where the documented standard does not exist, so the finding rests on judgment
rather than policy. Cross-link `context/open-questions.md`.
