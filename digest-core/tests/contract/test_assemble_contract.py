import json
from pathlib import Path

from digest_core.assemble.jsonout import JSONAssembler
from digest_core.assemble.markdown import MarkdownAssembler
from digest_core.llm.schemas import Digest, Item, Section


def _sample_digest() -> Digest:
    return Digest(
        prompt_version="extract_actions.v1",
        digest_date="2024-01-15",
        trace_id="trace-123",
        sections=[
            Section(
                title="Мои действия",
                items=[
                    Item(
                        title="Подготовить отчёт",
                        due="2024-01-16",
                        evidence_id="ev-1",
                        confidence=0.8,
                        source_ref={"type": "email", "msg_id": "msg-1"},
                    )
                ],
            )
        ],
    )


def test_json_assembler_writes_schema_shape(tmp_path: Path):
    assembler = JSONAssembler()
    output_path = tmp_path / "digest.json"

    assembler.write_digest(_sample_digest(), output_path)

    payload = json.loads(output_path.read_text(encoding="utf-8"))
    assert payload["schema_version"] == "1.0"
    assert payload["digest_date"] == "2024-01-15"
    assert payload["sections"][0]["items"][0]["evidence_id"] == "ev-1"


def test_markdown_assembler_writes_digest_header(tmp_path: Path):
    assembler = MarkdownAssembler()
    output_path = tmp_path / "digest.md"

    assembler.write_digest(_sample_digest(), output_path)

    content = output_path.read_text(encoding="utf-8")
    assert "# Дайджест действий - 2024-01-15" in content
    assert "Подготовить отчёт" in content
    assert "evidence ev-1" in content
