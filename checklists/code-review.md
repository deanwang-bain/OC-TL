# Code review checklist

Applied when reviewing SN's OI 3.0 code. **Review only — never push code to their
repositories.** A snippet illustrating a fix inside a review comment is fine.

Order matters: an architectural violation outranks a style nit, and saying so keeps
reviews useful.

## 1. Architectural conformance

- [ ] **No business rules or authoritative calculations in the frontend.** The headless
      split is a stated decision, not a preference. Calculation logic in React is a
      blocking finding.
- [ ] Deterministic operations go through FastAPI REST; AI capabilities go through the
      governed interfaces, not ad-hoc calls.
- [ ] Consistent with ADR-001 to ADR-009 on decomposition, orchestration, persistence.
      Cite the ADR when flagging.
- [ ] Stack additions justified — a new library overlapping an approved one (state,
      grids, charts) needs a reason.

## 2. Product constraints

These are commitments, so breaking one is a correctness bug:

- [ ] **Provenance preserved.** Any surfaced number can still be traced to source,
      reasoning, and confidence. Silently dropping provenance is blocking.
- [ ] **Module boundaries respected.** Changing peers or context reruns only affected
      modules; no hidden coupling forcing a full recompute.
- [ ] **Gates behave correctly.** Hard gates block; soft gates proceed and flag. A hard
      gate downgraded to a warning is blocking.
- [ ] Export path still produces Bain / ThinkCell-compatible output.

## 3. Correctness

- [ ] Logic does what the story says; edge cases handled.
- [ ] Failure modes handled — upstream (VCC, CapIQ, IRIS, LSEG, Expert Search) timeouts
      and partial data do not corrupt an analysis.
- [ ] No swallowed exceptions hiding data-quality problems.
- [ ] Tests cover the change and would fail without it.

## 4. Data handling

- [ ] Confidential data handled per the documented rules; check the page before ruling.
- [ ] No credentials, tokens, or client data in code, logs, or fixtures.
- [ ] Schema changes reconciled against the Data Dictionary and per-screen requirements.

## 5. Maintainability

- [ ] Readable by the next person; naming matches surrounding code.
- [ ] No copy-paste of logic that belongs in one place.
- [ ] Public interfaces documented where behaviour is non-obvious.

## Where the standard is missing

Security, NFR, observability, and API-contract standards are **undocumented**. Do not
invent one and present it as policy. Say the standard is unwritten, give the concrete
risk, propose a rule, and log it in `context/open-questions.md`.

## Severity

| Level | Meaning |
| ----- | ------- |
| **Blocking** | Architectural violation, broken product constraint, data/security risk, or a correctness bug |
| **Should fix** | Real problem, not release-blocking — missing tests, unhandled edge case, unclear failure |
| **Nit** | Style or preference. Mark clearly as optional |
