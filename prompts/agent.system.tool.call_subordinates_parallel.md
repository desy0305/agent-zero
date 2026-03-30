{{if agent_profiles}}
### call_subordinates_parallel

Use this tool to run multiple independent subtasks at the same time.

**Use when**
- The subtasks do not depend on each other
- You want to inspect several files, tests, or findings in parallel
- You want faster turnaround than sequential delegation

**Parameters**
- `tasks` required: array of task objects
  - `profile`: optional agent profile name
  - `message`: task instructions for the subordinate
- `max_parallel` optional: maximum concurrent subordinates

**Example**
~~~json
{
  "tool_name": "call_subordinates_parallel",
  "tool_args": {
    "tasks": [
      {"profile": "security", "message": "Review auth flow for bypasses"},
      {"profile": "engineer", "message": "Check database layer for bottlenecks"}
    ],
    "max_parallel": 2
  }
}
~~~

**Response handling**
- Results are returned together with one section per subordinate
- Use `§§include(<path>)` if a response is too long to quote again

**Available profiles**
{{agent_profiles}}
{{endif}}
