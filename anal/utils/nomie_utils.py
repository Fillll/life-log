from pathlib import Path
import pandas as pd
import json


def load_nomie_data(nomie_file: Path) -> pd.DataFrame:
    """Load Nomie export (JSON or CSV) and prepare for analysis.

    Args:
        nomie_file: Path to Nomie JSON or CSV export

    Returns:
        DataFrame with columns: date, year, emoji, value, tracker, etc.
    """
    nomie_file = Path(nomie_file)

    # Load based on file extension
    if nomie_file.suffix == '.json':
        with open(nomie_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
        df = pd.DataFrame(data)
    else:
        # Assume CSV
        df = pd.read_csv(nomie_file)

    # Parse dates - handle both timestamp formats
    if 'start' in df.columns:
        # Convert start column (could be epoch milliseconds or ISO string)
        df['date'] = pd.to_datetime(df['start'], unit='ms', errors='ignore')
        # If that didn't work, try parsing as string
        if df['date'].isna().all():
            df['date'] = pd.to_datetime(df['start'])
        df['date'] = df['date'].dt.floor('D')
        df['year'] = df['date'].dt.to_period('Y')

    return df


def filter_alcohol_substances(df: pd.DataFrame) -> pd.DataFrame:
    """Filter Nomie data for alcohol/substance emojis.

    Args:
        df: Nomie DataFrame

    Returns:
        Filtered DataFrame with only alcohol/substance entries
    """
    alcohol_emojis = ['🍺', '🥂', '🍷', '🥃', '🚬', '🍸']
    return df[df['emoji'].isin(alcohol_emojis)]


def get_daily_counts(df: pd.DataFrame) -> pd.Series:
    """Get daily count of tracked items.

    Args:
        df: Nomie DataFrame (potentially filtered)

    Returns:
        Pandas Series with date index and counts
    """
    daily_counts = df.groupby(['date']).count().reset_index()[['date', 'tracker']]
    return pd.Series(daily_counts['tracker'].values, index=daily_counts['date'])
