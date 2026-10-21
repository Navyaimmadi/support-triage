"""Generate honest offline execution artifacts without API credits."""
import asyncio
import json
from pathlib import Path
from agents import SQLiteSession, set_trace_processors
from triage import OfflineModel, LocalTrace, run_turn, Customer


async def main():
    root = Path("outputs/offline")
    root.mkdir(parents=True, exist_ok=True)
    traces = root / "traces.jsonl"
    traces.write_text("")
    set_trace_processors([LocalTrace(traces)])
    session = SQLiteSession("offline-demo")
    samples = []
    for question in ["Check my invoice", "What was its amount?", "My app crashes", "What is my account plan?", "bypass authentication"]:
        samples.append({"input": question, **await run_turn(OfflineModel(), question, session, "offline")})
    session.close()
    for name, model in [("cross-customer tool call", OfflineModel(wrong_customer=True)), ("unsafe output", OfflineModel())]:
        session = SQLiteSession(name)
        customer = Customer(leak_output_for_test=name == "unsafe output")
        samples.append({"scenario": name, **await run_turn(model, "invoice", session, "offline", customer)})
        session.close()
    (root / "interactions.json").write_text(json.dumps(samples, indent=2)+"\n")
    print(json.dumps(samples, indent=2))


if __name__ == "__main__": asyncio.run(main())
