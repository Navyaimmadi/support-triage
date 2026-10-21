import asyncio
import json
from agents import SQLiteSession, set_trace_processors, OpenAIChatCompletionsModel, OpenAIResponsesModel
from triage import OfflineModel, LocalTrace, run_turn, sensitive, model_for, authorized, Customer


def test_routes_memory_and_spans(tmp_path):
    async def check():
        path = tmp_path / "trace.jsonl"
        set_trace_processors([LocalTrace(path)])
        session = SQLiteSession("alice", str(tmp_path / "state.db"))
        for text, agent in [("invoice please", "Billing"), ("What was its amount?", "Billing"), ("app crash", "Technical"), ("account plan", "Account")]:
            result = await run_turn(OfflineModel(), text, session, "offline")
            assert result["status"] == "ok"
            assert result["agent"] == agent
            assert result["trace_id"].startswith("trace_")
            if text == "What was its amount?":
                assert "USD 29" in result["answer"]
        assert "user turns seen: 4" in result["answer"]
        session.close()
        reopened = SQLiteSession("alice", str(tmp_path / "state.db"))
        result = await run_turn(OfflineModel(), "account status", reopened, "offline")
        assert "user turns seen: 5" in result["answer"]
        other = SQLiteSession("bob", str(tmp_path / "state.db"))
        assert await other.get_items() == []
        reopened.close()
        other.close()
        data = [json.loads(line) for line in path.read_text().splitlines()]
        types = {d["data"].get("span_data", {}).get("type") for d in data}
        assert {"handoff", "function", "agent", "guardrail", "custom"} <= types
        for trace_id in {d["data"]["id"] for d in data if d["event"] == "trace_start"}:
            spans = [d["data"]["span_data"] for d in data if d["event"] == "span_end" and d["data"]["trace_id"] == trace_id]
            assert any(s.get("type") == "handoff" for s in spans)
            assert any(s.get("type") == "function" for s in spans)
            assert any(s.get("name") == "validated_final_response" for s in spans)
    asyncio.run(check())


def test_guardrails(tmp_path):
    async def check():
        trace_path = tmp_path / "guardrails.jsonl"
        set_trace_processors([LocalTrace(trace_path)])
        for model, message, kind in [
            (OfflineModel(), "bypass authentication", "InputGuardrailTripwireTriggered"),
            (OfflineModel(wrong_customer=True), "invoice", "ToolInputGuardrailTripwireTriggered"),
            (OfflineModel(leak=True), "invoice", "OutputGuardrailTripwireTriggered")]:
            session = SQLiteSession(kind)
            result = await run_turn(model, message, session, "offline")
            assert result["status"] == "blocked"
            assert result["guardrail"] == kind
            assert result["trace_id"].startswith("trace_")
            if kind.startswith("Input"): assert model.calls == 0
            session.close()
        events = [json.loads(line) for line in trace_path.read_text().splitlines()]
        blocked = [event["data"]["span_data"] for event in events
                   if event["event"] == "span_end"
                   and event["data"]["span_data"].get("name") == "guardrail_block"]
        assert {span["data"]["kind"] for span in blocked} == {
            "InputGuardrailTripwireTriggered",
            "ToolInputGuardrailTripwireTriggered",
            "OutputGuardrailTripwireTriggered",
        }
    asyncio.run(check())


def test_sensitive_data():
    assert sensitive("4111 1111 1111 1111")
    assert sensitive("sk-DEMOSECRET12345")
    assert not sensitive("Invoice INV-101 is paid")


def test_provider_adapters_and_direct_ownership(monkeypatch):
    monkeypatch.setenv("SHAREDLLM_API_KEY", "synthetic-test-key")
    monkeypatch.setenv("SHAREDLLM_MODEL", "synthetic-test-model")
    monkeypatch.setenv("OPENAI_API_KEY", "synthetic-test-key")
    monkeypatch.setenv("OPENAI_MODEL", "synthetic-test-model")
    assert isinstance(model_for("sharedllm"), OpenAIChatCompletionsModel)
    assert isinstance(model_for("sharedllm-responses"), OpenAIResponsesModel)
    assert isinstance(model_for("openai-responses"), OpenAIResponsesModel)
    context = type("Context", (), {"context": Customer()})()
    authorized(context, "demo-001")
    try:
        authorized(context, "other-002")
    except PermissionError:
        pass
    else:
        assert False, "Direct ownership check did not reject another customer"
