# Multi-Agent Customer Support Triage

Course lab built with the OpenAI Agents SDK. A Router hands customer requests to Billing, Technical, or Account specialists. Each specialist calls a read-only synthetic lookup. Input, output, and tool guardrails protect the workflow; SQLite keeps conversation history; a local SDK tracing processor records handoffs, lookup calls, guardrails, and validated final responses.

**Status:** Offline verification passes. SharedLLM authentication was repaired by removing the SDK's unnecessary upstream Authorization header. `gpt-oss:120b` made a real Router-to-Billing handoff and one lookup, but also produced an unsupported invoice answer; later no-lookup answers were blocked. An approved `glm-5.3-flash` Billing attempt returned `AuthenticationError`. No Billing result is accepted as final submission evidence. Successful live routes, a real Responses API workflow, screenshots, and publication remain open requirements.

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

SharedLLM uses `https://api.sharedllm.com/openai/v1` with `X-SharedLLM-Key`. Set `SHAREDLLM_API_KEY` and an exact, currently available tool-capable `SHAREDLLM_MODEL`. Its standard mode uses Chat Completions through the Agents SDK:

```bash
python triage.py --mode sharedllm --allow-paid --session course-demo --message "Check my invoice"
python triage.py --mode sharedllm --allow-paid --session course-demo --message "What was its amount?"
```

`sharedllm-responses` uses the same gateway and model through the SDK's `OpenAIResponsesModel`; this path has **not** been verified against SharedLLM. The [SharedLLM documentation](https://www.sharedllm.com/docs) currently demonstrates `/chat/completions` and does not establish `/responses` support. A successful real Responses request is required before this mode can count for the lab. The separate `openai-responses` mode uses `OPENAI_API_KEY` and `OPENAI_MODEL`; it can incur separately billed charges and needs separate authorization.

```bash
python triage.py --mode sharedllm-responses --allow-paid --session responses-demo --message "Check my invoice"
python triage.py --mode openai-responses --allow-paid --session responses-demo --message "Check my invoice"
```

The CLI prints a `trace_id` with each successful or blocked turn. `runtime/<mode>-traces.jsonl` stores local SDK spans; `runtime/conversations.db` stores per-mode, per-session history. Both are git-ignored and may contain conversation text. Open [trace_viewer.html](trace_viewer.html) in a browser and choose a reviewed JSONL file to inspect traces locally. This is a local viewer, not OpenAI hosted tracing. Publish only reviewed, sanitized evidence in `outputs/live`; see [reports/live-verification.md](reports/live-verification.md).

Specialists are configured to call their named lookup tool and return its result as the final answer. An output guardrail blocks any specialist response that skipped its lookup or contains a detected secret. This prevents unsupported invoice facts from being published as an answer if a gateway model ignores the requested tool call.

All records and identities used by the demo are synthetic. The fixed trusted identity demonstrates tool ownership checks, but this CLI is not a production authentication service. No refunds, password changes, or account mutations occur.

For the implementation map, see [architecture](docs/architecture.md), [design](docs/design.md), and [submission status](SUBMISSION_CHECKLIST.md). The course PDF was not present in this workspace during this verification; its requirements should be checked against these materials if supplied.
