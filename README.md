# Multi-Agent Customer Support Triage

Course lab built with the OpenAI Agents SDK. A Router hands customer requests to Billing, Technical, or Account specialists. Each specialist calls a read-only synthetic lookup. Input, output, and tool guardrails protect the workflow; SQLite keeps conversation history; a local SDK tracing processor records handoffs, lookup calls, guardrails, and validated final responses.

**Status:** Offline tests pass. SharedLLM live verification succeeded for Billing, Technical, and Account with actual SDK handoffs, named lookup calls, and lookup-derived answers. A Billing follow-up in the same persisted session returned the earlier lookup result without restating invoice details; its turn used history and did not repeat the handoff or lookup. A real Responses API Router clarification and a live input-guardrail block are also preserved.

## Setup and offline verification

Use Python 3.11 or newer. The example uses `python3.12`; substitute any installed 3.11+ executable if needed. From this directory:

```bash
python3.12 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
python -m pytest -q
python demo.py
python triage.py --message "Check my invoice"
```

`demo.py` writes [offline interactions](outputs/offline/interactions.json) and [offline SDK traces](outputs/offline/traces.jsonl). Its `OfflineModel` is a scripted test double. It exercises the SDK agent graph, handoffs, guardrails, tools, and sessions without model inference or API credits. The second turn, “What was its amount?”, uses prior session history to refer to the invoice.

## Live provider configuration

Copy `.env.example` to an ignored `.env` and enter credentials there. Do not commit `.env` or paste keys into prompts, screenshots, or output artifacts. Live commands require `--allow-paid`; run them only with explicit approval for the selected provider and model.

SharedLLM's documented OpenAI-compatible base URL is `https://api.sharedllm.com/openai/v1`; a Custom OpenAI-compatible resource-pool endpoint is exposed at `https://api.sharedllm.com/custom-openai/v1`. Both use `X-SharedLLM-Key`. The docs say routing is by model ID and IDs may be used on compatible endpoints; use the custom route when explicitly targeting the configured custom endpoint, and don't infer endpoint interchangeability from an error. Set `SHAREDLLM_API_KEY`, the intended base URL, and an exact currently available `SHAREDLLM_MODEL`. The custom route is configured to request identity encoding because its compressed `/models` response failed HTTPX decompression in verification. Standard mode uses Chat Completions through the Agents SDK:

```bash
python triage.py --mode sharedllm --allow-paid --session course-demo --message "Check my invoice"
python triage.py --mode sharedllm --allow-paid --session course-demo --message "What was its amount?"
```

For bounded runs, `--max-turns 3 --max-output-tokens 512` caps the SDK agent loop and per-request output tokens; the live verification also disables automatic retries in the client. The CLI default remains six turns.

`sharedllm-responses` uses the same gateway and model through the SDK's `OpenAIResponsesModel`. A real Router clarification completed successfully through this mode; see [its interaction](outputs/live/interactions.json) and [matching trace](outputs/live/responses-success-trace.jsonl). A specialist handoff through Responses was also observed, but its answer was blocked because no lookup occurred. The [SharedLLM documentation](https://www.sharedllm.com/docs) demonstrates `/chat/completions`; the real trace establishes Responses behavior for this configured gateway/model at verification time. The separate `openai-responses` mode uses `OPENAI_API_KEY` and `OPENAI_MODEL`; it can incur separately billed charges and needs separate authorization.

Live specialist evidence for the configured custom model is in [the verification report](reports/live-verification.md), including [Billing](outputs/live/billing-success-trace.jsonl), [Technical](outputs/live/technical-success-trace.jsonl), [Account](outputs/live/account-success-trace.jsonl) and [the contextual Billing follow-up](outputs/live/billing-followup-trace.jsonl). The follow-up used the same SQLite session as the Billing lookup and answered from its persisted history; it did not perform a second lookup.

```bash
python triage.py --mode sharedllm-responses --allow-paid --session responses-demo --message "Check my invoice"
python triage.py --mode openai-responses --allow-paid --session responses-demo --message "Check my invoice"
```

The CLI prints a `trace_id` with each successful or blocked turn. `runtime/<mode>-traces.jsonl` stores local SDK spans; `runtime/conversations.db` stores per-mode, per-session history. Both are git-ignored and may contain conversation text. Open [trace_viewer.html](trace_viewer.html) in a browser and choose a reviewed JSONL file to inspect traces locally. This is a local viewer, not OpenAI hosted tracing. Publish only reviewed, sanitized evidence in `outputs/live`; see [reports/live-verification.md](reports/live-verification.md).

Specialists are configured to call their named lookup tool and return its result as the final answer. An output guardrail blocks any specialist response that skipped its lookup or contains a detected secret. This prevents unsupported invoice facts from being published as an answer if a gateway model ignores the requested tool call.

All records and identities used by the demo are synthetic. The fixed trusted identity demonstrates tool ownership checks, but this CLI is not a production authentication service. No refunds, password changes, or account mutations occur.

For the implementation map, see [architecture](docs/architecture.md), [design](docs/design.md), and [submission status](SUBMISSION_CHECKLIST.md).
