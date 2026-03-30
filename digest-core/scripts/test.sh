#!/bin/bash
# Contract test runner aligned to docs/ARCHITECTURE.md
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"

echo "Running tests with pytest..."

cd "$PROJECT_ROOT"

if [[ -x "$PROJECT_ROOT/.venv/bin/pytest" ]]; then
    PYTEST_BIN="$PROJECT_ROOT/.venv/bin/pytest"
elif command -v pytest >/dev/null 2>&1; then
    PYTEST_BIN="$(command -v pytest)"
else
    echo "Error: pytest not found. Install dependencies first (for example: uv sync)"
    exit 1
fi

CONTRACT_TESTS=(
    tests/test_config.py
    tests/test_evidence_split.py
    tests/test_empty_day.py
    tests/test_normalize.py
    tests/test_quote_preservation.py
    tests/test_regex_fallback.py
    tests/test_regex_cyr.py
    tests/test_ru_detectors.py
    tests/test_nlp_lemmatization.py
    tests/test_normalized_message_sender.py
    tests/test_sender_fix_integration.py
    tests/test_actions_sender_integration.py
    tests/test_tz_utils.py
    tests/test_llm_contract.py
    tests/test_llm_strict_validation.py
    tests/test_gateway_tokens_init.py
    tests/test_fallback_degrade.py
    tests/contract
)

if "$PYTEST_BIN" --help 2>/dev/null | grep -q -- '--cov'; then
    echo "Running contract tests with coverage..."
    "$PYTEST_BIN" "${CONTRACT_TESTS[@]}" -v --cov=src/digest_core --cov-report=term-missing --cov-report=html
else
    echo "Running contract tests..."
    "$PYTEST_BIN" "${CONTRACT_TESTS[@]}" -v
fi

echo "All contract tests passed!"
