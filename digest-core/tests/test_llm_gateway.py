"""
Test LLM gateway against the current retry and response contract.
"""

from unittest.mock import Mock

import pytest

from digest_core.config import LLMConfig
from digest_core.evidence.split import EvidenceChunk
from digest_core.llm.gateway import LLMGateway


def _mock_response(content: str, *, status_code: int = 200, prompt_tokens: int = 100,
                   completion_tokens: int = 50, headers: dict | None = None) -> Mock:
    response = Mock()
    response.status_code = status_code
    response.headers = headers or {}
    response.raise_for_status = Mock()
    response.json.return_value = {
        "choices": [{"message": {"content": content}}],
        "usage": {
            "prompt_tokens": prompt_tokens,
            "completion_tokens": completion_tokens,
        },
    }
    return response


@pytest.fixture
def gateway(monkeypatch):
    """LLM gateway with a current LLMConfig fixture."""
    monkeypatch.setenv("LLM_TOKEN", "test-token")
    config = LLMConfig(
        endpoint="https://api.openai.com/v1/chat/completions",
        model="qwen3.5-397b",
        timeout_s=30,
    )
    return LLMGateway(config)


def test_invalid_json_retry(gateway):
    """Invalid JSON should trigger one retry and then return parsed sections."""
    invalid_response = _mock_response("{invalid json")
    valid_response = _mock_response('{"sections": [{"title": "Test", "items": []}]}')
    gateway.client.post = Mock(side_effect=[invalid_response, valid_response])

    result = gateway.extract_actions([], "Return strict JSON", "test-trace-id")

    assert result["sections"] == [{"title": "Test", "items": []}]
    assert result["_meta"]["retry_count"] == 1
    assert gateway.client.post.call_count == 2


def test_quality_retry_empty_sections(gateway):
    """Empty sections with positive evidence should trigger one quality retry."""
    empty_response = _mock_response('{"sections": []}')
    content_response = _mock_response('{"sections": [{"title": "Test", "items": []}]}')
    gateway.client.post = Mock(side_effect=[empty_response, content_response])

    evidence = [EvidenceChunk(evidence_id="ev-1", content="Important action item", priority_score=2.0)]
    result = gateway.extract_actions(evidence, "Return strict JSON", "test-trace-id")

    assert result["sections"] == [{"title": "Test", "items": []}]
    assert gateway.client.post.call_count == 2


def test_token_usage_extraction(gateway):
    """Usage metadata should be exposed via the _meta envelope."""
    gateway.client.post = Mock(
        return_value=_mock_response('{"sections": [{"title": "Test", "items": []}]}')
    )

    result = gateway.extract_actions([], "Return strict JSON", "test-trace-id")

    assert result["_meta"]["tokens_in"] == 100
    assert result["_meta"]["tokens_out"] == 50
    assert result["_meta"]["http_status"] == 200


def test_network_error_propagation(gateway):
    """Unexpected transport errors should propagate to the caller."""
    gateway.client.post = Mock(side_effect=Exception("Network error"))

    with pytest.raises(Exception, match="Network error"):
        gateway.extract_actions([], "Return strict JSON", "test-trace-id")


def test_evidence_formatting(gateway):
    """Formatted request payload should include both system and user messages."""
    gateway.client.post = Mock(
        return_value=_mock_response('{"sections": []}')
    )
    evidence = [
        EvidenceChunk(
            evidence_id="ev-1",
            content="First evidence chunk",
            message_metadata={"from": "sender@example.com", "subject": "Subject"},
            source_ref={"msg_id": "msg-1"},
            msg_id="msg-1",
        ),
        EvidenceChunk(
            evidence_id="ev-2",
            content="Second evidence chunk",
            message_metadata={"from": "sender@example.com", "subject": "Subject"},
            source_ref={"msg_id": "msg-2"},
            msg_id="msg-2",
        ),
    ]

    gateway.extract_actions(evidence, "Return strict JSON", "test-trace-id")

    call_args = gateway.client.post.call_args
    messages = call_args.kwargs["json"]["messages"]
    assert len(messages) == 2
    assert messages[0]["role"] == "system"
    assert messages[1]["role"] == "user"
