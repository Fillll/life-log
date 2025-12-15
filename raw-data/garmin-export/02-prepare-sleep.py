#!/usr/bin/env python3
"""Extract and process Garmin sleep data."""

import argparse
from pathlib import Path
import sys

import pandas as pd

# Add anal/utils directory to path to import utils
sys.path.insert(0, str(Path(__file__).parent.parent.parent / 'anal'))

from utils.garmin_utils import load_garmin_sleep


def main(args):
    """Main execution function."""
    garmin_path = Path(args.garmin_path)
    output_path = Path(args.output)

    print("Loading Garmin sleep data...")
    df_sleep = load_garmin_sleep(garmin_path, timezone_offset_hours=args.timezone_offset)
    print(f"Loaded {len(df_sleep)} sleep records (timezone offset: {args.timezone_offset:+d}h)")

    print("Calculating sleep duration...")
    df_sleep['sleep_duration_h'] = (
        df_sleep['sleep_end'] - df_sleep['sleep_start']
    ).dt.total_seconds() / 3600

    print(f"Saving sleep data to {output_path}")
    output_path.parent.mkdir(parents=True, exist_ok=True)
    df_sleep.to_csv(output_path, sep='\t', index=False)

    if args.verbose:
        print("\nData Summary:")
        print(f"Date range: {df_sleep['date'].min()} to {df_sleep['date'].max()}")
        print(f"Total records: {len(df_sleep)}")
        print(f"Columns: {list(df_sleep.columns)}")
        print("\nSleep duration statistics (hours):")
        print(df_sleep['sleep_duration_h'].describe())
        print("\nFirst few rows:")
        print(df_sleep.head())


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description='Extract and process Garmin sleep data'
    )
    parser.add_argument(
        '--garmin-path',
        default='./data/',
        help='Path to Garmin data directory (default: ./data/)'
    )
    parser.add_argument(
        '--output',
        default='../../data/my_garmin_sleep.tsv',
        help='Output TSV file path (default: ../../data/my_garmin_sleep.tsv)'
    )
    parser.add_argument(
        '--verbose',
        action='store_true',
        help='Print summary statistics'
    )
    parser.add_argument(
        '--timezone-offset',
        type=int,
        default=-5,
        help='Timezone offset from GMT in hours (default: -5 for US Eastern)'
    )

    args = parser.parse_args()
    main(args)
