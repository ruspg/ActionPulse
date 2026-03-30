"""
Test idempotency helpers for the T-48h rebuild window.
"""

import os
from datetime import datetime, timezone

import pytest

from digest_core.run import _artifact_age_hours, _should_skip_existing_artifacts


@pytest.fixture
def temp_output_dir(tmp_path):
    """Temporary output directory for testing."""
    out_dir = tmp_path / "out"
    out_dir.mkdir(parents=True, exist_ok=True)
    return out_dir


def test_idempotency_within_48h(temp_output_dir):
    """Recent JSON+MD artifacts should trigger a skip."""
    json_path = temp_output_dir / "digest-2024-01-15.json"
    md_path = temp_output_dir / "digest-2024-01-15.md"

    json_path.touch()
    md_path.touch()

    assert _should_skip_existing_artifacts(json_path, md_path) is True


def test_idempotency_outside_48h(temp_output_dir):
    """Old artifacts should not block a rebuild."""
    json_path = temp_output_dir / "digest-2024-01-15.json"
    md_path = temp_output_dir / "digest-2024-01-15.md"

    json_path.touch()
    md_path.touch()

    old_time = datetime.now(timezone.utc).timestamp() - (50 * 3600)
    os.utime(json_path, (old_time, old_time))
    os.utime(md_path, (old_time, old_time))

    assert _artifact_age_hours(json_path) >= 49
    assert _should_skip_existing_artifacts(json_path, md_path) is False


def test_idempotency_missing_artifacts(temp_output_dir):
    """Missing artifacts should not trigger a skip."""
    json_path = temp_output_dir / "digest-2024-01-15.json"
    md_path = temp_output_dir / "digest-2024-01-15.md"

    assert _should_skip_existing_artifacts(json_path, md_path) is False


def test_idempotency_partial_artifacts(temp_output_dir):
    """Partial artifacts should not trigger a skip."""
    json_path = temp_output_dir / "digest-2024-01-15.json"
    md_path = temp_output_dir / "digest-2024-01-15.md"

    json_path.touch()

    assert _should_skip_existing_artifacts(json_path, md_path) is False
