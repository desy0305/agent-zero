from agent import AgentConfig
from models import ModelConfig, ModelType

from python.helpers.agent_config import clone_agent_config, merge_agent_config


def _make_config() -> AgentConfig:
    chat = ModelConfig(
        type=ModelType.CHAT,
        provider="provider-a",
        name="model-a",
        api_base="http://example.invalid",
        ctx_length=4096,
        kwargs={"nested": {"value": 1}},
    )
    utility = ModelConfig(
        type=ModelType.CHAT,
        provider="provider-b",
        name="model-b",
    )
    embedding = ModelConfig(
        type=ModelType.EMBEDDING,
        provider="provider-c",
        name="model-c",
    )
    browser = ModelConfig(
        type=ModelType.CHAT,
        provider="provider-d",
        name="model-d",
    )

    return AgentConfig(
        chat_model=chat,
        utility_model=utility,
        embeddings_model=embedding,
        browser_model=browser,
        mcp_servers='[{"name":"demo"}]',
        profile="base",
        memory_subdir="memory-base",
        knowledge_subdirs=["default", "custom"],
        browser_http_headers={"X-Test": "one"},
        additional={"flags": {"keep": True}},
    )


def test_clone_agent_config_deep_copies_nested_state():
    original = _make_config()
    cloned = clone_agent_config(original)

    cloned.browser_http_headers["X-Test"] = "two"
    cloned.chat_model.kwargs["nested"]["value"] = 2
    cloned.additional["flags"]["keep"] = False

    assert original.browser_http_headers["X-Test"] == "one"
    assert original.chat_model.kwargs["nested"]["value"] == 1
    assert original.additional["flags"]["keep"] is True


def test_merge_agent_config_preserves_parent_customizations():
    current = _make_config()
    current.browser_http_headers["X-Parent"] = "keep"
    current.additional["parent"] = "yes"

    baseline = _make_config()
    override = clone_agent_config(baseline)
    override.profile = "child"
    override.memory_subdir = "memory-child"
    override.browser_http_headers = {"X-Override": "applied"}
    override.chat_model.ctx_length = 8192

    merged = merge_agent_config(current, baseline, override)

    assert merged.profile == "child"
    assert merged.memory_subdir == "memory-child"
    assert merged.browser_http_headers == {"X-Override": "applied"}
    assert merged.chat_model.ctx_length == 8192
    assert merged.additional["parent"] == "yes"
    assert merged.browser_http_headers is not current.browser_http_headers
