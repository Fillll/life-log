#!/usr/bin/env python3
"""Extract and process Garmin stress data."""

import argparse
from pathlib import Path
import sys

import pandas as pd

# Add anal/utils directory to path to import utils
sys.path.insert(0, str(Path(__file__).parent.parent.parent / 'anal'))

from utils.garmin_utils import load_garmin_stress


def main(args):
    """Main execution function."""
    garmin_path = Path(args.garmin_path)
    output_path = Path(args.output)

    print("Loading Garmin stress data...")
    df_stress = load_garmin_stress(garmin_path)
    print(f"Loaded {len(df_stress)} stress records")

    # Fill missing dates with zero (or we could use NaN)
    if not df_stress.empty:
        print("Filling missing dates...")
        date_range = pd.date_range(
            start=df_stress['date'].min(),
            end=df_stress['date'].max(),
            freq='D'
        )
        all_dates = pd.DataFrame({'date': date_range.date})
        df_stress = all_dates.merge(df_stress, on='date', how='left')

    print(f"Saving stress data to {output_path}")
    output_path.parent.mkdir(parents=True, exist_ok=True)
    df_stress.to_csv(output_path, sep='\t', index=False)

    if args.verbose:
        print("\nData Summary:")
        print(f"Date range: {df_stress['date'].min()} to {df_stress['date'].max()}")
        print(f"Total records: {len(df_stress)}")
        print(f"Records with stress data: {df_stress['avg_stress_level'].notna().sum()}")
        print(f"Columns: {list(df_stress.columns)}")
        print("\nAverage stress level statistics:")
        print(df_stress['avg_stress_level'].describe())
        print("\nFirst few rows:")
        print(df_stress.head(10))


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description='Extract and process Garmin stress data'
    )
    parser.add_argument(
        '--garmin-path',
        default='./data/',
        help='Path to Garmin data directory (default: ./data/)'
    )
    parser.add_argument(
        '--output',
        default='../../data/my_garmin_stress.tsv',
        help='Output TSV file path (default: ../../data/my_garmin_stress.tsv)'
    )
    parser.add_argument(
        '--verbose',
        action='store_true',
        help='Print summary statistics'
    )

    args = parser.parse_args()
    main(args)
