from typing import Any, TYPE_CHECKING

from python.helpers import projects, subagents
from python.helpers.files import VariablesPlugin

if TYPE_CHECKING:
    from agent import Agent


class ParallelSubordinates(VariablesPlugin):
    """Provide agent_profiles for the parallel subordinate prompt."""

    def get_variables(
        self, file: str, backup_dirs: list[str] | None = None, **kwargs
    ) -> dict[str, Any]:
        agent: Agent | None = kwargs.get("_agent", None)
        project = projects.get_context_project_name(agent.context) if agent else None
        agents = subagents.get_available_agents_dict(project)

        if not agents:
            return {"agent_profiles": None}

        profiles: dict[str, dict[str, str]] = {}
        for name, subagent in agents.items():
            profiles[name] = {
                "title": subagent.title,
                "description": subagent.description,
                "context": subagent.context,
            }
        return {"agent_profiles": profiles}
