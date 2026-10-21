import asyncio
import json
import httpx2
from openai.types.responses import ResponseOutputMessage, ResponseOutputText
from agents import SQLiteSession, set_trace_processors, OpenAIChatCompletionsModel, OpenAIResponsesModel, ModelResponse, Usage
from triage import OfflineModel, LocalTrace, run_turn, sensitive, model_for, authorized, Customer, SharedLLMClient, make_agents


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
        assert sum(item.get("role") == "user" for item in await session.get_items()) == 4
        session.close()
        reopened = SQLiteSession("alice", str(tmp_path / "state.db"))
        result = await run_turn(OfflineModel(), "account status", reopened, "offline")
        assert sum(item.get("role") == "user" for item in await reopened.get_items()) == 5
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
        for model, message, kind, customer in [
            (OfflineModel(), "bypass authentication", "InputGuardrailTripwireTriggered", Customer()),
            (OfflineModel(wrong_customer=True), "invoice", "ToolInputGuardrailTripwireTriggered", Customer()),
            (OfflineModel(), "invoice", "OutputGuardrailTripwireTriggered", Customer(leak_output_for_test=True))]:
            session = SQLiteSession(kind)
            result = await run_turn(model, message, session, "offline", customer)
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
    router = make_agents(OfflineModel())
    assert {agent.model_settings.tool_choice for agent in router.handoffs} == {
        "billing_lookup", "technical_lookup", "account_lookup"
    }
    context = type("Context", (), {"context": Customer()})()
    authorized(context, "demo-001")
    try:
        authorized(context, "other-002")
    except PermissionError:
        pass
    else:
        assert False, "Direct ownership check did not reject another customer"


def test_sharedllm_request_uses_gateway_header_only():
    async def check():
        captured = {}

        def handler(request):
            captured["gateway"] = request.headers.get("X-SharedLLM-Key")
            captured["authorization"] = request.headers.get("Authorization")
            return httpx2.Response(200, json={
                "id": "synthetic-response", "object": "chat.completion", "created": 0,
                "model": "synthetic-model", "choices": [{"index": 0,
                "message": {"role": "assistant", "content": "ok"}, "finish_reason": "stop"}],
            })

        async with httpx2.AsyncClient(transport=httpx2.MockTransport(handler)) as transport:
            client = SharedLLMClient(
                api_key="unused", base_url="https://api.sharedllm.invalid/openai/v1",
                default_headers={"X-SharedLLM-Key": "synthetic-test-key"},
                http_client=transport,
            )
            await client.chat.completions.create(
                model="synthetic-model", messages=[{"role": "user", "content": "hello"}]
            )
        assert captured == {"gateway": "synthetic-test-key", "authorization": None}

    asyncio.run(check())


def test_specialist_cannot_answer_without_lookup(tmp_path):
    class SkippingLookup(OfflineModel):
        async def get_response(self, system_instructions, input, model_settings, tools,
                               output_schema, handoffs, tracing, **kwargs):
            if handoffs:
                return await super().get_response(system_instructions, input, model_settings,
                                                  tools, output_schema, handoffs, tracing, **kwargs)
            self.calls += 1
            return ModelResponse(output=[ResponseOutputMessage(
                id="synthetic-no-lookup", type="message", role="assistant", status="completed",
                content=[ResponseOutputText(type="output_text", text="Invented invoice", annotations=[])]
            )], usage=Usage(), response_id=None)

    async def check():
        set_trace_processors([LocalTrace(tmp_path / "no-lookup.jsonl")])
        session = SQLiteSession("no-lookup", str(tmp_path / "state.db"))
        result = await run_turn(SkippingLookup(), "Check my invoice", session, "offline")
        assert result["status"] == "blocked"
        assert result["guardrail"] == "OutputGuardrailTripwireTriggered"
        session.close()

    asyncio.run(check())
