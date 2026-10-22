# Submission status

**Status: ready for submission.** Offline tests and SharedLLM live workflows are verified. SharedLLM `~z-ai/glm-flash-latest` completed Billing, Technical, and Account handoffs and lookups with grounded final responses. The Billing follow-up used the same persisted SQLite session and answered from the prior lookup; it did not make another handoff or lookup. A real Responses API Router clarification and a live input-guardrail block are also captured.

| Requirement | Current evidence | Status |
|---|---|---|
| Router, Billing, Technical, Account | `triage.py`, offline route tests, three accepted live route traces | Implemented and live verified |
| Actual SDK handoffs | Offline spans and Billing, Technical, Account live handoff traces | Verified offline and live |
| Input, output, tool guardrails | Offline tests and blocked scenarios; real SharedLLM-mode input block trace | Verified; live input block captured |
| Persistent state and contextual follow-up | SQLite reopen/isolation tests; live invoice amount follow-up in same session | Verified; follow-up uses prior persisted lookup, no new tool call |
| Real Responses API workflow | Successful SharedLLM Router clarification; `outputs/live/responses-success-trace.jsonl` and screenshot | Verified for Router clarification; specialist Responses turn blocked on missing lookup |
| Routing, handoff, tool, guardrail, final traces | Local SDK JSONL and trace IDs; live input block and three accepted specialist traces | Verified offline and live |
| Source, architecture, design, samples | Repository files and offline samples | Prepared |
| Genuine live screenshots | Responses Router, input guardrail, Billing, Technical, Account, and Billing follow-up screenshots under `screenshots/` | Captured from local SDK trace viewer |
| Public GitHub repository | [github.com/Navyaimmadi/support-triage](https://github.com/Navyaimmadi/support-triage), branch `main` | Published; local branch tracks `origin/main` |

Chat Completions and the offline fixture do not meet the Responses requirement; the successful Router clarification uses the real Responses API. The explicit lab deliverables documented in this repository are evidenced above.
