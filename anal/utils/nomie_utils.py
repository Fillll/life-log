from pathlib import Path
import pandas as pd
import json
import re


# Tracker name to emoji mapping
TRACKER_EMOJI_MAP = {
    'beer': '🍺',
    'wine': '🍷',
    'champagne': '🥂',
    'coctail': '🍸',
    'cocktail': '🍸',
    'shot': '🥃',
    'cigar': '🚬',
}


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

        # Parse notes field to extract tracker and value
        if 'notes' in df.columns:
            parsed = df['notes'].apply(_parse_notes)
            df['tracker'] = parsed.apply(lambda x: x[0])
            df['value'] = parsed.apply(lambda x: x[1])
            df['emoji'] = df['tracker'].map(TRACKER_EMOJI_MAP)

    else:
        # Assume CSV (DailyNomie export format)
        df = pd.read_csv(nomie_file)

    # Parse dates - handle both timestamp formats
    if 'start' in df.columns:
        # Try epoch milliseconds first
        try:
            df['date'] = pd.to_datetime(df['start'], unit='ms')
        except (ValueError, TypeError):
            # If that fails, try parsing as string
            df['date'] = pd.to_datetime(df['start'])

        df['date'] = df['date'].dt.floor('D')
        df['year'] = df['date'].dt.to_period('Y')

    return df


def _parse_notes(notes: str) -> tuple:
    """Parse Nomie notes field to extract tracker and value.

    Args:
        notes: Notes string like ' \n#beer(1)' or '#wine(2)'

    Returns:
        Tuple of (tracker_name, value)
    """
    if not notes or not isinstance(notes, str):
        return (None, None)

    # Match pattern like #tracker(value)
    match = re.search(r'#(\w+)\((\d+(?:\.\d+)?)\)', notes)
    if match:
        return (match.group(1), float(match.group(2)))

    return (None, None)


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
