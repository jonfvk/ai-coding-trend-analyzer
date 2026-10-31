from typing import List, Dict, Literal, Any
from datetime import datetime
from .aggregation import aggregate_commits_by_period

def generate_time_series(
    commit_data: List[Dict[str, Any]],
    period: Literal['week', 'month'] = 'week',
    timestamp_key: str = 'timestamp',
    agent_key: str = 'agent_keyword_found',
) -> List[Dict[str, Any]]:
    """
    Generates time-series data from aggregated commit info.
    Returns a list of dicts sorted by period key (chronological order):
        [
            {
                'period': '2024-W18',
                'total': 5,
                'agent': 2,
                'human': 3
            },
            ...
        ]
    """
    agg = aggregate_commits_by_period(
        commit_data,
        period=period,
        timestamp_key=timestamp_key,
        agent_key=agent_key
    )
    # Sort period keys chronologically
    def _period_sort_key(key: str) -> Any:
        if period == 'week':
            # Format: YYYY-Www
            try:
                year, week = key.split('-W')
                return (int(year), int(week))
            except Exception:
                return (9999, 99)
        else:
            # Format: YYYY-MM
            try:
                year, month = key.split('-')
                return (int(year), int(month))
            except Exception:
                return (9999, 99)
    sorted_keys = sorted(agg.keys(), key=_period_sort_key)
    result = []
    for key in sorted_keys:
        entry = {'period': key}
        entry.update(agg[key])
        result.append(entry)
    return result
