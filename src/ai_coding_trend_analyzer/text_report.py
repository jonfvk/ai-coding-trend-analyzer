from typing import List, Dict, Any, Optional
from datetime import datetime

def summarize_trend_data(
    time_series: List[Dict[str, Any]],
    period_label: str = 'week',
    agent_key: str = 'agent',
    human_key: str = 'human',
    total_key: str = 'total',
    period_key: str = 'period',
) -> str:
    """
    Generates a plain text summary of AI coding adoption trends.
    time_series: list of dicts with keys [period, agent, human, total]
    Returns a multi-line string summarizing findings.
    """
    if not time_series:
        return "No trend data available to summarize."

    # Overall totals
    total_commits = sum(entry.get(total_key, 0) for entry in time_series)
    total_agent = sum(entry.get(agent_key, 0) for entry in time_series)
    total_human = sum(entry.get(human_key, 0) for entry in time_series)
    agent_pct = (100.0 * total_agent / total_commits) if total_commits else 0.0
    human_pct = (100.0 * total_human / total_commits) if total_commits else 0.0

    # Find first and last period
    first_period = time_series[0][period_key]
    last_period = time_series[-1][period_key]

    # Find peak agent usage period
    peak_agent = max(time_series, key=lambda x: x.get(agent_key, 0))
    peak_agent_count = peak_agent.get(agent_key, 0)
    peak_agent_period = peak_agent.get(period_key)

    # Find period with highest agent share
    def agent_share(entry):
        t = entry.get(total_key, 0)
        a = entry.get(agent_key, 0)
        return (a / t) if t else 0.0
    peak_share_entry = max(time_series, key=agent_share)
    peak_share = agent_share(peak_share_entry)
    peak_share_period = peak_share_entry.get(period_key)

    # Trend direction (compare first and last period)
    first_agent = time_series[0].get(agent_key, 0)
    last_agent = time_series[-1].get(agent_key, 0)
    trend = "increased" if last_agent > first_agent else ("decreased" if last_agent < first_agent else "remained stable")

    lines = []
    lines.append(f"AI Coding Trend Analysis Report ({period_label.capitalize()}ly)")
    lines.append(f"Period analyzed: {first_period} to {last_period}")
    lines.append("")
    lines.append(f"Total commits analyzed: {total_commits}")
    lines.append(f"AI-assisted commits: {total_agent} ({agent_pct:.1f}%)")
    lines.append(f"Human-only commits: {total_human} ({human_pct:.1f}%)")
    lines.append("")
    lines.append(f"Peak AI-assisted commits: {peak_agent_count} in {peak_agent_period}")
    lines.append(f"Highest AI share: {peak_share*100:.1f}% in {peak_share_period}")
    lines.append("")
    lines.append(f"AI-assisted commit count has {trend} from first to last period.")
    lines.append("")
    # Optionally, show a simple table of the last 5 periods
    lines.append(f"Recent {period_label}s:")
    lines.append(f"{'Period':<12} {'AI':>6} {'Human':>7} {'Total':>7}  AI Share")
    for entry in time_series[-5:]:
        t = entry.get(total_key, 0)
        a = entry.get(agent_key, 0)
        h = entry.get(human_key, 0)
        share = (a / t * 100) if t else 0.0
        lines.append(f"{entry.get(period_key, ''):<12} {a:>6} {h:>7} {t:>7}  {share:5.1f}%")
    return "\n".join(lines)
