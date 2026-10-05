---
title: "Dev streaming and chat-agent checks: summary"
confluence_id: 19899842692
confluence_url: https://bainco.atlassian.net/wiki/spaces/OI30/pages/19899842692
version: 1
updated: 2026-10-04T18:10:59.038Z
---

# Dev streaming and chat-agent checks: summary

[View in Confluence](https://bainco.atlassian.net/wiki/spaces/OI30/pages/19899842692)

**Date:** 4 October 2026 · **Environment:** dev, through the Azure Front Door endpoint `fde-oi-dev-nonprod-1`, and the chat-assistant agent in the PoC Foundry project

## Bottom line

The case event stream works through Azure Front Door as intended. Events and heartbeats reach the client as they are sent, without buffering, compression or early cuts. Clients can resume after a reconnect without losing or repeating events. The settings that keep this working have plenty of margin, but they depend on each other and should be documented together.

The chat agent works through the Foundry hosted endpoint, for single requests, streaming and multi-turn conversations. Two behaviours affect how it will feel to users, and answers based on web search are currently withheld by the agent's own answer check.

## Case event stream through Front Door

| Area  | Result  | What we found  |
|---|---|---|
| Event delivery  | Pass  | Each event and heartbeat arrived as soon as the BFF sent it. Events from one user action arrived spread out, matching the work being done.  |
| Compression  | Pass  | Even when the client asks for compression, the stream comes back uncompressed, so it isn't held back to be compressed.  |
| Stream lifetime  | Pass  | The stream ran its full designed lifetime of five minutes and ended with the BFF's own close message. Front Door never ended it early.  |
| Front Door timeout  | Pass  | Front Door's origin timeout on the dev profile is 120 s. It applies to silence between bytes, not to the length of the stream. The 15 s heartbeat stays well inside it.  |
| Resume after reconnect  | Pass  | A client reconnecting with its last event id gets exactly the events it missed, in order, then live events.  |
| Invalid resume position  | Pass  | Malformed positions and positions beyond the latest event are refused with a clear 400 that names the problem.  |
| Streams per session  | Pass  | A session holds up to three streams. A fourth is refused with 429, and slots free up as soon as streams close.  |

**Delay between a user action and its events.** Events arrived a few seconds after the user's action. The timings show the delay happens before the event reaches the BFF, in the pipeline that publishes events. It isn't introduced by Front Door or the BFF.

### Where it can fail, and how it is handled

- **Heartbeat vs Front Door timeout.** A stream on a quiet case is kept alive only by the heartbeat. If someone raises the heartbeat interval above Front Door's timeout, or lowers the timeout below the heartbeat interval, quiet streams will be cut. Today the heartbeat is 15 s, the BFF allows at most 60 s, and Front Door is set to 120 s. These three values should be documented together and changed together.
- **Too many open case tabs.** A user with more than three case views open on one session gets 429 on the next one. The response gives no hint of when to retry, and we haven't checked how the UI handles it.
- **A resume position that is too old.** Events are kept for 72 hours, so a client resuming from an older position should get a "cursor expired" response. This wasn't tested, because it needs a case with events older than the retention window.
- **Front Door support status.** Microsoft doesn't list server-sent events as a supported Front Door workload. These results are observed behaviour, not a guarantee. The design doesn't depend on any single connection lasting long: streams close after five minutes and clients resume by event id.

## Chat assistant agent in Foundry

| Area  | Result  | What we found  |
|---|---|---|
| Streaming responses  | Pass, with caveats  | Progress steps arrive before the answer, as separate events.  |
| Conversations  | Pass  | Conversations can be created with metadata, a follow-up in the same conversation keeps the context, the stored history can be read back, and a conversation can be deleted.  |
| Acting as another user  | Pass  | A request asking to act as a different user is refused unless the caller holds the impersonation role.  |

### Caveats and gaps

- **A silent start.** Nothing, not even the response headers, reaches the client until the agent has finished reading the case. So the first progress step ("Reading the case") appears only once that step is already done. From outside it isn't clear whether the agent or the Foundry hosting layer holds the response back.
- **The answer arrives all at once.** The answer text comes as a single block, not word by word, so the UI can't show it being typed out.
- **Web-cited answers are withheld.** The agent checks every citation against the case's own sources before showing an answer, and web search results aren't counted as sources. Any answer that relies on web search is replaced with a message saying it couldn't be checked. Web search itself works in the project, so this needs a change in the agent, not in infrastructure.
- **Stored conversation data.** Each stored user message holds the full turn document, including the user's identity and tenant. That data falls under the rule that users must be able to delete their conversations.

## Recommended next steps

1. Document the heartbeat interval, Front Door's origin timeout and the BFF's stream lifetime together as dependent settings.
1. Decide how the UI should behave when it gets 429 for too many streams, and consider adding a retry hint to that response.
1. Test the expired-cursor response once a case has events older than 72 hours.
1. Find out whether the delay before the agent's first streamed event comes from the agent or from Foundry hosting. If it's the agent, send the first progress step before the case reading starts.
1. Change the agent's answer check to accept the sources its tools return, then redeploy and test web search again.

## How this was tested

All checks ran against the deployed dev environment, with no code or configuration changes. Stream behaviour was measured by a small client that records when each line arrives, using a test user's session, while case actions were run in the browser. Front Door settings were read from the deployed profile without changing anything. The agent was called directly through its Foundry endpoint, and the test conversation was deleted afterwards.
