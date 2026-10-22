# Brief design document

## Purpose and scope

Provide a production-style teaching example of customer support triage, not a deployed production service. All records and identities are synthetic. Billing can explain an invoice but cannot issue refunds; Account can explain status but cannot reset passwords; Technical reads fixed diagnostics.

## Decisions

Use the OpenAI Agents SDK for orchestration rather than hand-built live routing. Real models decide handoffs; the deterministic fixture exists only for reliable no-credit tests. Returning to Router on every new turn allows changes of subject. SQLite retains full history for contextual follow-ups. A six-turn maximum, no automatic HTTP retries and 30-second provider timeout bound individual runs; these are not a dollar budget guarantee.

Three guardrail layers demonstrate different boundaries: blocking input validation, final-output validation, and tool ownership checks. Tools repeat authorization checks as defense in depth. Every final responder including Router has an output guardrail. Specialists request their named lookup and return the lookup result directly. Their output guardrail blocks a response if the lookup did not run. This policy was added after a live model produced unsupported invoice details. Secret detection is a deliberately narrow heuristic, not comprehensive DLP or a prompt-injection firewall. Input restrictions cannot replace authorization.

## Provider compatibility and limits

SharedLLM configuration follows the gateway/header guidance. The pinned OpenAI SDK initially sent `Authorization: Bearer unused` in addition to `X-SharedLLM-Key`; the gateway treats a supplied Authorization header as an upstream key. The SharedLLM client suppresses that header, verified with a mock request. On the custom resource route, identity encoding avoids a confirmed compressed `/models` response decompression error. A bounded live run with `~z-ai/glm-flash-latest` completed Billing, Technical, and Account handoffs and lookups; see the matching sanitized traces and SDK-reported usage in the live report. Earlier requests with `glm-5.3-flash`, `kimi-k2.6`, and `kimi-k2.7-code` failed authentication, and earlier custom-model attempts failed before HTTP response; the former exact POST cause is unrecoverable. The contextual follow-up answered from the same persisted Billing session, without a new lookup. The gateway's [public documentation](https://www.sharedllm.com/docs) demonstrates Chat Completions but does not explicitly document Responses. A real `sharedllm-responses` Router clarification succeeded and its SDK trace contains a Responses span and validated final answer. A separate Responses Billing handoff was blocked because no lookup ran. The separate `openai-responses` path uses a different provider and was not run. Native extended thinking and provider prompt caching are not required or claimed. Never call a simulated or Chat Completions response a Responses API workflow.

## Privacy and deployment gaps

Local traces and sessions can contain conversation text. Only synthetic inputs should be used. The local final-response event intentionally stores the validated answer; inspect it before publication. Hosted tracing is off by replacement of its processor. No retention policy, encrypted persistence, authenticated multi-user server, rate limiter, production diagnostic integration, robust DLP, human approval queue or deployment monitoring is included. Before production, add those controls, bound/compact conversation history, scope sessions to authenticated users and define cleanup on guardrail failures.

## Validation

Offline tests cover all specialist destinations, a contextual invoice follow-up, persistent history after reopening, session isolation, SDK trace span types linked by trace ID, direct ownership checks, provider adapter selection, and input/tool/output blocks. Scripted tests do not establish live model quality, gateway support, or Responses endpoint compatibility. Live acceptance tests and screenshots are explicit submission gates.

## References

- Course PDF: referenced in the original project notes but not present in this workspace during the current verification.
- https://developers.openai.com/api/docs/guides/agents
- https://developers.openai.com/api/docs/guides/agents/guardrails-approvals
- https://developers.openai.com/api/docs/guides/text
- https://openai.github.io/openai-agents-python/

Implementation signatures were inspected against installed openai-agents 0.24.0; dependencies are pinned for reproducibility.
