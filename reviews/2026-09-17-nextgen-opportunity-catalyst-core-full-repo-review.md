---
date: 2026-09-17
subject: "Full-repo review: Bain/nextgen-opportunity-catalyst-core (StatusNeo)"
source: "https://github.com/Bain/nextgen-opportunity-catalyst-core, main branch, snapshot uploaded 2026-09-17 (GitHub ZIP export, no commit SHA available — not a git checkout)"
reviewer: Claude (for Tech Lead sign-off)
outcome: "approve with comments"
---

# Review: nextgen-opportunity-catalyst-core (full repo)

## Scope

Full working tree as of the 2026-09-17 snapshot: all eight `services/` (audit, calculation-engine,
case, company-search, compliance, evidence, experience-bff, identity), `database/` (migrations,
provisioning), `utilities/` (data-product, entity-normaliser, search-index-builder, journey-docs),
`tools/service-scaffolder`, `tools/service-standards`, `governance/`, `contracts/`, `deploy/azure/`.

Two passes were run:

1. **`tools/service-standards` — the repo's own governance checker**, executed directly
   (`uv sync --extra dev && uv run oc-standards check --repo ../..`). This enforces layering,
   contract/descriptor schema, secret canaries, migration ownership, toolchain pinning, and CI
   supply-chain rules mechanically. Result: `status: pass`, 25 checks run, **0 errors, 0
   warnings**, 3 gates (all pre-existing, admin-scope items unrelated to code: GitHub team-slug
   resolution and branch-protection verification, both blocked by 403/404 on the checking
   account, not by anything in this repo), 10 checks not run for structurally legitimate reasons
   (BFF is TypeScript so the Python AST route-scanner doesn't apply to it; `utilities/` is
   declared unmanaged; migration streams have no `src/` tree to scan; the tracked-file secret
   scan needs `git ls-files`, unavailable on a ZIP export rather than a clone).
2. **Manual review** against `checklists/code-review.md` and this repository's own stated
   invariants (root `AGENTS.md`, `docs/engineering/guide.md`), split across five areas run in
   parallel: `experience-bff`; `calculation-engine` + `case-service`; `evidence-service` +
   `compliance-service` + `audit-service`; `identity-service` + `company-search-service` +
   `database/`; `utilities/data-product` + `entity-normaliser` + `search-index-builder` +
   `tools/service-scaffolder`.

**Not reviewed:** `agents/` (absent — not yet created), `deploy/azure/` provisioning correctness
(infra, not application code), CI/CD workflow logic beyond what the standards checker covers,
and anything requiring a running stack (no live integration testing was performed).

## Outcome

**Approve with comments.** This is a materially above-average delivery: the repo enforces its
own architecture mechanically (a real governance checker, not just prose), the calculation
engine avoids `eval()`/dynamic execution by construction and the claim was verified rather than
taken on faith, and several areas SN has already self-documented known gaps by ID before this
review found them independently. One finding is release-blocking: a mandatory EBIT
reconciliation gate is computed but not wired to the value's confidence tier or audit status, so
a value that fails reconciliation can still surface as the highest-confidence figure. Two
services (`evidence-service`, `compliance-service`) are explicitly `lifecycle: scaffold` with no
business logic yet — their most important product commitments (licensing enforcement,
provenance/confidence fields) simply have no implementing code, which is an open item to gate
before those services go active, not a code defect today.

## Blocking

### B1. EBIT reconciliation failure does not gate confidence or audit status
`services/calculation-engine/src/oi3_calc/adjustments.py` — `AdjustmentStatus.NOT_RECONCILED`
(line 108) is defined for "applied, but EBIT does not tie" but is never assigned anywhere in the
module (confirmed by grep: the only hit is the declaration). `adjust_row` (lines 256–306) sets
status only to `ANCHOR_MISSING` / `PASS_THROUGH` / `ADJUSTED`. The separate `reconcile_ebit` call
(line 305) produces a `ReconciliationResult.FAILED`, but that result lands only in
`report.checks` — it never flows back into the per-line-item `AdjustmentEntry.status` that
Screen 02's Data Sources tab renders (per the module's own docstring, lines 121–123).
`config/metrics.yaml` (lines 69, 100, 164) statically tags `cogs_adjusted` / `ebit_adjusted` /
`sga_adjusted` as `confidence: adjusted` — the highest tier — with no per-row conditioning on
reconciliation outcome.

**Why it matters:** this is exactly the failure mode the product's transparency requirement
exists to prevent — a number a partner would defend to a CEO, surfaced at maximum confidence,
that the engine itself has already determined doesn't tie. It is masked today only because a
target structure is never actually supplied (always `None`), so the check has no live case yet;
it will start firing silently the first time target-structure input is wired up.
`test_adjustments.py` has no test asserting a FAILED reconciliation changes entry status or
confidence — the gap is untested as well as unwired.

**Ask:** wire `reconcile_ebit`'s `FAILED` result into `AdjustmentEntry.status` (using the
already-defined `NOT_RECONCILED`) and downgrade the affected metrics' confidence tier before
target-structure input goes live; add a test asserting this.

## Should fix

### S1. `oi3-data-product`'s MCP/size-prize paths bypass the calculation port
`utilities/data-product/src/oi3_data_product/mcp_server.py:54,81,406-408` and
`size_prize.py:30,81` instantiate `oi3_calc.resolver.Resolver` directly instead of going through
`ports.CalculationClient` the way `runner.py` (the Gold path) does. `mcp_server.py`'s
`EngineContext.frame` (lines 86–91) never calls `oi3_calc.adjustments.adjust_frame`, while
`runner.py:175-176` does. This is documented in `calculation-engine/ARCHITECTURE.md:457`'s own
dependency diagram, so it isn't hidden, and `adjust_frame` is currently a no-op (no target
structure supplied yet) so results happen to agree — but the moment adjustment logic becomes
real (the same P7 milestone as B1 above), MCP-served and Gold-served answers for the same
company/metric can silently diverge, which breaks the "one calculation path, one number"
guarantee the docstring itself states as the reason the port exists. No test exercises
swapping the adapter on this path the way `test_ports.py` does for `runner.run`.

### S2. Evidence/compliance service commitments have no implementing code yet
`services/evidence-service` and `services/compliance-service` both declare `lifecycle: scaffold`
and expose only `/health/live` and `/health/ready`. Grepping their `src/` trees for
`licens|LSEG|retention|provenance|confidence|citation` returns nothing. `evidence_ref`
(`database/migrations/evidence-service/versions/rev_0001_evidence_core.py:37-44`) stores
`source_ref` and `trace_id` but no confidence field; `immutable_record` (lines 49-61) has a
free-text `retention_policy` column nothing reads or enforces. This is the review's structural
caveat, not a bug: the "evidence service is the one place licensing is enforced" and "provenance
preserved" product constraints have no code to violate yet. It should be a named gate before
either service leaves `scaffold` — recommend logging it against `context/open-questions.md` and
re-checking specifically when business logic lands.

### S3. `company-search-service` `/query` route has no upper bound on `page_size` at the transport layer
`services/company-search-service/src/company_search_service/transport/http/companies.py:308` —
`page_size: Annotated[int | None, Query(ge=1)]` has no `le=` unlike the adjacent
`size_rank_min`/`size_rank_max` (`le=1_000_000`). Not exploitable today — `QueryBounds.page_size_for`
(`domain/query.py:67-81`) enforces the real ceiling downstream and rejects out-of-range values —
but it's an inconsistency in the OpenAPI contract worth tightening for defense-in-depth.

### S4. `experience-bff` `service.json` dependency-operation list is stale
`services/experience-bff/service.json:33-37` lists `Case.authorizeResource` as a dependency,
which `contracts/provider-bindings.json:195-202` records was **removed** 2026-09-14 and which no
longer appears anywhere in `src/` except a comment noting its removal (`journeys.ts:309`).
Meanwhile `Case.list`, `Case.archive`, `Case.restore`, `Case.delete` — all actually called via
`HttpCaseProvider` and routed in `app.ts` — are missing from the manifest. This is exactly the
kind of drift the "no ungoverned service" invariant's machine-readable manifests exist to catch;
right now the manifest both overstates (authorize) and understates (archive/restore/delete) what
this BFF touches.

### S5. `experience-bff` error envelope doesn't cover HTTP-parser-level failures
SN's own adversarial pass (`services/experience-bff/adversarial/passes/P02-2026-09-11.md`,
finding N08) records this as confirmed-open, and it's still true today: no `clientErrorHandler`
exists anywhere in `src/` (grep confirms). A malformed request line, invalid HTTP version, or
oversize header — errors caught at the parser level before Fastify routing — bypass the unified
`BffError`/`toErrorBody`/`redact` envelope and get the framework default instead. No evidence of
secret leakage was found, but the "one error shape, no raw internals" guarantee doesn't hold for
this class of request.

## Nits

- `services/experience-bff/src/adapters/provider-transport.ts:317` — the 401 message ("The
  forwarded caller credential was rejected") is a holdover from an earlier design that forwarded
  the caller's token; the service now authenticates with its own workload token
  (`provider-transport.ts:14-23`), so the message would misdirect an operator debugging a 401
  toward a stale user session rather than the BFF's own credential.
- `services/experience-bff/src/transport/docs.ts:258-273` — a JSDoc block describing
  `registerDocsRoutes` sits above `assertDocsAssetsPresent()` instead; `registerDocsRoutes` is
  now undocumented and a future reader will misattribute the comment.

## What holds up cleanly (no findings)

- **No `eval()`/dynamic execution in the calculation engine** — verified by grep and by reading
  `grammar/parse.py` / `resolver.py`; every AST node type is validated before the resolver walks
  it, and series-function arguments are type-checked at load time.
- **Identity service** — permission checks fail closed through a `PermissionChecker` port
  (`security.py:64-80`), JWT verification pins algorithm, issuer, audience, expiry with
  constant-time comparison (`adapters/identity/__init__.py:138-181`), tokens are never logged.
- **Database/migrations** — all five owners (audit, case, compliance, evidence, identity) have
  exactly one canonical migration directory each; `owner_role` (`database/src/oc_database/roles.py:31-45`)
  actively raises if a migrator role collides with the shared release identity or the runtime
  role; no service Dockerfile or startup path runs migrations or DDL; the one destructive
  migration found (`case-service` archive/delete) documents its no-downgrade rationale and
  guards against live data.
- **`tools/service-scaffolder`'s safety claim** ("no install, subprocess, Git mutation or cloud
  call; never overwrite an existing target") — verified literally: the only subprocess use in
  the tool is the separately-documented `certify` command, unreachable from `plan`/`apply`;
  overwrite protection uses `RENAME_NOREPLACE`/`RENAME_EXCL` with exclusive-create fallback; a
  test suite (`test_apply_safety.py`) monkeypatches socket/subprocess/os.system to raise if
  called and still passes, and it does.
- **`case-service`** — no calculation-logic duplication; explicitly refuses to invent a metric
  and reports `"unavailable"` rather than guessing (`domain/cases.py:69-73`).
- **`audit-service`** — append failures are abandoned for redelivery, never swallowed
  (`application/consumer.py:120-139`); outbox relay bounds retries and quarantines rather than
  looping or dropping silently.
- General hygiene across all five areas: no hardcoded secrets/connection strings (all read via
  `*_FILE` settings or Key Vault references), no bare `except:`/`except Exception: pass` in
  application code, UTC-aware timestamps throughout, `Decimal` used end-to-end for
  financial-adjacent fields and serialized as strings rather than floats.

## Standards gaps hit

Security design, NFR/latency targets, observability, and API-contract standards remain
unwritten in Confluence (per `context/open-questions.md`), so this review's judgment on
"failure modes handled" and "bounded inputs" rests on code-level inspection rather than a
written standard to check against. S2 above (evidence/compliance licensing and provenance) is
the concrete instance where that absence matters most: there is no written rule yet for exactly
what evidence-service must enforce before it can leave `scaffold`, which is itself worth raising
back to the open-questions log rather than inventing a bar SN would be held to retroactively.
