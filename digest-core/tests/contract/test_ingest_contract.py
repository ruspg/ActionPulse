from datetime import datetime, timezone
from pathlib import Path
from types import SimpleNamespace

import pytest

from digest_core.config import EWSConfig, TimeConfig
from digest_core.ingest.ews import EWSIngest


def _make_ingest(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> EWSIngest:
    monkeypatch.setenv("EWS_PASSWORD", "secret")
    config = EWSConfig(
        endpoint="https://ews.example.test/EWS/Exchange.asmx",
        user_upn="user@example.test",
        user_login="user",
        user_domain="example",
        sync_state_path=str(tmp_path / "ews.syncstate"),
    )
    time_config = TimeConfig(user_timezone="UTC", mailbox_tz="UTC", window="calendar_day")
    return EWSIngest(config, time_config=time_config)


def test_calendar_day_window_uses_digest_date(tmp_path, monkeypatch):
    ingest = _make_ingest(tmp_path, monkeypatch)

    start_utc, end_utc = ingest._get_time_window("2024-01-15", ingest.time_config)

    assert start_utc == datetime(2024, 1, 15, 0, 0, tzinfo=timezone.utc)
    assert end_utc == datetime(2024, 1, 15, 23, 59, 59, tzinfo=timezone.utc)


def test_sync_state_round_trip(tmp_path, monkeypatch):
    ingest = _make_ingest(tmp_path, monkeypatch)
    timestamp = datetime(2024, 1, 15, 10, 30, tzinfo=timezone.utc)

    ingest._update_sync_state(timestamp)

    assert ingest._load_sync_state() == timestamp.isoformat()


def test_normalize_message_preserves_canonical_fields(tmp_path, monkeypatch):
    ingest = _make_ingest(tmp_path, monkeypatch)
    message = SimpleNamespace(
        internet_message_id="<Message-001@example.test>",
        id="ews-id-1",
        conversation_id="conv-123",
        datetime_received=datetime(2024, 1, 15, 10, 30, tzinfo=timezone.utc),
        sender=SimpleNamespace(email_address="Sender@Example.test", name="Sender Name"),
        subject="Status update",
        text_body="<p>Hello</p>",
        to_recipients=[SimpleNamespace(email_address="to@example.test")],
        cc_recipients=[SimpleNamespace(email_address="cc@example.test")],
        importance="High",
        is_flagged=True,
        has_attachments=True,
        attachments=[SimpleNamespace(name="report.pdf")],
    )

    normalized = ingest._normalize_message(message)

    assert normalized.msg_id == "message-001@example.test"
    assert normalized.conversation_id == "conv-123"
    assert normalized.sender_email == "sender@example.test"
    assert normalized.from_email == "sender@example.test"
    assert normalized.from_name == "Sender Name"
    assert normalized.subject == "Status update"
    assert normalized.to_recipients == ["to@example.test"]
    assert normalized.cc_recipients == ["cc@example.test"]
    assert normalized.attachment_types == ["pdf"]
