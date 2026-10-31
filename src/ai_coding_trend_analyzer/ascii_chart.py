from typing import List, Dict, Optional

def plot_ascii_trend(
    time_series: List[Dict],
    agent_key: str = 'agent',
    human_key: str = 'human',
    total_key: str = 'total',
    period_key: str = 'period',
    width: int = 60,
    height: int = 12,
    show_legend: bool = True,
    show_total: bool = False,
    label_truncate: int = 8,
    ) -> str:
    """
    Plots an ASCII chart of agent vs human commit counts over time.
    time_series: list of dicts with keys [period, agent, human, total]
    Returns a string containing the ASCII chart.
    """
    if not time_series:
        return "No data to plot."
    # Extract series
    periods = [entry[period_key] for entry in time_series]
    agent_counts = [entry.get(agent_key, 0) for entry in time_series]
    human_counts = [entry.get(human_key, 0) for entry in time_series]
    if show_total:
        total_counts = [entry.get(total_key, 0) for entry in time_series]
    # Determine y-axis range
    max_count = max(
        max(agent_counts, default=0),
        max(human_counts, default=0),
        max(total_counts if show_total else [0], default=0)
    )
    if max_count == 0:
        return "All counts are zero."
    # Downsample if too many periods
    n = len(periods)
    if n > width:
        step = max(1, n // width)
        indices = list(range(0, n, step))
        periods = [periods[i] for i in indices]
        agent_counts = [agent_counts[i] for i in indices]
        human_counts = [human_counts[i] for i in indices]
        if show_total:
            total_counts = [total_counts[i] for i in indices]
    # Build chart grid (height rows, width columns)
    chart = [[' ' for _ in range(len(periods))] for _ in range(height)]
    def scale(val):
        return int(round((val / max_count) * (height - 1)))
    # Plot agent (use '*'), human (use '+'), total (use '#')
    for i, (a, h) in enumerate(zip(agent_counts, human_counts)):
        ay = scale(a)
        hy = scale(h)
        if show_total:
            ty = scale(total_counts[i])
            chart[height - 1 - ty][i] = '#'
        chart[height - 1 - ay][i] = '*'
        chart[height - 1 - hy][i] = '+' if chart[height - 1 - hy][i] == ' ' else chart[height - 1 - hy][i]
    # Build y-axis labels
    y_labels = []
    for row in range(height):
        val = int(round(max_count * (height - 1 - row) / (height - 1)))
        y_labels.append(f"{val:>4}")
    # Build lines
    lines = []
    for y, row in zip(y_labels, chart):
        lines.append(f"{y} | {''.join(row)}")
    # X-axis
    lines.append("     +" + '-' * len(periods))
    # X labels (truncate for width)
    label_line = [' ' for _ in range(len(periods))]
    for i, p in enumerate(periods):
        label = p[-label_truncate:] if len(p) > label_truncate else p
        if label_truncate >= 3:
            label = label[-label_truncate:]
        # Place only first char of label to avoid overlap
        label_line[i] = label[0]
    lines.append("     " + ''.join(label_line))
    # Legend
    if show_legend:
        legend = ["Legend:", "  * = Agent commits", "  + = Human commits"]
        if show_total:
            legend.append("  # = Total commits")
        lines.extend(legend)
    return '\n'.join(lines)
