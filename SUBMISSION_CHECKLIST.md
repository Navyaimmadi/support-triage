# Submission status

The offline implementation is verified. A real SharedLLM-mode input guardrail block and a successful Responses API Router clarification are captured with genuine local trace screenshots. `gpt-oss:120b` made a Router-to-Billing handoff and `billing_lookup` in one live run, but added unsupported invoice facts; later no-lookup answers were blocked. Approved `glm-5.3-flash`, `kimi-k2.6`, and `kimi-k2.7-code` checks failed authentication. This project is **not yet submission-ready** because accepted live specialist results and their screenshots are missing.

| Requirement | Current evidence | Status |
|---|---|---|
| Router, Billing, Technical, Account | `triage.py`, offline route tests | Implemented; live routes unverified |
| Actual SDK handoffs | Offline SDK spans; live Router-to-Billing span recorded in ignored runtime trace | Offline verified; live handoff observed, accepted live sample pending |
| Input, output, tool guardrails | Offline tests and three blocked demo scenarios; real SharedLLM-mode input block trace | Offline verified; live input block captured |
| Persistent state and contextual follow-up | SQLite reopen/isolation tests; invoice amount follow-up | Offline verified; live follow-up pending |
| Real Responses API workflow | Successful SharedLLM Router clarification; `outputs/live/responses-success-trace.jsonl` and screenshot | Verified for Router clarification; specialist Responses turn blocked on missing lookup |
| Routing, handoff, tool, guardrail, final traces | Local SDK JSONL and trace IDs; live input block and rejected Billing attempts | Offline verified; accepted full live trace pending |
| Source, architecture, design, samples | Repository files and offline samples | Prepared |
| Genuine live screenshots | `screenshots/responses-router.png`, `screenshots/input-guardrail.png` from local SDK trace viewer | Partial; specialist handoff/tool/final screenshots pending |
| Public GitHub repository | [github.com/Navyaimmadi/support-triage](https://github.com/Navyaimmadi/support-triage), branch `main` | Published; local branch tracks `origin/main` |

Before submission, complete the specialist live plan in [reports/live-verification.md](reports/live-verification.md) and publish sanitized specialist evidence and screenshots to the repository. Chat Completions and the offline fixture do not meet the Responses requirement; the successful Router clarification uses the real Responses API.
