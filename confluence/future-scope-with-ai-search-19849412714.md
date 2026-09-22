---
title: "Future Scope-- With ai search."
confluence_id: 19849412714
confluence_url: https://bainco.atlassian.net/wiki/spaces/OI30/pages/19849412714
version: 1
updated: 2026-09-21T06:05:54.717Z
---

# Future Scope-- With ai search.

[View in Confluence](https://bainco.atlassian.net/wiki/spaces/OI30/pages/19849412714)

# Future scope

>

**Scope.** This page proposes moving document handling from an ad-hoc, chat-time process to an **event-driven ingestion pipeline**: files are parsed by Azure Document Intelligence when they land, chunked by section, embedded, and served from a single filtered Azure AI Search index. The diagrams show the current and target shapes; the sections after them give the design decisions, the benefits, the comparison against plain web search, and the limitations.

## Architecture diagrams

Four diagrams, in increasing detail. Figure 2 is roughly where things stand today — the RAG index is written to blob storage. Figures 3 and 4 are the proposal, where that index moves to Azure AI Search and ingestion becomes event-driven. Reading them in order makes the argument in Design decisions concrete.

All four are attached as SVG so they stay sharp when zoomed; they are wide (up to 6,300 px) and are best opened full-screen.

### Figure 1 — The pipeline at a glance

![01-pipeline-at-a-glance.svg](_attachments/19849412714/01-pipeline-at-a-glance.svg)

**What it shows.** The whole system reduced to six steps: **input** (preference + ids) → **find peers** → **get metrics** → **RAG agent** → **recommend** → **peers**. Underneath sits the supporting infrastructure it draws on: **new file** events, **Document Intelligence**, **AI Search** and **blob storage**.

**Why it matters.** The orientation diagram — use it to introduce the system before showing anyone Figure 4.

### Figure 2 — Storage paths as they work today

![02-storage-paths-current.svg](_attachments/19849412714/02-storage-paths-current.svg)

**What it shows.** The same flow with the actual blob layout written out, organised as three numbered paths:

1. **blob documents path**
1. **rag storage path**
1. **param-index** (append, rerank, reset)

Inputs are user preference, data metrics, project id and user id. A **web search** produces *"based on user preference, internet research, I found these peers"* and writes to blob; a second **web search** resolves *peer name → company name* and finds basic metrics per company. The **blob chat agent (RAG)** then *"downloads the files from blob, chunks them, stores them back to blob, and starts talking to it"* — with a manual *"refresh data for specific folder (project/user)"* action. Results feed a **recommendation engine** combining internet peers with CapIQ peers data.

The three storage roots are spelled out on the diagram:

| Path  | Blob location  |
|---|---|
| Peers, raw  | `project id/uuid/username/user_id/data/websearch/peers/raw/`  |
| Peers data, raw  | `project id/uuid/username/user_id/data/websearch/peers_data/raw/`  |
| RAG index  | `project id/uuid/username/user_id/data/websearch/peers_rag/`  |

**Why it matters.** This is the *before* picture, and the two things this page proposes changing are both visible on it: **the index is stored on blob**, and **refresh is manual**.

### Figure 3 — Event-driven ingestion

![03-event-driven-ingestion.svg](_attachments/19849412714/03-event-driven-ingestion.svg)

**What it shows.** The proposed shape. A user uploads filings and reports to `blob/uploads`; the **new file** event goes to **Event Grid** → **queue** → **Document Intelligence** → **chunk + embed** → **Azure AI Search**. A parse failure goes to a **dead letter** rather than disappearing. The web-search paths still write `peers/raw` and `peers_data/raw`, the **RAG agent** reads the index, and the **chat engine** answers with **peers, why, sources**.

**Why it matters.** This is the diagram that shows the queue doing its job: the upload returns immediately and the parse happens behind the event.

### Figure 4 — Target architecture, annotated

![04-target-architecture.svg](_attachments/19849412714/04-target-architecture.svg)

**What it shows.** The fullest version, split into three labelled lanes — **documents path**, **rag path**, and **params** — with the design decisions written onto the diagram itself:

- **"new file event — ingestion, runs on its own clock"**
- **Event Grid** — `BlobCreated` on the project prefix
- **Azure Document Intelligence**, *layout model* → text, tables, key-value pairs, page spans
- **"extracted json back to blob **`.../extracted/` — reparse is free"
- **chunk by section + embed**, `text-embedding-3-small`
- **Azure AI Search** — *one index*, filtered by `project_id` + `user_id`, *hybrid: keyword + vector*
- **"parse failed → dead letter + status on the record"**
- **blob chat agent (RAG)** — *"queries a ready index, does not chunk at chat time"*
- **recommendation engine** — internet peers + CapIQ peers data → **peers, ranked**

Blob roots on this version: `.../data/uploads/`, `.../data/websearch/peers/raw/`, `.../data/websearch/peers_data/raw/`, `.../data/websearch/peers_rag/`. Web search runs through a **serpapi engine**.

**Why it matters.** Every annotation here maps onto a bullet in Design decisions below — this is the reference diagram for the proposal.

## Design decisions

- **AI Search, not blob** — the index lives in Azure AI Search. Blob cannot serve a filtered hybrid query. AI Search gives keyword + vector + the semantic reranker, and filters by `project_id` and `user_id`, which is the per-folder scoping the pipeline needs.
- **Parse first** — Document Intelligence runs before chunking, not instead of it. A filing's tables do not survive naive text chunking, and parsing at chat time makes the first question slow.
- **Event driven** — a file indexes itself when it lands. Manual refresh stays as an escape hatch, not the only path.
- **Keep the extraction** — extracted JSON stays in blob. Document Intelligence is the expensive step, so re-chunking or changing the embedding model never re-runs it.
- **Queue in between** — a 200-page filing takes minutes; the upload must return immediately.

## Benefits

### Azure AI Search instead of an index on blob

- **Speed** — a blob index has to be downloaded and searched inside the app process on every question. AI Search answers server-side in tens of milliseconds, with no cold start after a restart.
- **Hybrid** — keyword and vector in one query. Keyword catches tickers, exact figures and defined terms; vector catches paraphrase. A blob index gives you whichever one you coded, not both.
- **Reranker** — one flag improves the ordering of the top results, with no extra LLM calls.
- **Filtering** — `project_id` and `user_id` are filters inside the query, so one index serves every project safely. With a blob index you need a separate file per folder, or you load everything and filter afterwards.
- **Incremental** — add or delete single documents. A blob index usually means rewriting the whole file, which is slow and races with concurrent readers.
- **Scale** — the index no longer has to fit in the app's memory.

### Document Intelligence before chunking

- **Tables survive** — filings are mostly tables. Plain text extraction turns a table into a run of loose numbers with no row or column meaning, and wrong numbers reaching the model are worse than no numbers.
- **Citations** — each chunk carries its page and section, so an answer can point at page 42 of a named file.
- **OCR** — a PDF that is really an image yields nothing from a text librareads it.
- **Chunk boundaries** — chunking by section rather than character count means fewer chunks cut mid-sentence or mid-table.
- **One shape** — PDF, docx and images all come back in the same structure,s one path.

### New file event

- **Always fresh** — the document is searchable by the time the user asks. Nobody has to remember to press refresh.
- **Fast upload** — the parse happens behind the event, not in the request.
- **One path** — user uploads and pipeline outputs index themselves the same way.
- **Replayable** — the queue gives retries and a dead letter, so a bad fileer than a silent gap.
- **Scales out** — a burst of fifty files drains through the queue instead of hitting the Document Intelligence rate limit at once.

### Keeping the extracted JSON

- **Parse once** — changing chunk size, changing the embedding model, or rething extra.
- **Cheap reset** — re-index from `extracted/` with no Document Intelligence call.
- **Debuggable** — you can read exactly what the model was given.

### Overall

- **Cost** — parsing is once per file, not once per chat. Embedding is once per chunk.
- **Traceability** — every answer walks back to a blob path and a page.
- **Isolation** — per-project filters keep one customer's documents out of another's answers.

## Compared with plain web search and embedding HTML

### Audit

- **Evidence kept** — the original file sits in blob with the date it was fthere is nothing to open, only a vector and, if you were careful, a URL.
- **URLs rot** — a page cited today may be edited or gone in six months. An audit that cannot reach the source is not an audit.
- **Full chain** — raw file, extracted JSON, chunk, answer. Naive embeddingage to vector, and the middle is unrecoverable.
- **Reproducible** — re-running a year later uses the same stored inputs. Web search returns different pages on different days.
- **Who and when** — the blob path carries project and user, the file event
- **Provable scope** — you can list exactly which documents informed a conclusion. With live web search you cannot reconstruct it.

### Search quality

- **No page junk** — navigation, cookie banners, footers and ad rails get eent and pollute the top results.
- **Tables hold** — a financial table as a string loses its rows and columns, so numbers lose their line item.
- **Whole document** — web search hands you the few pages an engine picked;where segment detail usually is.
- **Many questions** — the index answers repeatedly and cheaply. Web search pays latency and cost per question for a summary you cannot re-query.
- **Stable results** — same query, same chunks, until you change the index.
- **Filtered scope** — open web search can pull in a different company with a similar name and answer confidently from it.
- **Freshness on purpose** — you choose when to re-ingest, rather than a wet.

## Limitations

### Cost and operations

- **Standing bill** — AI Search is a running service, charged whether anyone queries it or not. A blob index costs storage only.
- **Per-page parsing** — Document Intelligence is priced per page, and the layout model costs more than plain read. A few thousand filings is a real number.
- **More moving parts** — Event Grid, queue, worker, Document Intelligence, AI Search and blob all have to be deployed, monitored, secured and paid for. The simple version has one.
- **Harder local dev** — you need real Azure services or emulators to run the ingestion path end to end.

### Freshness and consistency

- **Ingest lag** — a file is not searchable the moment it lands. Parsing takes seconds to minutes, so the UI needs a visible status.
- **Index drift** — blob and AI Search can diverge. Deleting a file from blob does not remove its chunks unless deletion is also evented; you need a reconciliation job.
- **Stale by design** — freshness being a decision cuts both ways. The index stays as of the last ingest until someone refreshes it.

### What the tooling cannot do

- **Parsing is not perfect** — nested tables, multi-column layouts, footnotes and handwriting still come out wrong sometimes. It gives layout, not meaning, and has page-size and rate limits.
- **AI Search has ceilings** — index size and vector capacity depend on tier, the semantic reranker has its own quota and only reranks the top slice, and filter fields must be designed up front. A schema change means a re-index.
- **Retrieval can still miss** — hybrid improves the odds, it does not guarantee the right chunk is in the top k. Bad chunking is not fixed by the index.
- **The model can still be wrong** — a citation proves where a chunk came from, not that the answer read it correctly.

### Audit caveats

- **Inputs are reproducible, outputs are not** — the same chunks can produce different wording, sometimes different numbers, on a second run. Storage fixes the evidence, not the model's determinism.
- **Retention is now your problem** — keeping every source document has compliance and cost consequences, and a deletion request has to reach blob, `extracted/` and the index.
- **One index, one bug** — with per-project filters, a mistake in the filter leaks across projects. An index per project is safer and costs more.

### Scope

- **Documents only answer what is in them** — finding new peers still needs live web search. This design makes the evidence trail solid; it does not remove the search step.
