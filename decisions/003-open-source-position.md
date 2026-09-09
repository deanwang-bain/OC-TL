---
id: 003
date: 2026-09-09
status: proposed
---

# 003 — Open source in OI 3.0: default yes, bounded by four rules

## Context

Asked by the Tech Lead: what are the risks and trade-offs of using open-source code, and
what is our view.

The question arrives alongside
`requests/2026-08-31-third-party-and-oss-positions.md`, which assesses the specific
open-source items declared in
[Technology Choices](https://bainco.atlassian.net/wiki/spaces/OI30/pages/19751338017).
That request rules on *those items*. This decision states the general position, so the
next library does not need the same argument run again.

**No page in the OI30 space states an open-source position.** Technology Choices records
Build / Adopt / Buy for 66 entries but never records a licence, and
[Security Design](https://bainco.atlassian.net/wiki/spaces/OI30/pages/19705167996) — where
a control set would live — is empty. So there is no written standard to apply, and this
decision is judgment, stated as such.

### Open source is not a proposal here; it is already the substrate

Technology Choices commits to it in four different shapes, which carry four different
risk profiles. Conflating them is what makes the question hard to answer.

| Shape | Examples from the page | Risk profile |
| ----- | ---------------------- | ------------ |
| **Standards and formats** | OpenTelemetry, Parquet, MCP, A2A (§4, §5, §8) | Lowest. An open format is the thing that *creates* the exit from everything else |
| **Libraries linked into our code** | TanStack Query, Zustand, Radix, i18next, Vega-Lite, DuckDB, Zvec (§2, §4, §5) | Bounded and mostly reversible. This is where licence and supply-chain hygiene matter |
| **Foundations** | React, TypeScript, Vite, Node, Python, FastAPI, gRPC, headless Chromium (§2, §3) | High switching cost, but the alternative is not "less open source", it is a different open-source stack |
| **Open core, sold under a commercial tier** | AG-Grid Enterprise, CopilotKit, dbt, Datadog (§2, §5, §8) | **Not an open-source risk. A procurement risk wearing open-source clothes** |

The entire test suite in §9.2 to §9.4 is open source as well — Vitest, Playwright,
axe-core, pytest, Schemathesis, Hypothesis, Testcontainers, buf, Trivy, OWASP ZAP, PyRIT,
Checkov. So "should we use open source" is not a live question. **Which risks are real,
and what rules bound them, is.**

## The risks, in the order they bite this programme

### 1. Re-derivability — the one that is programme-specific

Technology Choices §3.3 makes the sharpest available argument, and it is *ours*, not a
generic one. It rejects sandboxed Python for calculation definitions because

> reproducing the figure in 2031 would require reproducing the interpreter and every
> transitive dependency as they stood in 2026.

The same logic applies to any open-source dependency whose behaviour can reach a number a
partner puts in front of a client. A charting library cannot break the guarantee — it
renders something already computed. A statistics or date library inside the calculation
engine can, silently, on a patch bump.

This is the risk with real teeth, and it does not argue against open source generally. It
argues for a boundary in one place.

### 2. Licence class and IP contamination

Permissive licences (MIT, BSD, Apache-2.0, ISC) carry attribution obligations and nothing
that touches Bain IP. Strong copyleft is different in kind: **AGPL** obligations trigger
on *network use*, not distribution, which is exactly how OI 3.0 is consumed, so an AGPL
component linked into a service is the one licence class that could reach Bain code.
GPL/LGPL matter less for a hosted internal product but are still not free of argument.

Separately, several widely-used projects have **relicensed away from open source
mid-life** — the source-available SSPL and BSL wave. That is a tail risk with a real
mitigation: it lands on the party operating the software. OI 3.0 consumes Redis as
**Azure Cache for Redis** (§5), so Redis's own licence change is Microsoft's problem, not
ours. That is the managed-first rubric paying for itself, and it generalises.

Note what open source does *not* contaminate: nothing in a library's licence attaches to
the deck OI 3.0 produces. The output-side licensing exposure in this programme is data —
CapIQ, LSEG, VCC — not code.

### 3. Supply chain and vulnerabilities

The transitive dependency count, not the direct one, is the exposure. Two runtimes means
two dependency graphs and two scanners, a cost §3.2 already concedes and accepts.

Controls partly exist: §9.4 specifies CodeQL every pull request, **Dependabot with alerts
as blocking**, Trivy and Defender on every build, secret scanning with push protection.
That is a stronger baseline than most programmes start with. What is missing is an
**SBOM per deployable**, a stated **remediation SLA** for a blocking alert, and a rule
that lockfiles are committed and builds are reproducible. Without the SLA, "blocking"
degrades into "muted" the first sprint it costs a demo.

### 4. Maintainer and abandonment risk

The bus-factor question: who ships the fix when it breaks. **Zvec** (§4.2) is the live
example — the one dependency in the set nobody will recognise, unresolved in the
2026-08-31 request. The mitigation is not avoidance, it is blast radius: Zvec is a
run-scoped in-memory cache holding nothing durable, so the exit is a rewrite of one
function. DuckDB carries the opposite profile — heavily used, embedded, no operational
surface — which is why §10.3 calls it *"never a real question."*

### 5. Operability, when open source means self-hosted

Nobody to call at 2am, and patching is ours. This is the risk the Azure-first rubric
already answers, and the distinction that matters is **library versus server**: DuckDB
embedded in a process has no operational surface, a self-hosted cluster has all of it.

### 6. Open core, which is the risk most often mislabelled

CopilotKit is recorded as "Buy, licence" but is open core; AG-Grid Enterprise rests on
"existing Bain licence"; dbt has a commercial tier above dbt Core. The pattern is the free
tier shaping the product, then the price appearing after the architecture is committed.
CopilotKit shapes the assistant surface, so reversibility is poor and cost discovery is
late. These are procurement decisions and should be assessed as procurement.

## The trade-off in the other direction, which is larger

Every open-source refusal converts into a custom build, and Technology Choices §10.1
already concedes the count *"flatters the custom build"* at 24 of 27 components. Only five
builds are argued as genuinely differentiated (§10.2). Refusing a permissive library on
principle adds a sixth that nobody would defend.

Three further arguments run *for* open source specifically in this programme:

- **Inspectability supports the transparency requirement.** OI 3.0's central commitment is
  that any number is drillable to source, reasoning and confidence. When behaviour is
  disputed, DuckDB's evaluation order can be read. A SaaS query service's cannot.
- **Open formats are the exit.** Parquet, OpenTelemetry, MCP and OpenAPI are what make
  the "Adopt" positions reversible at all. Reversibility is one of the four tests every
  choice on the page has to survive (§1.2).
- **Seven weeks to GLS.** Time spent re-implementing solved problems is time not spent on
  the 30-minute end-to-end claim, which has never been measured and has no NFR page to
  measure against.

## Decision

**Open source is the default for libraries, formats and tooling in OI 3.0. It needs no
request when it is permissively licensed, mainstream, and inside a bounded concern.**
Four rules bound that default.

### Rule 1 — Licence class decides the path

| Class | Licences | Path |
| ----- | -------- | ---- |
| **Green** | MIT, BSD-2/3, Apache-2.0, ISC, MPL-2.0, Unlicense/CC0 | Default yes. No request. Record it |
| **Amber** | LGPL, EPL, CDDL, dual-licensed, custom terms, **no licence file at all** | Tech Lead ruling before it enters a lockfile |
| **Red** | AGPL, SSPL, BSL, Commons Clause, anything "source available" | No, unless consumed as a managed service someone else operates, or ruled on explicitly with Bain Legal |

A dependency with no licence file is red, not amber: unlicensed code is "all rights
reserved" by default.

### Rule 2 — Nothing on the deterministic calculation path takes a dependency whose behaviour can enter a figure

Direct from §3.3. The engine's arithmetic, evaluation order, rounding, unit and currency
handling are ours. Libraries for transport, serialisation, storage and testing around the
engine are fine; a library that computes part of an answer is not. Where one is
unavoidable, it is pinned by exact version, its version is recorded in the trace, and
trace replay (§9.2) has to reproduce the figure byte for byte across an upgrade.

### Rule 3 — Managed first still applies, and library beats server

Where the same capability is available as an Azure managed service, adopt the managed
service — that is the page's own rubric, and it also transfers licence-change and patching
risk to the operator. An embedded library (DuckDB, Zvec) is not a server and does not
trigger this rule.

### Rule 4 — Open core is a Buy, assessed as procurement

Name the tier, the price, the seat or deployment basis, and what happens at renewal,
before the architecture depends on it. "Existing Bain licence" is an assertion to verify,
not an approval — confirm it covers this application, this deployment model and this seat
count.

### And one standing requirement: record the licence

Technology Choices tests every choice for fit, rubric, reversibility and operability, and
never records the licence — the one thing a third-party approval actually turns on. Ask
StatusNeo for **licence, version and project home** as columns on that table, an **SBOM
per deployable** published by the pipeline, and a **remediation SLA** for blocking
Dependabot alerts (proposed: critical within 7 days, high within 30, or a recorded
exception with an owner).

### Two rules for the direction nobody asks about

- **Contributing upstream** — a fix a StatusNeo engineer wants to push to a project used
  here needs Tech Lead sign-off and must carry no Bain IP, client data, or programme
  detail. A bug report with a real repro is the common way client material leaks.
- **Copied code** — a vendored snippet from a blog, an issue thread, or an AI assistant
  carries whatever licence it came from and lands in the repository with no record. It is
  a dependency without a lockfile entry. Treat it as one.

## Consequences

- **StatusNeo is unblocked by default.** A permissive, mainstream library inside a bounded
  concern is a decision they make and record, not a request they raise. That is the point;
  a policy that queues every `npm install` at the Tech Lead will be routed around.
- **A licence column and an SBOM are new work for StatusNeo**, small but not zero, and
  they only stay current if the pipeline produces them rather than a person.
- **Rule 2 has a cost.** Some arithmetic the engine could import, it will write. §3.3
  already accepted that cost for the parser — *"roughly a thousand lines and it is the
  price of the re-derivability guarantee."* This extends the same reasoning rather than
  adding a new position.
- **Red-class licences will occasionally block something good.** The escape hatch is a
  ruling, not silence, and it needs Bain Legal rather than this workspace.
- **This position cannot override firmwide policy.** If Bain has an OSS or third-party
  software standard, it outranks everything here. This workspace has no copy of one, and
  that gap is now logged in `context/open-questions.md`.

## Promotion

Should become a Confluence ADR, and would partly populate the empty
[Security Design](https://bainco.atlassian.net/wiki/spaces/OI30/pages/19705167996) page —
supply chain, dependency policy and SBOM belong in a written control set, which does not
currently exist.

## Sign-off

_Tech Lead decision and date — pending._
