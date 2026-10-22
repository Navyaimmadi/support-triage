# Submission

Multi-Agent Customer Support Triage demonstrates OpenAI Agents SDK handoffs among a Router and three support specialists, input/output/tool guardrails, synthetic read-only lookups, SQLite conversation history, and local SDK traces. The offline fixture and its evidence are labeled as simulation.

Public repository: [github.com/Navyaimmadi/support-triage](https://github.com/Navyaimmadi/support-triage).

One real SharedLLM Responses API Router clarification is verified with a matching local SDK trace and genuine screenshot. Billing, Technical, and Account each have a successful live handoff, lookup, and grounded response, with matching traces and genuine screenshots. A follow-up in the persistent Billing session returned the earlier lookup result without restating the invoice; its own turn required no additional lookup. See [submission status](SUBMISSION_CHECKLIST.md) and [live verification](reports/live-verification.md).
