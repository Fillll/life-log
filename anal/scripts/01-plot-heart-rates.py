#!/usr/bin/env python3
"""Plot Garmin heart rate data with calendar visualizations."""

import argparse
from pathlib import Path
import sys

import pandas as pd
import matplotlib.pyplot as plt
import calplot

# Add parent directory to path to import utils
sys.path.insert(0, str(Path(__file__).parent.parent))

from utils.colormap_utils import create_resting_hr_colormap, create_general_hr_colormap


def main(args):
    """Main execution function."""
    input_path = Path(args.input)

    print(f"Loading data from {input_path}")
    df = pd.read_csv(input_path, sep='\t', parse_dates=['date'])

    if args.verbose:
        print(f"Data range: {df['date'].min()} to {df['date'].max()}")
        print(f"Total days: {len(df)}")
        print("\nHeart rate statistics:")
        for col in ['min_hr', 'min_avg_hr', 'max_avg_hr', 'max_hr', 'resting_hr']:
            if col in df.columns:
                print(f"\n{col}:")
                print(df[col].describe())

    # Define metrics to plot
    metrics = [
        ('min_hr', 'Minimum Heart Rate', create_general_hr_colormap()),
        ('min_avg_hr', 'Minimum Average Heart Rate', create_general_hr_colormap()),
        ('max_avg_hr', 'Maximum Average Heart Rate', create_general_hr_colormap()),
        ('max_hr', 'Maximum Heart Rate', create_general_hr_colormap()),
        ('resting_hr', 'Resting Heart Rate', create_resting_hr_colormap())
    ]

    for metric_col, metric_title, colormap in metrics:
        if metric_col not in df.columns:
            print(f"Warning: {metric_col} not found in data, skipping...")
            continue

        # Skip if no data
        if df[metric_col].isna().all():
            print(f"Warning: No data for {metric_col}, skipping...")
            continue

        print(f"Creating calendar visualization for {metric_title}...")
        hr_series = pd.Series(df[metric_col].values, index=pd.to_datetime(df['date']))

        # Set vmax based on metric type
        if metric_col == 'resting_hr':
            vmax = 150
        else:
            vmax = 220

        if args.verbose:
            print(f"  Data range: {hr_series.min():.0f} - {hr_series.max():.0f}")

        fig = plt.figure(figsize=(16, 10))
        calplot.calplot(
            hr_series,
            textformat='{:.0f}',
            textcolor='#999999',
            cmap=colormap,
            linewidth=0.0005,
            edgecolor='white',
            vmin=0,
            vmax=vmax
        )
        plt.suptitle(metric_title, fontsize=20, y=0.98)

        # Determine output filename
        if args.output_prefix:
            output_file = f"{args.output_prefix}_{metric_col}.png"
            plt.savefig(output_file, bbox_inches='tight', dpi=100)
            print(f"Saved {metric_title} to {output_file}")

        if args.show_plot:
            plt.show()
        else:
            plt.close()


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description='Plot Garmin heart rate data with calendar visualizations'
    )
    parser.add_argument(
        '--input',
        default='../../data/my_garmin_data.tsv',
        help='Input TSV file from 01-prepare-steps (default: ../../data/my_garmin_data.tsv)'
    )
    parser.add_argument(
        '--output-prefix',
        help='Output file prefix for PNG files (e.g., "hr" creates hr_min_hr.png, hr_max_hr.png, etc.)'
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
