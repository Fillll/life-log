#!/usr/bin/env python3
"""Extract and combine Garmin steps and sleep data."""

import argparse
from pathlib import Path
import sys

import pandas as pd

# Add anal/utils directory to path to import utils
sys.path.insert(0, str(Path(__file__).parent.parent.parent / 'anal'))

from utils.garmin_utils import load_garmin_steps, load_garmin_sleep


def main(args):
    """Main execution function."""
    garmin_path = Path(args.garmin_path)
    output_path = Path(args.output)

    print("Loading Garmin steps data...")
    df_steps = load_garmin_steps(garmin_path)
    print(f"Loaded {len(df_steps)} step records")

    print("Loading Garmin sleep data...")
    tz_offset = None if args.timezone_offset == 'auto' else int(args.timezone_offset)
    df_sleep = load_garmin_sleep(garmin_path, timezone_offset_hours=tz_offset)
    if tz_offset is None:
        print(f"Loaded {len(df_sleep)} sleep records (timezone: auto-detect Moscow/DC)")
    else:
        print(f"Loaded {len(df_sleep)} sleep records (timezone offset: {tz_offset:+d}h)")

    print("Merging datasets...")
    if df_steps.empty and df_sleep.empty:
        print("Error: No data found in either steps or sleep data")
        return
    elif df_steps.empty:
        df = df_sleep
    elif df_sleep.empty:
        df = df_steps
    else:
        df = pd.merge(df_steps, df_sleep, on='date', how='outer')

    # Convert floors from meters to floor count (1 floor ≈ 3 meters)
    if 'floors_ascended_m' in df.columns:
        df['floors_climbed'] = df['floors_ascended_m'] / 3.0
        print(f"Converted floors from meters to floor count")

    print(f"Saving combined data to {output_path}")
    output_path.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(output_path, sep='\t', index=False)

    if args.verbose:
        print("\nData Summary:")
        print(f"Date range: {df['date'].min()} to {df['date'].max()}")
        print(f"Total records: {len(df)}")
        print(f"Columns: {list(df.columns)}")
        print("\nFirst few rows:")
        print(df.head())


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description='Extract and combine Garmin steps and sleep data'
    )
    parser.add_argument(
        '--garmin-path',
        default='./data/',
        help='Path to Garmin data directory (default: ./data/)'
    )
    parser.add_argument(
        '--output',
        default='../../data/my_garmin_data.tsv',
        help='Output TSV file path (default: ../../data/my_garmin_data.tsv)'
    )
    parser.add_argument(
        '--verbose',
        action='store_true',
        help='Print summary statistics'
    )
    parser.add_argument(
        '--timezone-offset',
        default='auto',
        help='Timezone offset from GMT in hours, or "auto" to detect Moscow/DC transition (default: auto)'
    )

    args = parser.parse_args()
    main(args)
