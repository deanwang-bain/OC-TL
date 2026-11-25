# OC 3.0 — deployed architecture, as actually built

**Source**: StatusNeo/Engineering's answers to the Archie technical sign-off review,
dated 24 November 2026 (`Archie_OC.xlsx`, sheets "Need from you", "Changes before
go-live", "Do not block", "Other reviews"). This is StatusNeo's own account of their
repositories, Terraform state, and live environments as of that date — **the most
authoritative source this workspace has on what is actually deployed**, as distinct
from `confluence/`, which records what was decided or designed. Where the two disagree,
this file wins for deployment questions; `confluence/` still wins for design rationale
and north-star intent. Full detail and exact wording lives in
`requests/2026-09-23-production-approval-confirmations.md`, Round 15.

**No production environment exists yet.** Everything below is Dev and UAT. UAT is being
built as the intended production design; production is planned to follow UAT's pattern
once built.

## Hosting and regions

- **Dev**: Germany West Central, except the Dev agents' Foundry project (and its
  conversation history), which runs in Sweden Central on a proof-of-concept account
  (`poc-swc-oi-sweden-test`) — not yet defined in Terraform, built by hand in the portal.
- **UAT**: East US 2.
- **Production**: planned for a US region, not yet built.
- "United States only" holds for UAT and the production plan — **it does not hold for
  Dev**, which spans Germany and Sweden.
- All resources sit in Bain's own Azure subscription `nextgenoi01`, created by **Bain's
  CloudLaunch platform** as the landing zone (Entra ID groups, the HCP Terraform
  workspace `nextgenoi01-azure-client` with its deploy credentials, and — via Env0 — the
  GitHub deploy identity and Entra ID app registrations). **Bain DevOps**, not
  StatusNeo, writes and applies the application's own Terraform in Bain's infrastructure
  repository; StatusNeo deploys application code into the environment, not its
  infrastructure, via GitHub Actions using OIDC federation.

## Networking and edge

- **Cloudflare in front of Azure Front Door Premium with WAF** is confirmed as the real
  edge for Dev and UAT (`dev.opcat-nonprod.bain.io`, `uat.opcat-nonprod.bain.io`), not
  just an adopted position on paper.
- **Has Public Endpoints is Yes**, correcting the GRC form's "No." Every route requires
  Entra ID sign-in except static UI assets and health checks.
- **The Cloudflare-only WAF rule is now enforced**: both Dev and UAT moved to
  **Prevention mode with the block rule on** as of 20 November 2026, with no exempt
  path since 22 November — closing the gap the 23 November review flagged (WAF had been
  in Detection/Log-only mode, nothing actually blocked). Raw `azurefd.net` addresses now
  return 403 to anything not arriving via Cloudflare.
- UAT's direction (in progress) is for agents to call services **privately**, through
  Foundry network injection into UAT's own virtual network, removing the need for any
  public agent-tool route. Production will follow this pattern from the start.
- Several Azure services (Key Vault, PostgreSQL, Blob Storage, the Foundry/AI Services
  account, Document Intelligence, the container registry) keep public network access on
  but default-deny, admitting only listed Bain egress addresses plus two Portkey
  addresses on the Foundry accounts.

## Data stores — corrects the GRC form materially

**No Azure SQL. No SharePoint.** The actual stores:

| Data | Store |
| ---- | ----- |
| Case data, roles/permissions, analysis state, document records (extracted text), evidence records, audit trail | **Azure Database for PostgreSQL Flexible Server v18** (one schema per owning service) |
| Partner-uploaded documents, parser output, sealed audit segments, evidence files, licensed company reference snapshot | **Azure Blob Storage** |
| User sessions, live status streams | **Redis** — a container in Dev, **Azure Managed Redis** in UAT (TLS-only, private endpoint, no persistence) |
| Secrets and keys | **Azure Key Vault** |
| Inter-service messages in transit | **Azure Service Bus** |
| Agent conversation history | **Microsoft Foundry Agent Service** (Foundry deletes after 30 days inactivity) |
| Logs and telemetry | Log Analytics, Application Insights, Datadog |
| Company reference/financial data | **Snowflake**, read-only, Semantic Layer only, via a service user — connection being set up, not yet live |

The audit trail is a **hash-chained, append-only PostgreSQL table**, sealed every
minute into create-only Blob segments — not Azure SQL ledger tables. Storage-level
immutability (write-once enforcement at the storage layer, not just the service/DB
layer) is **not yet applied**.

## AI model routing

- **Portkey is live for Dev** (merged to main 18 Nov, deployed 18–20 Nov): all six Dev
  agents route through `https://portkey.bain.dev/v1`.
- **UAT is mid-migration**: the three UAT agents were switched to Portkey in a draft PR
  on 24 Nov, not yet merged; first UAT Portkey deployment is in progress. No UAT agent
  call has gone through Portkey yet as of this writing.
- Models in use: **gpt-5.2** and **claude-opus-5-5**, via Portkey's provider routing to
  the project's own Foundry accounts (Dev: Sweden Central POC account; UAT: East US 2).
  `text-embedding-3-small` is deployed in UAT's Terraform but unused by any agent.
- No fallback exists — reverting an agent to call Foundry directly is a manual change,
  never automatic.
- Document Intelligence (layout/text extraction, not generative) is called directly, not
  through Portkey.
- Local dev no longer calls `api.openai.com` or uses a personal key — corrected to route
  through Bain's AI Hub / Portkey (PR #368).

## Access, vendor model, and commit history remediation

- **Vendor engineers hold named Bain Entra ID accounts** (`v-firstname.lastname@bain.com`),
  marked third-party, used on Bain-managed devices or Bain's VDI — covering Azure,
  Snowflake, Portkey, Datadog, Jira and Teams. GitHub itself does not require SSO.
- **Commit history was remediated on 23 November**: core and UI repository history was
  fully re-authored so every commit now carries a `@bain.com` address (apart from
  GitHub's own merge-commit identity and Dependabot). A branch-protection ruleset now
  **rejects any push with a non-`@bain.com` author address** — tested against the old
  history (111 violations correctly refused). The statusneo.com/gmail.com commits
  flagged in the prior review round no longer exist on any branch.
- **Glean access is a sandbox**, not production Glean — narrower than "full Bain content
  library and client portfolio" as earlier stated to Data Governance. Covers only the
  connectors enabled in that sandbox; documents still open only for users who already
  have access to them in the source system.

## Monitoring

- **Datadog is primary**, Application Insights alongside for Foundry-hosted agents.
  Logs flow since 21 Nov via Bain's central Log Analytics workspace; metrics via the
  Datadog Azure integration; **traces are not yet flowing** (planned via OpenTelemetry).

## Security posture — corrects several form "No" answers to "Yes"

Per Engineering's 24 Nov answers, confirmed against the live Dev/UAT deployment (not
just architectural intent):

- **Encryption at rest**: Yes (Blob double encryption, PostgreSQL/Key Vault
  platform-encrypted, Microsoft-managed keys, no CMK).
- **Encryption in transit**: Yes, with **one exception** — Dev's Redis container does not
  use TLS (UAT's Managed Redis is TLS-only).
- **App and maintainer RBAC**: Yes (Entra app roles map to application roles; per-case
  permissions checked on every read/write; Azure access via Entra groups).
- **Secure sessions**: Yes (server-side in Redis, random 256-bit ID stored only as its
  hash, 30-min idle / 8-hour absolute timeout, PKCE + state + nonce on sign-in).
- **Security headers**: Yes (CSP with no inline script, X-Frame-Options DENY,
  X-Content-Type-Options nosniff, Referrer-Policy, HSTS for one year, Permissions-Policy).
- **Secure cookies**: Yes (`__Host-` prefix, HttpOnly, Secure, SameSite=Lax).
- **Injection/XSS protection**: Yes (schema/typed-model validation, bound SQL
  parameters, uploads checked by signature not executed, agent text rendered as text
  never raw HTML, CSP blocks inline script).
- **CSRF protection**: Yes (synchronizer token + Origin check, SameSite=Lax).
- **Penetration test**: **No** — none done as of 24 Nov. Per-PR Wiz scanning
  (secret/vulnerability/data/software) and per-deployment image scanning with a
  High/Critical-with-fix stop gate are the current control.
- **Sign-in provider**: Microsoft Entra ID (Bain tenant) via OIDC — **not Okta**; the
  stale diagrams naming Okta are being replaced.

## Known, acknowledged gaps (not yet closed)

- **PII/DLP detection and redaction on uploaded content is not implemented.** The GRC
  form's claim that this "hard-stops submission" is **wrong** and is being corrected.
  The control-coverage record marks it `post_mvp ... not scheduled in this build`.
  Planned for January, after the Beta. Interim mitigation proposed: Beta scope is
  public + Bain-internal documents only, no client-provided documents; Bain-only sign-in;
  per-case document visibility.
- **No storage-level immutability** yet on the audit trail or evidence segments —
  write-once is enforced by the application/database layer only, not storage policy.
- **Classification mapping to Bain's formal scheme is still "to be confirmed"** for
  every data store and for the new data-flow diagram's descriptive categories (Public,
  Internal, Personal data, Confidential case content, Licensed third-party data,
  Credentials and secrets).
- **Infrastructure-as-code is not fully merged to `main`** — Dev and UAT changes
  (Front Door, WAF, Postgres, Cloudflare, DNS) sit on open/draft PRs, applied via
  targeted Terraform runs against a **shared workspace and state**, which is why every
  run must stay targeted (an untargeted plan from one branch would attempt to delete
  what that branch's state lacks). Splitting UAT into its own workspace is planned, not
  done.
- **Pendo sent full names until UI PR #110 deploys** (pseudonymous object ID + role only
  going forward); names already sent remain in the Pendo subscription pending removal.
  Pendo also records browser IP unless a subscription setting disables it — unconfirmed
  either way.
- **CloudLaunch landing-zone template version** is unconfirmed; Platform Engineering's
  review of the custom application Terraform (Front Door/WAF/Postgres/App Service) is
  also unconfirmed, though Wiz scans on it pass (IaC scan itself reports as skipped).
- Several resources exist **outside Terraform state**, created by hand during early
  setup (the Sweden POC Foundry account and its role assignments, several Dev Blob
  containers, one storage firewall address, a diagnostic setting) — each tracked with
  a remediation date where known.

## Risk rating — status, not a decision

Still **"to be set"**, per Engineering's own framing — they supplied facts, not a
rating. Global Risk recorded Low on 14 September; a 24 September question to revisit as
High had no reply; the Tech Lead was open to revising as of 29 September. The facts that
have changed since then, on balance: more reassuring on *scope* (Beta is confirmed
internal-data-only, no client documents, Bain-only access, Pendo de-identified), but
**unchanged on the PII/redaction gap** that Data Privacy's 7 October approval was
conditioned on — that control still doesn't exist and won't until January. A Low rating
is more defensible for the Beta specifically, under the interim mitigations Engineering
proposed, than it would be for general production use. This is the Tech Lead's call, not
one this file settles.

## Still to be confirmed (Engineering's own list, not this workspace's)

CloudLaunch template version · Platform Engineering's review of custom Terraform ·
production build and networking dates · model deployment type (Data Zone vs Global
Standard) for production and for Dev's Sweden account · Bain's formal classification
mapping for each store and diagram category · Pendo's IP-collection setting · records
retention period for the audit trail and evidence · whether services move to
private-endpoints-only · date of the Security Architecture Review and penetration test.
