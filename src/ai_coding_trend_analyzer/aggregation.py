from collections import defaultdict
from datetime import datetime
from typing import List, Dict, Literal, Optional

def _get_week_key(dt: datetime) -> str:
    """
    Returns a string key for the year and ISO week number, e.g. '2024-W18'
    """
    iso_year, iso_week, _ = dt.isocalendar()
    return f"{iso_year}-W{iso_week:02d}"

def _get_month_key(dt: datetime) -> str:
    """
    Returns a string key for the year and month, e.g. '2024-05'
    """
    return f"{dt.year}-{dt.month:02d}"

def aggregate_commits_by_period(
    commit_data: List[Dict],
    period: Literal['week', 'month'] = 'week',
    timestamp_key: str = 'timestamp',
    agent_key: str = 'agent_keyword_found',
) -> Dict[str, Dict[str, int]]:
    """
    Aggregates commit data by week or month.
    commit_data: list of dicts with at least keys [timestamp_key, agent_key]
    period: 'week' or 'month'
    Returns dict mapping period key to dict with counts:
        {
            '2024-W18': {'total': 5, 'agent': 2, 'human': 3},
            ...
        }
    """
    if period not in ('week', 'month'):
        raise ValueError("period must be 'week' or 'month'")
    agg = defaultdict(lambda: {'total': 0, 'agent': 0, 'human': 0})
    for entry in commit_data:
        dt = entry.get(timestamp_key)
        if not isinstance(dt, datetime):
            continue  # skip malformed
        if period == 'week':
            key = _get_week_key(dt)
        else:
            key = _get_month_key(dt)
        agg[key]['total'] += 1
        if entry.get(agent_key):
            agg[key]['agent'] += 1
        else:
            agg[key]['human'] += 1
    return dict(agg)
