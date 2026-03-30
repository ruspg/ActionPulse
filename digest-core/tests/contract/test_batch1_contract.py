from pathlib import Path

from digest_core.config import LLMConfig
from digest_core.llm.prompt_registry import get_prompt_template_path, get_prompts_dir


def test_llm_timeout_default_is_120_seconds():
    assert LLMConfig().timeout_s == 120


def test_extract_actions_prompts_resolve_from_repo_root(monkeypatch):
    repo_root = Path(__file__).resolve().parents[3]
    monorepo_root = repo_root.parent
    monkeypatch.chdir(monorepo_root)

    prompts_dir = get_prompts_dir()

    ru_prompt = prompts_dir / get_prompt_template_path("extract_actions.v1")
    en_prompt = prompts_dir / get_prompt_template_path("extract_actions.en.v1")

    assert ru_prompt.exists()
    assert en_prompt.exists()
    assert ru_prompt.suffix == ".txt"
    assert en_prompt.suffix == ".txt"
