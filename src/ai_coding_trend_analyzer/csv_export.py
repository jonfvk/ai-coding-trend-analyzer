import csv
from typing import List, Dict, Any, Optional

def export_trend_data_as_csv(
    time_series: List[Dict[str, Any]],
    filepath: str,
    fieldnames: Optional[List[str]] = None
) -> None:
    """
    Exports time-series trend data to a CSV file.
    time_series: list of dicts, each with keys like 'period', 'total', 'agent', 'human'.
    filepath: path to write the CSV file.
    fieldnames: optional list of column names. If None, uses keys from first entry.
    """
    if not time_series:
        raise ValueError("No data to export.")
    if fieldnames is None:
        # Use all keys from first entry, sorted for consistency
        fieldnames = list(sorted(time_series[0].keys()))
    with open(filepath, 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for entry in time_series:
            # Only include specified fields
            row = {k: entry.get(k, '') for k in fieldnames}
            writer.writerow(row)
