# Live verification

**Status: not run.** No credentials were present in local `.env` or the relevant process environment during preparation. No course credits or separate provider credits were consumed. No successful Responses API workflow or live trace screenshot is claimed.

## Planned small verification run (requires one consolidated approval)

Provider: SharedLLM, `https://api.sharedllm.com/openai/v1`, authenticated by `X-SharedLLM-Key`. Model: exact tool-capable `SHAREDLLM_MODEL` from the user's account; currently unavailable. The public [SharedLLM documentation](https://www.sharedllm.com/docs) describes a model catalog with prices and pool availability, but does not expose this account's model choice here.

After credentials, model, and approval are available:

1. Run one Billing, one Technical, and one Account request in `sharedllm` mode, then a contextual invoice follow-up in the Billing session. Each workflow can make several model requests for handoff, lookup, and answer; the SDK has no automatic HTTP retries and caps a workflow at six turns.
2. Demonstrate an input guardrail block with a synthetic “bypass authentication” request; blocking occurs before model inference.
3. Make one small `sharedllm-responses` Billing workflow to check actual gateway Responses support. If it succeeds, retain its response and trace as Responses evidence. If the endpoint or selected model rejects it, stop; do not call a separately billed provider without authorization.
4. Review `runtime` outputs for secrets and personal data. Copy only sanitized live responses and matching trace events to `outputs/live`, record commands and trace IDs below, then capture genuine screenshots from `trace_viewer.html` displaying those trace IDs and spans.

## Actual results

| Command / workflow | Provider and model | Result | Evidence |
|---|---|---|---|
| Not run | Not selected | Blocked by absent credentials/model and spend approval | None |

## Current limitations

The [SharedLLM docs](https://www.sharedllm.com/docs) list `/chat/completions` and say upstream supported paths are forwarded, but do not specifically document `/responses`. This is inconclusive; a real authorized request must establish compatibility. `openai-responses` is a separate provider path and remains unrun. Local SDK tracing is not the hosted OpenAI trace dashboard. No cost is reported because no live usage was measured.
