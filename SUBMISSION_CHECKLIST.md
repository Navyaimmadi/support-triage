# Submission status

The offline implementation is verified. A real SharedLLM-mode input guardrail block is captured. Authentication now works, and a Router-to-Billing handoff and `billing_lookup` occurred in one live run, but the model added unsupported invoice facts; later no-lookup answers were blocked. This project is **not yet submission-ready** because accepted live specialist results, a real Responses API workflow, screenshots, and a public repository URL are missing.

| Requirement | Current evidence | Status |
|---|---|---|
| Router, Billing, Technical, Account | `triage.py`, offline route tests | Implemented; live routes unverified |
| Actual SDK handoffs | Offline SDK spans; live Router-to-Billing span recorded in ignored runtime trace | Offline verified; live handoff observed, accepted live sample pending |
| Input, output, tool guardrails | Offline tests and three blocked demo scenarios; real SharedLLM-mode input block trace | Offline verified; live input block captured |
| Persistent state and contextual follow-up | SQLite reopen/isolation tests; invoice amount follow-up | Offline verified; live follow-up pending |
| Real Responses API workflow | SDK adapter code only | **Required; not verified** |
| Routing, handoff, tool, guardrail, final traces | Local SDK JSONL and trace IDs; live input block and rejected Billing attempts | Offline verified; accepted full live trace pending |
| Source, architecture, design, samples | Repository files and offline samples | Prepared |
| Genuine live screenshots | None | Pending live run |
| Public GitHub repository | No repository or remote exists in this folder | Pending publication approval |

Before submission, complete the authorized live plan in [reports/live-verification.md](reports/live-verification.md), review and publish sanitized evidence, capture genuine screenshots from the local trace viewer, verify a real Responses workflow, and publish a reviewed public GitHub repository. Chat Completions and the offline fixture do not meet the Responses requirement.
