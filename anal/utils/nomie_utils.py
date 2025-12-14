from pathlib import Path
import pandas as pd


def load_nomie_data(nomie_file: Path) -> pd.DataFrame:
    """Load Nomie export CSV and prepare for analysis.

    Args:
        nomie_file: Path to Nomie CSV export

    Returns:
        DataFrame with columns: date, year, emoji, value, tracker, etc.
    """
    df = pd.read_csv(nomie_file)

    # Parse dates
    df['date'] = df.apply(lambda row: pd.to_datetime(row['start']).floor('D'), axis=1)
    df['year'] = df.apply(lambda row: pd.to_datetime(row['start']).to_period('Y'), axis=1)

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
