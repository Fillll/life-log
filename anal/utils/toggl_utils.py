import os
from pathlib import Path
import pandas as pd


def parse_duration(duration_string: str) -> float:
    """Parse Toggl duration format (HH:MM:SS) to hours.

    Args:
        duration_string: Duration in format 'HH:MM:SS'

    Returns:
        Duration in hours as float
    """
    elements = duration_string.split(':')
    duration = int(elements[0]) + int(elements[1]) / 60 + int(elements[2]) / (60 * 60)
    return duration


def load_toggl_hours(toggl_path: Path, clients_exclude=None, clients_include=None) -> pd.DataFrame:
    """Load Toggl time tracking data and aggregate to daily hours.

    Args:
        toggl_path: Path to toggl directory with CSV files
        clients_exclude: List of client names to exclude (optional)
        clients_include: List of client names to include only (optional)

    Returns:
        DataFrame with columns: date, duration_h
    """
    toggl_files = sorted([
        os.path.join(toggl_path, f)
        for f in os.listdir(toggl_path)
        if f.startswith('Toggl')
    ])

    all_dates_business_hours = pd.DataFrame()

    for each_toggl_year_file in toggl_files:
        df = pd.read_csv(each_toggl_year_file, parse_dates=['Start date'])

        # Filter clients
        if 'Client' in df.columns:
            # Always filter out clients starting with "~"
            df = df[~df['Client'].astype(str).str.startswith('~')]

            # Apply include filter if specified
            if clients_include is not None:
                df = df[df['Client'].isin(clients_include)]

            # Apply exclude filter if specified
            if clients_exclude is not None:
                df = df[~df['Client'].isin(clients_exclude)]

        df['duration_h'] = df['Duration'].map(parse_duration)
        duration_each_day = pd.DataFrame(
            df.groupby(['Start date'])['duration_h'].sum()
        ).reset_index()
        duration_each_day = duration_each_day.rename(columns={'Start date': 'date'})
        all_dates_business_hours = pd.concat([all_dates_business_hours, duration_each_day])

    # Normalize durations > 24h
    while all_dates_business_hours.duration_h.max() > 24:
        all_dates_business_hours['duration_h'] = all_dates_business_hours['duration_h'].map(
            lambda x: x - 24 if x > 24 else x
        )

    return all_dates_business_hours
