from unittest.mock import patch

from typer.testing import CliRunner

from digest_core.cli import app


runner = CliRunner()


def test_run_dispatches_dry_run():
    with patch("digest_core.cli.setup_logging"), patch(
        "digest_core.cli.run_digest_dry_run"
    ) as mock_run:
        result = runner.invoke(app, ["run", "--dry-run"])

    assert result.exit_code == 2
    assert "Dry-run mode" in result.output
    mock_run.assert_called_once()


def test_run_dispatches_full_pipeline():
    with patch("digest_core.cli.setup_logging"), patch(
        "digest_core.cli.run_digest"
    ) as mock_run:
        mock_run.return_value = True
        result = runner.invoke(app, ["run"])

    assert result.exit_code == 0
    mock_run.assert_called_once()


def test_run_reports_pipeline_error():
    with patch("digest_core.cli.setup_logging"), patch(
        "digest_core.cli.run_digest"
    ) as mock_run:
        mock_run.side_effect = RuntimeError("boom")
        result = runner.invoke(app, ["run"])

    assert result.exit_code == 1
    assert "boom" in result.output
