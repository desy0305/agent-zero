from __future__ import annotations

from copy import deepcopy
from dataclasses import fields
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from agent import AgentConfig


def clone_agent_config(config: "AgentConfig") -> "AgentConfig":
    """Return a deep copy of an agent config so mutable state is never shared."""

    return deepcopy(config)


def merge_agent_config(
    current_config: "AgentConfig",
    baseline_config: "AgentConfig",
    override_config: "AgentConfig",
) -> "AgentConfig":
    """
    Merge only the fields that changed relative to the baseline config.

    This keeps any parent-agent customizations that were already present on
    ``current_config`` while still applying the requested profile overrides.
    """

    merged = deepcopy(current_config)
    for field_info in fields(current_config):
        field_name = field_info.name
        if getattr(override_config, field_name) != getattr(baseline_config, field_name):
            setattr(merged, field_name, deepcopy(getattr(override_config, field_name)))
    return merged
