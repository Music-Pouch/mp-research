from mp_research.adapters.gpt_researcher import GPTResearcherAdapter


def test_collect_model_configuration_captures_free_game_settings(monkeypatch):
    monkeypatch.setenv("RETRIEVER", "duckduckgo")
    monkeypatch.setenv("OPENAI_API_KEY", "ollama")
    monkeypatch.setenv("OPENAI_API_BASE", "http://127.0.0.1:11434/v1")
    monkeypatch.setenv("OLLAMA_BASE_URL", "http://127.0.0.1:11434")
    monkeypatch.setenv("FAST_LLM", "ollama:qwen3:4b")
    monkeypatch.setenv("SMART_LLM", "ollama:qwen3:4b")
    monkeypatch.setenv("STRATEGIC_LLM", "ollama:qwen3:4b")
    monkeypatch.setenv("EMBEDDING", "ollama:nomic-embed-text")

    configuration = GPTResearcherAdapter._collect_model_configuration()

    assert configuration["retriever"] == "duckduckgo"
    assert configuration["fast_llm"] == "ollama:qwen3:4b"
    assert configuration["embedding"] == "ollama:nomic-embed-text"
    assert configuration["credential_mode"] == "local-openai-compatible"


def test_collect_model_configuration_does_not_expose_secret_values(monkeypatch):
    monkeypatch.setenv("OPENAI_API_KEY", "super-secret")
    monkeypatch.setenv("TAVILY_API_KEY", "tvly-secret")

    configuration = GPTResearcherAdapter._collect_model_configuration()

    assert configuration["credential_mode"] == "api-key"
    assert configuration["retriever_credential"] == "configured"
    assert "openai_api_key" not in configuration
    assert "tavily_api_key" not in configuration
