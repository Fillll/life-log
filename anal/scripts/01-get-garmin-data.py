#!/usr/bin/env python3
"""Extract and combine Garmin steps and sleep data."""

import argparse
from pathlib import Path
import sys

import pandas as pd

# Add parent directory to path to import utils
sys.path.insert(0, str(Path(__file__).parent.parent))

from utils.garmin_utils import load_garmin_steps, load_garmin_sleep


def main(args):
    """Main execution function."""
    garmin_path = Path(args.garmin_path)
    output_path = Path(args.output)

    print("Loading Garmin steps data...")
    df_steps = load_garmin_steps(garmin_path)
    print(f"Loaded {len(df_steps)} step records")

    print("Loading Garmin sleep data...")
    df_sleep = load_garmin_sleep(garmin_path)
    print(f"Loaded {len(df_sleep)} sleep records")

    print("Merging datasets...")
    df = pd.merge(df_steps, df_sleep, on='date', how='left')

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
        default='../../raw-data/garmin/',
        help='Path to Garmin data directory (default: ../../raw-data/garmin/)'
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

    args = parser.parse_args()
    main(args)
