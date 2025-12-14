#!/usr/bin/env python3
"""Extract and process Garmin activities/exercise data."""

import argparse
from pathlib import Path
import sys

import pandas as pd

# Add anal/utils directory to path to import utils
sys.path.insert(0, str(Path(__file__).parent.parent.parent / 'anal'))

from utils.garmin_utils import load_garmin_activities


def main(args):
    """Main execution function."""
    garmin_path = Path(args.garmin_path)
    output_path = Path(args.output)

    print("Loading Garmin activities data...")
    df_activities = load_garmin_activities(garmin_path)
    print(f"Loaded {len(df_activities)} activity records")

    print("Calculating daily activity counts...")
    # Count activities per day
    daily_activities = df_activities.groupby('date').size().reset_index(name='activity_count')

    print(f"Saving activities data to {output_path}")
    output_path.parent.mkdir(parents=True, exist_ok=True)
    daily_activities.to_csv(output_path, sep='\t', index=False)

    if args.verbose:
        print("\nData Summary:")
        print(f"Date range: {daily_activities['date'].min()} to {daily_activities['date'].max()}")
        print(f"Total days with activities: {len(daily_activities)}")
        print(f"Total activities: {len(df_activities)}")
        print(f"Columns: {list(daily_activities.columns)}")
        print("\nActivity count statistics:")
        print(daily_activities['activity_count'].describe())
        print("\nActivity types:")
        print(df_activities['activity_type'].value_counts().head(10))
        print("\nFirst few rows:")
        print(daily_activities.head())


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description='Extract and process Garmin activities/exercise data'
    )
    parser.add_argument(
        '--garmin-path',
        default='./data/',
        help='Path to Garmin data directory (default: ./data/)'
    )
    parser.add_argument(
        '--output',
        default='../../data/my_garmin_activities.tsv',
        help='Output TSV file path (default: ../../data/my_garmin_activities.tsv)'
    )
    parser.add_argument(
        '--verbose',
        action='store_true',
        help='Print summary statistics'
    )

    args = parser.parse_args()
    main(args)
