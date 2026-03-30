"""
Swarm analytics tool - query swarm mission history and insights.
"""

from python.helpers.swarm_analytics import get_analytics
from python.helpers.tool import Response, Tool


class SwarmAnalyticsTool(Tool):
    """Expose swarm analytics to the agent."""

    async def execute(self, query: str = "stats", days: int = 30, **kwargs):
        analytics = get_analytics()

        if query == "stats":
            stats = analytics.get_stats(days)
            if "message" in stats:
                return Response(
                    message=f"# Swarm Analytics\n\n{stats['message']}",
                    break_loop=False,
                )

            lines = [
                f"# Swarm Analytics (Last {stats['period_days']} Days)",
                "",
                f"**Total Missions:** {stats['total_missions']}",
                f"**Agents Deployed:** {stats['total_agents_deployed']}",
                f"**Overall Success Rate:** {stats['success_rate'] * 100:.1f}%",
                f"**Avg Mission Duration:** {stats['avg_mission_duration_seconds']:.1f}s",
                f"**Avg Effectiveness Score:** {stats['avg_effectiveness_score']:.1f}/100",
                "",
                "## Strategy Performance",
                "",
            ]

            for strat, data in stats.get("strategy_performance", {}).items():
                lines.append(
                    f"- **{strat}**: {data['count']} missions, "
                    f"{data['avg_effectiveness']:.1f} avg effectiveness"
                )

            lines.extend(["", "## Category Performance", ""])

            for cat, data in stats.get("category_performance", {}).items():
                lines.append(
                    f"- **{cat}**: {data['count']} missions, "
                    f"avg size {data['avg_swarm_size']:.1f} agents"
                )

            return Response(message="\n".join(lines), break_loop=False)

        if query == "insights":
            insights = analytics.generate_insights()
            lines = [
                "# Swarm Insights",
                "",
                "Based on mission history analysis:",
                "",
            ]
            for insight in insights:
                lines.append(f"- {insight}")
            return Response(message="\n".join(lines), break_loop=False)

        if query == "leaderboard":
            leaderboard = analytics.get_leaderboard()
            lines = [
                "# Agent Profile Leaderboard",
                "",
            ]
            for i, performer in enumerate(leaderboard.get("top_performers", []), 1):
                lines.append(
                    f"{i}. **{performer['profile']}** - {performer['success_rate']}% success "
                    f"({performer['missions']} missions)"
                )
            return Response(message="\n".join(lines), break_loop=False)

        return Response(
            message=(
                "# Swarm Analytics\n\n"
                "Available queries:\n"
                "- `stats` - Mission statistics\n"
                "- `insights` - Performance insights\n"
                "- `leaderboard` - Top performing profiles"
            ),
            break_loop=False,
        )
