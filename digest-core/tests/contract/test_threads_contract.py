from datetime import datetime, timedelta, timezone

from digest_core.ingest.ews import NormalizedMessage
from digest_core.threads.build import ThreadBuilder


def _message(msg_id: str, conversation_id: str, when: datetime, sender: str, subject: str) -> NormalizedMessage:
    return NormalizedMessage(
        msg_id=msg_id,
        conversation_id=conversation_id,
        datetime_received=when,
        sender_email=sender,
        subject=subject,
        text_body=f"Body for {msg_id}",
        to_recipients=["user@example.test"],
        cc_recipients=[],
        importance="Normal",
        is_flagged=False,
        has_attachments=False,
        attachment_types=[],
        from_email=sender,
        from_name=None,
        to_emails=["user@example.test"],
        cc_emails=[],
        message_id=msg_id,
        body_norm=f"Body for {msg_id}",
        received_at=when,
    )


def test_build_threads_groups_by_conversation_and_sorts_messages():
    base = datetime(2024, 1, 15, 10, 0, tzinfo=timezone.utc)
    builder = ThreadBuilder()
    messages = [
        _message("msg-2", "conv-1", base + timedelta(hours=1), "b@example.test", "Re: Budget"),
        _message("msg-1", "conv-1", base, "a@example.test", "Budget"),
        _message("msg-3", "conv-2", base + timedelta(hours=2), "c@example.test", "Launch"),
    ]

    threads = builder.build_threads(messages)

    assert len(threads) == 2
    first_thread = next(thread for thread in threads if thread.conversation_id == "conv_conv-1")
    assert [msg.msg_id for msg in first_thread.messages] == ["msg-1", "msg-2"]
    assert first_thread.latest_message_time == base + timedelta(hours=1)
    assert first_thread.participant_count == 3
