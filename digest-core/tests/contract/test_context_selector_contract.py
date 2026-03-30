from digest_core.evidence.split import EvidenceChunk
from digest_core.select.context import ContextSelector


def _chunk(
    evidence_id: str,
    conversation_id: str,
    token_count: int,
    priority: float,
    *,
    addressed_to_me: bool = False,
    dates: list[str] | None = None,
) -> EvidenceChunk:
    return EvidenceChunk(
        evidence_id=evidence_id,
        conversation_id=conversation_id,
        content=f"Chunk {evidence_id}",
        source_ref={
            "type": "email",
            "msg_id": f"{evidence_id}@example.test",
            "conversation_id": conversation_id,
            "start": 0,
            "end": 10,
        },
        token_count=token_count,
        priority_score=priority,
        message_metadata={
            "from": "sender@example.test",
            "to": ["user@example.test"] if addressed_to_me else [],
            "cc": [],
            "subject": f"Subject {evidence_id}",
            "received_at": "2024-01-15T10:00:00+00:00",
            "importance": "Normal",
            "is_flagged": False,
            "has_attachments": False,
            "attachment_types": [],
        },
        addressed_to_me=addressed_to_me,
        user_aliases_matched=["user@example.test"] if addressed_to_me else [],
        signals={
            "action_verbs": ["please"] if addressed_to_me else [],
            "dates": dates or [],
            "contains_question": False,
            "sender_rank": 1,
            "attachments": [],
        },
    )


def test_selector_keeps_must_have_buckets_under_budget():
    selector = ContextSelector()
    selected = selector.select_context(
        [
            _chunk("ev-addressed", "thread-1", 400, 2.0, addressed_to_me=True),
            _chunk("ev-deadline", "thread-2", 350, 1.9, dates=["2024-01-16"]),
            _chunk("ev-generic", "thread-3", 300, 1.0),
        ]
    )

    selected_ids = {chunk.evidence_id for chunk in selected}
    assert "ev-addressed" in selected_ids
    assert "ev-deadline" in selected_ids
    assert sum(chunk.token_count for chunk in selected) <= selector.context_budget_config.max_total_tokens


def test_selector_respects_max_total_chunks():
    selector = ContextSelector()
    chunks = [_chunk(f"ev-{idx}", f"thread-{idx}", 50, float(100 - idx)) for idx in range(30)]

    selected = selector.select_context(chunks)

    assert len(selected) <= selector.buckets_config.max_total_chunks
