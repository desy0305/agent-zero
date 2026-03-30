### swarm_analytics

Query swarm mission history and performance trends.

**Parameters**
- `query` optional: `stats`, `insights`, or `leaderboard`
- `days` optional: number of days to inspect

**Use when**
- You want to review swarm performance over time
- You want a recommendation for future swarm size or strategy
- You want to see which agent profiles perform best

**Example**
~~~json
{
  "tool_name": "swarm_analytics",
  "tool_args": {
    "query": "stats",
    "days": 30
  }
}
~~~
