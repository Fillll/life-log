#!/usr/bin/env python3
"""Plot sleep start and wake times with calendar visualizations."""

import argparse
from pathlib import Path
import sys

import pandas as pd
import matplotlib.pyplot as plt
import calplot

# Add parent directory to path to import utils
sys.path.insert(0, str(Path(__file__).parent.parent))

from utils.colormap_utils import create_bedtime_colormap, create_waketime_colormap


def extract_hour_decimal(dt_series):
    """Extract hour as decimal from datetime series.

    Args:
        dt_series: Pandas datetime series

    Returns:
        Series with hours as decimals (e.g., 22.5 for 22:30)
    """
    return dt_series.dt.hour + dt_series.dt.minute / 60.0


def main(args):
    """Main execution function."""
    input_path = Path(args.input)

    print(f"Loading data from {input_path}")
    df = pd.read_csv(input_path, sep='\t', parse_dates=['date', 'sleep_start', 'sleep_end'])

    # Extract hours from sleep times
    df['bedtime_hour'] = extract_hour_decimal(df['sleep_start'])
    df['waketime_hour'] = extract_hour_decimal(df['sleep_end'])

    if args.verbose:
        print(f"Data range: {df['date'].min()} to {df['date'].max()}")
        print(f"Total days: {len(df)}")
        print(f"Days with sleep data: {df['sleep_start'].notna().sum()}")
        print("\nBedtime statistics:")
        print(df['bedtime_hour'].describe())
        print("\nWake time statistics:")
        print(df['waketime_hour'].describe())

    # Visualize bedtime (sleep start)
    print("Creating bedtime calendar visualization...")
    bedtime_series = pd.Series(df['bedtime_hour'].values, index=pd.to_datetime(df['date']))
    bedtime_cmap = create_bedtime_colormap()

    fig = plt.figure(figsize=(16, 10))
    calplot.calplot(
        bedtime_series,
        textformat='{:.0f}',
        textcolor='#999999',
        cmap=bedtime_cmap,
        linewidth=0.0005,
        edgecolor='white',
        vmin=0,
        vmax=24
    )

    if args.output_bedtime:
        plt.savefig(args.output_bedtime, bbox_inches='tight', dpi=100)
        print(f"Saved bedtime calendar to {args.output_bedtime}")

    if args.show_plot:
        plt.show()
    else:
        plt.close()

    # Visualize wake time (sleep end)
    print("Creating wake time calendar visualization...")
    waketime_series = pd.Series(df['waketime_hour'].values, index=pd.to_datetime(df['date']))
    waketime_cmap = create_waketime_colormap()

    fig = plt.figure(figsize=(16, 10))
    calplot.calplot(
        waketime_series,
        textformat='{:.0f}',
        textcolor='#999999',
        cmap=waketime_cmap,
        linewidth=0.0005,
        edgecolor='white',
        vmin=0,
        vmax=24
    )

    if args.output_waketime:
        plt.savefig(args.output_waketime, bbox_inches='tight', dpi=100)
        print(f"Saved wake time calendar to {args.output_waketime}")

    if args.show_plot:
        plt.show()
    else:
        plt.close()


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description='Plot sleep start and wake times with calendar visualizations'
    )
    parser.add_argument(
        '--input',
        default='../../data/my_garmin_data.tsv',
        help='Input TSV file from 01-prepare-steps (default: ../../data/my_garmin_data.tsv)'
    )
    parser.add_argument(
        '--output-bedtime',
        help='Output PNG for bedtime calendar plot (default: no save)'
    )
    parser.add_argument(
        '--output-waketime',
        help='Output PNG for wake time calendar plot (default: no save)'
    )
    parser.add_argument(
        '--show-plot',
        action='store_true',
        help='Display plots instead of saving'
    )
    parser.add_argument(
        '--verbose',
        action='store_true',
        help='Print analysis summary'
    )

    args = parser.parse_args()
    main(args)
