# Offline verification

Verified on 2026-10-21 with Python 3.12, `openai-agents==0.24.0`, and the pinned dependencies in `requirements.txt`.

`.venv/bin/python -m pytest -q`: **4 passed**. Tests cover all specialist routes, a contextual invoice follow-up, SQLite reopening and session isolation, handoff/tool/guardrail/final spans linked by trace ID, all three guardrail tripwires, direct ownership enforcement, and adapter selection. The blocking input guardrail invokes the model zero times.

`.venv/bin/python demo.py`: succeeded. It generated [interactions](../outputs/offline/interactions.json) and [traces](../outputs/offline/traces.jsonl), including three blocked scenarios. The fixture's route choice is deterministic and is **not** evidence of live LLM reasoning, SharedLLM compatibility, a Responses request, or API cost.

The sandbox blocked the first dependency download because DNS access was unavailable. A user-approved dependency installation succeeded; no live model calls were made.
