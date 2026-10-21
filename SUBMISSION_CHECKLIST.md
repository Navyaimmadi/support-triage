# Submission status

The offline implementation is verified. This project is **not yet submission-ready** because a real Responses API workflow, live trace evidence, screenshots, and a public repository URL are missing.

| Requirement | Current evidence | Status |
|---|---|---|
| Router, Billing, Technical, Account | `triage.py`, offline route tests | Implemented; live routes unverified |
| Actual SDK handoffs | SDK handoff spans in `outputs/offline/traces.jsonl` | Offline verified; live unverified |
| Input, output, tool guardrails | Offline tests and three blocked demo scenarios | Offline verified; live demonstration pending |
| Persistent state and contextual follow-up | SQLite reopen/isolation tests; invoice amount follow-up | Offline verified; live follow-up pending |
| Real Responses API workflow | SDK adapter code only | **Required; not verified** |
| Routing, handoff, tool, guardrail, final traces | Local SDK JSONL, trace IDs, trace viewer | Offline verified; live capture pending |
| Source, architecture, design, samples | Repository files and offline samples | Prepared |
| Genuine live screenshots | None | Pending live run |
| Public GitHub repository | No repository or remote exists in this folder | Pending publication approval |

Before submission, complete the authorized live plan in [reports/live-verification.md](reports/live-verification.md), review and publish sanitized evidence, capture genuine screenshots from the local trace viewer, verify a real Responses workflow, and publish a reviewed public GitHub repository. Chat Completions and the offline fixture do not meet the Responses requirement.
