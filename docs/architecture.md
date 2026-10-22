# Architecture

Each CLI turn starts at Router with persisted conversation history. Router delegates via SDK handoff to Billing, Technical or Account. Each specialist has one read-only synthetic lookup tool and an output guardrail. The specialist requests its named tool and, when called, returns the verified lookup result as its final answer. A skipped lookup trips the output guardrail. The blocking input guardrail runs before model inference. The tool guardrail verifies the customer ID against trusted application context; each tool also checks ownership directly.

```mermaid
flowchart TD
    U[User turn] --> G[Blocking input guardrail]
    G --> R[Router and SQLite history]
    R --> B[Billing]
    R --> T[Technical]
    R --> A[Account]
    B --> V[Ownership-checked lookup]
    T --> V
    A --> V
    V --> O[Output guardrail and response]
```

SDK tracing surrounds execution and exports trace, agent, handoff, function and guardrail spans. A custom span records only the validated answer. Routing decisions are observable from handoff destinations, not hidden chain-of-thought. Local JSONL export avoids dependence on hosted trace authentication. Remote export is not enabled.

Provider paths: `OfflineModel` is a scripted fixture; `sharedllm` uses `OpenAIChatCompletionsModel`; `sharedllm-responses` and the separate `openai-responses` path use `OpenAIResponsesModel`. A real SharedLLM Responses Router clarification succeeded and is captured in `outputs/live/responses-success-trace.jsonl`; the specialist Billing Responses attempt was blocked because the model skipped its lookup. All modes use the same agent graph. SQLite session IDs are prefixed by provider mode within one ignored local database. Persistent session state is not an authentication mechanism. Each CLI result includes the local SDK trace ID for matching evidence.

The current live SharedLLM custom-model evidence includes a verified handoff and lookup for each specialist. The contextual Billing follow-up reuses the prior synthetic lookup stored in SQLite and is traced as a Router response without a new handoff or lookup; see `outputs/live/billing-followup-trace.jsonl`. Sanitized traces and screenshots are listed in `reports/live-verification.md`.
