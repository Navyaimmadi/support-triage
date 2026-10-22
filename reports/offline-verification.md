# Offline verification

Verified on 2026-10-22 with Python 3.12. The clean setup resolved `openai-agents==0.24.0`, `openai==3.36.1`, and the versions specified by `requirements.txt`.

`.venv/bin/python -m pytest -q`: **8 passed** in both the project virtual environment and a clean temporary environment installed from `requirements.txt`. Tests cover all specialist routes, contextual follow-up, SQLite reopening and session isolation, handoff/tool/guardrail/final spans linked by trace ID, all three guardrail tripwires, direct ownership enforcement, adapter selection, gateway header handling, identity encoding on the custom endpoint, safe exception-chain logging, output-token settings, and rejection of a specialist answer that skipped its lookup. The blocking input guardrail invokes the model zero times.

`.venv/bin/python demo.py`: succeeded. It generated [interactions](../outputs/offline/interactions.json) and [traces](../outputs/offline/traces.jsonl), including three blocked scenarios. The fixture's route choice is deterministic and is **not** evidence of live LLM reasoning, SharedLLM compatibility, a Responses request, or API cost. Running the offline demo and tests makes no live model calls.

The default sandbox blocks external DNS. A user-approved installation in the temporary clean environment succeeded after network escalation; the temporary environment was removed after testing.
