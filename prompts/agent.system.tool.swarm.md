### swarm

Use this tool when one task should be split across multiple agents and run in parallel.

**Parameters**
- `mission` required: the overall task to accomplish
- `swarm_size` optional: number of agents, between 2 and 12, or `auto`
- `strategy` optional: `auto`, `divide`, `research`, `review`, or `implement`

**When to use**
- Security audits
- Multi-angle research
- Multi-module implementation
- Large code reviews

**Example**
~~~json
{
  "tool_name": "swarm",
  "tool_args": {
    "mission": "Review the authentication system for security issues",
    "swarm_size": 5,
    "strategy": "review"
  }
}
~~~

**Notes**
- Start with `auto` if you are unsure how many agents are needed
- Each worker should focus on its own slice of the mission
