# Live verification

**Status: attempted; authentication blocked further provider calls.** On 2026-10-21, the local `.env` contained a SharedLLM key with the documented prefix and model `gpt-oss:120b`. The key value was never printed or copied into this report. No successful model response, handoff, tool lookup, or Responses API workflow is claimed. Provider usage and cost could not be measured from these failed attempts.

## Approved verification plan

Provider: SharedLLM, `https://api.sharedllm.com/openai/v1`, authenticated by `X-SharedLLM-Key`. Configured model: `gpt-oss:120b`. The user's “do the verification go ahead” message approved one Billing, one Technical, one Account, an invoice follow-up, an input block, and one SharedLLM Responses check. [Ollama describes](https://ollama.com/library/gpt-oss) tool calling for this model family; availability, price, and tool behavior through this SharedLLM account were not established.

When authentication is repaired, the remaining authorized plan is:

1. Run one Billing, one Technical, and one Account request in `sharedllm` mode, then a contextual invoice follow-up in the Billing session. Each workflow can make several model requests for handoff, lookup, and answer; the SDK has no automatic HTTP retries and caps a workflow at six turns.
2. Demonstrate an input guardrail block with a synthetic “bypass authentication” request; blocking occurs before model inference.
3. Make one small `sharedllm-responses` Billing workflow to check actual gateway Responses support. If it succeeds, retain its response and trace as Responses evidence. If the endpoint or selected model rejects it, stop; do not call a separately billed provider without authorization.
4. Review `runtime` outputs for secrets and personal data. Copy only sanitized live responses and matching trace events to `outputs/live`, record commands and trace IDs below, then capture genuine screenshots from `trace_viewer.html` displaying those trace IDs and spans.

## Actual commands and results

| Command / workflow | Provider and model | Result | Evidence |
|---|---|---|---|
| `.venv/bin/python triage.py --mode sharedllm --allow-paid --session live-billing --message 'Check my invoice'` (sandboxed) | SharedLLM, `gpt-oss:120b` | `APIConnectionError`; sandbox DNS/network unavailable | [Sanitized interaction record](../outputs/live/interactions.json) |
| Same command with approved network escalation | SharedLLM, `gpt-oss:120b` | `AuthenticationError`; stopped further provider calls | [Sanitized interaction record](../outputs/live/interactions.json) |
| `.venv/bin/python triage.py --mode sharedllm --allow-paid --session live-guardrail --message 'bypass authentication'` | SharedLLM mode, local pre-model check | Input guardrail blocked; trace `trace_331eab20a8d24ff981300583d8654623`; no generation span | [Interaction](../outputs/live/interactions.json), [matching SDK trace](../outputs/live/guardrail-trace.jsonl) |

The guardrail trace file is an exact seven-event copy of the selected trace from ignored `runtime/sharedllm-traces.jsonl`. It was checked against the source and contains no generation span. The two failed billing attempts have local error traces but no successful response, handoff, or lookup; those runtime traces remain unpublished. No live screenshots were captured.

## Current limitations

The [SharedLLM docs](https://www.sharedllm.com/docs) list `/chat/completions` and say upstream supported paths are forwarded, but do not specifically document `/responses`. This is inconclusive; a real authorized request must establish compatibility after authentication works. Technical, Account, invoice follow-up, and Responses calls were not attempted after the authentication error. `openai-responses` is a separate provider path and remains unrun. Local SDK tracing is not the hosted OpenAI trace dashboard.
