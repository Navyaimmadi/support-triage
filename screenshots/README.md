# Trace screenshots

These are genuine headless Chrome captures of `trace_viewer.html` loading the matching sanitized local SDK JSONL trace files. `responses-router.png` shows the successful real Responses API Router clarification; `input-guardrail.png` shows the blocked input guardrail. `billing-handoff.png`, `technical-handoff.png`, and `account-handoff.png` show each live specialist handoff, lookup, and final response. `billing-followup.png` shows the contextual follow-up response; that trace has no new handoff or lookup because it uses the prior Billing result persisted in the same session. The trace IDs are visible in the screenshots.

The viewer reads local SDK traces. These images must not be labeled as OpenAI hosted tracing. Review the selected trace file and the screenshots for secrets or personal data before publication.
