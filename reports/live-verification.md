# Live verification

**Status: blocked by live provider behavior; no accepted live specialist result yet.** On 2026-10-21, SharedLLM authentication initially failed because the pinned OpenAI SDK sent `Authorization: Bearer unused` alongside `X-SharedLLM-Key`. Removing that header resolved authentication for `gpt-oss:120b`. The key value was never printed or copied into this report. One live Router-to-Billing handoff and `billing_lookup` ran, but the specialist added unsupported invoice facts, so that result is rejected as submission evidence. Later no-lookup attempts were blocked by the strengthened output guardrail. After user approval to switch models, the first `glm-5.3-flash` call returned `AuthenticationError`, and further provider calls stopped. No real Responses API workflow is claimed. Provider usage and cost were not measured.

## Approved verification plan

Provider: SharedLLM, `https://api.sharedllm.com/openai/v1`, authenticated by `X-SharedLLM-Key`. Configured model: `gpt-oss:120b`. The user's “do the verification go ahead” message approved one Billing, one Technical, one Account, an invoice follow-up, an input block, and one SharedLLM Responses check. The user-provided dashboard listed `gpt-oss:120b` at about $0.262/M blended with 4/4 pool keys; this is a catalog estimate, not measured cost. [Ollama describes](https://ollama.com/library/gpt-oss) tool calling for this model family. Its tool use through SharedLLM proved inconsistent in the runs below.

The remaining verification plan is:

1. Obtain an accepted Billing result with a real lookup, then run Technical and Account requests and a contextual invoice follow-up in the Billing session. Each workflow can make several model requests; the SDK has no automatic HTTP retries and caps a workflow at six turns. The user approved a switch to the lower-cost, tool-capable `glm-5.3-flash`; its first call failed authentication despite the same gateway key having worked with `gpt-oss:120b`.
2. The synthetic “bypass authentication” input guardrail demonstration is complete; it blocked before model inference.
3. Make one small `sharedllm-responses` Billing workflow to check actual gateway Responses support. If it succeeds, retain its response and trace as Responses evidence. If the endpoint or selected model rejects it, stop; do not call a separately billed provider without authorization.
4. Review `runtime` outputs for secrets and personal data. Copy only sanitized live responses and matching trace events to `outputs/live`, record commands and trace IDs below, then capture genuine screenshots from `trace_viewer.html` displaying those trace IDs and spans.

## Actual commands and results

| Command / workflow | Provider and model | Result | Evidence |
|---|---|---|---|
| `.venv/bin/python triage.py --mode sharedllm --allow-paid --session live-billing --message 'Check my invoice'` (sandboxed) | SharedLLM, `gpt-oss:120b` | `APIConnectionError`; sandbox DNS/network unavailable | [Sanitized interaction record](../outputs/live/interactions.json) |
| Same command with approved network escalation | SharedLLM, `gpt-oss:120b` | `AuthenticationError`; stopped further provider calls | [Sanitized interaction record](../outputs/live/interactions.json) |
| `.venv/bin/python triage.py --mode sharedllm --allow-paid --session live-guardrail --message 'bypass authentication'` | SharedLLM mode, local pre-model check | Input guardrail blocked; trace `trace_331eab20a8d24ff981300583d8654623`; no generation span | [Interaction](../outputs/live/interactions.json), [matching SDK trace](../outputs/live/guardrail-trace.jsonl) |
| Billing after key replacement, before header fix | SharedLLM, `gpt-oss:120b` | `AuthenticationError`, trace `trace_24d0ce6aaa8040c3afe9efd622e19a6d` | [Sanitized interaction record](../outputs/live/interactions.json) |
| Billing after header fix, trace `trace_be9783051e294c0ebc2f804c46defdb1` | SharedLLM, `gpt-oss:120b` | Handoff occurred, no lookup; model invented invoice details. Rejected as evidence. | Local ignored runtime trace; [sanitized record](../outputs/live/interactions.json) |
| Billing with required tool, trace `trace_b416e8a90ea541ecba16b4c7cd798a7b` | SharedLLM, `gpt-oss:120b` | Handoff and `billing_lookup` occurred, but final model answer added unsupported details. Rejected as evidence. | Local ignored runtime trace; [sanitized record](../outputs/live/interactions.json) |
| Billing with lookup-required output guardrail, trace `trace_29a27c1bc44446b783cc7cf567a63f49` | SharedLLM, `gpt-oss:120b` | No lookup; output blocked | Local ignored runtime trace; [sanitized record](../outputs/live/interactions.json) |
| Billing with named tool choice, trace `trace_dcee1a0a5c66485f960e280397946647` | SharedLLM, `gpt-oss:120b` | No lookup; output blocked | Local ignored runtime trace; [sanitized record](../outputs/live/interactions.json) |
| `.venv/bin/python triage.py --mode sharedllm --allow-paid --session glm-billing --message 'Check my invoice'`, trace `trace_ecc1de86ffac4d719736c7bb31e59758` | SharedLLM, `glm-5.3-flash` | `AuthenticationError`; stopped provider calls | [Sanitized record](../outputs/live/interactions.json) |

The guardrail trace file is an exact seven-event copy of the selected trace from ignored `runtime/sharedllm-traces.jsonl`. It was checked against the source and contains no generation span. The other local runtime traces remain unpublished while results are being reviewed. No live screenshots were captured.

## Current limitations

The [SharedLLM docs](https://www.sharedllm.com/docs) list `/chat/completions` and say upstream supported paths are forwarded, but do not specifically document `/responses`. This is inconclusive; a real authorized request must establish compatibility. Technical, Account, invoice follow-up, and Responses calls are still pending. The `glm-5.3-flash` error may reflect model or pool credentials, but the redacted SDK trace does not establish its cause. `openai-responses` is a separate provider path and remains unrun. Local SDK tracing is not the hosted OpenAI trace dashboard.
